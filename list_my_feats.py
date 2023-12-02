from utilities import * 
from sklearn.manifold import TSNE


window_size = 20
deg = 5
maxoffset = 0.005
step_size = window_size
#step_size = 1 

header = ["start", "window_size", "vehicle", "ride"] 
skip = ["key", "flip", "zone", "engine", "in_zone", "ignition", "sleep_mode", "staff_mode", "buzzer_active", "in_primary_zone", "in_restricted_zone", "onboard_geofencing", "speed_limit_active"]
all_subdirs = os.listdir() 

def make_clusters_multi_feats():
    printed = False
    dict_for_clustering= dict()
    dict_for_clustering[window_size] = dict()
    train_names = set()
    test_names = set()  
    
    for subdir_name in all_subdirs:
 
        if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
            continue 
        dict_for_clustering[window_size][subdir_name] = dict()
        
        all_files = os.listdir(subdir_name + "/cleaned_csv/") 
        bad_rides_filenames = set()
        if os.path.isfile(subdir_name + "/bad_rides_filenames"):
            bad_rides_filenames = load_object(subdir_name + "/bad_rides_filenames")
        gap_rides_filenames = set()
        if os.path.isfile(subdir_name + "/gap_rides_filenames"):
            gap_rides_filenames = load_object(subdir_name + "/gap_rides_filenames")
            
        train_rides = set()
        if os.path.isfile(subdir_name + "/train_rides"):
            train_rides = load_object(subdir_name + "/train_rides")
            
        test_rides = set()
        if os.path.isfile(subdir_name + "/test_rides"):
            test_rides = load_object(subdir_name + "/test_rides")

        #open_feats_scaled = pd.read_csv("all_feats/all_feats_scaled_" + subdir_name + ".csv", index_col = False)
        open_feats_scaled_max = pd.read_csv("all_feats/all_feats_scaled_to_max_" + subdir_name + ".csv", index_col = False)
        #open_feats = pd.read_csv("all_feats/all_feats_" + subdir_name + ".csv", index_col = False)

        for some_file in all_files:  
            if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames:
                continue 

            file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
            dict_for_clustering[window_size][subdir_name][some_file] = dict()
            longitudes = list(file_with_ride["fields_longitude"])
            latitudes = list(file_with_ride["fields_latitude"]) 
            
            if some_file in train_rides:
                train_names.add(some_file)

            if some_file in test_rides:
                test_names.add(some_file) 
 
            only_number = some_file.replace(".csv", "").replace("events_", "")
            if "no_rays" not in subdirname:
                dsmax = dict()
                #dsc = dict()
                #dpp = dict()
                #d = dict()
                nsmax = dict()
                #nsc = dict()
                #npp = dict()
                #n = dict() 
                for size in os.listdir("rays"):  
                    if "size" in subdirname and "_" + str(size) + "_" not in subdirname:
                        continue
                    start_path = "rays/" + str(size) + "/" + subdir_name + "/" + only_number
                    dsmax[size] = pd.read_csv(start_path + "/all_distances_scaled_to_max_trajs.csv", index_col = False)
                    #dsc[size] = pd.read_csv(start_path + "/all_distances_scaled_trajs.csv", index_col = False)
                    #dpp[size] = pd.read_csv(start_path + "/all_distances_preprocessed_trajs.csv", index_col = False)
                    #d[size] = pd.read_csv(start_path + "/all_distances_trajs.csv", index_col = False)
                    nsmax[size] = load_object(start_path + "/all_nums_scaled_to_max_trajs")
                    #nsc[size] = load_object(start_path + "/all_nums_scaled_trajs")
                    #npp[size] = load_object(start_path + "/all_nums_preprocessed_trajs")
                    #n[size] = load_object(start_path + "/all_nums_trajs") 
    
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
                
                #print(x)
                dict_for_clustering[window_size][subdir_name][some_file][x] = dict()

                if "only_rays" not in subdirname:
    
                    for index in range(len(open_feats_scaled_max["start"])):
                        if str(open_feats_scaled_max["start"][index]) != str(x):
                            continue
                        if str(open_feats_scaled_max["window_size"][index]) != str(window_size):
                            continue
                        if str(open_feats_scaled_max["vehicle"][index]) != str(subdir_name):
                            continue
                        if str(open_feats_scaled_max["ride"][index]) != str(only_number):
                            continue  
                        #print("Located feats")
                        for key_name in open_feats_scaled_max.head(): 
                            if key_name in header:
                                continue
                            if key_name in skip and "flags" not in subdirname:
                                continue
                            if "poly" in key_name and "poly" not in subdirname:
                                continue
                            if "diff" in key_name:
                                continue
                            if "Unnamed" in key_name:
                                continue
                            #dict_for_clustering[window_size][subdir_name][some_file][x]["all_feats_scaled_" + key_name] = open_feats_scaled[key_name][index]
                            dict_for_clustering[window_size][subdir_name][some_file][x]["all_feats_scaled_to_max_" + key_name] = open_feats_scaled_max[key_name][index]
                            #dict_for_clustering[window_size][subdir_name][some_file][x]["all_feats_" + key_name] = open_feats[key_name][index]
                    
                    #print(len(dict_for_clustering[window_size][subdir_name][some_file][x]))
 
                if "no_rays" not in subdirname:
                    for size in os.listdir("rays"):  
                        if "size" in subdirname and "_" + str(size) + "_" not in subdirname:
                            continue
                        for index in range(len(dsmax[size]["start"])):
                            if str(dsmax[size]["start"][index]) != str(x):
                                continue
                            if str(dsmax[size]["window_size"][index]) != str(window_size):
                                continue
                            if str(dsmax[size]["vehicle"][index]) != str(subdir_name):
                                continue
                            if str(dsmax[size]["ride"][index]) != str(only_number):
                                continue  
                            #print("Located dist", size)
                            for key_name in dsmax[size].head(): 
                                if key_name in header:
                                    continue
                                if "offset" not in key_name:
                                    continue
                                if "only offset" in key_name:
                                    continue
                                dict_for_clustering[window_size][subdir_name][some_file][x][str(size) + "all_distances_scaled_to_max_trajs_distances_" + key_name] = dsmax[size][key_name][index]
                                #dict_for_clustering[window_size][subdir_name][some_file][x][str(size) + "all_distances_scaled_trajs_distances_" + key_name] = dsc[size][key_name][index]
                                #dict_for_clustering[window_size][subdir_name][some_file][x][str(size) + "all_distances_trajs_distances_" + key_name] = d[size][key_name][index]
                                #dict_for_clustering[window_size][subdir_name][some_file][x][str(size) + "all_distances_preprocesssed_trajs_distances_" + key_name] = dpp[size][key_name][index]

                        #print(len(dict_for_clustering[window_size][subdir_name][some_file][x]))
                        #print("Located num", size)
 
                        if x in nsmax[size]:
                            for key_name in nsmax[size][x]:
                                if key_name != "offset":
                                    continue
                                dict_for_clustering[window_size][subdir_name][some_file][x][str(size) + "all_nums_scaled_to_max_trajs_num_intersections_" + key_name] = nsmax[size][x][key_name]
                                #dict_for_clustering[window_size][subdir_name][some_file][x][str(size) + "all_nums_scaled_trajs_num_intersections_" + key_name] = nsc[size][x][key_name]
                                #dict_for_clustering[window_size][subdir_name][some_file][x][str(size) + "all_nums_trajs_num_intersections_" + key_name] = n[size][x][key_name]
                                #dict_for_clustering[window_size][subdir_name][some_file][x][str(size) + "all_nums_preprocesssed_trajs_num_intersections_" + key_name] = npp[size][x][key_name]

                        #print(len(dict_for_clustering[window_size][subdir_name][some_file][x]))
    
                print(len(dict_for_clustering[window_size][subdir_name][some_file][x].keys()))
                for k in dict_for_clustering[window_size][subdir_name][some_file][x]:
                    print(k)
                    printed = True
                if printed:
                    break
            if printed:
                break
        if printed:
            break

#for subdirname in os.listdir("all_clus"):
for subdirname in ["all_poly_flags"]:
    print(subdirname)
    make_clusters_multi_feats()