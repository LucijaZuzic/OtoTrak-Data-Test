from utilities import *
 
window_size = 20
deg = 5
maxoffset = 0.005
step_size = window_size
#step_size = 1
max_trajs = 100
name_extension = "_window_" + str(window_size) + "_step_" + str(step_size) + "_segments_" + str(max_trajs)

all_subdirs = os.listdir() 
  
all_possible_trajs = dict()   
all_possible_trajs[window_size] = dict()

all_feats_trajs = dict()   
all_feats_trajs[window_size] = dict()

all_feats_scaled_trajs = dict()   
all_feats_scaled_trajs[window_size] = dict()

all_feats_scaled_to_max_trajs = dict()   
all_feats_scaled_to_max_trajs[window_size] = dict()

trajectory_monotonous = dict()
trajectory_monotonous[window_size] = dict()
  
trajectory_flags = dict()
for flag in flag_names:
    trajectory_flags[flag] = dict()
    trajectory_flags[flag][window_size] = dict()

label_NF = 0
label_NM = 0
label_I = 0
label_D = 0
 
total_possible_trajs = 0
 
metric_names = ["euclidean", "dtw", "simpson", "trapz", "custom", "simpson x", "trapz x", "simpson y", "trapz y"]
sample_names = dict()

left_edge_x = [0 for i in range(window_size)]
left_edge_y = [x * 1 / (window_size - 1) for x in range(window_size)] 
sample_names["left"] = {"long": left_edge_x, "lat": left_edge_y}

right_edge_x = [1 for i in range(window_size)]
right_edge_y = [x * 1 / (window_size - 1) for x in range(window_size)] 
sample_names["right"] = {"long": right_edge_x, "lat": right_edge_y}

down_edge_x = [x * 1 / (window_size - 1) for x in range(window_size)]
down_edge_y = [0 for i in range(window_size)] 
sample_names["down"] = {"long": down_edge_x, "lat": down_edge_y}

up_edge_x = [x * 1 / (window_size - 1) for x in range(window_size)]
up_edge_y = [1 for i in range(window_size)] 
sample_names["up"] = {"long": up_edge_x, "lat": up_edge_y}

diagonal_edge_x = [x * 1 / (window_size - 1) for x in range(window_size)]
diagonal_edge_y = [x * 1 / (window_size - 1) for x in range(window_size)] 
sample_names["diagonal"] = {"long": diagonal_edge_x, "lat": diagonal_edge_y}

left_circle_y = [x * 1 / (window_size - 1) for x in range(window_size)]
left_circle_x = [np.sqrt(- y * (y - 1)) for y in left_circle_y] 
sample_names["left_circle"] = {"long": left_circle_x, "lat": left_circle_y}

right_circle_y = [x * 1 / (window_size - 1) for x in range(window_size)]
right_circle_x = [1 - np.sqrt(- y * (y - 1)) for y in right_circle_y] 
sample_names["right_circle"] = {"long": right_circle_x, "lat": right_circle_y}

down_circle_x = [x * 1 / (window_size - 1) for x in range(window_size)]
down_circle_y = [np.sqrt(- x * (x - 1)) for x in down_circle_x] 
sample_names["down_circle"] = {"long": down_circle_x, "lat": down_circle_y}

up_circle_x = [x * 1 / (window_size - 1) for x in range(window_size)]
up_circle_y = [1 - np.sqrt(- x * (x - 1)) for x in up_circle_x]  
sample_names["up_circle"] = {"long": up_circle_x, "lat": up_circle_y}

sin_x = [x * 1 / (window_size - 1) for x in range(window_size)]
sin_y = [np.sin(x * np.pi * 2) for x in sin_x]  
sample_names["sin"] = {"long": sin_x, "lat": sin_y}

sin_reverse_x = [x * 1 / (window_size - 1) for x in range(window_size)]
sin_reverse_y = [np.sin(x * np.pi * 2 + np.pi) for x in sin_x]  
sample_names["sin_reverse"] = {"long": sin_reverse_x, "lat": sin_reverse_y}

sin_half_x = [x * 1 / (window_size - 1) for x in range(window_size)]
sin_half_y = [np.sin(x * np.pi) for x in sin_half_x]  
sample_names["sin_half"] = {"long": sin_half_x, "lat": sin_half_y}

