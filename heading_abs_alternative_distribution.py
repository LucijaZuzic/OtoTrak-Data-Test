from utilities import *
    
all_subdirs = os.listdir() 

if not os.path.isdir("num_occurences"):
    os.makedirs("num_occurences")
if not os.path.isdir("probability"):
    os.makedirs("probability")
if not os.path.isdir("predicted"):
    os.makedirs("predicted")
flag_replace = False

if flag_replace or not os.path.isfile("num_occurences/num_occurences_of_direction_abs_alternative"):
    num_occurences_of_direction_abs_alternative = dict()
    num_occurences_of_direction_abs_alternative_diff = dict()
    num_occurences_of_direction_abs_alternative_in_next_step = dict()
    num_occurences_of_direction_abs_alternative_in_next_next_step = dict()

    for subdir_name in all_subdirs: 
        if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
            continue 
        
        all_rides_cleaned = os.listdir(subdir_name + "/cleaned_csv/")
        
        all_files = os.listdir(subdir_name + "/cleaned_csv/") 
        bad_rides_filenames = set()
        if os.path.isfile(subdir_name + "/bad_rides_filenames"):
            bad_rides_filenames = load_object(subdir_name + "/bad_rides_filenames")
        gap_rides_filenames = set()
        if os.path.isfile(subdir_name + "/gap_rides_filenames"):
            gap_rides_filenames = load_object(subdir_name + "/gap_rides_filenames")
        test_rides = set()
        if os.path.isfile(subdir_name + "/test_rides"):
            test_rides = load_object(subdir_name + "/test_rides")
            
        for some_file in all_files:  
            if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames or some_file in test_rides: 
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
                    if ydistance_int[heading_alternative_index] < 0:
                        direction_abs_alternative_int.append(270.0)
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
                last_value = direction_abs_alternative_int[heading_alternative_index]
 
            for direction_abs_alternative in direction_abs_alternative_int:
                if direction_abs_alternative not in num_occurences_of_direction_abs_alternative:
                    num_occurences_of_direction_abs_alternative[direction_abs_alternative] = 0
                num_occurences_of_direction_abs_alternative[direction_abs_alternative] += 1

            for direction_abs_alternative_index in range(len(direction_abs_alternative_int) - 1):
                direction_abs_alternative = direction_abs_alternative_int[direction_abs_alternative_index]
                next_direction_abs_alternative = direction_abs_alternative_int[direction_abs_alternative_index + 1]
                direction_abs_alternative_diff = abs(next_direction_abs_alternative - direction_abs_alternative)
                if direction_abs_alternative_diff > 180:
                    direction_abs_alternative_diff = 360 - direction_abs_alternative_diff
                if direction_abs_alternative_diff not in num_occurences_of_direction_abs_alternative_diff: 
                    num_occurences_of_direction_abs_alternative_diff[direction_abs_alternative_diff] = 0
                num_occurences_of_direction_abs_alternative_diff[direction_abs_alternative_diff] += 1
                if direction_abs_alternative not in num_occurences_of_direction_abs_alternative_in_next_step:
                    num_occurences_of_direction_abs_alternative_in_next_step[direction_abs_alternative] = dict()
                if next_direction_abs_alternative not in num_occurences_of_direction_abs_alternative_in_next_step[direction_abs_alternative]:
                    num_occurences_of_direction_abs_alternative_in_next_step[direction_abs_alternative][next_direction_abs_alternative] = 0
                num_occurences_of_direction_abs_alternative_in_next_step[direction_abs_alternative][next_direction_abs_alternative] += 1
                if direction_abs_alternative_index < len(direction_abs_alternative_int) - 2:
                    next_next_direction_abs_alternative = direction_abs_alternative_int[direction_abs_alternative_index + 2]
                    if direction_abs_alternative not in num_occurences_of_direction_abs_alternative_in_next_next_step:
                        num_occurences_of_direction_abs_alternative_in_next_next_step[direction_abs_alternative] = dict()
                    if next_direction_abs_alternative not in num_occurences_of_direction_abs_alternative_in_next_next_step[direction_abs_alternative]:
                        num_occurences_of_direction_abs_alternative_in_next_next_step[direction_abs_alternative][next_direction_abs_alternative] = dict()
                    if next_next_direction_abs_alternative not in num_occurences_of_direction_abs_alternative_in_next_next_step[direction_abs_alternative][next_direction_abs_alternative]:
                        num_occurences_of_direction_abs_alternative_in_next_next_step[direction_abs_alternative][next_direction_abs_alternative][next_next_direction_abs_alternative] = 0
                    num_occurences_of_direction_abs_alternative_in_next_next_step[direction_abs_alternative][next_direction_abs_alternative][next_next_direction_abs_alternative] += 1

    #print(num_occurences_of_direction_abs_alternative)
    save_object("num_occurences/num_occurences_of_direction_abs_alternative", num_occurences_of_direction_abs_alternative)
    #print(num_occurences_of_direction_abs_alternative.keys())

    #print(num_occurences_of_direction_abs_alternative_diff)
    plt.bar(num_occurences_of_direction_abs_alternative_diff.keys(), num_occurences_of_direction_abs_alternative_diff.values())
    plt.show()

    #print(num_occurences_of_direction_abs_alternative_in_next_step)
    save_object("num_occurences/num_occurences_of_direction_abs_alternative_in_next_step", num_occurences_of_direction_abs_alternative_in_next_step)
    #print(num_occurences_of_direction_abs_alternative_in_next_next_step)
    save_object("num_occurences/num_occurences_of_direction_abs_alternative_in_next_next_step", num_occurences_of_direction_abs_alternative_in_next_next_step)

    probability_of_direction_abs_alternative = dict()
    for direction_abs_alternative in num_occurences_of_direction_abs_alternative:
        probability_of_direction_abs_alternative[direction_abs_alternative] = num_occurences_of_direction_abs_alternative[direction_abs_alternative] / sum(list(num_occurences_of_direction_abs_alternative.values()))

    probability_of_direction_abs_alternative_in_next_step = dict()
    for prev_direction_abs_alternative in num_occurences_of_direction_abs_alternative_in_next_step:
        probability_of_direction_abs_alternative_in_next_step[prev_direction_abs_alternative] = dict()
        for direction_abs_alternative in num_occurences_of_direction_abs_alternative_in_next_step[prev_direction_abs_alternative]:
            probability_of_direction_abs_alternative_in_next_step[prev_direction_abs_alternative][direction_abs_alternative] = num_occurences_of_direction_abs_alternative_in_next_step[prev_direction_abs_alternative][direction_abs_alternative] / sum(list(num_occurences_of_direction_abs_alternative_in_next_step[prev_direction_abs_alternative].values()))

    probability_of_direction_abs_alternative_in_next_next_step = dict()
    for prev_prev_direction_abs_alternative in num_occurences_of_direction_abs_alternative_in_next_next_step:
        probability_of_direction_abs_alternative_in_next_next_step[prev_prev_direction_abs_alternative] = dict()
        for prev_direction_abs_alternative in num_occurences_of_direction_abs_alternative_in_next_next_step[prev_prev_direction_abs_alternative]:
            probability_of_direction_abs_alternative_in_next_next_step[prev_prev_direction_abs_alternative][prev_direction_abs_alternative] = dict()
            for direction_abs_alternative in num_occurences_of_direction_abs_alternative_in_next_next_step[prev_prev_direction_abs_alternative][prev_direction_abs_alternative]:
                probability_of_direction_abs_alternative_in_next_next_step[prev_prev_direction_abs_alternative][prev_direction_abs_alternative][direction_abs_alternative] = num_occurences_of_direction_abs_alternative_in_next_next_step[prev_prev_direction_abs_alternative][prev_direction_abs_alternative][direction_abs_alternative] / sum(list(num_occurences_of_direction_abs_alternative_in_next_next_step[prev_prev_direction_abs_alternative][prev_direction_abs_alternative].values()))

    #print(probability_of_direction_abs_alternative)
    save_object("probability/probability_of_direction_abs_alternative", probability_of_direction_abs_alternative)
    #print(probability_of_direction_abs_alternative_in_next_step)
    save_object("probability/probability_of_direction_abs_alternative_in_next_step", probability_of_direction_abs_alternative_in_next_step)
    #print(probability_of_direction_abs_alternative_in_next_next_step)
    save_object("probability/probability_of_direction_abs_alternative_in_next_next_step", probability_of_direction_abs_alternative_in_next_next_step)

