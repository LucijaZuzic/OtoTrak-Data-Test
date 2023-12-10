from utilities import *
  
header = ["start", "window_size", "vehicle", "ride"] 
properties = load_object("dict_for_clustering") 
ws = 20
sdna = "Vehicle_11"
sfl = list(properties[ws][sdna].keys())[0] 
strt = list(properties[ws][sdna][sfl].keys())[0]  
print("all_clus")
for subdirname in os.listdir("all_clus/"):
    print("all_clus/" + subdirname)
    for filename in os.listdir("all_clus/" + subdirname + "/filenames"):
        if os.path.isfile("all_clus/" + subdirname + "/output_clus/" + filename + "_var.csv"):
            continue
        if not os.path.isdir("all_clus/" + subdirname + "/output_clus/"):
            os.makedirs("all_clus/" + subdirname + "/output_clus/")
        if os.path.isfile("all_clus/" + subdirname + "/output_clus/" + filename + ".csv"):
            continue
        print("all_clus/" + subdirname + "/filenames/" + filename)
        output_clus = "subdir,file,cluster,size,"
        for prop in properties[ws][sdna][sfl][strt]:
            if skip_var(prop, subdirname):
                continue
            output_clus += str(prop) + ","
        output_clus = output_clus[:-1]
        output_clus += "\n"  
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