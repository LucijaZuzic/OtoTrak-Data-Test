from utilities import *
     
predicted_time = load_object("predicted/predicted_time") 
probability_of_time = load_object("probability/probability_of_time") 
probability_of_time_in_next_step = load_object("probability/probability_of_time_in_next_step") 
probability_of_time_in_next_next_step = load_object("probability/probability_of_time_in_next_next_step") 
#print("probability/probability_of_time", min(probability_of_time.keys()), max(probability_of_time.keys()))

predicted_distance = load_object("predicted/predicted_distance") 
probability_of_distance = load_object("probability/probability_of_distance") 
probability_of_distance_in_next_step = load_object("probability/probability_of_distance_in_next_step") 
probability_of_distance_in_next_next_step = load_object("probability/probability_of_distance_in_next_next_step") 
#print("probability/probability_of_distance", min(probability_of_distance.keys()), max(probability_of_distance.keys()))

predicted_longitude = load_object("predicted/predicted_longitude") 
probability_of_longitude = load_object("probability/probability_of_longitude") 
probability_of_longitude_in_next_step = load_object("probability/probability_of_longitude_in_next_step") 
probability_of_longitude_in_next_next_step = load_object("probability/probability_of_longitude_in_next_next_step") 
#print("probability/probability_of_longitude", min(probability_of_longitude.keys()), max(probability_of_longitude.keys()))

predicted_latitude = load_object("predicted/predicted_latitude") 
probability_of_latitude = load_object("probability/probability_of_latitude") 
probability_of_latitude_in_next_step = load_object("probability/probability_of_latitude_in_next_step") 
probability_of_latitude_in_next_next_step = load_object("probability/probability_of_latitude_in_next_next_step") 
#print("probability/probability_of_latitude", min(probability_of_latitude.keys()), max(probability_of_latitude.keys()))

predicted_longitude_sgn = load_object("predicted/predicted_longitude_sgn") 
probability_of_longitude_sgn = load_object("probability/probability_of_longitude_sgn") 
probability_of_longitude_sgn_in_next_step = load_object("probability/probability_of_longitude_sgn_in_next_step") 
probability_of_longitude_sgn_in_next_next_step = load_object("probability/probability_of_longitude_sgn_in_next_next_step") 
#print("probability/probability_of_longitude_sgn", min(probability_of_longitude_sgn.keys()), max(probability_of_longitude_sgn.keys()))

predicted_latitude_sgn = load_object("predicted/predicted_latitude_sgn") 
probability_of_latitude_sgn = load_object("probability/probability_of_latitude_sgn") 
probability_of_latitude_sgn_in_next_step = load_object("probability/probability_of_latitude_sgn_in_next_step") 
probability_of_latitude_sgn_in_next_next_step = load_object("probability/probability_of_latitude_sgn_in_next_next_step") 
#print("probability/probability_of_latitude_sgn", min(probability_of_latitude_sgn.keys()), max(probability_of_latitude_sgn.keys()))

predicted_longitude_no_abs = load_object("predicted/predicted_longitude_no_abs") 
probability_of_longitude_no_abs = load_object("probability/probability_of_longitude_no_abs") 
probability_of_longitude_no_abs_in_next_step = load_object("probability/probability_of_longitude_no_abs_in_next_step") 
probability_of_longitude_no_abs_in_next_next_step = load_object("probability/probability_of_longitude_no_abs_in_next_next_step") 
#print("probability/probability_of_longitude_no_abs", min(probability_of_longitude_no_abs.keys()), max(probability_of_longitude_no_abs.keys()))

predicted_latitude_no_abs = load_object("predicted/predicted_latitude_no_abs") 
probability_of_latitude_no_abs = load_object("probability/probability_of_latitude_no_abs") 
probability_of_latitude_no_abs_in_next_step = load_object("probability/probability_of_latitude_no_abs_in_next_step") 
probability_of_latitude_no_abs_in_next_next_step = load_object("probability/probability_of_latitude_no_abs_in_next_next_step") 
#print("probability/probability_of_latitude_no_abs", min(probability_of_latitude_no_abs.keys()), max(probability_of_latitude_no_abs.keys()))

predicted_direction = load_object("predicted/predicted_direction") 
probability_of_direction = load_object("probability/probability_of_direction") 
probability_of_direction_in_next_step = load_object("probability/probability_of_direction_in_next_step") 
probability_of_direction_in_next_next_step = load_object("probability/probability_of_direction_in_next_next_step") 
#print("probability/probability_of_direction", min(probability_of_direction.keys()), max(probability_of_direction.keys()))