probability_of_direction_abs_alternative = load_object("probability/probability_of_direction_abs_alternative") 
probability_of_direction_abs_alternative_in_next_step = load_object("probability/probability_of_direction_abs_alternative_in_next_step") 
probability_of_direction_abs_alternative_in_next_next_step = load_object("probability/probability_of_direction_abs_alternative_in_next_next_step")  

x = []
n = 10000
prev_direction_abs_alternative = 0
prev_prev_direction_abs_alternative = 0
for i in range(n):
    if i == 0:
        direction_abs_alternative = np.random.choice(list(probability_of_direction_abs_alternative.keys()),p=list(probability_of_direction_abs_alternative.values()))  
    if i == 1:
        if prev_direction_abs_alternative in probability_of_direction_abs_alternative_in_next_step:
            direction_abs_alternative = np.random.choice(list(probability_of_direction_abs_alternative_in_next_step[prev_direction_abs_alternative].keys()),p=list(probability_of_direction_abs_alternative_in_next_step[prev_direction_abs_alternative].values())) 
        else:
            break
    if i > 1:
        if prev_prev_direction_abs_alternative in probability_of_direction_abs_alternative_in_next_next_step and prev_direction_abs_alternative in probability_of_direction_abs_alternative_in_next_next_step[prev_prev_direction_abs_alternative]:
            direction_abs_alternative = np.random.choice(list(probability_of_direction_abs_alternative_in_next_next_step[prev_prev_direction_abs_alternative][prev_direction_abs_alternative].keys()),p=list(probability_of_direction_abs_alternative_in_next_next_step[prev_prev_direction_abs_alternative][prev_direction_abs_alternative].values())) 
        else:
            break
    prev_prev_direction_abs_alternative = prev_direction_abs_alternative
    prev_direction_abs_alternative = direction_abs_alternative
    x.append(direction_abs_alternative)

