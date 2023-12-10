from utilities import *

header = ["start", "window_size", "vehicle", "ride"]
properties = load_object("dict_for_clustering") 
ws = 20
sdna = "Vehicle_11"
sfl = list(properties[ws][sdna].keys())[0] 
strt = list(properties[ws][sdna][sfl].keys())[0]
print("all_isomap")
for subdirname in os.listdir("all_isomap/"):
    print("all_isomap/" + subdirname)
    for filename in os.listdir("all_isomap/" + subdirname + "/filenames"):
        if os.path.isfile("all_isomap/" + subdirname + "/output_iso/" + filename + "_var.csv"):
            continue
        if not os.path.isdir("all_isomap/" + subdirname + "/output_iso/"):
            os.makedirs("all_isomap/" + subdirname + "/output_iso/")
        if os.path.isfile("all_isomap/" + subdirname + "/output_iso/" + filename + ".csv"):
            continue
        print("all_isomap/" + subdirname + "/filenames/" + filename)
        output_iso = "subdir,file,cluster,size,"
        for prop in properties[ws][sdna][sfl][strt]:
            if skip_var(prop, subdirname):
                continue
            output_iso += str(prop) + ","
        output_iso = output_iso[:-1]
        output_iso += "\n"  
        var_iso, std_iso, varscaled_iso, stdscaled_iso, avg_iso, min_iso, max_iso, range_iso = speed_cluster(load_object("all_isomap/" + subdirname + "/filenames/" + filename), subdirname, filename, output_iso)
        file_iso = open("all_isomap/" + subdirname + "/output_iso/" + filename + "_var.csv", "w")
        file_iso.write(var_iso)
        file_iso.close()
        file_iso = open("all_isomap/" + subdirname + "/output_iso/" + filename + "_std.csv", "w")
        file_iso.write(std_iso)
        file_iso.close() 
        file_iso = open("all_isomap/" + subdirname + "/output_iso/" + filename + "_var_scaled.csv", "w")
        file_iso.write(varscaled_iso)
        file_iso.close()
        file_iso = open("all_isomap/" + subdirname + "/output_iso/" + filename + "_std_scaled.csv", "w")
        file_iso.write(stdscaled_iso)
        file_iso.close() 
        file_iso = open("all_isomap/" + subdirname + "/output_iso/" + filename + "_avg.csv", "w")
        file_iso.write(avg_iso)
        file_iso.close()
        file_iso = open("all_isomap/" + subdirname + "/output_iso/" + filename + "_min.csv", "w")
        file_iso.write(min_iso)
        file_iso.close()
        file_iso = open("all_isomap/" + subdirname + "/output_iso/" + filename + "_max.csv", "w")
        file_iso.write(max_iso)
        file_iso.close()
        file_iso = open("all_isomap/" + subdirname + "/output_iso/" + filename + "_range.csv", "w")
        file_iso.write(range_iso)
        file_iso.close()