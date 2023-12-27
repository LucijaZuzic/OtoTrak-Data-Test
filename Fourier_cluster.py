from utilities import *
from sklearn.manifold import TSNE
from knees import kneefind
all_feats_fourier_scaled_to_max = pd.read_csv("all_feats_fourier/all_feats_fourier_scaled_to_max.csv")
header_of_file = ["window_size", "vehicle", "ride", "start"]
longitude_train_complex = []
latitude_train_complex = []
times_train_complex = []
wtrain = []
vtrain = []
rtrain = []
strain = []

longitude_test_complex = []
latitude_test_complex = []
times_test_complex = []
wtest = []
vtest = []
rtest = []
stest = []

for index in range(len(all_feats_fourier_scaled_to_max["window_size"])):
    subdir_name = all_feats_fourier_scaled_to_max["vehicle"][index]
    filename = "events_" + str(all_feats_fourier_scaled_to_max["ride"][index]) + ".csv" 
    x = all_feats_fourier_scaled_to_max["start"][index]
    ws = all_feats_fourier_scaled_to_max["window_size"][index]
    file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + filename)
    times = list(file_with_ride["time"])  
    times_tmp = times[x:x + ws]  
      
    train_rides = set()
    if os.path.isfile(subdir_name + "/train_rides"):
        train_rides = load_object(subdir_name + "/train_rides") 
        
    test_rides = set()
    if os.path.isfile(subdir_name + "/test_rides"):
        test_rides = load_object(subdir_name + "/test_rides")

    if filename in train_rides:
        times_train_complex.append(times_tmp)
        wtrain.append(ws)
        vtrain.append(subdir_name)
        rtrain.append(filename)
        strain.append(x)
        longitude_train_complex.append([])
        latitude_train_complex.append([])
        
    if filename in test_rides:
        times_test_complex.append(times_tmp)
        wtest.append(ws)
        vtest.append(subdir_name)
        rtest.append(filename)
        stest.append(x)
        longitude_test_complex.append([])
        latitude_test_complex.append([])

    for feat in all_feats_fourier_scaled_to_max.head():
        if feat in header_of_file:
            continue
        complex_number = complex(all_feats_fourier_scaled_to_max[feat][index])

        if filename in train_rides:
            if "long" in feat:
                longitude_train_complex[-1].append(complex_number)
            if "lat" in feat:
                latitude_train_complex[-1].append(complex_number)

        if filename in test_rides:
            if "long" in feat:
                longitude_test_complex[-1].append(complex_number)
            if "lat" in feat:
                latitude_test_complex[-1].append(complex_number)
         
signal_test_x = range(20)
signal_test_y = np.arange(0, 0.005, 0.005 / len(signal_test_x))
fft_sig = np.fft.fft(signal_test_y)
fft_sig_real = [fft_val.real for fft_val in fft_sig]
fft_sig_imag = [fft_val.imag for fft_val in fft_sig]

results_x_test = []
results_y_test = []  
results_xy_test = []  
for i, xfft in enumerate(longitude_test_complex):
    yfft = latitude_test_complex[i]
    rx = sum([abs(xfft[i] * fft_sig[i]) for i in range(len(xfft))])
    ry = sum([abs(yfft[i] * fft_sig[i]) for i in range(len(yfft))])
    results_x_test.append(rx)
    results_y_test.append(ry) 
    results_xy_test.append([rx, ry]) 

results_x_train = []
results_y_train = []  
results_xy_train = []  
for i, xfft in enumerate(longitude_train_complex):
    yfft = latitude_train_complex[i]
    rx = sum([abs(xfft[i] * fft_sig[i]) for i in range(len(xfft))])
    ry = sum([abs(yfft[i] * fft_sig[i]) for i in range(len(yfft))])
    results_x_train.append(rx)
    results_y_train.append(ry) 
    results_xy_train.append([rx, ry]) 

def one_fourier_clus(type_clus, attempt, train_arr, test_arr, clus_params, sd_subdir_train, sd_ride_train, sd_start_train, sd_window_train, sd_subdir_test, sd_ride_test, sd_start_test, sd_window_test):
    clus_train = attempt.fit(train_arr)
    train_labels = clus_train.labels_ 
 
    if not os.path.isdir("all_fourier_clus/clus_train"):
        os.makedirs("all_fourier_clus/clus_train")
	
    save_object("all_fourier_clus/clus_train/clus_train_" + type_clus + " train " + str(clus_params), clus_train) 
       
    train_embedded = train_arr
    test_embedded = test_arr

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
 
    if not os.path.isdir("all_fourier_clus/clus_test"):
        os.makedirs("all_fourier_clus/clus_test")
	
    save_object("all_fourier_clus/clus_test/clus_test_" + type_clus + " test " + str(clus_params), clus_test) 

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
    if not os.path.isdir("all_fourier_clus/plots"):
        os.makedirs("all_fourier_clus/plots")
    plt.savefig("all_fourier_clus/plots/" + type_clus + " test " + str(clus_params) + ".png") 
    plt.close()

    score_train = "undefined"
    if len(dict_train_by_label) > 1:
        score_train = silhouette_score(train_arr, train_labels)
		
    score_test = "undefined"
    if len(dict_test_by_label) > 1:
        score_test = silhouette_score(test_arr, test_labels) 
  
    if not os.path.isdir("all_fourier_clus/filenames/"):
        os.makedirs("all_fourier_clus/filenames/")

    save_object("all_fourier_clus/filenames/filenames_in_cluster_train " + type_clus + " test " + str(clus_params), filenames_in_cluster_train)
    save_object("all_fourier_clus/filenames/filenames_in_cluster_test " + type_clus + " test " + str(clus_params), filenames_in_cluster_test) 
    
    if type_clus == "KMeans":
        return attempt.inertia_, score_train, score_test 
    if type_clus == "DBSCAN":
        return score_train, score_test 

def make_fourier_clus(type_clus, sd_window_train, sd_subdir_train, sd_ride_train, sd_start_train, sd_x_train, sd_window_test, sd_subdir_test, sd_ride_test, sd_start_test, sd_x_test):
	 
    vals_clus = range(2, 11)   
    
    inertia_list = []
    silhouette_list_train = []
    silhouette_list_test = []
    vals_clus_sil_train = []
    vals_clus_sil_test = [] 

    for val_clus in vals_clus:
        if type_clus == "KMeans":
            attempt = KMeans(n_clusters = val_clus, random_state = 42) 
            inertia_val, siltrain, siltest = one_fourier_clus(type_clus, attempt, sd_x_train, sd_x_test, "nclus " + str(val_clus), sd_subdir_train, sd_ride_train, sd_start_train, sd_window_train, sd_subdir_test, sd_ride_test, sd_start_test, sd_window_test)
            inertia_list.append(inertia_val)

        if type_clus == "DBSCAN": 
            new_eps = kneefind(int(len(sd_x_train) // val_clus), sd_x_train)
            attempt = DBSCAN(min_samples = int(len(sd_x_train) // val_clus), eps = new_eps) 
            siltrain, siltest = one_fourier_clus(type_clus, attempt, sd_x_train, sd_x_test, "nclus " + str(val_clus), sd_subdir_train, sd_ride_train, sd_start_train, sd_window_train, sd_subdir_test, sd_ride_test, sd_start_test, sd_window_test)
  
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
      
make_fourier_clus("DBSCAN", wtrain, vtrain, rtrain, strain, results_xy_train, wtest, vtest, rtest, stest, results_xy_test)
make_fourier_clus("KMeans", wtrain, vtrain, rtrain, strain, results_xy_train, wtest, vtest, rtest, stest, results_xy_test)