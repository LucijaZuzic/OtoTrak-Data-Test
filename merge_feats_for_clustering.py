from utilities import * 
from sklearn.manifold import TSNE

subdirname = "no_rays_flags"

def one_clusters(type_clus, attempt, train_arr, test_arr, clus_params, sd_subdir_train, sd_ride_train, sd_start_train, sd_window_train, sd_subdir_test, sd_ride_test, sd_start_test, sd_window_test):
    clus_train = attempt.fit(train_arr)
    train_labels = clus_train.labels_ 
       
    train_embedded = TSNE(n_components=2).fit_transform(train_arr)
    test_embedded = TSNE(n_components=2).fit_transform(test_arr)

    dict_train_by_label = dict()
    for label in train_labels:
        dict_train_by_label[label] = {"x": [], "y": []}
	
    filenames_in_cluster_train = dict()
    for label_index in range(len(train_labels)):
        label = train_labels[label_index]
        dict_train_by_label[label]["x"].append(float(train_embedded[label_index][0]))
        dict_train_by_label[label]["y"].append(float(train_embedded[label_index][1]))
        if label not in filenames_in_cluster_train:
            filenames_in_cluster_train[label] = []
        filenames_in_cluster_train[label].append({"short_name": sd_subdir_train[label_index] + "/" + sd_ride_train[label_index], "window": sd_window_train[label_index], "start": sd_start_train[label_index]})
	
    if type_clus == "KMeans":
        clus_test = attempt.predict(test_arr) 
        test_labels = clus_test
    if type_clus == "DBSCAN":
        clus_test = attempt.fit_predict(test_arr) 
        test_labels = clus_test

    dict_test_by_label = dict()
    for label in clus_test:
        dict_test_by_label[label] = {"x": [], "y": []}
	
    filenames_in_cluster_test = dict()
    for label_index in range(len(clus_test)):
        label = clus_test[label_index]
        dict_test_by_label[label]["x"].append(test_embedded[label_index][0])
        dict_test_by_label[label]["y"].append(test_embedded[label_index][1])
        if label not in filenames_in_cluster_test:
            filenames_in_cluster_test[label] = []
        filenames_in_cluster_test[label].append({"short_name": sd_subdir_test[label_index] + "/" + sd_ride_test[label_index], "window": sd_window_test[label_index], "start": sd_start_test[label_index]})
	
    random_colors_set = random_colors(len(set(dict_train_by_label.keys()).union(set(dict_test_by_label.keys()))))
    random_colors_dict = dict()
    index_num = 0
    for label in set(dict_train_by_label.keys()).union(set(dict_test_by_label.keys())):
        random_colors_dict[label] = random_colors_set[index_num]
        index_num += 1
 
    plt.rcParams.update({'font.size': 22})
    plt.figure(figsize=(20, 10))
    plt.subplot(1, 2, 1)
    label_index = 0 
    for label in dict_train_by_label:  
        plt.title(type_clus + " train " + str(clus_params))  
        plt.scatter(dict_train_by_label[label]["x"], dict_train_by_label[label]["y"], color = random_colors_dict[label], label = str(label) + " train")   
        label_index += 1 
    plt.legend()
    plt.subplot(1, 2, 2) 
    label_index = 0
    for label in dict_test_by_label:  
        plt.title(type_clus + " test " + str(clus_params))    
        plt.scatter(dict_test_by_label[label]["x"], dict_test_by_label[label]["y"], color = random_colors_dict[label], label = str(label) + " test")  
        label_index += 1
    plt.legend()
    if not os.path.isdir("all_clus/" + subdirname + "/plots/"):
        os.makedirs("all_clus/" + subdirname + "/plots/")
    plt.savefig("all_clus/" + subdirname + "/plots/" + type_clus + " test " + str(clus_params) + ".png") 
    plt.close()

    score_train = "undefined"
    if len(dict_train_by_label) > 1:
        score_train = silhouette_score(train_arr, train_labels)
		
    score_test = "undefined"
    if len(dict_test_by_label) > 1:
        score_test = silhouette_score(test_arr, test_labels) 
 
    if not os.path.isdir("all_clus/" + subdirname + "/filenames/"):
        os.makedirs("all_clus/" + subdirname + "/filenames/")
	
    save_object("all_clus/" + subdirname + "/filenames/filenames_in_cluster_train " + type_clus + " test  " + str(clus_params), filenames_in_cluster_train)
    save_object("all_clus/" + subdirname + "/filenames/filenames_in_cluster_test " + type_clus + " test " + str(clus_params), filenames_in_cluster_test) 
    if type_clus == "KMeans":
        return attempt.inertia_, score_train, score_test 
    if type_clus == "DBSCAN":
        return score_train, score_test 

