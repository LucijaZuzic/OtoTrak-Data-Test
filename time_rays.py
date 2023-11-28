from utilities import *
from time import time

for size in [4, 8, 12, 16]:
    window_size = 20
    
    print(size)
    dotsx_original, dotsy_original = make_rays(size)

    deg = 5
    maxoffset = 0.005
    step_size = window_size
    #step_size = 1
    max_trajs = 100
    name_extension = "_window_" + str(window_size) + "_step_" + str(step_size) + "_segments_" + str(max_trajs)

    all_subdirs = os.listdir()  
    
    scale_val = [True, True, False, False]
    offset_val = [False, True, False, True]
    name_val = ["scale", "offset", "no scale", "only offset"]  

    numtests = 0
    maxtest = 100
    times_val = dict() 
    for name  in name_val:
        times_val[name] = 0
    for subdir_name in all_subdirs:
    
        if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
            continue
        print(subdir_name)    
        
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
            
            all_distances_trajs = dict()
            all_distances_preprocessed_trajs = dict()
            all_distances_scaled_trajs = dict()
            all_distances_scaled_to_max_trajs = dict() 

            only_number = some_file.replace(".csv", "").replace("events_", "")
            
            start_path = "rays/" + str(size) + "/" + subdir_name + "/" + only_number
    
            all_distances_trajs_other = dict()
            all_distances_preprocessed_trajs_other = dict()
            all_distances_scaled_trajs_other = dict()
            all_distances_scaled_to_max_trajs_other = dict() 
    
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
             
                if x not in all_distances_trajs_other:
                    all_distances_trajs_other[x] = dict()
                    all_distances_preprocessed_trajs_other[x] = dict()
                    all_distances_scaled_trajs_other[x] = dict()
                    all_distances_scaled_to_max_trajs_other[x] = dict()
                
                for value_for_dict in range(len(name_val)):
                    timescale = 0
                    timeoffset = 0
                    timenoscale = 0
                    timeonlyoffset = 0

                    start_time = time()
                    all_distances, all_distancesx, all_distancesy, intersections, distances, distancesx, distancesy, ni = compare_traj_ray(dotsx_original, dotsy_original, longitudes_tmp, latitudes_tmp, scale_val[value_for_dict], offset_val[value_for_dict]) 
                    all_distances_trajs[x][name_val[value_for_dict]] = (all_distances, all_distancesx, all_distancesy)
                    all_distances_trajs_other[x][name_val[value_for_dict]] = (intersections, distances, distancesx, distancesy)
                    
                    all_preprocessed_trajs_distances, all_preprocessed_trajs_distancesx, all_preprocessed_trajs_distancesy, intersections_preprocessed_trajs, distances_preprocessed_trajs, distancesx_preprocessed_trajs, distancesy_preprocessed_trajs, ni_pre = compare_traj_ray(dotsx_original, dotsy_original, longitudes_tmp_transform, latitudes_tmp_transform, scale_val[value_for_dict], offset_val[value_for_dict]) 
                    all_distances_preprocessed_trajs[x][name_val[value_for_dict]] = (all_preprocessed_trajs_distances, all_preprocessed_trajs_distancesx, all_preprocessed_trajs_distancesy)
                    all_distances_preprocessed_trajs_other[x][name_val[value_for_dict]] = (intersections_preprocessed_trajs, distances_preprocessed_trajs, distancesx_preprocessed_trajs, distancesy_preprocessed_trajs)
                    
                    all_scaled_trajs_distances, all_scaled_trajs_distancesx, all_scaled_trajs_distancesy, intersections_scaled_trajs, distances_scaled_trajs, distancesx_scaled_trajs, distancesy_scaled_trajs, ni_scale = compare_traj_ray(dotsx_original, dotsy_original, longitudes_scaled, latitudes_scaled, scale_val[value_for_dict], offset_val[value_for_dict]) 
                    all_distances_scaled_trajs[x][name_val[value_for_dict]] = (all_scaled_trajs_distances, all_scaled_trajs_distancesx, all_scaled_trajs_distancesy)
                    all_distances_scaled_trajs_other[x][name_val[value_for_dict]] = (intersections_scaled_trajs, distances_scaled_trajs, distancesx_scaled_trajs, distancesy_scaled_trajs)
                    
                    all_scaled_to_max_distances, all_scaled_to_max_distancesx, all_scaled_to_max_distancesy, intersections_scaled_to_max, distances_scaled_to_max, distancesx_scaled_to_max, distancesy_scaled_to_max, ni_scale_max = compare_traj_ray(dotsx_original, dotsy_original, longitudes_scaled_to_max, latitudes_scaled_to_max, scale_val[value_for_dict], offset_val[value_for_dict]) 
                    all_distances_scaled_to_max_trajs[x][name_val[value_for_dict]] = (all_scaled_to_max_distances, all_scaled_to_max_distancesx, all_scaled_to_max_distancesy)
                    all_distances_scaled_to_max_trajs_other[x][name_val[value_for_dict]] = (intersections_scaled_to_max, distances_scaled_to_max, distancesx_scaled_to_max, distancesy_scaled_to_max)
                    end_time = time()
                    times_val[name_val[value_for_dict]] += end_time - start_time
                
                numtests += 1

                if numtests == maxtest:
                    break
            if numtests == maxtest:
                break
        if numtests == maxtest:
            break
        
    for word in times_val:
        print(times_val[word] / 4 / maxtest)