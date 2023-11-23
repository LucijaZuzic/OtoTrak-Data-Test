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

if not os.path.isfile("num_occurences_of_longitude_sgn"):
    num_occurences_of_longitude_sgn = dict()
    num_occurences_of_longitude_sgn_in_next_step = dict()
    num_occurences_of_longitude_sgn_in_next_next_step = dict()

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
            longitude_int = [longitudes[longitude_index + 1] > longitudes[longitude_index] for longitude_index in range(len(longitudes) - 1)]

            for longitude in longitude_int:
                if longitude not in num_occurences_of_longitude_sgn:
                    num_occurences_of_longitude_sgn[longitude] = 0
                num_occurences_of_longitude_sgn[longitude] += 1
 
            for longitude_index in range(len(longitude_int) - 1):
                longitude = longitude_int[longitude_index]
                next_longitude_sgn = longitude_int[longitude_index + 1]
                if longitude not in num_occurences_of_longitude_sgn_in_next_step:
                    num_occurences_of_longitude_sgn_in_next_step[longitude] = dict()
                if next_longitude_sgn not in num_occurences_of_longitude_sgn_in_next_step[longitude]:
                    num_occurences_of_longitude_sgn_in_next_step[longitude][next_longitude_sgn] = 0
                num_occurences_of_longitude_sgn_in_next_step[longitude][next_longitude_sgn] += 1
                if longitude_index < len(longitude_int) - 2:
                    next_next_longitude_sgn = longitude_int[longitude_index + 2]
                    if longitude not in num_occurences_of_longitude_sgn_in_next_next_step:
                        num_occurences_of_longitude_sgn_in_next_next_step[longitude] = dict()
                    if next_longitude_sgn not in num_occurences_of_longitude_sgn_in_next_next_step[longitude]:
                        num_occurences_of_longitude_sgn_in_next_next_step[longitude][next_longitude_sgn] = dict()
                    if next_next_longitude_sgn not in num_occurences_of_longitude_sgn_in_next_next_step[longitude][next_longitude_sgn]:
                        num_occurences_of_longitude_sgn_in_next_next_step[longitude][next_longitude_sgn][next_next_longitude_sgn] = 0
                    num_occurences_of_longitude_sgn_in_next_next_step[longitude][next_longitude_sgn][next_next_longitude_sgn] += 1

    #print(num_occurences_of_longitude_sgn)
    save_object("num_occurences_of_longitude_sgn", num_occurences_of_longitude_sgn)
    #print(num_occurences_of_longitude_sgn.keys())

    plt.bar(num_occurences_of_longitude_sgn.keys(), num_occurences_of_longitude_sgn.values())
    plt.show()

    #print(num_occurences_of_longitude_sgn_in_next_step)
    save_object("num_occurences_of_longitude_sgn_in_next_step", num_occurences_of_longitude_sgn_in_next_step)
    #print(num_occurences_of_longitude_sgn_in_next_next_step)
    save_object("num_occurences_of_longitude_sgn_in_next_next_step", num_occurences_of_longitude_sgn_in_next_next_step)

    probability_of_longitude_sgn = dict()
    for longitude in num_occurences_of_longitude_sgn:
        probability_of_longitude_sgn[longitude] = num_occurences_of_longitude_sgn[longitude] / sum(list(num_occurences_of_longitude_sgn.values()))

    probability_of_longitude_sgn_in_next_step = dict()
    for prev_longitude_sgn in num_occurences_of_longitude_sgn_in_next_step:
        probability_of_longitude_sgn_in_next_step[prev_longitude_sgn] = dict()
        for longitude in num_occurences_of_longitude_sgn_in_next_step[prev_longitude_sgn]:
            probability_of_longitude_sgn_in_next_step[prev_longitude_sgn][longitude] = num_occurences_of_longitude_sgn_in_next_step[prev_longitude_sgn][longitude] / sum(list(num_occurences_of_longitude_sgn_in_next_step[prev_longitude_sgn].values()))

    probability_of_longitude_sgn_in_next_next_step = dict()
    for prev_prev_longitude_sgn in num_occurences_of_longitude_sgn_in_next_next_step:
        probability_of_longitude_sgn_in_next_next_step[prev_prev_longitude_sgn] = dict()
        for prev_longitude_sgn in num_occurences_of_longitude_sgn_in_next_next_step[prev_prev_longitude_sgn]:
            probability_of_longitude_sgn_in_next_next_step[prev_prev_longitude_sgn][prev_longitude_sgn] = dict()
            for longitude in num_occurences_of_longitude_sgn_in_next_next_step[prev_prev_longitude_sgn][prev_longitude_sgn]:
                probability_of_longitude_sgn_in_next_next_step[prev_prev_longitude_sgn][prev_longitude_sgn][longitude] = num_occurences_of_longitude_sgn_in_next_next_step[prev_prev_longitude_sgn][prev_longitude_sgn][longitude] / sum(list(num_occurences_of_longitude_sgn_in_next_next_step[prev_prev_longitude_sgn][prev_longitude_sgn].values()))

    #print(probability_of_longitude_sgn)
    save_object("probability_of_longitude_sgn", probability_of_longitude_sgn)
    #print(probability_of_longitude_sgn_in_next_step)
    save_object("probability_of_longitude_sgn_in_next_step", probability_of_longitude_sgn_in_next_step)
    #print(probability_of_longitude_sgn_in_next_next_step)
    save_object("probability_of_longitude_sgn_in_next_next_step", probability_of_longitude_sgn_in_next_next_step)

