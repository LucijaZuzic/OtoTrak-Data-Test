from utilities import *
all_subdirs = os.listdir() 
 
def read_distance(title): 
    all_x = load_object("predicted/predicted_distance")
    all_mine = dict()
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
            train_rides= load_object(subdir_name + "/train_rides")
            
        for some_file in all_files:  
            if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames or some_file in train_rides: 
                continue
        
            file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
            longitudes = list(file_with_ride["fields_longitude"]) 
            latitudes = list(file_with_ride["fields_latitude"]) 
            longitudes, latitudes = preprocess_long_lat(longitudes, latitudes)
            longitudes, latitudes = scale_long_lat(longitudes, latitudes, 0.1, 0.1, True)
            distance_int = [np.round(np.sqrt((longitudes[distance_index + 1] - longitudes[distance_index]) ** 2 + (latitudes[distance_index + 1] - latitudes[distance_index]) ** 2), 5) for distance_index in range(len(longitudes) - 1)]
            all_mine[subdir_name + "/cleaned_csv/" + some_file] = distance_int
    end_read(title, all_x, all_mine)

def read_heading_abs_alternative(title): 
    all_x = load_object("predicted/predicted_direction_abs_alternative")
    all_mine = dict()
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
            train_rides= load_object(subdir_name + "/train_rides")
            
        for some_file in all_files:  
            if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames or some_file in train_rides: 
                continue
        
            file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
            longitudes = list(file_with_ride["fields_longitude"]) 
            latitudes = list(file_with_ride["fields_latitude"]) 
            longitudes, latitudes = preprocess_long_lat(longitudes, latitudes)
            longitudes, latitudes = scale_long_lat(longitudes, latitudes, 0.1, 0.1, True)
            xdistance_int = [abs(longitudes[distance_index + 1] - longitudes[distance_index]) for distance_index in range(len(longitudes) - 1)]
            ydistance_int = [abs(latitudes[distance_index + 1] - latitudes[distance_index]) for distance_index in range(len(latitudes) - 1)]
            direction_abs_alternative_int = []
            for heading_alternative_index in range(len(longitudes) - 1):
                if xdistance_int[heading_alternative_index] != 0:
                    direction_abs_alternative_int.append((360 + np.round(np.arctan(ydistance_int[heading_alternative_index] / xdistance_int[heading_alternative_index]) / np.pi * 180, 0)) % 360)
                else:
                    if ydistance_int[heading_alternative_index] > 0:
                        direction_abs_alternative_int.append(90.0) 
                    if ydistance_int[heading_alternative_index] == 0:  
                        direction_abs_alternative_int.append("undefined")
                        last_value = "undefined"
            for heading_alternative_index in range(len(longitudes) - 1):
                if direction_abs_alternative_int[heading_alternative_index] == "undefined":
                    if last_value != "undefined":
                        direction_abs_alternative_int[heading_alternative_index] = last_value
                    else:
                        for heading_alternative_index2 in range(heading_alternative_index + 1, len(longitudes) - 1): 
                            if direction_abs_alternative_int[heading_alternative_index2] != "undefined":
                                direction_abs_alternative_int[heading_alternative_index] = direction_abs_alternative_int[heading_alternative_index2]
                                break
            all_mine[subdir_name + "/cleaned_csv/" + some_file] = direction_abs_alternative_int
    end_read(title, all_x, all_mine, True)

