from utilities import *

dict_for_clustering = load_object("dict_for_clustering")
def compare_random_cluster(subdirname, files_in_cluster, nrow, ncol, filename):
    print(filename)
    for cluster in files_in_cluster:
        if len(files_in_cluster[cluster]) > 0: 
            print(cluster, len(files_in_cluster[cluster]))
            if nrow * ncol > len(files_in_cluster[cluster]):
                ncol = int(np.sqrt(len(files_in_cluster[cluster])))
                nrow = ncol
            indexes = set([x for x in range(len(files_in_cluster[cluster]))])
            while len(indexes) > nrow * ncol:
                index_remove = np.random.randint(0, len(files_in_cluster[cluster]))
                if index_remove in indexes:
                    indexes.remove(index_remove)
                    
            for index in indexes:
                name_file = files_in_cluster[cluster][index]["short_name"].split("/")
                subdir_name = name_file[0]
                some_file = name_file[1]
                ws = files_in_cluster[cluster][index]["window"]
                x = files_in_cluster[cluster][index]["start"]
                for entry in dict_for_clustering: 
                    prop = dict_for_clustering[ws][subdir_name][some_file][x][entry]
