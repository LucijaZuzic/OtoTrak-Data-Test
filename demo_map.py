from utilities import *  
import subprocess
 
all_subdirs = os.listdir()

location_vehicles = load_object("location_vehicles")
vehicle_location = load_object("vehicle_location")
min_long_loc = dict()
max_long_loc = dict()
max_lat_loc = dict()
min_lat_loc = dict()
min_long_vehicle = dict()
max_long_vehicle = dict()
max_lat_vehicle = dict()
min_lat_vehicle = dict()
min_long_ride = dict()
max_long_ride = dict()
max_lat_ride = dict()
min_lat_ride = dict()
  
for loc in location_vehicles:
    print(loc)
    min_long_loc[loc] = 1000000
    max_long_loc[loc] = -1000000
    min_lat_loc[loc] = 1000000
    max_lat_loc[loc] = -1000000
    for subdir_name in location_vehicles[loc]: 
        print(subdir_name)
        min_long_vehicle[subdir_name] = 1000000
        max_long_vehicle[subdir_name] = -1000000
        min_lat_vehicle[subdir_name] = 1000000
        max_lat_vehicle[subdir_name] = -1000000
        if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
            continue 
        all_files = os.listdir(subdir_name + "/cleaned_csv/") 
        for some_file in all_files:  
            file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
            min_long_ride[some_file] = 1000000
            max_long_ride[some_file] = -1000000
            min_lat_ride[some_file] = 1000000
            max_lat_ride[some_file] = -1000000
            longitudes = list(file_with_ride["fields_longitude"])
            latitudes = list(file_with_ride["fields_latitude"]) 

            min_long_loc[loc] = min(min_long_loc[loc], min(longitudes))
            max_long_loc[loc] = max(max_long_loc[loc], max(longitudes))
            min_lat_loc[loc] = min(min_lat_loc[loc], min(latitudes))
            max_lat_loc[loc] = max(max_lat_loc[loc], max(latitudes))

            min_long_vehicle[subdir_name] = min(min_long_vehicle[subdir_name], min(longitudes))
            max_long_vehicle[subdir_name] = max(max_long_vehicle[subdir_name], max(longitudes))
            min_lat_vehicle[subdir_name] = min(min_lat_vehicle[subdir_name], min(latitudes))
            max_lat_vehicle[subdir_name] = max(max_lat_vehicle[subdir_name], max(latitudes))

            min_long_ride[some_file] = min(min_long_ride[some_file], min(longitudes))
            max_long_ride[some_file] = max(max_long_ride[some_file], max(longitudes))
            min_lat_ride[some_file] = min(min_lat_ride[some_file], min(latitudes))
            max_lat_ride[some_file] = max(max_lat_ride[some_file], max(latitudes))

            if not os.path.isdir("traj_GPS/" + subdir_name):
                os.makedirs("traj_GPS/" + subdir_name)  
            
    print(min_long_loc[loc], max_long_loc[loc], min_lat_loc[loc], max_lat_loc[loc])
    
if not os.path.isdir("location_data"):
    os.makedirs("location_data") 
    
save_object("location_data/min_long_loc", min_long_loc)
save_object("location_data/max_long_loc", max_long_loc)
save_object("location_data/min_lat_loc", min_lat_loc)
save_object("location_data/max_lat_loc", max_lat_loc)

save_object("location_data/min_long_vehicle", min_long_vehicle)
save_object("location_data/max_long_vehicle", max_long_vehicle)
save_object("location_data/min_lat_vehicle", min_lat_vehicle)
save_object("location_data/max_lat_vehicle", max_lat_vehicle)

save_object("location_data/min_long_ride", min_long_ride)
save_object("location_data/max_long_ride", max_long_ride)
save_object("location_data/min_lat_ride", min_lat_ride)
save_object("location_data/max_lat_ride", max_lat_ride)