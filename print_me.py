from utilities import *
import seaborn as sns

window_size = 20 
step_size = window_size
all_subdirs = os.listdir()
maxoffset = 0.005 
label_dict = {"D": 0, "NF": 0, "I": 0, "NM": 0}
num_inflections = dict()
num_x_inflections = dict()
num_y_inflections = dict()
num_larger_inflections = dict()
num_smaller_inflections = dict()
num_label_inflections = dict()
x_y_infls = []
x_y_infl_long_trajs = dict()
x_y_infl_lat_trajs = dict()
x_y_infl_id_trajs = dict()
x_y_infl_infl_trajs = dict()
x_y_infl_crossing_trajs = dict()
cross_myself = []
cross_myself_times = []
crossings_dict = dict() 
identifier = [] 
rotatedx = []
rotatedy = []
infl_pos_long = []
infl_pos_lat = []
infl_pos_all = []
infl_pos_longer = []
infl_pos_shorter = []
offlens = []
offlens_for_inc = []
tss = []
ts_I = []
maxx = 0
minx = -10000
maxda = [] 
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
 
            crossing_positions = []

            for pos1 in range(len(longitudes_scaled_to_max) - 1):
                for pos2 in range(pos1 + 2, len(longitudes_scaled_to_max) - 1):
                    xs, ys = get_intersection(longitudes_scaled_to_max[pos1], longitudes_scaled_to_max[pos1 + 1], latitudes_scaled_to_max[pos1], latitudes_scaled_to_max[pos1 + 1], longitudes_scaled_to_max[pos2], longitudes_scaled_to_max[pos2 + 1], latitudes_scaled_to_max[pos2], latitudes_scaled_to_max[pos2 + 1])
                    if xs != "Nan":
                        pol1 = point_on_line(xs, ys, longitudes_scaled_to_max[pos1], longitudes_scaled_to_max[pos1 + 1], latitudes_scaled_to_max[pos1], latitudes_scaled_to_max[pos1 + 1]) 
                        pol2 = point_on_line(xs, ys, longitudes_scaled_to_max[pos2], longitudes_scaled_to_max[pos2 + 1], latitudes_scaled_to_max[pos2], latitudes_scaled_to_max[pos2 + 1])

                        if pol1 and pol2:     
                            crossing_positions.append((xs, ys))
  
            if len(crossing_positions) not in crossings_dict:
                crossings_dict[len(crossing_positions)] = 0
            crossings_dict[len(crossing_positions)] += 1
            cross_myself_times.append(len(crossing_positions))
            ind = len(longitudes_scaled_to_max) - 1
            while longitudes_scaled_to_max[ind] == 0 or latitudes_scaled_to_max[ind] == 0:
                ind -= 1
            a = longitudes_scaled_to_max[ind] / latitudes_scaled_to_max[ind]
            da = []
            for i in range(len(latitudes_scaled_to_max)):
                if longitudes_scaled_to_max[i] == 0 or latitudes_scaled_to_max[i] == 0:
                    continue
                da.append(abs(longitudes_scaled_to_max[i] / latitudes_scaled_to_max[i] - a) / a)
            maxda.append(max(da)) 

            total_infls = set()
            infls_long = set()
            minspace = 0
            for long_ind in range(minspace, len(long_sgns_change) - minspace):
                if not long_sgns_change[long_ind]:
                    found = False
                    if minspace > 0:
                        for k in range(minspace):
                            if long_ind > k and (not long_sgns_change[long_ind - k - 1] or not lat_sgns_change[long_ind - k - 1]):
                                found = True
                                break
                    if found:
                        continue 
                    infls_long.add(long_ind + 1)
                    total_infls.add(long_ind + 1)
            infls_lat = set()
            for lat_ind in range(minspace, len(lat_sgns_change) - minspace):
                if not lat_sgns_change[lat_ind]:
                    found = False
                    if minspace > 0:
                        for k in range(minspace):
                            if lat_ind > k and (not long_sgns_change[lat_ind - k - 1] or not lat_sgns_change[lat_ind - k - 1]):
                                found = True
                                break
                    if found:
                        continue 
                    infls_lat.add(lat_ind + 1)
                    total_infls.add(lat_ind + 1) 
            infls_long = list(infls_long)
            infls_lat = list(infls_lat)
            total_infls = list(total_infls)
            infl_pos_long.append(infls_long)
            infl_pos_lat.append(infls_lat)
            infl_pos_all.append(total_infls)

            #if sum_dist / offset_total < 1.2 or ts < 0.001:
                #crossing_positions = [] 
                #total_infls = []
                #infls_lat = []
                #infls_long = []
  
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
                x_y_infls.append([len(total_infls), len(infls_lat), len(infls_long), len(crossing_positions)])

                if len(infls_lat) not in num_larger_inflections:
                    num_larger_inflections[len(infls_lat)] = 0
                num_larger_inflections[len(infls_lat)] += 1 
                infl_pos_longer.append(infls_lat)
                
                if len(infls_long) not in num_smaller_inflections:
                    num_smaller_inflections[len(infls_long)] = 0
                num_smaller_inflections[len(infls_long)] += 1 
                infl_pos_shorter.append(infls_long)

                nx = [l for l in longitudes_scaled_to_max]
                ny = [l for l in latitudes_scaled_to_max]
                ncross = [(c[0], c[1]) for c in crossing_positions]
            else:
                labelm += str(len(infls_long)) + "_" + str(len(infls_lat))
                x_y_infls.append([len(total_infls), len(infls_long), len(infls_lat), len(crossing_positions)])

                if len(infls_long) not in num_larger_inflections:
                    num_larger_inflections[len(infls_long)] = 0
                num_larger_inflections[len(infls_long)] += 1 
                infl_pos_longer.append(infls_long)
                
                if len(infls_lat) not in num_smaller_inflections:
                    num_smaller_inflections[len(infls_lat)] = 0
                num_smaller_inflections[len(infls_lat)] += 1 
                infl_pos_shorter.append(infls_lat)

                nx = [l for l in latitudes_scaled_to_max]
                ny = [l for l in longitudes_scaled_to_max]
                ncross = [(c[1], c[0]) for c in crossing_positions]

            if not nx[0] < nx[1]:
                nx = [max(nx) - l for l in nx]
                ncross = [(max(nx) - c[0], c[1]) for c in ncross]
            if not ny[0] < ny[1]:
                ny = [max(ny) - l for l in ny]
                ncross = [(c[0], max(ny) - c[1]) for c in ncross]
            
            labelm += "_" + str(len(crossing_positions))

            if labelm not in num_label_inflections:
                num_label_inflections[labelm] = 0
            num_label_inflections[labelm] += 1

            if labelm not in x_y_infl_long_trajs:
                x_y_infl_long_trajs[labelm] = []
            x_y_infl_long_trajs[labelm].append(nx)
            rotatedx.append(nx)

            if labelm not in x_y_infl_lat_trajs:
                x_y_infl_lat_trajs[labelm] = []
            x_y_infl_lat_trajs[labelm].append(ny)
            rotatedy.append(ny)

            if labelm not in x_y_infl_id_trajs:
                x_y_infl_id_trajs[labelm] = []
            x_y_infl_id_trajs[labelm].append([window_size, int(subdir_name.replace("Vehicle_", "")), int(only_num_ride), x])
            identifier.append([window_size, int(subdir_name.replace("Vehicle_", "")), int(only_num_ride), x])
             
            color_infl = []
            for infl in total_infls: 
                if infl in infls_lat and infl in infls_long:
                    color_infl.append(2)
                    continue
                if len(infls_lat) > len(infls_long):
                    color_infl.append(int(infl in infls_lat))
                else:
                    color_infl.append(int(infl in infls_long))

            if labelm not in x_y_infl_infl_trajs:
                x_y_infl_infl_trajs[labelm] = []
            x_y_infl_infl_trajs[labelm].append([total_infls, color_infl])

            if labelm not in x_y_infl_crossing_trajs:
                x_y_infl_crossing_trajs[labelm] = []
            x_y_infl_crossing_trajs[labelm].append(ncross)
            cross_myself.append(ncross)

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

