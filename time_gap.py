from utilities import *

all_subdirs = os.listdir() 
 
for subdir_name in all_subdirs: 
    if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
        continue 
    
    all_rides_cleaned = os.listdir(subdir_name + "/cleaned_csv/")
    
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
    
        file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
        
        times = list(file_with_ride["time"])
        times_processed = [process_time(time_new) for time_new in times] 
        times_delays = [times_processed[time_index + 1] - times_processed[time_index] for time_index in range(len(times_processed) - 1)] 
        for time_index in range(len(times_delays)):
            if times_delays[time_index] == 0:  
                gap_rides_filenames.add(subdir_name + "/cleaned_csv/" + some_file)
                break

    save_object(subdir_name + "/gap_rides_filenames", gap_rides_filenames)
    print(subdir_name, len(gap_rides_filenames))