def read_heading_alternative(title):
    all_x = load_object("predicted/predicted_direction_alternative")
    all_mine = dict()
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
            train_rides= load_object(subdir_name + "/train_rides")
            
        for some_file in all_files:  
            if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames or some_file in train_rides: 
                continue
        
            file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
            longitudes = list(file_with_ride["fields_longitude"]) 
            latitudes = list(file_with_ride["fields_latitude"]) 
            longitudes, latitudes = preprocess_long_lat(longitudes, latitudes)
            longitudes, latitudes = scale_long_lat(longitudes, latitudes, 0.1, 0.1, True)
            xdistance_int = [longitudes[distance_index + 1] - longitudes[distance_index] for distance_index in range(len(longitudes) - 1)]
            ydistance_int = [latitudes[distance_index + 1] - latitudes[distance_index] for distance_index in range(len(latitudes) - 1)]
            direction_alternative_int = []
            for heading_alternative_index in range(len(longitudes) - 1):
                if xdistance_int[heading_alternative_index] != 0:
                    direction_alternative_int.append((360 + np.round(np.arctan(ydistance_int[heading_alternative_index] / xdistance_int[heading_alternative_index]) / np.pi * 180, 0)) % 360)
                else:
                    if ydistance_int[heading_alternative_index] > 0:
                        direction_alternative_int.append(90.0)
                    if ydistance_int[heading_alternative_index] < 0:
                        direction_alternative_int.append(270.0)
                    if ydistance_int[heading_alternative_index] == 0:  
                        direction_alternative_int.append("undefined")
                        last_value = "undefined"
            for heading_alternative_index in range(len(longitudes) - 1):
                if direction_alternative_int[heading_alternative_index] == "undefined":
                    if last_value != "undefined":
                        direction_alternative_int[heading_alternative_index] = last_value
                    else:
                        for heading_alternative_index2 in range(heading_alternative_index + 1, len(longitudes) - 1): 
                            if direction_alternative_int[heading_alternative_index2] != "undefined":
                                direction_alternative_int[heading_alternative_index] = direction_alternative_int[heading_alternative_index2]
                                break
            all_mine[subdir_name + "/cleaned_csv/" + some_file] = direction_alternative_int
    end_read(title, all_x, all_mine, True)

def read_heading(title): 
    all_x = load_object("predicted/predicted_direction")
    all_mine = dict()
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
            train_rides= load_object(subdir_name + "/train_rides")
            
        for some_file in all_files:  
            if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames or some_file in train_rides: 
                continue
        
            file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
            directions = list(file_with_ride["fields_direction"]) 
            direction_int = [np.round(direction, 0) for direction in directions]
            all_mine[subdir_name + "/cleaned_csv/" + some_file] = direction_int
    end_read(title, all_x, all_mine, True)

def read_latitude(title): 
    all_x = load_object("predicted/predicted_latitude")
    all_mine = dict()
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
            train_rides= load_object(subdir_name + "/train_rides")
            
        for some_file in all_files:  
            if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames or some_file in train_rides: 
                continue
        
            file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
            longitudes = list(file_with_ride["fields_longitude"]) 
            latitudes = list(file_with_ride["fields_latitude"]) 
            longitudes, latitudes = preprocess_long_lat(longitudes, latitudes)
            longitudes, latitudes = scale_long_lat(longitudes, latitudes, 0.1, 0.1, True)
            latitude_int = [np.round(abs(latitudes[latitude_index + 1] - latitudes[latitude_index]), 10) for latitude_index in range(len(latitudes) - 1)]
            all_mine[subdir_name + "/cleaned_csv/" + some_file] = latitude_int
    end_read(title, all_x, all_mine)

def read_latitude_no_abs(title): 
    all_x = load_object("predicted/predicted_latitude_no_abs")
    all_mine = dict()
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
            train_rides= load_object(subdir_name + "/train_rides")
            
        for some_file in all_files:  
            if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames or some_file in train_rides: 
                continue
        
            file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
            longitudes = list(file_with_ride["fields_longitude"]) 
            latitudes = list(file_with_ride["fields_latitude"]) 
            longitudes, latitudes = preprocess_long_lat(longitudes, latitudes)
            longitudes, latitudes = scale_long_lat(longitudes, latitudes, 0.1, 0.1, True)
            latitude_int = [np.round(latitudes[latitude_index + 1] - latitudes[latitude_index], 10) for latitude_index in range(len(latitudes) - 1)]
            all_mine[subdir_name + "/cleaned_csv/" + some_file] = latitude_int
    end_read(title, all_x, all_mine)

def read_latitude_sgn(title): 
    all_x = load_object("predicted/predicted_latitude_sgn")
    all_mine = dict()
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
            train_rides= load_object(subdir_name + "/train_rides")
            
        for some_file in all_files:  
            if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames or some_file in train_rides: 
                continue
        
            file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
            longitudes = list(file_with_ride["fields_longitude"]) 
            latitudes = list(file_with_ride["fields_latitude"]) 
            longitudes, latitudes = preprocess_long_lat(longitudes, latitudes)
            longitudes, latitudes = scale_long_lat(longitudes, latitudes, 0.1, 0.1, True)
            latitude_int = [latitudes[latitude_index + 1] > latitudes[latitude_index] for latitude_index in range(len(latitudes) - 1)]
            all_mine[subdir_name + "/cleaned_csv/" + some_file] = latitude_int
    end_read(title, all_x, all_mine)