print(num_inflections)
print(num_x_inflections)
print(num_y_inflections)
print(num_larger_inflections)
print(num_smaller_inflections)

def heatmap_from_arrays(arr, ind1, ind2):
    minx = min(arr[:, ind1])
    miny = min(arr[:, ind2])
    maxx = max(arr[:, ind1])
    maxy = max(arr[:, ind2])
    mtr = []
    for x in range(minx, maxx + 1):
        mtr.append([])
        for y in range(miny, maxy + 1):
            c = 0
            for a in arr:
                if a[ind1] == x and a[ind2] == y:
                    c += 1
            mtr[-1].append(c)
    sns.heatmap(mtr, annot = True)
    plt.show()
 
x_y_infls = np.array(x_y_infls)  
heatmap_from_arrays(x_y_infls, 0, 1)

#plt.scatter(x_y_infls[:, 0], x_y_infls[:, -1])
#plt.show()
 
def composite_img(long1, lat1, titles, nrow, ncol, labelname, infls_mark, cross_mark): 
    #plt.rcParams.update({'font.size': 6})
    #plt.figure(figsize=(ncol, nrow))
    for row in range(nrow):
        for col in range(ncol):
            ix = row * ncol + col
            if ix >= len(long1):
                continue
            #plt.subplot(nrow, ncol, ix + 1) 
            plt.axis('off')
            ws, veh, nr, pos = titles[ix]
            str_title = str(ws) + "_Vehicle_" + str(veh) + "_events_" + str(nr) + "_" + str(pos)
            plt.plot(long1[ix], lat1[ix], color = "k")
            plt.plot([long1[ix][0], long1[ix][-1]], [lat1[ix][0], lat1[ix][-1]], color = "r")
            for c in cross_mark[ix]:
                plt.scatter(c[0], c[1], color = "b")
                
            for ixx, i in enumerate(infls_mark[ix][0]):
                if infls_mark[ix][1][ixx] == 2:
                    plt.scatter(long1[ix][i], lat1[ix][i], color = "g")
                if infls_mark[ix][1][ixx] == 0:
                    plt.scatter(long1[ix][i], lat1[ix][i], color = "orange")
                if infls_mark[ix][1][ixx] == 1:
                    plt.scatter(long1[ix][i], lat1[ix][i], color = "purple")
                    
            if not os.path.isdir("infl_cross/mark/" + labelname):
                os.makedirs("infl_cross/mark/" + labelname)
            #plt.show()
            plt.savefig("infl_cross/mark/" + labelname + "/" + labelname + "_" + str_title + ".png", bbox_inches = "tight")  
            plt.close() 

