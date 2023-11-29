from utilities import *
    
window_size = 20
 
size = 4
dotsx_original, dotsy_original = make_rays(size)

deg = 5
maxoffset = 0.005
step_size = window_size
#step_size = 1
max_trajs = 100
name_extension = "_window_" + str(window_size) + "_step_" + str(step_size) + "_segments_" + str(max_trajs)

all_subdirs = os.listdir()  
 
scale_val = [True, True, False, False]
offset_val = [False, True, False, True]
name_val = ["scale", "offset", "no scale", "only offset"]  
 
def count_in_matrix(matrix_inter):
    n = 0
    tot = 0
    for r in matrix_inter:
        for c in r:
            for t in c:
                if t != ("Nan", "Nan"):
                    n += 1
                tot += 1
    return n / tot

for size in range(4, 40, 4):
    print(size)
    for subdir_name in all_subdirs:
    
        if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
            continue
        print(subdir_name)    
        
        all_files = os.listdir(subdir_name + "/cleaned_csv/") 
        bad_rides_filenames = set()
        if os.path.isfile(subdir_name + "/bad_rides_filenames"):
            bad_rides_filenames = load_object(subdir_name + "/bad_rides_filenames")
        gap_rides_filenames = set()
        if os.path.isfile(subdir_name + "/gap_rides_filenames"):
            gap_rides_filenames = load_object(subdir_name + "/gap_rides_filenames")
            
        for some_file in all_files:  
            if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames:
                #print("Skipped ride", some_file)
                continue
            #print("Used ride", some_file)
             
            all_distances_trajs = dict()
            all_distances_preprocessed_trajs = dict()
            all_distances_scaled_trajs = dict()
            all_distances_scaled_to_max_trajs = dict() 

            only_number = some_file.replace(".csv", "").replace("events_", "")
            start_path = "rays/" + str(size) + "/" + subdir_name + "/" + only_number
            all_distances_trajs_file = pd.read_csv(start_path + "/all_distances_trajs.csv", index_col=False)
            all_distances_preprocessed_trajs_file = pd.read_csv(start_path + "/all_distances_preprocessed_trajs.csv", index_col=False)
            all_distances_scaled_trajs_file = pd.read_csv(start_path + "/all_distances_scaled_trajs.csv", index_col=False)
            all_distances_scaled_to_max_trajs_file = pd.read_csv(start_path + "/all_distances_scaled_to_max_trajs.csv", index_col=False)
 
            file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
            longitudes = list(file_with_ride["fields_longitude"])
            latitudes = list(file_with_ride["fields_latitude"]) 
            times = list(file_with_ride["time"])   
            for x in range(0, len(longitudes) - window_size + 1, step_size):
                all_distances_trajs[x] = dict()
                all_distances_preprocessed_trajs[x] = dict()
                all_distances_scaled_trajs[x] = dict()
                all_distances_scaled_to_max_trajs[x] = dict() 
                for value_for_dict in range(len(name_val)): 
                    for index in range(len(all_distances_trajs_file[name_val[value_for_dict]])):
                        all_distances_trajs[x][name_val[value_for_dict]] = (all_distances_trajs_file[name_val[value_for_dict]][index] * window_size / (window_size - 1), all_distances_trajs_file[name_val[value_for_dict] + " x"][index] * window_size / (window_size - 1) , all_distances_trajs_file[name_val[value_for_dict] + " y"][index] * window_size / (window_size - 1))  
                    for index in range(len(all_distances_preprocessed_trajs_file[name_val[value_for_dict]])):
                        all_distances_preprocessed_trajs[x][name_val[value_for_dict]] = (all_distances_preprocessed_trajs_file[name_val[value_for_dict]][index] * window_size / (window_size - 1), all_distances_preprocessed_trajs_file[name_val[value_for_dict] + " x"][index] * window_size / (window_size - 1) , all_distances_preprocessed_trajs_file[name_val[value_for_dict] + " y"][index] * window_size / (window_size - 1))  
                    for index in range(len(all_distances_scaled_trajs_file[name_val[value_for_dict]])):
                        all_distances_scaled_trajs[x][name_val[value_for_dict]] = (all_distances_scaled_trajs_file[name_val[value_for_dict]][index] * window_size / (window_size - 1), all_distances_scaled_trajs_file[name_val[value_for_dict] + " x"][index] * window_size / (window_size - 1) , all_distances_scaled_trajs_file[name_val[value_for_dict] + " y"][index] * window_size / (window_size - 1))  
                    for index in range(len(all_distances_scaled_to_max_trajs_file[name_val[value_for_dict]])):
                        all_distances_scaled_to_max_trajs[x][name_val[value_for_dict]] = (all_distances_scaled_to_max_trajs_file[name_val[value_for_dict]][index] * window_size / (window_size - 1), all_distances_scaled_to_max_trajs_file[name_val[value_for_dict] + " x"][index] * window_size / (window_size - 1) , all_distances_scaled_to_max_trajs_file[name_val[value_for_dict] + " y"][index] * window_size / (window_size - 1))  
 
            #process_csv_ray(window_size, subdir_name, int(only_number), all_distances_trajs, start_path + "/all_distances_trajs.csv", True)
            #process_csv_ray(window_size, subdir_name, int(only_number), all_distances_preprocessed_trajs, start_path + "/all_distances_preprocessed_trajs.csv", True)
            #process_csv_ray(window_size, subdir_name, int(only_number), all_distances_scaled_trajs, start_path + "/all_distances_scaled_trajs.csv", True)
            #process_csv_ray(window_size, subdir_name, int(only_number), all_distances_scaled_to_max_trajs, start_path + "/all_distances_scaled_to_max_trajs.csv", True)