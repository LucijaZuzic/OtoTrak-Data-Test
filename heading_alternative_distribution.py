import os
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    
all_subdirs = os.listdir() 

if not os.path.isdir("num_occurences"):
    os.makedirs("num_occurences")
if not os.path.isdir("probability"):
    os.makedirs("probability")
if not os.path.isdir("predicted"):
    os.makedirs("predicted")

if not os.path.isfile("num_occurences/num_occurences_of_direction_alternative"):
    num_occurences_of_direction_alternative = dict()
    num_occurences_of_direction_alternative_diff = dict()
    num_occurences_of_direction_alternative_in_next_step = dict()
    num_occurences_of_direction_alternative_in_next_next_step = dict()

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
                last_value = direction_alternative_int[heading_alternative_index]
 
            for direction_alternative in direction_alternative_int:
                if direction_alternative not in num_occurences_of_direction_alternative:
                    num_occurences_of_direction_alternative[direction_alternative] = 0
                num_occurences_of_direction_alternative[direction_alternative] += 1

            for direction_alternative_index in range(len(direction_alternative_int) - 1):
                direction_alternative = direction_alternative_int[direction_alternative_index]
                next_direction_alternative = direction_alternative_int[direction_alternative_index + 1]
                direction_alternative_diff = abs(next_direction_alternative - direction_alternative)
                if direction_alternative_diff > 180:
                    direction_alternative_diff = 360 - direction_alternative_diff
                if direction_alternative_diff not in num_occurences_of_direction_alternative_diff: 
                    num_occurences_of_direction_alternative_diff[direction_alternative_diff] = 0
                num_occurences_of_direction_alternative_diff[direction_alternative_diff] += 1
                if direction_alternative not in num_occurences_of_direction_alternative_in_next_step:
                    num_occurences_of_direction_alternative_in_next_step[direction_alternative] = dict()
                if next_direction_alternative not in num_occurences_of_direction_alternative_in_next_step[direction_alternative]:
                    num_occurences_of_direction_alternative_in_next_step[direction_alternative][next_direction_alternative] = 0
                num_occurences_of_direction_alternative_in_next_step[direction_alternative][next_direction_alternative] += 1
                if direction_alternative_index < len(direction_alternative_int) - 2:
                    next_next_direction_alternative = direction_alternative_int[direction_alternative_index + 2]
                    if direction_alternative not in num_occurences_of_direction_alternative_in_next_next_step:
                        num_occurences_of_direction_alternative_in_next_next_step[direction_alternative] = dict()
                    if next_direction_alternative not in num_occurences_of_direction_alternative_in_next_next_step[direction_alternative]:
                        num_occurences_of_direction_alternative_in_next_next_step[direction_alternative][next_direction_alternative] = dict()
                    if next_next_direction_alternative not in num_occurences_of_direction_alternative_in_next_next_step[direction_alternative][next_direction_alternative]:
                        num_occurences_of_direction_alternative_in_next_next_step[direction_alternative][next_direction_alternative][next_next_direction_alternative] = 0
                    num_occurences_of_direction_alternative_in_next_next_step[direction_alternative][next_direction_alternative][next_next_direction_alternative] += 1

    #print(num_occurences_of_direction_alternative)
    save_object("num_occurences/num_occurences_of_direction_alternative", num_occurences_of_direction_alternative)
    #print(num_occurences_of_direction_alternative.keys())

    #print(num_occurences_of_direction_alternative_diff)
    plt.bar(num_occurences_of_direction_alternative_diff.keys(), num_occurences_of_direction_alternative_diff.values())
    plt.show()

    #print(num_occurences_of_direction_alternative_in_next_step)
    save_object("num_occurences/num_occurences_of_direction_alternative_in_next_step", num_occurences_of_direction_alternative_in_next_step)
    #print(num_occurences_of_direction_alternative_in_next_next_step)
    save_object("num_occurences/num_occurences_of_direction_alternative_in_next_next_step", num_occurences_of_direction_alternative_in_next_next_step)

    probability_of_direction_alternative = dict()
    for direction_alternative in num_occurences_of_direction_alternative:
        probability_of_direction_alternative[direction_alternative] = num_occurences_of_direction_alternative[direction_alternative] / sum(list(num_occurences_of_direction_alternative.values()))

    probability_of_direction_alternative_in_next_step = dict()
    for prev_direction_alternative in num_occurences_of_direction_alternative_in_next_step:
        probability_of_direction_alternative_in_next_step[prev_direction_alternative] = dict()
        for direction_alternative in num_occurences_of_direction_alternative_in_next_step[prev_direction_alternative]:
            probability_of_direction_alternative_in_next_step[prev_direction_alternative][direction_alternative] = num_occurences_of_direction_alternative_in_next_step[prev_direction_alternative][direction_alternative] / sum(list(num_occurences_of_direction_alternative_in_next_step[prev_direction_alternative].values()))

    probability_of_direction_alternative_in_next_next_step = dict()
    for prev_prev_direction_alternative in num_occurences_of_direction_alternative_in_next_next_step:
        probability_of_direction_alternative_in_next_next_step[prev_prev_direction_alternative] = dict()
        for prev_direction_alternative in num_occurences_of_direction_alternative_in_next_next_step[prev_prev_direction_alternative]:
            probability_of_direction_alternative_in_next_next_step[prev_prev_direction_alternative][prev_direction_alternative] = dict()
            for direction_alternative in num_occurences_of_direction_alternative_in_next_next_step[prev_prev_direction_alternative][prev_direction_alternative]:
                probability_of_direction_alternative_in_next_next_step[prev_prev_direction_alternative][prev_direction_alternative][direction_alternative] = num_occurences_of_direction_alternative_in_next_next_step[prev_prev_direction_alternative][prev_direction_alternative][direction_alternative] / sum(list(num_occurences_of_direction_alternative_in_next_next_step[prev_prev_direction_alternative][prev_direction_alternative].values()))

    #print(probability_of_direction_alternative)
    save_object("probability/probability_of_direction_alternative", probability_of_direction_alternative)
    #print(probability_of_direction_alternative_in_next_step)
    save_object("probability/probability_of_direction_alternative_in_next_step", probability_of_direction_alternative_in_next_step)
    #print(probability_of_direction_alternative_in_next_next_step)
    save_object("probability/probability_of_direction_alternative_in_next_next_step", probability_of_direction_alternative_in_next_next_step)