predicted_direction_alternative = load_object("predicted/predicted_direction_alternative") 
probability_of_direction_alternative = load_object("probability/probability_of_direction_alternative") 
probability_of_direction_alternative_in_next_step = load_object("probability/probability_of_direction_alternative_in_next_step") 
probability_of_direction_alternative_in_next_next_step = load_object("probability/probability_of_direction_alternative_in_next_next_step") 
#print("probability/probability_of_direction_alternative", min(probability_of_direction_alternative.keys()), max(probability_of_direction_alternative.keys()))
 
predicted_speed = load_object("predicted/predicted_speed") 
probability_of_speed = load_object("probability/probability_of_speed") 
probability_of_speed_in_next_step = load_object("probability/probability_of_speed_in_next_step") 
probability_of_speed_in_next_next_step = load_object("probability/probability_of_speed_in_next_next_step") 
#print("probability/probability_of_speed", min(probability_of_speed.keys()), max(probability_of_speed.keys()))

predicted_speed_alternative = load_object("predicted/predicted_speed_alternative") 
probability_of_speed_alternative = load_object("probability/probability_of_speed_alternative") 
probability_of_speed_alternative_in_next_step = load_object("probability/probability_of_speed_alternative_in_next_step") 
probability_of_speed_alternative_in_next_next_step = load_object("probability/probability_of_speed_alternative_in_next_next_step") 
#print("probability/probability_of_speed_alternative", min(probability_of_speed_alternative.keys()), max(probability_of_speed_alternative.keys()))

predicted_x_speed_alternative = load_object("predicted/predicted_x_speed_alternative") 
probability_of_x_speed_alternative = load_object("probability/probability_of_x_speed_alternative") 
probability_of_x_speed_alternative_in_next_step = load_object("probability/probability_of_x_speed_alternative_in_next_step") 
probability_of_x_speed_alternative_in_next_next_step = load_object("probability/probability_of_x_speed_alternative_in_next_next_step") 
#print("probability/probability_of_x_speed_alternative", min(probability_of_x_speed_alternative.keys()), max(probability_of_x_speed_alternative.keys()))

predicted_y_speed_alternative = load_object("predicted/predicted_y_speed_alternative") 
probability_of_y_speed_alternative = load_object("probability/probability_of_y_speed_alternative") 
probability_of_y_speed_alternative_in_next_step = load_object("probability/probability_of_y_speed_alternative_in_next_step") 
probability_of_y_speed_alternative_in_next_next_step = load_object("probability/probability_of_y_speed_alternative_in_next_next_step") 
#print("probability/probability_of_y_speed_alternative", min(probability_of_y_speed_alternative.keys()), max(probability_of_y_speed_alternative.keys()))

predicted_x_speed_no_abs_alternative = load_object("predicted/predicted_x_speed_no_abs_alternative") 
probability_of_x_speed_no_abs_alternative = load_object("probability/probability_of_x_speed_no_abs_alternative") 
probability_of_x_speed_no_abs_alternative_in_next_step = load_object("probability/probability_of_x_speed_no_abs_alternative_in_next_step") 
probability_of_x_speed_no_abs_alternative_in_next_next_step = load_object("probability/probability_of_x_speed_no_abs_alternative_in_next_next_step") 
#print("probability/probability_of_x_speed_no_abs_alternative", min(probability_of_x_speed_no_abs_alternative.keys()), max(probability_of_x_speed_no_abs_alternative.keys()))

predicted_y_speed_no_abs_alternative = load_object("predicted/predicted_y_speed_no_abs_alternative") 
probability_of_y_speed_no_abs_alternative = load_object("probability/probability_of_y_speed_no_abs_alternative") 
probability_of_y_speed_no_abs_alternative_in_next_step = load_object("probability/probability_of_y_speed_no_abs_alternative_in_next_step") 
probability_of_y_speed_no_abs_alternative_in_next_next_step = load_object("probability/probability_of_y_speed_no_abs_alternative_in_next_next_step") 
#print("probability/probability_of_y_speed_no_abs_alternative", min(probability_of_y_speed_no_abs_alternative.keys()), max(probability_of_y_speed_no_abs_alternative.keys()))

all_subdirs = os.listdir() 

path_lengths = []

#pair 1: longitudes (no abs) + latitudes (no abs) 4
#pair 2: longitudes (no abs) + y_speed (no abs) * time 4
#pair 3: x_speed (no abs) * time + latitudes (no abs) 4
#pair 4: x_speed (no abs) * time + y_speed (no abs) * time 4
#pair 5: distance + heading (heading_alternative) 2
#pair 6: speed (speed_alternative) * time + heading (heading_alternative) 4

times_cumulative = []

long_cumulative = []
lat_cumulative = []

long_no_abs_cumulative = []
lat_no_abs_cumulative = []

