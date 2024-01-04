from utilities import *  
  
all_subdirs = os.listdir()   
     
def str_convert(val):
    if val == False:
        return "0"
    if val == True:
        return "1"
    new_val = val
    power_to = 0
    while abs(new_val) < 1 and new_val != 0.0:
        new_val *= 10
        power_to += 1 
    rounded = str(np.round(new_val, 2))
    if rounded[-2:] == '.0':
        rounded = rounded[:-2]
    if power_to != 0:  
        rounded += " \\times 10^{-" + str(power_to) + "}"
    return rounded

def print_row(header_val, no_gap_val, int_val):
    middle_sec = translate_var[header_val.replace("predicted_", "").replace("_", " ").replace("alternative", "alt").replace("x speed alt", "x speed").replace("y speed alt", "y speed").replace("speed no abs alt", "speed no abs").capitalize()]
    if len(middle_sec) > 20:
        nh = middle_sec[:20]
    else:
        nh = "\\multirow{2}{*}{" + middle_sec + "}"
    nh += " & lanac" 
    for v in no_gap_val:
        nh += " & $" + str_convert(v) + "$"
    nh += " \\\\ \cline{2-" + str(len(no_gap_val) + 2) + "}\n" 
    if len(middle_sec) > 20:
        nh += middle_sec[20:] 
    nh += " & realno"  
    for v in int_val:
        nh += " & $" + str_convert(v) + "$"
    nh += " \\\\ \hline\n" 
    print(nh)
    return nh

def print_method(long, lat, newx):
    middle_sec = "Original"
    if long != "":
        middle_sec = translate_method(long + "-" + lat) 
    nh = middle_sec.replace("x", "$x$").replace("y", "$y$") 
    for v in newx:
        nh += " & $" + str_convert(v) + "$"
    nh += " \\\\ \hline\n"   
    print(nh)
    return nh

predicted_time = load_object("predicted/predicted_time")  
predicted_distance = load_object("predicted/predicted_distance")  
predicted_longitude = load_object("predicted/predicted_longitude")  
predicted_latitude = load_object("predicted/predicted_latitude")  
predicted_longitude_sgn = load_object("predicted/predicted_longitude_sgn")  
predicted_latitude_sgn = load_object("predicted/predicted_latitude_sgn")  
predicted_longitude_no_abs = load_object("predicted/predicted_longitude_no_abs")  
predicted_latitude_no_abs = load_object("predicted/predicted_latitude_no_abs")  
predicted_direction = load_object("predicted/predicted_direction")  
predicted_direction_alternative = load_object("predicted/predicted_direction_alternative")
predicted_direction_abs_alternative = load_object("predicted/predicted_direction_abs_alternative")
predicted_speed = load_object("predicted/predicted_speed")  
predicted_speed_alternative = load_object("predicted/predicted_speed_alternative")  
predicted_x_speed_alternative = load_object("predicted/predicted_x_speed_alternative")  
predicted_y_speed_alternative = load_object("predicted/predicted_y_speed_alternative")  
predicted_x_speed_no_abs_alternative = load_object("predicted/predicted_x_speed_no_abs_alternative")  
predicted_y_speed_no_abs_alternative = load_object("predicted/predicted_y_speed_no_abs_alternative")  

long_dict = load_object("markov_result/long_dict")
lat_dict = load_object("markov_result/lat_dict")
distance_predicted = load_object("markov_result/distance_predicted")
  
