from utilities import *  
  
dict_for_clustering = load_object("dict_for_clustering")
train_names = load_object("train_names")
test_names = load_object("test_names") 
 
def shortenfv(str_extension, ws, vehicle, shortfile, x):     
    print(ws, vehicle, shortfile, x)
    retarr = load_object("all_closest/closest_ids/" + str_extension+ "/" + ws + "/" + vehicle + "/" + shortfile + "/" + x + "/closest_ids_" + str_extension+ "_" + ws + "_" + vehicle + "_" + shortfile + "_" + x)
    sa = shorten_arr(retarr)
    ea = elongate_arr(sa)
    print(sa[:3])
    print(retarr[:3])
    print(ea[:3]) 
    save_object("all_closest/closest_ids/" + str_extension+ "/" + ws + "/" + vehicle + "/" + shortfile + "/" + x + "/closest_ids_" + str_extension+ "_" + ws + "_" + vehicle + "_" + shortfile + "_" + x, sa)

def shorten_arr(retarr):
    if not isinstance(retarr[0][1], str):
        return retarr
    retarrn = [[v for v in r] for r in retarr]
    for rn in range(len(retarrn)):
        retarrn[rn][0] = int(retarrn[rn][0])
        retarrn[rn][1] = int(retarrn[rn][1].replace("Vehicle_", ""))
        retarrn[rn][2] = int(retarrn[rn][2].replace("events_", "").replace(".csv", ""))
        retarrn[rn][3] = int(retarrn[rn][3])
        retarr[rn] = np.array(retarr[rn])
    retarr = np.array(retarr)
    return retarrn 

def elongate_arr(retarr):
    if isinstance(retarr[0][1], str):
        return retarr
    retarrn = [[v for v in r] for r in retarr]
    for rn in range(len(retarrn)):
        retarrn[rn][0] = str(retarrn[rn][0])
        retarrn[rn][1] = "Vehicle_" + str(retarrn[rn][1])
        retarrn[rn][2] = "events_" + str(retarrn[rn][2]) + ".csv"
        retarrn[rn][3] = str(retarrn[rn][3])
        retarr[rn] = np.array(retarr[rn])
    retarr = np.array(retarr)
    return retarrn 
 
for method in os.listdir("all_closest/closest_dist"):
    for ws in os.listdir("all_closest/closest_dist/" + method):
        for veh in os.listdir("all_closest/closest_dist/" + method + "/" + ws):
            for ride in os.listdir("all_closest/closest_dist/" + method + "/" + ws + "/" + veh):
                for x in os.listdir("all_closest/closest_dist/" + method + "/" + ws + "/" + veh + "/" + ride):
                    shortenfv(method, ws, veh, ride, x)
                        