sin_half_reverse_x = [x * 1 / (window_size - 1) for x in range(window_size)]
sin_half_reverse_y = [np.sin(x * np.pi + np.pi) for x in sin_half_x]  
sample_names["sin_half_reverse"] = {"long": sin_half_reverse_x, "lat": sin_half_reverse_y}

cos_x = [x * 1 / (window_size - 1) for x in range(window_size)]
cos_y = [np.cos(x * np.pi * 2) for x in cos_x]  
sample_names["cos"] = {"long": cos_x, "lat": cos_y}

cos_reverse_x = [x * 1 / (window_size - 1) for x in range(window_size)]
cos_reverse_y = [np.cos(x * np.pi * 2 + np.pi) for x in cos_x]  
sample_names["cos_reverse"] = {"long": cos_reverse_x, "lat": cos_reverse_y}

cos_half_x = [x * 1 / (window_size - 1) for x in range(window_size)]
cos_half_y = [np.cos(x * np.pi) for x in cos_half_x]  
sample_names["cos_half"] = {"long": cos_half_x, "lat": cos_half_y}

cos_half_reverse_x = [x * 1 / (window_size - 1) for x in range(window_size)]
cos_half_reverse_y = [np.cos(x * np.pi + np.pi) for x in cos_half_x]  
sample_names["cos_half_reverse"] = {"long": cos_half_reverse_x, "lat": cos_half_reverse_y}

