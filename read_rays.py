from utilities import *
from sympy import Matrix 
from sklearn.cluster import KMeans
from kneed import KneeLocator
from sklearn.metrics import silhouette_score
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors

def random_sample_of_cluster(files_in_cluster, num_to_sample):
	for cluster in files_in_cluster:
		if len(files_in_cluster[cluster]) > 0:
			indexes = np.random.randint(0, len(files_in_cluster[cluster]), size = num_to_sample)
			for index in indexes:
				name_file = list(files_in_cluster[cluster].keys())[index]
				print(len(files_in_cluster[cluster].keys()))
				print(name_file)
				long, lat, time = load_traj_window_name(name_file, files_in_cluster[cluster][name_file]["start"], files_in_cluster[cluster][name_file]["window"])
				long, lat = preprocess_long_lat(long, lat)
				long, lat = scale_long_lat(long, lat, 1, 1, True) 
				plt.title("Cluster " + str(cluster) + " " + str(name_file))
				plt.plot(long, lat)
				plt.show()
				plt.close()
			 
def kneefind(NN, X_embedded):
	nbrs = NearestNeighbors(n_neighbors = NN).fit(X_embedded)
	distances, indices = nbrs.kneighbors(X_embedded)
	distance_desc = sorted(distances[:,NN-1], reverse=True)
	#plt.plot(list(range(1,len(distance_desc)+1)), distance_desc)
	#plt.show()
	#plt.close()
	kl = KneeLocator(list(range(1,len(distance_desc )+1)), distance_desc, curve = "convex", direction = "decreasing") 
	return kl.knee_y

def scatter_me(sd_x, sd_y):
	for size in sd_x:
		for variable_name in sd_x[size]: 
			if variable_name != "offset":
				continue
			plt.title("size " + size + " " + variable_name)
			plt.scatter(sd_x[size][variable_name], sd_y[size][variable_name], color = 'b')
			plt.show()

def one_cluster(size, type_clus, attempt, train_arr, test_arr, variable_name, clus_params, sd_names_train, sd_start_train, sd_window_train, sd_names_test, sd_start_test, sd_window_test):
	clus_train = attempt.fit(train_arr)
	train_labels = clus_train.labels_

	dict_train_by_label = dict()
	for label in train_labels:
		dict_train_by_label[label] = {"x": [], "y": []}
	
	filenames_in_cluster_train = dict()
	for label_index in range(len(train_labels)):
		label = train_labels[label_index]
		dict_train_by_label[label]["x"].append(float(train_arr[label_index][0]))
		dict_train_by_label[label]["y"].append(float(train_arr[label_index][1]))
		if label not in filenames_in_cluster_train:
			filenames_in_cluster_train[label] = dict()
		filenames_in_cluster_train[label][sd_names_train[label_index]] = {"window": sd_window_train[label_index], "start": sd_start_train[label_index]}
	
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
		dict_test_by_label[label]["x"].append(test_arr[label_index][0])
		dict_test_by_label[label]["y"].append(test_arr[label_index][1])
		if label not in filenames_in_cluster_test:
			filenames_in_cluster_test[label] = dict()
		filenames_in_cluster_test[label][sd_names_test[label_index]] = {"window": sd_window_test[label_index], "start": sd_start_test[label_index]}
	
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
		plt.title(type_clus + " train size " + size + " " + variable_name + " " + str(clus_params))  
		plt.scatter(dict_train_by_label[label]["x"], dict_train_by_label[label]["y"], color = random_colors_dict[label], label = str(label) + " train")   
		label_index += 1 
	plt.legend()
	plt.subplot(1, 2, 2) 
	label_index = 0
	for label in dict_test_by_label:  
		plt.title(type_clus + " test size " + size + " " + variable_name + " " + str(clus_params))    
		plt.scatter(dict_test_by_label[label]["x"], dict_test_by_label[label]["y"], color = random_colors_dict[label], label = str(label) + " test")  
		label_index += 1
	plt.legend()
	if not os.path.isdir("rays/" + size + "/rays_plot/"):
		os.makedirs("rays/" + size + "/rays_plot/")
	plt.savefig("rays/" + size + "/rays_plot/" + type_clus + " test size " + size + " " + variable_name+ " " + str(clus_params) + ".png")
	plt.close()

	score_train = "undefined"
	if len(dict_train_by_label) > 1:
		score_train = silhouette_score(train_arr, train_labels)
		
	score_test = "undefined"
	if len(dict_test_by_label) > 1:
		score_test = silhouette_score(test_arr, test_labels) 
 
	if not os.path.isdir("rays/" + size + "/clustering/"):
		os.makedirs("rays/" + size + "/clustering/")
	
	save_object("rays/" + size + "/clustering/filenames_in_cluster_train " + type_clus + " test size " + size + " " + variable_name+ " " + str(clus_params), filenames_in_cluster_train)
	save_object("rays/" + size + "/clustering/filenames_in_cluster_test " + type_clus + " test size " + size + " " + variable_name+ " " + str(clus_params), filenames_in_cluster_test)
	#random_sample_of_cluster(filenames_in_cluster_train, 3)
	#random_sample_of_cluster(filenames_in_cluster_test, 3)
	if type_clus == "KMeans":
		return attempt.inertia_, score_train, score_test 
	if type_clus == "DBSCAN":
		return score_train, score_test 

