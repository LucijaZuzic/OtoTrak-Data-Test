from utilities import *
from sklearn.manifold import TSNE
all_feats_fourier_scaled_to_max = pd.read_csv("all_feats_fourier/all_feats_fourier_scaled_to_max.csv")
header_of_file = ["window_size", "vehicle", "ride", "start"]
train_data = []
test_data = []

for index in range(len(all_feats_fourier_scaled_to_max["window_size"])):
    subdir_name = all_feats_fourier_scaled_to_max["vehicle"][index]
    filename = "events_" + str(all_feats_fourier_scaled_to_max["ride"][index]) + ".csv" 

    train_rides = set()
    if os.path.isfile(subdir_name + "/train_rides"):
        train_rides = load_object(subdir_name + "/train_rides") 
        
    test_rides = set()
    if os.path.isfile(subdir_name + "/test_rides"):
        test_rides = load_object(subdir_name + "/test_rides")

    if filename in train_rides:
        train_data.append([])

    if filename in test_rides:
        test_data.append([])

    for feat in all_feats_fourier_scaled_to_max.head():
        if feat in header_of_file:
            continue
        complex_number = complex(all_feats_fourier_scaled_to_max[feat][index])
        if filename in train_rides:
            train_data[-1].append(complex_number.real)
            train_data[-1].append(complex_number.imag)
        if filename in test_rides:
            test_data[-1].append(complex_number.real)
            test_data[-1].append(complex_number.imag)
train_data = np.array(train_data)
test_data = np.array(test_data)
print(len(test_data))
print(len(train_data))
print(len(test_data[0]))
print(len(train_data[0]))

vals_clus = range(2, 3)   

for val_clus in vals_clus:
    attemptK = KMeans(n_clusters = val_clus, random_state = 42)  
    new_eps = kneefind(int(len(train_data) // val_clus), train_data)
    attemptD = DBSCAN(min_samples = int(len(train_data) // val_clus), eps = new_eps)  

    clus_train = attemptK.fit(train_data)
    train_labels = clus_train.labels_ 

    train_embedded = TSNE(n_components=2).fit_transform(train_data) 

    dict_train_by_label = dict()
    for label in train_labels:
        dict_train_by_label[label] = {"x": [], "y": []}
	 
    for label_index in range(len(train_labels)):
        label = train_labels[label_index]
        dict_train_by_label[label]["x"].append(float(train_embedded[label_index][0]))
        dict_train_by_label[label]["y"].append(float(train_embedded[label_index][1]))
       
    random_colors_set = random_colors(len(set(dict_train_by_label.keys())))
    random_colors_dict = dict()
    index_num = 0
    for label in set(dict_train_by_label.keys()):
        random_colors_dict[label] = random_colors_set[index_num]
        index_num += 1

    label_index = 0 
    for label in dict_train_by_label:   
        plt.scatter(dict_train_by_label[label]["x"], dict_train_by_label[label]["y"], color = random_colors_dict[label], label = str(label) + " train")   
        label_index += 1 
    plt.legend()
    plt.show()

signal = [i for i in np.arange(0, 0.005, 0.0001)]
fft_sig = np.fft.fft(signal)
plt.plot(np.arange(0, 0.005, 0.0001), fft_sig)
plt.show()