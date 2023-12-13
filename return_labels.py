from utilities import *
all_subdirs = os.listdir()

def return_labels(nclus):
    filname_test = "all_location_clus/hand_made_labels/all_labels_filenames_in_cluster_test KMeans test nclus " + str(nclus)
    filname_train = "all_location_clus/hand_made_labels/all_labels_filenames_in_cluster_train KMeans test nclus " + str(nclus)
    all_labels_test = load_object(filname_test)
    all_labels_train = load_object(filname_train) 
    labels_to_cluster_train = [] 
    labels_to_cluster_test = []
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
            times = list(file_with_ride["time"])  
            times_tmp_transform = transform_time(times)
            speeds_tmp = list(file_with_ride["fields_speed"])  
            headings = list(file_with_ride["fields_direction"])   
            longitudes = list(file_with_ride["fields_longitude"])
            latitudes = list(file_with_ride["fields_latitude"])  
            times = list(file_with_ride["time"])  
            times_tmp_transform = transform_time(times) 
            xsteps, ysteps, absxsteps, absysteps = return_steps_by_axis(longitudes, latitudes, times) 
            accelers_ototrak_trajs = return_acceler_speeds(speeds_tmp, times_tmp_transform)
            angles = return_angle_diffs(headings)    

            if some_file in train_rides: 
                for i in range(len(accelers_ototrak_trajs)):    
                    labels_to_cluster_train.append(all_labels_train[subdir_name][some_file][i])
            if some_file in test_rides: 
                for i in range(len(accelers_ototrak_trajs)):   
                    labels_to_cluster_test.append(all_labels_test[subdir_name][some_file][i])  
    labels_to_cluster_train = np.array(labels_to_cluster_train)  
    labels_to_cluster_test = np.array(labels_to_cluster_test) 
    return labels_to_cluster_train, labels_to_cluster_test
 
for nclus in range(2, 16):
    return_labels(nclus)