x_speed_cumulative = []
y_speed_cumulative = []

x_speed_no_abs_cumulative = []
y_speed_no_abs_cumulative = []

longitude_from_distance_heading_alternative = []
latitude_from_distance_heading_alternative = []

longitude_from_distance_heading = []
latitude_from_distance_heading = []

longitude_from_speed_alternative_time_heading_alternative = []
latitude_from_speed_alternative_time_heading_alternative = []

longitude_from_speed_alternative_time_heading = []
latitude_from_speed_alternative_time_heading = []

longitude_from_speed_time_heading_alternative = []
latitude_from_speed_time_heading_alternative = []

longitude_from_speed_time_heading = []
latitude_from_speed_time_heading = []
i = 0
for subdir_name in all_subdirs: 
    if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
        continue 
    
    all_rides_cleaned = os.listdir(subdir_name + "/cleaned_csv/")
      
    all_files = os.listdir(subdir_name + "/cleaned_csv/") 
    bad_rides_filenames = set()
    if os.path.isfile(subdir_name + "/bad_rides_filenames"):
        bad_rides_filenames = load_object(subdir_name + "/bad_rides_filenames")
    train_rides = set()
    if os.path.isfile(subdir_name + "/train_rides"):
        train_rides= load_object(subdir_name + "/train_rides")
        
    for some_file in all_files:  
        if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or some_file in train_rides: 
            continue 
    
        file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
        longitudes = list(file_with_ride["fields_longitude"]) 
        latitudes = list(file_with_ride["fields_latitude"]) 
        longitudes, latitudes = preprocess_long_lat(longitudes, latitudes)
        longitudes, latitudes = scale_long_lat(longitudes, latitudes, 0.1, 0.1, True)

        time_no_gap = fill_gap(predicted_time[i])
        distance_no_gap = fill_gap(predicted_distance[i])
        longitudes_no_gap = fill_gap(predicted_longitude[i])
        latitudes_no_gap = fill_gap(predicted_latitude[i])
        longitudes_no_abs_no_gap = fill_gap(predicted_longitude_no_abs[i])
        latitudes_no_abs_no_gap = fill_gap(predicted_latitude_no_abs[i])
        direction_no_gap = fill_gap(predicted_direction[i])
        direction_alternative_no_gap = fill_gap(predicted_direction_alternative[i])
        speed_no_gap = fill_gap(predicted_speed[i])
        speed_alternative_no_gap = fill_gap(predicted_speed_alternative[i])
        x_speed_alternative_no_gap = fill_gap(predicted_x_speed_alternative[i]) 
        y_speed_alternative_no_gap = fill_gap(predicted_y_speed_alternative[i])
        x_speed_no_abs_alternative_no_gap = fill_gap(predicted_x_speed_no_abs_alternative[i])
        y_speed_no_abs_alternative_no_gap = fill_gap(predicted_y_speed_no_abs_alternative[i])

        x_dir = list(file_with_ride["fields_longitude"])[0] < list(file_with_ride["fields_longitude"])[-1]
        y_dir = list(file_with_ride["fields_latitude"])[0] < list(file_with_ride["fields_latitude"])[-1]

        times_cumulative.append([0])
        for time_index in range(len(time_no_gap)):
            times_cumulative[i].append(times_cumulative[i][-1] + time_no_gap[time_index])

        long_cumulative.append([longitudes[0]])
        lat_cumulative.append([latitudes[0]])
        for index_long in range(len(longitudes_no_gap)):
            long_cumulative[i].append(long_cumulative[i][-1] - longitudes_no_gap[index_long] + longitudes_no_gap[index_long] * 2 * predicted_longitude_sgn[i][index_long])
            lat_cumulative[i].append(lat_cumulative[i][-1] - latitudes_no_gap[index_long] + latitudes_no_gap[index_long] * 2 * predicted_latitude_sgn[i][index_long])

        long_no_abs_cumulative.append([longitudes[0]])
        lat_no_abs_cumulative.append([latitudes[0]])
        for index_long in range(len(longitudes_no_abs_no_gap)):
            long_no_abs_cumulative[i].append(long_no_abs_cumulative[i][-1] + longitudes_no_abs_no_gap[index_long])
            lat_no_abs_cumulative[i].append(lat_no_abs_cumulative[i][-1] + latitudes_no_abs_no_gap[index_long])
            
        x_speed_cumulative.append([longitudes[0]]) 
        y_speed_cumulative.append([latitudes[0]])   
        for index_long in range(len(x_speed_alternative_no_gap)):
            x_speed_cumulative[i].append(x_speed_cumulative[i][-1] - x_speed_alternative_no_gap[index_long] * time_no_gap[index_long] + x_speed_alternative_no_gap[index_long] * time_no_gap[index_long] * 2 * predicted_longitude_sgn[i][index_long])
            y_speed_cumulative[i].append(y_speed_cumulative[i][-1] - y_speed_alternative_no_gap[index_long] * time_no_gap[index_long] + y_speed_alternative_no_gap[index_long] * time_no_gap[index_long] * 2 * predicted_latitude_sgn[i][index_long])
            
        x_speed_no_abs_cumulative.append([longitudes[0]])    
        y_speed_no_abs_cumulative.append([latitudes[0]])   
        for index_long in range(len(x_speed_no_abs_alternative_no_gap)):
            x_speed_no_abs_cumulative[i].append(x_speed_no_abs_cumulative[i][-1] + x_speed_no_abs_alternative_no_gap[index_long])
            y_speed_no_abs_cumulative[i].append(y_speed_no_abs_cumulative[i][-1] + y_speed_no_abs_alternative_no_gap[index_long])
            
        longitude_from_distance_heading_alternative.append([longitudes[0]])  
        latitude_from_distance_heading_alternative.append([latitudes[0]])  
        cumulative_heading = 0
        for index_long in range(len(distance_no_gap)):
            cumulative_heading = direction_alternative_no_gap[index_long]
            new_long, new_lat = get_sides_from_angle(distance_no_gap[index_long], cumulative_heading)
            longitude_from_distance_heading_alternative[i].append(longitude_from_distance_heading_alternative[i][-1] + new_long)
            latitude_from_distance_heading_alternative[i].append(latitude_from_distance_heading_alternative[i][-1] + new_lat)
            
        longitude_from_distance_heading.append([longitudes[0]])  
        latitude_from_distance_heading.append([latitudes[0]])  
        for index_long in range(len(distance_no_gap)):
            new_dir = (90 - direction_no_gap[index_long] + 360) % 360 
            if not x_dir: 
                new_dir = (180 - new_dir + 360) % 360
            if not y_dir: 
                new_dir = 360 - new_dir 
            new_long, new_lat = get_sides_from_angle(distance_no_gap[index_long], new_dir)
            longitude_from_distance_heading[i].append(longitude_from_distance_heading[i][-1] + new_long)
            latitude_from_distance_heading[i].append(latitude_from_distance_heading[i][-1] + new_lat)
            
        longitude_from_speed_alternative_time_heading_alternative.append([longitudes[0]])  
        latitude_from_speed_alternative_time_heading_alternative.append([latitudes[0]])  
        cumulative_heading = 0
        for index_long in range(len(time_no_gap)):
            cumulative_heading = direction_alternative_no_gap[index_long]
            new_long, new_lat = get_sides_from_angle(speed_alternative_no_gap[index_long] * time_no_gap[index_long], cumulative_heading)
            longitude_from_speed_alternative_time_heading_alternative[i].append(longitude_from_speed_alternative_time_heading_alternative[i][-1] + new_long)
            latitude_from_speed_alternative_time_heading_alternative[i].append(latitude_from_speed_alternative_time_heading_alternative[i][-1] + new_lat)
            
        longitude_from_speed_alternative_time_heading.append([longitudes[0]])  
        latitude_from_speed_alternative_time_heading.append([latitudes[0]])  
        for index_long in range(len(time_no_gap)): 
            new_dir = (90 - direction_no_gap[index_long] + 360) % 360 
            if not x_dir: 
                new_dir = (180 - new_dir + 360) % 360
            if not y_dir: 
                new_dir = 360 - new_dir 
            new_long, new_lat = get_sides_from_angle(speed_alternative_no_gap[index_long] * time_no_gap[index_long], new_dir)
            longitude_from_speed_alternative_time_heading[i].append(longitude_from_speed_alternative_time_heading[i][-1] + new_long)
            latitude_from_speed_alternative_time_heading[i].append(latitude_from_speed_alternative_time_heading[i][-1] + new_lat) 
            
        longitude_from_speed_time_heading_alternative.append([longitudes[0]])  
        latitude_from_speed_time_heading_alternative.append([latitudes[0]])  
        cumulative_heading = 0
        for index_long in range(len(time_no_gap)):
            cumulative_heading = direction_alternative_no_gap[index_long]
            new_long, new_lat = get_sides_from_angle(speed_no_gap[index_long] / 111 / 0.1 / 3600 * time_no_gap[index_long], cumulative_heading)
            longitude_from_speed_time_heading_alternative[i].append(longitude_from_speed_time_heading_alternative[i][-1] + new_long)
            latitude_from_speed_time_heading_alternative[i].append(latitude_from_speed_time_heading_alternative[i][-1] + new_lat) 
            
        longitude_from_speed_time_heading.append([longitudes[0]])  
        latitude_from_speed_time_heading.append([latitudes[0]])   
        for index_long in range(len(time_no_gap)): 
            new_dir = (90 - direction_no_gap[index_long] + 360) % 360 
            if not x_dir: 
                new_dir = (180 - new_dir + 360) % 360
            if not y_dir: 
                new_dir = 360 - new_dir 
            new_long, new_lat = get_sides_from_angle(speed_no_gap[index_long] / 111 / 0.1 / 3600 * time_no_gap[index_long], new_dir)
            longitude_from_speed_time_heading[i].append(longitude_from_speed_time_heading[i][-1] + new_long)
            latitude_from_speed_time_heading[i].append(latitude_from_speed_time_heading[i][-1] + new_lat)  
        i += 1 
        