def read_longitude(title): 
    all_x = load_object("predicted/predicted_longitude")
    all_mine = dict()
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
            train_rides= load_object(subdir_name + "/train_rides")
            
        for some_file in all_files:  
            if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames or some_file in train_rides: 
                continue
        
            file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
            longitudes = list(file_with_ride["fields_longitude"]) 
            latitudes = list(file_with_ride["fields_latitude"]) 
            longitudes, latitudes = preprocess_long_lat(longitudes, latitudes)
            longitudes, latitudes = scale_long_lat(longitudes, latitudes, 0.1, 0.1, True)
            longitude_int = [np.round(abs(longitudes[longitude_index + 1] - longitudes[longitude_index]), 10) for longitude_index in range(len(longitudes) - 1)]
            all_mine[subdir_name + "/cleaned_csv/" + some_file] = longitude_int
    end_read(title, all_x, all_mine)

def read_longitude_no_abs(title): 
    all_x = load_object("predicted/predicted_longitude_no_abs")
    all_mine = dict()
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
            train_rides= load_object(subdir_name + "/train_rides")
            
        for some_file in all_files:  
            if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames or some_file in train_rides: 
                continue
        
            file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
            longitudes = list(file_with_ride["fields_longitude"]) 
            latitudes = list(file_with_ride["fields_latitude"]) 
            longitudes, latitudes = preprocess_long_lat(longitudes, latitudes)
            longitudes, latitudes = scale_long_lat(longitudes, latitudes, 0.1, 0.1, True)
            longitude_int = [np.round(longitudes[longitude_index + 1] - longitudes[longitude_index], 10) for longitude_index in range(len(longitudes) - 1)]
            all_mine[subdir_name + "/cleaned_csv/" + some_file] = longitude_int
    end_read(title, all_x, all_mine)

def read_longitude_sgn(title): 
    all_x = load_object("predicted/predicted_longitude_sgn")
    all_mine = dict()
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
            train_rides= load_object(subdir_name + "/train_rides")
            
        for some_file in all_files:  
            if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames or some_file in train_rides: 
                continue
        
            file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
            longitudes = list(file_with_ride["fields_longitude"]) 
            latitudes = list(file_with_ride["fields_latitude"]) 
            longitudes, latitudes = preprocess_long_lat(longitudes, latitudes)
            longitudes, latitudes = scale_long_lat(longitudes, latitudes, 0.1, 0.1, True)
            longitude_int = [longitudes[longitude_index + 1] > longitudes[longitude_index] for longitude_index in range(len(longitudes) - 1)] 
            all_mine[subdir_name + "/cleaned_csv/" + some_file] = longitude_int
    end_read(title, all_x, all_mine)

def read_speed_alternative(title): 
    all_x = load_object("predicted/predicted_speed_alternative")
    all_mine = dict()
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
            train_rides= load_object(subdir_name + "/train_rides")
            
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
            distance_int = [np.sqrt((longitudes[distance_index + 1] - longitudes[distance_index]) ** 2 + (latitudes[distance_index + 1] - latitudes[distance_index]) ** 2) for distance_index in range(len(longitudes) - 1)]
            speed_alternative_int = [np.round(distance_int[speed_alternative_index] / times_delays[speed_alternative_index], 5) for speed_alternative_index in range(len(times_delays))]
            all_mine[subdir_name + "/cleaned_csv/" + some_file] = speed_alternative_int
    end_read(title, all_x, all_mine)

def read_speed(title): 
    all_x = load_object("predicted/predicted_speed")
    all_mine = dict()
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
            train_rides= load_object(subdir_name + "/train_rides")
            
        for some_file in all_files:  
            if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames or some_file in train_rides: 
                continue
        
            file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
            speeds = list(file_with_ride["fields_speed"]) 
            speed_int = [np.round(speed, 0) for speed in speeds] 
            all_mine[subdir_name + "/cleaned_csv/" + some_file] = speed_int
    end_read(title, all_x, all_mine)