def plot_trapezoid(f, g, x, str_pr, filename):  
    l1 = [i for i in np.arange(min(min(f), min(g)) - 0.0001, min(f[0], g[0]) + 0.00001, 0.00001)]
    x1 = [x[0] for i in np.arange(min(min(f), min(g)) - 0.0001, min(f[0], g[0]) + 0.00001, 0.00001)]
    l2 = [i for i in np.arange(min(min(f), min(g)) - 0.0001, max(f[-1], g[-1]) + 0.00001, 0.00001)]
    x2 = [x[-1] for i in np.arange(min(min(f), min(g)) - 0.0001, max(f[-1], g[-1]) + 0.00001, 0.00001)]
    l5 = [i for i in np.arange(min(min(f), min(g)) - 0.0001, f[-1] + 0.00001, 0.00001)]
    x5 = [x[-1] for i in np.arange(min(min(f), min(g)) - 0.0001, f[-1] + 0.00001, 0.00001)]
    l6 = [i for i in np.arange(min(min(f), min(g)) - 0.0001, g[-1] + 0.00001, 0.00001)]
    x6 = [x[-1] for i in np.arange(min(min(f), min(g)) - 0.0001, g[-1] + 0.00001, 0.00001)]
    x3 = [v for v in np.arange(x[0], x[-1] + 0.0001, 0.0001)]
    s2 = [0 for v in x3] 
    s = [min(min(f), min(g)) - 0.0001 for v in x3] 
    df = [abs(f[i] - g[i]) for i in range(len(x))]
    l4 = [i for i in np.arange(0, df[-1] + 0.00001, 0.00001)]
    x4 = [x[-1] for i in np.arange(0, df[-1] + 0.00001, 0.00001)] 
    diff = 1000
    for ixix in range(len(x)):
        if abs(x[ixix] - 25) < diff:
            diff = abs(x[ixix] - 25) 
            ix = ixix 
    plt.rcParams['font.size'] = 20
    plt.rcParams['font.family'] = "serif"
    plt.rcParams["mathtext.fontset"] = "dejavuserif"
    plt.figure(figsize=(20, 7))
    plt.subplot(1, 2, 1)
    plt.xlabel("$t$")
    plt.ylabel('$' + str_pr[2] + '$')  
    #for ixix in range(len(x)): 
        #plt.plot([x[ixix], x[ixix]], [f[ixix], g[ixix]], c = "c") 
    plt.plot(x, f, label = "f", c = "r")
    if f[ix] > g[ix]:  
        plt.text(x[ix], f[ix] + 0.00031, '$f' + str_pr + '$', size=20, color='r')
    else:    
        plt.text(x[ix], f[ix] - 0.00015, '$f' + str_pr + '$', size=20, color='r')
    plt.ylim(min(min(f), min(g)), max(max(f), max(g)) + 0.0001)
    plt.plot(x, g, label = "g", c = "b")
    if g[ix] > f[ix]:  
        plt.text(x[ix], g[ix] + 0.00026, '$g' + str_pr + '$', size=20, color='b')
    else:    
        plt.text(x[ix], g[ix] - 0.00036, '$g' + str_pr + '$', size=20, color='b')
    plt.text(x[ix], (f[ix] + g[ix]) / 2, '$A$', size=20, color='k')
    if f[-1] < g[-1]:
        plt.plot(x1, l1, c = "r")
    else:
        plt.plot(x1, l1, c = "b")
    if f[-1] < g[-1]:
        plt.plot(x6, l6, c = "b")
        plt.plot(x5, l5, c = "r")
    else:
        plt.plot(x5, l5, c = "r")
        plt.plot(x6, l6, c = "b")
    if f[-1] < g[-1]:
        plt.plot(x3, s, c = "r") 
    else:
        plt.plot(x3, s, c = "b")
    plt.subplot(1, 2, 2) 
    plt.xlabel("$t$")
    plt.ylabel('$' + str_pr[2] + '$')  
    plt.plot(x, df, c = "magenta") 
    plt.ylim(- 0.0001, max(max(f), max(g)) + 0.0001 - min(min(f), min(g)) + 0.0001) 
    plt.plot(x4, l4, c = "magenta")
    plt.text(x[ix], df[ix] / 2, '$A$', size=20, color='k')
    plt.text(x[ix], df[ix] + 0.0005, '$|f' + str_pr + '-g' + str_pr + '|$', size=20, color='magenta')
    plt.plot(x3, s2, c = "magenta")
    plt.savefig("presentation_plots/" + filename + ".png", bbox_inches = "tight")
    plt.close()
    plot_trapezoid_left(f, g, x, str_pr, filename)
    
