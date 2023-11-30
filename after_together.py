from utilities import *  
  
all_subdirs = os.listdir()  

def new_metric(metric_name):
    new_metric_name = {"simpson x": "Simpsonova integracija x", "trapz x": "Integracija pomoću trapeza x", 
              "simpson y": "Simpsonova integracija y", "trapz y": "Integracija pomoću trapeza y",
              "euclidean": "Prosječna euklidska udaljenost"}
    if metric_name in new_metric_name:
        return new_metric_name[metric_name]
    else:
        return metric_name

def translate(longlat):
    translate_name = {
        "long no abs-lat no abs": "Pomak u x i y smjeru",
        "long-lat": "Apsolutna vrijednost pomaka u x i y smjeru",
        "long dist dir abs alt-lat dist dir abs alt": "Euklidska udaljenost i kut s osi x",
        "long dist dir-lat dist dir": "Euklidska udaljenost i odmak od sjevera",
        "long speed ones alt dir abs alt-lat speed ones alt dir abs alt": "Brzina na segmentu i kut s osi x, jedna sekunda",
        "x speed-y speed": "Apsolutna vrijednost brzine u x i y smjeru",
        "x speed no abs-y speed no abs": "Brzina u x i y smjeru",
        "long speed dir-lat speed dir": "Brzina u točki i odmak od sjevera",
        "long speed ones alt dir-lat speed ones alt dir": "Brzina na segmentu i odmak od sjevera, jedna sekunda",
        "long speed alt dir abs alt-lat speed alt dir abs alt": "Brzina na segmentu i kut s osi x",
        "long speed alt dir-lat speed alt dir": "Brzina na segmentu i odmak od sjevera",
        "long speed dir abs alt-lat speed dir abs alt": "Brzina u točki i kut s osi x",
        "x speed ones no abs-y speed ones no abs": "Brzina u x i y smjeru, jedna sekunda",
        "long speed ones dir-lat speed ones dir": "Brzina u točki i odmak od sjevera, jedna sekunda",
        "long speed ones dir abs alt-lat speed ones dir abs alt": "Brzina u točki i kut s osi x, jedna sekunda",
        "x speed ones-y speed ones": "Apsolutna vrijednost brzine u x i y smjeru, jedna sekunda",
        "long dist dir alt-lat dist dir alt": "Euklidska udaljenost i odmak od osi x",
        "long speed ones alt dir alt-lat speed ones alt dir alt": "Brzina na segmentu i odmak od osi x, jedna sekunda",
        "long speed ones dir alt-lat speed ones dir alt": "Brzina u točki i odmak od osi x, jedna sekunda",
        "long speed alt dir alt-lat speed alt dir alt": "Brzina na segmentu i odmak od osi x",
        "long speed dir alt-lat speed dir alt": "Brzina u točki i odmak od osi x",
    }
    if longlat in translate_name:
        return translate_name[longlat]
    else:
        return longlat

long_dict = load_object("markov_result/long_dict")
lat_dict = load_object("markov_result/lat_dict")
distance_predicted = load_object("markov_result/distance_predicted")

best_best = dict()
worst_worst = dict()
best_best_ride = dict()
worst_worst_ride = dict()
best_best_score = dict()
worst_worst_score = dict()

best_best_avg_ride = dict()
worst_worst_avg_ride = dict()
best_best_avg_score = dict()
worst_worst_avg_score = dict()

avg_for_ride_longlat = dict()

all_metrics = dict()
all_longs = dict()
all_lats = dict()
all_longlats = dict()
for vehicle in distance_predicted:
    avg_for_ride_longlat[vehicle] = dict() 
    for event in distance_predicted[vehicle]:  
        avg_for_ride_longlat[vehicle][event] = dict()
        for metric_name in distance_predicted[vehicle][event]:
            if "ray" in metric_name or "custom" in metric_name:
                continue
            if "no time" in metric_name or "custom" in metric_name:
                continue
            all_metrics[metric_name] = True
            for longlat in distance_predicted[vehicle][event][metric_name]:
                #if "ones" in longlat:
                    #continue
                if "actual" in longlat:
                    continue
                long = longlat.split("-")[0] 
                lat = long.replace("long", "lat").replace("x", "y")
                all_longs[long] = True
                all_lats[lat] = True
                all_longlats[long+"-"+lat] = True

