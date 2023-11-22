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
    if os.path.isfile(subdir_name + "/bad_rides_filenames"):
        bad_rides_filenames = load_object(subdir_name + "/bad_rides_filenames")

    bad_rides_filenames2 = set() 
    if os.path.isfile("../OtoTrak-Similarity/"+ subdir_name + "/bad_rides_filenames"):
        bad_rides_filenames2 = load_object("../OtoTrak-Similarity/"+ subdir_name + "/bad_rides_filenames")
         
    print(len(bad_rides_filenames), len(bad_rides_filenames2), subdir_name)