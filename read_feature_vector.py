from utilities import * 
import random
  
dict_for_clustering = load_object("dict_for_clustering")
train_names = load_object("train_names")
test_names = load_object("test_names") 

def savefv(subdirname, features = [], maxlen = 1):
    str_extension = subdirname
    if subdirname == "":
        str_extension = "no_skip"
    for feat in features:
        str_extension += "_" + str(feat)
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
                        #if len(features) != 0 and feat not in features:
                            #continue
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
    retarr = []
    distarr = []
 
    samp = random.sample(range(0, len(feats_vect)), maxlen)
    for num in samp:
        retv, retd = get_euclid(feats_vect, 1, trajs_order, [num])
        for rv in retv:
            retarr.append(rv)
        for rd in retd:
            distarr.append(rd)

    retarr = np.array(retarr)
    distarr = np.array(distarr)
    print(np.shape(retarr))
    print(np.shape(distarr))
    return retarr, distarr
    #if not os.path.isdir("all_closest"):
        #os.makedirs("all_closest")
    #save_object("all_closest/closest_ids_" + str_extension, retarr)
    #save_object("all_closest/closest_dist_" + str_extension, distarr) 

def get_euclid(array_np, size_of_sample, torder, random_numbers = []):  
    start_range = 0
    end_range = len(array_np)  
    if random_numbers == []:
        random_numbers = random.sample(range(start_range, end_range + 1), size_of_sample) 
    
    frobenius_norm = np.linalg.norm(array_np, 'fro') 
    array_np = array_np / frobenius_norm
    array_np2 = array_np[random_numbers, ] 
    distances_np = np.linalg.norm(array_np[:, None] - array_np2, axis=2) 
    
    to, na = [], []
    for cn in range(np.shape(distances_np)[1]):
        new_array = distances_np[:, cn]
        new_array_orig = list(distances_np[:, cn])
        new_array = sorted(new_array)
        ixes = [new_array_orig.index(val) for val in new_array]
        to.append(np.array(torder[ixes]))
        na.append(np.array(new_array))
    return np.array(to), np.array(na)

def getfv(subdirname, r, c, sumto, topv, draw = False, features = [], maxlen = 1):   
    str_extension = subdirname
    if subdirname == "":
        str_extension = "no_skip"
    for feat in features:
        str_extension += "_" + str(feat)
    #savefv()
    #retarr = load_object("all_closest/closest_ids_" + str_extension)
    #distarr = load_object("all_closest/closest_dist_" + str_extension) 
    retarr, distarr = savefv(subdirname, features, maxlen)
    for cn in range(len(retarr)):
        print(retarr[cn][0][2])
        dict_vehicle = dict()
        total_vehicle = dict()
        all_vehicle_nums = [v[2] for v in retarr[cn][1:]]
        so_far = dict()
        for i, veh in enumerate(all_vehicle_nums):
            if veh not in so_far:
                so_far[veh] = 0
            so_far[veh] += 1
            total_vehicle[i] = dict()
            for k in so_far:
                total_vehicle[i][k] = so_far[k] 
        '''
        for v in retarr[cn][1:sumto]:
            if v[2] not in dict_vehicle:
                dict_vehicle[v[2]] = 0
            dict_vehicle[v[2]] += 1
        for v in retarr[cn]:
            if v[2] not in total_vehicle:
                total_vehicle[v[2]] = 0
            total_vehicle[v[2]] += 1
        '''
        for dv in total_vehicle[sumto]:
            dict_vehicle[dv] = total_vehicle[sumto][dv] / total_vehicle[len(retarr[cn]) - 2][dv]

        printedv = 0
        for dv in dict(sorted(dict_vehicle.items(), key=lambda item: item[1], reverse=True)):
            if printedv > topv:
                break
            print(dict_vehicle[dv], dv) 
            printedv += 1
        if draw:
            plt.figure(figsize=(r, c))
            for ix in range(0, r * c):
                plt.subplot(r, c, ix + 1)
                plt.axis('off') 
                longitudes, latitudes, times = load_traj_window(retarr[cn][ix][1], retarr[cn][ix][2].replace("events_", "").replace(".csv", ""), int(retarr[cn][ix][3]), int(retarr[cn][ix][0]))
                longitudes_scaled_to_max, latitudes_scaled_to_max = scale_long_lat(longitudes, latitudes, xmax = 0.005, ymax = 0.005, keep_aspect_ratio = True)
                plt.plot(longitudes_scaled_to_max, latitudes_scaled_to_max, color = "k")     
            plt.show() 

r = 4
c = 5
sumto = 1000
topv = 20
getfv("no_rays_no_xy_no_same_acceler_heading", r, c, sumto, topv, maxlen = 1) 
getfv("", r, c, sumto, topv, maxlen = 1)
str_extension = "no_skip"
retarr = load_object("all_closest/closest_ids_" + str_extension)
distarr = load_object("all_closest/closest_dist_" + str_extension) 
print(np.shape(retarr))
print(np.shape(distarr))