probability_of_longitude_sgn = load_object("probability_of_longitude_sgn") 
probability_of_longitude_sgn_in_next_step = load_object("probability_of_longitude_sgn_in_next_step") 
probability_of_longitude_sgn_in_next_next_step = load_object("probability_of_longitude_sgn_in_next_next_step")  

x = []
n = 10000
prev_longitude_sgn = 0
prev_prev_longitude_sgn = 0
for i in range(n):
    if i == 0:
        longitude = np.random.choice(list(probability_of_longitude_sgn.keys()),p=list(probability_of_longitude_sgn.values()))  
    if i == 1:
        if prev_longitude_sgn in probability_of_longitude_sgn_in_next_step:
            longitude = np.random.choice(list(probability_of_longitude_sgn_in_next_step[prev_longitude_sgn].keys()),p=list(probability_of_longitude_sgn_in_next_step[prev_longitude_sgn].values())) 
        else:
            break
    if i > 1:
        if prev_prev_longitude_sgn in probability_of_longitude_sgn_in_next_next_step and prev_longitude_sgn in probability_of_longitude_sgn_in_next_next_step[prev_prev_longitude_sgn]:
            longitude = np.random.choice(list(probability_of_longitude_sgn_in_next_next_step[prev_prev_longitude_sgn][prev_longitude_sgn].keys()),p=list(probability_of_longitude_sgn_in_next_next_step[prev_prev_longitude_sgn][prev_longitude_sgn].values())) 
        else:
            break
    prev_prev_longitude_sgn = prev_longitude_sgn
    prev_longitude_sgn = longitude
    x.append(longitude)

plt.plot(x)
plt.xlabel('Longitude Signs',fontsize=20)
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
        longitude_int = [longitudes[longitude_index + 1] > longitudes[longitude_index] for longitude_index in range(len(longitudes) - 1)]
 
        x = []
        n = len(longitude_int)
        prev_longitude_sgn = 0
        prev_prev_longitude_sgn = 0
        for i in range(n):
            longitude = -1
            if i == 0:
                longitude = np.random.choice(list(probability_of_longitude_sgn.keys()),p=list(probability_of_longitude_sgn.values()))  
            if i == 1:
                if longitude_int[i - 1] in probability_of_longitude_sgn_in_next_step:
                    longitude = np.random.choice(list(probability_of_longitude_sgn_in_next_step[longitude_int[i - 1]].keys()),p=list(probability_of_longitude_sgn_in_next_step[longitude_int[i - 1]].values())) 
            if i > 1:
                if longitude_int[i - 2] in probability_of_longitude_sgn_in_next_next_step and longitude_int[i - 1] in probability_of_longitude_sgn_in_next_next_step[longitude_int[i - 2]]:
                    longitude = np.random.choice(list(probability_of_longitude_sgn_in_next_next_step[longitude_int[i - 2]][longitude_int[i - 1]].keys()),p=list(probability_of_longitude_sgn_in_next_next_step[longitude_int[i - 2]][longitude_int[i - 1]].values())) 
            x.append(longitude)

        match_score = 0 
        no_empty = 0
        delta_series = [] 
        for i in range(n):
            if x[i] == longitude_int[i]:
                match_score += 1
            if x[i] != -1:
                no_empty += 1
                delta_x = (longitude_int[i] != x[i]) * 1
                delta_series.append(delta_x)
                delta_series_total.append(delta_x)
        #print(match_score / n, match_score / no_empty, min(delta_series), np.quantile(delta_series, 0.25), np.quantile(delta_series, 0.5), np.quantile(delta_series, 0.75), max(delta_series), np.average(delta_series), np.std(delta_series), np.var(delta_series))
        total_guesses += n
        total_guesses_no_empty += no_empty
        total_match_score += match_score 
        #plt.hist(delta_series)
        #plt.show()
        all_x.append(x)
save_object("predicted_longitude_sgn", all_x)
print(total_match_score / total_guesses, total_match_score / total_guesses_no_empty, min(delta_series_total), np.quantile(delta_series_total, 0.25), np.quantile(delta_series_total, 0.5), np.quantile(delta_series_total, 0.75), max(delta_series_total), np.average(delta_series_total), np.std(delta_series_total), np.var(delta_series_total))

plt.hist(delta_series_total)
plt.show()