def make_clusters(type_clus, sd_window_train, sd_subdir_train, sd_ride_train, sd_start_train, sd_x_train, sd_window_test, sd_subdir_test, sd_ride_test, sd_start_test, sd_x_test):
	 
    vals_clus = range(2, 15)   
    
    inertia_list = []
    silhouette_list_train = []
    silhouette_list_test = []
    vals_clus_sil_train = []
    vals_clus_sil_test = [] 

    for val_clus in vals_clus:
        if type_clus == "KMeans":
            attempt = KMeans(n_clusters = val_clus, random_state = 42) 
            inertia_val, siltrain, siltest = one_clusters(type_clus, attempt, sd_x_train, sd_x_test, "nclus " + str(val_clus), sd_subdir_train, sd_ride_train, sd_start_train, sd_window_train, sd_subdir_test, sd_ride_test, sd_start_test, sd_window_test)
            inertia_list.append(inertia_val)

        if type_clus == "DBSCAN": 
            new_eps = kneefind(int(len(sd_x_train) // val_clus), sd_x_train)
            attempt = DBSCAN(min_samples = int(len(sd_x_train) // val_clus), eps = new_eps) 
            siltrain, siltest = one_clusters(type_clus, attempt, sd_x_train, sd_x_test, "nclus " + str(val_clus), sd_subdir_train, sd_ride_train, sd_start_train, sd_window_train, sd_subdir_test, sd_ride_test, sd_start_test, sd_window_test)
  
        if siltrain != "undefined":
            silhouette_list_train.append(siltrain)
            vals_clus_sil_train.append(val_clus)

        if siltest != "undefined":
            silhouette_list_test.append(siltest) 
            vals_clus_sil_test.append(val_clus)

    if len(silhouette_list_train) > 0:
        print(max(silhouette_list_train), vals_clus_sil_train[silhouette_list_train.index(max(silhouette_list_train))])
   
    if len(silhouette_list_test) > 0:
        print(max(silhouette_list_test), vals_clus_sil_test[silhouette_list_test.index(max(silhouette_list_test))])	
     
def divide_train_test(properties, train_set, test_set): 
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
  
    for window_size in properties:
        for subdir_name in properties[window_size]:
            for some_file in properties[window_size][subdir_name]:
                for start in properties[window_size][subdir_name][some_file]: 
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
    
    for rn in range(len(sd_x_train)):
        for cn in range(len(sd_x_train[rn])):
            sd_x_train[rn][cn] = float(sd_x_train[rn][cn])
     
    for rn in range(len(sd_x_test)):
        for cn in range(len(sd_x_test[rn])):
            sd_x_test[rn][cn] = float(sd_x_test[rn][cn])

    sd_x_train = np.array(sd_x_train)
    sd_x_test = np.array(sd_x_test)

    print(np.shape(sd_x_train), np.shape(sd_x_test))
    return sd_window_train, sd_subdir_train, sd_ride_train, sd_start_train, sd_x_train, sd_window_test, sd_subdir_test, sd_ride_test, sd_start_test, sd_x_test 
    
window_size = 20
deg = 5
maxoffset = 0.005
step_size = window_size
#step_size = 1 

header = ["start", "window_size", "vehicle", "ride"] 
skip = ["key","flip","zone","engine","in_zone","ignition","sleep_mode","staff_mode","buzzer_active","in_primary_zone","in_restricted_zone","onboard_geofencing","speed_limit_active"]
all_subdirs = os.listdir() 

def make_clusters_multi_feats():
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
    
    sd_window_train, sd_subdir_train, sd_ride_train, sd_start_train, sd_x_train, sd_window_test, sd_subdir_test, sd_ride_test, sd_start_test, sd_x_test  = divide_train_test(dict_for_clustering, train_rides, test_rides)
    print(len(sd_x_train), len(sd_x_train[0]), sd_x_train[0][:10])
    print(len(sd_x_test))
    make_clusters("KMeans", sd_window_train, sd_subdir_train, sd_ride_train, sd_start_train, sd_x_train, sd_window_test, sd_subdir_test, sd_ride_test, sd_start_test, sd_x_test)
    make_clusters("DBSCAN", sd_window_train, sd_subdir_train, sd_ride_train, sd_start_train, sd_x_train, sd_window_test, sd_subdir_test, sd_ride_test, sd_start_test, sd_x_test)

make_clusters_multi_feats()

def read_clusters():
    for filename in os.listdir("all_clus/" + subdirname + "/filenames"):
        random_sample_of_cluster(subdirname, load_object("all_clus/" + subdirname + "/filenames/" + filename), 100, 100, filename)

read_clusters()