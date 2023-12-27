from utilities import *
import seaborn as sns

window_size = 20 
step_size = window_size
all_subdirs = os.listdir()
maxoffset = 0.005 
label_dict = {"D": 0, "NF": 0, "I": 0, "NM": 0} 
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
    
            total_infls = set()
            minspace = 0

            infls_long = set()
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
            
            labelm = str(len(total_infls)) + "_"
            if len(infls_lat) > len(infls_long): 
                nx = [l for l in longitudes_scaled_to_max]
                ny = [l for l in latitudes_scaled_to_max]
                ncross = [(c[0], c[1]) for c in crossing_positions]
            else: 
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
   
            if len(lat_sgn) > 1 and len(long_sgn) > 1:
                label = "NF"   
            if (len(lat_sgn) == 1 and len(long_sgn) > 1) or (len(lat_sgn) > 1 and len(long_sgn) == 1):
                label = "NM"   
            if len(lat_sgn) == 1 and len(long_sgn) == 1:
                if (True in lat_sgn and True in long_sgn) or (False in lat_sgn and False in long_sgn):
                    label = "I"
                else:
                    label = "D" 
                    
            label_dict[label] += 1
 