def plot_trapezoid_left(f, g, x, str_pr, filename):  
    l1 = [i for i in np.arange(min(min(f), min(g)) - 0.0001, min(f[0], g[0]) + 0.00001, 0.00001)]
    x1 = [x[0] for i in np.arange(min(min(f), min(g)) - 0.0001, min(f[0], g[0]) + 0.00001, 0.00001)]
    l2 = [i for i in np.arange(min(min(f), min(g)) - 0.0001, max(f[-1], g[-1]) + 0.00001, 0.00001)]
    x2 = [x[-1] for i in np.arange(min(min(f), min(g)) - 0.0001, max(f[-1], g[-1]) + 0.00001, 0.00001)]
    l5 = [i for i in np.arange(min(min(f), min(g)) - 0.0001, f[-1] + 0.00001, 0.00001)]
    x5 = [x[-1] for i in np.arange(min(min(f), min(g)) - 0.0001, f[-1] + 0.00001, 0.00001)]
    l6 = [i for i in np.arange(min(min(f), min(g)) - 0.0001, g[-1] + 0.00001, 0.00001)]
    x6 = [x[-1] for i in np.arange(min(min(f), min(g)) - 0.0001, g[-1] + 0.00001, 0.00001)]
    x3 = [v for v in np.arange(x[0], x[-1] + 0.0001, 0.0001)]
    s2 = [0 for v in x3] 
    s = [min(min(f), min(g)) - 0.0001 for v in x3] 
    df = [abs(f[i] - g[i]) for i in range(len(x))]
    l4 = [i for i in np.arange(0, df[-1] + 0.00001, 0.00001)]
    x4 = [x[-1] for i in np.arange(0, df[-1] + 0.00001, 0.00001)] 
    diff = 1000
    for ixix in range(len(x)):
        if abs(x[ixix] - 25) < diff:
            diff = abs(x[ixix] - 25) 
            ix = ixix 
    plt.rcParams['font.size'] = 20
    plt.rcParams['font.family'] = "serif"
    plt.rcParams["mathtext.fontset"] = "dejavuserif"  
    plt.xlabel("$t$")
    plt.ylabel('$' + str_pr[2] + '$')  
    #for ixix in range(len(x)): 
        #plt.plot([x[ixix], x[ixix]], [f[ixix], g[ixix]], c = "c") 
    plt.plot(x, f, label = "f", c = "r")
    if f[ix] > g[ix]:  
        plt.text(x[ix], f[ix] + 0.00041, '$f' + str_pr + '$', size=20, color='r')
    else:    
        plt.text(x[ix], f[ix] - 0.00025, '$f' + str_pr + '$', size=20, color='r')
    plt.ylim(min(min(f), min(g)), max(max(f), max(g)) + 0.0001)
    plt.plot(x, g, label = "g", c = "b")
    if g[ix] > f[ix]:  
        plt.text(x[ix], g[ix] + 0.00044, '$g' + str_pr + '$', size=20, color='b')
    else:    
        plt.text(x[ix], g[ix] - 0.00053, '$g' + str_pr + '$', size=20, color='b')
    plt.text(x[ix], (f[ix] + g[ix]) / 2, '$A$', size=20, color='k')
    if f[-1] < g[-1]:
        plt.plot(x1, l1, c = "r")
    else:
        plt.plot(x1, l1, c = "b")
    if f[-1] < g[-1]:
        plt.plot(x6, l6, c = "b")
        plt.plot(x5, l5, c = "r")
    else:
        plt.plot(x5, l5, c = "r")
        plt.plot(x6, l6, c = "b")
    if f[-1] < g[-1]:
        plt.plot(x3, s, c = "r") 
    else:
        plt.plot(x3, s, c = "b") 
    plt.savefig("presentation_plots/" + filename + "_left.png", bbox_inches = "tight")
    plt.close()
    
