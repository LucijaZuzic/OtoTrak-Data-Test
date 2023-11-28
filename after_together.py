from utilities import *  
  
all_subdirs = os.listdir()  

long_dict = load_object("markov_result/long_dict")
lat_dict = load_object("markov_result/lat_dict")
distance_predicted = load_object("markov_result/distance_predicted")

count_best_longit_latit = load_object("markov_result/count_best_longit_latit")
count_best_longit = load_object("markov_result/count_best_longit")
count_best_latit = load_object("markov_result/count_best_latit")
count_best_longit_latit_metric = load_object("markov_result/count_best_longit_latit_metric")
count_best_longit_metric = load_object("markov_result/count_best_longit_metric")
count_best_latit_metric = load_object("markov_result/count_best_latit_metric")

best_match_for_metric = load_object("markov_result/best_match_for_metric")
worst_match_for_metric = load_object("markov_result/worst_match_for_metric")
best_match_for_metric_long_lat = load_object("markov_result/best_match_for_metric_long_lat")
worst_match_for_metric_long_lat = load_object("markov_result/worst_match_for_metric_long_lat")
best_match_for_metric_long = load_object("markov_result/best_match_for_metric_long")
worst_match_for_metric_long = load_object("markov_result/worst_match_for_metric_long")
best_match_for_metric_lat = load_object("markov_result/best_match_for_metric_lat")
worst_match_for_metric_lat = load_object("markov_result/worst_match_for_metric_lat")
   
