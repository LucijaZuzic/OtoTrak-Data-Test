from utilities import *

def is_anomaly_once(probab_array, limit = 10 ** -20):
    return [val <= limit for val in probab_array] 

def is_anomaly(probab_arrays, limit = 10 ** -20):
    return {probab_array: is_anomaly_once(probab_arrays[probab_array], limit) for probab_array in probab_arrays}

def is_anomaly_which(probab_arrays, limit = 10 ** -20, key_set = 0):
    if key_set == 0:
        key_set = list(probab_arrays.keys())
    maxlens = [len(probab_arrays[probab_array]) for probab_array in key_set]
    which = []
    any = []
    all = []
    for index in range(max(maxlens)):
        detected = []
        for probab_array in key_set:
            if index < len(probab_arrays[probab_array]) and probab_arrays[probab_array][index] <= limit:
                detected.append(probab_array)
        which.append(detected)
        any.append(len(detected) > 0)
        all.append(len(detected) == len(key_set))
    return which, any, all
  
def plot_anomaly(long, lat, arr, val_arr, probs, title):
    plt.title(title)
    plt.plot(long, lat, color = "blue")
    long_anomaly = []
    lat_anomaly = []
    for inde in range(len(arr)):
        if inde < len(long) and inde < len(lat) and arr[inde]:
            long_anomaly.append(long[inde])
            lat_anomaly.append(lat[inde])
    plt.scatter(long_anomaly, lat_anomaly, color = "red")
    #plt.show() 
    #'''
    for inde in range(len(arr)):
        if inde < len(long) and inde < len(lat) and arr[inde]: 
            min_new = max(0, inde - 2)
            max_new = min(len(long), inde + 1) 
            new_title = title + "=" 
            if inde > 1:
                new_title += str(val_arr[inde - 2]) + ","
            if inde > 0:
                new_title += str(val_arr[inde - 1]) + ","
            #plt.title(new_title + str(val_arr[inde]) + "\n" + str(probs[inde] * 100) + "%")
            plt.plot(long[min_new:max_new], lat[min_new:max_new], color = "red")
            #plt.scatter(long[inde], lat[inde], color = "red")
            #plt.show()
    #'''
    plt.show() 

all_entries_max = dict()
all_entries_zero = dict()
positive_entries_max = dict()
positive_entries_zero = dict()

all_entries_sum_zero = 0
positive_entries_sum_zero = 0

all_entries_mul_zero = 0
positive_entries_mul_zero = 0

all_entries_sum_max = 0
positive_entries_sum_max = 0

all_entries_mul_max = 0
positive_entries_mul_max = 0

all_labels_sum_zero = 0
positive_labels_sum_zero = 0
  
all_labels_sum_max = 0
positive_labels_sum_max = 0
  
window_sizes = [3, 20]

labels_window_size_zero = dict()
labels_window_size_max = dict()
percents_window_size_zero = dict()
percents_window_size_max = dict()

for ws in window_sizes:
    labels_window_size_zero[ws] = dict()
    labels_window_size_max[ws] = dict()
    percents_window_size_zero[ws] = dict()
    percents_window_size_max[ws] = dict()

labels_window_size_zero_dict = dict()
labels_window_size_max_dict = dict()
percents_window_size_zero_dict = dict()
percents_window_size_max_dict = dict()

for ws in window_sizes:
    labels_window_size_zero_dict[ws] = dict()
    labels_window_size_max_dict[ws] = dict()
    percents_window_size_zero_dict[ws] = dict()
    percents_window_size_max_dict[ws] = dict()
 
total_probs_zero_sum_dict = dict()
total_probs_zero_mul_dict = dict()
total_probs_max_sum_dict = dict()
total_probs_max_mul_dict = dict()

for ws in window_sizes:
    total_probs_zero_sum_dict[ws] = dict()
    total_probs_zero_mul_dict[ws] = dict()
    total_probs_max_sum_dict[ws] = dict()
    total_probs_max_mul_dict[ws] = dict()

total_labels_zero_sum_dict = dict() 
total_labels_max_sum_dict = dict() 

