from utilities import *

dict_for_clustering = load_object("dict_for_clustering")

def compare_random_cluster(files_in_cluster, nsamples):
    props = dict()
 
    for cluster in files_in_cluster:
        props[cluster] = dict()
        indexes = set([x for x in range(len(files_in_cluster[cluster]))])
        while len(indexes) > min(nsamples, len(files_in_cluster[cluster])):
            index_remove = np.random.randint(0, len(files_in_cluster[cluster]))
            if index_remove in indexes:
                indexes.remove(index_remove)
        for index in indexes:
            name_file = files_in_cluster[cluster][index]["short_name"].split("/")
            subdir_name = name_file[0]
            some_file = name_file[1]
            ws = files_in_cluster[cluster][index]["window"]
            x = files_in_cluster[cluster][index]["start"]
            for entry in dict_for_clustering[ws][subdir_name][some_file][x]: 
                if entry not in props[cluster]:
                    props[cluster][entry] = []
                props[cluster][entry].append(dict_for_clustering[ws][subdir_name][some_file][x][entry])
    return props

def sample_get(part1, nsamples, subdirnames = [], filenames = [], subdirnames_skip = [], filenames_skip = []): 
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
            compare_random_cluster(load_object(part1 + subdirname + "/filenames/" + filename), nsamples)
            break
        break

samplenum = 1000
subdirnames = ["all", "no_same", "no_xy", "heading", "acceler"]
filenames = ["KMeans"]
subdirnames_skip = ["poly", "flags"]
filenames_skip = ["_train"] 

subdirnames = []
filenames = []
subdirnames_skip = []
filenames_skip = ["_train"] 

part1 = "all_clus/" 
sample_get(part1, samplenum, subdirnames, filenames, subdirnames_skip, filenames_skip)
part1 = "all_isomap/" 
sample_get(part1, samplenum, subdirnames, filenames, subdirnames_skip, filenames_skip)