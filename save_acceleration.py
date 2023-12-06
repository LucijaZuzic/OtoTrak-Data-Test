from utilities import *
 
window_size = 20
deg = 5
maxoffset = 0.005
step_size = window_size
#step_size = 1
max_trajs = 100
name_extension = "_window_" + str(window_size) + "_step_" + str(step_size) + "_segments_" + str(max_trajs)

all_subdirs = os.listdir() 
   
all_feats_acceler_trajs = dict()   
all_feats_acceler_trajs[window_size] = dict()

all_feats_acceler_scaled_trajs = dict()   
all_feats_acceler_scaled_trajs[window_size] = dict()

all_feats_acceler_scaled_to_max_trajs = dict()   
all_feats_acceler_scaled_to_max_trajs[window_size] = dict()
   
for subdir_name in all_subdirs:

    trajs_in_dir = 0
    
    if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
        continue
      
    all_feats_acceler_trajs[window_size][subdir_name] = dict() 
    all_feats_acceler_scaled_trajs[window_size][subdir_name] = dict() 
    all_feats_acceler_scaled_to_max_trajs[window_size][subdir_name] = dict()  

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
          
        all_feats_acceler_trajs[window_size][subdir_name][only_num_ride] = dict()
        all_feats_acceler_scaled_trajs[window_size][subdir_name][only_num_ride] = dict()
        all_feats_acceler_scaled_to_max_trajs[window_size][subdir_name][only_num_ride] = dict()  
    
        file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
        longitudes = list(file_with_ride["fields_longitude"])
        latitudes = list(file_with_ride["fields_latitude"]) 
        times = list(file_with_ride["time"])  
        speeds = list(file_with_ride["fields_speed"])   
  
        for x in range(0, len(longitudes) - window_size + 1, step_size):
            longitudes_tmp = longitudes[x:x + window_size]
            latitudes_tmp = latitudes[x:x + window_size]
            times_tmp = times[x:x + window_size] 
            speeds_tmp = speeds[x:x + window_size]   

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
  
            trajs_in_dir += 1 

            speeds_trajs = return_speeds_long_lat(longitudes_tmp_transform, latitudes_tmp_transform, times_tmp_transform)
            accelers_trajs = return_acceler_speeds(speeds_trajs)
            avg_speed_trajs = sum(speeds_trajs) / len(speeds_trajs)
            avg_acceler_trajs = sum(accelers_trajs) / len(accelers_trajs)
            
            accelers_ototrak_trajs = return_acceler_speeds(speeds_tmp) 
            avg_speed_ototrak_trajs = sum(speeds_tmp) / len(speeds_tmp)
            avg_acceler_ototrak_trajs = sum(accelers_ototrak_trajs) / len(accelers_ototrak_trajs)

            avg_ratio_speed_trajs = avg_ratio(speeds_trajs, speeds_tmp)
            avg_ratio_acceler_trajs = avg_ratio(accelers_trajs, accelers_ototrak_trajs)
  
            all_feats_acceler_trajs[window_size][subdir_name][only_num_ride][x] = {"mean_speed": avg_speed_trajs, 
                                                                           "mean_acceler": avg_acceler_trajs,
                                                                           "mean_speed_ototrak": avg_speed_ototrak_trajs,
                                                                           "mean_acceler_ototrak": avg_acceler_ototrak_trajs, 
                                                                           "avg_ratio_speed": avg_ratio_speed_trajs, 
                                                                           "avg_ratio_acceler": avg_ratio_acceler_trajs,
                                                                           }
            
            speeds_scaled_trajs = return_speeds_long_lat(longitudes_scaled, latitudes_scaled, times_tmp_transform)
            accelers_scaled_trajs = return_acceler_speeds(speeds_scaled_trajs)
            avg_speed_scaled_trajs = sum(speeds_scaled_trajs) / len(speeds_scaled_trajs)
            avg_acceler_scaled_trajs = sum(accelers_scaled_trajs) / len(accelers_scaled_trajs)
            
            accelers_ototrak_scaled_trajs = return_acceler_speeds(speeds_tmp) 
            avg_speed_ototrak_scaled_trajs = sum(speeds_tmp) / len(speeds_tmp)
            avg_acceler_ototrak_scaled_trajs = sum(accelers_ototrak_scaled_trajs) / len(accelers_ototrak_scaled_trajs)

            avg_ratio_speed_scaled_trajs = avg_ratio(speeds_scaled_trajs, speeds_tmp)
            avg_ratio_acceler_scaled_trajs = avg_ratio(accelers_scaled_trajs, accelers_ototrak_scaled_trajs)
  
            all_feats_acceler_scaled_trajs[window_size][subdir_name][only_num_ride][x] = {"mean_speed": avg_speed_scaled_trajs, 
                                                                                  "mean_acceler": avg_acceler_scaled_trajs, 
                                                                                  "mean_speed_ototrak": avg_speed_ototrak_scaled_trajs,
                                                                                  "mean_acceler_ototrak": avg_acceler_ototrak_scaled_trajs,
                                                                                  "avg_ratio_speed": avg_ratio_speed_scaled_trajs,
                                                                                  "avg_ratio_acceler": avg_ratio_acceler_scaled_trajs,
                                                                                  }

            speeds_scaled_to_max_trajs = return_speeds_long_lat(longitudes_scaled_to_max, latitudes_scaled_to_max, times_tmp_transform)
            accelers_scaled_to_max_trajs = return_acceler_speeds(speeds_scaled_to_max_trajs)
            avg_speed_scaled_to_max_trajs = sum(speeds_scaled_to_max_trajs) / len(speeds_scaled_to_max_trajs)
            avg_acceler_scaled_to_max_trajs = sum(accelers_scaled_to_max_trajs) / len(accelers_scaled_to_max_trajs)
            
            accelers_ototrak_scaled_to_max_trajs = return_acceler_speeds(speeds_tmp) 
            avg_speed_ototrak_scaled_to_max_trajs = sum(speeds_tmp) / len(speeds_tmp)
            avg_acceler_ototrak_scaled_to_max_trajs = sum(accelers_ototrak_scaled_to_max_trajs) / len(accelers_ototrak_scaled_to_max_trajs)

            avg_ratio_speed_scaled_to_max_trajs = avg_ratio(speeds_scaled_to_max_trajs, speeds_tmp)
            avg_ratio_acceler_scaled_to_max_trajs = avg_ratio(accelers_scaled_to_max_trajs, accelers_ototrak_scaled_to_max_trajs)
  
            all_feats_acceler_scaled_to_max_trajs[window_size][subdir_name][only_num_ride][x] = {"mean_speed": avg_speed_scaled_to_max_trajs,
                                                                                         "mean_acceler": avg_acceler_scaled_to_max_trajs,
                                                                                         "mean_speed_ototrak": avg_speed_ototrak_scaled_to_max_trajs,
                                                                                         "mean_acceler_ototrak": avg_acceler_ototrak_scaled_to_max_trajs,
                                                                                         "avg_ratio_speed": avg_ratio_speed_scaled_to_max_trajs,
                                                                                         "avg_ratio_acceler": avg_ratio_acceler_scaled_to_max_trajs,
                                                                                        }
                
        #print(only_num_ride, trajs_in_ride)
    print(subdir_name, trajs_in_dir) 

if not os.path.isdir("all_feats_acceler"):
    os.makedirs("all_feats_acceler")

process_csv_generic(window_size, all_feats_acceler_trajs, "all_feats_acceler/all_feats_acceler.csv")
process_csv_generic(window_size, all_feats_acceler_scaled_trajs, "all_feats_acceler/all_feats_acceler_scaled.csv")
process_csv_generic(window_size, all_feats_acceler_scaled_to_max_trajs, "all_feats_acceler/all_feats_acceler_scaled_to_max.csv")