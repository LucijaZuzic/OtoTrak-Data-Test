from utilities import *
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

print(len(test_data))
print(len(train_data))
print(len(test_data[0]))
print(len(train_data[0]))

vals_clus = range(2, 3)   

for val_clus in vals_clus:
    attemptK = KMeans(n_clusters = val_clus, random_state = 42)  
    #new_eps = kneefind(int(len(train_data) // val_clus), train_data)
    #attemptD = DBSCAN(min_samples = int(len(train_data) // val_clus), eps = new_eps)  

    clus_train = attemptK.fit(train_data)
    train_labels = clus_train.labels_ 
         
