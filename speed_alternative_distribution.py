from utilities import *
      
all_subdirs = os.listdir() 

if not os.path.isdir("num_occurences"):
    os.makedirs("num_occurences")
if not os.path.isdir("probability"):
    os.makedirs("probability")
if not os.path.isdir("predicted"):
    os.makedirs("predicted")
flag_replace = False

if flag_replace or not os.path.isfile("num_occurences/num_occurences_of_speed_alternative"):
    num_occurences_of_speed_alternative = dict()
    num_occurences_of_speed_alternative_in_next_step = dict()
    num_occurences_of_speed_alternative_in_next_next_step = dict()

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
            times = list(file_with_ride["time"])
            times_processed = [process_time(time_new) for time_new in times] 
            times_delays = [times_processed[time_index + 1] - times_processed[time_index] for time_index in range(len(times_processed) - 1)] 
            for time_index in range(len(times_delays)):
                if times_delays[time_index] == 0:
                    times_delays[time_index] = 10 ** -20
            distance_int = [np.sqrt((longitudes[distance_index + 1] - longitudes[distance_index]) ** 2 + (latitudes[distance_index + 1] - latitudes[distance_index]) ** 2) for distance_index in range(len(longitudes) - 1)]
            speed_alternative_int = [np.round(distance_int[speed_alternative_index] / times_delays[speed_alternative_index], 5) for speed_alternative_index in range(len(times_delays))]

            for speed_alternative in speed_alternative_int:
                if speed_alternative not in num_occurences_of_speed_alternative:
                    num_occurences_of_speed_alternative[speed_alternative] = 0
                num_occurences_of_speed_alternative[speed_alternative] += 1

            for speed_alternative_index in range(len(speed_alternative_int) - 1):
                speed_alternative = speed_alternative_int[speed_alternative_index]
                next_speed_alternative = speed_alternative_int[speed_alternative_index + 1]
                if speed_alternative not in num_occurences_of_speed_alternative_in_next_step:
                    num_occurences_of_speed_alternative_in_next_step[speed_alternative] = dict()
                if next_speed_alternative not in num_occurences_of_speed_alternative_in_next_step[speed_alternative]:
                    num_occurences_of_speed_alternative_in_next_step[speed_alternative][next_speed_alternative] = 0
                num_occurences_of_speed_alternative_in_next_step[speed_alternative][next_speed_alternative] += 1
                if speed_alternative_index < len(speed_alternative_int) - 2:
                    next_next_speed_alternative = speed_alternative_int[speed_alternative_index + 2]
                    if speed_alternative not in num_occurences_of_speed_alternative_in_next_next_step:
                        num_occurences_of_speed_alternative_in_next_next_step[speed_alternative] = dict()
                    if next_speed_alternative not in num_occurences_of_speed_alternative_in_next_next_step[speed_alternative]:
                        num_occurences_of_speed_alternative_in_next_next_step[speed_alternative][next_speed_alternative] = dict()
                    if next_next_speed_alternative not in num_occurences_of_speed_alternative_in_next_next_step[speed_alternative][next_speed_alternative]:
                        num_occurences_of_speed_alternative_in_next_next_step[speed_alternative][next_speed_alternative][next_next_speed_alternative] = 0
                    num_occurences_of_speed_alternative_in_next_next_step[speed_alternative][next_speed_alternative][next_next_speed_alternative] += 1

    #print(num_occurences_of_speed_alternative)
    save_object("num_occurences/num_occurences_of_speed_alternative", num_occurences_of_speed_alternative)
    #print(num_occurences_of_speed_alternative.keys())

    plt.bar(num_occurences_of_speed_alternative.keys(), num_occurences_of_speed_alternative.values())
    plt.show()

    #print(num_occurences_of_speed_alternative_in_next_step)
    save_object("num_occurences/num_occurences_of_speed_alternative_in_next_step", num_occurences_of_speed_alternative_in_next_step)
    #print(num_occurences_of_speed_alternative_in_next_next_step)
    save_object("num_occurences/num_occurences_of_speed_alternative_in_next_next_step", num_occurences_of_speed_alternative_in_next_next_step)

    probability_of_speed_alternative = dict()
    for speed_alternative in num_occurences_of_speed_alternative:
        probability_of_speed_alternative[speed_alternative] = num_occurences_of_speed_alternative[speed_alternative] / sum(list(num_occurences_of_speed_alternative.values()))

    probability_of_speed_alternative_in_next_step = dict()
    for prev_speed_alternative in num_occurences_of_speed_alternative_in_next_step:
        probability_of_speed_alternative_in_next_step[prev_speed_alternative] = dict()
        for speed_alternative in num_occurences_of_speed_alternative_in_next_step[prev_speed_alternative]:
            probability_of_speed_alternative_in_next_step[prev_speed_alternative][speed_alternative] = num_occurences_of_speed_alternative_in_next_step[prev_speed_alternative][speed_alternative] / sum(list(num_occurences_of_speed_alternative_in_next_step[prev_speed_alternative].values()))

    probability_of_speed_alternative_in_next_next_step = dict()
    for prev_prev_speed_alternative in num_occurences_of_speed_alternative_in_next_next_step:
        probability_of_speed_alternative_in_next_next_step[prev_prev_speed_alternative] = dict()
        for prev_speed_alternative in num_occurences_of_speed_alternative_in_next_next_step[prev_prev_speed_alternative]:
            probability_of_speed_alternative_in_next_next_step[prev_prev_speed_alternative][prev_speed_alternative] = dict()
            for speed_alternative in num_occurences_of_speed_alternative_in_next_next_step[prev_prev_speed_alternative][prev_speed_alternative]:
                probability_of_speed_alternative_in_next_next_step[prev_prev_speed_alternative][prev_speed_alternative][speed_alternative] = num_occurences_of_speed_alternative_in_next_next_step[prev_prev_speed_alternative][prev_speed_alternative][speed_alternative] / sum(list(num_occurences_of_speed_alternative_in_next_next_step[prev_prev_speed_alternative][prev_speed_alternative].values()))

    #print(probability_of_speed_alternative)
    save_object("probability/probability_of_speed_alternative", probability_of_speed_alternative)
    #print(probability_of_speed_alternative_in_next_step)
    save_object("probability/probability_of_speed_alternative_in_next_step", probability_of_speed_alternative_in_next_step)
    #print(probability_of_speed_alternative_in_next_next_step)
    save_object("probability/probability_of_speed_alternative_in_next_next_step", probability_of_speed_alternative_in_next_next_step)