def plot_all(fx, fy, gx, gy, maxnum, filename):  
    plt.rcParams['font.size'] = 15 
    for i in range(len(fx[:maxnum])):  
        plt.plot([fx[i], gx[i]], [fy[i], gy[i]], color='k')
        if i == 0:
            if fy[i] > gy[i]:
                plt.text(fx[i] - 0.0002, fy[i] + 0.00007,'$f_{' + str(i + 1) + '}$', size=15, color='r')
                plt.text(gx[i] - 0.0002, gy[i] - 0.00006, '$g_{' + str(i + 1) + '}$', size=15, color='b')
            else:
                plt.text(fx[i] - 0.0002, fy[i] - 0.00007,'$f_{' + str(i + 1) + '}$', size=15, color='r')
                plt.text(gx[i] - 0.0002, gy[i] + 0.00006, '$g_{' + str(i + 1) + '}$', size=15, color='b')
        else:
            if fy[i] > gy[i]:
                plt.text(fx[i], fy[i] + 0.00007,'$f_{' + str(i + 1) + '}$', size=15, color='r')
                plt.text(gx[i], gy[i] - 0.00006, '$g_{' + str(i + 1) + '}$', size=15, color='b')
            else:
                plt.text(fx[i], fy[i] - 0.00007,'$f_{' + str(i + 1) + '}$', size=15, color='r')
                plt.text(gx[i] - 0.0001, gy[i] + 0.00006, '$g_{' + str(i + 1) + '}$', size=15, color='b')
    plt.plot(fx[:maxnum], fy[:maxnum], c = "r")
    plt.plot(gx[:maxnum], gy[:maxnum], c = "b")
    plt.xlabel("$x$")
    plt.ylabel('$y$')  
    plt.xlim(min(min(fx[:maxnum]), min(gx[:maxnum])) - 0.00033, max(max(fx[:maxnum]), max(gx[:maxnum])) + 0.00033)
    plt.ylim(min(min(fy[:maxnum]), min(gy[:maxnum])) - 0.00015, max(max(fy[:maxnum]), max(gy[:maxnum])) + 0.00015)
    plt.savefig("presentation_plots/" + filename + ".png", bbox_inches = "tight")
    plt.close()
 
def plot_original_file_method(lf, long):
    olong, olat, times = load_traj_name(lf)
    olong, olat = preprocess_long_lat(olong, olat)
    olong, olat = scale_long_lat(olong, olat, 0.1, 0.1, True)
    times_processed = [process_time(time_new) for time_new in times] 
    times_processed = [time_new - times_processed[0] for time_new in times_processed] 
    lat = long.replace("long", "lat").replace("x", "y") 
    filename = lf.replace("/cleaned_csv/events", "").replace(".csv", "") + "_" + long
    plot_trapezoid(long_dict[lf][long], olong, times_processed, "_{x}", filename + "_x_trapz")
    plot_trapezoid(lat_dict[lf][lat], olat, times_processed, "_{y}", filename + "_y_trapz")
    plot_all(long_dict[lf][long], lat_dict[lf][lat], olong, olat, 10, filename + "_euclid")