def read_time(title): 
    all_x = load_object("predicted/predicted_time")
    all_mine = dict()
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
            train_rides= load_object(subdir_name + "/train_rides")
            
        for some_file in all_files:  
            if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames or some_file in train_rides: 
                continue
        
            file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
            times = list(file_with_ride["time"])
            times_processed = [process_time(time_new) for time_new in times] 
            time_int = [np.round(times_processed[time_index + 1] - times_processed[time_index], 3) for time_index in range(len(times_processed) - 1)] 
            for time_index in range(len(time_int)):
                    if time_int[time_index] == 0: 
                        time_int[time_index] = 10 ** -20 
            all_mine[subdir_name + "/cleaned_csv/" + some_file] = time_int
    end_read(title, all_x, all_mine)
 
def read_x_speed(title): 
    all_x = load_object("predicted/predicted_x_speed_alternative")
    all_mine = dict()
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
            train_rides= load_object(subdir_name + "/train_rides")
            
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
            distance_int = [abs(longitudes[distance_index + 1] - longitudes[distance_index]) for distance_index in range(len(longitudes) - 1)]
            x_speed_alternative_int = [np.round(distance_int[x_speed_alternative_index] / times_delays[x_speed_alternative_index], 5) for x_speed_alternative_index in range(len(times_delays))]
            all_mine[subdir_name + "/cleaned_csv/" + some_file] = x_speed_alternative_int
    end_read(title, all_x, all_mine)
 
def read_x_speed_no_abs(title): 
    all_x = load_object("predicted/predicted_x_speed_no_abs_alternative")
    all_mine = dict()
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
            train_rides= load_object(subdir_name + "/train_rides")
            
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
            distance_int = [longitudes[distance_index + 1] - longitudes[distance_index] for distance_index in range(len(longitudes) - 1)]
            x_speed_no_abs_alternative_int = [np.round(distance_int[x_speed_no_abs_alternative_index] / times_delays[x_speed_no_abs_alternative_index], 5) for x_speed_no_abs_alternative_index in range(len(times_delays))]
            all_mine[subdir_name + "/cleaned_csv/" + some_file] = x_speed_no_abs_alternative_int
    end_read(title, all_x, all_mine)

def read_y_speed(title): 
    all_x = load_object("predicted/predicted_y_speed_alternative")
    all_mine = dict()
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
            train_rides= load_object(subdir_name + "/train_rides")
            
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
            distance_int = [abs(latitudes[distance_index + 1] - latitudes[distance_index]) for distance_index in range(len(latitudes) - 1)]
            y_speed_alternative_int = [np.round(distance_int[y_speed_alternative_index] / times_delays[y_speed_alternative_index], 5) for y_speed_alternative_index in range(len(times_delays))]
            all_mine[subdir_name + "/cleaned_csv/" + some_file] = y_speed_alternative_int
    end_read(title, all_x, all_mine)

def read_y_speed_no_abs(title):
    all_x = load_object("predicted/predicted_y_speed_no_abs_alternative")
    all_mine = dict()
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
            train_rides= load_object(subdir_name + "/train_rides")
            
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
            distance_int = [latitudes[distance_index + 1] - latitudes[distance_index] for distance_index in range(len(latitudes) - 1)]
            y_speed_no_abs_alternative_int = [np.round(distance_int[y_speed_no_abs_alternative_index] / times_delays[y_speed_no_abs_alternative_index], 5) for y_speed_no_abs_alternative_index in range(len(times_delays))]
            all_mine[subdir_name + "/cleaned_csv/" + some_file] = y_speed_no_abs_alternative_int
    end_read(title, all_x, all_mine)

def format_e(n):
    if n >= 10 ** -2 or n == 0:
        return "$" + str(np.round(n, 2)).replace(".0", "") + "$ &"
    a = '%.2E' % n
    return "$" + str(str(a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]) + "}$ &").replace("E-0", "*10^{-").replace("E+0", "*10^{")

