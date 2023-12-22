from utilities import *
 
window_size = 20 
step_size = window_size
all_subdirs = os.listdir()
maxoffset = 0.005 
label_dict = {"D": 0, "NF": 0, "I": 0, "NM": 0}
num_inflections = dict()
num_x_inflections = dict()
num_y_inflections = dict()
num_label_inflections = dict()
x_y_infls = []
x_y_infl_long_trajs = dict()
x_y_infl_lat_trajs = dict()
x_y_infl_id_trajs = dict()
cross_myself = []
crossings_dict = dict() 
identifier = [] 
offlens = []
offlens_for_inc = []
tss = []
ts_I = []
maxx = 0
minx = -10000
for subdir_name in all_subdirs: 
    trajs_in_dir = 0 
    if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
        continue
    if not os.path.isdir(subdir_name + "/cleaned_csv/"):
        os.makedirs(subdir_name + "/cleaned_csv/")  
    all_files = os.listdir(subdir_name + "/cleaned_csv/") 
    bad_rides_filenames = set()
    if os.path.isfile(subdir_name + "/bad_rides_filenames"):
        bad_rides_filenames = load_object(subdir_name + "/bad_rides_filenames")
    gap_rides_filenames = set()
    if os.path.isfile(subdir_name + "/gap_rides_filenames"):
        gap_rides_filenames = load_object(subdir_name + "/gap_rides_filenames") 
    for some_file in all_files:  
        if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames:
            #print("Skipped ride", some_file)
            continue
        #print("Used ride", some_file) 
        only_num_ride = some_file.replace(".csv", "").replace("events_", "")  
        trajs_in_ride = 0 
        file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
        longitudes = list(file_with_ride["fields_longitude"])
        latitudes = list(file_with_ride["fields_latitude"])   
        for x in range(0, len(longitudes) - window_size + 1, step_size): 
            longitudes_tmp = longitudes[x:x + window_size]
            latitudes_tmp = latitudes[x:x + window_size]  
            set_longs = set()
            set_lats = set()
            set_points = set()
            for tmp_long in longitudes_tmp:
                set_longs.add(tmp_long)
            for tmp_lat in latitudes_tmp:
                set_lats.add(tmp_lat)
            for some_index in range(len(latitudes_tmp)):
                set_points.add((latitudes_tmp[some_index], longitudes_tmp[some_index])) 
            if len(set_lats) == 1 or len(set_longs) == 1:
                continue
            if len(set_points) < 3:
                continue 
            longitudes_tmp_transform, latitudes_tmp_transform = preprocess_long_lat(longitudes_tmp, latitudes_tmp)
            longitudes_scaled_to_max, latitudes_scaled_to_max = scale_long_lat(longitudes_tmp_transform, latitudes_tmp_transform, xmax = maxoffset, ymax = maxoffset, keep_aspect_ratio = True)
            sum_dist, offset_total = traj_len_offset(longitudes_scaled_to_max, latitudes_scaled_to_max)
            ts = total_surf(longitudes_scaled_to_max, latitudes_scaled_to_max)
            tss.append(ts) 
            offlens.append(sum_dist / offset_total)
            long_sgns = [longitudes_scaled_to_max[long_ind + 1] > longitudes_scaled_to_max[long_ind] for long_ind in range(len(longitudes_tmp_transform) - 1)]
            long_sgns_change = [long_sgns[long_ind + 1] == long_sgns[long_ind] for long_ind in range(len(long_sgns) - 1)]
            long_sgn = set(long_sgns)  
            lat_sgns = [latitudes_scaled_to_max[lat_ind + 1] > latitudes_scaled_to_max[lat_ind] for lat_ind in range(len(latitudes_tmp_transform) - 1)]
            lat_sgns_change = [lat_sgns[lat_ind + 1] == lat_sgns[lat_ind] for lat_ind in range(len(lat_sgns) - 1)]
            lat_sgn = set(lat_sgns)

            crossings = 0
            crossing_positions = []

            for pos1 in range(len(longitudes_scaled_to_max) - 1):
                for pos2 in range(pos1 + 2, len(longitudes_scaled_to_max) - 1):
                    xs, ys = get_intersection(longitudes_scaled_to_max[pos1], longitudes_scaled_to_max[pos1 + 1], latitudes_scaled_to_max[pos1], latitudes_scaled_to_max[pos1 + 1], longitudes_scaled_to_max[pos2], longitudes_scaled_to_max[pos2 + 1], latitudes_scaled_to_max[pos2], latitudes_scaled_to_max[pos2 + 1])
                    if xs != "Nan":
                        pol1 = point_on_line(xs, ys, longitudes_scaled_to_max[pos1], longitudes_scaled_to_max[pos1 + 1], latitudes_scaled_to_max[pos1], latitudes_scaled_to_max[pos1 + 1]) 
                        pol2 = point_on_line(xs, ys, longitudes_scaled_to_max[pos2], longitudes_scaled_to_max[pos2 + 1], latitudes_scaled_to_max[pos2], latitudes_scaled_to_max[pos2 + 1])

                        if pol1 and pol2:    
                            crossings += 1
                            crossing_positions.append((xs, ys))
  
            if crossings not in crossings_dict:
                crossings_dict[crossings] = 0
            crossings_dict[crossings] += 1
            cross_myself.append(crossings)

            total_infls = set()
            infls_long = []
            for long_ind in range(len(long_sgns_change)):
                if not long_sgns_change[long_ind]:
                    infls_long.append(long_ind + 1)
                    total_infls.add(long_ind + 1)
            infls_lat = []
            for lat_ind in range(len(lat_sgns_change)):
                if not lat_sgns_change[lat_ind]:
                    infls_lat.append(lat_ind + 1)
                    total_infls.add(lat_ind + 1) 
  
            if len(infls_long) not in num_x_inflections:
                num_x_inflections[len(infls_long)] = 0
            num_x_inflections[len(infls_long)] += 1

            if len(infls_lat) not in num_y_inflections:
                num_y_inflections[len(infls_lat)] = 0
            num_y_inflections[len(infls_lat)] += 1
 
            if len(total_infls) not in num_inflections:
                num_inflections[len(total_infls)] = 0
            num_inflections[len(total_infls)] += 1 

            labelm = str(len(total_infls)) + "_"
            if len(infls_lat) > len(infls_long):
                labelm += str(len(infls_lat)) + "_" + str(len(infls_long))
                x_y_infls.append([len(total_infls), len(infls_lat), len(infls_long)])
                nx = [l for l in longitudes_scaled_to_max]
                ny = [l for l in latitudes_scaled_to_max]
            else:
                labelm += str(len(infls_long)) + "_" + str(len(infls_lat))
                x_y_infls.append([len(total_infls), len(infls_long), len(infls_lat)])
                nx = [l for l in latitudes_scaled_to_max]
                ny = [l for l in longitudes_scaled_to_max]

            if not nx[0] < nx[1]:
                nx = [l - max(nx) for l in nx]
            if not ny[0] < ny[1]:
                ny = [l - max(ny) for l in nx]
            
            labelm += "_" + str(crossings)

            if labelm not in num_label_inflections:
                num_label_inflections[labelm] = 0
            num_label_inflections[labelm] += 1

            if labelm not in x_y_infl_long_trajs:
                x_y_infl_long_trajs[labelm] = []
            x_y_infl_long_trajs[labelm].append(nx)

            if labelm not in x_y_infl_lat_trajs:
                x_y_infl_lat_trajs[labelm] = []
            x_y_infl_lat_trajs[labelm].append(ny)

            if labelm not in x_y_infl_id_trajs:
                x_y_infl_id_trajs[labelm] = []
            x_y_infl_id_trajs[labelm].append([window_size, int(subdir_name.replace("Vehicle_", "")), int(only_num_ride), x])

            if len(lat_sgn) > 1 and len(long_sgn) > 1:
                label = "NF"   
            if (len(lat_sgn) == 1 and len(long_sgn) > 1) or (len(lat_sgn) > 1 and len(long_sgn) == 1):
                label = "NM"   
            if len(lat_sgn) == 1 and len(long_sgn) == 1:
                if (True in lat_sgn and True in long_sgn) or (False in lat_sgn and False in long_sgn):
                    label = "I" 
                    offlens_for_inc.append(sum_dist / offset_total)
                    ts_I.append(ts)
                else:
                    label = "D" 
                    
            label_dict[label] += 1
            
            identifier.append([window_size, int(subdir_name.replace("Vehicle_", "")), int(only_num_ride), x])