probability_of_speed_alternative = load_object("probability/probability_of_speed_alternative") 
probability_of_speed_alternative_in_next_step = load_object("probability/probability_of_speed_alternative_in_next_step") 
probability_of_speed_alternative_in_next_next_step = load_object("probability/probability_of_speed_alternative_in_next_next_step")  

x = []
n = 10000
prev_speed_alternative = 0
prev_prev_speed_alternative = 0
for i in range(n):
    if i == 0:
        speed_alternative = np.random.choice(list(probability_of_speed_alternative.keys()),p=list(probability_of_speed_alternative.values()))  
    if i == 1:
        if prev_speed_alternative in probability_of_speed_alternative_in_next_step:
            speed_alternative = np.random.choice(list(probability_of_speed_alternative_in_next_step[prev_speed_alternative].keys()),p=list(probability_of_speed_alternative_in_next_step[prev_speed_alternative].values())) 
        else:
            break
    if i > 1:
        if prev_prev_speed_alternative in probability_of_speed_alternative_in_next_next_step and prev_speed_alternative in probability_of_speed_alternative_in_next_next_step[prev_prev_speed_alternative]:
            speed_alternative = np.random.choice(list(probability_of_speed_alternative_in_next_next_step[prev_prev_speed_alternative][prev_speed_alternative].keys()),p=list(probability_of_speed_alternative_in_next_next_step[prev_prev_speed_alternative][prev_speed_alternative].values())) 
        else:
            break
    prev_prev_speed_alternative = prev_speed_alternative
    prev_speed_alternative = speed_alternative
    x.append(speed_alternative)

