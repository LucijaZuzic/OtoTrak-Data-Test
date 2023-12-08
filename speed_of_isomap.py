
from utilities import *

#open_feats_acceler_scaled = pd.read_csv("all_feats_acceler/all_feats_acceler_scaled.csv", index_col = False)
open_feats_acceler_scaled_max = pd.read_csv("all_feats_acceler/all_feats_acceler_scaled_to_max.csv", index_col = False)
#open_feats_acceler = pd.read_csv("all_feats_acceler/all_feats_acceler.csv", index_col = False)

header = ["start", "window_size", "vehicle", "ride"] 
def add_key(key, val, wheradd):
    if "monoto" not in key:
        if math.isnan(val):
            wheradd.append(0)
        else:
            wheradd.append(val) 
    else:
        if val == "I":
            wheradd.append(3)
        if val == "D":
            wheradd.append(2)
        if val == "NM":
            wheradd.append(1)
        if val == "NF":
            wheradd.append(0)
    return wheradd
def speed_cluster(files_in_cluster, sdn, filename, output): 
    avg_values = dict()
    for cluster in files_in_cluster:
        if len(files_in_cluster[cluster]) > 0:
            avg_values[cluster] = dict()
            output += str(sdn) + "," + str(filename) + "," + str(cluster) + "," + str(len(files_in_cluster[cluster])) + ","
            for index in range(len(files_in_cluster[cluster])): 
                name_file = files_in_cluster[cluster][index]["short_name"]
                vehicle_ride = name_file.split("/") 
                subdir_name = vehicle_ride[0] 

                #open_feats_scaled = pd.read_csv("all_feats/all_feats_scaled_" + subdir_name + ".csv", index_col = False)
                open_feats_scaled_max = pd.read_csv("all_feats/all_feats_scaled_to_max_" + subdir_name + ".csv", index_col = False)
                #open_feats = pd.read_csv("all_feats/all_feats_" + subdir_name + ".csv", index_col = False)

                only_number = vehicle_ride[1].replace("events_", "").replace(".csv", "")

                dsmax = dict()
                #dsc = dict()
                #dpp = dict()
                #d = dict()
                nsmax = dict()
                #nsc = dict()
                #npp = dict()
                #n = dict() 
                for size in os.listdir("rays"):   
                    start_path = "rays/" + str(size) + "/" + subdir_name + "/" + only_number
                    dsmax[size] = pd.read_csv(start_path + "/all_distances_scaled_to_max_trajs.csv", index_col = False)
                    #dsc[size] = pd.read_csv(start_path + "/all_distances_scaled_trajs.csv", index_col = False)
                    #dpp[size] = pd.read_csv(start_path + "/all_distances_preprocessed_trajs.csv", index_col = False)
                    #d[size] = pd.read_csv(start_path + "/all_distances_trajs.csv", index_col = False)
                    nsmax[size] = load_object(start_path + "/all_nums_scaled_to_max_trajs")
                    #nsc[size] = load_object(start_path + "/all_nums_scaled_trajs")
                    #npp[size] = load_object(start_path + "/all_nums_preprocessed_trajs")
                    #n[size] = load_object(start_path + "/all_nums_trajs") 

                window_size = files_in_cluster[cluster][index]["window"]
                x = files_in_cluster[cluster][index]["start"] 

                for index in range(len(open_feats_scaled_max["start"])):
                    if str(open_feats_scaled_max["start"][index]) != str(x):
                        continue
                    if str(open_feats_scaled_max["window_size"][index]) != str(window_size):
                        continue
                    if str(open_feats_scaled_max["vehicle"][index]) != str(subdir_name):
                        continue
                    if str(open_feats_scaled_max["ride"][index]) != str(only_number):
                        continue   
                    for key_name in open_feats_scaled_max.head(): 
                        if key_name in header:
                            continue 
                        if "diff" in key_name:
                            continue
                        if "Unnamed" in key_name:
                            continue
                        if key_name not in avg_values[cluster]:
                            avg_values[cluster][key_name] = []
                        avg_values[cluster][key_name] = add_key(key_name, open_feats_scaled_max[key_name][index], avg_values[cluster][key_name]) 
                    
                for size in os.listdir("rays"):   
                    for index in range(len(dsmax[size]["start"])):
                        if str(dsmax[size]["start"][index]) != str(x):
                            continue
                        if str(dsmax[size]["window_size"][index]) != str(window_size):
                            continue
                        if str(dsmax[size]["vehicle"][index]) != str(subdir_name):
                            continue
                        if str(dsmax[size]["ride"][index]) != str(only_number):
                            continue   
                        for key_name in dsmax[size].head(): 
                            if key_name in header:
                                continue
                            if "offset" not in key_name:
                                continue
                            if "only offset" in key_name:
                                continue
                            if str(size) + "_d_" + key_name not in avg_values[cluster]:
                                avg_values[cluster][str(size) + "_d_" + key_name] = []
                            avg_values[cluster][str(size) + "_d_" + key_name] = add_key(key_name, dsmax[size][key_name][index], avg_values[cluster][str(size) + "_d_" + key_name])  
                            
                    if x in nsmax[size]:
                        for key_name in nsmax[size][x]:
                            if key_name != "offset":  
                                continue
                            if str(size) + "_n_" + key_name not in avg_values[cluster]:
                                avg_values[cluster][str(size) + "_n_" + key_name] = []
                            avg_values[cluster][str(size) + "_n_" + key_name] = add_key(key_name, nsmax[size][x][key_name], avg_values[cluster][str(size) + "_n_" + key_name])  

                for index in range(len(open_feats_acceler_scaled_max["start"])):
                    if str(open_feats_acceler_scaled_max["start"][index]) != str(x):
                        continue
                    if str(open_feats_acceler_scaled_max["window_size"][index]) != str(window_size):
                        continue
                    if str(open_feats_acceler_scaled_max["vehicle"][index]) != str(subdir_name):
                        continue
                    if str(open_feats_acceler_scaled_max["ride"][index]) != str(only_number):
                        continue    
                    for key_name in open_feats_acceler_scaled_max.head(): 
                        if key_name in header:
                            continue 
                        if "Unnamed" in key_name:
                            continue
                        if key_name not in avg_values[cluster]:
                            avg_values[cluster][key_name] = [] 
                        avg_values[cluster][key_name] = add_key(key_name, open_feats_acceler_scaled_max[key_name][index], avg_values[cluster][key_name])  

            for key_name in avg_values[cluster]:                     
                output += str(sum(avg_values[cluster][key_name]) / len(avg_values[cluster][key_name])) + ","
            output = output[:-1]
            output += "\n"
    return output
