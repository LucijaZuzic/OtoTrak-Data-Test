from utilities import *
import random
import seaborn as sns

dict_for_clustering = load_object("dict_for_clustering")
train_names = load_object("train_names")
test_names = load_object("test_names") 
from sklearn.manifold import TSNE
from sklearn.manifold import Isomap

def only_shape(subdirname, features = []):
    feats_vect = []
    feats_vect_train = []
    feats_vect_test = [] 
    feature_order = []
    trajs_order = []
    trajs_train_order = []
    trajs_test_order = []
    for window_size in dict_for_clustering: 
        for subdir_name in dict_for_clustering[window_size]: 
            for some_file in dict_for_clustering[window_size][subdir_name]: 
                for x in dict_for_clustering[window_size][subdir_name][some_file]:  
                    for feat in dict_for_clustering[window_size][subdir_name][some_file][x]:
                        if len(features) != 0 and feat not in features:
                            continue
                        if subdirname != "" and skip_var(feat, subdirname):
                            continue 
                        feature_order.append(feat)
                    if len(feature_order) > 0:
                        break
                if len(feature_order) > 0:
                    break
            if len(feature_order) > 0:
                break
        if len(feature_order) > 0:
            break 
    for window_size in dict_for_clustering: 
        for subdir_name in dict_for_clustering[window_size]: 
            for some_file in dict_for_clustering[window_size][subdir_name]: 
                for x in dict_for_clustering[window_size][subdir_name][some_file]: 
                    if len(dict_for_clustering[window_size][subdir_name][some_file][x]) == 0:
                        continue 
                    feats_vect.append([])
                    trajs_order.append((window_size, subdir_name, some_file, x))
                    if some_file in train_names:
                        feats_vect_train.append([])
                        trajs_train_order.append((window_size, subdir_name, some_file, x))
                    if some_file in test_names:
                        feats_vect_test.append([])
                        trajs_test_order.append((window_size, subdir_name, some_file, x))
                    for feat in feature_order: 
                        if subdirname != "" and skip_var(feat, subdirname):
                            continue 
                        feats_vect[-1] = add_key(feat, dict_for_clustering[window_size][subdir_name][some_file][x][feat], feats_vect[-1])
                        if some_file in train_names:
                            feats_vect_train[-1] = add_key(feat, dict_for_clustering[window_size][subdir_name][some_file][x][feat], feats_vect_train[-1])
                        if some_file in test_names:
                            feats_vect_test[-1] = add_key(feat, dict_for_clustering[window_size][subdir_name][some_file][x][feat], feats_vect_test[-1])

    feats_vect = np.array(feats_vect)
    feats_vect_train = np.array(feats_vect_train) 
    feats_vect_test = np.array(feats_vect_test)
    trajs_order = np.array(trajs_order)
    trajs_train_order = np.array(trajs_train_order)
    trajs_test_order = np.array(trajs_test_order)

    print(np.shape(feats_vect)) 
    print(np.shape(feats_vect_train))
    print(np.shape(feats_vect_test))
    '''
    for i, name1 in enumerate(feature_order): 
        for j, name2 in enumerate(feature_order[i: ]):
            plt.title(name1 + " " + name2)
            plt.scatter(feats_vect[:, i], feats_vect[:, j])
            plt.show()

    train_embedded = TSNE(n_components=2).fit_transform(feats_vect_train)
    test_embedded = TSNE(n_components=2).fit_transform(feats_vect_test)
    all_embedded = TSNE(n_components=2).fit_transform(feats_vect)
    embedding = Isomap(n_components=2)
    isomap_new = embedding.fit(feats_vect_train)
    sd_x_train = isomap_new.transform(feats_vect_train) 
    sd_x_test = isomap_new.transform(feats_vect_test)
    sd_x_all = isomap_new.transform(feats_vect)
 
    plt.rcParams.update({'font.size': 22})
    plt.figure(figsize=(20, 10))
    plt.subplot(1, 3, 1) 
    plt.title("Train TSNE")  
    plt.scatter(train_embedded[:, 0], train_embedded[:, 1])    
    plt.subplot(1, 3, 2) 
    plt.title("Test TSNE")  
    plt.scatter(test_embedded[:, 0], test_embedded[:, 1])   
    plt.subplot(1, 3, 3) 
    plt.title("All TSNE")  
    plt.scatter(all_embedded[:, 0], all_embedded[:, 1])   
    plt.show()
    
    plt.figure(figsize=(20, 10))
    plt.subplot(1, 3, 1) 
    plt.title("Train Isomap")  
    plt.scatter(sd_x_train[:, 0], sd_x_train[:, 1])    
    plt.subplot(1, 3, 2) 
    plt.title("Test Isomap")  
    plt.scatter(sd_x_test[:, 0], sd_x_test[:, 1])   
    plt.subplot(1, 3, 3) 
    plt.title("All Isomap")  
    plt.scatter(sd_x_all[:, 0], sd_x_all[:, 1])   
    plt.show()
    '''
    str_extension = subdirname
    if subdirname == "":
        str_extension = "no_skip"
    for feat in features:
        str_extension += "_" + str(feat)
    retarr = []
    distarr = []
    for num in range(100):
        retv, retd = get_euclid(feats_vect, 2, trajs_order, [num])
        retarr.append(retv)
        distarr.append(retd)
        #print(num)
    #analyse_cols(feats_vect, feature_order)
    retarr = np.array(retarr)
    distarr = np.array(distarr)
    print(np.shape(retarr))
    print(np.shape(distarr))
    if not os.path.isdir("all_closest"):
        os.makedirs("all_closest")
    save_object("all_closest/closest_ids_" + str_extension, retarr)
    save_object("all_closest/closest_dist_" + str_extension, distarr) 