for longlat in all_longlats: 
    best_best_avg_ride[longlat] = ""
    worst_worst_avg_ride[longlat] = ""
    best_best_avg_score[longlat] = 100000
    worst_worst_avg_score[longlat] = -100000
    for vehicle in distance_predicted:
        for event in distance_predicted[vehicle]:  
            avg_score = 0
            for metric_name in all_metrics:   
                avg_score += distance_predicted[vehicle][event][metric_name][longlat]
            avg_score /= len(all_metrics) 
            avg_for_ride_longlat[vehicle][event][longlat] = avg_score
            if avg_score < best_best_avg_score[longlat]:
                best_best_avg_score[longlat] = avg_score
                best_best_avg_ride[longlat] = vehicle + "/" + event  
            if avg_score > worst_worst_avg_score[longlat]:
                worst_worst_avg_score[longlat] = avg_score
                worst_worst_avg_ride[longlat] = vehicle + "/" + event  

count_best_by_avg = dict()
count_worst_by_avg = dict()
for longlat in all_longlats: 
    count_best_by_avg[longlat] = 0
    count_worst_by_avg[longlat] = 0

for vehicle in avg_for_ride_longlat:
    for event in avg_for_ride_longlat[vehicle]:  
        bestlonglat = 100000
        worstlonglat = -100000
        bestlonglatname = ""
        worstlonglatname = "" 
        for longlat in avg_for_ride_longlat[vehicle][event]: 
            if avg_for_ride_longlat[vehicle][event][longlat] < bestlonglat:
                bestlonglat = avg_for_ride_longlat[vehicle][event][longlat]
                bestlonglatname = longlat
            if avg_for_ride_longlat[vehicle][event][longlat] > worstlonglat:
                worstlonglat = avg_for_ride_longlat[vehicle][event][longlat]
                worstlonglatname = longlat 
        count_best_by_avg[bestlonglatname] += 1
        count_worst_by_avg[worstlonglatname] += 1
        
for metric_name in all_metrics:   
    best_best[metric_name] = dict()
    worst_worst[metric_name] = dict()
    best_best_ride[metric_name] = dict()
    worst_worst_ride[metric_name] = dict()
    best_best_score[metric_name] = dict()
    worst_worst_score[metric_name] = dict()
    longlats = set()
    for longlat in all_longlats:   
        best_best[metric_name][longlat] = 0
        worst_worst[metric_name][longlat] = 0
        best_best_ride[metric_name][longlat] = ""
        worst_worst_ride[metric_name][longlat] = ""
        best_best_score[metric_name][longlat] = 100000
        worst_worst_score[metric_name][longlat] = -100000
    for vehicle in distance_predicted:
        for event in distance_predicted[vehicle]:  
            minmetric = 100000
            minname = ""  
            bestride = ""
            maxmetric = -100000
            maxname = ""
            worstride = ""
            for longlat in all_longlats:
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

print("Worst occurence") 
first_row = ""
sum_cols = dict()
for metric_name in worst_worst:
    first_row += metric_name + " & "   
    sum_cols[metric_name] = 0            
print(first_row + "\\\\ \\hline") 
sum_rows = dict()
sum_x = dict()
sum_y = dict()
sum_else = dict()
for longlat in worst_worst["euclidean"]:
    sum_x[longlat] = 0
    sum_y[longlat] = 0
    sum_else[longlat] = 0 
for longlat in worst_worst["euclidean"]:
    sum_row = 0
    row_str = translate(longlat) + " & "
    for metric_name in worst_worst:
        row_str += str(translate(worst_worst[metric_name][longlat])) + " & "
        sum_row += worst_worst[metric_name][longlat]
        sum_cols[metric_name] += worst_worst[metric_name][longlat]
        if " x" in metric_name:
            sum_x[longlat] += worst_worst[metric_name][longlat]
        if " y" in metric_name:
            sum_y[longlat] += worst_worst[metric_name][longlat]
        if " y" not in metric_name and " x" not in metric_name:
            sum_else[longlat] += worst_worst[metric_name][longlat]
    sum_rows[longlat] = sum_row
    if sum_row > 0:
        print(row_str + "$" + str(sum_row) + "$ \\\\ \\hline")  
