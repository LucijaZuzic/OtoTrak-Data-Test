import os
import pickle
from sklearn.model_selection import train_test_split

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
num_occurences_of_direction = dict()
num_occurences_of_direction_diff = dict()
num_occurences_of_direction_in_next_step = dict()
num_occurences_of_direction_in_next_next_step = dict()

for subdir_name in all_subdirs: 
    if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
        continue 
    
    all_rides_cleaned = os.listdir(subdir_name + "/cleaned_csv/")
      
    all_files = os.listdir(subdir_name + "/cleaned_csv/") 
    bad_rides_filenames = set()
    good_rides = dict()  
    if os.path.isfile(subdir_name + "/bad_rides_filenames"):
        bad_rides_filenames = load_object(subdir_name + "/bad_rides_filenames")
        
    for some_file in all_files:  
        if some_file not in bad_rides_filenames:
            good_rides[some_file] = 0
    
    if len(good_rides) > 0:  
        X_train, X_test, y_train, y_test = train_test_split(list(good_rides.keys()), list(good_rides.values()), test_size=0.33, random_state=42)
        save_object(subdir_name + "/test_rides", X_test)
        save_object(subdir_name + "/train_rides", X_train)