def get_euclid(array_np, size_of_sample, torder, random_numbers = []):  
    start_range = 0
    end_range = len(array_np)  
    if random_numbers == []:
        random_numbers = random.sample(range(start_range, end_range + 1), size_of_sample)
    #print(random_numbers)
    # Calculate the Frobenius norm
    frobenius_norm = np.linalg.norm(array_np, 'fro') 
    # Normalize the matrix
    array_np = array_np / frobenius_norm
    array_np2 = array_np[random_numbers, ]
    #print(np.shape(array_np))
    #print(np.shape(array_np2))
    distances_np = np.linalg.norm(array_np[:, None] - array_np2, axis=2) 
    '''
    print("Euclidean distances between rows:")
    print(distances_np)
    for rn in range(size_of_sample): 
        new_row = [x for x in distances_np[rn, :]]
        new_row = sorted(new_row)
        new_index = [random_numbers[list(distances_np[rn, :]).index(x)] for x in new_row]
        print(random_numbers[rn], new_row[1:11], new_index[1:11])
    '''
    #sns.heatmap(distances_np, cmap='YlGnBu', xticklabels=random_numbers, yticklabels=random_numbers)
    #plt.title('Heatmap from NumPy Array')
    #plt.xlabel('X axis') 
    #plt.ylabel('Y axis')
    #plt.show()
    #print(np.shape(distances_np))
    for cn in range(np.shape(distances_np)[1]):
        new_array = distances_np[:, cn]
        new_array_orig = list(distances_np[:, cn])
        new_array = sorted(new_array)
        ixes = [new_array_orig.index(val) for val in new_array]
        return torder[ixes], new_array
        '''
        print(new_array)
        print(ixes)
        print(torder[random_numbers[cn]])
        print(torder[ixes]) 
        plt.figure(figsize=(30, 40))
        for ix in range(1200):
            plt.subplot(30, 40, ix + 1)
            plt.axis('off')
            some_ids = torder[ixes][ix]
            longitudes, latitudes, times = load_traj_window(some_ids[1], some_ids[2].replace("events_", "").replace(".csv", ""), int(some_ids[3]), int(some_ids[0]))
            longitudes_scaled_to_max, latitudes_scaled_to_max = scale_long_lat(longitudes, latitudes, xmax = 0.005, ymax = 0.005, keep_aspect_ratio = True)
            plt.plot(longitudes_scaled_to_max, latitudes_scaled_to_max, color = "k")     
        plt.show()
        '''
 
