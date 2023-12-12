from utilities import *
all_subdirs = os.listdir()
MIN_VAL = -1
MAX_VAL = 360 
labels_by_hand = dict()
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
        angles = return_angle_diffs(headings)    