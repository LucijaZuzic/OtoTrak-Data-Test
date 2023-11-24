from utilities import *
    
all_subdirs = os.listdir() 

if not os.path.isdir("num_occurences"):
    os.makedirs("num_occurences")
if not os.path.isdir("probability"):
    os.makedirs("probability")
if not os.path.isdir("predicted"):
    os.makedirs("predicted")

if not os.path.isfile("num_occurences/num_occurences_of_latitude_no_abs"):
    num_occurences_of_latitude_no_abs = dict()
    num_occurences_of_latitude_no_abs_in_next_step = dict()
    num_occurences_of_latitude_no_abs_in_next_next_step = dict()

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
            latitude_int = [np.round(latitudes[latitude_index + 1] - latitudes[latitude_index], 10) for latitude_index in range(len(latitudes) - 1)]

            for latitude in latitude_int:
                if latitude not in num_occurences_of_latitude_no_abs:
                    num_occurences_of_latitude_no_abs[latitude] = 0
                num_occurences_of_latitude_no_abs[latitude] += 1
 
            for latitude_index in range(len(latitude_int) - 1):
                latitude = latitude_int[latitude_index]
                next_latitude_no_abs = latitude_int[latitude_index + 1]
                if latitude not in num_occurences_of_latitude_no_abs_in_next_step:
                    num_occurences_of_latitude_no_abs_in_next_step[latitude] = dict()
                if next_latitude_no_abs not in num_occurences_of_latitude_no_abs_in_next_step[latitude]:
                    num_occurences_of_latitude_no_abs_in_next_step[latitude][next_latitude_no_abs] = 0
                num_occurences_of_latitude_no_abs_in_next_step[latitude][next_latitude_no_abs] += 1
                if latitude_index < len(latitude_int) - 2:
                    next_next_latitude_no_abs = latitude_int[latitude_index + 2]
                    if latitude not in num_occurences_of_latitude_no_abs_in_next_next_step:
                        num_occurences_of_latitude_no_abs_in_next_next_step[latitude] = dict()
                    if next_latitude_no_abs not in num_occurences_of_latitude_no_abs_in_next_next_step[latitude]:
                        num_occurences_of_latitude_no_abs_in_next_next_step[latitude][next_latitude_no_abs] = dict()
                    if next_next_latitude_no_abs not in num_occurences_of_latitude_no_abs_in_next_next_step[latitude][next_latitude_no_abs]:
                        num_occurences_of_latitude_no_abs_in_next_next_step[latitude][next_latitude_no_abs][next_next_latitude_no_abs] = 0
                    num_occurences_of_latitude_no_abs_in_next_next_step[latitude][next_latitude_no_abs][next_next_latitude_no_abs] += 1

    #print(num_occurences_of_latitude_no_abs)
    save_object("num_occurences/num_occurences_of_latitude_no_abs", num_occurences_of_latitude_no_abs)
    #print(num_occurences_of_latitude_no_abs.keys())

    plt.bar(num_occurences_of_latitude_no_abs.keys(), num_occurences_of_latitude_no_abs.values())
    plt.show()

    #print(num_occurences_of_latitude_no_abs_in_next_step)
    save_object("num_occurences/num_occurences_of_latitude_no_abs_in_next_step", num_occurences_of_latitude_no_abs_in_next_step)
    #print(num_occurences_of_latitude_no_abs_in_next_next_step)
    save_object("num_occurences/num_occurences_of_latitude_no_abs_in_next_next_step", num_occurences_of_latitude_no_abs_in_next_next_step)

    probability_of_latitude_no_abs = dict()
    for latitude in num_occurences_of_latitude_no_abs:
        probability_of_latitude_no_abs[latitude] = num_occurences_of_latitude_no_abs[latitude] / sum(list(num_occurences_of_latitude_no_abs.values()))

    probability_of_latitude_no_abs_in_next_step = dict()
    for prev_latitude_no_abs in num_occurences_of_latitude_no_abs_in_next_step:
        probability_of_latitude_no_abs_in_next_step[prev_latitude_no_abs] = dict()
        for latitude in num_occurences_of_latitude_no_abs_in_next_step[prev_latitude_no_abs]:
            probability_of_latitude_no_abs_in_next_step[prev_latitude_no_abs][latitude] = num_occurences_of_latitude_no_abs_in_next_step[prev_latitude_no_abs][latitude] / sum(list(num_occurences_of_latitude_no_abs_in_next_step[prev_latitude_no_abs].values()))

    probability_of_latitude_no_abs_in_next_next_step = dict()
    for prev_prev_latitude_no_abs in num_occurences_of_latitude_no_abs_in_next_next_step:
        probability_of_latitude_no_abs_in_next_next_step[prev_prev_latitude_no_abs] = dict()
        for prev_latitude_no_abs in num_occurences_of_latitude_no_abs_in_next_next_step[prev_prev_latitude_no_abs]:
            probability_of_latitude_no_abs_in_next_next_step[prev_prev_latitude_no_abs][prev_latitude_no_abs] = dict()
            for latitude in num_occurences_of_latitude_no_abs_in_next_next_step[prev_prev_latitude_no_abs][prev_latitude_no_abs]:
                probability_of_latitude_no_abs_in_next_next_step[prev_prev_latitude_no_abs][prev_latitude_no_abs][latitude] = num_occurences_of_latitude_no_abs_in_next_next_step[prev_prev_latitude_no_abs][prev_latitude_no_abs][latitude] / sum(list(num_occurences_of_latitude_no_abs_in_next_next_step[prev_prev_latitude_no_abs][prev_latitude_no_abs].values()))

    #print(probability_of_latitude_no_abs)
    save_object("probability/probability_of_latitude_no_abs", probability_of_latitude_no_abs)
    #print(probability_of_latitude_no_abs_in_next_step)
    save_object("probability/probability_of_latitude_no_abs_in_next_step", probability_of_latitude_no_abs_in_next_step)
    #print(probability_of_latitude_no_abs_in_next_next_step)
    save_object("probability/probability_of_latitude_no_abs_in_next_next_step", probability_of_latitude_no_abs_in_next_next_step)

