from utilities import *

all_subdirs = os.listdir() 

if not os.path.isdir("num_occurences"):
    os.makedirs("num_occurences")
if not os.path.isdir("probability"):
    os.makedirs("probability")
if not os.path.isdir("predicted"):
    os.makedirs("predicted")

if not os.path.isfile("num_occurences/num_occurences_of_y_speed_alternative"):
    num_occurences_of_y_speed_alternative = dict()
    num_occurences_of_y_speed_alternative_in_next_step = dict()
    num_occurences_of_y_speed_alternative_in_next_next_step = dict()

    for subdir_name in all_subdirs: 
        if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
            continue 
        
        all_rides_cleaned = os.listdir(subdir_name + "/cleaned_csv/")
        
        all_files = os.listdir(subdir_name + "/cleaned_csv/") 
        bad_rides_filenames = set()
        if os.path.isfile(subdir_name + "/bad_rides_filenames"):
            bad_rides_filenames = load_object(subdir_name + "/bad_rides_filenames")
        test_rides = set()
        if os.path.isfile(subdir_name + "/test_rides"):
            test_rides = load_object(subdir_name + "/test_rides")
            
        for some_file in all_files:  
            if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or some_file in test_rides: 
                continue 
        
            file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
            longitudes = list(file_with_ride["fields_longitude"]) 
            latitudes = list(file_with_ride["fields_latitude"]) 
            longitudes, latitudes = preprocess_long_lat(longitudes, latitudes)
            longitudes, latitudes = scale_long_lat(longitudes, latitudes, 0.1, 0.1, True)  
            times = list(file_with_ride["time"])
            times_processed = [process_time(time_new) for time_new in times] 
            times_delays = [times_processed[time_index + 1] - times_processed[time_index] for time_index in range(len(times_processed) - 1)] 
            for time_index in range(len(times_delays)):
                if times_delays[time_index] == 0:
                    times_delays[time_index] = 10 ** -4
                    print(subdir_name, some_file, time_index, times_processed[time_index - 1], times_processed[time_index], times_processed[time_index + 1])
                    print(longitudes[time_index - 1], longitudes[time_index], longitudes[time_index + 1])
                    print(latitudes[time_index - 1], latitudes[time_index], latitudes[time_index + 1])

            distance_int = [abs(latitudes[distance_index + 1] - latitudes[distance_index]) for distance_index in range(len(latitudes) - 1)]
            y_speed_alternative_int = [np.round(distance_int[y_speed_alternative_index] / times_delays[y_speed_alternative_index], 10) for y_speed_alternative_index in range(len(times_delays))]
 