def analyse_cols(array, feature_order):
    import numpy as np 
    var_col = np.var(array, axis=0) 
    std_col = np.var(array, axis=0) 
    mean_col = np.mean(array, axis=0) 
    median_col = np.mean(array, axis=0) 
    q1_col = np.percentile(array, 25, axis=0) 
    q3_col = np.percentile(array, 75, axis=0) 
    iqr_col = q3_col - q1_col 
    ptp_col = np.ptp(array, axis=0)  

    values_to_divide = {"Standard deviation": var_col, "Variance": std_col}
    values_to_divide_by = {"Mean": mean_col, "Median": median_col, "PTP": ptp_col, "IQR": iqr_col}  
 
    #for key2 in ["PTP"]: 
        #for colnum in range(len(values_to_divide_by[key2])):
            #if values_to_divide_by[key2][colnum] == 0:
                #print(key2, feature_order[colnum])

    feature_set = dict()
    for key in values_to_divide:
        feature_set[key] = dict()
        for key2 in values_to_divide_by: 
            result = values_to_divide[key] / values_to_divide_by[key2]
            dict_sorted = dict()
            for i, name in enumerate(feature_order):
                dict_sorted[name] = result[i]
            #print(key, "/", key2, "of each column:")
            feature_set[key][key2] = set()
            count = 0
            for name in dict(sorted(dict_sorted.items(), key=lambda item: item[1], reverse = True)):
                if dict_sorted[name] > 0.95 and not math.isinf(dict_sorted[name]) and not math.isnan(dict_sorted[name]):
                    count += 1  
                    feature_set[key][key2].add(name)
            #print(count / len(dict_sorted))

    all_feats = feature_set["Standard deviation"]["PTP"]
    for key in values_to_divide:
        for key2 in values_to_divide_by:
            all_feats = all_feats.intersection(feature_set[key][key2])
            
    correlation_matrix = np.corrcoef(array, rowvar=False)
    set_correlated = dict()
    for i, name1 in enumerate(feature_order):
        if name1 not in all_feats:
            continue
        for j, name2 in enumerate(feature_order[i: ]):
            if name2 not in all_feats:
                continue
            if abs(correlation_matrix[i, j]) > 0.95: 
                if name1 not in set_correlated:
                    set_correlated[name1] = set([name1])
                if name2 not in set_correlated:
                    set_correlated[name2] = set([name2])
                set_correlated[name1].add(name2)
                set_correlated[name2].add(name1)

    #print(sorted(list(all_feats)))   
    #for x in set_correlated: 
        #print(x.replace("all_feats_", "".replace("scaled_to_max_", "")), len(set_correlated[x])) 
        #for y in set_correlated[x]:
            #print(" ", y.replace("all_feats_", "").replace("scaled_to_max_", ""))
                
    size_limit = 1
    res = False
    while not res:
        res = minimal_cover(set_correlated, set(), set(), size_limit)
        size_limit += 1
    print(len(set_correlated), len(all_feats), len(feature_order))
    print(len(set_correlated['all_feats_acceler_scaled_to_max_x_acceler_abs'].union(set_correlated['all_feats_acceler_scaled_to_max_mean_speed_ototrak'])))
    print(set_correlated['all_feats_acceler_scaled_to_max_x_acceler_abs'].intersection(set_correlated['all_feats_acceler_scaled_to_max_mean_speed_ototrak']))

def minimal_cover(sets, chosen, seen, size_limit):
    if len(chosen) > size_limit:
        return False
    if len(seen) == len(sets):
        return False
    covered_sets = set() 
    for x in sets:
        if x in chosen:
            covered_sets = covered_sets.union(sets[x]) 
    if len(covered_sets) == len(sets):
        number_same = 0
        for y in chosen:
            if "same" in y:
                number_same += 1
        print(len(chosen), number_same, chosen)
        return True
    else:
        result = False
        seen_so_far = set([y for y in seen])
        for x in sets: 
            if x in chosen:
                continue
            if x in seen:
                continue
            chosen_new = set([y for y in chosen]) 
            chosen_new.add(x)
            result |= minimal_cover(sets, chosen_new, seen_so_far, size_limit)
            seen_so_far.add(x)
        return result
             
features = ['all_feats_acceler_scaled_to_max_x_acceler_abs', 'all_feats_acceler_scaled_to_max_mean_speed_ototrak']
features = []
only_shape("no_rays_no_xy_no_same_acceler_heading", features) 
only_shape("")
'''
for subdirname_p1 in ["all", "no_rays"]:
    for subdirname_p2 in ["", "_poly", "_flags", "_poly_flags"]:
        for subdirname_p3 in ["", "_no_same", "_no_xy", "_no_same_no_xy"]:
            for subdirname_p4 in ["", "_acceler", "_heading", "_acceler_heading"]:
                subdirname = subdirname_p1 + subdirname_p2 + subdirname_p3 + subdirname_p4 
                print(subdirname)
                only_shape(subdirname)
                
part2 = []
for size in os.listdir("rays"):
    part2.append("_size_" + str(size) + "_")  
for subdirname_p1 in ["", "_acceler", "_heading", "_acceler_heading"]:
    for subdirname_p2 in part2:    
        subdirname = "only_rays" + subdirname_p1 + subdirname_p2 
        print(subdirname) 
        only_shape(subdirname)
'''    