from utilities import * 
from sklearn.manifold import TSNE
from knees import kneefind

window_size = 20
deg = 5
maxoffset = 0.005
step_size = window_size
#step_size = 1 
 
all_subdirs = os.listdir() 

def one_clusters(type_clus, attempt, train_arr, test_arr, clus_params, sd_subdir_train, sd_ride_train, sd_start_train, sd_window_train, sd_subdir_test, sd_ride_test, sd_start_test, sd_window_test):
    clus_train = attempt.fit(train_arr)
    train_labels = clus_train.labels_ 
 
    if not os.path.isdir("all_clus/" + subdirname + "/clus_train/"):
        os.makedirs("all_clus/" + subdirname + "/clus_train/")
	
    save_object("all_clus/" + subdirname + "/clus_train/clus_train_" + type_clus + " train " + str(clus_params), clus_train) 
       
    train_embedded = TSNE(n_components=2).fit_transform(train_arr)
    test_embedded = TSNE(n_components=2).fit_transform(test_arr)
 
    if not os.path.isdir("all_clus/" + subdirname + "/TSNE/"):
        os.makedirs("all_clus/" + subdirname + "/TSNE/")
	
    save_object("all_clus/" + subdirname + "/TSNE/TSNE_" + type_clus + " train " + str(clus_params), train_embedded)
    save_object("all_clus/" + subdirname + "/TSNE/TSNE_" + type_clus + " test " + str(clus_params), test_embedded) 

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

    if not os.path.isdir("all_clus/" + subdirname + "/clus_test/"):
        os.makedirs("all_clus/" + subdirname + "/clus_test/")
	
    save_object("all_clus/" + subdirname + "/clus_test/clus_test_" + type_clus + " test " + str(clus_params), clus_test) 

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
	
    save_object("all_clus/" + subdirname + "/filenames/filenames_in_cluster_train " + type_clus + " test " + str(clus_params), filenames_in_cluster_train)
    save_object("all_clus/" + subdirname + "/filenames/filenames_in_cluster_test " + type_clus + " test " + str(clus_params), filenames_in_cluster_test)
    
    if type_clus == "KMeans":
        return attempt.inertia_, score_train, score_test 
    if type_clus == "DBSCAN":
        return score_train, score_test 

def make_clusters(type_clus, sd_window_train, sd_subdir_train, sd_ride_train, sd_start_train, sd_x_train, sd_window_test, sd_subdir_test, sd_ride_test, sd_start_test, sd_x_test):
	 
    vals_clus = range(2, 11)   
    
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
  
def make_clusters_multi_feats(subdirname):
    dict_for_clustering= dict()
    dict_for_clustering[window_size] = dict() 

    dict_for_clustering = load_object("dict_for_clustering")
    train_names = load_object("train_names")
    test_names = load_object("test_names")

    sd_window_train = load_object("sd_window_train")
    sd_subdir_train = load_object("sd_subdir_train")
    sd_ride_train = load_object("sd_ride_train") 
    sd_start_train = load_object("sd_start_train") 
    sd_ride_test = load_object("sd_ride_test") 
    sd_x_train = load_object("sd_x_train") 

    sd_window_test = load_object("sd_window_test")
    sd_subdir_test = load_object("sd_subdir_test")
    sd_ride_test = load_object("sd_ride_test") 
    sd_start_test = load_object("sd_start_test") 
    sd_ride_test = load_object("sd_ride_test") 
    sd_x_test = load_object("sd_x_test") 

    sd_window_train, sd_subdir_train, sd_ride_train, sd_start_train, sd_x_train, sd_window_test, sd_subdir_test, sd_ride_test, sd_start_test, sd_x_test  = divide_train_test(dict_for_clustering, train_names, test_names, subdirname)

    print(len(sd_x_train), len(sd_x_train[0]), sd_x_train[0][:10])
    print(len(sd_x_test))
    make_clusters("KMeans", sd_window_train, sd_subdir_train, sd_ride_train, sd_start_train, sd_x_train, sd_window_test, sd_subdir_test, sd_ride_test, sd_start_test, sd_x_test)
    #make_clusters("DBSCAN", sd_window_train, sd_subdir_train, sd_ride_train, sd_start_train, sd_x_train, sd_window_test, sd_subdir_test, sd_ride_test, sd_start_test, sd_x_test)

for subdirname_p1 in ["all", "no_rays"]:
    for subdirname_p2 in ["", "_poly", "_flags", "_poly_flags"]:
        for subdirname_p3 in ["", "_no_same", "_no_xy", "_no_same_no_xy"]:
            for subdirname_p4 in ["", "_acceler", "_heading", "_acceler_heading"]:
                subdirname = subdirname_p1 + subdirname_p2 + subdirname_p3 + subdirname_p4
                if os.path.isdir("all_clus/" + subdirname):
                    continue
                print(subdirname)
                make_clusters_multi_feats(subdirname)
                #read_clusters(subdirname) 
'''            
part2 = []
for size in os.listdir("rays"):
    part2.append("_size_" + str(size) + "_")  
for subdirname_p1 in ["", "_acceler", "_heading", "_acceler_heading"]:
    for subdirname_p2 in part2:    
        subdirname = "only_rays" + subdirname_p1 + subdirname_p2
        if os.path.isdir("all_clus/" + subdirname):
            continue
        print(subdirname)
        make_clusters_multi_feats(subdirname)
        #read_clusters(subdirname)
'''