best_match_name_for_metric = load_object("markov_result/best_match_name_for_metric")
worst_match_name_for_metric = load_object("markov_result/worst_match_name_for_metric")
best_match_name_for_metric_long_lat = load_object("markov_result/best_match_name_for_metric_long_lat")
worst_match_name_for_metric_long_lat = load_object("markov_result/worst_match_name_for_metric_long_lat")
best_match_name_for_metric_long = load_object("markov_result/best_match_name_for_metric_long")
worst_match_name_for_metric_long = load_object("markov_result/worst_match_name_for_metric_long")
best_match_name_for_metric_lat = load_object("markov_result/best_match_name_for_metric_lat")
worst_match_name_for_metric_lat = load_object("markov_result/worst_match_name_for_metric_lat")
'''  
diction_include = set()
print("count_best_longit_latit")
for x in dict(sorted(count_best_longit_latit.items(), key=lambda item: item[1], reverse=True)):
    long = x.split("-")[0]
    lat = x.split("-")[1] 
    long_lat_file_name = best_match_name_for_metric_long_lat["euclidean"][x] 
    long_index = list(long_dict[long_lat_file_name].keys()).index(long)
    lat_index = list(lat_dict[long_lat_file_name].keys()).index(lat)
    if long_index != lat_index:
        continue
    if count_best_longit_latit[x] > 0:
        print(" ", x, count_best_longit_latit[x])  
        diction_include.add(x)

print("count_best_latit")
for x in dict(sorted(count_best_latit.items(), key=lambda item: item[1], reverse=True)):
    if count_best_latit[x] > 0:
        print(x, count_best_latit[x]) 

print("count_best_longit")
for x in dict(sorted(count_best_longit.items(), key=lambda item: item[1], reverse=True)):
    if count_best_longit[x] > 0:
        print(x, count_best_longit[x]) 
 
for metric_name in count_best_longit_latit_metric:   
    print(metric_name, "count_best_longit_latit")
    for x in dict(sorted(count_best_longit_latit_metric[metric_name].items(), key=lambda item: item[1], reverse=True)):
        long = x.split("-")[0]
        lat = x.split("-")[1] 
        long_lat_file_name = best_match_name_for_metric_long_lat[metric_name][x] 
        long_index = list(long_dict[long_lat_file_name].keys()).index(long)
        lat_index = list(lat_dict[long_lat_file_name].keys()).index(lat)
        if long_index != lat_index:
            continue
        if count_best_longit_latit_metric[metric_name][x] > 0:
            print(" ", x, count_best_longit_latit_metric[metric_name][x])  
            diction_include.add(x)
    
    print(metric_name, "count_best_latit")
    for x in dict(sorted(count_best_latit_metric[metric_name].items(), key=lambda item: item[1], reverse=True)):
        if count_best_latit_metric[metric_name][x] > 0:
            print(x, count_best_latit_metric[metric_name][x]) 

    print(metric_name, "count_best_longit")
    for x in dict(sorted(count_best_longit_metric[metric_name].items(), key=lambda item: item[1], reverse=True)):
        if count_best_longit[x] > 0:
            print(x, count_best_longit_metric[metric_name][x])  

for metric_name in best_match_name_for_metric:   
    metric_file_name = best_match_name_for_metric[metric_name]    
    split_vals = metric_file_name.split("/")
    vehicle = split_vals[0]
    event = split_vals[-1] 
    new_best_long_lat = set() 
    print("Best for " + metric_name + " " + metric_file_name) 
    for longlat in distance_predicted[vehicle][event][metric_name]:
        if distance_predicted[vehicle][event][metric_name][longlat] == best_match_for_metric[metric_name]:
            print(longlat, distance_predicted[vehicle][event][metric_name][longlat])
            new_best_long_lat.add(longlat)
    plot_long_lat_pairs("Best long lat pairs for " + metric_name, long_dict, lat_dict, metric_file_name, new_best_long_lat, 0.1, 0.1)
    #plot_long_lat_dict("Best for " + metric_name, long_dict, lat_dict, metric_file_name, long_dict[metric_file_name].keys(), lat_dict[metric_file_name].keys(), 0.1, 0.1)
    for long in best_match_name_for_metric_long[metric_name].keys(): 
        long_file_name = best_match_name_for_metric_long[metric_name][long]
        if long_file_name != metric_file_name:
            continue
        #print("Best for long " + long + " " + metric_name + " " + long_file_name)
        #plot_long_lat_dict("Best for long " + metric_name, long_dict, lat_dict, long_file_name, [long], lat_dict[long_file_name].keys(), 0.1, 0.1) 
        for lat in best_match_name_for_metric_lat[metric_name].keys():
            lat_file_name = best_match_name_for_metric_lat[metric_name][lat] 
            if lat_file_name != metric_file_name:
                continue
            #print("Best for lat " + lat + " " +  metric_name + " " + lat_file_name)
            #plot_long_lat_dict("Best for lat " + metric_name, long_dict, lat_dict, lat_file_name, long_dict[lat_file_name].keys(), [lat], 0.1, 0.1) 
            long_lat_file_name = best_match_name_for_metric_long_lat[metric_name][long + "-" + lat]
            #print("Best for long lat " + long + "-" + lat + " " + metric_name + " " + long_lat_file_name)
            #plot_long_lat_dict("Best for long lat " + metric_name,long_dict, lat_dict, long_lat_file_name, [long], [lat], 0.1, 0.1) 

for metric_name in worst_match_name_for_metric:   
    metric_file_name = worst_match_name_for_metric[metric_name]    
    print("Worst for " + metric_name + " " + metric_file_name)
    #plot_long_lat_dict("Worst for " + metric_name, long_dict, lat_dict, metric_file_name, long_dict[metric_file_name].keys(), lat_dict[metric_file_name].keys(), 0.1, 0.1)
    for long in worst_match_name_for_metric_long[metric_name].keys():
        long_file_name = worst_match_name_for_metric_long[metric_name][long]
        if long_file_name != metric_file_name:
            continue
        #print("Worst for long " + long + " " + metric_name + " " + long_file_name)
        #plot_long_lat_dict("Worst for long " + metric_name, long_dict, lat_dict, long_file_name, [long], lat_dict[long_file_name].keys(), 0.1, 0.1) 
        for lat in worst_match_name_for_metric_lat[metric_name].keys():
            lat_file_name = worst_match_name_for_metric_lat[metric_name][lat] 
            if lat_file_name != metric_file_name:
                continue
            #print("Worst for lat " + lat + " " +  metric_name + " " + lat_file_name)
            #plot_long_lat_dict("Worst for lat " + metric_name, long_dict, lat_dict, lat_file_name, long_dict[lat_file_name].keys(), [lat], 0.1, 0.1) 
            long_lat_file_name = worst_match_name_for_metric_long_lat[metric_name][long + "-" + lat]
            #print("Worst for long lat " + long + "-" + lat + " " + metric_name + " " + long_lat_file_name)
            #plot_long_lat_dict("Worst for long lat " + metric_name,long_dict, lat_dict, long_lat_file_name, [long], [lat], 0.1, 0.1)

for metric_name in best_match_name_for_metric:   
    for long in best_match_name_for_metric_long[metric_name].keys():  
        for lat in best_match_name_for_metric_lat[metric_name].keys():
            if long + "-" + lat not in diction_include:
                continue
            long_lat_file_name = best_match_name_for_metric_long_lat[metric_name][long + "-" + lat]
            long_index = list(long_dict[long_lat_file_name].keys()).index(long)
            lat_index = list(lat_dict[long_lat_file_name].keys()).index(lat)
            if long_index != lat_index:
                continue
            split_vals = long_lat_file_name.split("/")
            vehicle = split_vals[0]
            event = split_vals[-1] 
            new_best_long_lat = set() 
            print("Best for " + metric_name + " for " + long + "-" + lat + " " + long_lat_file_name) 
            new_best_long_lat.add(long + "-" + lat)
            #plot_long_lat_pairs("Best for " + metric_name + " for " + long + "-" + lat, long_dict, lat_dict, long_lat_file_name, new_best_long_lat, 0.1, 0.1)
'''
best_best = dict()
worst_worst = dict()
best_best_ride = dict()
worst_worst_ride = dict()
best_best_score = dict()
worst_worst_score = dict()
for metric_name in best_match_name_for_metric:   
    if "ray" in metric_name or "custom" in metric_name:
        continue
    if "no time" in metric_name or "custom" in metric_name:
        continue
    best_best[metric_name] = dict()
    worst_worst[metric_name] = dict()
    best_best_ride[metric_name] = dict()
    worst_worst_ride[metric_name] = dict()
    best_best_score[metric_name] = dict()
    worst_worst_score[metric_name] = dict()
    longlats = set()
    for long in best_match_name_for_metric_long[metric_name].keys():  
        for lat in best_match_name_for_metric_lat[metric_name].keys():
            if "ones" in long or "ones" in lat:
                continue
            if "actual" in long or "actual" in lat:
                continue
            long_lat_file_name = best_match_name_for_metric_long_lat[metric_name][long + "-" + lat]
            long_index = list(long_dict[long_lat_file_name].keys()).index(long)
            lat_index = list(lat_dict[long_lat_file_name].keys()).index(lat)
            if long_index != lat_index:
                continue
            longlats.add(long + "-" + lat) 
            best_best[metric_name][long + "-" + lat] = 0
            worst_worst[metric_name][long + "-" + lat] = 0
            best_best_ride[metric_name][long + "-" + lat] = ""
            worst_worst_ride[metric_name][long + "-" + lat] = ""
            best_best_score[metric_name][long + "-" + lat] = 100000
            worst_worst_score[metric_name][long + "-" + lat] = -100000
    for vehicle in distance_predicted:
            for event in distance_predicted[vehicle]:  
                minmetric = 100000
                minname = ""  
                bestride = ""
                maxmetric = -100000
                maxname = ""
                worstride = ""
                for longlat in longlats:
                    if distance_predicted[vehicle][event][metric_name][longlat] < minmetric:
                        minmetric = distance_predicted[vehicle][event][metric_name][longlat]
                        minname = longlat
                    if distance_predicted[vehicle][event][metric_name][longlat] > maxmetric:
                        maxmetric = distance_predicted[vehicle][event][metric_name][longlat]
                        maxname = longlat
                    if distance_predicted[vehicle][event][metric_name][longlat] < best_best_score[metric_name][longlat]:
                        best_best_score[metric_name][longlat] = distance_predicted[vehicle][event][metric_name][longlat]
                        best_best_ride[metric_name][longlat] = vehicle + "/" + event
                    if distance_predicted[vehicle][event][metric_name][longlat] > worst_worst_score[metric_name][longlat]:
                        worst_worst_score[metric_name][longlat] = distance_predicted[vehicle][event][metric_name][longlat]
                        worst_worst_ride[metric_name][longlat] = vehicle + "/" + event 
                best_best[metric_name][minname] += 1
                worst_worst[metric_name][maxname] += 1

    #print(metric_name) 
    #for longlat in dict(sorted(best_best[metric_name].items(), key=lambda item: item[1], reverse=True)): 
        #print(longlat, best_best[metric_name][longlat])
             