probability_of_direction_alternative = load_object("probability/probability_of_direction_alternative") 
probability_of_direction_alternative_in_next_step = load_object("probability/probability_of_direction_alternative_in_next_step") 
probability_of_direction_alternative_in_next_next_step = load_object("probability/probability_of_direction_alternative_in_next_next_step")  

x = []
n = 10000
prev_direction_alternative = 0
prev_prev_direction_alternative = 0
for i in range(n):
    if i == 0:
        direction_alternative = np.random.choice(list(probability_of_direction_alternative.keys()),p=list(probability_of_direction_alternative.values()))  
    if i == 1:
        if prev_direction_alternative in probability_of_direction_alternative_in_next_step:
            direction_alternative = np.random.choice(list(probability_of_direction_alternative_in_next_step[prev_direction_alternative].keys()),p=list(probability_of_direction_alternative_in_next_step[prev_direction_alternative].values())) 
        else:
            break
    if i > 1:
        if prev_prev_direction_alternative in probability_of_direction_alternative_in_next_next_step and prev_direction_alternative in probability_of_direction_alternative_in_next_next_step[prev_prev_direction_alternative]:
            direction_alternative = np.random.choice(list(probability_of_direction_alternative_in_next_next_step[prev_prev_direction_alternative][prev_direction_alternative].keys()),p=list(probability_of_direction_alternative_in_next_next_step[prev_prev_direction_alternative][prev_direction_alternative].values())) 
        else:
            break
    prev_prev_direction_alternative = prev_direction_alternative
    prev_direction_alternative = direction_alternative
    x.append(direction_alternative)

plt.plot(x)
plt.xlabel('Directions',fontsize=20)
plt.ylabel(r'$S_{n}$',fontsize=20)
plt.show()

total_match_score = 0
total_guesses = 0 
total_guesses_no_empty = 0
delta_series_total = [] 
all_x = []
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
            last_value = direction_alternative_int[heading_alternative_index]

        x = []
        n = len(direction_alternative_int)
        prev_direction_alternative = 0
        prev_prev_direction_alternative = 0
        for i in range(n):
            direction_alternative = -1
            if i == 0:
                direction_alternative = np.random.choice(list(probability_of_direction_alternative.keys()),p=list(probability_of_direction_alternative.values()))  
            if i == 1:
                if direction_alternative_int[i - 1] in probability_of_direction_alternative_in_next_step:
                    direction_alternative = np.random.choice(list(probability_of_direction_alternative_in_next_step[direction_alternative_int[i - 1]].keys()),p=list(probability_of_direction_alternative_in_next_step[direction_alternative_int[i - 1]].values())) 
            if i > 1:
                if direction_alternative_int[i - 2] in probability_of_direction_alternative_in_next_next_step and direction_alternative_int[i - 1] in probability_of_direction_alternative_in_next_next_step[direction_alternative_int[i - 2]]:
                    direction_alternative = np.random.choice(list(probability_of_direction_alternative_in_next_next_step[direction_alternative_int[i - 2]][direction_alternative_int[i - 1]].keys()),p=list(probability_of_direction_alternative_in_next_next_step[direction_alternative_int[i - 2]][direction_alternative_int[i - 1]].values())) 
            x.append(direction_alternative)

        match_score = 0 
        no_empty = 0
        delta_series = [] 
        for i in range(n):
            if x[i] == direction_alternative_int[i]:
                match_score += 1
            if x[i] != -1:
                no_empty += 1
                delta_x = abs(direction_alternative_int[i] - x[i])
                if delta_x > 180:
                    delta_x = 360 - delta_x
                delta_series.append(delta_x)
                delta_series_total.append(delta_x)
        #print(match_score / n, match_score / no_empty, min(delta_series), np.quantile(delta_series, 0.25), np.quantile(delta_series, 0.5), np.quantile(delta_series, 0.75), max(delta_series), np.average(delta_series), np.std(delta_series), np.var(delta_series))
        total_guesses += n
        total_guesses_no_empty += no_empty
        total_match_score += match_score 
        #plt.hist(delta_series)
        #plt.show()
        all_x.append(x)
save_object("predicted/predicted_direction_alternative", all_x)
print(total_match_score / total_guesses, total_match_score / total_guesses_no_empty, min(delta_series_total), np.quantile(delta_series_total, 0.25), np.quantile(delta_series_total, 0.5), np.quantile(delta_series_total, 0.75), max(delta_series_total), np.average(delta_series_total), np.std(delta_series_total), np.var(delta_series_total))

plt.hist(delta_series_total)
plt.show()
