from utilities import *
    
window_size = 20
 
size = 36
dotsx_original, dotsy_original = make_rays(size)

deg = 5
maxoffset = 0.005
step_size = window_size
#step_size = 1
max_trajs = 100
name_extension = "_window_" + str(window_size) + "_step_" + str(step_size) + "_segments_" + str(max_trajs)

all_subdirs = os.listdir()  

all_distances_trajs = dict()   
all_distances_trajs[window_size] = dict()

all_distances_preprocessed_trajs = dict()   
all_distances_preprocessed_trajs[window_size] = dict()

all_distances_scaled_trajs = dict()   
all_distances_scaled_trajs[window_size] = dict()

all_distances_scaled_to_max_trajs = dict()   
all_distances_scaled_to_max_trajs[window_size] = dict()

total_possible_trajs = 0
  
for subdir_name in all_subdirs:

    trajs_in_dir = 0
    
    if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
        continue
    print(subdir_name)  
    all_distances_trajs[window_size][subdir_name] = dict() 
    all_distances_preprocessed_trajs[window_size][subdir_name] = dict() 
    all_distances_scaled_trajs[window_size][subdir_name] = dict() 
    all_distances_scaled_to_max_trajs[window_size][subdir_name] = dict()  

    all_rides_cleaned = os.listdir(subdir_name + "/cleaned_csv/")
    
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
 
        all_distances_trajs[window_size][subdir_name][only_num_ride] = dict()
        all_distances_preprocessed_trajs[window_size][subdir_name][only_num_ride] = dict()
        all_distances_scaled_trajs[window_size][subdir_name][only_num_ride] = dict()
        all_distances_scaled_to_max_trajs[window_size][subdir_name][only_num_ride] = dict() 
        
        file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
        longitudes = list(file_with_ride["fields_longitude"])
        latitudes = list(file_with_ride["fields_latitude"]) 
        times = list(file_with_ride["time"])  
  
        for x in range(0, len(longitudes) - window_size + 1, step_size):
            longitudes_tmp = longitudes[x:x + window_size]
            latitudes_tmp = latitudes[x:x + window_size]
            times_tmp = times[x:x + window_size]  

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
		  
            total_possible_trajs += 1
            trajs_in_ride += 1
            trajs_in_dir += 1
            
            all_distances_trajs[window_size][subdir_name][only_num_ride][x] = {"scale": compare_traj_ray(size, window_size, dotsx_original, dotsy_original, longitudes_tmp, latitudes_tmp, True, False), "offset": compare_traj_ray(size, window_size, dotsx_original, dotsy_original, longitudes_tmp, latitudes_tmp, True, True), "no scale": compare_traj_ray(size, window_size, dotsx_original, dotsy_original, longitudes_tmp, latitudes_tmp, False, False)}
            all_distances_preprocessed_trajs[window_size][subdir_name][only_num_ride][x] = {"scale": compare_traj_ray(size, window_size, dotsx_original, dotsy_original, longitudes_tmp_transform, latitudes_tmp_transform, True, False), "offset": compare_traj_ray(size, window_size, dotsx_original, dotsy_original, longitudes_tmp_transform, latitudes_tmp_transform, True, True), "no scale": compare_traj_ray(size, window_size, dotsx_original, dotsy_original, longitudes_tmp_transform, latitudes_tmp_transform, False, False)}
            all_distances_scaled_trajs[window_size][subdir_name][only_num_ride][x] = {"scale": compare_traj_ray(size, window_size, dotsx_original, dotsy_original, longitudes_scaled, latitudes_scaled, True, False), "offset": compare_traj_ray(size, window_size, dotsx_original, dotsy_original, longitudes_scaled, latitudes_scaled, True, True), "no scale": compare_traj_ray(size, window_size, dotsx_original, dotsy_original, longitudes_scaled, latitudes_scaled, False, False)} 
            all_distances_scaled_to_max_trajs[window_size][subdir_name][only_num_ride][x] = {"scale": compare_traj_ray(size, window_size, dotsx_original, dotsy_original, longitudes_scaled_to_max, latitudes_scaled_to_max, True, False), "offset": compare_traj_ray(size, window_size, dotsx_original, dotsy_original, longitudes_scaled_to_max, latitudes_scaled_to_max, True, True), "no scale": compare_traj_ray(size, window_size, dotsx_original, dotsy_original, longitudes_scaled_to_max, latitudes_scaled_to_max, False, False)}
   
process_csv_ray(window_size, all_distances_trajs, "all_distances_trajs_" + str(size) + ".csv")
process_csv_ray(window_size, all_distances_preprocessed_trajs, "all_distances_preprocessed_trajs_" + str(size) + ".csv")
process_csv_ray(window_size, all_distances_scaled_trajs, "all_distances_scaled_trajs_" + str(size) + ".csv")
process_csv_ray(window_size, all_distances_scaled_to_max_trajs, "all_distances_scaled_to_max_trajs_" + str(size) + ".csv")