print("Best occurence") 
first_row = ""
sum_cols = dict()
for metric_name in best_best:
    first_row += metric_name + " & "   
    sum_cols[metric_name] = 0            
print(first_row + "\\\\ \\hline") 
sum_rows = dict()
sum_x = dict()
sum_y = dict()
sum_else = dict()
for longlat in best_best["euclidean"]:
    sum_x[longlat] = 0
    sum_y[longlat] = 0
    sum_else[longlat] = 0 
for longlat in best_best["euclidean"]:
    sum_row = 0
    row_str = longlat + " & "
    for metric_name in best_best:
        row_str += str(best_best[metric_name][longlat]) + " & "
        sum_row += best_best[metric_name][longlat]
        sum_cols[metric_name] += best_best[metric_name][longlat]
        if " x" in metric_name:
            sum_x[longlat] += best_best[metric_name][longlat]
        if " y" in metric_name:
            sum_y[longlat] += best_best[metric_name][longlat]
        if " y" not in metric_name and " x" not in metric_name:
            sum_else[longlat] += best_best[metric_name][longlat]
    sum_rows[longlat] = sum_row
    if sum_row > 0:
        print(row_str + str(sum_row) + " \\\\ \\hline")  
last_row = "" 
sum_sum_cols = 0
for metric_name in sum_cols:
    last_row += str(sum_cols[metric_name]) + " & "  
    sum_sum_cols += sum_cols[metric_name]