for ws in window_sizes:
    total_labels_zero_sum_dict[ws] = dict() 
    total_labels_max_sum_dict[ws] = dict() 

all_subdirs = os.listdir() 
for subdir_name in all_subdirs: 
    for ws in window_sizes:
        labels_window_size_zero_dict[ws][subdir_name] = dict()
        labels_window_size_max_dict[ws][subdir_name] = dict()
        percents_window_size_zero_dict[ws][subdir_name] = dict()
        percents_window_size_max_dict[ws][subdir_name] = dict()

        total_probs_zero_sum_dict[ws][subdir_name] = dict()
        total_probs_zero_mul_dict[ws][subdir_name] = dict()
        total_probs_max_sum_dict[ws][subdir_name] = dict()
        total_probs_max_mul_dict[ws][subdir_name] = dict()

        total_labels_zero_sum_dict[ws][subdir_name] = dict() 
        total_labels_max_sum_dict[ws][subdir_name] = dict() 

    if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
        continue
      
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
        
    for some_file in all_files:  
        if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames or some_file in train_rides: 
            continue 
        for ws in window_sizes:
            labels_window_size_zero_dict[ws][subdir_name][some_file] = dict()
            labels_window_size_max_dict[ws][subdir_name][some_file] = dict()
            percents_window_size_zero_dict[ws][subdir_name][some_file] = dict()
            percents_window_size_max_dict[ws][subdir_name][some_file] = dict()

            total_probs_zero_sum_dict[ws][subdir_name][some_file] = dict()
            total_probs_zero_mul_dict[ws][subdir_name][some_file] = dict()
            total_probs_max_sum_dict[ws][subdir_name][some_file] = dict()
            total_probs_max_mul_dict[ws][subdir_name][some_file] = dict()

            total_labels_zero_sum_dict[ws][subdir_name][some_file] = dict() 
            total_labels_max_sum_dict[ws][subdir_name][some_file] = dict() 

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
                    times_delays[time_index] = 10 ** -20 

        speeds = list(file_with_ride["fields_speed"]) 
        speed_int = [np.round(speed, 0) for speed in speeds]
        
        directions = list(file_with_ride["fields_direction"]) 
        direction_int = [np.round(direction, 0) for direction in directions]
       
        longitude_abs_int = [np.round(abs(longitudes[longitude_index + 1] - longitudes[longitude_index]), 10) for longitude_index in range(len(longitudes) - 1)]
        longitude_int = [np.round(longitudes[longitude_index + 1] - longitudes[longitude_index], 10) for longitude_index in range(len(longitudes) - 1)]
        longitude_dir_int = [longitudes[longitude_index + 1] > longitudes[longitude_index] for longitude_index in range(len(longitudes) - 1)] 
        latitude_abs_int = [np.round(abs(latitudes[latitude_index + 1] - latitudes[latitude_index]), 10) for latitude_index in range(len(latitudes) - 1)]
        latitude_int = [np.round(latitudes[latitude_index + 1] - latitudes[latitude_index], 10) for latitude_index in range(len(latitudes) - 1)]
        latitude_dir_int = [latitudes[latitude_index + 1] > latitudes[latitude_index] for latitude_index in range(len(latitudes) - 1)]
         
        distance_int = [np.round(np.sqrt((longitudes[distance_index + 1] - longitudes[distance_index]) ** 2 + (latitudes[distance_index + 1] - latitudes[distance_index]) ** 2), 5) for distance_index in range(len(longitudes) - 1)]
         
        distance_euclid_int = [np.sqrt((longitudes[distance_index + 1] - longitudes[distance_index]) ** 2 + (latitudes[distance_index + 1] - latitudes[distance_index]) ** 2) for distance_index in range(len(longitudes) - 1)]
        speed_alternative_int = [np.round(distance_euclid_int[speed_alternative_index] / times_delays[speed_alternative_index], 5) for speed_alternative_index in range(len(times_delays))]
       
        distance_x_int = [longitudes[distance_index + 1] - longitudes[distance_index] for distance_index in range(len(longitudes) - 1)]
        distance_x_abs_int = [abs(longitudes[distance_index + 1] - longitudes[distance_index]) for distance_index in range(len(longitudes) - 1)]
        x_speed_alternative_int = [np.round(distance_x_abs_int[x_speed_alternative_index] / times_delays[x_speed_alternative_index], 5) for x_speed_alternative_index in range(len(times_delays))]
        x_speed_no_abs_alternative_int = [np.round(distance_int[x_speed_no_abs_alternative_index] / times_delays[x_speed_no_abs_alternative_index], 5) for x_speed_no_abs_alternative_index in range(len(times_delays))]
       
        distance_y_int = [latitudes[distance_index + 1] - latitudes[distance_index] for distance_index in range(len(latitudes) - 1)]
        distance_y_abs_int = [abs(latitudes[distance_index + 1] - latitudes[distance_index]) for distance_index in range(len(latitudes) - 1)]
        y_speed_alternative_int = [np.round(distance_y_abs_int[y_speed_alternative_index] / times_delays[y_speed_alternative_index], 5) for y_speed_alternative_index in range(len(times_delays))]
        y_speed_no_abs_alternative_int = [np.round(distance_int[y_speed_no_abs_alternative_index] / times_delays[y_speed_no_abs_alternative_index], 5) for y_speed_no_abs_alternative_index in range(len(times_delays))]
     
        direction_alternative_int = []
        for heading_alternative_index in range(len(longitudes) - 1): 
            direction_alternative_int.append((360 + np.round(np.arctan2(distance_y_int[heading_alternative_index], distance_x_int[heading_alternative_index]) / np.pi * 180, 0)) % 360)
             
        direction_abs_alternative_int = []
        for heading_abs_alternative_index in range(len(longitudes) - 1): 
            direction_abs_alternative_int.append((360 + np.round(np.arctan2(distance_y_abs_int[heading_abs_alternative_index], distance_x_abs_int[heading_abs_alternative_index]) / np.pi * 180, 0)) % 360)
             
        short_file = some_file.replace("events_", "").replace(".csv", "")
 
        all_probs_zero_max = pd.read_csv("all_probs_zero_max/" + str(subdir_name) + "/" + str(short_file) + "/all_probs_zero_max_" + str(subdir_name) + "_" + str(short_file) + ".csv", index_col=False)
        all_probs_zero = pd.read_csv("all_probs_zero/" + str(subdir_name) + "/" + str(short_file) + "/all_probs_zero_" + str(subdir_name) + "_" + str(short_file) + ".csv", index_col=False)
        all_probs_max = pd.read_csv("all_probs_max/" + str(subdir_name) + "/" + str(short_file) + "/all_probs_max_" + str(subdir_name) + "_" + str(short_file) + ".csv", index_col=False)
        
        all_thr_zero_max = pd.read_csv("all_thr_zero_max/" + str(subdir_name) + "/" + str(short_file) + "/all_thr_zero_max_" + str(subdir_name) + "_" + str(short_file) + ".csv", index_col=False)
        all_thr_zero = pd.read_csv("all_thr_zero/" + str(subdir_name) + "/" + str(short_file) + "/all_thr_zero_" + str(subdir_name) + "_" + str(short_file) + ".csv", index_col=False)
        all_thr_max = pd.read_csv("all_thr_max/" + str(subdir_name) + "/" + str(short_file) + "/all_thr_max_" + str(subdir_name) + "_" + str(short_file) + ".csv", index_col=False)
        
        all_labels_zero_max = pd.read_csv("all_labels_zero_max/" + str(subdir_name) + "/" + str(short_file) + "/all_labels_zero_max_" + str(subdir_name) + "_" + str(short_file) + ".csv", index_col=False)
        all_labels_zero = pd.read_csv("all_labels_zero/" + str(subdir_name) + "/" + str(short_file) + "/all_labels_zero_" + str(subdir_name) + "_" + str(short_file) + ".csv", index_col=False)
        all_labels_max = pd.read_csv("all_labels_max/" + str(subdir_name) + "/" + str(short_file) + "/all_labels_max_" + str(subdir_name) + "_" + str(short_file) + ".csv", index_col=False)
        
        total_probs_zero_sum = [0 for ix in range(len(all_probs_zero["distance_probs_zero"]))]
        total_probs_zero_mul = [1 for ix in range(len(all_probs_zero["distance_probs_zero"]))]
        all_probs_zero_dict = dict()
        for col in all_probs_zero:
            if "zero" not in col:
                continue
            all_probs_zero_dict[col] = list(all_probs_zero[col])
            for ix in range(len(all_probs_zero_dict[col])):
                all_probs_zero_dict[col][ix] = float(all_probs_zero_dict[col][ix])
                total_probs_zero_sum[ix] += float(all_probs_zero_dict[col][ix])
                total_probs_zero_mul[ix] *= float(all_probs_zero_dict[col][ix])
 
        for ws in window_sizes:
            for pos in range(0, len(total_probs_zero_sum), ws):
                total_probs_zero_sum_dict[ws][subdir_name][some_file][pos] = dict()
                total_probs_zero_sum_dict[ws][subdir_name][some_file][pos]["total_probs_zero_sum_dict"] = sum(total_probs_zero_sum[pos:pos + ws]) / len(all_probs_zero.keys()) / ws < 0.1

        total_probs_zero_sum = [total_prob / len(all_probs_zero.keys()) < 0.1 for total_prob in total_probs_zero_sum]
        all_entries_sum_zero += len(total_probs_zero_sum)
        positive_entries_sum_zero += sum(total_probs_zero_sum)

        for ws in window_sizes:
            for pos in range(0, len(total_probs_zero_mul), ws):
                total_probs_zero_mul_dict[ws][subdir_name][some_file][pos] = dict()
                total_probs_zero_mul_dict[ws][subdir_name][some_file][pos]["total_probs_zero_mul_dict"] = sum(total_probs_zero_mul[pos:pos + ws]) / ws < 0.1

        total_probs_zero_mul = [total_prob < ((10 ** -10) ** len(all_probs_max.keys())) for total_prob in total_probs_zero_mul]
        all_entries_mul_zero += len(total_probs_zero_mul)
        positive_entries_mul_zero += sum(total_probs_zero_mul)

        total_probs_max_sum = [0 for ix in range(len(all_probs_max["distance_probs_max"]))]
        total_probs_max_mul = [1 for ix in range(len(all_probs_max["distance_probs_max"]))]
        all_probs_max_dict = dict()
        for col in all_probs_max:
            if "max" not in col:
                continue
            all_probs_max_dict[col] = list(all_probs_max[col])
            for ix in range(len(all_probs_max_dict[col])):
                all_probs_max_dict[col][ix] = float(all_probs_max_dict[col][ix])
                total_probs_max_sum[ix] += float(all_probs_max_dict[col][ix])
                total_probs_max_mul[ix] *= float(all_probs_max_dict[col][ix])
 
        for ws in window_sizes:
            for pos in range(0, len(total_probs_max_sum), ws):
                total_probs_max_sum_dict[ws][subdir_name][some_file][pos] = dict()
                total_probs_max_sum_dict[ws][subdir_name][some_file][pos]["total_probs_max_sum_dict"] = sum(total_probs_max_sum[pos:pos + ws]) / len(all_probs_max.keys()) / ws < 0.1

        total_probs_max_sum = [total_prob / len(all_probs_max.keys()) < 0.1 for total_prob in total_probs_max_sum]
        all_entries_sum_max += len(total_probs_max_sum)
        positive_entries_sum_max += sum(total_probs_max_sum)

        for ws in window_sizes:
            for pos in range(0, len(total_probs_max_mul), ws):
                total_probs_max_mul_dict[ws][subdir_name][some_file][pos] = dict()
                total_probs_max_mul_dict[ws][subdir_name][some_file][pos]["total_probs_max_mul_dict"] = sum(total_probs_max_mul[pos:pos + ws]) / ws < 0.1

        total_probs_max_mul = [total_prob < (0.1 ** len(all_probs_max.keys())) for total_prob in total_probs_max_mul]
        all_entries_mul_max += len(total_probs_max_mul)
        positive_entries_mul_max += sum(total_probs_max_mul)
        
        total_labels_zero_sum = [0 for ix in range(len(all_labels_zero["distance_labels_zero"]))] 
        all_labels_zero_dict = dict()
        for col in all_labels_zero:
            if "zero" not in col:
                continue
            all_labels_zero_dict[col] = list(all_labels_zero[col])
            for ix in range(len(all_labels_zero_dict[col])):
                all_labels_zero_dict[col][ix] = float(all_labels_zero_dict[col][ix])
                total_labels_zero_sum[ix] += float(all_labels_zero_dict[col][ix]) 
 
        for ws in window_sizes:
            for pos in range(0, len(total_labels_zero_sum), ws):
                total_labels_zero_sum_dict[ws][subdir_name][some_file][pos] = dict()
                total_labels_zero_sum_dict[ws][subdir_name][some_file][pos]["total_labels_zero_sum_dict"] = sum(total_labels_zero_sum[pos:pos + ws]) / len(all_labels_zero.keys()) / ws < 0.1

        total_labels_zero_sum = [total_prob / len(all_labels_zero.keys()) < 0.1 for total_prob in total_labels_zero_sum]
        all_labels_sum_zero += len(total_labels_zero_sum)
        positive_labels_sum_zero += sum(total_labels_zero_sum)
  
        total_labels_max_sum = [0 for ix in range(len(all_labels_max["distance_labels_max"]))] 
        all_labels_max_dict = dict()
        for col in all_labels_max:
            if "max" not in col:
                continue
            all_labels_max_dict[col] = list(all_labels_max[col])
            for ix in range(len(all_labels_max_dict[col])):
                all_labels_max_dict[col][ix] = float(all_labels_max_dict[col][ix])
                total_labels_max_sum[ix] += float(all_labels_max_dict[col][ix]) 
 
        for ws in window_sizes:
            for pos in range(0, len(total_labels_max_sum), ws):
                total_labels_max_sum_dict[ws][subdir_name][some_file][pos] = dict()
                total_labels_max_sum_dict[ws][subdir_name][some_file][pos]["total_labels_max_sum_dict"] = sum(total_labels_max_sum[pos:pos + ws]) / len(all_labels_max.keys()) / ws < 0.1

        total_labels_max_sum = [total_prob / len(all_labels_max.keys()) < 0.1 for total_prob in total_labels_max_sum]
        all_labels_sum_max += len(total_labels_max_sum)
        positive_labels_sum_max += sum(total_labels_max_sum)
 
        all_thr_zero_dict = dict()
        for col in all_thr_zero:
            if "zero" not in col:
                continue
            all_thr_zero_dict[col] = list(all_thr_zero[col])
            for ix in range(len(all_thr_zero_dict[col])):
                all_thr_zero_dict[col][ix] = float(all_thr_zero_dict[col][ix])

        all_thr_max_dict = dict()
        for col in all_thr_max:
            if "max" not in col:
                continue
            all_thr_max_dict[col] = list(all_thr_max[col])
            for ix in range(len(all_thr_max_dict[col])):
                all_thr_max_dict[col][ix] = float(all_thr_max_dict[col][ix])
            
        all_labels_zero_dict = dict()
        for col in all_labels_zero:
            if "zero" not in col:
                continue
            all_labels_zero_dict[col] = list(all_labels_zero[col])
            for ix in range(len(all_labels_zero_dict[col])):
                all_labels_zero_dict[col][ix] = bool(all_labels_zero_dict[col][ix])

        all_labels_max_dict = dict()
        for col in all_labels_max:
            if "max" not in col:
                continue
            all_labels_max_dict[col] = list(all_labels_max[col])
            for ix in range(len(all_labels_max_dict[col])):
                all_labels_max_dict[col][ix] = bool(all_labels_max_dict[col][ix])
        '''
        all_probs_zero_one = is_anomaly(all_probs_zero_dict)
        all_probs_max_one = is_anomaly(all_probs_max_dict, 0.1) 
        which_zero, any_zero, all_zero = is_anomaly_which(all_probs_zero_dict)
        which_max, any_max, all_max = is_anomaly_which(all_probs_max_dict, 0.1)
 
        plot_anomaly(longitudes, latitudes, all_probs_max_one["speed_probs_max"], speed_int, all_probs_max_dict["speed_probs_max"], "speed_probs_max")
        
        for entry in all_probs_zero_one:
            if entry not in all_entries_zero:
                all_entries_zero[entry] = 0
            if entry not in positive_entries_zero:
                positive_entries_zero[entry] = 0
            all_entries_zero[entry] += len(all_probs_zero_one[entry])  
            positive_entries_zero[entry] += sum(all_probs_zero_one[entry])  

        for entry in all_probs_max_one:
            if entry not in all_entries_max:
                all_entries_max[entry] = 0
            if entry not in positive_entries_max:
                positive_entries_max[entry] = 0
            all_entries_max[entry] += len(all_probs_max_one[entry])  
            positive_entries_max[entry] += sum(all_probs_max_one[entry]) 
        '''
        for entry in all_labels_zero_dict:
            if entry not in all_entries_zero:
                all_entries_zero[entry] = 0
            if entry not in positive_entries_zero:
                positive_entries_zero[entry] = 0
            all_entries_zero[entry] += len(all_labels_zero_dict[entry])  
            positive_entries_zero[entry] += sum(all_labels_zero_dict[entry])  

        for entry in all_labels_max_dict:
            if entry not in all_entries_max:
                all_entries_max[entry] = 0
            if entry not in positive_entries_max:
                positive_entries_max[entry] = 0
            all_entries_max[entry] += len(all_labels_max_dict[entry])  
            positive_entries_max[entry] += sum(all_labels_max_dict[entry]) 
        
        #plot_anomaly(longitudes, latitudes, all_labels_max_dict["speed_alternative_labels_max"], speed_int, all_probs_max_dict["speed_alternative_probs_max"], "speed_alternative_labels_max")

        #plot_anomaly(longitudes, latitudes, total_probs_zero_mul, speed_int, all_probs_max_dict["direction_probs_max"], "total_probs_zero_mul")
        ##plot_anomaly(longitudes, latitudes, total_probs_zero_sum, speed_int, all_probs_max_dict["direction_probs_max"], "total_probs_zero_sum")
        
        #plot_anomaly(longitudes, latitudes, total_probs_max_mul, speed_int, all_probs_max_dict["direction_probs_max"], "total_probs_max_mul")
        #plot_anomaly(longitudes, latitudes, total_probs_max_sum, speed_int, all_probs_max_dict["direction_probs_max"], "total_probs_max_sum")

        for entry in all_labels_zero_dict:
            for ws in window_sizes:
                if entry not in labels_window_size_zero[ws]:
                    labels_window_size_zero[ws][entry] = []
                for pos in range(0, len(all_labels_zero_dict[entry]), ws):
                    val = sum(all_labels_zero_dict[entry][pos:pos + ws]) / len(all_labels_zero_dict[entry][pos:pos + ws]) > 0.1
                    labels_window_size_zero[ws][entry].append(val)
                    if pos not in labels_window_size_zero_dict[ws][subdir_name][some_file]:
                        labels_window_size_zero_dict[ws][subdir_name][some_file][pos] = dict()
                    if entry not in labels_window_size_zero_dict[ws][subdir_name][some_file][pos]:
                        labels_window_size_zero_dict[ws][subdir_name][some_file][pos][entry] = val

        for entry in all_probs_zero_dict:
            for ws in window_sizes:
                if entry not in percents_window_size_zero[ws]:
                    percents_window_size_zero[ws][entry] = []
                for pos in range(0, len(all_probs_zero_dict[entry]), ws):
                    val = sum(all_probs_zero_dict[entry][pos:pos + ws]) / len(all_probs_zero_dict[entry][pos:pos + ws]) < 0.1
                    percents_window_size_zero[ws][entry].append(val)
                    if pos not in percents_window_size_zero_dict[ws][subdir_name][some_file]:
                        percents_window_size_zero_dict[ws][subdir_name][some_file][pos] = dict()
                    if entry not in percents_window_size_zero_dict[ws][subdir_name][some_file][pos]:
                        percents_window_size_zero_dict[ws][subdir_name][some_file][pos][entry] = val
            
        for entry in all_labels_max_dict:
            for ws in window_sizes:
                if entry not in labels_window_size_max[ws]:
                    labels_window_size_max[ws][entry] = []
                for pos in range(0, len(all_labels_max_dict[entry]), ws):
                    val = sum(all_labels_max_dict[entry][pos:pos + ws]) / len(all_labels_max_dict[entry][pos:pos + ws]) > 0.1
                    labels_window_size_max[ws][entry].append(val)
                    if pos not in labels_window_size_max_dict[ws][subdir_name][some_file]:
                        labels_window_size_max_dict[ws][subdir_name][some_file][pos] = dict()
                    if entry not in labels_window_size_max_dict[ws][subdir_name][some_file][pos]:
                        labels_window_size_max_dict[ws][subdir_name][some_file][pos][entry] = val

        for entry in all_probs_max_dict:
            for ws in window_sizes:
                if entry not in percents_window_size_max[ws]:
                    percents_window_size_max[ws][entry] = []
                for pos in range(0, len(all_probs_max_dict[entry]), ws):
                    val = sum(all_probs_max_dict[entry][pos:pos + ws]) / len(all_probs_max_dict[entry][pos:pos + ws]) < 0.1
                    percents_window_size_max[ws][entry].append(val)
                    if pos not in percents_window_size_max_dict[ws][subdir_name][some_file]:
                        percents_window_size_max_dict[ws][subdir_name][some_file][pos] = dict()
                    if entry not in percents_window_size_max_dict[ws][subdir_name][some_file][pos]:
                        percents_window_size_max_dict[ws][subdir_name][some_file][pos][entry] = val

