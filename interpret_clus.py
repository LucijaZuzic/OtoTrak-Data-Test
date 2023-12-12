from utilities import *
parts_to_ignore = ["subdir", "file", "cluster", "size"]

def make_avg(part1, part2, thr, subdirnames = [], filenames = [], subdirnames_skip = [], filenames_skip = []):
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
            print(part1 + subdirname + part2 + filename)
            file_clus_var = pd.read_csv(part1 + subdirname + part2 + filename + "_var.csv", index_col = False) 
            file_clus_std = pd.read_csv(part1 + subdirname + part2 + filename + "_std.csv", index_col = False) 
            file_clus_var_scaled = pd.read_csv(part1 + subdirname + part2 + filename + "_var_scaled.csv", index_col = False) 
            file_clus_std_scaled = pd.read_csv(part1 + subdirname + part2 + filename + "_std_scaled.csv", index_col = False) 
            file_clus_avg = pd.read_csv(part1 + subdirname + part2 + filename + "_avg.csv", index_col = False)  
            file_clus_min = pd.read_csv(part1 + subdirname + part2 + filename + "_min.csv", index_col = False)  
            file_clus_max = pd.read_csv(part1 + subdirname + part2 + filename + "_max.csv", index_col = False) 
            file_clus_range = pd.read_csv(part1 + subdirname + part2 + filename + "_range.csv", index_col = False)

            clusters = dict()
            for i, cluster in enumerate(list(file_clus_var["cluster"])):
                clusters[cluster] = i
            cluster_keys = sorted(list(clusters.keys()))
            features = []
            for feature in file_clus_var.head():
                if feature not in parts_to_ignore:
                    features.append(feature)

            min_min_for_feature = dict()
            max_max_for_feature = dict()
            max_range_for_feature = dict()
            for feature in features:
                min_min_for_feature[feature] = 1000000
                for mini in file_clus_min[feature]:
                    min_min_for_feature[feature] = min(min_min_for_feature[feature], mini)
                max_max_for_feature[feature] = 0
                for maxi in file_clus_max[feature]:
                    max_max_for_feature[feature] = max(max_max_for_feature[feature], maxi)
                max_range_for_feature[feature] = max_max_for_feature[feature] - min_min_for_feature[feature]

            relative_average_for_cluster_feature = dict()
            for i, cluster in enumerate(cluster_keys): 
                relative_average_for_cluster_feature[cluster] = dict()

            for i, cluster in enumerate(cluster_keys): 
                for j, cluster_second in enumerate(cluster_keys[i + 1:]): 
                    relative_average_for_cluster_feature[cluster][cluster_second] = dict() 
                    relative_average_for_cluster_feature[cluster_second][cluster] = dict()

            for i, cluster in enumerate(cluster_keys): 
                for j, cluster_second in enumerate(cluster_keys[i + 1:]): 
                    for feature in features: 
                        if max_range_for_feature[feature] != 0:
                            value = abs(file_clus_avg[feature][clusters[cluster]] - file_clus_avg[feature][clusters[cluster_second]]) / max_range_for_feature[feature]
                            relative_average_for_cluster_feature[cluster][cluster_second][feature] = value
                            relative_average_for_cluster_feature[cluster_second][cluster][feature] = value
            
            print(len(clusters))
            for i, cluster in enumerate(cluster_keys): 
                for j, cluster_second in enumerate(cluster_keys[i + 1:]): 
                    for feat in dict(sorted(relative_average_for_cluster_feature[cluster][cluster_second].items(), key = lambda item: item[1], reverse = True)): 
                        if relative_average_for_cluster_feature[cluster][cluster_second][feat] > thr:
                            print(cluster, cluster_second, feat, relative_average_for_cluster_feature[cluster][cluster_second][feat])
                            break
    
def make_var(part1, part2, feature_name, subdirnames = [], filenames = [], subdirnames_skip = [], filenames_skip = []):
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
            print(part1 + subdirname + part2 + filename)   
            file_clus_var_scaled = pd.read_csv(part1 + subdirname + part2 + filename + feature_name + ".csv", index_col = False)  

            clusters = dict()
            for i, cluster in enumerate(list(file_clus_var_scaled["cluster"])):
                clusters[cluster] = i
            cluster_keys = sorted(list(clusters.keys()))
            features = []
            for feature in file_clus_var_scaled.head():
                if feature not in parts_to_ignore:
                    features.append(feature)
            stdevs_for_cluster = dict()
            for cluster in cluster_keys:  
                stdevs_for_cluster[cluster] = dict()
                for feature in features: 
                    if not math.isnan(file_clus_var_scaled[feature][clusters[cluster]]) and not math.isinf(file_clus_var_scaled[feature][clusters[cluster]]):
                        stdevs_for_cluster[cluster][feature] = file_clus_var_scaled[feature][clusters[cluster]] 
                        stdevs_for_cluster[cluster][feature] = file_clus_var_scaled[feature][clusters[cluster]]
                for feat in dict(sorted(stdevs_for_cluster[cluster].items(), key = lambda item: item[1], reverse = True)):
                    print(cluster, feat, stdevs_for_cluster[cluster][feat])
                    break 

subdirnames = ["all", "no_same", "no_xy", "heading", "acceler"]
filenames = ["KMeans"]
subdirnames_skip = ["poly", "flags"]
filenames_skip = ["_train"] 
feature_name = "_std_scaled"
thr = 0.5

part1 = "all_clus/"
part2 = "/output_clus/"
#make_avg(part1, part2, thr, subdirnames, filenames, subdirnames_skip, filenames_skip)
#make_var(part1, part2, feature_name, subdirnames, filenames, subdirnames_skip, filenames_skip)

part1 = "all_isomap/"
part2 = "/output_iso/"  
make_avg(part1, part2, thr, subdirnames, filenames, subdirnames_skip, filenames_skip)
#make_var(part1, part2, feature_name, subdirnames, filenames, subdirnames_skip, filenames_skip)