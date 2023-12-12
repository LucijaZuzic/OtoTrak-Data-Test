from utilities import * 
dict_for_clustering = dict()
window_size = 20
all_subdirs = os.listdir()
train_names = set()
test_names = set()   
dict_for_clustering[window_size] = dict()
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
        
        if some_file in train_names:
            print("ERROR", some_file)
        if some_file in test_names:
            print("ERROR", some_file)
        if some_file in train_rides:
            train_names.add(some_file)

        if some_file in test_rides:
            test_names.add(some_file) 
print(len(train_names), len(test_names))