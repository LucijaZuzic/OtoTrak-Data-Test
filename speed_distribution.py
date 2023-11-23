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
    
all_subdirs = os.listdir() 

if not os.path.isdir("num_occurences"):
    os.makedirs("num_occurences")
if not os.path.isdir("probability"):
    os.makedirs("probability")
if not os.path.isdir("predicted"):
    os.makedirs("predicted")

if not os.path.isfile("num_occurences/num_occurences_of_speed"):
    num_occurences_of_speed = dict()
    num_occurences_of_speed_in_next_step = dict()
    num_occurences_of_speed_in_next_next_step = dict()

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
            speeds = list(file_with_ride["fields_speed"]) 
            speed_int = [np.round(speed, 0) for speed in speeds]

            for speed in speed_int:
                if speed not in num_occurences_of_speed:
                    num_occurences_of_speed[speed] = 0
                num_occurences_of_speed[speed] += 1

            for speed_index in range(len(speed_int) - 1):
                speed = speed_int[speed_index]
                next_speed = speed_int[speed_index + 1]
                if speed not in num_occurences_of_speed_in_next_step:
                    num_occurences_of_speed_in_next_step[speed] = dict()
                if next_speed not in num_occurences_of_speed_in_next_step[speed]:
                    num_occurences_of_speed_in_next_step[speed][next_speed] = 0
                num_occurences_of_speed_in_next_step[speed][next_speed] += 1
                if speed_index < len(speed_int) - 2:
                    next_next_speed = speed_int[speed_index + 2]
                    if speed not in num_occurences_of_speed_in_next_next_step:
                        num_occurences_of_speed_in_next_next_step[speed] = dict()
                    if next_speed not in num_occurences_of_speed_in_next_next_step[speed]:
                        num_occurences_of_speed_in_next_next_step[speed][next_speed] = dict()
                    if next_next_speed not in num_occurences_of_speed_in_next_next_step[speed][next_speed]:
                        num_occurences_of_speed_in_next_next_step[speed][next_speed][next_next_speed] = 0
                    num_occurences_of_speed_in_next_next_step[speed][next_speed][next_next_speed] += 1

    #print(num_occurences_of_speed)
    save_object("num_occurences/num_occurences_of_speed", num_occurences_of_speed)
    #print(num_occurences_of_speed.keys())

    plt.bar(num_occurences_of_speed.keys(), num_occurences_of_speed.values())
    plt.show()

    #print(num_occurences_of_speed_in_next_step)
    save_object("num_occurences/num_occurences_of_speed_in_next_step", num_occurences_of_speed_in_next_step)
    #print(num_occurences_of_speed_in_next_next_step)
    save_object("num_occurences/num_occurences_of_speed_in_next_next_step", num_occurences_of_speed_in_next_next_step)

    probability_of_speed = dict()
    for speed in num_occurences_of_speed:
        probability_of_speed[speed] = num_occurences_of_speed[speed] / sum(list(num_occurences_of_speed.values()))

    probability_of_speed_in_next_step = dict()
    for prev_speed in num_occurences_of_speed_in_next_step:
        probability_of_speed_in_next_step[prev_speed] = dict()
        for speed in num_occurences_of_speed_in_next_step[prev_speed]:
            probability_of_speed_in_next_step[prev_speed][speed] = num_occurences_of_speed_in_next_step[prev_speed][speed] / sum(list(num_occurences_of_speed_in_next_step[prev_speed].values()))

    probability_of_speed_in_next_next_step = dict()
    for prev_prev_speed in num_occurences_of_speed_in_next_next_step:
        probability_of_speed_in_next_next_step[prev_prev_speed] = dict()
        for prev_speed in num_occurences_of_speed_in_next_next_step[prev_prev_speed]:
            probability_of_speed_in_next_next_step[prev_prev_speed][prev_speed] = dict()
            for speed in num_occurences_of_speed_in_next_next_step[prev_prev_speed][prev_speed]:
                probability_of_speed_in_next_next_step[prev_prev_speed][prev_speed][speed] = num_occurences_of_speed_in_next_next_step[prev_prev_speed][prev_speed][speed] / sum(list(num_occurences_of_speed_in_next_next_step[prev_prev_speed][prev_speed].values()))

    #print(probability_of_speed)
    save_object("probability/probability_of_speed", probability_of_speed)
    #print(probability_of_speed_in_next_step)
    save_object("probability/probability_of_speed_in_next_step", probability_of_speed_in_next_step)
    #print(probability_of_speed_in_next_next_step)
    save_object("probability/probability_of_speed_in_next_next_step", probability_of_speed_in_next_next_step)

