from utilities import *
    
all_subdirs = os.listdir() 

if not os.path.isdir("num_occurences"):
    os.makedirs("num_occurences")
if not os.path.isdir("probability"):
    os.makedirs("probability")
if not os.path.isdir("predicted"):
    os.makedirs("predicted")
flag_replace = False

if flag_replace or not os.path.isfile("num_occurences/num_occurences_of_time"):
    num_occurences_of_time = dict()
    num_occurences_of_time_in_next_step = dict()
    num_occurences_of_time_in_next_next_step = dict()

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
            times = list(file_with_ride["time"])
            times_processed = [process_time(time_new) for time_new in times] 
            time_int = [np.round(times_processed[time_index + 1] - times_processed[time_index], 10) for time_index in range(len(times_processed) - 1)] 
            for time_index in range(len(time_int)):
                            if time_int[time_index] == 0:
                                time_int[time_index] = 10 ** -20
                                
            for time in time_int:
                if time not in num_occurences_of_time:
                    num_occurences_of_time[time] = 0
                num_occurences_of_time[time] += 1

            for time_index in range(len(time_int) - 1):
                time = time_int[time_index]
                next_time = time_int[time_index + 1]
                if time not in num_occurences_of_time_in_next_step:
                    num_occurences_of_time_in_next_step[time] = dict()
                if next_time not in num_occurences_of_time_in_next_step[time]:
                    num_occurences_of_time_in_next_step[time][next_time] = 0
                num_occurences_of_time_in_next_step[time][next_time] += 1
                if time_index < len(time_int) - 2:
                    next_next_time = time_int[time_index + 2]
                    if time not in num_occurences_of_time_in_next_next_step:
                        num_occurences_of_time_in_next_next_step[time] = dict()
                    if next_time not in num_occurences_of_time_in_next_next_step[time]:
                        num_occurences_of_time_in_next_next_step[time][next_time] = dict()
                    if next_next_time not in num_occurences_of_time_in_next_next_step[time][next_time]:
                        num_occurences_of_time_in_next_next_step[time][next_time][next_next_time] = 0
                    num_occurences_of_time_in_next_next_step[time][next_time][next_next_time] += 1

    #print(num_occurences_of_time)
    save_object("num_occurences/num_occurences_of_time", num_occurences_of_time)
    #print(num_occurences_of_time.keys())

    plt.bar(num_occurences_of_time.keys(), num_occurences_of_time.values())
    plt.show()

    #print(num_occurences_of_time_in_next_step)
    save_object("num_occurences/num_occurences_of_time_in_next_step", num_occurences_of_time_in_next_step)
    #print(num_occurences_of_time_in_next_next_step)
    save_object("num_occurences/num_occurences_of_time_in_next_next_step", num_occurences_of_time_in_next_next_step)

    probability_of_time = dict()
    for time in num_occurences_of_time:
        probability_of_time[time] = num_occurences_of_time[time] / sum(list(num_occurences_of_time.values()))

    probability_of_time_in_next_step = dict()
    for prev_time in num_occurences_of_time_in_next_step:
        probability_of_time_in_next_step[prev_time] = dict()
        for time in num_occurences_of_time_in_next_step[prev_time]:
            probability_of_time_in_next_step[prev_time][time] = num_occurences_of_time_in_next_step[prev_time][time] / sum(list(num_occurences_of_time_in_next_step[prev_time].values()))

    probability_of_time_in_next_next_step = dict()
    for prev_prev_time in num_occurences_of_time_in_next_next_step:
        probability_of_time_in_next_next_step[prev_prev_time] = dict()
        for prev_time in num_occurences_of_time_in_next_next_step[prev_prev_time]:
            probability_of_time_in_next_next_step[prev_prev_time][prev_time] = dict()
            for time in num_occurences_of_time_in_next_next_step[prev_prev_time][prev_time]:
                probability_of_time_in_next_next_step[prev_prev_time][prev_time][time] = num_occurences_of_time_in_next_next_step[prev_prev_time][prev_time][time] / sum(list(num_occurences_of_time_in_next_next_step[prev_prev_time][prev_time].values()))

    #print(probability_of_time)
    save_object("probability/probability_of_time", probability_of_time)
    #print(probability_of_time_in_next_step)
    save_object("probability/probability_of_time_in_next_step", probability_of_time_in_next_step)
    #print(probability_of_time_in_next_next_step)
    save_object("probability/probability_of_time_in_next_next_step", probability_of_time_in_next_next_step)

