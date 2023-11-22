import os
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

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
    
all_subdirs = os.listdir() 

if not os.path.isfile("num_occurences_of_y_speed_alternative"):
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
            latitudes = list(file_with_ride["fields_latitude"])  
            times = list(file_with_ride["time"])
            times_processed = [process_time(time_new) for time_new in times] 
            times_delays = [(times_processed[time_index + 1] - times_processed[time_index]).total_seconds() + 0.001 for time_index in range(len(times_processed) - 1)] 
            distance_int = [abs(latitudes[distance_index + 1] - latitudes[distance_index]) for distance_index in range(len(latitudes) - 1)]
            y_speed_alternative_int = [np.round(distance_int[y_speed_alternative_index] / times_delays[y_speed_alternative_index], 5) for y_speed_alternative_index in range(len(times_delays))]

            for y_speed_alternative in y_speed_alternative_int:
                if y_speed_alternative not in num_occurences_of_y_speed_alternative:
                    num_occurences_of_y_speed_alternative[y_speed_alternative] = 0
                num_occurences_of_y_speed_alternative[y_speed_alternative] += 1

            for y_speed_alternative_index in range(len(y_speed_alternative_int) - 1):
                y_speed_alternative = y_speed_alternative_int[y_speed_alternative_index]
                next_y_speed_alternative = y_speed_alternative_int[y_speed_alternative_index + 1]
                if y_speed_alternative not in num_occurences_of_y_speed_alternative_in_next_step:
                    num_occurences_of_y_speed_alternative_in_next_step[y_speed_alternative] = dict()
                if next_y_speed_alternative not in num_occurences_of_y_speed_alternative_in_next_step[y_speed_alternative]:
                    num_occurences_of_y_speed_alternative_in_next_step[y_speed_alternative][next_y_speed_alternative] = 0
                num_occurences_of_y_speed_alternative_in_next_step[y_speed_alternative][next_y_speed_alternative] += 1
                if y_speed_alternative_index < len(y_speed_alternative_int) - 2:
                    next_next_y_speed_alternative = y_speed_alternative_int[y_speed_alternative_index + 2]
                    if y_speed_alternative not in num_occurences_of_y_speed_alternative_in_next_next_step:
                        num_occurences_of_y_speed_alternative_in_next_next_step[y_speed_alternative] = dict()
                    if next_y_speed_alternative not in num_occurences_of_y_speed_alternative_in_next_next_step[y_speed_alternative]:
                        num_occurences_of_y_speed_alternative_in_next_next_step[y_speed_alternative][next_y_speed_alternative] = dict()
                    if next_next_y_speed_alternative not in num_occurences_of_y_speed_alternative_in_next_next_step[y_speed_alternative][next_y_speed_alternative]:
                        num_occurences_of_y_speed_alternative_in_next_next_step[y_speed_alternative][next_y_speed_alternative][next_next_y_speed_alternative] = 0
                    num_occurences_of_y_speed_alternative_in_next_next_step[y_speed_alternative][next_y_speed_alternative][next_next_y_speed_alternative] += 1

    #print(num_occurences_of_y_speed_alternative)
    save_object("num_occurences_of_y_speed_alternative", num_occurences_of_y_speed_alternative)
    #print(num_occurences_of_y_speed_alternative.keys())

    plt.bar(num_occurences_of_y_speed_alternative.keys(), num_occurences_of_y_speed_alternative.values())
    plt.show()

    #print(num_occurences_of_y_speed_alternative_in_next_step)
    save_object("num_occurences_of_y_speed_alternative_in_next_step", num_occurences_of_y_speed_alternative_in_next_step)
    #print(num_occurences_of_y_speed_alternative_in_next_next_step)
    save_object("num_occurences_of_y_speed_alternative_in_next_next_step", num_occurences_of_y_speed_alternative_in_next_next_step)

    probability_of_y_speed_alternative = dict()
    for y_speed_alternative in num_occurences_of_y_speed_alternative:
        probability_of_y_speed_alternative[y_speed_alternative] = num_occurences_of_y_speed_alternative[y_speed_alternative] / sum(list(num_occurences_of_y_speed_alternative.values()))

    probability_of_y_speed_alternative_in_next_step = dict()
    for prev_y_speed_alternative in num_occurences_of_y_speed_alternative_in_next_step:
        probability_of_y_speed_alternative_in_next_step[prev_y_speed_alternative] = dict()
        for y_speed_alternative in num_occurences_of_y_speed_alternative_in_next_step[prev_y_speed_alternative]:
            probability_of_y_speed_alternative_in_next_step[prev_y_speed_alternative][y_speed_alternative] = num_occurences_of_y_speed_alternative_in_next_step[prev_y_speed_alternative][y_speed_alternative] / sum(list(num_occurences_of_y_speed_alternative_in_next_step[prev_y_speed_alternative].values()))

    probability_of_y_speed_alternative_in_next_next_step = dict()
    for prev_prev_y_speed_alternative in num_occurences_of_y_speed_alternative_in_next_next_step:
        probability_of_y_speed_alternative_in_next_next_step[prev_prev_y_speed_alternative] = dict()
        for prev_y_speed_alternative in num_occurences_of_y_speed_alternative_in_next_next_step[prev_prev_y_speed_alternative]:
            probability_of_y_speed_alternative_in_next_next_step[prev_prev_y_speed_alternative][prev_y_speed_alternative] = dict()
            for y_speed_alternative in num_occurences_of_y_speed_alternative_in_next_next_step[prev_prev_y_speed_alternative][prev_y_speed_alternative]:
                probability_of_y_speed_alternative_in_next_next_step[prev_prev_y_speed_alternative][prev_y_speed_alternative][y_speed_alternative] = num_occurences_of_y_speed_alternative_in_next_next_step[prev_prev_y_speed_alternative][prev_y_speed_alternative][y_speed_alternative] / sum(list(num_occurences_of_y_speed_alternative_in_next_next_step[prev_prev_y_speed_alternative][prev_y_speed_alternative].values()))

    #print(probability_of_y_speed_alternative)
    save_object("probability_of_y_speed_alternative", probability_of_y_speed_alternative)
    #print(probability_of_y_speed_alternative_in_next_step)
    save_object("probability_of_y_speed_alternative_in_next_step", probability_of_y_speed_alternative_in_next_step)
    #print(probability_of_y_speed_alternative_in_next_next_step)
    save_object("probability_of_y_speed_alternative_in_next_next_step", probability_of_y_speed_alternative_in_next_next_step)