print(num_inflections)
print(num_x_inflections)
print(num_y_inflections)

x_y_infls = np.array(x_y_infls) 
#plt.scatter(x_y_infls[:, 0], x_y_infls[:, 1])
#plt.show()
 
def composite_img(long1, lat1, titles, nrow, ncol, filename): 
    plt.rcParams.update({'font.size': 6})
    plt.figure(figsize=(ncol, nrow))
    for row in range(nrow):
        for col in range(ncol):
            ix = row * ncol + col
            plt.subplot(nrow, ncol, ix + 1) 
            plt.axis('off')
            #plt.title(titles[ix])   
            plt.plot(long1[ix], lat1[ix], color = "k")      
    #plt.savefig(filename, bbox_inches = "tight")  
    plt.show()
    plt.close() 

for k in sorted(list(num_label_inflections.keys())): 
    print(k, num_label_inflections[k])
    nrow = 10
    ncol = 10  
    if nrow * ncol > num_label_inflections[k]:
        ncol = int(np.sqrt(num_label_inflections[k]))
        nrow = ncol
    #composite_img(x_y_infl_long_trajs[k][:nrow*ncol], x_y_infl_lat_trajs[k][:nrow*ncol], x_y_infl_id_trajs[k][:nrow*ncol], nrow, ncol, "")

print(num_label_inflections)

print(crossings_dict)
print(min(tss), max(tss))
print(np.quantile(tss, 0.25), np.quantile(tss, 0.5), np.quantile(tss, 0.75), np.quantile(tss, 0.9), np.quantile(tss, 0.95))  
print(min(ts_I), max(ts_I))

print(np.quantile(ts_I, 0.25), np.quantile(ts_I, 0.5), np.quantile(ts_I, 0.75), np.quantile(ts_I, 0.9), np.quantile(ts_I, 0.95)) 
 
print(label_dict)
print(min(offlens), max(offlens))
print(np.quantile(offlens, 0.25), np.quantile(offlens, 0.5), np.quantile(offlens, 0.75), np.quantile(offlens, 0.9), np.quantile(offlens, 0.95))  
print(min(offlens_for_inc), max(offlens_for_inc))
print(np.quantile(offlens_for_inc, 0.25), np.quantile(offlens_for_inc, 0.5), np.quantile(offlens_for_inc, 0.75), np.quantile(offlens_for_inc, 0.9), np.quantile(offlens_for_inc, 0.95)) 