headercsv = "subdir,file,cluster,size,"
open_feats_scaled_maxtmp = pd.read_csv("all_feats/all_feats_scaled_to_max_Vehicle_11.csv", index_col = False)
for key_name in open_feats_scaled_maxtmp.head(): 
    if key_name in header:
        continue 
    if "diff" in key_name:
        continue
    if "Unnamed" in key_name:
        continue
    headercsv += str(key_name) + ","
dsmaxtmp = dict() 
nsmaxtmp = dict() 
for size in os.listdir("rays"):   
    start_path = "rays/" + str(size) + "/Vehicle_11/8354807"
    dsmaxtmp[size] = pd.read_csv(start_path + "/all_distances_scaled_to_max_trajs.csv", index_col = False) 
    nsmaxtmp[size] = load_object(start_path + "/all_nums_scaled_to_max_trajs")   
    for key_name in dsmaxtmp[size].head(): 
        if key_name in header:
            continue
        if "offset" not in key_name:
            continue
        if "only offset" in key_name:
            continue
        headercsv += str(size) + "_d_" + str(key_name) + "," 
    for key_name in nsmaxtmp[size][0]:
        if key_name != "offset":
            continue
        headercsv += str(size) + "_n_" + str(key_name) + ","
for key_name in open_feats_acceler_scaled_max.head(): 
    if key_name in header:
        continue 
    if "Unnamed" in key_name:
        continue 
    headercsv += str(key_name) + ","
headercsv = headercsv[:-1]
headercsv += "\n"  
print("all_isomap")
for subdirname in os.listdir("all_isomap/"):
    print("all_isomap/" + subdirname)
    for filename in os.listdir("all_isomap/" + subdirname + "/filenames"):
        print("all_isomap/" + subdirname + "/filenames/" + filename)
        output_isomap = headercsv
        output_isomap = speed_cluster(load_object("all_isomap/" + subdirname + "/filenames/" + filename), subdirname, filename, output_isomap)
        if not os.path.isdir("all_isomap/" + subdirname + "/output_isomap/"):
            os.path.makedirs("all_isomap/" + subdirname + "/output_isomap/")
        file_isomap = open("all_isomap/" + subdirname + "/output_isomap/" + filename + ".csv")
        file_isomap.write(output_isomap)
        file_isomap.close()