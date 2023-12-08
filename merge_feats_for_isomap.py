
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
    var_iso = output
    std_iso = output
    varscaled_iso = output
    stdscaled_iso = output
    avg_iso = output
    min_iso = output
    max_iso = output
    range_iso = output
    for cluster in files_in_cluster:
        if len(files_in_cluster[cluster]) > 0:
            avg_values[cluster] = dict()
            var_iso += str(sdn) + "," + str(filename) + "," + str(cluster) + "," + str(len(files_in_cluster[cluster])) + ","
            std_iso += str(sdn) + "," + str(filename) + "," + str(cluster) + "," + str(len(files_in_cluster[cluster])) + ","
            varscaled_iso += str(sdn) + "," + str(filename) + "," + str(cluster) + "," + str(len(files_in_cluster[cluster])) + ","
            stdscaled_iso += str(sdn) + "," + str(filename) + "," + str(cluster) + "," + str(len(files_in_cluster[cluster])) + ","
            avg_iso += str(sdn) + "," + str(filename) + "," + str(cluster) + "," + str(len(files_in_cluster[cluster])) + ","
            min_iso += str(sdn) + "," + str(filename) + "," + str(cluster) + "," + str(len(files_in_cluster[cluster])) + ","
            max_iso += str(sdn) + "," + str(filename) + "," + str(cluster) + "," + str(len(files_in_cluster[cluster])) + ","
            range_iso += str(sdn) + "," + str(filename) + "," + str(cluster) + "," + str(len(files_in_cluster[cluster])) + ","
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
                var_iso += str(np.var(avg_values[cluster][key_name])) + ","
            var_iso = var_iso[:-1]
            var_iso += "\n"

            for key_name in avg_values[cluster]:                     
                std_iso += str(np.std(avg_values[cluster][key_name])) + ","
            std_iso = std_iso[:-1]
            std_iso += "\n"

            for key_name in avg_values[cluster]:                     
                varscaled_iso += str(np.var(avg_values[cluster][key_name]) / ((max(avg_values[cluster][key_name]) - min(avg_values[cluster][key_name])) ** 2)) + ","
            varscaled_iso = varscaled_iso[:-1]
            varscaled_iso += "\n"

            for key_name in avg_values[cluster]:                     
                stdscaled_iso += str(np.std(avg_values[cluster][key_name]) / (max(avg_values[cluster][key_name]) - min(avg_values[cluster][key_name]))) + ","
            stdscaled_iso = stdscaled_iso[:-1]
            stdscaled_iso += "\n"

            for key_name in avg_values[cluster]:                     
                avg_iso += str(sum(avg_values[cluster][key_name]) / len(avg_values[cluster][key_name])) + ","
            avg_iso = avg_iso[:-1]
            avg_iso += "\n"

            for key_name in avg_values[cluster]:                     
                min_iso += str(min(avg_values[cluster][key_name])) + ","
            min_iso = min_iso[:-1]
            min_iso += "\n"

            for key_name in avg_values[cluster]:                     
                max_iso += str(max(avg_values[cluster][key_name])) + ","
            max_iso = max_iso[:-1]
            max_iso += "\n"

            for key_name in avg_values[cluster]:                     
                range_iso += str(max(avg_values[cluster][key_name]) - min(avg_values[cluster][key_name])) + ","
            range_iso = range_iso[:-1]
            range_iso += "\n"
              
    return var_iso, std_iso, varscaled_iso, stdscaled_iso, avg_iso, min_iso, max_iso, range_iso
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
print("all_isomap")
for subdirname in os.listdir("all_isomap/"):
    print("all_isomap/" + subdirname)
    for filename in os.listdir("all_isomap/" + subdirname + "/filenames"):
        if not os.path.isdir("all_isomap/" + subdirname + "/output_isomap/"):
            os.makedirs("all_isomap/" + subdirname + "/output_isomap/")
        if os.path.isfile("all_isomap/" + subdirname + "/output_isomap/" + filename + ".csv"):
            continue
        print("all_isomap/" + subdirname + "/filenames/" + filename)
        output_iso = headercsv
        var_iso, std_iso, varscaled_iso, stdscaled_iso, avg_iso, min_iso, max_iso, range_iso = speed_cluster(load_object("all_isomap/" + subdirname + "/filenames/" + filename), subdirname, filename, output_iso)
        file_iso = open("all_isomap/" + subdirname + "/output_isomap/" + filename + "_var.csv", "w")
        file_iso.write(var_iso)
        file_iso.close()
        file_iso = open("all_isomap/" + subdirname + "/output_isomap/" + filename + "_std.csv", "w")
        file_iso.write(std_iso)
        file_iso.close() 
        file_iso = open("all_isomap/" + subdirname + "/output_isomap/" + filename + "_var_scaled.csv", "w")
        file_iso.write(varscaled_iso)
        file_iso.close()
        file_iso = open("all_isomap/" + subdirname + "/output_isomap/" + filename + "_std_scaled.csv", "w")
        file_iso.write(stdscaled_iso)
        file_iso.close() 
        file_iso = open("all_isomap/" + subdirname + "/output_isomap/" + filename + "_avg.csv", "w")
        file_iso.write(avg_iso)
        file_iso.close()
        file_iso = open("all_isomap/" + subdirname + "/output_isomap/" + filename + "_min.csv", "w")
        file_iso.write(min_iso)
        file_iso.close()
        file_iso = open("all_isomap/" + subdirname + "/output_isomap/" + filename + "_max.csv", "w")
        file_iso.write(max_iso)
        file_iso.close()
        file_iso = open("all_isomap/" + subdirname + "/output_isomap/" + filename + "_range.csv", "w")
        file_iso.write(range_iso)
        file_iso.close()