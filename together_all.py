import os
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime  

def process_time(time_as_str):
    time_as_str = time_as_str.split(".")[0]
    return datetime.strptime(time_as_str, '%Y-%m-%d %H:%M:%S')

def process_time(time_as_str):
    time_as_str = time_as_str.split(".")[0]
    return datetime.strptime(time_as_str, '%Y-%m-%d %H:%M:%S')
 
def save_object(file_name, std1):       
    with open(file_name, 'wb') as file_object:
        pickle.dump(std1, file_object) 
        file_object.close()

def load_object(file_name): 
    with open(file_name, 'rb') as file_object:
        data = pickle.load(file_object) 
        file_object.close()
        return data

def preprocess_long_lat(long_list, lat_list):
    x_dir = long_list[0] < long_list[-1]
    y_dir = lat_list[0] < lat_list[-1]
 
    long_list2 = [x - min(long_list) for x in long_list]
    lat_list2 = [y - min(lat_list) for y in lat_list]
    if x_dir == False: 
        long_list2 = [max(long_list2) - x for x in long_list2]
    if y_dir == False:
        lat_list2 = [max(lat_list2) - y for y in lat_list2]

    return long_list2, lat_list2    
      
def scale_long_lat(long_list, lat_list, xmax = 0, ymax = 0, keep_aspect_ratio = True):
    minx = np.min(long_list)
    maxx = np.max(long_list)
    miny = np.min(lat_list)
    maxy = np.max(lat_list)
    x_diff = maxx - minx
    if x_diff == 0:
        x_diff = 1
    y_diff = maxy - miny 
    if y_diff == 0:
        y_diff = 1
    if xmax == 0 and ymax == 0 and keep_aspect_ratio:
        xmax = max(x_diff, y_diff)
        ymax = max(x_diff, y_diff)
    if xmax == 0 and ymax == 0 and not keep_aspect_ratio:
        xmax = x_diff
        ymax = y_diff
    if xmax == 0 and ymax != 0 and keep_aspect_ratio:
        xmax = ymax 
    if xmax == 0 and ymax != 0 and not keep_aspect_ratio:
        xmax = x_diff 
    if xmax != 0 and ymax == 0 and keep_aspect_ratio:
        ymax = xmax 
    if xmax != 0 and ymax == 0 and not keep_aspect_ratio:
        ymax = y_diff 
    if xmax != 0 and ymax != 0 and keep_aspect_ratio and xmax != ymax:
        ymax = xmax # ymax = xmax or xmax = ymax or keep_aspect_ratio = False or return
    long_list2 = [(x - min(long_list)) / xmax for x in long_list]
    lat_list2 = [(y - min(lat_list)) / ymax for y in lat_list]
    return long_list2, lat_list2  
     
predicted_time = load_object("predicted_time") 
probability_of_time = load_object("probability_of_time") 
probability_of_time_in_next_step = load_object("probability_of_time_in_next_step") 
probability_of_time_in_next_next_step = load_object("probability_of_time_in_next_next_step") 
print("probability_of_time", min(probability_of_time.keys()), max(probability_of_time.keys()))

predicted_distance = load_object("predicted_distance") 
probability_of_distance = load_object("probability_of_distance") 
probability_of_distance_in_next_step = load_object("probability_of_distance_in_next_step") 
probability_of_distance_in_next_next_step = load_object("probability_of_distance_in_next_next_step") 
print("probability_of_distance", min(probability_of_distance.keys()), max(probability_of_distance.keys()))

predicted_longitude = load_object("predicted_longitude") 
probability_of_longitude = load_object("probability_of_longitude") 
probability_of_longitude_in_next_step = load_object("probability_of_longitude_in_next_step") 
probability_of_longitude_in_next_next_step = load_object("probability_of_longitude_in_next_next_step") 
print("probability_of_longitude", min(probability_of_longitude.keys()), max(probability_of_longitude.keys()))

predicted_latitude = load_object("predicted_latitude") 
probability_of_latitude = load_object("probability_of_latitude") 
probability_of_latitude_in_next_step = load_object("probability_of_latitude_in_next_step") 
probability_of_latitude_in_next_next_step = load_object("probability_of_latitude_in_next_next_step") 
print("probability_of_latitude", min(probability_of_latitude.keys()), max(probability_of_latitude.keys()))

predicted_longitude_sgn = load_object("predicted_longitude_sgn") 
probability_of_longitude_sgn = load_object("probability_of_longitude_sgn") 
probability_of_longitude_sgn_in_next_step = load_object("probability_of_longitude_sgn_in_next_step") 
probability_of_longitude_sgn_in_next_next_step = load_object("probability_of_longitude_sgn_in_next_next_step") 
print("probability_of_longitude_sgn", min(probability_of_longitude_sgn.keys()), max(probability_of_longitude_sgn.keys()))