print(last_row + str(sum_sum_cols) + " \\\\ \\hline")  
print("Best occurence percent")   
print(first_row + "\\\\ \\hline") 
for longlat in dict(sorted(sum_rows.items(), key=lambda item: item[1], reverse=True)): 
    if sum_rows[longlat] > 0:
        row_str = longlat + " & "
        for metric_name in best_best:
            row_str += str(np.round(best_best[metric_name][longlat] / sum_cols[metric_name] * 100, 2)) + "\\% & "  
        print(row_str + str(np.round(sum_rows[longlat] / sum_sum_cols * 100, 2)) + "\\% \\\\ \\hline")  
print(last_row + str(sum_sum_cols) + " \\\\ \\hline")   
print("Best occurence percent x")   
for longlat in dict(sorted(sum_x.items(), key=lambda item: item[1], reverse=True)): 
    if sum_rows[longlat] > 0:
        row_str = longlat + " & "
        for metric_name in ["simpson x", "trapz x"]:
            row_str += str(np.round(best_best[metric_name][longlat] / sum_cols[metric_name] * 100, 2)) + "\\% & "  
        print(row_str + "\\\\ \\hline")    
print("Best occurence percent y")    
for longlat in dict(sorted(sum_y.items(), key=lambda item: item[1], reverse=True)): 
    if sum_rows[longlat] > 0:
        row_str = longlat + " & "
        for metric_name in ["simpson y", "trapz y"]:
            row_str += str(np.round(best_best[metric_name][longlat] / sum_cols[metric_name] * 100, 2)) + "\\% & "  
        print(row_str +  "\\\\ \\hline")    
print("Best occurence percent other total")    
for longlat in dict(sorted(sum_else.items(), key=lambda item: item[1], reverse=True)): 
    if sum_rows[longlat] > 0:
        row_str = longlat + " & "
        for metric_name in ["euclidean"]:
            row_str += str(np.round(best_best[metric_name][longlat] / sum_cols[metric_name] * 100, 2)) + "\\% & "  
        print(row_str + str(np.round(sum_rows[longlat] / sum_sum_cols * 100, 2)) + "\\% \\\\ \\hline")  
print("Worst occurence") 
first_row = ""
sum_cols = dict()
for metric_name in worst_worst:
    first_row += metric_name + " & "   
    sum_cols[metric_name] = 0            
print(first_row + "\\\\ \\hline") 
sum_rows = dict()
for longlat in worst_worst["euclidean"]:
    sum_row = 0
    row_str = longlat + " & "
    for metric_name in worst_worst:
        row_str += str(worst_worst[metric_name][longlat]) + " & "
        sum_row += worst_worst[metric_name][longlat]
        sum_cols[metric_name] += worst_worst[metric_name][longlat]
    sum_rows[longlat] = sum_row
    if sum_row > 0:
        print(row_str + str(sum_row) + " \\\\ \\hline")  