size = 8
dotsx_original, dotsy_original = make_rays(size)
for subdir_name in all_subdirs:

    trajs_in_dir = 0
    
    if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
        continue
     
    all_possible_trajs[window_size][subdir_name] = dict() 
    all_feats_trajs[window_size][subdir_name] = dict() 
    all_feats_scaled_trajs[window_size][subdir_name] = dict() 
    all_feats_scaled_to_max_trajs[window_size][subdir_name] = dict() 
    trajectory_monotonous[window_size][subdir_name] = dict() 
    for flag in flag_names:
        trajectory_flags[flag][window_size][subdir_name] = dict()  

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

        all_possible_trajs[window_size][subdir_name][only_num_ride] = dict()
        all_feats_trajs[window_size][subdir_name][only_num_ride] = dict()
        all_feats_scaled_trajs[window_size][subdir_name][only_num_ride] = dict()
        all_feats_scaled_to_max_trajs[window_size][subdir_name][only_num_ride] = dict() 
        trajectory_monotonous[window_size][subdir_name][only_num_ride] = dict() 
        for flag in flag_names:
            trajectory_flags[flag][window_size][subdir_name][only_num_ride] = dict() 
    
        file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
        longitudes = list(file_with_ride["fields_longitude"])
        latitudes = list(file_with_ride["fields_latitude"]) 
        times = list(file_with_ride["time"])  
        flags_dict = dict()
        for flag in flag_names:
            flags_dict[flag] = list(file_with_ride["fields_" + flag])
  
        for x in range(0, len(longitudes) - window_size + 1, step_size):
            longitudes_tmp = longitudes[x:x + window_size]
            latitudes_tmp = latitudes[x:x + window_size]
            times_tmp = times[x:x + window_size] 
            for flag in flag_names:
                trajectory_flags_tmp = flags_dict[flag][x:x + window_size] 
 
                count_limit = False 
                for val_flag in trajectory_flags_tmp:  
                    if val_flag:
                        count_limit = True
                        break
                        
                trajectory_flags[flag][window_size][subdir_name][only_num_ride][x] = count_limit

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
            
            longitudes_scaled, latitudes_scaled = scale_long_lat(longitudes_tmp_transform, latitudes_tmp_transform)
            
            longitudes_scaled_to_max, latitudes_scaled_to_max = scale_long_lat(longitudes_tmp_transform, latitudes_tmp_transform, xmax = maxoffset, ymax = maxoffset, keep_aspect_ratio = True)

            times_tmp_transform = transform_time(times_tmp)

            total_possible_trajs += 1
            trajs_in_ride += 1
            trajs_in_dir += 1 

            all_possible_trajs[window_size][subdir_name][only_num_ride][x] = {"long": longitudes_tmp_transform, "lat": latitudes_tmp_transform, "time": times_tmp_transform}
 
            sp_len = mean_speed_len(longitudes_tmp_transform, latitudes_tmp_transform, times_tmp_transform)  
            sp_offset = mean_speed_offset(longitudes_tmp_transform, latitudes_tmp_transform, times_tmp_transform)   
            surfarea = total_surf(longitudes_tmp_transform, latitudes_tmp_transform) 
            surf_trapz_x, surf_trapz_y = get_surf_xt_yt(longitudes_tmp_transform, latitudes_tmp_transform, times_tmp_transform, "trapz")
            surf_simpson_x, surf_simpson_y = get_surf_xt_yt(longitudes_tmp_transform, latitudes_tmp_transform, times_tmp_transform, "simpson")
                
            sp_len_scaled = mean_speed_len(longitudes_scaled, latitudes_scaled, times_tmp_transform)  
            sp_offset_scaled = mean_speed_offset(longitudes_scaled, latitudes_scaled, times_tmp_transform)   
            surfarea_scaled = total_surf(longitudes_scaled, latitudes_scaled)  
            surf_trapz_x_scaled, surf_trapz_y_scaled = get_surf_xt_yt(longitudes_scaled, latitudes_scaled, times_tmp_transform, "trapz")
            surf_simpson_x_scaled, surf_simpson_y_scaled = get_surf_xt_yt(longitudes_scaled, latitudes_scaled, times_tmp_transform, "simpson") 
         
            sp_len_scaled_to_max = mean_speed_len(longitudes_scaled_to_max, latitudes_scaled_to_max, times_tmp_transform)  
            sp_offset_scaled_to_max = mean_speed_offset(longitudes_scaled_to_max, latitudes_scaled_to_max, times_tmp_transform)   
            surfarea_scaled_to_max = total_surf(longitudes_scaled_to_max, latitudes_scaled_to_max)   
            surf_trapz_x_scaled_to_max, surf_trapz_y_scaled_to_max = get_surf_xt_yt(longitudes_scaled_to_max, latitudes_scaled_to_max, times_tmp_transform, "trapz")
            surf_simpson_x_scaled_to_max, surf_simpson_y_scaled_to_max = get_surf_xt_yt(longitudes_scaled_to_max, latitudes_scaled_to_max, times_tmp_transform, "simpson") 

            long_sgn = set()
            for long_ind in range(len(longitudes_tmp_transform) - 1):
                long_sgn.add(longitudes_tmp_transform[long_ind + 1] > longitudes_tmp_transform[long_ind])
                if len(long_sgn) > 1:
                    break

            lat_sgn = set()
            for lat_ind in range(len(latitudes_tmp_transform) - 1):
                lat_sgn.add(latitudes_tmp_transform[lat_ind + 1] > latitudes_tmp_transform[lat_ind])
                if len(lat_sgn) > 1:
                    break

            x_poly, y_poly = get_poly_xt_yt(longitudes_tmp_transform, latitudes_tmp_transform, times_tmp_transform, deg)
            xy_poly = []
            if len(lat_sgn) == 1 and len(long_sgn) == 1:
                xy_poly = np.polyfit(longitudes_tmp_transform, latitudes_tmp_transform, deg)
                
            x_poly_scaled, y_poly_scaled = get_poly_xt_yt(longitudes_scaled, latitudes_scaled, times_tmp_transform, deg)
            xy_poly_scaled = []
            if len(lat_sgn) == 1 and len(long_sgn) == 1:
                xy_poly_scaled = np.polyfit(longitudes_scaled, latitudes_scaled, deg)

            x_poly_scaled_to_max, y_poly_scaled_to_max = get_poly_xt_yt(longitudes_scaled_to_max, latitudes_scaled_to_max, times_tmp_transform, deg)
            xy_poly_scaled_to_max = []
            if len(lat_sgn) == 1 and len(long_sgn) == 1:
                xy_poly_scaled_to_max = np.polyfit(longitudes_scaled_to_max, latitudes_scaled_to_max, deg)

            all_feats_trajs[window_size][subdir_name][only_num_ride][x] = { 
                                                                           "max_x": max(longitudes_tmp_transform),
                                                                           "max_y": max(latitudes_tmp_transform),
                                                                           "surf_trapz_x": surf_trapz_x, 
                                                                           "surf_trapz_y": surf_trapz_y, 
                                                                           "surf_simpson_x": surf_simpson_x, 
                                                                           "surf_simpson_y": surf_simpson_y, 
                                                                           "x_poly": x_poly, 
                                                                           "y_poly": y_poly, 
                                                                           "xy_poly": xy_poly, 
                                                                           "duration": times_tmp_transform[-1],
                                                                           "len": sp_len * times_tmp_transform[-1], 
                                                                           "offset": sp_offset * times_tmp_transform[-1],
                                                                           "mean_speed_len": sp_len, 
                                                                           "mean_speed_offset": sp_offset,
                                                                           "len_vs_offset": sp_len / sp_offset,
                                                                           "total_surf": surfarea}

            for sample_name in sample_names:
                 for metric_name in metric_names: 
                    oldx = [valx for valx in sample_names[sample_name]["long"]]
                    oldy = [valy for valy in sample_names[sample_name]["lat"]]
                    newx = [valx * max(max(longitudes_tmp_transform), max(latitudes_tmp_transform)) for valx in sample_names[sample_name]["long"]]
                    newy = [valy * max(max(longitudes_tmp_transform), max(latitudes_tmp_transform)) for valy in sample_names[sample_name]["lat"]]
                    all_feats_trajs[window_size][subdir_name][only_num_ride][x][sample_name + "_same_" + metric_name] = compare_traj_and_sample(newx, newy, range(len(newx)), {"long": longitudes_tmp_transform, "lat": latitudes_tmp_transform, "time": times_tmp_transform}, metric_name, False, False, True, True, dotsx_original, dotsy_original)
                    all_feats_trajs[window_size][subdir_name][only_num_ride][x][sample_name + "_diff_" + metric_name] = compare_traj_and_sample(oldx, oldy, range(len(oldx)), {"long": longitudes_tmp_transform, "lat": latitudes_tmp_transform, "time": times_tmp_transform}, metric_name, False, False, True, True, dotsx_original, dotsy_original)

            all_feats_scaled_trajs[window_size][subdir_name][only_num_ride][x] = { 
                                                                           "max_x": max(longitudes_scaled),
                                                                           "max_y": max(latitudes_scaled),
                                                                           "surf_trapz_x": surf_trapz_x_scaled, 
                                                                           "surf_trapz_y": surf_trapz_y_scaled, 
                                                                           "surf_simpson_x": surf_simpson_x_scaled, 
                                                                           "surf_simpson_y": surf_simpson_y_scaled, 
                                                                           "x_poly": x_poly_scaled, 
                                                                           "y_poly": y_poly_scaled, 
                                                                           "xy_poly": xy_poly_scaled, 
                                                                           "duration": times_tmp_transform[-1],
                                                                           "len": sp_len_scaled * times_tmp_transform[-1], 
                                                                           "offset": sp_offset_scaled * times_tmp_transform[-1],
                                                                           "mean_speed_len": sp_len_scaled, 
                                                                           "mean_speed_offset": sp_offset_scaled,
                                                                           "len_vs_offset": sp_len_scaled / sp_offset_scaled,
                                                                           "total_surf": surfarea_scaled} 
            
            for sample_name in sample_names:
                 for metric_name in metric_names: 
                    oldx = [valx for valx in sample_names[sample_name]["long"]]
                    oldy = [valy for valy in sample_names[sample_name]["lat"]]
                    newx = [valx * max(max(longitudes_scaled), max(latitudes_scaled)) for valx in sample_names[sample_name]["long"]]
                    newy = [valy * max(max(longitudes_scaled), max(latitudes_scaled)) for valy in sample_names[sample_name]["lat"]]
                    all_feats_scaled_trajs[window_size][subdir_name][only_num_ride][x][sample_name + "_same_" + metric_name] = compare_traj_and_sample(newx, newy, range(len(newx)), {"long": longitudes_scaled, "lat": latitudes_scaled, "time": times_tmp_transform}, metric_name)
                    all_feats_scaled_trajs[window_size][subdir_name][only_num_ride][x][sample_name + "_diff_" + metric_name] = compare_traj_and_sample(oldx, oldy, range(len(oldx)), {"long": longitudes_scaled, "lat": latitudes_scaled, "time": times_tmp_transform}, metric_name)

            all_feats_scaled_to_max_trajs[window_size][subdir_name][only_num_ride][x] = {  
                                                                           "max_x": max(longitudes_scaled_to_max),
                                                                           "max_y": max(latitudes_scaled_to_max),
                                                                           "surf_trapz_x": surf_trapz_x_scaled_to_max, 
                                                                           "surf_trapz_y": surf_trapz_y_scaled_to_max, 
                                                                           "surf_simpson_x": surf_simpson_x_scaled_to_max, 
                                                                           "surf_simpson_y": surf_simpson_y_scaled_to_max, 
                                                                           "x_poly": x_poly_scaled_to_max, 
                                                                           "y_poly": y_poly_scaled_to_max, 
                                                                           "xy_poly": xy_poly_scaled_to_max, 
                                                                           "duration": times_tmp_transform[-1],
                                                                           "len": sp_len_scaled_to_max * times_tmp_transform[-1], 
                                                                           "offset": sp_offset_scaled_to_max * times_tmp_transform[-1],
                                                                           "mean_speed_len": sp_len_scaled_to_max, 
                                                                           "mean_speed_offset": sp_offset_scaled_to_max,
                                                                           "len_vs_offset": sp_len_scaled_to_max / sp_offset_scaled_to_max,
                                                                           "total_surf": surfarea_scaled_to_max}
            
            for sample_name in sample_names:
                 for metric_name in metric_names: 
                    oldx = [valx for valx in sample_names[sample_name]["long"]]
                    oldy = [valy for valy in sample_names[sample_name]["lat"]]
                    newx = [valx * max(max(longitudes_scaled_to_max), max(latitudes_scaled_to_max)) for valx in sample_names[sample_name]["long"]]
                    newy = [valy * max(max(longitudes_scaled_to_max), max(latitudes_scaled_to_max)) for valy in sample_names[sample_name]["lat"]]
                    all_feats_scaled_to_max_trajs[window_size][subdir_name][only_num_ride][x][sample_name + "_same_" + metric_name] = compare_traj_and_sample(newx, newy, range(len(newx)), {"long": longitudes_scaled_to_max, "lat": latitudes_scaled_to_max, "time": times_tmp_transform}, metric_name)
                    all_feats_scaled_to_max_trajs[window_size][subdir_name][only_num_ride][x][sample_name + "_diff_" + metric_name] = compare_traj_and_sample(oldx, oldy, range(len(oldx)), {"long": longitudes_scaled_to_max, "lat": latitudes_scaled_to_max, "time": times_tmp_transform}, metric_name)
            
            if len(lat_sgn) > 1 and len(long_sgn) > 1:
                trajectory_monotonous[window_size][subdir_name][only_num_ride][x] = "NF"
                label_NF += 1
            if (len(lat_sgn) == 1 and len(long_sgn) > 1) or (len(lat_sgn) > 1 and len(long_sgn) == 1):
                trajectory_monotonous[window_size][subdir_name][only_num_ride][x] = "NM"
                label_NM += 1
            if len(lat_sgn) == 1 and len(long_sgn) == 1:
                if (True in lat_sgn and True in long_sgn) or (False in lat_sgn and False in long_sgn):
                    trajectory_monotonous[window_size][subdir_name][only_num_ride][x] = "I"
                    label_I += 1
                else:
                    trajectory_monotonous[window_size][subdir_name][only_num_ride][x] = "D"
                    label_D += 1
                 
        #print(only_num_ride, trajs_in_ride)
    print(subdir_name, trajs_in_dir)
print(total_possible_trajs)
print("NF", label_NF, "NM", label_NM, "D", label_D, "I", label_I) 

if not os.path.isdir("all_feats"):
    os.makedirs("all_feats")

process_csv(trajectory_flags, trajectory_monotonous, window_size, all_possible_trajs, sample_names, metric_names, deg, all_feats_trajs, "all_feats/all_feats.csv")
process_csv(trajectory_flags, trajectory_monotonous, window_size, all_possible_trajs, sample_names, metric_names, deg, all_feats_scaled_trajs, "all_feats/all_feats_scaled.csv")
process_csv(trajectory_flags, trajectory_monotonous, window_size, all_possible_trajs, sample_names, metric_names, deg, all_feats_scaled_to_max_trajs, "all_feats/all_feats_scaled_to_max.csv")