def end_read(title, all_x, all_mine, isangle = False):
    total_match_score = 0
    total_guesses = 0 
    total_guesses_no_empty = 0
    delta_series_total = []  
    data_series_total = []  
    minval = 10000000
    maxval = -10000000 
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
            train_rides= load_object(subdir_name + "/train_rides")
            
        for some_file in all_files:  
            if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames or some_file in train_rides: 
                continue

            x = all_x[subdir_name + "/cleaned_csv/" + some_file]
            other = all_mine[subdir_name + "/cleaned_csv/" + some_file]
            minval = min(minval, min(fill_gap(x)))
            maxval = max(maxval, max(fill_gap(x))) 
            n = len(x)
            match_score = 0 
            no_empty = 0
            delta_series = [] 
            for i in range(2, n):
                if x[i] == other[i]:
                    match_score += 1
                if x[i] != "undefined":
                    no_empty += 1
                    delta_x = abs(other[i] - x[i])
                    if isangle:
                        if delta_x > 180:
                            delta_x = 360 - delta_x
                    delta_series.append(delta_x)
                    delta_series_total.append(delta_x)
                    data_series_total.append(x[i]) 

    total_guesses += n - 2
    total_guesses_no_empty += no_empty
    total_match_score += match_score  
    no_extension = title.replace(".png", "").replace("markov_hist/", "").capitalize()
    plt.rcParams.update({'font.size': 22})
    plt.figure(figsize=(25, 10))
    print(no_extension)
    #print(minval, maxval, (total_guesses - total_guesses_no_empty) / total_guesses, total_match_score / total_guesses, total_match_score / total_guesses_no_empty, min(delta_series_total), np.quantile(delta_series_total, 0.25), np.quantile(delta_series_total, 0.5), np.quantile(delta_series_total, 0.75), max(delta_series_total), np.average(delta_series_total), np.std(delta_series_total), np.var(delta_series_total))
    #print(np.quantile(delta_series_total, 0.80), np.quantile(delta_series_total, 0.85), np.quantile(delta_series_total, 0.90), np.quantile(delta_series_total, 0.95))
    print(format_e(minval), format_e(maxval), "$" + str(np.round(total_match_score / total_guesses * 100, 2)) + "\\%$ & ", format_e(np.average(delta_series_total)), format_e(np.std(delta_series_total)), format_e(np.var(delta_series_total)), format_e(max(delta_series_total))) 
    print(format_e(np.quantile(delta_series_total, 0.25)), format_e(np.quantile(delta_series_total, 0.50)), format_e(np.quantile(delta_series_total, 0.75)), format_e(np.quantile(delta_series_total, 0.80)),format_e(np.quantile(delta_series_total, 0.85)), format_e(np.quantile(delta_series_total, 0.90)), format_e(np.quantile(delta_series_total, 0.95)))
    plt.subplot(1, 2, 1)
    plt.title(no_extension + " data")  
    plt.hist(data_series_total)
    plt.xlabel("Data")
    plt.ylabel("Number of occurences")
    plt.subplot(1, 2, 2) 
    plt.title(no_extension + " delta")  
    plt.hist(delta_series_total)
    plt.xlabel("Delta")
    plt.ylabel("Number of occurences")
    plt.savefig(title, bbox_inches = "tight")
    plt.close()

if not os.path.isdir("markov_hist"):
    os.makedirs("markov_hist")

read_distance("markov_hist/distance.png")
read_heading("markov_hist/direction.png")
read_heading_abs_alternative("markov_hist/direction abs alt.png")
read_heading_alternative("markov_hist/direction alt.png")
read_latitude("markov_hist/latitude.png")
read_latitude_no_abs("markov_hist/latitude no abs.png")
read_latitude_sgn("markov_hist/latitude sgn.png")
read_longitude("markov_hist/longitude.png")
read_longitude_no_abs("markov_hist/longitude no abs.png")
read_longitude_sgn("markov_hist/longitude sgn.png")
read_time("markov_hist/time.png")
read_speed("markov_hist/speed.png")
read_speed_alternative("markov_hist/speed alt.png")
read_x_speed("markov_hist/x speed.png")
read_x_speed_no_abs("markov_hist/x speed no abs.png")
read_y_speed("markov_hist/y speed.png")
read_y_speed_no_abs("markov_hist/y speed no abs.png")