save_object("labels_window_size_zero_dict", labels_window_size_zero_dict)
save_object("percents_window_size_zero_dict", percents_window_size_zero_dict)
save_object("labels_window_size_max_dict", labels_window_size_max_dict)
save_object("percents_window_size_max_dict", percents_window_size_max_dict)

save_object("total_probs_zero_mul_dict", total_probs_zero_mul_dict)
save_object("total_probs_zero_sum_dict", total_probs_zero_sum_dict)
save_object("total_probs_max_mul_dict", total_probs_max_mul_dict)
save_object("total_probs_max_sum_dict", total_probs_max_sum_dict)
 
save_object("total_labels_zero_sum_dict", total_labels_zero_sum_dict) 
save_object("total_labels_max_sum_dict", total_labels_max_sum_dict)

for ws in window_sizes:
    for entry in labels_window_size_max[ws]:
        print(ws, entry, sum(labels_window_size_max[ws][entry]) / len(labels_window_size_max[ws][entry]))
    for entry in percents_window_size_max[ws]:
        print(ws, entry, sum(percents_window_size_max[ws][entry]) / len(percents_window_size_max[ws][entry]))

for ws in window_sizes:
    for entry in labels_window_size_zero[ws]:
        print(ws, entry, sum(labels_window_size_zero[ws][entry]) / len(labels_window_size_zero[ws][entry]))
    for entry in percents_window_size_zero[ws]:
        print(ws, entry, sum(percents_window_size_zero[ws][entry]) / len(percents_window_size_zero[ws][entry]))

print("total_probs_zero_mul", positive_entries_mul_zero / all_entries_mul_zero * 100)
print("total_probs_zero_sum", positive_entries_sum_zero / all_entries_sum_zero * 100)

print("total_probs_max_mul", positive_entries_mul_max / all_entries_mul_max * 100)
print("total_probs_max_sum", positive_entries_sum_max / all_entries_sum_max * 100)
 
print("total_labels_zero_sum", positive_labels_sum_zero / all_labels_sum_zero * 100)
 
print("total_labels_max_sum", positive_labels_sum_max / all_labels_sum_max * 100)

for entry in dict(sorted(positive_entries_zero.items(), key = lambda item: item[1])): 
    print(entry, positive_entries_zero[entry] / all_entries_zero[entry] * 100)

for entry in dict(sorted(positive_entries_max.items(), key = lambda item: item[1])): 
    print(entry, positive_entries_max[entry] / all_entries_max[entry] * 100)