probability_of_latitude_no_abs = load_object("probability/probability_of_latitude_no_abs") 
probability_of_latitude_no_abs_in_next_step = load_object("probability/probability_of_latitude_no_abs_in_next_step") 
probability_of_latitude_no_abs_in_next_next_step = load_object("probability/probability_of_latitude_no_abs_in_next_next_step")   

x = []
n = 10000
prev_latitude_no_abs = 0
prev_prev_latitude_no_abs = 0
for i in range(n):
    if i == 0:
        latitude = np.random.choice(list(probability_of_latitude_no_abs.keys()),p=list(probability_of_latitude_no_abs.values()))  
    if i == 1:
        if prev_latitude_no_abs in probability_of_latitude_no_abs_in_next_step:
            latitude = np.random.choice(list(probability_of_latitude_no_abs_in_next_step[prev_latitude_no_abs].keys()),p=list(probability_of_latitude_no_abs_in_next_step[prev_latitude_no_abs].values())) 
        else:
            break
    if i > 1:
        if prev_prev_latitude_no_abs in probability_of_latitude_no_abs_in_next_next_step and prev_latitude_no_abs in probability_of_latitude_no_abs_in_next_next_step[prev_prev_latitude_no_abs]:
            latitude = np.random.choice(list(probability_of_latitude_no_abs_in_next_next_step[prev_prev_latitude_no_abs][prev_latitude_no_abs].keys()),p=list(probability_of_latitude_no_abs_in_next_next_step[prev_prev_latitude_no_abs][prev_latitude_no_abs].values())) 
        else:
            break
    prev_prev_latitude_no_abs = prev_latitude_no_abs
    prev_latitude_no_abs = latitude
    x.append(latitude)

plt.plot(x)
plt.xlabel('Latitudes',fontsize=20)
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
        latitude_int = [np.round(latitudes[latitude_index + 1] - latitudes[latitude_index], 10) for latitude_index in range(len(latitudes) - 1)]
 
        x = []
        n = len(latitude_int)
        prev_latitude_no_abs = 0
        prev_prev_latitude_no_abs = 0
        for i in range(n):
            latitude = -1
            if i == 0:
                latitude = np.random.choice(list(probability_of_latitude_no_abs.keys()),p=list(probability_of_latitude_no_abs.values()))  
            if i == 1:
                if latitude_int[i - 1] in probability_of_latitude_no_abs_in_next_step:
                    latitude = np.random.choice(list(probability_of_latitude_no_abs_in_next_step[latitude_int[i - 1]].keys()),p=list(probability_of_latitude_no_abs_in_next_step[latitude_int[i - 1]].values())) 
            if i > 1:
                if latitude_int[i - 2] in probability_of_latitude_no_abs_in_next_next_step and latitude_int[i - 1] in probability_of_latitude_no_abs_in_next_next_step[latitude_int[i - 2]]:
                    latitude = np.random.choice(list(probability_of_latitude_no_abs_in_next_next_step[latitude_int[i - 2]][latitude_int[i - 1]].keys()),p=list(probability_of_latitude_no_abs_in_next_next_step[latitude_int[i - 2]][latitude_int[i - 1]].values())) 
            x.append(latitude)

        match_score = 0 
        no_empty = 0
        delta_series = [] 
        for i in range(n):
            if x[i] == latitude_int[i]:
                match_score += 1
            if x[i] != -1:
                no_empty += 1
                delta_x = abs(latitude_int[i] - x[i])
                delta_series.append(delta_x)
                delta_series_total.append(delta_x)
        #print(match_score / n, match_score / no_empty, min(delta_series), np.quantile(delta_series, 0.25), np.quantile(delta_series, 0.5), np.quantile(delta_series, 0.75), max(delta_series), np.average(delta_series), np.std(delta_series), np.var(delta_series))
        total_guesses += n
        total_guesses_no_empty += no_empty
        total_match_score += match_score 
        #plt.hist(delta_series)
        #plt.show()
        all_x.append(x)
save_object("predicted/predicted_latitude_no_abs", all_x)
print(total_match_score / total_guesses, total_match_score / total_guesses_no_empty, min(delta_series_total), np.quantile(delta_series_total, 0.25), np.quantile(delta_series_total, 0.5), np.quantile(delta_series_total, 0.75), max(delta_series_total), np.average(delta_series_total), np.std(delta_series_total), np.var(delta_series_total))

plt.hist(delta_series_total)
plt.show()
