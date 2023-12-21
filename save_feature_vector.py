from utilities import * 
import random
  
dict_for_clustering = load_object("dict_for_clustering")
train_names = load_object("train_names")
test_names = load_object("test_names") 

def myfv(subdirname, features = [], maxlen = 1):
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
  
    for num in range(len(feats_vect)):
        retv, retd = get_euclid_save(feats_vect, num, trajs_order) 
        print(np.shape(retv))
        print(np.shape(retd), retv[0], retd[0])
        shortfile = retv[0][2].replace("events_", "").replace(".csv", "")
 
        if not os.path.isdir("all_closest/closest_ids/" + str_extension + "/" + retv[0][0] + "/" + retv[0][1] + "/" + shortfile + "/" + retv[0][3]):
            os.makedirs("all_closest/closest_ids/" + str_extension + "/" + retv[0][0] + "/" + retv[0][1] + "/" + shortfile + "/" + retv[0][3])
        save_object("all_closest/closest_ids/" + str_extension + "/" + retv[0][0] + "/" + retv[0][1] + "/" + shortfile + "/" + retv[0][3] + "/closest_ids_" + str_extension + "_" + retv[0][0] + "_" + retv[0][1] + "_" + shortfile + "_" + retv[0][3], retv)
 
        if not os.path.isdir("all_closest/closest_dist/" + str_extension + "/" + retv[0][0] + "/" + retv[0][1] + "/" + shortfile + "/" + retv[0][3]):
            os.makedirs("all_closest/closest_dist/" + str_extension + "/" + retv[0][0] + "/" + retv[0][1] + "/" + shortfile + "/" + retv[0][3])
        save_object("all_closest/closest_dist/" + str_extension + "/" + retv[0][0] + "/" + retv[0][1] + "/" + shortfile + "/" + retv[0][3] + "/closest_dist_" + str_extension + "_" + retv[0][0] + "_" + retv[0][1] + "_" + shortfile + "_" + retv[0][3], retd)

def get_euclid_save(array_np, num_sample, torder):  
    start_range = 0
    end_range = len(array_np)   
    
    frobenius_norm = np.linalg.norm(array_np, 'fro') 
    array_np = array_np / frobenius_norm
    array_np2 = array_np[num_sample, ] 
    distances_np = np.linalg.norm(array_np[:, None] - array_np2, axis=2) 
    
    new_array = distances_np[:, 0] 
    new_dict = dict()
    for i in range(len(new_array)):
        new_dict[i] = new_array[i]
    norder = []
    ndist = []
    for i in dict(sorted(new_dict.items(), key=lambda item: item[1])):
        norder.append(torder[i])
        ndist.append(new_dict[i])
    return np.array(norder), np.array(ndist)
 
def getfv(str_extension, ws, vehicle, shortfile, x, r, c, sumto, topv, draw = False):     
    print(ws, vehicle, shortfile, x)
    retarr = load_object("all_closest/closest_ids/" + str_extension+ "/" + ws + "/" + vehicle + "/" + shortfile + "/" + x + "/closest_ids_" + str_extension+ "_" + ws + "_" + vehicle + "_" + shortfile + "_" + x)
    distarr = load_object("all_closest/closest_dist/" + str_extension+ "/" + ws + "/" + vehicle + "/" + shortfile + "/" + x + "/closest_dist_" + str_extension+ "_" + ws + "_" + vehicle + "_" + shortfile + "_" + x)

    print(retarr[0][2])
    dict_vehicle = dict()
    total_vehicle = dict()
    all_vehicle_nums = [v[2] for v in retarr[1:]]
    so_far = dict()
    for i, veh in enumerate(all_vehicle_nums):
        if veh not in so_far:
            so_far[veh] = 0
        so_far[veh] += 1
        total_vehicle[i] = dict()
        for k in so_far:
            total_vehicle[i][k] = so_far[k] 
            
    for dv in total_vehicle[sumto]:
        dict_vehicle[dv] = total_vehicle[sumto][dv] / total_vehicle[len(retarr) - 2][dv]

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
            longitudes, latitudes, times = load_traj_window(retarr[ix][1], retarr[ix][2].replace("events_", "").replace(".csv", ""), int(retarr[ix][3]), int(retarr[ix][0]))
            longitudes_scaled_to_max, latitudes_scaled_to_max = scale_long_lat(longitudes, latitudes, xmax = 0.005, ymax = 0.005, keep_aspect_ratio = True)
            plt.plot(longitudes_scaled_to_max, latitudes_scaled_to_max, color = "k")     
        plt.show() 

