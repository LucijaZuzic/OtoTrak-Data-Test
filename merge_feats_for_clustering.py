from utilities import * 
from sklearn.manifold import TSNE
 
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
            filenames_in_cluster_train[label] = dict()
        filenames_in_cluster_train[label][sd_subdir_train[label_index] + "/" + sd_ride_train[label_index]] = {"window": sd_window_train[label_index], "start": sd_start_train[label_index]}
	
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
            filenames_in_cluster_test[label] = dict()
        filenames_in_cluster_test[label][sd_subdir_test[label_index] + "/" + sd_ride_test[label_index]] = {"window": sd_window_test[label_index], "start": sd_start_test[label_index]}
	
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
    if not os.path.isdir("all_clus/plots/"):
        os.makedirs("all_clus/plots/")
    plt.savefig("all_clus/plots/" + type_clus + " test " + str(clus_params) + ".png") 
    plt.close()

    score_train = "undefined"
    if len(dict_train_by_label) > 1:
        score_train = silhouette_score(train_arr, train_labels)
		
    score_test = "undefined"
    if len(dict_test_by_label) > 1:
        score_test = silhouette_score(test_arr, test_labels) 
 
    if not os.path.isdir("all_clus/filenames/"):
        os.makedirs("all_clus/filenames/")
	
    save_object("all_clus/filenames/filenames_in_cluster_train " + type_clus + " test  " + str(clus_params), filenames_in_cluster_train)
    save_object("all_clus/filenames/filenames_in_cluster_test " + type_clus + " test " + str(clus_params), filenames_in_cluster_test)
    #random_sample_of_cluster(filenames_in_cluster_train, 3)
    #random_sample_of_cluster(filenames_in_cluster_test, 3)
    if type_clus == "KMeans":
        return attempt.inertia_, score_train, score_test 
    if type_clus == "DBSCAN":
        return score_train, score_test 