last_row = "" 
sum_sum_cols = 0
for metric_name in sum_cols:
    last_row += "$" + str(sum_cols[metric_name]) + "$ & "  
    sum_sum_cols += sum_cols[metric_name]
print(last_row + str(sum_sum_cols) + " \\\\ \\hline")  

print("Worst occurence percent")   
print(first_row + "\\\\ \\hline") 
for longlat in dict(sorted(sum_rows.items(), key=lambda item: item[1])): 
    if sum_rows[longlat] > 0:
        row_str = translate(longlat) + " & "
        for metric_name in worst_worst:
            row_str += "$" + str(round(worst_worst[metric_name][longlat] / sum_cols[metric_name] * 100, 2)) + "\\%$ & "  
        print(row_str + "$" + str(np.round(sum_rows[longlat] / sum_sum_cols * 100, 2)) + "\\%$ \\\\ \\hline")  
print(last_row + str(sum_sum_cols) + " \\\\ \\hline")   

print("Worst occurence percent x y")    
for longlat in dict(sorted(sum_x.items(), key=lambda item: item[1])): 
    if sum_rows[longlat] > 0:
        row_str = translate(longlat) + " & "
        for metric_name in ["simpson x", "trapz x"]:
            row_str += "$" + str(round(worst_worst[metric_name][longlat] / sum_cols[metric_name] * 100, 2)) + "\\%$ & "  
        row_str += "$" + str(round(sum_x[longlat] / 2 / sum_cols[metric_name] * 100, 2)) + "\\%$ "  
        for metric_name in ["simpson y", "trapz y"]:
            row_str += "$" + str(round(worst_worst[metric_name][longlat] / sum_cols[metric_name] * 100, 2)) + "\\%$ & "  
        row_str += "$" + str(round(sum_y[longlat] / 2 / sum_cols[metric_name] * 100, 2)) + "\\%$ "  
        row_str += "$" + str(round((sum_x[longlat] + sum_y[longlat]) / 4 / sum_cols[metric_name] * 100, 2)) + "\\%$ "  
        print(row_str +  "\\\\ \\hline")   

print("Worst occurence percent x")   
for longlat in dict(sorted(sum_x.items(), key=lambda item: item[1])): 
    if sum_rows[longlat] > 0:
        row_str = translate(longlat) + " & "
        for metric_name in ["simpson x", "trapz x"]:
            row_str += "$" + str(round(worst_worst[metric_name][longlat] / sum_cols[metric_name] * 100, 2)) + "\\%$ & "  
        row_str += "$" + str(round(sum_x[longlat] / 2 / sum_cols[metric_name] * 100, 2)) + "\\%$ "  
        print(row_str + "\\\\ \\hline")    

print("Worst occurence percent y")    
for longlat in dict(sorted(sum_y.items(), key=lambda item: item[1])): 
    if sum_rows[longlat] > 0:
        row_str = translate(longlat) + " & "
        for metric_name in ["simpson y", "trapz y"]:
            row_str += "$" + str(round(worst_worst[metric_name][longlat] / sum_cols[metric_name] * 100, 2)) + "\\%$ & " 
        row_str += "$" + str(round(sum_y[longlat] / 2 / sum_cols[metric_name] * 100, 2)) + "\\%$ "   
        print(row_str +  "\\\\ \\hline")   

print("Worst occurence percent other")    
for longlat in dict(sorted(sum_else.items(), key=lambda item: item[1])): 
    if sum_rows[longlat] > 0:
        row_str = translate(longlat) + " & "
        for metric_name in ["euclidean"]:
            row_str += "$" + str(round(worst_worst[metric_name][longlat] / sum_cols[metric_name] * 100, 2)) + "\\%$ & "  
        print(row_str + "$" + str(np.round(sum_rows[longlat] / sum_sum_cols * 100, 2)) + "\\%$ \\\\ \\hline")  
        
print("Worst occurence percent average")    
for longlat in dict(sorted(count_worst_by_avg.items(), key=lambda item: item[1])):  
    if sum_rows[longlat] > 0:
        row_str = translate(longlat) + " & "
        row_str += "$" + str(count_worst_by_avg[longlat]) + "$ & "
        row_str += "$" + str(round(count_worst_by_avg[longlat] / sum(list(count_worst_by_avg.values())) * 100, 2)) + "\\%$ \\\\hline"
        print(row_str)