probability_of_y_speed_alternative = load_object("probability_of_y_speed_alternative") 
probability_of_y_speed_alternative_in_next_step = load_object("probability_of_y_speed_alternative_in_next_step") 
probability_of_y_speed_alternative_in_next_next_step = load_object("probability_of_y_speed_alternative_in_next_next_step")  

x = []
n = 10000
prev_y_speed_alternative = 0
prev_prev_y_speed_alternative = 0
for i in range(n):
    if i == 0:
        y_speed_alternative = np.random.choice(list(probability_of_y_speed_alternative.keys()),p=list(probability_of_y_speed_alternative.values()))  
    if i == 1:
        if prev_y_speed_alternative in probability_of_y_speed_alternative_in_next_step:
            y_speed_alternative = np.random.choice(list(probability_of_y_speed_alternative_in_next_step[prev_y_speed_alternative].keys()),p=list(probability_of_y_speed_alternative_in_next_step[prev_y_speed_alternative].values())) 
        else:
            break
    if i > 1:
        if prev_prev_y_speed_alternative in probability_of_y_speed_alternative_in_next_next_step and prev_y_speed_alternative in probability_of_y_speed_alternative_in_next_next_step[prev_prev_y_speed_alternative]:
            y_speed_alternative = np.random.choice(list(probability_of_y_speed_alternative_in_next_next_step[prev_prev_y_speed_alternative][prev_y_speed_alternative].keys()),p=list(probability_of_y_speed_alternative_in_next_next_step[prev_prev_y_speed_alternative][prev_y_speed_alternative].values())) 
        else:
            break
    prev_prev_y_speed_alternative = prev_y_speed_alternative
    prev_y_speed_alternative = y_speed_alternative
    x.append(y_speed_alternative)