probability_of_time = load_object("probability/probability_of_time") 
probability_of_time_in_next_step = load_object("probability/probability_of_time_in_next_step") 
probability_of_time_in_next_next_step = load_object("probability/probability_of_time_in_next_next_step")  
 
x = []
n = 10000
prev_time = 0
prev_prev_time = 0
for i in range(n):
    if i == 0:
        time = np.random.choice(list(probability_of_time.keys()),p=list(probability_of_time.values()))  
    if i == 1:
        if prev_time in probability_of_time_in_next_step:
            time = np.random.choice(list(probability_of_time_in_next_step[prev_time].keys()),p=list(probability_of_time_in_next_step[prev_time].values())) 
        else:
            break
    if i > 1:
        if prev_prev_time in probability_of_time_in_next_next_step and prev_time in probability_of_time_in_next_next_step[prev_prev_time]:
            time = np.random.choice(list(probability_of_time_in_next_next_step[prev_prev_time][prev_time].keys()),p=list(probability_of_time_in_next_next_step[prev_prev_time][prev_time].values())) 
        else:
            break
    prev_prev_time = prev_time
    prev_time = time
    x.append(time)

plt.plot(x)
plt.xlabel('Times',fontsize=20)
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
        times = list(file_with_ride["time"])
        times_processed = [process_time(time_new) for time_new in times] 
        time_int = [np.round(times_processed[time_index + 1] - times_processed[time_index], 10) for time_index in range(len(times_processed) - 1)] 
        for time_index in range(len(time_int)):
                if time_int[time_index] == 0:
                    time_int[time_index] = 10 ** -20
 
        x = []
        n = len(time_int)
        prev_time = 0
        prev_prev_time = 0
        for i in range(n):
            time = -1
            if i == 0:
                time = np.random.choice(list(probability_of_time.keys()),p=list(probability_of_time.values()))  
            if i == 1:
                if time_int[i - 1] in probability_of_time_in_next_step:
                    time = np.random.choice(list(probability_of_time_in_next_step[time_int[i - 1]].keys()),p=list(probability_of_time_in_next_step[time_int[i - 1]].values())) 
            if i > 1:
                if time_int[i - 2] in probability_of_time_in_next_next_step and time_int[i - 1] in probability_of_time_in_next_next_step[time_int[i - 2]]:
                    time = np.random.choice(list(probability_of_time_in_next_next_step[time_int[i - 2]][time_int[i - 1]].keys()),p=list(probability_of_time_in_next_next_step[time_int[i - 2]][time_int[i - 1]].values())) 
            x.append(time)

        match_score = 0 
        no_empty = 0
        delta_series = [] 
        for i in range(n):
            if x[i] == time_int[i]:
                match_score += 1
            if x[i] != -1:
                no_empty += 1
                delta_x = abs(time_int[i] - x[i])
                delta_series.append(delta_x)
                delta_series_total.append(delta_x)
        #print(match_score / n, match_score / no_empty, min(delta_series), np.quantile(delta_series, 0.25), np.quantile(delta_series, 0.5), np.quantile(delta_series, 0.75), max(delta_series), np.average(delta_series), np.std(delta_series), np.var(delta_series))
        total_guesses += n
        total_guesses_no_empty += no_empty
        total_match_score += match_score 
        #plt.hist(delta_series)
        #plt.show()
        all_x[subdir_name + "/cleaned_csv/" + some_file] = x
save_object("predicted/predicted_time", all_x)
print(total_match_score / total_guesses, total_match_score / total_guesses_no_empty, min(delta_series_total), np.quantile(delta_series_total, 0.25), np.quantile(delta_series_total, 0.5), np.quantile(delta_series_total, 0.75), max(delta_series_total), np.average(delta_series_total), np.std(delta_series_total), np.var(delta_series_total))

plt.hist(delta_series_total)
plt.show()
