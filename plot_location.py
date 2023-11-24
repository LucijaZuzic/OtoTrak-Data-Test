from utilities import *

all_subdirs = os.listdir() 
for subdir_name in all_subdirs:
    if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
        continue
    print(subdir_name)
      
    all_files = os.listdir(subdir_name + "/cleaned_csv/") 
    bad_rides_filenames = dict()
    if os.path.isfile(subdir_name + "/bad_rides_filenames"):
        bad_rides_filenames = load_object(subdir_name + "/bad_rides_filenames")
    gap_rides_filenames = dict()
    if os.path.isfile(subdir_name + "/gap_rides_filenames"):
        gap_rides_filenames = load_object(subdir_name + "/gap_rides_filenames")
    for some_file in all_files:  
        if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames:
            #print("Skipped ride", some_file)
            continue
        #print("Used ride", some_file)
    
        file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
        longitudes = list(file_with_ride["fields_longitude"])
        latitudes = list(file_with_ride["fields_latitude"])  
        plt.plot(longitudes, latitudes) 
        plt.title(subdir_name + " " + some_file.replace(".csv", ""))
        plt.xticks([min(longitudes), max(longitudes)], [np.round(min(longitudes), 3), np.round(max(longitudes), 3)]) 
        plt.yticks([min(latitudes), max(latitudes)], [np.round(min(latitudes), 3), np.round(max(latitudes), 3)])  
        plt.show()