def compare_methods(str_extensions, wsz, vehicle, shortfile, x):  
    print(wsz, vehicle, shortfile, x) 
    print(str_extensions)
    vehicle_positions = dict() 
    for str_extension in str_extensions:
        print(str_extension)  
        retarr = load_object("all_closest/closest_ids/" + str_extension+ "/" + wsz + "/" + vehicle + "/" + shortfile + "/" + x + "/closest_ids_" + str_extension+ "_" + wsz + "_" + vehicle + "_" + shortfile + "_" + x)
        distarr = load_object("all_closest/closest_dist/" + str_extension+ "/" + wsz + "/" + vehicle + "/" + shortfile + "/" + x + "/closest_dist_" + str_extension+ "_" + wsz + "_" + vehicle + "_" + shortfile + "_" + x)
        print(np.shape(retarr))
        print(np.shape(distarr)) 
        print(retarr[0])
        print(distarr[0])
        for i in range(1, len(retarr)):
            str_comb = retarr[i][0] + "/" + retarr[i][1] + "/" + retarr[i][2] + "/" + retarr[i][3] 
            if str_comb not in vehicle_positions: 
                vehicle_positions[str_comb] = dict()  
            vehicle_positions[str_comb][str_extension] = (i, distarr[i])  
    maxiddiff = 0
    maxdistdiff = 0
    vehstr_id = ""
    vehstr_dist = ""
    id1 = ""
    id2 = ""
    dist1 = ""
    dist2 = ""
    for vehstr in vehicle_positions: 
        for i, method1 in enumerate(str_extensions): 
            x1 = vehicle_positions[vehstr][method1]
            for method2 in str_extensions[i + 1:]:  
                x2 = vehicle_positions[vehstr][method2]
                iddiff = abs(x1[0] - x2[0])
                distdiff = abs(x1[1] - x2[1])
                if iddiff > maxiddiff:
                    maxiddiff = iddiff
                    vehstr_id = vehstr
                    id1 = method1
                    id2 = method2
                if distdiff > maxdistdiff:
                    maxdistdiff = distdiff
                    vehstr_dist = vehstr 
                    dist1 = method1
                    dist2 = method2
    print("id", vehstr_id, str_extension, vehicle_positions[vehstr_id][id1], vehicle_positions[vehstr_id][id2])
    #comparetwo(vehstr_id, wsz, vehicle, shortfile, x, "vehstr_id\n" + str(id1) + "\n" + str(id2))  
    print("dist", vehstr_dist, str_extension, vehicle_positions[vehstr_dist][dist1], vehicle_positions[vehstr_dist][dist2])
    #comparetwo(vehstr_dist, wsz, vehicle, shortfile, x, "vehstr_dist\n" + str(dist1) + "\n" + str(dist2)) 

def comparetwo(vehstr_dist, wsz, vehicle, shortfile, x, title):
        vh_strs = vehstr_dist.split("/")
        ws = int(vh_strs[0])
        vh = vh_strs[1]
        rd = vh_strs[2].replace("events_", "").replace(".csv", "")
        pos = int(vh_strs[3]) 
        plt.subplot(1, 2, 1)
        plt.axis('off')  
        plt.title(wsz + " " + vehicle + "\n" + shortfile + "\n" + x)
        longitudes, latitudes, times = load_traj_window(vehicle, shortfile, int(x), int(wsz))
        longitudes_scaled_to_max, latitudes_scaled_to_max = scale_long_lat(longitudes, latitudes, xmax = 0.005, ymax = 0.005, keep_aspect_ratio = True)
        plt.plot(longitudes_scaled_to_max, latitudes_scaled_to_max, color = "k")  
        plt.subplot(1, 2, 2)
        plt.axis('off') 
        plt.title(title)
        longitudes, latitudes, times = load_traj_window(vh, rd, pos, ws)
        longitudes_scaled_to_max, latitudes_scaled_to_max = scale_long_lat(longitudes, latitudes, xmax = 0.005, ymax = 0.005, keep_aspect_ratio = True)
        plt.plot(longitudes_scaled_to_max, latitudes_scaled_to_max, color = "k")      
        plt.show() 

#myfv("no_rays_no_xy_no_same_acceler_heading") 
#myfv("")

r = 4
c = 5
sumto = 1000
topv = 3
for method in os.listdir("all_closest/closest_dist"):
    for ws in os.listdir("all_closest/closest_dist/" + method):
        for veh in os.listdir("all_closest/closest_dist/" + method + "/" + ws):
            for ride in os.listdir("all_closest/closest_dist/" + method + "/" + ws + "/" + veh):
                for x in os.listdir("all_closest/closest_dist/" + method + "/" + ws + "/" + veh + "/" + ride):
                        getfv(method, ws, veh, ride, x, r, c, sumto, topv)
methods = []
for method in os.listdir("all_closest/closest_dist"):
    methods.append(method) 
print(methods)
wss = []
for ws in os.listdir("all_closest/closest_dist/" + methods[0]):
    wss.append(ws)
print(wss)
for veh in os.listdir("all_closest/closest_dist/" + methods[0] + "/" + wss[0]):
    for ride in os.listdir("all_closest/closest_dist/" + methods[0] + "/" + wss[0] + "/" + veh):
        for x in os.listdir("all_closest/closest_dist/" + methods[0] + "/" + wss[0] + "/" + veh + "/" + ride):
            compare_methods(methods, wss[0], veh, ride, x)