print("Worst occurence percent other total")    
for longlat in dict(sorted(sum_else.items(), key=lambda item: item[1])): 
    if sum_rows[longlat] > 0:
        row_str = translate(longlat) + " & "
        for metric_name in ["euclidean"]:
            row_str += "$" + str(round(worst_worst[metric_name][longlat] / sum_cols[metric_name] * 100, 2)) + "\\%$ & "  
        row_str += "$" + str(round(count_worst_by_avg[longlat] / sum(list(count_worst_by_avg.values())) * 100, 2)) + "\\%$ & "
        print(row_str + "$" + str(np.round(sum_rows[longlat] / sum_sum_cols * 100, 2)) + "\\%$ \\\\ \\hline")
  
#print("Worst ride") 
first_row = ""
for metric_name in worst_worst_ride:
    first_row += metric_name + " & "         
#print(first_row + "\\\\ \\hline") 

worst_scores_for_longlat_all = [] 
worst_subs_for_longlat_all = [] 
worst_longs_for_longlat_all = [] 
worst_lats_for_longlat_all = []    
worst_other_longs_for_longlat_all = [] 
worst_other_lats_for_longlat_all = []  

for metric_name in worst_worst_ride: 
    worst_scores_for_longlat_all.append(100000)
    worst_subs_for_longlat_all.append("")
    worst_longs_for_longlat_all.append([])
    worst_lats_for_longlat_all.append([])
    worst_other_longs_for_longlat_all.append([])
    worst_other_lats_for_longlat_all.append([])
worst_scores_for_longlat_all.append(100000)
worst_subs_for_longlat_all.append("")
worst_longs_for_longlat_all.append([])
worst_lats_for_longlat_all.append([])
worst_other_longs_for_longlat_all.append([])
worst_other_lats_for_longlat_all.append([])

for longlat in worst_worst_ride["euclidean"]: 
    worst_worst_of = 1000000 
    
    row_str = translate(longlat) + " & "  
    worst_subs_for_longlat = [] 
    worst_longs_for_longlat = [] 
    worst_lats_for_longlat = []    
    worst_other_longs_for_longlat = [] 
    worst_other_lats_for_longlat = []  
    
    ix = 0
    for metric_name in worst_worst_ride: 
        row_str += str(translate(worst_worst_ride[metric_name][longlat])) + " & "
        longer_name = worst_worst_ride[metric_name][longlat].replace("/", "/cleaned_csv/")
        long, lat, time = load_traj_name(longer_name)
        long, lat = preprocess_long_lat(long, lat)
        long, lat = scale_long_lat(long, lat, 0.1, 0.1)
        process_ride = worst_worst_ride[metric_name][longlat].replace("/events_", " Vožnja ").replace(".csv", "").replace("Vehicle_", "Vozilo ")
        
        worst_subs_for_longlat.append(translate(longlat) + "\n" + new_metric(metric_name) + " = " + str(np.round(worst_worst_score[metric_name][longlat], 5)) + "\n" + process_ride)
        worst_longs_for_longlat.append(long)
        worst_lats_for_longlat.append(lat) 
        worst_other_longs_for_longlat.append([long_dict[longer_name][longlat.split("-")[0]]])
        worst_other_lats_for_longlat.append([lat_dict[longer_name][longlat.split("-")[1]]])

        if worst_worst_score[metric_name][longlat] < worst_scores_for_longlat_all[ix]:
            worst_subs_for_longlat_all[ix] = translate(longlat) + "\n" + new_metric(metric_name) + " = " + str(np.round(worst_worst_score[metric_name][longlat], 5)) + "\n" + process_ride
            worst_longs_for_longlat_all[ix] = long 
            worst_lats_for_longlat_all[ix] = lat  
            worst_other_longs_for_longlat_all[ix] = [long_dict[longer_name][longlat.split("-")[0]]] 
            worst_other_lats_for_longlat_all[ix] = [lat_dict[longer_name][longlat.split("-")[1]]] 
            worst_scores_for_longlat_all[ix] = worst_worst_score[metric_name][longlat]

        ix += 1
      
    longer_name = worst_worst_avg_ride[longlat].replace("/", "/cleaned_csv/")
    long, lat, time = load_traj_name(longer_name)
    long, lat = preprocess_long_lat(long, lat)
    long, lat = scale_long_lat(long, lat, 0.1, 0.1)
    process_ride = worst_worst_avg_ride[longlat].replace("/events_", " Vožnja ").replace(".csv", "").replace("Vehicle_", "Vozilo ")
    worst_subs_for_longlat.append(translate(longlat) + "\nProsjek = " + str(np.round(worst_worst_avg_score[longlat], 5)) +  "\n" + process_ride)
    worst_longs_for_longlat.append(long)
    worst_lats_for_longlat.append(lat) 
    worst_other_longs_for_longlat.append([long_dict[longer_name][longlat.split("-")[0]]])
    worst_other_lats_for_longlat.append([lat_dict[longer_name][longlat.split("-")[1]]])
    
    if worst_worst_score[metric_name][longlat] < worst_scores_for_longlat_all[ix]: 
        worst_subs_for_longlat_all[ix] = translate(longlat) + "\nProsjek = " + str(np.round(worst_worst_avg_score[longlat], 5)) +  "\n" + process_ride
        worst_longs_for_longlat_all[ix] = long
        worst_lats_for_longlat_all[ix] = lat
        worst_other_longs_for_longlat_all[ix] = [long_dict[longer_name][longlat.split("-")[0]]]
        worst_other_lats_for_longlat_all[ix] = [lat_dict[longer_name][longlat.split("-")[1]]] 
        worst_scores_for_longlat_all[ix] = worst_worst_avg_score[longlat]

    if not os.path.isdir("markov_rides"):
        os.makedirs("markov_rides")
    filename = "markov_rides/" + longlat + "_worst.png"

    composite_image(filename, worst_longs_for_longlat, worst_lats_for_longlat, 3, 2, worst_other_longs_for_longlat, worst_other_lats_for_longlat, ["Procjena"], True, worst_subs_for_longlat)
    #print(row_str + "\\\\ \\hline")      