predicted_latitude_sgn = load_object("predicted_latitude_sgn") 
probability_of_latitude_sgn = load_object("probability_of_latitude_sgn") 
probability_of_latitude_sgn_in_next_step = load_object("probability_of_latitude_sgn_in_next_step") 
probability_of_latitude_sgn_in_next_next_step = load_object("probability_of_latitude_sgn_in_next_next_step") 
print("probability_of_latitude_sgn", min(probability_of_latitude_sgn.keys()), max(probability_of_latitude_sgn.keys()))

predicted_longitude_no_abs = load_object("predicted_longitude_no_abs") 
probability_of_longitude_no_abs = load_object("probability_of_longitude_no_abs") 
probability_of_longitude_no_abs_in_next_step = load_object("probability_of_longitude_no_abs_in_next_step") 
probability_of_longitude_no_abs_in_next_next_step = load_object("probability_of_longitude_no_abs_in_next_next_step") 
print("probability_of_longitude_no_abs", min(probability_of_longitude_no_abs.keys()), max(probability_of_longitude_no_abs.keys()))

predicted_latitude_no_abs = load_object("predicted_latitude_no_abs") 
probability_of_latitude_no_abs = load_object("probability_of_latitude_no_abs") 
probability_of_latitude_no_abs_in_next_step = load_object("probability_of_latitude_no_abs_in_next_step") 
probability_of_latitude_no_abs_in_next_next_step = load_object("probability_of_latitude_no_abs_in_next_next_step") 
print("probability_of_latitude_no_abs", min(probability_of_latitude_no_abs.keys()), max(probability_of_latitude_no_abs.keys()))

predicted_direction = load_object("predicted_direction") 
probability_of_direction = load_object("probability_of_direction") 
probability_of_direction_in_next_step = load_object("probability_of_direction_in_next_step") 
probability_of_direction_in_next_next_step = load_object("probability_of_direction_in_next_next_step") 
print("probability_of_direction", min(probability_of_direction.keys()), max(probability_of_direction.keys()))

predicted_direction_alternative = load_object("predicted_direction_alternative") 
probability_of_direction_alternative = load_object("probability_of_direction_alternative") 
probability_of_direction_alternative_in_next_step = load_object("probability_of_direction_alternative_in_next_step") 
probability_of_direction_alternative_in_next_next_step = load_object("probability_of_direction_alternative_in_next_next_step") 
print("probability_of_direction_alternative", min(probability_of_direction_alternative.keys()), max(probability_of_direction_alternative.keys()))
 
predicted_speed = load_object("predicted_speed") 
probability_of_speed = load_object("probability_of_speed") 
probability_of_speed_in_next_step = load_object("probability_of_speed_in_next_step") 
probability_of_speed_in_next_next_step = load_object("probability_of_speed_in_next_next_step") 
print("probability_of_speed", min(probability_of_speed.keys()), max(probability_of_speed.keys()))

predicted_speed_alternative = load_object("predicted_speed_alternative") 
probability_of_speed_alternative = load_object("probability_of_speed_alternative") 
probability_of_speed_alternative_in_next_step = load_object("probability_of_speed_alternative_in_next_step") 
probability_of_speed_alternative_in_next_next_step = load_object("probability_of_speed_alternative_in_next_next_step") 
print("probability_of_speed_alternative", min(probability_of_speed_alternative.keys()), max(probability_of_speed_alternative.keys()))

predicted_x_speed_alternative = load_object("predicted_x_speed_alternative") 
probability_of_x_speed_alternative = load_object("probability_of_x_speed_alternative") 
probability_of_x_speed_alternative_in_next_step = load_object("probability_of_x_speed_alternative_in_next_step") 
probability_of_x_speed_alternative_in_next_next_step = load_object("probability_of_x_speed_alternative_in_next_next_step") 
print("probability_of_x_speed_alternative", min(probability_of_x_speed_alternative.keys()), max(probability_of_x_speed_alternative.keys()))

predicted_y_speed_alternative = load_object("predicted_y_speed_alternative") 
probability_of_y_speed_alternative = load_object("probability_of_y_speed_alternative") 
probability_of_y_speed_alternative_in_next_step = load_object("probability_of_y_speed_alternative_in_next_step") 
probability_of_y_speed_alternative_in_next_next_step = load_object("probability_of_y_speed_alternative_in_next_next_step") 
print("probability_of_y_speed_alternative", min(probability_of_y_speed_alternative.keys()), max(probability_of_y_speed_alternative.keys()))

