
from utilities import *

#open_feats_acceler_scaled = pd.read_csv("all_feats_acceler/all_feats_acceler_scaled.csv", index_col = False)
open_feats_acceler_scaled_max = pd.read_csv("all_feats_acceler/all_feats_acceler_scaled_to_max.csv", index_col = False)
#open_feats_acceler = pd.read_csv("all_feats_acceler/all_feats_acceler.csv", index_col = False)

#open_feats_heading_scaled = pd.read_csv("all_feats_heading/all_feats_heading_scaled.csv", index_col = False)
open_feats_heading_scaled_max = pd.read_csv("all_feats_heading/all_feats_heading_scaled_to_max.csv", index_col = False)
#open_feats_heading = pd.read_csv("all_feats_heading/all_feats_heading.csv", index_col = False)


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
    var_clus = output
    std_clus = output
    varscaled_clus = output
    stdscaled_clus = output
    avg_clus = output
    min_clus = output
    max_clus = output
    range_clus = output
    for cluster in files_in_cluster:
        if len(files_in_cluster[cluster]) > 0:
            avg_values[cluster] = dict()
            var_clus += str(sdn) + "," + str(filename) + "," + str(cluster) + "," + str(len(files_in_cluster[cluster])) + ","
            std_clus += str(sdn) + "," + str(filename) + "," + str(cluster) + "," + str(len(files_in_cluster[cluster])) + ","
            varscaled_clus += str(sdn) + "," + str(filename) + "," + str(cluster) + "," + str(len(files_in_cluster[cluster])) + ","
            stdscaled_clus += str(sdn) + "," + str(filename) + "," + str(cluster) + "," + str(len(files_in_cluster[cluster])) + ","
            avg_clus += str(sdn) + "," + str(filename) + "," + str(cluster) + "," + str(len(files_in_cluster[cluster])) + ","
            min_clus += str(sdn) + "," + str(filename) + "," + str(cluster) + "," + str(len(files_in_cluster[cluster])) + ","
            max_clus += str(sdn) + "," + str(filename) + "," + str(cluster) + "," + str(len(files_in_cluster[cluster])) + ","
            range_clus += str(sdn) + "," + str(filename) + "," + str(cluster) + "," + str(len(files_in_cluster[cluster])) + ","
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
                        
                for index in range(len(open_feats_heading_scaled_max["start"])):
                    if str(open_feats_heading_scaled_max["start"][index]) != str(x):
                        continue
                    if str(open_feats_heading_scaled_max["window_size"][index]) != str(window_size):
                        continue
                    if str(open_feats_heading_scaled_max["vehicle"][index]) != str(subdir_name):
                        continue
                    if str(open_feats_heading_scaled_max["ride"][index]) != str(only_number):
                        continue    
                    for key_name in open_feats_heading_scaled_max.head(): 
                        if key_name in header:
                            continue 
                        if "Unnamed" in key_name:
                            continue
                        if key_name not in avg_values[cluster]:
                            avg_values[cluster][key_name] = [] 
                        avg_values[cluster][key_name] = add_key(key_name, open_feats_heading_scaled_max[key_name][index], avg_values[cluster][key_name])  

            for key_name in avg_values[cluster]:                     
                var_clus += str(np.var(avg_values[cluster][key_name])) + ","
            var_clus = var_clus[:-1]
            var_clus += "\n"

            for key_name in avg_values[cluster]:                     
                std_clus += str(np.std(avg_values[cluster][key_name])) + ","
            std_clus = std_clus[:-1]
            std_clus += "\n"

            for key_name in avg_values[cluster]:                     
                varscaled_clus += str(np.var(avg_values[cluster][key_name]) / ((max(avg_values[cluster][key_name]) - min(avg_values[cluster][key_name])) ** 2)) + ","
            varscaled_clus = varscaled_clus[:-1]
            varscaled_clus += "\n"

            for key_name in avg_values[cluster]:                     
                stdscaled_clus += str(np.std(avg_values[cluster][key_name]) / (max(avg_values[cluster][key_name]) - min(avg_values[cluster][key_name]))) + ","
            stdscaled_clus = stdscaled_clus[:-1]
            stdscaled_clus += "\n"

            for key_name in avg_values[cluster]:                     
                avg_clus += str(sum(avg_values[cluster][key_name]) / len(avg_values[cluster][key_name])) + ","
            avg_clus = avg_clus[:-1]
            avg_clus += "\n"

            for key_name in avg_values[cluster]:                     
                min_clus += str(min(avg_values[cluster][key_name])) + ","
            min_clus = min_clus[:-1]
            min_clus += "\n"

            for key_name in avg_values[cluster]:                     
                max_clus += str(max(avg_values[cluster][key_name])) + ","
            max_clus = max_clus[:-1]
            max_clus += "\n"

            for key_name in avg_values[cluster]:                     
                range_clus += str(max(avg_values[cluster][key_name]) - min(avg_values[cluster][key_name])) + ","
            range_clus = range_clus[:-1]
            range_clus += "\n"
              
    return var_clus, std_clus, varscaled_clus, stdscaled_clus, avg_clus, min_clus, max_clus, range_clus
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
for key_name in open_feats_heading_scaled_max.head(): 
    if key_name in header:
        continue 
    if "Unnamed" in key_name:
        continue 
    headercsv += str(key_name) + ","
headercsv = headercsv[:-1]
headercsv += "\n" 
print("all_clus")
for subdirname in os.listdir("all_clus/"):
    print("all_clus/" + subdirname)
    for filename in os.listdir("all_clus/" + subdirname + "/filenames"):
        if not os.path.isdir("all_clus/" + subdirname + "/output_clus/"):
            os.makedirs("all_clus/" + subdirname + "/output_clus/")
        if os.path.isfile("all_clus/" + subdirname + "/output_clus/" + filename + ".csv"):
            continue
        print("all_clus/" + subdirname + "/filenames/" + filename)
        output_clus = headercsv
        var_clus, std_clus, varscaled_clus, stdscaled_clus, avg_clus, min_clus, max_clus, range_clus = speed_cluster(load_object("all_clus/" + subdirname + "/filenames/" + filename), subdirname, filename, output_clus)
        file_clus = open("all_clus/" + subdirname + "/output_clus/" + filename + "_var.csv", "w")
        file_clus.write(var_clus)
        file_clus.close()
        file_clus = open("all_clus/" + subdirname + "/output_clus/" + filename + "_std.csv", "w")
        file_clus.write(std_clus)
        file_clus.close() 
        file_clus = open("all_clus/" + subdirname + "/output_clus/" + filename + "_var_scaled.csv", "w")
        file_clus.write(varscaled_clus)
        file_clus.close()
        file_clus = open("all_clus/" + subdirname + "/output_clus/" + filename + "_std_scaled.csv", "w")
        file_clus.write(stdscaled_clus)
        file_clus.close() 
        file_clus = open("all_clus/" + subdirname + "/output_clus/" + filename + "_avg.csv", "w")
        file_clus.write(avg_clus)
        file_clus.close()
        file_clus = open("all_clus/" + subdirname + "/output_clus/" + filename + "_min.csv", "w")
        file_clus.write(min_clus)
        file_clus.close()
        file_clus = open("all_clus/" + subdirname + "/output_clus/" + filename + "_max.csv", "w")
        file_clus.write(max_clus)
        file_clus.close()
        file_clus = open("all_clus/" + subdirname + "/output_clus/" + filename + "_range.csv", "w")
        file_clus.write(range_clus)
        file_clus.close()