composite_image("markov_rides/A_worst.png", worst_longs_for_longlat_all, worst_lats_for_longlat_all, 3, 2, worst_other_longs_for_longlat_all, worst_other_lats_for_longlat_all, ["Procjena"], True, worst_subs_for_longlat_all)

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
    row_str = translate(longlat) + " & "
    for metric_name in best_best:
        row_str += str(translate(best_best[metric_name][longlat])) + " & "
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
        print(row_str + "$" + str(sum_row) + "$ \\\\ \\hline")  
last_row = "" 
sum_sum_cols = 0
for metric_name in sum_cols:
    last_row += "$" + str(sum_cols[metric_name]) + "$ & "  
    sum_sum_cols += sum_cols[metric_name]
print(last_row + str(sum_sum_cols) + " \\\\ \\hline")  

print("Best occurence percent")   
print(first_row + "\\\\ \\hline") 
for longlat in dict(sorted(sum_rows.items(), key=lambda item: item[1], reverse=True)): 
    if sum_rows[longlat] > 0:
        row_str = translate(longlat) + " & "
        for metric_name in best_best:
            row_str += "$" + str(round(best_best[metric_name][longlat] / sum_cols[metric_name] * 100, 2)) + "\\%$ & "  
        print(row_str + "$" + str(np.round(sum_rows[longlat] / sum_sum_cols * 100, 2)) + "\\%$ \\\\ \\hline")  
print(last_row + str(sum_sum_cols) + " \\\\ \\hline")   

print("Best occurence percent x y")   
for longlat in dict(sorted(sum_x.items(), key=lambda item: item[1], reverse=True)): 
    if sum_rows[longlat] > 0:
        row_str = translate(longlat) + " & "
        for metric_name in ["simpson x", "trapz x"]:
            row_str += "$" + str(round(best_best[metric_name][longlat] / sum_cols[metric_name] * 100, 2)) + "\\%$ & " 
        row_str += "$" + str(round(sum_x[longlat] / 2 / sum_cols[metric_name] * 100, 2)) + "\\%$ & "   
        for metric_name in ["simpson y", "trapz y"]:
            row_str += "$" + str(round(best_best[metric_name][longlat] / sum_cols[metric_name] * 100, 2)) + "\\%$ & " 
        row_str += "$" + str(round(sum_y[longlat] / 2 / sum_cols[metric_name] * 100, 2)) + "\\%$ & "     
        row_str += "$" + str(round((sum_x[longlat] + sum_y[longlat]) / 4 / sum_cols[metric_name] * 100, 2)) + "\\%$ "     
        print(row_str + "\\\\ \\hline")   

