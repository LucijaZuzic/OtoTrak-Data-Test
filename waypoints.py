from utilities import *
MAX_VAL = 1000000
 
def return_closest_key(probability, distance, maximum_delta = 0):
    if distance in probability:
        return distance 
    min_delta = MAX_VAL
    new_key = "undefined" 
    for key in probability:
        if key == "undefined":
            continue
        if abs(key - distance) < min_delta and abs(key - distance) <= maximum_delta: 
            min_delta = abs(key - distance) 
            new_key = key 
        if abs(key - distance) == min_delta and key < new_key and abs(key - distance) <= maximum_delta: 
            min_delta = abs(key - distance) 
            new_key = key 
    return new_key

def prob_with_array(probability, probability_in_next_step, probability_in_next_next_step, array_vals, maximum_delta = 0): 
    x = []
    thresholds = []
    labels = []
    n = len(array_vals)
    prev_distance = 0
    prev_prev_distance = 0 
    for i in range(n):
        probability_new = 10 ** -20
        threshold = 10 ** -20
        distance = array_vals[i]
        if i > 1:
            prev_prev_distance = array_vals[i - 2]
        if i > 0:
            prev_distance = array_vals[i - 1]
        if i == 0:
            new_distance = return_closest_key(probability, distance, maximum_delta)
            probability_new = probability[new_distance] 
            threshold = 1 / len(probability)
        if i == 1:
            new_prev_distance = return_closest_key(probability_in_next_step, prev_distance, maximum_delta)
            new_distance = return_closest_key(probability_in_next_step[new_prev_distance], distance, maximum_delta)
            probability_new = probability_in_next_step[new_prev_distance][new_distance]   
            threshold = 1 / len(probability_in_next_step[new_prev_distance])
        if i > 1:
            new_prev_prev_distance = return_closest_key(probability_in_next_next_step, prev_prev_distance, maximum_delta)
            new_prev_distance = return_closest_key(probability_in_next_next_step[new_prev_prev_distance], prev_distance, maximum_delta)
            new_distance = return_closest_key(probability_in_next_next_step[new_prev_prev_distance][new_prev_distance], distance, maximum_delta)
            probability_new = probability_in_next_next_step[new_prev_prev_distance][new_prev_distance][new_distance] 
            threshold = 1 / len(probability_in_next_next_step[new_prev_prev_distance][new_prev_distance])
        x.append(probability_new)  
        thresholds.append(threshold)
        labels.append(probability_new <= threshold)
    return x, thresholds, labels

def process_csv_probs(probab_arrays_all, save_name, vehicle1, r1):
    header = "vehicle,ride,pos,"
    found = False 
    for feat_name in probab_arrays_all:
        header += feat_name + "," 
    header = header[:-1]
    header += "\n" 
    new_csv_content = header 
    max_pos = [len(probab_arrays_all[feat_name]) for feat_name in probab_arrays_all]
    for pos in range(max(max_pos)):
        new_csv_content += str(vehicle1) + "," + str(r1) + "," + str(pos) + ","
        for feat_name in probab_arrays_all: 
            if pos < len(probab_arrays_all[feat_name]):
                new_csv_content += str(probab_arrays_all[feat_name][pos]) 
            new_csv_content += ","
        new_csv_content = new_csv_content[:-1]
        new_csv_content += "\n"  
    csv_file = open(save_name, "w")
    csv_file.write(new_csv_content)
    csv_file.close()
    
probability_of_direction = load_object("probability/probability_of_direction") 
probability_of_direction_in_next_step = load_object("probability/probability_of_direction_in_next_step") 
probability_of_direction_in_next_next_step = load_object("probability/probability_of_direction_in_next_next_step")

probability_of_direction_alternative = load_object("probability/probability_of_direction_alternative") 
probability_of_direction_alternative_in_next_step = load_object("probability/probability_of_direction_alternative_in_next_step") 
probability_of_direction_alternative_in_next_next_step = load_object("probability/probability_of_direction_alternative_in_next_next_step")  

probability_of_direction_abs_alternative = load_object("probability/probability_of_direction_abs_alternative") 
probability_of_direction_abs_alternative_in_next_step = load_object("probability/probability_of_direction_abs_alternative_in_next_step") 
probability_of_direction_abs_alternative_in_next_next_step = load_object("probability/probability_of_direction_abs_alternative_in_next_next_step")  

probability_of_speed_alternative = load_object("probability/probability_of_speed_alternative") 
probability_of_speed_alternative_in_next_step = load_object("probability/probability_of_speed_alternative_in_next_step") 
probability_of_speed_alternative_in_next_next_step = load_object("probability/probability_of_speed_in_next_next_step")  

probability_of_speed = load_object("probability/probability_of_speed") 
probability_of_speed_in_next_step = load_object("probability/probability_of_speed_in_next_step") 
probability_of_speed_in_next_next_step = load_object("probability/probability_of_speed_in_next_next_step")  

