from utilities import *
from sklearn.manifold import TSNE
from knees import kneefind
location_vehicles = dict()
vehicle_location = dict()
dict_for_clustering = load_object("dict_for_clustering")
window_size = 20
all_subdirs = os.listdir()
for subdir_name in all_subdirs:
 
        if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
            continue
        dict_for_clustering[window_size][subdir_name] = dict()
        
        all_files = os.listdir(subdir_name + "/cleaned_csv/")  
        for some_file in all_files:   
            file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
            location_veh = file_with_ride["location_id"][0]
            break
        if location_veh not in location_vehicles:
            location_vehicles[location_veh] = []
        location_vehicles[location_veh].append(subdir_name)
        vehicle_location[subdir_name] = location_veh
print(location_vehicles)
print(vehicle_location)
save_object("location_vehicles", location_vehicles)
save_object("vehicle_location", vehicle_location)

def one_location_clus(type_clus, attempt, train_arr, test_arr, clus_params, sd_subdir_train, sd_ride_train, sd_start_train, sd_window_train, sd_subdir_test, sd_ride_test, sd_start_test, sd_window_test):
    clus_train = attempt.fit(train_arr)
    train_labels = clus_train.labels_ 
 
    if not os.path.isdir("all_location_clus/clus_train"):
        os.makedirs("all_location_clus/clus_train")
	
    save_object("all_location_clus/clus_train/clus_train_" + type_clus + " train " + str(clus_params), clus_train) 
       
    train_embedded = train_arr
    test_embedded = test_arr

    if len(train_arr[0]) > 2:
        train_embedded = TSNE(n_components=2).fit_transform(train_arr)
        test_embedded = TSNE(n_components=2).fit_transform(test_arr)
    
        if not os.path.isdir("all_location_clus/TSNE/"):
            os.makedirs("all_location_clus/TSNE/")
        
        save_object("all_location_clus/TSNE/TSNE_" + type_clus + " train " + str(clus_params), train_embedded)
        save_object("all_location_clus/TSNE/TSNE_" + type_clus + " test " + str(clus_params), test_embedded) 

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
 
    if not os.path.isdir("all_location_clus/clus_test"):
        os.makedirs("all_location_clus/clus_test")
	
    save_object("all_location_clus/clus_test/clus_test_" + type_clus + " test " + str(clus_params), clus_test) 

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
    if not os.path.isdir("all_location_clus/plots"):
        os.makedirs("all_location_clus/plots")
    plt.savefig("all_location_clus/plots/" + type_clus + " test " + str(clus_params) + ".png") 
    plt.close()

    score_train = "undefined"
    if len(dict_train_by_label) > 1:
        score_train = silhouette_score(train_arr, train_labels)
		
    score_test = "undefined"
    if len(dict_test_by_label) > 1:
        score_test = silhouette_score(test_arr, test_labels) 
  
    if not os.path.isdir("all_location_clus/filenames/"):
        os.makedirs("all_location_clus/filenames/")

    save_object("all_location_clus/filenames/filenames_in_cluster_train " + type_clus + " test " + str(clus_params), filenames_in_cluster_train)
    save_object("all_location_clus/filenames/filenames_in_cluster_test " + type_clus + " test " + str(clus_params), filenames_in_cluster_test) 
    
    if type_clus == "KMeans":
        return attempt.inertia_, score_train, score_test 
    if type_clus == "DBSCAN":
        return score_train, score_test 

