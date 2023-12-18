from utilities import *  
  
all_subdirs = os.listdir()   
     
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
    plt.rcParams['font.family'] = "serif"
    plt.rcParams["mathtext.fontset"] = "dejavuserif"
    plt.figure(figsize=(15, 7))
    plt.subplot(1, 2, 1)
    plt.xlabel("$t$")
    plt.ylabel('$' + str_pr[2] + '$')  
    for ixix in range(len(x)): 
        plt.plot([x[ixix], x[ixix]], [f[ixix], g[ixix]], c = "c") 
    plt.plot(x, f, label = "f", c = "r")
    if f[ix] > g[ix]:  
        plt.text(x[ix], f[ix] + 0.00025, '$f' + str_pr + '$', size=15, color='r')
    else:    
        plt.text(x[ix], f[ix] - 0.00015, '$f' + str_pr + '$', size=15, color='r')
    plt.ylim(min(min(f), min(g)), max(max(f), max(g)) + 0.0001)
    plt.plot(x, g, label = "g", c = "b")
    if g[ix] > f[ix]:  
        plt.text(x[ix], g[ix] + 0.00025, '$g' + str_pr + '$', size=15, color='b')
    else:    
        plt.text(x[ix], g[ix] - 0.0003, '$g' + str_pr + '$', size=15, color='b')
    plt.text(x[ix], (f[ix] + g[ix]) / 2, '$A$', size=15, color='k')
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
    plt.plot(x, df, c = "c") 
    plt.ylim(- 0.0001, max(max(f), max(g)) + 0.0001 - min(min(f), min(g)) + 0.0001) 
    plt.plot(x4, l4, c = "c")
    plt.text(x[ix], df[ix] / 2, '$A$', size=15, color='k')
    plt.text(x[ix], df[ix] + 0.0005, '$|f' + str_pr + '-g' + str_pr + '|$', size=15, color='c')
    plt.plot(x3, s2, c = "c")
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
    plt.rcParams['font.family'] = "serif"
    plt.rcParams["mathtext.fontset"] = "dejavuserif"  
    plt.xlabel("$t$")
    plt.ylabel('$' + str_pr[2] + '$')  
    for ixix in range(len(x)): 
        plt.plot([x[ixix], x[ixix]], [f[ixix], g[ixix]], c = "c") 
    plt.plot(x, f, label = "f", c = "r")
    if f[ix] > g[ix]:  
        plt.text(x[ix], f[ix] + 0.00035, '$f' + str_pr + '$', size=15, color='r')
    else:    
        plt.text(x[ix], f[ix] - 0.00025, '$f' + str_pr + '$', size=15, color='r')
    plt.ylim(min(min(f), min(g)), max(max(f), max(g)) + 0.0001)
    plt.plot(x, g, label = "g", c = "b")
    if g[ix] > f[ix]:  
        plt.text(x[ix], g[ix] + 0.00035, '$g' + str_pr + '$', size=15, color='b')
    else:    
        plt.text(x[ix], g[ix] - 0.0004, '$g' + str_pr + '$', size=15, color='b')
    plt.text(x[ix], (f[ix] + g[ix]) / 2, '$A$', size=15, color='k')
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

def get_all_for_name(lf): 
    file_with_ride = pd.read_csv(lf)
    longitudes, latitudes, times = load_traj_name(lf)
    longitudes, latitudes = preprocess_long_lat(longitudes, latitudes)
    longitudes, latitudes = scale_long_lat(longitudes, latitudes, 0.1, 0.1, True)
    times_processed = [process_time(time_new) for time_new in times] 
    time_int = [np.round(times_processed[time_index + 1] - times_processed[time_index], 3) for time_index in range(len(times_processed) - 1)] 
    times = [np.round(times_processed[time_index] - times_processed[0], 3) for time_index in range(len(times_processed))] 
    longer_file_name = lf
    time_no_gap = fill_gap(predicted_time[longer_file_name])
    distance_no_gap = fill_gap(predicted_distance[longer_file_name])
    longitudes_no_gap = fill_gap(predicted_longitude[longer_file_name])
    latitudes_no_gap = fill_gap(predicted_latitude[longer_file_name])
    longitudes_no_abs_no_gap = fill_gap(predicted_longitude_no_abs[longer_file_name])
    latitudes_no_abs_no_gap = fill_gap(predicted_latitude_no_abs[longer_file_name])
    direction_no_gap = fill_gap(predicted_direction[longer_file_name])
    direction_alternative_no_gap = fill_gap(predicted_direction_alternative[longer_file_name]) 
    direction_abs_alternative_no_gap = fill_gap(predicted_direction_abs_alternative[longer_file_name])
    speed_no_gap = fill_gap(predicted_speed[longer_file_name])
    speed_alternative_no_gap = fill_gap(predicted_speed_alternative[longer_file_name])
    x_speed_alternative_no_gap = fill_gap(predicted_x_speed_alternative[longer_file_name]) 
    y_speed_alternative_no_gap = fill_gap(predicted_y_speed_alternative[longer_file_name])
    x_speed_no_abs_alternative_no_gap = fill_gap(predicted_x_speed_no_abs_alternative[longer_file_name])
    y_speed_no_abs_alternative_no_gap = fill_gap(predicted_y_speed_no_abs_alternative[longer_file_name])

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