current_ride_index = 0
 
metric_names = ["simpson", "trapz", "simpson x", "trapz x", "simpson y", "trapz y", "euclidean", "custom", "dtw"]
metric_names = ["simpson", "trapz", "simpson x", "trapz x", "simpson y", "trapz y", "euclidean", "custom"] 
distance_predicted = dict()
distance_array = dict()
 
count_best_longit = dict()
count_best_latit = dict()
count_best_longit_latit = dict()

count_best_longit_metric = dict()
count_best_latit_metric = dict()
count_best_longit_latit_metric = dict() 
for metric_name in metric_names:
    count_best_longit_metric[metric_name] = dict()
    count_best_latit_metric[metric_name] = dict()
    count_best_longit_latit_metric[metric_name] = dict()
    if " " in metric_name:
        count_best_longit_metric[metric_name + " no time t1"] = dict()
        count_best_longit_metric[metric_name + " no time sample"] = dict()
        count_best_longit_metric[metric_name + " no time t1 no time sample"] = dict()
        count_best_latit_metric[metric_name + " no time t1"] = dict()
        count_best_latit_metric[metric_name + " no time sample"] = dict()
        count_best_latit_metric[metric_name + " no time t1 no time sample"] = dict()
        count_best_longit_latit_metric[metric_name + " no time t1"] = dict()
        count_best_longit_latit_metric[metric_name + " no time sample"] = dict()
        count_best_longit_latit_metric[metric_name + " no time t1 no time sample"] = dict()