predicted_x_speed_no_abs_alternative = load_object("predicted_x_speed_no_abs_alternative") 
probability_of_x_speed_no_abs_alternative = load_object("probability_of_x_speed_no_abs_alternative") 
probability_of_x_speed_no_abs_alternative_in_next_step = load_object("probability_of_x_speed_no_abs_alternative_in_next_step") 
probability_of_x_speed_no_abs_alternative_in_next_next_step = load_object("probability_of_x_speed_no_abs_alternative_in_next_next_step") 
print("probability_of_x_speed_no_abs_alternative", min(probability_of_x_speed_no_abs_alternative.keys()), max(probability_of_x_speed_no_abs_alternative.keys()))

predicted_y_speed_no_abs_alternative = load_object("predicted_y_speed_no_abs_alternative") 
probability_of_y_speed_no_abs_alternative = load_object("probability_of_y_speed_no_abs_alternative") 
probability_of_y_speed_no_abs_alternative_in_next_step = load_object("probability_of_y_speed_no_abs_alternative_in_next_step") 
probability_of_y_speed_no_abs_alternative_in_next_next_step = load_object("probability_of_y_speed_no_abs_alternative_in_next_next_step") 
print("probability_of_y_speed_no_abs_alternative", min(probability_of_y_speed_no_abs_alternative.keys()), max(probability_of_y_speed_no_abs_alternative.keys()))

all_subdirs = os.listdir() 

path_lengths = []

#pair 1: longitudes (no abs) + latitudes (no abs) 4
#pair 2: longitudes (no abs) + y_speed (no abs) * time 4
#pair 3: x_speed (no abs) * time + latitudes (no abs) 4
#pair 4: x_speed (no abs) * time + y_speed (no abs) * time 4
#pair 5: distance + heading (heading_alternative) 2
#pair 6: speed (speed_alternative) * time + heading (heading_alternative) 4

def get_sides_from_angle(longest, angle):
    return longest * np.cos(angle / 180 * np.pi), longest * np.sin(angle / 180 * np.pi)

def fill_gap(list_gap):
    list_no_gap = []
    last_val = 0
    for index_num in range(len(list_gap)):
        if list_gap[index_num] != -1:
            last_val = list_gap[index_num]
        list_no_gap.append(last_val)  
    return list_no_gap

time_no_gap = fill_gap(predicted_time)
distance_no_gap = fill_gap(predicted_distance)
longitudes_no_gap = fill_gap(predicted_longitude)
latitudes_no_gap = fill_gap(predicted_latitude)
longitudes_no_abs_no_gap = fill_gap(predicted_longitude_no_abs)
latitudes_no_abs_no_gap = fill_gap(predicted_latitude_no_abs)
direction_no_gap = fill_gap(predicted_direction)
direction_alternative_no_gap = fill_gap(predicted_direction_alternative)
speed_no_gap = fill_gap(predicted_speed)
speed_alternative_no_gap = fill_gap(predicted_speed_alternative)
x_speed_alternative_no_gap = fill_gap(predicted_x_speed_alternative) 
y_speed_alternative_no_gap = fill_gap(predicted_y_speed_alternative)
x_speed_no_abs_alternative_no_gap = fill_gap(predicted_x_speed_no_abs_alternative)
y_speed_no_abs_alternative_no_gap = fill_gap(predicted_y_speed_no_abs_alternative)

long_cumulative = [0]
lat_cumulative = [0]
for index_long in range(len(longitudes_no_gap)):
    long_cumulative.append(long_cumulative[-1] - longitudes_no_gap[index_long] + longitudes_no_gap[index_long] * 2 * predicted_longitude_sgn[index_long])
    lat_cumulative.append(lat_cumulative[-1] - latitudes_no_gap[index_long] + latitudes_no_gap[index_long] * 2 * predicted_latitude_sgn[index_long])
print(len(long_cumulative), len(lat_cumulative))

long_no_abs_cumulative = [0]
lat_no_abs_cumulative = [0]
for index_long in range(len(longitudes_no_abs_no_gap)):
    long_no_abs_cumulative.append(long_no_abs_cumulative[-1] + longitudes_no_abs_no_gap[index_long])
    lat_no_abs_cumulative.append(lat_no_abs_cumulative[-1] + latitudes_no_abs_no_gap[index_long])
print(len(long_no_abs_cumulative), len(lat_no_abs_cumulative)) 
    
x_speed_cumulative = [0]   
y_speed_cumulative = [0]   
for index_long in range(len(x_speed_alternative_no_gap)):
    x_speed_cumulative.append(x_speed_cumulative[-1] - x_speed_alternative_no_gap[index_long] * time_no_gap[index_long] + x_speed_alternative_no_gap[index_long] * time_no_gap[index_long] * 2 * predicted_longitude_sgn[index_long])
    y_speed_cumulative.append(y_speed_cumulative[-1] - y_speed_alternative_no_gap[index_long] * time_no_gap[index_long] + y_speed_alternative_no_gap[index_long] * time_no_gap[index_long] * 2 * predicted_longitude_sgn[index_long])
