
from utilities import *

#open_feats_acceler_scaled = pd.read_csv("all_feats_acceler/all_feats_acceler_scaled.csv", index_col = False)
open_feats_acceler_scaled_max = pd.read_csv("all_feats_acceler/all_feats_acceler_scaled_to_max.csv", index_col = False)
#open_feats_acceler = pd.read_csv("all_feats_acceler/all_feats_acceler.csv", index_col = False)

header = ["start", "window_size", "vehicle", "ride"] 

def speed_cluster(files_in_cluster): 
    avg_values = dict()
    for cluster in files_in_cluster:
        if len(files_in_cluster[cluster]) > 0:
            avg_values[cluster] = dict()
            print(cluster, len(files_in_cluster[cluster]))
            for index in range(len(files_in_cluster[cluster])): 
                name_file = files_in_cluster[cluster][index]["short_name"]
                vehicle_ride = name_file.split("/") 
                subdir_name = vehicle_ride[0]
                only_number = vehicle_ride[1].replace("events_", "").replace(".csv", "")
                window_size = files_in_cluster[cluster][index]["window"]
                x = files_in_cluster[cluster][index]["start"] 
                for index in range(len(open_feats_acceler_scaled_max["start"])):
                    if str(open_feats_acceler_scaled_max["start"][index]) != str(x):
                        continue
                    if str(open_feats_acceler_scaled_max["window_size"][index]) != str(window_size):
                        continue
                    if str(open_feats_acceler_scaled_max["vehicle"][index]) != str(subdir_name):
                        continue
                    if str(open_feats_acceler_scaled_max["ride"][index]) != str(only_number):
                        continue   
                    #print("Located feats")
                    for key_name in open_feats_acceler_scaled_max.head(): 
                        if key_name in header:
                            continue 
                        if "Unnamed" in key_name:
                            continue
                        if key_name not in avg_values[cluster]:
                            avg_values[cluster][key_name] = []
                        avg_values[cluster][key_name].append(open_feats_acceler_scaled_max[key_name][index])
            for key_name in avg_values[cluster]:                    
                print(key_name, sum(avg_values[cluster][key_name]) / len(avg_values[cluster][key_name]))
print("all_clus")                
for subdirname in os.listdir("all_clus/"):
    print("all_clus/" + subdirname)
    for filename in os.listdir("all_clus/" + subdirname + "/filenames"):
        print("all_clus/" + subdirname + "/filenames/" + filename)
        speed_cluster(load_object("all_clus/" + subdirname + "/filenames/" + filename))
print("all_isomap")
for subdirname in os.listdir("all_isomap/"):
    print("all_isomap/" + subdirname)
    for filename in os.listdir("all_isomap/" + subdirname + "/filenames"):
        print("all_isomap/" + subdirname + "/filenames/" + filename)
        speed_cluster(load_object("all_isomap/" + subdirname + "/filenames/" + filename))