plt.plot(x)
plt.xlabel('Y Speeds',fontsize=20)
plt.ylabel(r'$S_{n}$',fontsize=20)
plt.show()

total_match_score = 0
total_guesses = 0 
total_guesses_no_empty = 0
delta_series_total = [] 

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
        latitudes = list(file_with_ride["fields_latitude"])  
        times = list(file_with_ride["time"])
        times_processed = [process_time(time_new) for time_new in times] 
        times_delays = [(times_processed[time_index + 1] - times_processed[time_index]).total_seconds() + 0.001 for time_index in range(len(times_processed) - 1)] 
        distance_int = [abs(latitudes[distance_index + 1] - latitudes[distance_index]) for distance_index in range(len(latitudes) - 1)]
        y_speed_alternative_int = [np.round(distance_int[y_speed_alternative_index] / times_delays[y_speed_alternative_index], 5) for y_speed_alternative_index in range(len(times_delays))]

        x = []
        n = len(y_speed_alternative_int)
        prev_y_speed_alternative = 0
        prev_prev_y_speed_alternative = 0
        for i in range(n):
            y_speed_alternative = -1
            if i == 0:
                y_speed_alternative = np.random.choice(list(probability_of_y_speed_alternative.keys()),p=list(probability_of_y_speed_alternative.values()))  
            if i == 1:
                if y_speed_alternative_int[i - 1] in probability_of_y_speed_alternative_in_next_step:
                    y_speed_alternative = np.random.choice(list(probability_of_y_speed_alternative_in_next_step[y_speed_alternative_int[i - 1]].keys()),p=list(probability_of_y_speed_alternative_in_next_step[y_speed_alternative_int[i - 1]].values())) 
            if i > 1:
                if y_speed_alternative_int[i - 2] in probability_of_y_speed_alternative_in_next_next_step and y_speed_alternative_int[i - 1] in probability_of_y_speed_alternative_in_next_next_step[y_speed_alternative_int[i - 2]]:
                    y_speed_alternative = np.random.choice(list(probability_of_y_speed_alternative_in_next_next_step[y_speed_alternative_int[i - 2]][y_speed_alternative_int[i - 1]].keys()),p=list(probability_of_y_speed_alternative_in_next_next_step[y_speed_alternative_int[i - 2]][y_speed_alternative_int[i - 1]].values())) 
            x.append(y_speed_alternative)

        match_score = 0 
        no_empty = 0
        delta_series = [] 
        for i in range(n):
            if x[i] == y_speed_alternative_int[i]:
                match_score += 1
            if x[i] != -1:
                no_empty += 1
                delta_x = abs(y_speed_alternative_int[i] - x[i])
                delta_series.append(delta_x)
                delta_series_total.append(delta_x)
        #print(match_score / n, match_score / no_empty, min(delta_series), np.quantile(delta_series, 0.25), np.quantile(delta_series, 0.5), np.quantile(delta_series, 0.75), max(delta_series), np.average(delta_series), np.std(delta_series), np.var(delta_series))
        total_guesses += n
        total_guesses_no_empty += no_empty
        total_match_score += match_score 
        #plt.hist(delta_series)
        #plt.show()
print(total_match_score / total_guesses, total_match_score / total_guesses_no_empty, min(delta_series_total), np.quantile(delta_series_total, 0.25), np.quantile(delta_series_total, 0.5), np.quantile(delta_series_total, 0.75), max(delta_series_total), np.average(delta_series_total), np.std(delta_series_total), np.var(delta_series_total))

plt.hist(delta_series_total)
plt.show()