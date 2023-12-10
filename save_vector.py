from utilities import * 
from sklearn.manifold import TSNE
 
def divide_train_test_new(properties, train_set, test_set): 
    sd_window_train = []
    sd_subdir_train = []
    sd_ride_train = []
    sd_start_train = []
    sd_x_train = [] 

    sd_window_test = []
    sd_subdir_test = []
    sd_ride_test = []
    sd_start_test = []
    sd_x_test = []
    feat_names = []
    feat_array_test = dict()
    feat_array_train = dict()
    feat_array = dict()

    for window_size in properties:
        for subdir_name in properties[window_size]:
            for some_file in properties[window_size][subdir_name]:
                for start in properties[window_size][subdir_name][some_file]: 
                    feat_names = list(properties[window_size][subdir_name][some_file][start].keys())
                    for feat in feat_names:
                        if feat not in feat_array_test:
                            feat_array_test[feat] = []
                        if feat not in feat_array_train:
                            feat_array_train[feat] = []
                        if feat not in feat_array:
                            feat_array[feat] = []
                    if some_file in train_set:
                        sd_window_train.append(window_size)
                        sd_subdir_train.append(subdir_name)
                        sd_ride_train.append(some_file)
                        sd_start_train.append(start)
                        sd_x_train.append([]) 
                        for variable_name in properties[window_size][subdir_name][some_file][start]: 
                             
                            if "monoto" not in variable_name:
                                if math.isnan(properties[window_size][subdir_name][some_file][start][variable_name]):
                                    sd_x_train[-1].append(0)
                                else:
                                    sd_x_train[-1].append(properties[window_size][subdir_name][some_file][start][variable_name]) 
                            else:
                                if properties[window_size][subdir_name][some_file][start] == "I":
                                    sd_x_train[-1].append(3)
                                if properties[window_size][subdir_name][some_file][start] == "D":
                                    sd_x_train[-1].append(2)
                                if properties[window_size][subdir_name][some_file][start] == "NM":
                                    sd_x_train[-1].append(1)
                                if properties[window_size][subdir_name][some_file][start] == "NF":
                                    sd_x_train[-1].append(0)

                            feat_array[variable_name].append(sd_x_train[-1][-1])
                            feat_array_train[variable_name].append(sd_x_train[-1][-1])

                    if some_file in test_set:
                        sd_window_test.append(window_size)
                        sd_subdir_test.append(subdir_name)
                        sd_ride_test.append(some_file)
                        sd_start_test.append(start)
                        sd_x_test.append([])
                        for variable_name in properties[window_size][subdir_name][some_file][start]: 
                            if "monoto" not in variable_name:
                                if math.isnan(properties[window_size][subdir_name][some_file][start][variable_name]):
                                    sd_x_test[-1].append(0)
                                else:
                                    sd_x_test[-1].append(properties[window_size][subdir_name][some_file][start][variable_name]) 
                            else:
                                if properties[window_size][subdir_name][some_file][start] == "I":
                                    sd_x_test[-1].append(3)
                                if properties[window_size][subdir_name][some_file][start] == "D":
                                    sd_x_test[-1].append(2)
                                if properties[window_size][subdir_name][some_file][start] == "NM":
                                    sd_x_test[-1].append(1)
                                if properties[window_size][subdir_name][some_file][start] == "NF":
                                    sd_x_test[-1].append(0)

                            feat_array[variable_name].append(sd_x_test[-1][-1])
                            feat_array_test[variable_name].append(sd_x_test[-1][-1])
    
    for rn in range(len(sd_x_train)):
        for cn in range(len(sd_x_train[rn])):
            sd_x_train[rn][cn] = float(sd_x_train[rn][cn])
     
    for rn in range(len(sd_x_test)):
        for cn in range(len(sd_x_test[rn])):
            sd_x_test[rn][cn] = float(sd_x_test[rn][cn])

    sd_x_train = np.array(sd_x_train)
    sd_x_test = np.array(sd_x_test)

    print(np.shape(sd_x_train), np.shape(sd_x_test))
    return feat_names, feat_array, feat_array_train, feat_array_test, sd_window_train, sd_subdir_train, sd_ride_train, sd_start_train, sd_x_train, sd_window_test, sd_subdir_test, sd_ride_test, sd_start_test, sd_x_test 
    
window_size = 20
deg = 5
maxoffset = 0.005
step_size = window_size
#step_size = 1 

header = ["start", "window_size", "vehicle", "ride"] 
all_subdirs = os.listdir() 

#open_feats_acceler_scaled = pd.read_csv("all_feats_acceler/all_feats_acceler_scaled.csv", index_col = False)
open_feats_acceler_scaled_max = pd.read_csv("all_feats_acceler/all_feats_acceler_scaled_to_max.csv", index_col = False)
#open_feats_acceler = pd.read_csv("all_feats_acceler/all_feats_acceler.csv", index_col = False)

#open_feats_heading_scaled = pd.read_csv("all_feats_heading/all_feats_heading_scaled.csv", index_col = False)
open_feats_heading_scaled_max = pd.read_csv("all_feats_heading/all_feats_heading_scaled_to_max.csv", index_col = False)
#open_feats_heading = pd.read_csv("all_feats_heading/all_feats_heading.csv", index_col = False)
 