def get_all_for_name(lf, len_tr):  
    longitudes, latitudes, times = load_traj_name(lf)
    longitudes, latitudes = preprocess_long_lat(longitudes, latitudes)
    longitudes, latitudes = scale_long_lat(longitudes, latitudes, 0.1, 0.1, True)
    times_processed = [process_time(time_new) for time_new in times] 

    time_int = [np.round(times_processed[time_index + 1] - times_processed[time_index], 3) for time_index in range(len(times_processed) - 1)]  
    time_no_gap = fill_gap(predicted_time[lf])
    print_row("predicted_time", time_no_gap[:len_tr], time_int[:len_tr])

    distance_int = [np.round(np.sqrt((longitudes[distance_index + 1] - longitudes[distance_index]) ** 2 + (latitudes[distance_index + 1] - latitudes[distance_index]) ** 2), 5) for distance_index in range(len(longitudes) - 1)]
    distance_no_gap = fill_gap(predicted_distance[lf])
    print_row("predicted_distance", distance_no_gap[:len_tr], distance_int[:len_tr])

    longitude_int = [np.round(abs(longitudes[longitude_index + 1] - longitudes[longitude_index]), 10) for longitude_index in range(len(longitudes) - 1)]
    longitudes_no_gap = fill_gap(predicted_longitude[lf])
    print_row("predicted_longitude", longitudes_no_gap[:len_tr], longitude_int[:len_tr])

    longitude_no_abs_int = [np.round(longitudes[longitude_index + 1] - longitudes[longitude_index], 10) for longitude_index in range(len(longitudes) - 1)]
    longitudes_no_abs_no_gap = fill_gap(predicted_longitude_no_abs[lf])
    print_row("predicted_longitude_no_abs", longitudes_no_abs_no_gap[:len_tr], longitude_no_abs_int[:len_tr])
    
    longitude_sgn_int = [longitudes[longitude_index + 1] > longitudes[longitude_index] for longitude_index in range(len(longitudes) - 1)] 
    longitudes_sgn_no_gap = fill_gap(predicted_longitude_sgn[lf])
    print_row("predicted_longitude_sgn", longitudes_sgn_no_gap[:len_tr], longitude_sgn_int[:len_tr])
 
    latitude_int = [np.round(abs(latitudes[latitude_index + 1] - latitudes[latitude_index]), 10) for latitude_index in range(len(latitudes) - 1)]
    latitudes_no_gap = fill_gap(predicted_latitude[lf])
    print_row("predicted_latitude", latitudes_no_gap[:len_tr], latitude_int[:len_tr])

    latitude_no_abs_int = [np.round(latitudes[latitude_index + 1] - latitudes[latitude_index], 10) for latitude_index in range(len(latitudes) - 1)]
    latitudes_no_abs_no_gap = fill_gap(predicted_latitude_no_abs[lf])
    print_row("predicted_latitude_no_abs", latitudes_no_abs_no_gap[:len_tr], latitude_no_abs_int[:len_tr])
   
    latitude_sgn_int = [latitudes[latitude_index + 1] > latitudes[latitude_index] for latitude_index in range(len(latitudes) - 1)] 
    latitudes_sgn_no_gap = fill_gap(predicted_latitude_sgn[lf])
    print_row("predicted_latitude_sgn", latitudes_sgn_no_gap[:len_tr], latitude_sgn_int[:len_tr])
    
    file_with_ride = pd.read_csv(lf)
    directions = list(file_with_ride["fields_direction"]) 
    direction_int = [np.round(direction, 0) for direction in directions]
    direction_no_gap = fill_gap(predicted_direction[lf])
    print_row("predicted_direction", direction_no_gap[:len_tr], direction_int[:len_tr])
     
    xdistance_int = [longitudes[distance_index + 1] - longitudes[distance_index] for distance_index in range(len(longitudes) - 1)]
    ydistance_int = [latitudes[distance_index + 1] - latitudes[distance_index] for distance_index in range(len(latitudes) - 1)]
    direction_alternative_int = []
    for heading_alternative_index in range(len(longitudes) - 1):
        direction_alternative_int.append((360 + np.round(np.arctan2(ydistance_int[heading_alternative_index], xdistance_int[heading_alternative_index]) / np.pi * 180, 0)) % 360)
         
    direction_alternative_no_gap = fill_gap(predicted_direction_alternative[lf]) 
    print_row("predicted_direction_alternative", direction_alternative_no_gap[:len_tr], direction_alternative_int[:len_tr])

    xdistance_int = [abs(longitudes[distance_index + 1] - longitudes[distance_index]) for distance_index in range(len(longitudes) - 1)]
    ydistance_int = [abs(latitudes[distance_index + 1] - latitudes[distance_index]) for distance_index in range(len(latitudes) - 1)]
    direction_abs_alternative_int = []
    for heading_alternative_index in range(len(longitudes) - 1):
        direction_abs_alternative_int.append((360 + np.round(np.arctan2(ydistance_int[heading_alternative_index], xdistance_int[heading_alternative_index]) / np.pi * 180, 0)) % 360)
 
    direction_abs_alternative_no_gap = fill_gap(predicted_direction_abs_alternative[lf])
    print_row("predicted_direction_abs_alternative", direction_abs_alternative_no_gap[:len_tr], direction_abs_alternative_int[:len_tr])
 
    speeds = list(file_with_ride["fields_speed"]) 
    speed_int = [np.round(speed, 0) for speed in speeds] 
    speed_no_gap = fill_gap(predicted_speed[lf])
    print_row("predicted_speed", speed_no_gap[:len_tr], speed_int[:len_tr])

    times_delays = [times_processed[time_index + 1] - times_processed[time_index] for time_index in range(len(times_processed) - 1)] 
    for time_index in range(len(times_delays)):
            if times_delays[time_index] == 0:
                times_delays[time_index] = 10 ** -20
    distance_int = [np.sqrt((longitudes[distance_index + 1] - longitudes[distance_index]) ** 2 + (latitudes[distance_index + 1] - latitudes[distance_index]) ** 2) for distance_index in range(len(longitudes) - 1)]
    speed_alternative_int = [np.round(distance_int[speed_alternative_index] / times_delays[speed_alternative_index], 5) for speed_alternative_index in range(len(times_delays))]
    speed_alternative_no_gap = fill_gap(predicted_speed_alternative[lf])
    print_row("predicted_speed_alternative", speed_alternative_no_gap[:len_tr], speed_alternative_int[:len_tr])
    
    for time_index in range(len(times_delays)):
            if times_delays[time_index] == 0:
                times_delays[time_index] = 10 ** -20
    distance_int = [abs(longitudes[distance_index + 1] - longitudes[distance_index]) for distance_index in range(len(longitudes) - 1)]
    x_speed_alternative_int = [np.round(distance_int[x_speed_alternative_index] / times_delays[x_speed_alternative_index], 5) for x_speed_alternative_index in range(len(times_delays))]
    x_speed_alternative_no_gap = fill_gap(predicted_x_speed_alternative[lf]) 
    print_row("predicted_x_speed_alternative", x_speed_alternative_no_gap[:len_tr], x_speed_alternative_int[:len_tr])
    
    for time_index in range(len(times_delays)):
            if times_delays[time_index] == 0:
                times_delays[time_index] = 10 ** -20
    distance_int = [abs(latitudes[distance_index + 1] - latitudes[distance_index]) for distance_index in range(len(latitudes) - 1)]
    y_speed_alternative_int = [np.round(distance_int[y_speed_alternative_index] / times_delays[y_speed_alternative_index], 5) for y_speed_alternative_index in range(len(times_delays))]
    y_speed_alternative_no_gap = fill_gap(predicted_y_speed_alternative[lf])
    print_row("predicted_y_speed_alternative", y_speed_alternative_no_gap[:len_tr], y_speed_alternative_int[:len_tr])

    for time_index in range(len(times_delays)):
            if times_delays[time_index] == 0:
                times_delays[time_index] = 10 ** -20
    distance_int = [longitudes[distance_index + 1] - longitudes[distance_index] for distance_index in range(len(longitudes) - 1)]
    x_speed_no_abs_alternative_int = [np.round(distance_int[x_speed_no_abs_alternative_index] / times_delays[x_speed_no_abs_alternative_index], 5) for x_speed_no_abs_alternative_index in range(len(times_delays))]
    x_speed_no_abs_alternative_no_gap = fill_gap(predicted_x_speed_no_abs_alternative[lf])
    print_row("predicted_x_speed_no_abs_alternative", x_speed_no_abs_alternative_no_gap[:len_tr], x_speed_no_abs_alternative_int[:len_tr])
    
    for time_index in range(len(times_delays)):
            if times_delays[time_index] == 0:
                times_delays[time_index] = 10 ** -20
    distance_int = [latitudes[distance_index + 1] - latitudes[distance_index] for distance_index in range(len(latitudes) - 1)]
    y_speed_no_abs_alternative_int = [np.round(distance_int[y_speed_no_abs_alternative_index] / times_delays[y_speed_no_abs_alternative_index], 5) for y_speed_no_abs_alternative_index in range(len(times_delays))]
    y_speed_no_abs_alternative_no_gap = fill_gap(predicted_y_speed_no_abs_alternative[lf])
    print_row("predicted_y_speed_no_abs_alternative", y_speed_no_abs_alternative_no_gap[:len_tr], y_speed_no_abs_alternative_int[:len_tr])
      
    print_method("", "", longitudes[:len_tr])
    for long in long_dict[lf]:
        if "actual" in long:
            continue
        lat = long.replace("long", "lat").replace("x", "y") 
        print_method(long, lat, long_dict[lf][long][:len_tr])
        
    print_method("", "", latitudes[:len_tr])
    for long in long_dict[lf]:
        if "actual" in long:
            continue
        lat = long.replace("long", "lat").replace("x", "y") 
        print_method(long, lat, lat_dict[lf][lat][:len_tr])
             
min_len = 100000
lf = "" 
for long_filename in long_dict:
    for long in long_dict[long_filename]:
        if len(long_dict[long_filename][long]) < min_len:
            min_len = len(long_dict[long_filename][long])
            lf = long_filename
        break

print(min_len, lf)
if not os.path.isdir("presentation_plots"):
    os.makedirs("presentation_plots")
plot_original_file_method(lf, "long no abs")
get_all_for_name(lf, 5)