probability_of_speed = load_object("probability/probability_of_speed") 
probability_of_speed_in_next_step = load_object("probability/probability_of_speed_in_next_step") 
probability_of_speed_in_next_next_step = load_object("probability/probability_of_speed_in_next_next_step")  

x = []
n = 10000
prev_speed = 0
prev_prev_speed = 0
for i in range(n):
    if i == 0:
        speed = np.random.choice(list(probability_of_speed.keys()),p=list(probability_of_speed.values()))  
    if i == 1:
        if prev_speed in probability_of_speed_in_next_step:
            speed = np.random.choice(list(probability_of_speed_in_next_step[prev_speed].keys()),p=list(probability_of_speed_in_next_step[prev_speed].values())) 
        else:
            break
    if i > 1:
        if prev_prev_speed in probability_of_speed_in_next_next_step and prev_speed in probability_of_speed_in_next_next_step[prev_prev_speed]:
            speed = np.random.choice(list(probability_of_speed_in_next_next_step[prev_prev_speed][prev_speed].keys()),p=list(probability_of_speed_in_next_next_step[prev_prev_speed][prev_speed].values())) 
        else:
            break
    prev_prev_speed = prev_speed
    prev_speed = speed
    x.append(speed)

plt.plot(x)
plt.xlabel('Speeds',fontsize=20)
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
        speeds = list(file_with_ride["fields_speed"]) 
        speed_int = [np.round(speed, 0) for speed in speeds]
     
        x = []
        n = len(speed_int)
        prev_speed = 0
        prev_prev_speed = 0
        for i in range(n):
            speed = -1
            if i == 0:
                speed = np.random.choice(list(probability_of_speed.keys()),p=list(probability_of_speed.values()))  
            if i == 1:
                if speed_int[i - 1] in probability_of_speed_in_next_step:
                    speed = np.random.choice(list(probability_of_speed_in_next_step[speed_int[i - 1]].keys()),p=list(probability_of_speed_in_next_step[speed_int[i - 1]].values())) 
            if i > 1:
                if speed_int[i - 2] in probability_of_speed_in_next_next_step and speed_int[i - 1] in probability_of_speed_in_next_next_step[speed_int[i - 2]]:
                    speed = np.random.choice(list(probability_of_speed_in_next_next_step[speed_int[i - 2]][speed_int[i - 1]].keys()),p=list(probability_of_speed_in_next_next_step[speed_int[i - 2]][speed_int[i - 1]].values())) 
            x.append(speed)

        match_score = 0 
        no_empty = 0
        delta_series = [] 
        for i in range(n):
            if x[i] == speed_int[i]:
                match_score += 1
            if x[i] != -1:
                no_empty += 1
                delta_x = abs(speed_int[i] - x[i])
                delta_series.append(delta_x)
                delta_series_total.append(delta_x)
        #print(match_score / n, match_score / no_empty, min(delta_series), np.quantile(delta_series, 0.25), np.quantile(delta_series, 0.5), np.quantile(delta_series, 0.75), max(delta_series), np.average(delta_series), np.std(delta_series), np.var(delta_series))
        total_guesses += n
        total_guesses_no_empty += no_empty
        total_match_score += match_score 
        #plt.hist(delta_series)
        #plt.show()
        all_x.append(x)
save_object("predicted/predicted_speed", all_x)
print(total_match_score / total_guesses, total_match_score / total_guesses_no_empty, min(delta_series_total), np.quantile(delta_series_total, 0.25), np.quantile(delta_series_total, 0.5), np.quantile(delta_series_total, 0.75), max(delta_series_total), np.average(delta_series_total), np.std(delta_series_total), np.var(delta_series_total))

plt.hist(delta_series_total)
plt.show()
