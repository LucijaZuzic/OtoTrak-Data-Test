from utilities import *
  
header = ["start", "window_size", "vehicle", "ride"] 
properties = load_object("dict_for_clustering") 
ws = 20
sdna = "Vehicle_11"
sfl = list(properties[ws][sdna].keys())[0] 
strt = list(properties[ws][sdna][sfl].keys())[0] 
 
def make_averages_list(part1, part2, subdirnames = [], filenames = [], subdirnames_skip = [], filenames_skip = []):  
    for subdirname in os.listdir(part1):
        skipping = False
        for s in subdirnames:
            if s not in subdirname:
                skipping = True
                break
        for s in subdirnames_skip:
            if s in subdirname:
                skipping = True
                break
        if skipping:
            continue
        print(part1 + subdirname)
        for filename in os.listdir(part1 + subdirname + "/filenames"):
            skipping = False
            for f in filenames:
                if f not in filename:
                    skipping = True
                    break
            for f in filenames_skip:
                if f in filename:
                    skipping = True
                    break
            if skipping:
                continue
            if os.path.isfile(part1 + subdirname + part2 + filename + "_var.csv"):
                continue
            if not os.path.isdir(part1 + subdirname + part2):
                os.makedirs(part1 + subdirname + part2)
            if os.path.isfile(part1 + subdirname + part2 + filename + ".csv"):
                continue
            print(part1 + subdirname + "/filenames/" + filename)
            output_clus = "subdir,file,cluster,size,"
            for prop in properties[ws][sdna][sfl][strt]:
                if skip_var(prop, subdirname):
                    continue
                output_clus += str(prop) + ","
            output_clus = output_clus[:-1]
            output_clus += "\n"  
            var_clus, std_clus, varscaled_clus, stdscaled_clus, avg_clus, min_clus, max_clus, range_clus = speed_cluster(load_object(part1 + subdirname + "/filenames/" + filename), subdirname, filename, output_clus)
            file_clus = open(part1 + subdirname + part2 + filename + "_var.csv", "w")
            file_clus.write(var_clus)
            file_clus.close()
            file_clus = open(part1 + subdirname + part2 + filename + "_std.csv", "w")
            file_clus.write(std_clus)
            file_clus.close() 
            file_clus = open(part1 + subdirname + part2 + filename + "_var_scaled.csv", "w")
            file_clus.write(varscaled_clus)
            file_clus.close()
            file_clus = open(part1 + subdirname + part2 + filename + "_std_scaled.csv", "w")
            file_clus.write(stdscaled_clus)
            file_clus.close() 
            file_clus = open(part1 + subdirname + part2 + filename + "_avg.csv", "w")
            file_clus.write(avg_clus)
            file_clus.close()
            file_clus = open(part1 + subdirname + part2 + filename + "_min.csv", "w")
            file_clus.write(min_clus)
            file_clus.close()
            file_clus = open(part1 + subdirname + part2 + filename + "_max.csv", "w")
            file_clus.write(max_clus)
            file_clus.close()
            file_clus = open(part1 + subdirname + part2 + filename + "_range.csv", "w")
            file_clus.write(range_clus)
            file_clus.close()

subdirnames = ["all", "no_same", "no_xy", "heading", "acceler"]
filenames = ["KMeans"]
subdirnames_skip = ["poly", "flags"]
filenames_skip = ["_train"] 

subdirnames = []
filenames = []
subdirnames_skip = []
filenames_skip = ["_train"] 

part1 = "all_clus/"
part2 = "/output_clus/"
make_averages_list(part1, part2, subdirnames, filenames, subdirnames_skip, filenames_skip)
part1 = "all_isomap/"
part2 = "/output_iso/"
make_averages_list(part1, part2, subdirnames, filenames, subdirnames_skip, filenames_skip)