def make_clusters(type_clus, sd_window_train, sd_subdir_train, sd_ride_train, sd_start_train, sd_x_train, sd_window_test, sd_subdir_test, sd_ride_test, sd_start_test, sd_x_test):
	 
	vals_clus = range(2, 15) 
	vals_nn = [int(len(sd_x_train) // val_clus) for val_clus in vals_clus]  
	vals_eps_range = np.arange(0.005, 0.015, 0.001)
	index_clustering = 0

	if type_clus == "KMeans":

		inertia_list = []
		silhouette_list_train = []
		silhouette_list_test = []
		vals_clus_sil_train = []
		vals_clus_sil_test = [] 

		for val_clus in vals_clus:
			attempt = KMeans(n_clusters = val_clus, random_state = 42) 
			inertia_val, siltrain, siltest = one_clusters(type_clus, attempt, sd_x_train, sd_x_test, "nclus " + str(val_clus), sd_subdir_train, sd_ride_train, sd_start_train, sd_window_train, sd_subdir_test, sd_ride_test, sd_start_test, sd_window_test)

			inertia_list.append(inertia_val)

			if siltrain != "undefined":
				silhouette_list_train.append(siltrain)
				vals_clus_sil_train.append(val_clus)

			if siltest != "undefined":
				silhouette_list_test.append(siltest) 
				vals_clus_sil_test.append(val_clus)
 
	if type_clus == "DBSCAN": 

		inertia_list = dict()
		silhouette_list_train = dict()
		silhouette_list_test = dict()
		vals_clus_sil_train = dict()
		vals_clus_sil_test = dict()

		index_clustering = 0
		for val_nn in vals_nn:
			silhouette_list_train[vals_clus] = []
			silhouette_list_test[vals_clus] = []
			vals_clus_sil_train[vals_clus] = []
			vals_clus_sil_test[vals_clus] = []
			new_eps_vals = [eps_val for eps_val in vals_eps_range]
			new_eps = kneefind(val_nn, sd_x_train)
			print(vals_clus[index_clustering], val_nn, new_eps)
			new_eps_vals.append(new_eps)
			new_eps_vals.sort()
			for val_eps in new_eps_vals: 
				attempt = DBSCAN(eps = val_eps, min_samples = val_nn) 
				if val_eps != new_eps:
					siltrain, siltest = one_clusters(type_clus, attempt, sd_x_train, sd_x_test, "nn " + str(val_nn) + " eps " + str(np.round(val_eps, 3)), sd_subdir_train, sd_ride_train, sd_start_train, sd_window_train, sd_subdir_test, sd_ride_test, sd_start_test, sd_window_test) 
				else:
					siltrain, siltest = one_clusters(type_clus, attempt, sd_x_train, sd_x_test, "nn " + str(val_nn) + " best eps " + str(np.round(val_eps, 3)), sd_subdir_train, sd_ride_train, sd_start_train, sd_window_train, sd_subdir_test, sd_ride_test, sd_start_test, sd_window_test) 

				if siltrain != "undefined":
					silhouette_list_train[vals_clus].append(siltrain)
					vals_clus_sil_train[vals_clus].append(val_eps)

				if siltest != "undefined":
					silhouette_list_test[vals_clus].append(siltest) 
					vals_clus_sil_test[vals_clus].append(val_eps)
  
			index_clustering += 1
			 
	if type_clus == "KMeans":
		#plt.title(type_clus + " inertia")
		#plt.plot(vals_clus, inertia_list)
		#plt.show()
		#plt.close()

		#kl = KneeLocator(vals_clus, inertia_list, curve = "convex", direction = "decreasing")
		#print(kl.knee_y)

		#plt.title(type_clus + " silhouette train")
		#plt.plot(vals_clus_sil_train, silhouette_list_train)
		#plt.show()
		#plt.close()

		#plt.title(type_clus + " silhouette test")
		#plt.plot(vals_clus_sil_test, silhouette_list_test)
		#plt.show()
		#plt.close()

		print(max(silhouette_list_train), vals_clus_sil_train[silhouette_list_train.index(max(silhouette_list_train))])
		print(max(silhouette_list_test), vals_clus_sil_test[silhouette_list_test.index(max(silhouette_list_test))])	

	if type_clus == "DBSCAN":

		for val_clus in vals_clus_sil_train:

			#plt.title(type_clus + " silhouette train nclus " + str(val_clus))
			#plt.plot(vals_clus_sil_train[val_clus], silhouette_list_train[val_clus])
			#plt.show()
			#plt.close()

			print(max(silhouette_list_test[val_clus]), vals_clus_sil_test[val_clus][silhouette_list_test[val_clus].index(max(silhouette_list_test[val_clus]))])	

		for val_clus in vals_clus_sil_test:

			#plt.title(type_clus + " silhouette test nclus " + str(val_clus))
			#plt.plot(vals_clus_sil_test[val_clus], silhouette_list_test[val_clus])
			#plt.show()
			#plt.close()
 
			print(max(silhouette_list_train[val_clus]), vals_clus_sil_train[val_clus][silhouette_list_train[val_clus].index(max(silhouette_list_train[val_clus]))])
 
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
all_subdirs = os.listdir() 

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
        
    for some_file in all_files:  
        if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames:
            continue 
        dict_for_clustering[window_size][subdir_name][some_file] = dict()
  
for subdir_name in all_subdirs:

    trajs_in_dir = 0
    
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

        only_num_ride = some_file.replace(".csv", "").replace("events_", "")
        
        trajs_in_ride = 0
 
        file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
        longitudes = list(file_with_ride["fields_longitude"])
        latitudes = list(file_with_ride["fields_latitude"]) 
        times = list(file_with_ride["time"])   

        open_feats_scaled = pd.read_csv("all_feats/all_feats_scaled_" + subdir_name + ".csv", index_col = False)
        open_feats_scaled_max = pd.read_csv("all_feats/all_feats_scaled_to_max_" + subdir_name + ".csv", index_col = False)
        open_feats = pd.read_csv("all_feats/all_feats_" + subdir_name + ".csv", index_col = False)
         
        if some_file in train_rides:
            train_names.add(some_file)

        if some_file in test_rides:
            test_names.add(some_file) 
			
        for x in range(0, len(longitudes) - window_size + 1, step_size): 

            #print(x)
            dict_for_clustering[window_size][subdir_name][some_file][x] = dict()

            only_number = some_file.replace(".csv", "").replace("events_", "")   
            for index in range(len(open_feats_scaled["start"])):
                if str(open_feats_scaled["start"][index]) != str(x):
                    continue
                if str(open_feats_scaled["window_size"][index]) != str(window_size):
                    continue
                if str(open_feats_scaled["vehicle"][index]) != str(subdir_name):
                    continue
                if str(open_feats_scaled["ride"][index]) != str(only_number):
                    continue  
                #print("Located feats")
                for key_name in open_feats_scaled.head(): 
                    if key_name in header:
                        continue
                    dict_for_clustering[window_size][subdir_name][some_file][x]["all_feats_scaled_" + key_name] = open_feats_scaled[key_name][index]
                    dict_for_clustering[window_size][subdir_name][some_file][x]["all_feats_scaled_to_max_" + key_name] = open_feats_scaled_max[key_name][index]
                    dict_for_clustering[window_size][subdir_name][some_file][x]["all_feats_" + key_name] = open_feats[key_name][index]
                
            #print(len(dict_for_clustering[window_size][subdir_name][some_file][x]))

            #for size in os.listdir("rays"):
            for size in ["4", "8", "12", "16", "20", "24", "28", "36"]:
                start_path = "rays/" + str(size) + "/" + subdir_name + "/" + only_number
                dsmax = pd.read_csv(start_path + "/all_distances_scaled_to_max_trajs.csv", index_col = False)
                dsc = pd.read_csv(start_path + "/all_distances_scaled_trajs.csv", index_col = False)
                dpp = pd.read_csv(start_path + "/all_distances_preprocessed_trajs.csv", index_col = False)
                d = pd.read_csv(start_path + "/all_distances_trajs.csv", index_col = False)
             
                for index in range(len(dsmax["start"])):
                    if str(dsmax["start"][index]) != str(x):
                        continue
                    if str(dsmax["window_size"][index]) != str(window_size):
                        continue
                    if str(dsmax["vehicle"][index]) != str(subdir_name):
                        continue
                    if str(dsmax["ride"][index]) != str(only_number):
                        continue  
                    #print("Located dist", size)
                    for key_name in dsmax.head(): 
                        if key_name in header:
                            continue
                        dict_for_clustering[window_size][subdir_name][some_file][x][str(size) + "all_distances_scaled_to_max_trajs_distances_" + key_name] = dsmax[key_name][index]
                        dict_for_clustering[window_size][subdir_name][some_file][x][str(size) + "all_distances_scaled_trajs_distances_" + key_name] = dsc[key_name][index]
                        dict_for_clustering[window_size][subdir_name][some_file][x][str(size) + "all_distances_trajs_distances_" + key_name] = d[key_name][index]
                        dict_for_clustering[window_size][subdir_name][some_file][x][str(size) + "all_distances_preprocesssed_trajs_distances_" + key_name] = dpp[key_name][index]

                #print(len(dict_for_clustering[window_size][subdir_name][some_file][x]))
                #print("Located num", size)

                nsmax = load_object(start_path + "/all_nums_scaled_to_max_trajs")
                nsc = load_object(start_path + "/all_nums_scaled_trajs")
                npp = load_object(start_path + "/all_nums_preprocessed_trajs")
                n = load_object(start_path + "/all_nums_trajs") 
                if x in nsmax:
                    for key_name in nsmax[x]:
                        dict_for_clustering[window_size][subdir_name][some_file][x][str(size) + "all_nums_scaled_to_max_trajs_num_intersections_" + key_name] = nsmax[x][key_name]
                        dict_for_clustering[window_size][subdir_name][some_file][x][str(size) + "all_nums_scaled_trajs_num_intersections_" + key_name] = nsc[x][key_name]
                        dict_for_clustering[window_size][subdir_name][some_file][x][str(size) + "all_nums_trajs_num_intersections_" + key_name] = n[x][key_name]
                        dict_for_clustering[window_size][subdir_name][some_file][x][str(size) + "all_nums_preprocesssed_trajs_num_intersections_" + key_name] = npp[x][key_name]

                #print(len(dict_for_clustering[window_size][subdir_name][some_file][x]))
 
sd_window_train, sd_subdir_train, sd_ride_train, sd_start_train, sd_x_train, sd_window_test, sd_subdir_test, sd_ride_test, sd_start_test, sd_x_test  = divide_train_test(dict_for_clustering, train_rides, test_rides)
print(len(sd_x_train), len(sd_x_train[0]), sd_x_train[0][:10])
print(len(sd_x_test))
make_clusters("KMeans", sd_window_train, sd_subdir_train, sd_ride_train, sd_start_train, sd_x_train, sd_window_test, sd_subdir_test, sd_ride_test, sd_start_test, sd_x_test)
make_clusters("DBSCAN", sd_window_train, sd_subdir_train, sd_ride_train, sd_start_train, sd_x_train, sd_window_test, sd_subdir_test, sd_ride_test, sd_start_test, sd_x_test)