print("Best occurence percent x")   
for longlat in dict(sorted(sum_x.items(), key=lambda item: item[1], reverse=True)): 
    if sum_rows[longlat] > 0:
        row_str = translate(longlat) + " & "
        for metric_name in ["simpson x", "trapz x"]:
            row_str += "$" + str(round(best_best[metric_name][longlat] / sum_cols[metric_name] * 100, 2)) + "\\%$ & " 
        row_str += "$" + str(round(sum_x[longlat] / 2 / sum_cols[metric_name] * 100, 2)) + "\\%$ "   
        print(row_str + "\\\\ \\hline")    

print("Best occurence percent y")    
for longlat in dict(sorted(sum_y.items(), key=lambda item: item[1], reverse=True)): 
    if sum_rows[longlat] > 0:
        row_str = translate(longlat) + " & "
        for metric_name in ["simpson y", "trapz y"]:
            row_str += "$" + str(round(best_best[metric_name][longlat] / sum_cols[metric_name] * 100, 2)) + "\\%$ & "  
        row_str += "$" + str(round(sum_y[longlat] / 2 / sum_cols[metric_name] * 100, 2)) + "\\%$ "  
        print(row_str +  "\\\\ \\hline")    

print("Best occurence percent other")    
for longlat in dict(sorted(sum_else.items(), key=lambda item: item[1], reverse=True)): 
    if sum_rows[longlat] > 0:
        row_str = translate(longlat) + " & "
        for metric_name in ["euclidean"]:
            row_str += "$" + str(round(best_best[metric_name][longlat] / sum_cols[metric_name] * 100, 2)) + "\\%$ & "  
        print(row_str + "$" + str(np.round(sum_rows[longlat] / sum_sum_cols * 100, 2)) + "\\%$ \\\\ \\hline")  

print("Best occurence percent average")    
for longlat in dict(sorted(count_best_by_avg.items(), key=lambda item: item[1], reverse=True)): 
    if sum_rows[longlat] > 0: 
        row_str = translate(longlat) + " & "
        row_str += "$" + str(count_best_by_avg[longlat]) + "$ & "
        row_str += "$" + str(round(count_best_by_avg[longlat] / sum(list(count_best_by_avg.values())) * 100, 2)) + "\\%$ \\\\hline"
        print(row_str)

print("Best occurence percent other total")    
for longlat in dict(sorted(sum_else.items(), key=lambda item: item[1], reverse=True)): 
    if sum_rows[longlat] > 0:
        row_str = translate(longlat) + " & "
        for metric_name in ["euclidean"]:
            row_str += "$" + str(round(best_best[metric_name][longlat] / sum_cols[metric_name] * 100, 2)) + "\\%$ & "  
        row_str += "$" + str(round(count_best_by_avg[longlat] / sum(list(count_best_by_avg.values())) * 100, 2)) + "\\%$ & "
        print(row_str + "$" + str(np.round(sum_rows[longlat] / sum_sum_cols * 100, 2)) + "\\%$ \\\\ \\hline")  
  
#print("Best ride") 
first_row = ""
for metric_name in best_best_ride:
    first_row += metric_name + " & "         
#print(first_row + "\\\\ \\hline") 

best_scores_for_longlat_all = [] 
best_subs_for_longlat_all = [] 
best_longs_for_longlat_all = [] 
best_lats_for_longlat_all = []    
best_other_longs_for_longlat_all = [] 
best_other_lats_for_longlat_all = []  

for metric_name in best_best_ride: 
    best_scores_for_longlat_all.append(100000)
    best_subs_for_longlat_all.append("")
    best_longs_for_longlat_all.append([])
    best_lats_for_longlat_all.append([])
    best_other_longs_for_longlat_all.append([])
    best_other_lats_for_longlat_all.append([])
best_scores_for_longlat_all.append(100000)
best_subs_for_longlat_all.append("")
best_longs_for_longlat_all.append([])
best_lats_for_longlat_all.append([])
best_other_longs_for_longlat_all.append([])
best_other_lats_for_longlat_all.append([])