best_match_for_metric = dict()
worst_matc_for_metric = dict()
for metric_name in metric_names:
    best_match_for_metric[metric_name] = 0
    worst_matc_for_metric[metric_name] = 100000
    if " " in metric_name:
        best_match_for_metric[metric_name + " no time t1"] = 0
        best_match_for_metric[metric_name + " no time sample"] = 0
        best_match_for_metric[metric_name + " no time t1 no time sample"] = 0
        worst_matc_for_metric[metric_name + " no time t1"] = 100000
        worst_matc_for_metric[metric_name + " no time sample"] = 100000
        worst_matc_for_metric[metric_name + " no time t1 no time sample"] = 100000
 
for subdir_name in all_subdirs: 
    if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
        continue 
    
    distance_predicted[subdir_name] = dict()
    distance_array[subdir_name] = dict()

    all_rides_cleaned = os.listdir(subdir_name + "/cleaned_csv/")
      
    all_files = os.listdir(subdir_name + "/cleaned_csv/") 
    bad_rides_filenames = set()
    if os.path.isfile(subdir_name + "/bad_rides_filenames"):
        bad_rides_filenames = load_object(subdir_name + "/bad_rides_filenames")
    train_rides = set()
    if os.path.isfile(subdir_name + "/train_rides"):
        train_rides= load_object(subdir_name + "/train_rides")
        
    for some_file in all_files:  
        if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or some_file in train_rides: 
            continue 
    
        file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
        longitudes = list(file_with_ride["fields_longitude"]) 
        latitudes = list(file_with_ride["fields_latitude"]) 
        times = transform_time(list(file_with_ride["time"]))
        longitudes, latitudes = preprocess_long_lat(longitudes, latitudes)
        longitudes, latitudes = scale_long_lat(longitudes, latitudes, 0.1, 0.1, True) 

        longitude_cumulative, latitude_cumulative = long_cumulative[current_ride_index], lat_cumulative[current_ride_index]
        longitude_no_abs_cumulative, latitude_no_abs_cumulative= long_no_abs_cumulative[current_ride_index], lat_no_abs_cumulative[current_ride_index]
        x_cumulative, y_cumulative = x_speed_cumulative[current_ride_index], y_speed_cumulative[current_ride_index]
        x_no_abs_cumulative, y_no_abs_cumulative = x_speed_no_abs_cumulative[current_ride_index], y_speed_no_abs_cumulative[current_ride_index]
        long_dist_dir_alt, lat_dist_dir_alt = longitude_from_distance_heading_alternative[current_ride_index], latitude_from_distance_heading_alternative[current_ride_index]
        long_dist_dir, lat_dist_dir = longitude_from_distance_heading[current_ride_index], latitude_from_distance_heading[current_ride_index]
        long_speed_alt_dir_alt, lat_speed_alt_dir_alt = longitude_from_speed_alternative_time_heading_alternative[current_ride_index], latitude_from_speed_alternative_time_heading_alternative[current_ride_index]
        long_speed_alt_dir, lat_speed_alt_dir = longitude_from_speed_alternative_time_heading[current_ride_index], latitude_from_speed_alternative_time_heading[current_ride_index]
        long_speed_dir_alt, lat_speed_dir_alt = longitude_from_speed_time_heading_alternative[current_ride_index], latitude_from_speed_time_heading_alternative[current_ride_index]
        long_speed_dir, lat_speed_dir = longitude_from_speed_time_heading[current_ride_index], latitude_from_speed_time_heading[current_ride_index]   
 
        #plt.plot(longitudes, latitudes, label = "original")
        #plt.plot(longitudes[0], latitudes[0], 'ro', label = "original")

        long_dict = {
            "long": longitude_cumulative,
            "long no abs": longitude_no_abs_cumulative,
            "x speed": x_cumulative,
            "x speed no abs": x_no_abs_cumulative,
            #"long dist dir alt": long_dist_dir_alt,
            "long dist dir": long_dist_dir,
            #"long speed alt dir alt": long_speed_alt_dir_alt,
            "long speed alt dir": long_speed_alt_dir, 
            #"long speed dir alt": long_speed_dir_alt,
            "long speed dir": long_speed_dir, 
        }

        lat_dict = {
            "lat": latitude_cumulative,
            "lat no abs": latitude_cumulative,
            "y speed": y_cumulative,
            "y speed no abs": y_no_abs_cumulative,
            #"lat dist dir alt": lat_dist_dir_alt,
            "lat dist dir": lat_dist_dir,
            #"lat speed alt dir alt": lat_speed_alt_dir_alt,
            "lat speed alt dir": lat_speed_alt_dir, 
            #"lat speed dir alt": lat_speed_dir_alt,
            "lat speed dir": lat_speed_dir, 
        }
 
        distance_predicted[subdir_name][some_file] = dict() 
        for metric_name in metric_names: 
            distance_predicted[subdir_name][some_file][metric_name] = dict() 
            if " " in metric_name: 
                distance_predicted[subdir_name][some_file][metric_name + " no time t1"] = dict()
                distance_predicted[subdir_name][some_file][metric_name + " no time sample"] = dict()
                distance_predicted[subdir_name][some_file][metric_name + " no time t1 no time sample"] = dict()
            for latit in lat_dict:
                for longit in long_dict: 
                    #plt.plot(long_dict[longit], lat_dict[latit], label = longit + " " + latit)
                    distance_predicted[subdir_name][some_file][metric_name][longit + "-" + latit] = compare_traj_and_sample(long_dict[longit], lat_dict[latit], times_cumulative[current_ride_index], {"long": longitudes, "lat": latitudes, "time": times}, metric_name)
                    if " " in metric_name:    
                        distance_predicted[subdir_name][some_file][metric_name + " no time t1"][longit + "-" + latit] = compare_traj_and_sample(long_dict[longit], lat_dict[latit], range(len(times_cumulative[current_ride_index])), {"long": longitudes, "lat": latitudes, "time": times}, metric_name, True, False)
                        distance_predicted[subdir_name][some_file][metric_name + " no time sample"][longit + "-" + latit] = compare_traj_and_sample(long_dict[longit], lat_dict[latit], range(len(times_cumulative[current_ride_index])), {"long": longitudes, "lat": latitudes, "time": times}, metric_name, False, True)
                        distance_predicted[subdir_name][some_file][metric_name + " no time t1 no time sample"][longit + "-" + latit] = compare_traj_and_sample(long_dict[longit], lat_dict[latit], range(len(times_cumulative[current_ride_index])), {"long": longitudes, "lat": latitudes, "time": times}, metric_name, True, True)

        if "long" not in count_best_longit:
            for latit in lat_dict:
                count_best_latit[latit] = 0 
                for metric_name in metric_names:
                    count_best_latit_metric[metric_name][latit] = 0 
                    if " " in metric_name:
                        count_best_latit_metric[metric_name + " no time t1"][latit] = 0 
                        count_best_latit_metric[metric_name + " no time sample"][latit] = 0 
                        count_best_latit_metric[metric_name + " no time t1 no time sample"][latit] = 0 
                for longit in long_dict:
                    count_best_longit[longit] = 0 
                    count_best_longit_latit[longit + "-" + latit] = 0 
                    for metric_name in metric_names:  
                        count_best_longit_metric[metric_name][longit] = 0 
                        count_best_longit_latit_metric[metric_name][longit + "-" + latit] = 0 
                        if " " in metric_name:
                            count_best_longit_metric[metric_name + " no time t1"][longit] = 0 
                            count_best_longit_metric[metric_name + " no time sample"][longit] = 0 
                            count_best_longit_metric[metric_name + " no time t1 no time sample"][longit] = 0 
                            count_best_longit_latit_metric[metric_name + " no time t1"][longit + "-" + latit] = 0 
                            count_best_longit_latit_metric[metric_name + " no time sample"][longit + "-" + latit] = 0 
                            count_best_longit_latit_metric[metric_name + " no time t1 no time sample"][longit + "-" + latit] = 0 

        #print(subdir_name, some_file) 
        for metric_name in metric_names:  
            min_for_metric = 100000
            best_name = ""
            if " " in metric_name:  
                min_for_metric_no_t1 = 100000
                best_name_no_t1 = ""
                min_for_metric_no_sample = 100000
                best_name_no_sample = ""
                min_for_metric_no_t1_no_sample = 100000
                best_name_no_t1_no_sample = ""
            for latit in lat_dict:
                for longit in long_dict:  
                    if distance_predicted[subdir_name][some_file][metric_name][longit + "-" + latit] < min_for_metric:
                        min_for_metric = distance_predicted[subdir_name][some_file][metric_name][longit + "-" + latit]
                        best_name = longit + "-" + latit
                    if " " in metric_name: 
                        if distance_predicted[subdir_name][some_file][metric_name + " no time t1"][longit + "-" + latit] < min_for_metric_no_t1:
                            min_for_metric_no_t1 = distance_predicted[subdir_name][some_file][metric_name + " no time t1"][longit + "-" + latit]
                            best_name_no_t1 = longit + "-" + latit
                        if distance_predicted[subdir_name][some_file][metric_name + " no time sample"][longit + "-" + latit] < min_for_metric_no_sample:
                            min_for_metric_no_sample = distance_predicted[subdir_name][some_file][metric_name + " no time sample"][longit + "-" + latit]
                            best_name_no_sample = longit + "-" + latit
                        if distance_predicted[subdir_name][some_file][metric_name + " no time t1 no time sample"][longit + "-" + latit] < min_for_metric_no_t1_no_sample:
                            min_for_metric_no_t1_no_sample = distance_predicted[subdir_name][some_file][metric_name + " no time t1 no time sample"][longit + "-" + latit]
                            best_name_no_t1_no_sample = longit + "-" + latit
            print(metric_name, best_name)
            if best_name != '':
                    count_best_longit_latit[best_name] += 1
                    count_best_longit[best_name.split("-")[0]] += 1
                    count_best_latit[best_name.split("-")[1]] += 1
                    count_best_longit_latit_metric[metric_name][best_name] += 1
                    count_best_longit_metric[metric_name][best_name.split("-")[0]] += 1
                    count_best_latit_metric[metric_name][best_name.split("-")[1]] += 1
                    if " " in metric_name:  
                            count_best_longit_latit_metric[metric_name + " no time t1"][best_name_no_t1] += 1
                            count_best_longit_metric[metric_name + " no time t1"][best_name_no_t1.split("-")[0]] += 1
                            count_best_latit_metric[metric_name + " no time t1"][best_name_no_t1.split("-")[1]] += 1

                            count_best_longit_latit_metric[metric_name + " no time sample"][best_name_no_sample] += 1
                            count_best_longit_metric[metric_name + " no time sample"][best_name_no_sample.split("-")[0]] += 1
                            count_best_latit_metric[metric_name + " no time sample"][best_name_no_sample.split("-")[1]] += 1

                            count_best_longit_latit_metric[metric_name + " no time t1 no time sample"][best_name_no_t1_no_sample] += 1
                            count_best_longit_metric[metric_name + " no time t1 no time sample"][best_name_no_t1_no_sample.split("-")[0]] += 1
                            count_best_latit_metric[metric_name + " no time t1 no time sample"][best_name_no_t1_no_sample.split("-")[1]] += 1
 
        #plt.legend()
        #plt.show()
  
        current_ride_index += 1