probability_of_x_speed_alternative = load_object("probability/probability_of_x_speed_alternative") 
probability_of_x_speed_alternative_in_next_step = load_object("probability/probability_of_x_speed_alternative_in_next_step") 
probability_of_x_speed_alternative_in_next_next_step = load_object("probability/probability_of_x_speed_alternative_in_next_next_step")  

probability_of_x_speed_no_abs_alternative = load_object("probability/probability_of_x_speed_no_abs_alternative") 
probability_of_x_speed_no_abs_alternative_in_next_step = load_object("probability/probability_of_x_speed_no_abs_alternative_in_next_step") 
probability_of_x_speed_no_abs_alternative_in_next_next_step = load_object("probability/probability_of_x_speed_no_abs_alternative_in_next_next_step")  

probability_of_y_speed_alternative = load_object("probability/probability_of_y_speed_alternative") 
probability_of_y_speed_alternative_in_next_step = load_object("probability/probability_of_y_speed_alternative_in_next_step") 
probability_of_y_speed_alternative_in_next_next_step = load_object("probability/probability_of_y_speed_alternative_in_next_next_step")  

probability_of_y_speed_no_abs_alternative = load_object("probability/probability_of_y_speed_no_abs_alternative") 
probability_of_y_speed_no_abs_alternative_in_next_step = load_object("probability/probability_of_y_speed_no_abs_alternative_in_next_step") 
probability_of_y_speed_no_abs_alternative_in_next_next_step = load_object("probability/probability_of_y_speed_no_abs_alternative_in_next_next_step")  

probability_of_distance = load_object("probability/probability_of_distance") 
probability_of_distance_in_next_step = load_object("probability/probability_of_distance_in_next_step") 
probability_of_distance_in_next_next_step = load_object("probability/probability_of_distance_in_next_next_step")  

probability_of_longitude_no_abs = load_object("probability/probability_of_longitude_no_abs") 
probability_of_longitude_no_abs_in_next_step = load_object("probability/probability_of_longitude_no_abs_in_next_step") 
probability_of_longitude_no_abs_in_next_next_step = load_object("probability/probability_of_longitude_no_abs_in_next_next_step")   

probability_of_longitude_sgn = load_object("probability/probability_of_longitude_sgn") 
probability_of_longitude_sgn_in_next_step = load_object("probability/probability_of_longitude_sgn_in_next_step") 
probability_of_longitude_sgn_in_next_next_step = load_object("probability/probability_of_longitude_sgn_in_next_next_step")   

probability_of_longitude = load_object("probability/probability_of_longitude") 
probability_of_longitude_in_next_step = load_object("probability/probability_of_longitude_in_next_step") 
probability_of_longitude_in_next_next_step = load_object("probability/probability_of_longitude_in_next_next_step")   

probability_of_latitude_no_abs = load_object("probability/probability_of_latitude_no_abs") 
probability_of_latitude_no_abs_in_next_step = load_object("probability/probability_of_latitude_no_abs_in_next_step") 
probability_of_latitude_no_abs_in_next_next_step = load_object("probability/probability_of_latitude_no_abs_in_next_next_step")   

probability_of_latitude_sgn = load_object("probability/probability_of_latitude_sgn") 
probability_of_latitude_sgn_in_next_step = load_object("probability/probability_of_latitude_sgn_in_next_step") 
probability_of_latitude_sgn_in_next_next_step = load_object("probability/probability_of_latitude_sgn_in_next_next_step")   

probability_of_latitude = load_object("probability/probability_of_latitude") 
probability_of_latitude_in_next_step = load_object("probability/probability_of_latitude_in_next_step") 
probability_of_latitude_in_next_next_step = load_object("probability/probability_of_latitude_in_next_next_step")   

