from utilities import * 
import seaborn as sns
  
def savefv(subdirname, features = []):
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
    str_extension = subdirname
    if subdirname == "":
        str_extension = "no_skip"
    for feat in features:
        str_extension += "_" + str(feat)
    retarr = []
    distarr = []

    samp = random.sample(range(start_range, end_range + 1), 1)
    retv, retd = get_euclid(feats_vect, 1, trajs_order, [samp[0]])
    retarr.append(retv)
    distarr.append(retd)

    retarr = np.array(retarr)
    distarr = np.array(distarr)
    print(np.shape(retarr))
    print(np.shape(distarr))
    if not os.path.isdir("all_closest"):
        os.makedirs("all_closest")
    save_object("all_closest/closest_ids_" + str_extension, retarr)
    save_object("all_closest/closest_dist_" + str_extension, distarr) 

def get_euclid(array_np, torder, random_numbers):  
    start_range = 0
    end_range = len(array_np)  
    
    frobenius_norm = np.linalg.norm(array_np, 'fro') 
    array_np = array_np / frobenius_norm
    array_np2 = array_np[random_numbers, ] 
    distances_np = np.linalg.norm(array_np[:, None] - array_np2, axis=2) 
    
    new_array = distances_np[:, 0]
    new_array_orig = list(distances_np[:, 0])
    new_array = sorted(new_array)
    ixes = [new_array_orig.index(val) for val in new_array]
    return torder[ixes], new_array

def getfv(str_extension, r, c, draw = False):   
    #savefv()
    retarr = load_object("all_closest/closest_ids_" + str_extension)
    distarr = load_object("all_closest/closest_dist_" + str_extension) 
    dict_vehicle = dict()
    for v in retarr[0][1:r * c]:
        if v[2] not in dict_vehicle:
            dict_vehicle[v[2]] = 0
        dict_vehicle[v[2]] += 1
    print(dict_vehicle) 
    if draw:
        plt.figure(figsize=(r, c))
        for ix in range(0, r * c):
            plt.subplot(r, c, ix + 1)
            plt.axis('off') 
            longitudes, latitudes, times = load_traj_window(retarr[0][ix][1], retarr[0][ix][2].replace("events_", "").replace(".csv", ""), int(retarr[0][ix][3]), int(retarr[0][ix][0]))
            longitudes_scaled_to_max, latitudes_scaled_to_max = scale_long_lat(longitudes, latitudes, xmax = 0.005, ymax = 0.005, keep_aspect_ratio = True)
            plt.plot(longitudes_scaled_to_max, latitudes_scaled_to_max, color = "k")     
        plt.show() 

r = 400
c = 50
getfv("no_rays_no_xy_no_same_acceler_heading", r, c) 
getfv("no_skip", r, c) 