print(len(x_speed_cumulative), len(y_speed_cumulative)) 
     
x_speed_no_abs_cumulative = [0]   
y_speed_no_abs_cumulative = [0]   
for index_long in range(len(x_speed_no_abs_alternative_no_gap)):
    x_speed_no_abs_cumulative.append(x_speed_no_abs_cumulative[-1] + x_speed_no_abs_alternative_no_gap[index_long])
    y_speed_no_abs_cumulative.append(y_speed_no_abs_cumulative[-1] + y_speed_no_abs_alternative_no_gap[index_long])
print(len(x_speed_no_abs_cumulative), len(y_speed_no_abs_cumulative)) 
     
longitude_from_distance_heading_alternative = [0]
latitude_from_distance_heading_alternative = [0]
for index_long in range(len(distance_no_gap)):
    new_long, new_lat = get_sides_from_angle(distance_no_gap[index_long], direction_alternative_no_gap[index_long])
    longitude_from_distance_heading_alternative.append(longitude_from_distance_heading_alternative[-1] + new_long)
    latitude_from_distance_heading_alternative.append(latitude_from_distance_heading_alternative[-1] + new_lat)
print(len(longitude_from_distance_heading_alternative), len(latitude_from_distance_heading_alternative)) 
     
longitude_from_distance_heading = [0]
latitude_from_distance_heading = [0]
for index_long in range(len(distance_no_gap)):
    new_long, new_lat = get_sides_from_angle(distance_no_gap[index_long], (90 - direction_no_gap[index_long] + 360) % 360)
    longitude_from_distance_heading.append(longitude_from_distance_heading[-1] + new_long)
    latitude_from_distance_heading.append(latitude_from_distance_heading[-1] + new_lat)
print(len(longitude_from_distance_heading), len(latitude_from_distance_heading)) 
     
longitude_from_speed_alternative_time_heading_alternative = [0]
latitude_from_speed_alternative_time_heading_alternative = [0]
for index_long in range(len(time_no_gap)):
    new_long, new_lat = get_sides_from_angle(speed_alternative_no_gap[index_long] * time_no_gap[index_long], direction_alternative_no_gap[index_long])
    longitude_from_speed_alternative_time_heading_alternative.append(longitude_from_speed_alternative_time_heading_alternative[-1] + new_long)
    latitude_from_speed_alternative_time_heading_alternative.append(latitude_from_speed_alternative_time_heading_alternative[-1] + new_lat)
print(len(longitude_from_speed_alternative_time_heading_alternative), len(latitude_from_speed_alternative_time_heading_alternative)) 
    
longitude_from_speed_alternative_time_heading = [0]
latitude_from_speed_alternative_time_heading = [0]
for index_long in range(len(time_no_gap)):
    new_long, new_lat = get_sides_from_angle(speed_alternative_no_gap[index_long] * time_no_gap[index_long], (90 - direction_no_gap[index_long] + 360) % 360)
    longitude_from_speed_alternative_time_heading.append(longitude_from_speed_alternative_time_heading[-1] + new_long)
    latitude_from_speed_alternative_time_heading.append(latitude_from_speed_alternative_time_heading[-1] + new_lat)
print(len(longitude_from_speed_alternative_time_heading), len(latitude_from_speed_alternative_time_heading)) 
      
longitude_from_speed_time_heading_alternative = [0]
latitude_from_speed_time_heading_alternative = [0]
for index_long in range(len(time_no_gap)):
    new_long, new_lat = get_sides_from_angle(speed_no_gap[index_long] / 111 / 0.1 / 3600 * time_no_gap[index_long], direction_alternative_no_gap[index_long])
    longitude_from_speed_time_heading_alternative.append(longitude_from_speed_time_heading_alternative[-1] + new_long)
    latitude_from_speed_time_heading_alternative.append(latitude_from_speed_time_heading_alternative[-1] + new_lat)
print(len(longitude_from_speed_time_heading_alternative), len(latitude_from_speed_time_heading_alternative)) 
    
longitude_from_speed_time_heading = [0]
latitude_from_speed_time_heading = [0]
for index_long in range(len(time_no_gap)):
    new_long, new_lat = get_sides_from_angle(speed_no_gap[index_long] / 111 / 0.1 / 3600 * time_no_gap[index_long], (90 - direction_no_gap[index_long] + 360) % 360)
    longitude_from_speed_time_heading.append(longitude_from_speed_time_heading[-1] + new_long)
    latitude_from_speed_time_heading.append(latitude_from_speed_time_heading[-1] + new_lat)
print(len(longitude_from_speed_time_heading), len(latitude_from_speed_time_heading)) 
        
'''
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
        times = list(file_with_ride["time"])
        path_lengths.append(len(times))
        times_processed = [process_time(time_new) for time_new in times]  
'''
