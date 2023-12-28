from utilities import *
 
window_size = 20
deg = 5
maxoffset = 0.005
step_size = window_size
#step_size = 1
max_trajs = 100
name_extension = "_window_" + str(window_size) + "_step_" + str(step_size) + "_segments_" + str(max_trajs)

all_subdirs = os.listdir() 
   
all_feats_heading_trajs = dict()   
all_feats_heading_trajs[window_size] = dict()

all_feats_heading_scaled_trajs = dict()   
all_feats_heading_scaled_trajs[window_size] = dict()

all_feats_heading_scaled_to_max_trajs = dict()   
all_feats_heading_scaled_to_max_trajs[window_size] = dict()
   
for subdir_name in all_subdirs:

    trajs_in_dir = 0
    
    if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
        continue
      
    all_feats_heading_trajs[window_size][subdir_name] = dict() 
    all_feats_heading_scaled_trajs[window_size][subdir_name] = dict() 
    all_feats_heading_scaled_to_max_trajs[window_size][subdir_name] = dict()  

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
          
        all_feats_heading_trajs[window_size][subdir_name][only_num_ride] = dict()
        all_feats_heading_scaled_trajs[window_size][subdir_name][only_num_ride] = dict()
        all_feats_heading_scaled_to_max_trajs[window_size][subdir_name][only_num_ride] = dict()  
    
        file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
        longitudes = list(file_with_ride["fields_longitude"])
        latitudes = list(file_with_ride["fields_latitude"]) 
        times = list(file_with_ride["time"])   
        headings = list(file_with_ride["fields_direction"])   
  
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

            times_tmp_transform = transform_time(times_tmp)

            headings_tmp = headings[x:x + window_size]    
            x_dir = longitudes_tmp[0] < longitudes_tmp[-1]
            y_dir = latitudes_tmp[0] < latitudes_tmp[-1]
            headings_tmp_new = []    
            for ind in range(len(headings_tmp)):
                new_dir = (90 - headings_tmp[ind] + 360) % 360 
                if not x_dir: 
                    new_dir = (180 - new_dir + 360) % 360
                if not y_dir: 
                    new_dir = 360 - new_dir 
                headings_tmp_new.append(new_dir)
  
            trajs_in_dir += 1  

            headings_trajs = return_angles(longitudes_tmp_transform, latitudes_tmp_transform)
            headings_abs_trajs = return_angles_abs(longitudes_tmp_transform, latitudes_tmp_transform) 
 
            all_feats_heading_trajs[window_size][subdir_name][only_num_ride][x] = {"mean_heading": np.average(headings_trajs),
                                                                                   "mean_heading_abs": np.average(headings_abs_trajs),
                                                                                   "mean_heading_ototrak": np.average(headings_tmp),
                                                                                   "mean_heading_ototrak_new": np.average(headings_tmp_new)
                                                                                   }
            
            headings_scaled_trajs = return_angles(longitudes_scaled, latitudes_scaled)
            headings_abs_scaled_trajs = return_angles_abs(longitudes_scaled, latitudes_scaled) 

            all_feats_heading_scaled_trajs[window_size][subdir_name][only_num_ride][x] = {"mean_heading": np.average(headings_scaled_trajs),
                                                                                          "mean_heading_abs": np.average(headings_abs_scaled_trajs),
                                                                                          "mean_heading_ototrak": np.average(headings_tmp),
                                                                                          "mean_heading_ototrak_new": np.average(headings_tmp_new)
                                                                                          }
            
            headings_scaled_to_max_trajs = return_angles(longitudes_scaled_to_max, latitudes_scaled_to_max)
            headings_abs_scaled_to_max_trajs = return_angles_abs(longitudes_scaled_to_max, latitudes_scaled_to_max) 

            all_feats_heading_scaled_to_max_trajs[window_size][subdir_name][only_num_ride][x] = {"mean_heading": np.average(headings_scaled_to_max_trajs),
                                                                                                 "mean_heading_abs": np.average(headings_abs_scaled_to_max_trajs),
                                                                                                 "mean_heading_ototrak": np.average(headings_tmp),
                                                                                                 "mean_heading_ototrak_new": np.average(headings_tmp_new)
                                                                                                 }
                
        #print(only_num_ride, trajs_in_ride)
    print(subdir_name, trajs_in_dir) 

if not os.path.isdir("all_feats_heading"):
    os.makedirs("all_feats_heading")

process_csv_generic(window_size, all_feats_heading_trajs, "all_feats_heading/all_feats_heading.csv")
process_csv_generic(window_size, all_feats_heading_scaled_trajs, "all_feats_heading/all_feats_heading_scaled.csv")
process_csv_generic(window_size, all_feats_heading_scaled_to_max_trajs, "all_feats_heading/all_feats_heading_scaled_to_max.csv")

dict_for_clustering = load_object("dict_for_clustering")     
for window_size in dict_for_clustering: 
    for subdir_name in dict_for_clustering[window_size]: 
        for some_file in dict_for_clustering[window_size][subdir_name]: 
            short_file = some_file.replace("events_", "").replace(".csv", "")
            for x in dict_for_clustering[window_size][subdir_name][some_file]:
                if len(dict_for_clustering[window_size][subdir_name][some_file][x]) == 0:
                        continue
                for feat_name in dict_for_clustering[window_size][subdir_name][some_file][x]:
                    if "mean_heading" in feat_name:
                        if "all_feats_heading_scaled_to_max_" in feat_name:
                            short_feat = feat_name.replace("all_feats_heading_scaled_to_max_", "")
                            dict_for_clustering[window_size][subdir_name][some_file][x][feat_name] = all_feats_heading_scaled_to_max_trajs[window_size][subdir_name][short_file][x][short_feat]
save_object("dict_for_clustering", dict_for_clustering)