all_subdirs = os.listdir() 
for subdir_name in all_subdirs: 
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
        speed_probs_zero, speed_thr_zero, speed_labels_zero = prob_with_array(probability_of_speed, probability_of_speed_in_next_step, probability_of_speed_in_next_next_step, speed_int, 0)
        speed_probs_max, speed_thr_max, speed_labels_max = prob_with_array(probability_of_speed, probability_of_speed_in_next_step, probability_of_speed_in_next_next_step, speed_int, MAX_VAL)

        directions = list(file_with_ride["fields_direction"]) 
        direction_int = [np.round(direction, 0) for direction in directions]
        direction_probs_zero, direction_thr_zero, direction_labels_zero = prob_with_array(probability_of_direction, probability_of_direction_in_next_step, probability_of_direction_in_next_next_step, direction_int, 0)
        direction_probs_max, direction_thr_max, direction_labels_max = prob_with_array(probability_of_direction, probability_of_direction_in_next_step, probability_of_direction_in_next_next_step, direction_int, MAX_VAL)
        
        longitude_abs_int = [np.round(abs(longitudes[longitude_index + 1] - longitudes[longitude_index]), 10) for longitude_index in range(len(longitudes) - 1)]
        longitude_abs_probs_zero, longitude_abs_thr_zero, longitude_abs_labels_zero = prob_with_array(probability_of_longitude, probability_of_longitude_in_next_step, probability_of_longitude_in_next_next_step, longitude_abs_int, 0)
        longitude_abs_probs_max, longitude_abs_thr_max, longitude_abs_labels_max = prob_with_array(probability_of_longitude, probability_of_longitude_in_next_step, probability_of_longitude_in_next_next_step, longitude_abs_int, MAX_VAL)
        longitude_int = [np.round(longitudes[longitude_index + 1] - longitudes[longitude_index], 10) for longitude_index in range(len(longitudes) - 1)]
        longitude_probs_zero, longitude_thr_zero, longitude_labels_zero = prob_with_array(probability_of_longitude_no_abs, probability_of_longitude_no_abs_in_next_step, probability_of_longitude_no_abs_in_next_next_step, longitude_int, 0)
        longitude_probs_max, longitude_thr_max, longitude_labels_max = prob_with_array(probability_of_longitude_no_abs, probability_of_longitude_no_abs_in_next_step, probability_of_longitude_no_abs_in_next_next_step, longitude_int, MAX_VAL)
        longitude_dir_int = [longitudes[longitude_index + 1] > longitudes[longitude_index] for longitude_index in range(len(longitudes) - 1)]
        longitude_dir_probs_zero, longitude_dir_thr_zero, longitude_dir_labels_zero = prob_with_array(probability_of_longitude_sgn, probability_of_longitude_sgn_in_next_step, probability_of_longitude_sgn_in_next_next_step, longitude_dir_int, 0)
        longitude_dir_probs_max, longitude_dir_thr_max, longitude_dir_labels_max = prob_with_array(probability_of_longitude_sgn, probability_of_longitude_sgn_in_next_step, probability_of_longitude_sgn_in_next_next_step, longitude_dir_int, MAX_VAL)
        
        latitude_abs_int = [np.round(abs(latitudes[latitude_index + 1] - latitudes[latitude_index]), 10) for latitude_index in range(len(latitudes) - 1)]
        latitude_abs_probs_zero, latitude_abs_thr_zero, latitude_abs_labels_zero = prob_with_array(probability_of_latitude, probability_of_latitude_in_next_step, probability_of_latitude_in_next_next_step, latitude_abs_int, 0)
        latitude_abs_probs_max, latitude_abs_thr_max, latitude_abs_labels_max = prob_with_array(probability_of_latitude, probability_of_latitude_in_next_step, probability_of_latitude_in_next_next_step, latitude_abs_int, MAX_VAL)
        latitude_int = [np.round(latitudes[latitude_index + 1] - latitudes[latitude_index], 10) for latitude_index in range(len(latitudes) - 1)]
        latitude_probs_zero, latitude_thr_zero, latitude_labels_zero = prob_with_array(probability_of_latitude_no_abs, probability_of_latitude_no_abs_in_next_step, probability_of_latitude_no_abs_in_next_next_step, latitude_int, 0)
        latitude_probs_max, latitude_thr_max, latitude_labels_max = prob_with_array(probability_of_latitude_no_abs, probability_of_latitude_no_abs_in_next_step, probability_of_latitude_no_abs_in_next_next_step, latitude_int, MAX_VAL)
        latitude_dir_int = [latitudes[latitude_index + 1] > latitudes[latitude_index] for latitude_index in range(len(latitudes) - 1)]
        latitude_dir_probs_zero, latitude_dir_thr_zero, latitude_dir_labels_zero = prob_with_array(probability_of_latitude_sgn, probability_of_latitude_sgn_in_next_step, probability_of_latitude_sgn_in_next_next_step, latitude_dir_int, 0)
        latitude_dir_probs_max, latitude_dir_thr_max, latitude_dir_labels_max = prob_with_array(probability_of_latitude_sgn, probability_of_latitude_sgn_in_next_step, probability_of_latitude_sgn_in_next_next_step, latitude_dir_int, MAX_VAL)
        
        distance_int = [np.round(np.sqrt((longitudes[distance_index + 1] - longitudes[distance_index]) ** 2 + (latitudes[distance_index + 1] - latitudes[distance_index]) ** 2), 5) for distance_index in range(len(longitudes) - 1)]
        distance_probs_zero, distance_thr_zero, distance_labels_zero = prob_with_array(probability_of_distance, probability_of_distance_in_next_step, probability_of_distance_in_next_next_step, distance_int, 0)
        distance_probs_max, distance_thr_max, distance_labels_max = prob_with_array(probability_of_distance, probability_of_distance_in_next_step, probability_of_distance_in_next_next_step, distance_int, MAX_VAL)

        distance_euclid_int = [np.sqrt((longitudes[distance_index + 1] - longitudes[distance_index]) ** 2 + (latitudes[distance_index + 1] - latitudes[distance_index]) ** 2) for distance_index in range(len(longitudes) - 1)]
        speed_alternative_int = [np.round(distance_euclid_int[speed_alternative_index] / times_delays[speed_alternative_index], 5) for speed_alternative_index in range(len(times_delays))]
        speed_alternative_probs_zero, speed_alternative_thr_zero, speed_alternative_labels_zero = prob_with_array(probability_of_speed_alternative, probability_of_speed_alternative_in_next_step, probability_of_speed_alternative_in_next_next_step, speed_alternative_int, 0)
        speed_alternative_probs_max, speed_alternative_thr_max, speed_alternative_labels_max = prob_with_array(probability_of_speed_alternative, probability_of_speed_alternative_in_next_step, probability_of_speed_alternative_in_next_next_step, speed_alternative_int, MAX_VAL)

        distance_x_int = [longitudes[distance_index + 1] - longitudes[distance_index] for distance_index in range(len(longitudes) - 1)]
        distance_x_abs_int = [abs(longitudes[distance_index + 1] - longitudes[distance_index]) for distance_index in range(len(longitudes) - 1)]
        x_speed_alternative_int = [np.round(distance_x_abs_int[x_speed_alternative_index] / times_delays[x_speed_alternative_index], 5) for x_speed_alternative_index in range(len(times_delays))]
        x_speed_no_abs_alternative_int = [np.round(distance_int[x_speed_no_abs_alternative_index] / times_delays[x_speed_no_abs_alternative_index], 5) for x_speed_no_abs_alternative_index in range(len(times_delays))]
        x_speed_alternative_probs_zero, x_speed_alternative_thr_zero, x_speed_alternative_labels_zero = prob_with_array(probability_of_x_speed_alternative, probability_of_x_speed_alternative_in_next_step, probability_of_x_speed_alternative_in_next_next_step, x_speed_alternative_int, 0)
        x_speed_alternative_probs_max, x_speed_alternative_thr_max, x_speed_alternative_labels_max = prob_with_array(probability_of_x_speed_alternative, probability_of_x_speed_alternative_in_next_step, probability_of_x_speed_alternative_in_next_next_step, x_speed_alternative_int, MAX_VAL)
        x_speed_no_abs_alternative_probs_zero, x_speed_no_abs_alternative_thr_zero, x_speed_no_abs_alternative_labels_zero = prob_with_array(probability_of_x_speed_no_abs_alternative, probability_of_x_speed_no_abs_alternative_in_next_step, probability_of_x_speed_no_abs_alternative_in_next_next_step, x_speed_no_abs_alternative_int, 0)
        x_speed_no_abs_alternative_probs_max, x_speed_no_abs_alternative_thr_max, x_speed_no_abs_alternative_labels_max = prob_with_array(probability_of_x_speed_no_abs_alternative, probability_of_x_speed_no_abs_alternative_in_next_step, probability_of_x_speed_no_abs_alternative_in_next_next_step, x_speed_no_abs_alternative_int, MAX_VAL)

        distance_y_int = [latitudes[distance_index + 1] - latitudes[distance_index] for distance_index in range(len(latitudes) - 1)]
        distance_y_abs_int = [abs(latitudes[distance_index + 1] - latitudes[distance_index]) for distance_index in range(len(latitudes) - 1)]
        y_speed_alternative_int = [np.round(distance_y_abs_int[y_speed_alternative_index] / times_delays[y_speed_alternative_index], 5) for y_speed_alternative_index in range(len(times_delays))]
        y_speed_no_abs_alternative_int = [np.round(distance_int[y_speed_no_abs_alternative_index] / times_delays[y_speed_no_abs_alternative_index], 5) for y_speed_no_abs_alternative_index in range(len(times_delays))]
        y_speed_alternative_probs_zero, y_speed_alternative_thr_zero, y_speed_alternative_labels_zero = prob_with_array(probability_of_y_speed_alternative, probability_of_y_speed_alternative_in_next_step, probability_of_y_speed_alternative_in_next_next_step, y_speed_alternative_int, 0)
        y_speed_alternative_probs_max, y_speed_alternative_thr_max, y_speed_alternative_labels_max = prob_with_array(probability_of_y_speed_alternative, probability_of_y_speed_alternative_in_next_step, probability_of_y_speed_alternative_in_next_next_step, y_speed_alternative_int, MAX_VAL)
        y_speed_no_abs_alternative_probs_zero, y_speed_no_abs_alternative_thr_zero, y_speed_no_abs_alternative_labels_zero = prob_with_array(probability_of_y_speed_no_abs_alternative, probability_of_y_speed_no_abs_alternative_in_next_step, probability_of_y_speed_no_abs_alternative_in_next_next_step, y_speed_no_abs_alternative_int, 0)
        y_speed_no_abs_alternative_probs_max, y_speed_no_abs_alternative_thr_max, y_speed_no_abs_alternative_labels_max = prob_with_array(probability_of_y_speed_no_abs_alternative, probability_of_y_speed_no_abs_alternative_in_next_step, probability_of_y_speed_no_abs_alternative_in_next_next_step, y_speed_no_abs_alternative_int, MAX_VAL)

        direction_alternative_int = []
        for heading_alternative_index in range(len(longitudes) - 1): 
            direction_alternative_int.append((360 + np.round(np.arctan(distance_y_int[heading_alternative_index], distance_x_int[heading_alternative_index]) / np.pi * 180, 0)) % 360)
            
        direction_abs_alternative_int = []
        for heading_abs_alternative_index in range(len(longitudes) - 1):
            direction_abs_alternative_int.append((360 + np.round(np.arctan(distance_y_abs_int[heading_abs_alternative_index], distance_x_abs_int[heading_abs_alternative_index]) / np.pi * 180, 0)) % 360)
            
        direction_alternative_probs_zero, direction_alternative_thr_zero, direction_alternative_labels_zero = prob_with_array(probability_of_direction_alternative, probability_of_direction_alternative_in_next_step, probability_of_direction_alternative_in_next_next_step, direction_alternative_int, 0)
        direction_alternative_probs_max, direction_alternative_thr_max, direction_alternative_labels_max = prob_with_array(probability_of_direction_alternative, probability_of_direction_alternative_in_next_step, probability_of_direction_alternative_in_next_next_step, direction_alternative_int, MAX_VAL)
        direction_abs_alternative_probs_zero, direction_abs_alternative_thr_zero, direction_abs_alternative_labels_zero = prob_with_array(probability_of_direction_abs_alternative, probability_of_direction_abs_alternative_in_next_step, probability_of_direction_abs_alternative_in_next_next_step, direction_abs_alternative_int, 0)
        direction_abs_alternative_probs_max, direction_abs_alternative_thr_max, direction_abs_alternative_labels_max = prob_with_array(probability_of_direction_abs_alternative, probability_of_direction_abs_alternative_in_next_step, probability_of_direction_abs_alternative_in_next_next_step, direction_abs_alternative_int, MAX_VAL)
     
        all_probs_zero = {
            "speed_probs_zero": speed_probs_zero,
            "direction_probs_zero": direction_probs_zero,
            "longitude_abs_probs_zero": longitude_abs_probs_zero,
            "longitude_probs_zero": longitude_probs_zero,
            "longitude_dir_probs_zero": longitude_dir_probs_zero,
            "latitude_abs_probs_zero": latitude_abs_probs_zero,
            "latitude_probs_zero": latitude_probs_zero,
            "latitude_dir_probs_zero": latitude_dir_probs_zero,
            "distance_probs_zero": distance_probs_zero,
            "speed_alternative_probs_zero": speed_alternative_probs_zero,
            "x_speed_alternative_probs_zero": x_speed_alternative_probs_zero,
            "x_speed_no_abs_alternative_probs_zero": x_speed_no_abs_alternative_probs_zero,
            "y_speed_alternative_probs_zero": y_speed_alternative_probs_zero,
            "y_speed_no_abs_alternative_probs_zero": y_speed_no_abs_alternative_probs_zero,
            "direction_alternative_probs_zero": direction_alternative_probs_zero,
            "direction_abs_alternative_probs_zero": direction_abs_alternative_probs_zero, 
        }

        all_probs_max = {
            "speed_probs_max": speed_probs_max,
            "direction_probs_max": direction_probs_max,
            "longitude_abs_probs_max": longitude_abs_probs_max,
            "longitude_probs_max": longitude_probs_max,
            "longitude_dir_probs_max": longitude_dir_probs_max,
            "latitude_abs_probs_max": latitude_abs_probs_max,
            "latitude_probs_max": latitude_probs_max,
            "latitude_dir_probs_max": latitude_dir_probs_max,
            "distance_probs_max": distance_probs_max,
            "speed_alternative_probs_max": speed_alternative_probs_max,
            "x_speed_alternative_probs_max": x_speed_alternative_probs_max,
            "x_speed_no_abs_alternative_probs_max": x_speed_no_abs_alternative_probs_max,
            "y_speed_alternative_probs_max": y_speed_alternative_probs_max,
            "y_speed_no_abs_alternative_probs_max": y_speed_no_abs_alternative_probs_max,
            "direction_alternative_probs_max": direction_alternative_probs_max,
            "direction_abs_alternative_probs_max": direction_abs_alternative_probs_max, 
        }
        
        all_probs_zero_max = {
            "speed_probs_zero": speed_probs_zero,
            "direction_probs_zero": direction_probs_zero,
            "longitude_abs_probs_zero": longitude_abs_probs_zero,
            "longitude_probs_zero": longitude_probs_zero,
            "longitude_dir_probs_zero": longitude_dir_probs_zero,
            "latitude_abs_probs_zero": latitude_abs_probs_zero,
            "latitude_probs_zero": latitude_probs_zero,
            "latitude_dir_probs_zero": latitude_dir_probs_zero,
            "distance_probs_zero": distance_probs_zero,
            "speed_alternative_probs_zero": speed_alternative_probs_zero,
            "x_speed_alternative_probs_zero": x_speed_alternative_probs_zero,
            "x_speed_no_abs_alternative_probs_zero": x_speed_no_abs_alternative_probs_zero,
            "y_speed_alternative_probs_zero": y_speed_alternative_probs_zero,
            "y_speed_no_abs_alternative_probs_zero": y_speed_no_abs_alternative_probs_zero,
            "direction_alternative_probs_zero": direction_alternative_probs_zero,
            "direction_abs_alternative_probs_zero": direction_abs_alternative_probs_zero,  
            "speed_probs_max": speed_probs_max,
            "direction_probs_max": direction_probs_max,
            "longitude_abs_probs_max": longitude_abs_probs_max,
            "longitude_probs_max": longitude_probs_max,
            "longitude_dir_probs_max": longitude_dir_probs_max,
            "latitude_abs_probs_max": latitude_abs_probs_max,
            "latitude_probs_max": latitude_probs_max,
            "latitude_dir_probs_max": latitude_dir_probs_max,
            "distance_probs_max": distance_probs_max,
            "speed_alternative_probs_max": speed_alternative_probs_max,
            "x_speed_alternative_probs_max": x_speed_alternative_probs_max,
            "x_speed_no_abs_alternative_probs_max": x_speed_no_abs_alternative_probs_max,
            "y_speed_alternative_probs_max": y_speed_alternative_probs_max,
            "y_speed_no_abs_alternative_probs_max": y_speed_no_abs_alternative_probs_max,
            "direction_alternative_probs_max": direction_alternative_probs_max,
            "direction_abs_alternative_probs_max": direction_abs_alternative_probs_max, 
        }

        short_file = some_file.replace("events_", "").replace(".csv", "")

        if not os.path.isdir("all_probs_zero_max/" + str(subdir_name) + "/" + str(short_file)):
            os.makedirs("all_probs_zero_max/" + str(subdir_name) + "/" + str(short_file))
        process_csv_probs(all_probs_zero_max, "all_probs_zero_max/" + str(subdir_name) + "/" + str(short_file) + "/all_probs_zero_max_" + str(subdir_name) + "_" + str(short_file) + ".csv", subdir_name, short_file)
       
        if not os.path.isdir("all_probs_max/" + str(subdir_name) + "/" + str(short_file)):
            os.makedirs("all_probs_max/" + str(subdir_name) + "/" + str(short_file))
        process_csv_probs(all_probs_max, "all_probs_max/" + str(subdir_name) + "/" + str(short_file) + "/all_probs_max_" + str(subdir_name) + "_" + str(short_file) + ".csv", subdir_name, short_file)
        
        if not os.path.isdir("all_probs_zero/" + str(subdir_name) + "/" + str(short_file)):
            os.makedirs("all_probs_zero/" + str(subdir_name) + "/" + str(short_file))
        process_csv_probs(all_probs_zero, "all_probs_zero/" + str(subdir_name) + "/" + str(short_file) + "/all_probs_zero_" + str(subdir_name) + "_" + str(short_file) + ".csv", subdir_name, short_file)
       
        all_thr_zero = {
            "speed_thr_zero": speed_thr_zero,
            "direction_thr_zero": direction_thr_zero,
            "longitude_abs_thr_zero": longitude_abs_thr_zero,
            "longitude_thr_zero": longitude_thr_zero,
            "longitude_dir_thr_zero": longitude_dir_thr_zero,
            "latitude_abs_thr_zero": latitude_abs_thr_zero,
            "latitude_thr_zero": latitude_thr_zero,
            "latitude_dir_thr_zero": latitude_dir_thr_zero,
            "distance_thr_zero": distance_thr_zero,
            "speed_alternative_thr_zero": speed_alternative_thr_zero,
            "x_speed_alternative_thr_zero": x_speed_alternative_thr_zero,
            "x_speed_no_abs_alternative_thr_zero": x_speed_no_abs_alternative_thr_zero,
            "y_speed_alternative_thr_zero": y_speed_alternative_thr_zero,
            "y_speed_no_abs_alternative_thr_zero": y_speed_no_abs_alternative_thr_zero,
            "direction_alternative_thr_zero": direction_alternative_thr_zero,
            "direction_abs_alternative_thr_zero": direction_abs_alternative_thr_zero, 
        }

        all_thr_max = {
            "speed_thr_max": speed_thr_max,
            "direction_thr_max": direction_thr_max,
            "longitude_abs_thr_max": longitude_abs_thr_max,
            "longitude_thr_max": longitude_thr_max,
            "longitude_dir_thr_max": longitude_dir_thr_max,
            "latitude_abs_thr_max": latitude_abs_thr_max,
            "latitude_thr_max": latitude_thr_max,
            "latitude_dir_thr_max": latitude_dir_thr_max,
            "distance_thr_max": distance_thr_max,
            "speed_alternative_thr_max": speed_alternative_thr_max,
            "x_speed_alternative_thr_max": x_speed_alternative_thr_max,
            "x_speed_no_abs_alternative_thr_max": x_speed_no_abs_alternative_thr_max,
            "y_speed_alternative_thr_max": y_speed_alternative_thr_max,
            "y_speed_no_abs_alternative_thr_max": y_speed_no_abs_alternative_thr_max,
            "direction_alternative_thr_max": direction_alternative_thr_max,
            "direction_abs_alternative_thr_max": direction_abs_alternative_thr_max, 
        }
        
        all_thr_zero_max = {
            "speed_thr_zero": speed_thr_zero,
            "direction_thr_zero": direction_thr_zero,
            "longitude_abs_thr_zero": longitude_abs_thr_zero,
            "longitude_thr_zero": longitude_thr_zero,
            "longitude_dir_thr_zero": longitude_dir_thr_zero,
            "latitude_abs_thr_zero": latitude_abs_thr_zero,
            "latitude_thr_zero": latitude_thr_zero,
            "latitude_dir_thr_zero": latitude_dir_thr_zero,
            "distance_thr_zero": distance_thr_zero,
            "speed_alternative_thr_zero": speed_alternative_thr_zero,
            "x_speed_alternative_thr_zero": x_speed_alternative_thr_zero,
            "x_speed_no_abs_alternative_thr_zero": x_speed_no_abs_alternative_thr_zero,
            "y_speed_alternative_thr_zero": y_speed_alternative_thr_zero,
            "y_speed_no_abs_alternative_thr_zero": y_speed_no_abs_alternative_thr_zero,
            "direction_alternative_thr_zero": direction_alternative_thr_zero,
            "direction_abs_alternative_thr_zero": direction_abs_alternative_thr_zero,  
            "speed_thr_max": speed_thr_max,
            "direction_thr_max": direction_thr_max,
            "longitude_abs_thr_max": longitude_abs_thr_max,
            "longitude_thr_max": longitude_thr_max,
            "longitude_dir_thr_max": longitude_dir_thr_max,
            "latitude_abs_thr_max": latitude_abs_thr_max,
            "latitude_thr_max": latitude_thr_max,
            "latitude_dir_thr_max": latitude_dir_thr_max,
            "distance_thr_max": distance_thr_max,
            "speed_alternative_thr_max": speed_alternative_thr_max,
            "x_speed_alternative_thr_max": x_speed_alternative_thr_max,
            "x_speed_no_abs_alternative_thr_max": x_speed_no_abs_alternative_thr_max,
            "y_speed_alternative_thr_max": y_speed_alternative_thr_max,
            "y_speed_no_abs_alternative_thr_max": y_speed_no_abs_alternative_thr_max,
            "direction_alternative_thr_max": direction_alternative_thr_max,
            "direction_abs_alternative_thr_max": direction_abs_alternative_thr_max, 
        }

        short_file = some_file.replace("events_", "").replace(".csv", "")

        if not os.path.isdir("all_thr_zero_max/" + str(subdir_name) + "/" + str(short_file)):
            os.makedirs("all_thr_zero_max/" + str(subdir_name) + "/" + str(short_file))
        process_csv_probs(all_thr_zero_max, "all_thr_zero_max/" + str(subdir_name) + "/" + str(short_file) + "/all_thr_zero_max_" + str(subdir_name) + "_" + str(short_file) + ".csv", subdir_name, short_file)
       
        if not os.path.isdir("all_thr_max/" + str(subdir_name) + "/" + str(short_file)):
            os.makedirs("all_thr_max/" + str(subdir_name) + "/" + str(short_file))
        process_csv_probs(all_thr_max, "all_thr_max/" + str(subdir_name) + "/" + str(short_file) + "/all_thr_max_" + str(subdir_name) + "_" + str(short_file) + ".csv", subdir_name, short_file)
        
        if not os.path.isdir("all_thr_zero/" + str(subdir_name) + "/" + str(short_file)):
            os.makedirs("all_thr_zero/" + str(subdir_name) + "/" + str(short_file))
        process_csv_probs(all_thr_zero, "all_thr_zero/" + str(subdir_name) + "/" + str(short_file) + "/all_thr_zero_" + str(subdir_name) + "_" + str(short_file) + ".csv", subdir_name, short_file)
       
        all_labels_zero = {
            "speed_labels_zero": speed_labels_zero,
            "direction_labels_zero": direction_labels_zero,
            "longitude_abs_labels_zero": longitude_abs_labels_zero,
            "longitude_labels_zero": longitude_labels_zero,
            "longitude_dir_labels_zero": longitude_dir_labels_zero,
            "latitude_abs_labels_zero": latitude_abs_labels_zero,
            "latitude_labels_zero": latitude_labels_zero,
            "latitude_dir_labels_zero": latitude_dir_labels_zero,
            "distance_labels_zero": distance_labels_zero,
            "speed_alternative_labels_zero": speed_alternative_labels_zero,
            "x_speed_alternative_labels_zero": x_speed_alternative_labels_zero,
            "x_speed_no_abs_alternative_labels_zero": x_speed_no_abs_alternative_labels_zero,
            "y_speed_alternative_labels_zero": y_speed_alternative_labels_zero,
            "y_speed_no_abs_alternative_labels_zero": y_speed_no_abs_alternative_labels_zero,
            "direction_alternative_labels_zero": direction_alternative_labels_zero,
            "direction_abs_alternative_labels_zero": direction_abs_alternative_labels_zero, 
        }

        all_labels_max = {
            "speed_labels_max": speed_labels_max,
            "direction_labels_max": direction_labels_max,
            "longitude_abs_labels_max": longitude_abs_labels_max,
            "longitude_labels_max": longitude_labels_max,
            "longitude_dir_labels_max": longitude_dir_labels_max,
            "latitude_abs_labels_max": latitude_abs_labels_max,
            "latitude_labels_max": latitude_labels_max,
            "latitude_dir_labels_max": latitude_dir_labels_max,
            "distance_labels_max": distance_labels_max,
            "speed_alternative_labels_max": speed_alternative_labels_max,
            "x_speed_alternative_labels_max": x_speed_alternative_labels_max,
            "x_speed_no_abs_alternative_labels_max": x_speed_no_abs_alternative_labels_max,
            "y_speed_alternative_labels_max": y_speed_alternative_labels_max,
            "y_speed_no_abs_alternative_labels_max": y_speed_no_abs_alternative_labels_max,
            "direction_alternative_labels_max": direction_alternative_labels_max,
            "direction_abs_alternative_labels_max": direction_abs_alternative_labels_max, 
        }
        
        all_labels_zero_max = {
            "speed_labels_zero": speed_labels_zero,
            "direction_labels_zero": direction_labels_zero,
            "longitude_abs_labels_zero": longitude_abs_labels_zero,
            "longitude_labels_zero": longitude_labels_zero,
            "longitude_dir_labels_zero": longitude_dir_labels_zero,
            "latitude_abs_labels_zero": latitude_abs_labels_zero,
            "latitude_labels_zero": latitude_labels_zero,
            "latitude_dir_labels_zero": latitude_dir_labels_zero,
            "distance_labels_zero": distance_labels_zero,
            "speed_alternative_labels_zero": speed_alternative_labels_zero,
            "x_speed_alternative_labels_zero": x_speed_alternative_labels_zero,
            "x_speed_no_abs_alternative_labels_zero": x_speed_no_abs_alternative_labels_zero,
            "y_speed_alternative_labels_zero": y_speed_alternative_labels_zero,
            "y_speed_no_abs_alternative_labels_zero": y_speed_no_abs_alternative_labels_zero,
            "direction_alternative_labels_zero": direction_alternative_labels_zero,
            "direction_abs_alternative_labels_zero": direction_abs_alternative_labels_zero,  
            "speed_labels_max": speed_labels_max,
            "direction_labels_max": direction_labels_max,
            "longitude_abs_labels_max": longitude_abs_labels_max,
            "longitude_labels_max": longitude_labels_max,
            "longitude_dir_labels_max": longitude_dir_labels_max,
            "latitude_abs_labels_max": latitude_abs_labels_max,
            "latitude_labels_max": latitude_labels_max,
            "latitude_dir_labels_max": latitude_dir_labels_max,
            "distance_labels_max": distance_labels_max,
            "speed_alternative_labels_max": speed_alternative_labels_max,
            "x_speed_alternative_labels_max": x_speed_alternative_labels_max,
            "x_speed_no_abs_alternative_labels_max": x_speed_no_abs_alternative_labels_max,
            "y_speed_alternative_labels_max": y_speed_alternative_labels_max,
            "y_speed_no_abs_alternative_labels_max": y_speed_no_abs_alternative_labels_max,
            "direction_alternative_labels_max": direction_alternative_labels_max,
            "direction_abs_alternative_labels_max": direction_abs_alternative_labels_max, 
        }

        short_file = some_file.replace("events_", "").replace(".csv", "")

        if not os.path.isdir("all_labels_zero_max/" + str(subdir_name) + "/" + str(short_file)):
            os.makedirs("all_labels_zero_max/" + str(subdir_name) + "/" + str(short_file))
        process_csv_probs(all_labels_zero_max, "all_labels_zero_max/" + str(subdir_name) + "/" + str(short_file) + "/all_labels_zero_max_" + str(subdir_name) + "_" + str(short_file) + ".csv", subdir_name, short_file)
       
        if not os.path.isdir("all_labels_max/" + str(subdir_name) + "/" + str(short_file)):
            os.makedirs("all_labels_max/" + str(subdir_name) + "/" + str(short_file))
        process_csv_probs(all_labels_max, "all_labels_max/" + str(subdir_name) + "/" + str(short_file) + "/all_labels_max_" + str(subdir_name) + "_" + str(short_file) + ".csv", subdir_name, short_file)
        
        if not os.path.isdir("all_labels_zero/" + str(subdir_name) + "/" + str(short_file)):
            os.makedirs("all_labels_zero/" + str(subdir_name) + "/" + str(short_file))
        process_csv_probs(all_labels_zero, "all_labels_zero/" + str(subdir_name) + "/" + str(short_file) + "/all_labels_zero_" + str(subdir_name) + "_" + str(short_file) + ".csv", subdir_name, short_file)
       
       