plt.plot(x)
plt.xlabel('Speeds',fontsize=20)
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
        times = list(file_with_ride["time"])
        times_processed = [process_time(time_new) for time_new in times] 
        times_delays = [times_processed[time_index + 1] - times_processed[time_index] for time_index in range(len(times_processed) - 1)] 
        for time_index in range(len(times_delays)):
                if times_delays[time_index] == 0:
                    times_delays[time_index] = 10 ** -20
        distance_int = [np.sqrt((longitudes[distance_index + 1] - longitudes[distance_index]) ** 2 + (latitudes[distance_index + 1] - latitudes[distance_index]) ** 2) for distance_index in range(len(longitudes) - 1)]
        speed_alternative_int = [np.round(distance_int[speed_alternative_index] / times_delays[speed_alternative_index], 5) for speed_alternative_index in range(len(times_delays))]

        x = []
        n = len(speed_alternative_int)
        prev_speed_alternative = 0
        prev_prev_speed_alternative = 0
        for i in range(n):
            speed_alternative = -1
            if i == 0:
                speed_alternative = np.random.choice(list(probability_of_speed_alternative.keys()),p=list(probability_of_speed_alternative.values()))  
            if i == 1:
                if speed_alternative_int[i - 1] in probability_of_speed_alternative_in_next_step:
                    speed_alternative = np.random.choice(list(probability_of_speed_alternative_in_next_step[speed_alternative_int[i - 1]].keys()),p=list(probability_of_speed_alternative_in_next_step[speed_alternative_int[i - 1]].values())) 
            if i > 1:
                if speed_alternative_int[i - 2] in probability_of_speed_alternative_in_next_next_step and speed_alternative_int[i - 1] in probability_of_speed_alternative_in_next_next_step[speed_alternative_int[i - 2]]:
                    speed_alternative = np.random.choice(list(probability_of_speed_alternative_in_next_next_step[speed_alternative_int[i - 2]][speed_alternative_int[i - 1]].keys()),p=list(probability_of_speed_alternative_in_next_next_step[speed_alternative_int[i - 2]][speed_alternative_int[i - 1]].values())) 
            x.append(speed_alternative)

        match_score = 0 
        no_empty = 0
        delta_series = [] 
        for i in range(n):
            if x[i] == speed_alternative_int[i]:
                match_score += 1
            if x[i] != -1:
                no_empty += 1
                delta_x = abs(speed_alternative_int[i] - x[i])
                delta_series.append(delta_x)
                delta_series_total.append(delta_x)
        #print(match_score / n, match_score / no_empty, min(delta_series), np.quantile(delta_series, 0.25), np.quantile(delta_series, 0.5), np.quantile(delta_series, 0.75), max(delta_series), np.average(delta_series), np.std(delta_series), np.var(delta_series))
        total_guesses += n
        total_guesses_no_empty += no_empty
        total_match_score += match_score 
        #plt.hist(delta_series)
        #plt.show()
        all_x[subdir_name + "/cleaned_csv/" + some_file] = x
save_object("predicted/predicted_speed_alternative", all_x)
print(total_match_score / total_guesses, total_match_score / total_guesses_no_empty, min(delta_series_total), np.quantile(delta_series_total, 0.25), np.quantile(delta_series_total, 0.5), np.quantile(delta_series_total, 0.75), max(delta_series_total), np.average(delta_series_total), np.std(delta_series_total), np.var(delta_series_total))

plt.hist(delta_series_total)
plt.show()