def make_location_clus(type_clus, sd_window_train, sd_subdir_train, sd_ride_train, sd_start_train, sd_x_train, sd_window_test, sd_subdir_test, sd_ride_test, sd_start_test, sd_x_test):
	 
    vals_clus = range(15, 16)   
    
    inertia_list = []
    silhouette_list_train = []
    silhouette_list_test = []
    vals_clus_sil_train = []
    vals_clus_sil_test = [] 

    for val_clus in vals_clus:
        if type_clus == "KMeans":
            attempt = KMeans(n_clusters = val_clus, random_state = 42) 
            inertia_val, siltrain, siltest = one_location_clus(type_clus, attempt, sd_x_train, sd_x_test, "nclus " + str(val_clus), sd_subdir_train, sd_ride_train, sd_start_train, sd_window_train, sd_subdir_test, sd_ride_test, sd_start_test, sd_window_test)
            inertia_list.append(inertia_val)

        if type_clus == "DBSCAN": 
            new_eps = kneefind(int(len(sd_x_train) // val_clus), sd_x_train)
            attempt = DBSCAN(min_samples = int(len(sd_x_train) // val_clus), eps = new_eps) 
            siltrain, siltest = one_location_clus(type_clus, attempt, sd_x_train, sd_x_test, "nclus " + str(val_clus), sd_subdir_train, sd_ride_train, sd_start_train, sd_window_train, sd_subdir_test, sd_ride_test, sd_start_test, sd_window_test)
  
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
  
data_to_cluster_train = [] 
data_to_cluster_test = []

wtrain = []
vtrain = []
rtrain = []
strain = []

wtest = []
vtest = []
rtest = []
stest = []
 
for subdir_name in all_subdirs:
    if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
        continue
    print(subdir_name)
    
    all_files = os.listdir(subdir_name + "/cleaned_csv/") 
    bad_rides_filenames = dict()
    if os.path.isfile(subdir_name + "/bad_rides_filenames"):
        bad_rides_filenames = load_object(subdir_name + "/bad_rides_filenames")
    gap_rides_filenames = dict()
    if os.path.isfile(subdir_name + "/gap_rides_filenames"):
        gap_rides_filenames = load_object(subdir_name + "/gap_rides_filenames")
    train_rides = set()
    if os.path.isfile(subdir_name + "/train_rides"):
        train_rides = load_object(subdir_name + "/train_rides") 
        
    test_rides = set()
    if os.path.isfile(subdir_name + "/test_rides"):
        test_rides = load_object(subdir_name + "/test_rides")

    for some_file in all_files:  
        if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames:
            #print("Skipped ride", some_file)
            continue
        #print("Used ride", some_file)
    
        file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
        longitudes = list(file_with_ride["fields_longitude"])
        latitudes = list(file_with_ride["fields_latitude"])  
        times = list(file_with_ride["time"])  
        times_tmp_transform = transform_time(times)
        speeds_tmp = list(file_with_ride["fields_speed"])  
        headings = list(file_with_ride["fields_direction"])   

        accelers_ototrak_trajs = return_acceler_speeds(speeds_tmp, times_tmp_transform)   
        accelers_abs_ototrak_trajs = return_acceler_speeds(speeds_tmp, times_tmp_transform, True)  

        angles = return_angle_diffs(headings)   
        angles_speed = return_angle_diffs_time(headings, times_tmp_transform)

        if some_file in train_rides: 
            for i in range(len(accelers_ototrak_trajs)):
                wtrain.append(1)
                vtrain.append(subdir_name)
                rtrain.append(some_file)
                strain.append(i) 
                data_to_cluster_train.append([speeds_tmp[i], angles[i]]) 
        if some_file in test_rides: 
            for i in range(len(accelers_ototrak_trajs)):
                wtest.append(1)
                vtest.append(subdir_name)
                rtest.append(some_file)
                stest.append(i) 
                data_to_cluster_test.append([speeds_tmp[i], angles[i]]) 
              
data_to_cluster_test = np.array(data_to_cluster_test)
 
data_to_cluster_train = np.array(data_to_cluster_train)

#make_location_clus("DBSCAN", wtrain, vtrain, rtrain, strain, data_to_cluster_train, wtest, vtest, rtest, stest, data_to_cluster_test)
make_location_clus("KMeans", wtrain, vtrain, rtrain, strain, data_to_cluster_train, wtest, vtest, rtest, stest, data_to_cluster_test)

def random_sample_of_location_cluster(files_in_cluster, filename):
    print(filename)
    rcolors = random_colors(len(files_in_cluster) + 1)
    indc = 0
    rcolors_dict = dict()
    for cluster in files_in_cluster:
        rcolors_dict[cluster] = rcolors[indc]
        indc += 1
    points_from_traj_labels = dict()
 
    for cluster in files_in_cluster:
        for entry in files_in_cluster[cluster]:
            name_file = entry["short_name"]
            name_file_long = name_file.replace("/", "/cleaned_csv/") 
            pos = entry["start"]
            if name_file_long not in points_from_traj_labels:
                points_from_traj_labels[name_file_long] = dict()
            points_from_traj_labels[name_file_long][pos] = cluster 
            
    for subdir_name in all_subdirs:
        if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
            continue 
        
        all_files = os.listdir(subdir_name + "/cleaned_csv/") 
        bad_rides_filenames = dict()
        if os.path.isfile(subdir_name + "/bad_rides_filenames"):
            bad_rides_filenames = load_object(subdir_name + "/bad_rides_filenames")
        gap_rides_filenames = dict()
        if os.path.isfile(subdir_name + "/gap_rides_filenames"):
            gap_rides_filenames = load_object(subdir_name + "/gap_rides_filenames")
        train_rides = set()
        if os.path.isfile(subdir_name + "/train_rides"):
            train_rides = load_object(subdir_name + "/train_rides") 
            
        test_rides = set()
        if os.path.isfile(subdir_name + "/test_rides"):
            test_rides = load_object(subdir_name + "/test_rides")

        for some_file in all_files:  
            if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames:
                #print("Skipped ride", some_file)
                continue
            if some_file in train_rides and "_test" in filename:
                continue
            if some_file in test_rides and "_train" in filename:
                continue
            file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
            longitudes = list(file_with_ride["fields_longitude"])
            latitudes = list(file_with_ride["fields_latitude"]) 
            points_of_labels_x = dict()
            points_of_labels_y = dict()
            name_longer = subdir_name + "/cleaned_csv/" + some_file
            #print(name_longer, list(points_from_traj_labels.keys())[0])
            for i in range(len(longitudes)): 
                if name_longer in points_from_traj_labels and i in points_from_traj_labels[name_longer]: 
                    color_me = points_from_traj_labels[name_longer][i] 
                    if color_me not in points_of_labels_x:
                        points_of_labels_x[color_me] = []
                    points_of_labels_x[color_me].append(longitudes[i])
                    if color_me not in points_of_labels_y:
                        points_of_labels_y[color_me] = []
                    points_of_labels_y[color_me].append(latitudes[i]) 
            found = False
            for color_me in rcolors_dict:
                if color_me in points_of_labels_x and len(points_of_labels_x[color_me]) != 0:
                    plt.scatter(points_of_labels_x[color_me], points_of_labels_y[color_me], color = rcolors_dict[color_me], label = color_me)
                    found = True
            if found:
                plt.plot(longitudes, latitudes, color = rcolors[-1])
                plt.title(subdir_name + " " + some_file)
                plt.legend()
                if not os.path.isdir("all_location_clus/samples/" + filename + "/" + subdir_name):
                    os.makedirs("all_location_clus/samples/" + filename + "/" + subdir_name)
                plt.savefig("all_location_clus/samples/" + filename + "/" + subdir_name + "/" + filename + "_" + subdir_name + "_" + some_file + ".png", bbox_inches = "tight")
                plt.close()

for filename in os.listdir("all_location_clus/filenames/"):
    if "nclus 15" not in filename:
        continue
    random_sample_of_location_cluster(load_object("all_location_clus/filenames/" + filename), filename)