print("count_best_longit_latit")
for x in dict(sorted(count_best_longit_latit.items(), key=lambda item: item[1], reverse=True)):
    if count_best_longit_latit[x] > 0:
        print(x, count_best_longit_latit[x]) 
 
print("count_best_latit")
for x in dict(sorted(count_best_latit.items(), key=lambda item: item[1], reverse=True)):
    if count_best_latit[x] > 0:
        print(x, count_best_latit[x]) 

print("count_best_longit")
for x in dict(sorted(count_best_longit.items(), key=lambda item: item[1], reverse=True)):
    if count_best_longit[x] > 0:
        print(x, count_best_longit[x]) 

for metric_name in metric_names:   
    print(metric_name, "count_best_longit_latit")
    for x in dict(sorted(count_best_longit_latit_metric[metric_name].items(), key=lambda item: item[1], reverse=True)):
        if count_best_longit_latit_metric[metric_name][x] > 0:
            print(x, count_best_longit_latit_metric[metric_name][x]) 
    
    print(metric_name, "count_best_latit")
    for x in dict(sorted(count_best_latit_metric[metric_name].items(), key=lambda item: item[1], reverse=True)):
        if count_best_latit_metric[metric_name][x] > 0:
            print(x, count_best_latit_metric[metric_name][x]) 

    print(metric_name, "count_best_longit")
    for x in dict(sorted(count_best_longit_metric[metric_name].items(), key=lambda item: item[1], reverse=True)):
        if count_best_longit[x] > 0:
            print(x, count_best_longit_metric[metric_name][x]) 

    if " " in metric_name:  

        print(metric_name + " no time t1", "count_best_longit_latit")
        for x in dict(sorted(count_best_longit_latit_metric[metric_name + " no time t1"].items(), key=lambda item: item[1], reverse=True)):
            if count_best_longit_latit_metric[metric_name + " no time t1"][x] > 0:
                print(x, count_best_longit_latit_metric[metric_name + " no time t1"][x]) 
        
        print(metric_name + " no time t1", "count_best_latit")
        for x in dict(sorted(count_best_latit_metric[metric_name + " no time t1"].items(), key=lambda item: item[1], reverse=True)):
            if count_best_latit_metric[metric_name + " no time t1"][x] > 0:
                print(x, count_best_latit_metric[metric_name + " no time t1"][x]) 

        print(metric_name + " no time t1", "count_best_longit")
        for x in dict(sorted(count_best_longit_metric[metric_name + " no time t1"].items(), key=lambda item: item[1], reverse=True)):
            if count_best_longit[x] > 0:
                print(x, count_best_longit_metric[metric_name + " no time t1"][x]) 

        print(metric_name + " no time sample", "count_best_longit_latit")
        for x in dict(sorted(count_best_longit_latit_metric[metric_name + " no time sample"].items(), key=lambda item: item[1], reverse=True)):
            if count_best_longit_latit_metric[metric_name + " no time sample"][x] > 0:
                print(x, count_best_longit_latit_metric[metric_name + " no time sample"][x]) 
        
        print(metric_name + " no time sample", "count_best_latit")
        for x in dict(sorted(count_best_latit_metric[metric_name + " no time sample"].items(), key=lambda item: item[1], reverse=True)):
            if count_best_latit_metric[metric_name + " no time sample"][x] > 0:
                print(x, count_best_latit_metric[metric_name + " no time sample"][x]) 

        print(metric_name + " no time sample", "count_best_longit")
        for x in dict(sorted(count_best_longit_metric[metric_name + " no time sample"].items(), key=lambda item: item[1], reverse=True)):
            if count_best_longit[x] > 0:
                print(x, count_best_longit_metric[metric_name + " no time sample"][x]) 

        print(metric_name + " no time t1 no time sample", "count_best_longit_latit")
        for x in dict(sorted(count_best_longit_latit_metric[metric_name + " no time t1 no time sample"].items(), key=lambda item: item[1], reverse=True)):
            if count_best_longit_latit_metric[metric_name + " no time t1 no time sample"][x] > 0:
                print(x, count_best_longit_latit_metric[metric_name + " no time t1 no time sample"][x]) 
        
        print(metric_name + " no time t1 no time sample", "count_best_latit")
        for x in dict(sorted(count_best_latit_metric[metric_name + " no time t1 no time sample"].items(), key=lambda item: item[1], reverse=True)):
            if count_best_latit_metric[metric_name + " no time t1 no time sample"][x] > 0:
                print(x, count_best_latit_metric[metric_name + " no time t1 no time sample"][x]) 

        print(metric_name + " no time t1 no time sample", "count_best_longit")
        for x in dict(sorted(count_best_longit_metric[metric_name + " no time t1 no time sample"].items(), key=lambda item: item[1], reverse=True)):
            if count_best_longit[x] > 0:
                print(x, count_best_longit_metric[metric_name + " no time t1 no time sample"][x])  