def make_cluster(type_clus, size, variable_name, sd_x_train, sd_y_train, sd_names_train, sd_start_train, sd_window_train, sd_x_test, sd_y_test, sd_names_test, sd_start_test, sd_window_test):
	train_arr = []
	test_arr = []
	for index_val in range(len(sd_x_train)):
		train_arr.append([sd_x_train[index_val], sd_y_train[index_val]])
	for index_val in range(len(sd_x_test)):
		test_arr.append([sd_x_test[index_val], sd_y_test[index_val]])
 
	vals_clus = range(2, 15) 
	vals_nn = [int(len(train_arr) // val_clus) for val_clus in vals_clus] 
	vals_nn = [5 for val_clus in vals_clus] 
	vals_eps_range = np.arange(10 ** -3, 10 ** -2, 10 ** -3)
	index_clustering = 0

	if type_clus == "KMeans":

		inertia_list = []
		silhouette_list_train = []
		silhouette_list_test = []
		vals_clus_sil_train = []
		vals_clus_sil_test = [] 

		for val_clus in vals_clus:
			attempt = KMeans(n_clusters = val_clus, random_state = 42) 
			inertia_val, siltrain, siltest = one_cluster(size, type_clus, attempt, train_arr, test_arr, variable_name, "nclus " + str(val_clus), sd_names_train, sd_start_train, sd_window_train, sd_names_test, sd_start_test, sd_window_test)

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
			#new_eps = kneefind(val_nn, train_arr)
			#print(vals_clus[index_clustering], val_nn, new_eps)
			#new_eps_vals.append(new_eps)
			#new_eps_vals.sort()
			for val_eps in new_eps_vals: 
				attempt = DBSCAN(eps = val_eps, min_samples = val_nn) 
				siltrain, siltest = one_cluster(size, type_clus, attempt, train_arr, test_arr, variable_name, "nn " + str(val_nn) + " eps " + str(np.round(val_eps, 3)), sd_names_train, sd_start_train, sd_window_train, sd_names_test, sd_start_test, sd_window_test) 
				
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
 
def scatter_train_test(sd_x, sd_y, sd_common, sd_names, train_set, test_set):
	for size in sd_names:
		sd_x_train = dict()
		for variable_name in sd_x[size]: 
			sd_x_train[variable_name] = []
		sd_y_train = dict()
		for variable_name in sd_y[size]: 
			sd_y_train[variable_name] = []
		sd_names_train = []
		sd_start_train = []
		sd_window_train = []

		sd_x_test = dict()
		for variable_name in sd_x[size]: 
			sd_x_test[variable_name] = []
		sd_y_test= dict()
		for variable_name in sd_y[size]: 
			sd_y_test[variable_name] = []
		sd_names_test = []
		sd_start_test = []
		sd_window_test = []

		for index_val in range(len(sd_names[size])):
			if sd_names[size][index_val] in train_set:
				sd_names_train.append(sd_names[size][index_val])
				sd_start_train.append(sd_common[size]["start"][index_val])
				sd_window_train.append(sd_common[size]["window_size"][index_val])
				for variable_name in sd_y[size]: 
					sd_y_train[variable_name].append(sd_y[size][variable_name][index_val])
				for variable_name in sd_x[size]: 
					sd_x_train[variable_name].append(sd_x[size][variable_name][index_val])

			if sd_names[size][index_val] in test_set:
				sd_names_test.append(sd_names[size][index_val])
				sd_start_test.append(sd_common[size]["start"][index_val])
				sd_window_test.append(sd_common[size]["window_size"][index_val])
				for variable_name in sd_y[size]: 
					sd_y_test[variable_name].append(sd_y[size][variable_name][index_val])
				for variable_name in sd_x[size]: 
					sd_x_test[variable_name].append(sd_x[size][variable_name][index_val])

		for variable_name in sd_x[size]:  
			if variable_name != "offset":
				continue 
			print(len(sd_names_test), len(sd_names_test) / (len(sd_names_train) + len(sd_names_test)))
			print(len(sd_names_train), len(sd_names_train) / (len(sd_names_train) + len(sd_names_test)))
			'''
			plt.subplot(1, 2, 1)
			plt.title("size " + size + " train " + variable_name) 
			plt.scatter(sd_x_train[variable_name], sd_y_train[variable_name], color = 'b')
			plt.subplot(1, 2, 2)
			plt.title("size " + size + " test " + variable_name) 
			plt.scatter(sd_x_test[variable_name], sd_y_test[variable_name], color = 'r')
			plt.show()
			'''
			make_cluster("KMeans", size, variable_name, sd_x_train[variable_name], sd_y_train[variable_name], sd_names_train, sd_start_train, sd_window_train, sd_x_test[variable_name], sd_y_test[variable_name], sd_names_test, sd_start_test, sd_window_test)
			make_cluster("DBSCAN", size, variable_name, sd_x_train[variable_name], sd_y_train[variable_name], sd_names_train, sd_start_train, sd_window_train, sd_x_test[variable_name], sd_y_test[variable_name], sd_names_test, sd_start_test, sd_window_test)
 
#for size in os.listdir("rays"):
train_names = set()
test_names = set()

stuff_to_plot_all = dict()  
stuff_to_plot_x = dict() 
stuff_to_plot_y = dict() 
stuff_to_plot_common = dict() 
stuff_to_plot_names = dict() 

common_elements = ["window_size", "vehicle", "ride", "start"]

for size in ["8"]: 
#for size in ["4", "8", "12", "16", "20", "24", "28", "36"]:

	stuff_to_plot_all[size] = dict() 

	stuff_to_plot_x[size] = dict() 

	stuff_to_plot_y[size] = dict() 

	stuff_to_plot_common[size] = dict() 

	for colname in common_elements:
		stuff_to_plot_common[size][colname] = []

	stuff_to_plot_names[size] = [] 

	for vehicle in os.listdir("rays/" + size):
		if "Vehicle" not in vehicle:
			continue
		train_rides = set()
		if os.path.isfile(vehicle + "/train_rides"):
			train_rides = load_object(vehicle + "/train_rides")
		test_rides = set()
		if os.path.isfile(vehicle + "/test_rides"):
			test_rides = load_object(vehicle + "/test_rides")
		for some_file in os.listdir("rays/" + size + "/" + vehicle):
			some_file_events = vehicle + "/cleaned_csv/events_" + some_file + ".csv"

			if "events_" + some_file + ".csv" in train_rides:
				train_names.add(some_file_events)

			if "events_" + some_file + ".csv" in test_rides:
				test_names.add(some_file_events) 

			some_file_csv = pd.read_csv("rays/" + size + "/" + vehicle + "/" + some_file + "/all_distances_scaled_to_max_trajs.csv", index_col = False)
			 
			for colname in common_elements:
				for value_of_col in some_file_csv[colname]:
					stuff_to_plot_common[size][colname].append(value_of_col) 
					if colname == "start":
						stuff_to_plot_names[size].append(some_file_events) 
						 
			for colname in some_file_csv.head():
				if colname in common_elements:
					continue
				if not " x" in colname and not " y" in colname:  
					if colname not in stuff_to_plot_all[size]:
						stuff_to_plot_all[size][colname] = []
					for value_of_col in some_file_csv[colname]:
						stuff_to_plot_all[size][colname].append(value_of_col)
				if " x" in colname: 
					colname_short = colname.replace(" x", "")
					if colname_short not in stuff_to_plot_x[size]:
						stuff_to_plot_x[size][colname_short] = []
					for value_of_col in some_file_csv[colname]:
						stuff_to_plot_x[size][colname_short].append(value_of_col)
				if " y" in colname: 
					colname_short = colname.replace(" y", "")
					if colname_short not in stuff_to_plot_y[size]:
						stuff_to_plot_y[size][colname_short] = []
					for value_of_col in some_file_csv[colname]:
						stuff_to_plot_y[size][colname_short].append(value_of_col)
				 
			'''
			matrices_all = load_object("rays/" + size + "/" + vehicle + "/" + some_file + "/all_distances_scaled_to_max_trajs_other")
			matrices_all_x = matrices_all[0] 
			print(matrices_all_x.keys())
			for val in matrices_all_x.keys():
				print(val in some_file_csv.head())
			for x in matrices_all:
				distances_matrix = dict()
				for type_matrix in matrices_all[x]:
					matrices_all_x = matrices_all[x][type_matrix] 
					matrices_dist = matrices_all_x[1]  
					
					distances_matrix[type_matrix] = dict()
					for point_num in range(1, len(matrices_dist[0][0])):
						distances_matrix[type_matrix][point_num] = []
						for x1 in range(len(matrices_dist)):
							distances_matrix[type_matrix][point_num].append([])
							for x2 in range(len(matrices_dist[x1])): 
								distances_matrix[type_matrix][point_num][-1].append(matrices_dist[x1][x2][point_num]) 
						
				for point_num in [12]:#range(1, len(matrices_all[x]["scale"][0][0])):
					for type_matrix in matrices_all[x]:	
						distances_matrix[type_matrix][point_num] = Matrix(distances_matrix[type_matrix][point_num]) 
						#print(distances_matrix[type_matrix][point_num])
						distances_matrix_p, distances_matrix_j = distances_matrix[type_matrix][point_num].jordan_form()
						#print(distances_matrix_j)  
			'''
#scatter_me(stuff_to_plot_x, stuff_to_plot_y)
#scatter_train_test(stuff_to_plot_x, stuff_to_plot_y, stuff_to_plot_common, stuff_to_plot_names, train_names, test_names)

for size in ["8"]: 
#for size in ["4", "8", "12", "16", "20", "24", "28", "36"]:
	for filename_clus in os.listdir("rays/" + size + "/clustering"):
		if "DBSCAN" in filename_clus:
			object_clus = load_object("rays/" + size + "/clustering/" + filename_clus)
			print(filename_clus, len(object_clus))
			#random_sample_of_cluster(oobject_clus, 1)