last_row = "" 
sum_sum_cols = 0
for metric_name in sum_cols:
    last_row += str(sum_cols[metric_name]) + " & "  
    sum_sum_cols += sum_cols[metric_name]
print(last_row + str(sum_sum_cols) + " \\\\ \\hline")  
print("Worst occurence percent")   
print(first_row + "\\\\ \\hline") 
for longlat in dict(sorted(sum_rows.items(), key=lambda item: item[1], reverse=False)): 
    if sum_rows[longlat] > 0:
        row_str = longlat + " & "
        for metric_name in worst_worst:
            row_str += str(np.round(worst_worst[metric_name][longlat] / sum_cols[metric_name] * 100, 2)) + "\\% & "  
        print(row_str + str(np.round(sum_rows[longlat] / sum_sum_cols * 100, 2)) + "\\% \\\\ \\hline")  
print(last_row + str(sum_sum_cols) + " \\\\ \\hline")  

'''
print("Best ride") 
first_row = ""
for metric_name in best_best_ride:
    first_row += metric_name + " & "         
print(first_row + "\\\\ \\hline") 
for longlat in best_best_ride["euclidean"]: 
    row_str = longlat + " & "
    for metric_name in best_best_ride:
        row_str += str(best_best_ride[metric_name][longlat]) + " & " 
    print(row_str + "\\\\ \\hline")               
print("Worst ride") 
first_row = ""
for metric_name in worst_worst_ride:
    first_row += metric_name + " & "         
print(first_row + "\\\\ \\hline") 
for longlat in worst_worst_ride["euclidean"]: 
    row_str = longlat + " & "
    for metric_name in worst_worst_ride:
        row_str += str(worst_worst_ride[metric_name][longlat]) + " & " 
    print(row_str + "\\\\ \\hline")                
print("Best for longlat") 
for longlat in best_best_ride["euclidean"]:  
    best_best_of = 1000000
    best_best_of_name = ""
    best_best_of_file = ""
    for metric_name in best_best_ride:
        if best_best_score[metric_name][longlat] < best_best_of:
            best_best_of = best_best_score[metric_name][longlat]
            best_best_of_name = metric_name
            best_best_of_file = best_best_ride[metric_name][longlat]
    print(" ", longlat, best_best_of_name, best_best_of, best_best_of_file)
print("Best for metric") 
for metric_name in best_best_ride:  
    best_best_of = 1000000
    best_best_of_name = ""
    best_best_of_file = ""
    for longlat in best_best_ride[metric_name]:
        if best_best_score[metric_name][longlat] < best_best_of:
            best_best_of = best_best_score[metric_name][longlat]
            best_best_of_name = longlat
            best_best_of_file = best_best_ride[metric_name][longlat]
    print(" ", metric_name, best_best_of_name, best_best_of, best_best_of_file) 
print("Worst for longlat")
for longlat in worst_worst_ride["euclidean"]:  
    worst_worst_of = -1000000
    worst_worst_of_name = ""
    worst_worst_of_file = ""
    for metric_name in best_best_ride:
        if worst_worst_score[metric_name][longlat] > worst_worst_of:
            worst_worst_of = worst_worst_score[metric_name][longlat]
            worst_worst_of_name = metric_name
            worst_worst_of_file = worst_worst_ride[metric_name][longlat]
    print(" ", longlat, worst_worst_of_name, worst_worst_of, worst_worst_of_file)
print("Worst for metric")
for metric_name in worst_worst_ride:  
    worst_worst_of = -1000000
    worst_worst_of_name = ""
    worst_worst_of_file = ""
    for longlat in worst_worst_ride[metric_name]:
        if worst_worst_score[metric_name][longlat] > worst_worst_of:
            worst_worst_of = worst_worst_score[metric_name][longlat]
            worst_worst_of_name = longlat
            worst_worst_of_file = worst_worst_ride[metric_name][longlat]
    print(" ", metric_name, worst_worst_of_name, worst_worst_of, worst_worst_of_file)
'''