def composite_img_no_mark(long1, lat1, titles, nrow, ncol, labelname): 
    #plt.rcParams.update({'font.size': 6})
    #plt.figure(figsize=(ncol, nrow))
    for row in range(nrow):
        for col in range(ncol):
            ix = row * ncol + col
            if ix >= len(long1):
                continue
            #plt.subplot(nrow, ncol, ix + 1) 
            plt.axis('off')
            ws, veh, nr, pos = titles[ix]
            str_title = str(ws) + "_Vehicle_" + str(veh) + "_events_" + str(nr) + "_" + str(pos)
            plt.plot(long1[ix], lat1[ix], color = "k")
            
            if not os.path.isdir("infl_cross/no_mark/" + labelname):
                os.makedirs("infl_cross/no_mark/" + labelname)
            #plt.show()
            plt.savefig("infl_cross/no_mark/" + labelname + "/" + labelname + "_" + str_title + ".png", bbox_inches = "tight")  
            plt.close() 

#for k in sorted(list(num_label_inflections.keys())): 
for k in dict(sorted(num_label_inflections.items(), key=lambda item: item[1], reverse = True)): 
    #if k.split("_")[-1] != "0":
        #continue
    print(k, num_label_inflections[k])
    nrow = 124
    ncol = 124 
    if nrow * ncol > num_label_inflections[k]:
        ncol = int(np.sqrt(num_label_inflections[k]))
        nrow = ncol
    #composite_img(x_y_infl_long_trajs[k][:nrow*ncol], x_y_infl_lat_trajs[k][:nrow*ncol], x_y_infl_id_trajs[k][:nrow*ncol], nrow, ncol, k, x_y_infl_infl_trajs[k][:nrow*ncol], x_y_infl_crossing_trajs[k][:nrow*ncol])
    #composite_img_no_mark(x_y_infl_long_trajs[k][:nrow*ncol], x_y_infl_lat_trajs[k][:nrow*ncol], x_y_infl_id_trajs[k][:nrow*ncol], nrow, ncol, k)

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

print(min(maxda), max(maxda))
print(np.quantile(maxda, 0.25), np.quantile(maxda, 0.5), np.quantile(maxda, 0.75), np.quantile(maxda, 0.9), np.quantile(maxda, 0.95))