plt.plot(x)
plt.xlabel('Directions',fontsize=20)
plt.ylabel(r'$S_{n}$',fontsize=20)
plt.show()

total_match_score = 0
total_guesses = 0 
total_guesses_no_empty = 0
delta_series_total = [] 
all_x = dict()
for subdir_name in all_subdirs: 
    if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
        continue 
    
    all_rides_cleaned = os.listdir(subdir_name + "/cleaned_csv/")
      
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
                if ydistance_int[heading_alternative_index] < 0:
                    direction_abs_alternative_int.append(270.0)
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
            last_value = direction_abs_alternative_int[heading_alternative_index]

        x = []
        n = len(direction_abs_alternative_int)
        prev_direction_abs_alternative = 0
        prev_prev_direction_abs_alternative = 0
        for i in range(n):
            direction_abs_alternative = -1
            if i == 0:
                direction_abs_alternative = np.random.choice(list(probability_of_direction_abs_alternative.keys()),p=list(probability_of_direction_abs_alternative.values()))  
            if i == 1:
                if direction_abs_alternative_int[i - 1] in probability_of_direction_abs_alternative_in_next_step:
                    direction_abs_alternative = np.random.choice(list(probability_of_direction_abs_alternative_in_next_step[direction_abs_alternative_int[i - 1]].keys()),p=list(probability_of_direction_abs_alternative_in_next_step[direction_abs_alternative_int[i - 1]].values())) 
            if i > 1:
                if direction_abs_alternative_int[i - 2] in probability_of_direction_abs_alternative_in_next_next_step and direction_abs_alternative_int[i - 1] in probability_of_direction_abs_alternative_in_next_next_step[direction_abs_alternative_int[i - 2]]:
                    direction_abs_alternative = np.random.choice(list(probability_of_direction_abs_alternative_in_next_next_step[direction_abs_alternative_int[i - 2]][direction_abs_alternative_int[i - 1]].keys()),p=list(probability_of_direction_abs_alternative_in_next_next_step[direction_abs_alternative_int[i - 2]][direction_abs_alternative_int[i - 1]].values())) 
            x.append(direction_abs_alternative)

        match_score = 0 
        no_empty = 0
        delta_series = [] 
        for i in range(n):
            if x[i] == direction_abs_alternative_int[i]:
                match_score += 1
            if x[i] != -1:
                no_empty += 1
                delta_x = abs(direction_abs_alternative_int[i] - x[i])
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
        all_x[subdir_name + "/cleaned_csv/" + some_file] = x
save_object("predicted/predicted_direction_abs_alternative", all_x)
print(total_match_score / total_guesses, total_match_score / total_guesses_no_empty, min(delta_series_total), np.quantile(delta_series_total, 0.25), np.quantile(delta_series_total, 0.5), np.quantile(delta_series_total, 0.75), max(delta_series_total), np.average(delta_series_total), np.std(delta_series_total), np.var(delta_series_total))

plt.hist(delta_series_total)
plt.show()