def save_a_cluster_vector(subdirname):
    dict_for_clustering= dict()
    dict_for_clustering[window_size] = dict()
    train_names = set()
    test_names = set()   
    for subdir_name in all_subdirs:
 
        if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
            continue
        print(subdir_name)
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

                if "acceler" in subdirname:

                    for index in range(len(open_feats_acceler_scaled_max["start"])):
                        if str(open_feats_acceler_scaled_max["start"][index]) != str(x):
                            continue
                        if str(open_feats_acceler_scaled_max["window_size"][index]) != str(window_size):
                            continue
                        if str(open_feats_acceler_scaled_max["vehicle"][index]) != str(subdir_name):
                            continue
                        if str(open_feats_acceler_scaled_max["ride"][index]) != str(only_number):
                            continue  
                        #print("Located feats")
                        for key_name in open_feats_acceler_scaled_max.head(): 
                            if key_name in header:
                                continue 
                            if "Unnamed" in key_name:
                                continue
                            #dict_for_clustering[window_size][subdir_name][some_file][x]["all_feats_acceler_scaled_" + key_name] = open_feats_acceler_scaled[key_name][index]
                            dict_for_clustering[window_size][subdir_name][some_file][x]["all_feats_acceler_scaled_to_max_" + key_name] = open_feats_acceler_scaled_max[key_name][index]
                            #dict_for_clustering[window_size][subdir_name][some_file][x]["all_feats_acceler_" + key_name] = open_feats_acceler[key_name][index]
                    
                    #print(len(dict_for_clustering[window_size][subdir_name][some_file][x]))
                
                if "heading" in subdirname:

                    for index in range(len(open_feats_heading_scaled_max["start"])):
                        if str(open_feats_heading_scaled_max["start"][index]) != str(x):
                            continue
                        if str(open_feats_heading_scaled_max["window_size"][index]) != str(window_size):
                            continue
                        if str(open_feats_heading_scaled_max["vehicle"][index]) != str(subdir_name):
                            continue
                        if str(open_feats_heading_scaled_max["ride"][index]) != str(only_number):
                            continue  
                        #print("Located feats")
                        for key_name in open_feats_heading_scaled_max.head(): 
                            if key_name in header:
                                continue 
                            if "Unnamed" in key_name:
                                continue
                            #dict_for_clustering[window_size][subdir_name][some_file][x]["all_feats_heading_scaled_" + key_name] = open_feats_heading_scaled[key_name][index]
                            dict_for_clustering[window_size][subdir_name][some_file][x]["all_feats_heading_scaled_to_max_" + key_name] = open_feats_heading_scaled_max[key_name][index]
                            #dict_for_clustering[window_size][subdir_name][some_file][x]["all_feats_heading_" + key_name] = open_feats_heading[key_name][index]
                    
                    #print(len(dict_for_clustering[window_size][subdir_name][some_file][x]))
                 
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
                            if key_name in flag_names and "flags" not in subdirname:
                                continue 
                            if "poly" in key_name and "poly" not in subdirname:
                                continue 
                            if "same" in key_name and "no_same" in subdirname:
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
 
    save_object("dict_for_clustering", dict_for_clustering)
    save_object("train_rides", train_rides)
    save_object("test_rides", test_rides)
    return divide_train_test_new(dict_for_clustering, train_rides, test_rides)

subdirname = "all_poly_flags_acceler_heading" 
feat_names, feat_array, feat_array_train, feat_array_test, sd_window_train, sd_subdir_train, sd_ride_train, sd_start_train, sd_x_train, sd_window_test, sd_subdir_test, sd_ride_test, sd_start_test, sd_x_test = save_a_cluster_vector(subdirname)

save_object("feat_names", feat_names)
save_object("feat_array", feat_array)
save_object("feat_array_train", feat_array_train)
save_object("feat_array_test", feat_array_test)

save_object("sd_window_train", sd_window_train)
save_object("sd_subdir_train", sd_subdir_train)
save_object("sd_ride_train", sd_ride_train)
save_object("sd_start_train", sd_start_train)
save_object("sd_x_train", sd_x_train)

save_object("sd_window_test", sd_window_test)
save_object("sd_subdir_test", sd_subdir_test)
save_object("sd_ride_test", sd_ride_test)
save_object("sd_start_test", sd_start_test)
save_object("sd_x_test", sd_x_test)

feat_array = load_object("feat_array")
feat_names = list(feat_array.keys())
feat_var = dict() 
feat_var_scaled = dict() 
feat_std = dict() 
feat_std_scaled = dict() 
for feat in feat_names:
    varia = np.var(feat_array[feat]) 
    mini = min(feat_array[feat])
    maxi = max(feat_array[feat])
    if maxi == True:
        maxi = 1
    if mini == False:
        mini = 0
    stdevi = np.std(feat_array[feat]) 
    rangev = maxi - mini 

    feat_var[feat] = varia
    if rangev != 0:
        feat_var_scaled[feat] = varia / (rangev ** 2)

    feat_std[feat] = stdevi 
    if rangev != 0:
        feat_std_scaled[feat] = stdevi / rangev

for feat in dict(sorted(feat_std_scaled.items(), key=lambda item: item[1])): 
    print(feat, feat_std_scaled[feat], np.min(feat_array[feat]), np.max(feat_array[feat]), feat_std[feat], sum(feat_array[feat]) / len(feat_array[feat]), np.average(feat_array[feat]))
print("")
for feat in dict(sorted(feat_var_scaled.items(), key=lambda item: item[1])):
    print(feat, feat_var_scaled[feat], np.min(feat_array[feat]), np.max(feat_array[feat]), feat_var[feat], sum(feat_array[feat]) / len(feat_array[feat]), np.average(feat_array[feat]))