for longlat in best_best_ride["euclidean"]: 
    best_best_of = 1000000 
    
    row_str = translate(longlat) + " & "  
    best_subs_for_longlat = [] 
    best_longs_for_longlat = [] 
    best_lats_for_longlat = []    
    best_other_longs_for_longlat = [] 
    best_other_lats_for_longlat = []  
    
    ix = 0
    for metric_name in best_best_ride: 
        row_str += str(translate(best_best_ride[metric_name][longlat])) + " & "
        longer_name = best_best_ride[metric_name][longlat].replace("/", "/cleaned_csv/")
        long, lat, time = load_traj_name(longer_name)
        long, lat = preprocess_long_lat(long, lat)
        long, lat = scale_long_lat(long, lat, 0.1, 0.1)
        process_ride = best_best_ride[metric_name][longlat].replace("/events_", " Vožnja ").replace(".csv", "").replace("Vehicle_", "Vozilo ")
        
        best_subs_for_longlat.append(translate(longlat) + "\n" + new_metric(metric_name) + " = " + str(np.round(best_best_score[metric_name][longlat], 5)) + "\n" + process_ride)
        best_longs_for_longlat.append(long)
        best_lats_for_longlat.append(lat) 
        best_other_longs_for_longlat.append([long_dict[longer_name][longlat.split("-")[0]]])
        best_other_lats_for_longlat.append([lat_dict[longer_name][longlat.split("-")[1]]])

        if best_best_score[metric_name][longlat] < best_scores_for_longlat_all[ix]:
            best_subs_for_longlat_all[ix] = translate(longlat) + "\n" + new_metric(metric_name) + " = " + str(np.round(best_best_score[metric_name][longlat], 5)) + "\n" + process_ride
            best_longs_for_longlat_all[ix] = long 
            best_lats_for_longlat_all[ix] = lat  
            best_other_longs_for_longlat_all[ix] = [long_dict[longer_name][longlat.split("-")[0]]] 
            best_other_lats_for_longlat_all[ix] = [lat_dict[longer_name][longlat.split("-")[1]]] 
            best_scores_for_longlat_all[ix] = best_best_score[metric_name][longlat]

        ix += 1
      
    longer_name = best_best_avg_ride[longlat].replace("/", "/cleaned_csv/")
    long, lat, time = load_traj_name(longer_name)
    long, lat = preprocess_long_lat(long, lat)
    long, lat = scale_long_lat(long, lat, 0.1, 0.1)
    process_ride = best_best_avg_ride[longlat].replace("/events_", " Vožnja ").replace(".csv", "").replace("Vehicle_", "Vozilo ")
    best_subs_for_longlat.append(translate(longlat) + "\nProsjek = " + str(np.round(best_best_avg_score[longlat], 5)) +  "\n" + process_ride)
    best_longs_for_longlat.append(long)
    best_lats_for_longlat.append(lat) 
    best_other_longs_for_longlat.append([long_dict[longer_name][longlat.split("-")[0]]])
    best_other_lats_for_longlat.append([lat_dict[longer_name][longlat.split("-")[1]]])
    
    if best_best_score[metric_name][longlat] < best_scores_for_longlat_all[ix]: 
        best_subs_for_longlat_all[ix] = translate(longlat) + "\nProsjek = " + str(np.round(best_best_avg_score[longlat], 5)) +  "\n" + process_ride
        best_longs_for_longlat_all[ix] = long
        best_lats_for_longlat_all[ix] = lat
        best_other_longs_for_longlat_all[ix] = [long_dict[longer_name][longlat.split("-")[0]]]
        best_other_lats_for_longlat_all[ix] = [lat_dict[longer_name][longlat.split("-")[1]]] 
        best_scores_for_longlat_all[ix] = best_best_avg_score[longlat]

    if not os.path.isdir("markov_rides"):
        os.makedirs("markov_rides")
    filename = "markov_rides/" + longlat + "_best.png"

    composite_image(filename, best_longs_for_longlat, best_lats_for_longlat, 3, 2, best_other_longs_for_longlat, best_other_lats_for_longlat, ["Procjena"], True, best_subs_for_longlat)
    #print(row_str + "\\\\ \\hline")      
composite_image("markov_rides/A_best.png", best_longs_for_longlat_all, best_lats_for_longlat_all, 3, 2, best_other_longs_for_longlat_all, best_other_lats_for_longlat_all, ["Procjena"], True, best_subs_for_longlat_all)

'''  
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