import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np 
import pickle
from scipy.integrate import simpson
import scipy.fft
from sklearn.metrics import auc
from datetime import datetime     
from scipy.spatial import ConvexHull, convex_hull_plot_2d

def dtw(longitudes1, latitudes1, longitudes2, latitudes2): 
    if len(longitudes1) == 0 and len(latitudes1) == 0 and len(longitudes2) == 0 and len(latitudes2) == 0:
        return 0
    if len(longitudes1) == 0 and len(latitudes1) == 0 and len(longitudes2) > 0 and len(latitudes2) > 0:
        return 10000000
    if len(longitudes1) > 0 and len(latitudes1) > 0 and len(longitudes2) == 0 and len(latitudes2) == 0:
        return 10000000 
    headlong1 = [longitudes1[0]]
    restlong1 = []
    headlong2 = [longitudes2[0]]
    restlong2 = []
    headlat1 = [latitudes1[0]]
    restlat1 = []
    headlat2 = [latitudes2[0]]
    restlat2 = []
    if len(longitudes1) > 1 and len(latitudes1) > 1:
        restlong1 = longitudes1[1:]
        restlat1 = latitudes1[1:]
    if len(longitudes2) > 1 and len(latitudes2) > 1:
        restlong2 = longitudes2[1:]
        restlat2 = latitudes2[1:]
    dtw1 = dtw(headlong1, headlat1, restlong2, restlat2) 
    dtw2 = dtw(restlong1, restlat1, restlong2, restlat2)
    dtw3 = dtw(restlong1, restlat1, headlong2, headlat2)
    return euclidean(headlong1, headlat1, headlong2, headlat2) + min(min(dtw1, dtw2), dtw3)

def decompose_fft(data: list, threshold: float = 0.0):
    fft3 = np.fft.fft(data)
    x = np.arange(0, 10, 10 / len(data))
    freqs = np.fft.fftfreq(len(x), .01)
    recomb = np.zeros((len(x),))
    for i in range(len(fft3)):
        if abs(fft3[i]) / len(x) > threshold:
            sinewave = (
                1 
                / len(x) 
                * (
                    fft3[i].real 
                    * np.cos(freqs[i] * 2 * np.pi * x) 
                    - fft3[i].imag 
                    * np.sin(freqs[i] * 2 * np.pi * x)))
            recomb += sinewave
            plt.plot(x, sinewave)
    plt.title("Sinewave")
    plt.show()

    plt.plot(x, recomb, x, data)
    plt.title("Recomb")
    plt.show()
 
def process_time(time_as_str):
    time_as_str = time_as_str.split(".")[0]
    return datetime.strptime(time_as_str, '%Y-%m-%d %H:%M:%S')

def poly_calc(coeffs, xs):
    ys = []
    for xval in xs:
        yval = 0
        for i in range(len(coeffs)):
            yval += coeffs[i] * (xval ** (len(coeffs) - 1 - i))
        ys.append(yval)
    return ys

def get_fft_xt_yt(longitudes, latitudes, times_ride, deg): 
    xt, yt = get_poly_xt_yt(longitudes, latitudes, times_ride, deg)
    xn = poly_calc(xt, range(len(longitudes)))
    yn = poly_calc(yt, range(len(latitudes)))
    fftx = scipy.fft.fft(xn)
    ffty = scipy.fft.fft(yn)
    return xt, yt, xn, yn, fftx, ffty

def get_poly_xt_yt(longitudes, latitudes, times_ride, deg):
    xt = np.polyfit(times_ride, longitudes, deg)
    yt = np.polyfit(times_ride, latitudes, deg) 
    return xt, yt

def get_surf_xt_yt(longitudes, latitudes, times_ride, metric_used): 
    if metric_used == "trapz":
        return np.trapz(longitudes, times_ride), np.trapz(latitudes, times_ride) 
    if metric_used == "simpson":
        return simpson(longitudes, times_ride), simpson(latitudes, times_ride) 

def transform_time(times_ride): 
    times_ride = [process_time(time_as_str) for time_as_str in times_ride]
    times_ride = [(time_one - times_ride[0]).total_seconds() for time_one in times_ride] 
    return times_ride
    
def traj_len_offset(longitudes, latitudes):
    sum_dist = 0
    for i in range(len(longitudes) - 1):
        sum_dist += np.sqrt((longitudes[i + 1] - longitudes[i]) ** 2 + (latitudes[i + 1] - latitudes[i]) ** 2)
    offset_total = np.sqrt((longitudes[len(longitudes) - 1] - longitudes[0]) ** 2 + (latitudes[len(latitudes) - 1] - latitudes[0]) ** 2)
    return sum_dist, offset_total

def get_vector(x1, x2, y1, y2):
    if x1 == x2:
        return 0, -1, x1 
    else:
        a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1 
        return 1, a, b 
        
def get_intersection(x1, x2, y1, y2, x3, x4, y3, y4):
    yc1, a1, b1 = get_vector(x1, x2, y1, y2)
    yc2, a2, b2 = get_vector(x3, x4, y3, y4)
    if yc1 != 0 and yc2 != 0:
        if a1 != a2:
            xs = (b2 - b1) / (a1 - a2)
            ys = a1 * xs + b1
            return xs, ys
        else:
            return "Nan", "Nan"
    else:
        if yc1 == 0 and yc2 != 0:
            return x1, a2 * x1 + b2
        if yc2 == 0 and yc1 != 0:
            return x3, a1 * x3 + b1
        return "Nan", "Nan"
        
def point_on_line(xs, ys, x1, x2, y1, y2): 
    minx = min(x1, x2)
    maxx = max(x1, x2)
    miny = min(y1, y2)
    maxy = max(y1, y2) 
    return xs >= minx and xs <= maxx and ys >= miny and ys <= maxy
    
def get_surface(x1, x2, x3, y1, y2, y3):
    return 0.5 * abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y2 - y1))
    
def traj_segment_dist(x1, y1, x2, y2, x3, y3, x4, y4):
    xs, ys = get_intersection(x1, x2, y1, y2, x3, x4, y3, y4)
    s1 = get_surface(x2, x3, x4, y2, y3, y4)
    s2 = get_surface(x1, x3, x4, y1, y3, y4)
    s3 = get_surface(x1, x2, x4, y1, y2, y4)
    s4 = get_surface(x1, x2, x3, y1, y2, y3)
    if xs == "Nan":
        return (s1 + s2 + s3 + s4) / 2
    else:
        if point_on_line(xs, ys, x3, x4, y3, y4) or point_on_line(xs, ys, x1, x2, y1, y2):
            s5 = get_surface(x1, x2, xs, y1, y2, ys)
            s6 = get_surface(x3, x4, xs, y3, y4, ys)
            return s5 + s6
        else:
            return (s1 + s2 + s3 + s4) / 2
        
def traj_segment_dist_markings(color_paint, x1, y1, x2, y2, x3, y3, x4, y4):
    xs, ys = get_intersection(x1, x2, y1, y2, x3, x4, y3, y4)
    s1 = get_surface(x2, x3, x4, y2, y3, y4)
    s2 = get_surface(x1, x3, x4, y1, y3, y4)
    s3 = get_surface(x1, x2, x4, y1, y2, y4)
    s4 = get_surface(x1, x2, x3, y1, y2, y3)
    plt.plot([x1, x2], [y1, y2], color_paint)
    plt.plot([x1, x3], [y1, y3], color_paint)
    plt.plot([x1, x4], [y1, y4], color_paint)
    plt.plot([x2, x3], [y2, y3], color_paint)
    plt.plot([x2, x4], [y2, y4], color_paint)
    plt.plot([x3, x4], [y3, y4], color_paint)
    if xs == "Nan":
        return (s1 + s2 + s3 + s4) / 2
    else:
        if point_on_line(xs, ys, x3, x4, y3, y4) or point_on_line(xs, ys, x1, x2, y1, y2):
            s5 = get_surface(x1, x2, xs, y1, y2, ys)
            s6 = get_surface(x3, x4, xs, y3, y4, ys)
            return s5 + s6
        else:
            return (s1 + s2 + s3 + s4) / 2
     
def traj_dist(longitudes1, latitudes1, longitudes2, latitudes2):
    sum_dist = 0
    for i in range(len(longitudes1) - 1):
        sum_dist += traj_segment_dist(longitudes1[i], latitudes1[i], longitudes1[i + 1], latitudes1[i + 1], longitudes2[i], latitudes2[i], longitudes2[i + 1], latitudes2[i + 1])
    return sum_dist

def euclidean(longitudes1, latitudes1, longitudes2, latitudes2):
    sum_dist = 0
    for i in range(len(longitudes1)):
        sum_dist += np.sqrt((longitudes1[i] - longitudes2[i]) ** 2 + (latitudes1[i] - latitudes2[i]) ** 2)
    return sum_dist / len(longitudes1)

def traj_dist_markings(longitudes1, latitudes1, longitudes2, latitudes2):
    sum_dist = 0
    colors_set = random_colors(len(longitudes1) - 1)
    for i in range(len(longitudes1) - 1):
        sum_dist += traj_segment_dist_markings(colors_set[i], longitudes1[i], latitudes1[i], longitudes1[i + 1], latitudes1[i + 1], longitudes2[i], latitudes2[i], longitudes2[i + 1], latitudes2[i + 1])
    return sum_dist
    
def save_plot_longitude_latitudes_for_ride(longitudes, latitudes, image_name):  
    plt.plot(longitudes, latitudes, color = 'k', linewidth = 10) 
    ax = plt.gca()
    ax.xaxis.set_tick_params(labelbottom = False)
    ax.yaxis.set_tick_params(labelleft = False)  
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    plt.savefig(image_name, bbox_inches = 'tight') 
    plt.clf()

def random_colors(num_colors):
    colors_set = []
    for x in range(num_colors):
        string_color = "#"
        while string_color == "#" or string_color in colors_set:
            string_color = "#"
            set_letters = "0123456789ABCDEF"
            for y in range(6):
                string_color += set_letters[np.random.randint(0, 16)]
        colors_set.append(string_color)
    return colors_set
    
def save_object(file_name, std1):       
    with open(file_name, 'wb') as file_object:
        pickle.dump(std1, file_object) 
        file_object.close()

def load_object(file_name): 
    with open(file_name, 'rb') as file_object:
        data = pickle.load(file_object) 
        file_object.close()
        return data
    
def preprocess_long_lat(long_list, lat_list):
    x_dir = long_list[0] < long_list[-1]
    y_dir = lat_list[0] < lat_list[-1]
 
    long_list2 = [x - min(long_list) for x in long_list]
    lat_list2 = [y - min(lat_list) for y in lat_list]
    if x_dir == False: 
        long_list2 = [max(long_list2) - x for x in long_list2]
    if y_dir == False:
        lat_list2 = [max(lat_list2) - y for y in lat_list2]

    return long_list2, lat_list2    
      
def scale_long_lat(long_list, lat_list, xmax = 0, ymax = 0, keep_aspect_ratio = True):
    minx = np.min(long_list)
    maxx = np.max(long_list)
    miny = np.min(lat_list)
    maxy = np.max(lat_list)
    x_diff = maxx - minx
    if x_diff == 0:
        x_diff = 1
    y_diff = maxy - miny 
    if y_diff == 0:
        y_diff = 1
    if xmax == 0 and ymax == 0 and keep_aspect_ratio:
        xmax = max(x_diff, y_diff)
        ymax = max(x_diff, y_diff)
    if xmax == 0 and ymax == 0 and not keep_aspect_ratio:
        xmax = x_diff
        ymax = y_diff
    if xmax == 0 and ymax != 0 and keep_aspect_ratio:
        xmax = ymax 
    if xmax == 0 and ymax != 0 and not keep_aspect_ratio:
        xmax = x_diff 
    if xmax != 0 and ymax == 0 and keep_aspect_ratio:
        ymax = xmax 
    if xmax != 0 and ymax == 0 and not keep_aspect_ratio:
        ymax = y_diff 
    if xmax != 0 and ymax != 0 and keep_aspect_ratio and xmax != ymax:
        ymax = xmax # ymax = xmax or xmax = ymax or keep_aspect_ratio = False or return
    long_list2 = [(x - min(long_list)) / xmax for x in long_list]
    lat_list2 = [(y - min(lat_list)) / ymax for y in lat_list]
    return long_list2, lat_list2  

def total_len(long_list, lat_list):
    total_sum = 0
    for index_coord in range(len(long_list) - 1):
        total_sum += np.sqrt((long_list[index_coord + 1] - long_list[index_coord]) ** 2 + (lat_list[index_coord + 1] - lat_list[index_coord]) ** 2)
    return total_sum

def total_offset(long_list, lat_list):
    return np.sqrt((long_list[0] - long_list[-1]) ** 2 + (lat_list[0] - lat_list[-1]) ** 2)
     
def total_angle(long_list, lat_list):
    if long_list[0] != long_list[-1]: 
        return np.arctan((lat_list[0] - lat_list[-1]) / (long_list[0] - long_list[-1]))
    else:
        return np.arctan(0)
 
def mean_vect_turning_angles(long_list, lat_list):
    total_angles = []
    for index_coord in range(len(long_list) - 1):
        if long_list[index_coord + 1] != long_list[index_coord]: 
            total_angles.append(np.arctan((lat_list[index_coord + 1] - lat_list[index_coord]) / (long_list[index_coord + 1] - long_list[index_coord]))) 
        else:
            total_angles.append(np.arctan(0))
    return np.average(total_angles)

def mean_speed_len(long_list, lat_list, times_list):
    return total_len(long_list, lat_list) / times_list[-1]

def mean_speed_offset(long_list, lat_list, times_list):
    return total_offset(long_list, lat_list) / times_list[-1]

def SomePolyArea(corners):
    n = len(corners) # of corners 
    area = 0.0
    for i in range(n):
        j = (i + 1) % n 
        area += corners[i][0] * corners[j][1] 
        area -= corners[j][0] * corners[i][1]      
    area = abs(area) / 2.0
    return area

def total_surf(long_list, lat_list):
    points_data = np.column_stack((np.array(long_list), np.array(lat_list)))  
    ch = ConvexHull(points_data)
    corners = []  
    for vx in ch.vertices:
        corners.append((points_data[vx, 0], points_data[vx, 1]))  
    value_ret = SomePolyArea(corners)
    '''
    print(value_ret)
    plt.plot(points_data[:,0], points_data[:,1], 'o')
    for vx_index in range(len(ch.vertices) - 1):
        plt.plot(points_data[[ch.vertices[vx_index], ch.vertices[vx_index + 1]], 0], points_data[[ch.vertices[vx_index], ch.vertices[vx_index + 1]], 1], 'k-')
    plt.plot(points_data[[ch.vertices[len(ch.vertices) - 1], ch.vertices[0]], 0], points_data[[ch.vertices[len(ch.vertices) - 1], ch.vertices[0]], 1], 'k-')
    '''
    return value_ret
     
predicted_time = load_object("predicted/predicted_time") 
probability_of_time = load_object("probability/probability_of_time") 
probability_of_time_in_next_step = load_object("probability/probability_of_time_in_next_step") 
probability_of_time_in_next_next_step = load_object("probability/probability_of_time_in_next_next_step") 
#print("probability/probability_of_time", min(probability_of_time.keys()), max(probability_of_time.keys()))

predicted_distance = load_object("predicted/predicted_distance") 
probability_of_distance = load_object("probability/probability_of_distance") 
probability_of_distance_in_next_step = load_object("probability/probability_of_distance_in_next_step") 
probability_of_distance_in_next_next_step = load_object("probability/probability_of_distance_in_next_next_step") 
#print("probability/probability_of_distance", min(probability_of_distance.keys()), max(probability_of_distance.keys()))

predicted_longitude = load_object("predicted/predicted_longitude") 
probability_of_longitude = load_object("probability/probability_of_longitude") 
probability_of_longitude_in_next_step = load_object("probability/probability_of_longitude_in_next_step") 
probability_of_longitude_in_next_next_step = load_object("probability/probability_of_longitude_in_next_next_step") 
#print("probability/probability_of_longitude", min(probability_of_longitude.keys()), max(probability_of_longitude.keys()))

predicted_latitude = load_object("predicted/predicted_latitude") 
probability_of_latitude = load_object("probability/probability_of_latitude") 
probability_of_latitude_in_next_step = load_object("probability/probability_of_latitude_in_next_step") 
probability_of_latitude_in_next_next_step = load_object("probability/probability_of_latitude_in_next_next_step") 
#print("probability/probability_of_latitude", min(probability_of_latitude.keys()), max(probability_of_latitude.keys()))

predicted_longitude_sgn = load_object("predicted/predicted_longitude_sgn") 
probability_of_longitude_sgn = load_object("probability/probability_of_longitude_sgn") 
probability_of_longitude_sgn_in_next_step = load_object("probability/probability_of_longitude_sgn_in_next_step") 
probability_of_longitude_sgn_in_next_next_step = load_object("probability/probability_of_longitude_sgn_in_next_next_step") 
#print("probability/probability_of_longitude_sgn", min(probability_of_longitude_sgn.keys()), max(probability_of_longitude_sgn.keys()))

predicted_latitude_sgn = load_object("predicted/predicted_latitude_sgn") 
probability_of_latitude_sgn = load_object("probability/probability_of_latitude_sgn") 
probability_of_latitude_sgn_in_next_step = load_object("probability/probability_of_latitude_sgn_in_next_step") 
probability_of_latitude_sgn_in_next_next_step = load_object("probability/probability_of_latitude_sgn_in_next_next_step") 
#print("probability/probability_of_latitude_sgn", min(probability_of_latitude_sgn.keys()), max(probability_of_latitude_sgn.keys()))

predicted_longitude_no_abs = load_object("predicted/predicted_longitude_no_abs") 
probability_of_longitude_no_abs = load_object("probability/probability_of_longitude_no_abs") 
probability_of_longitude_no_abs_in_next_step = load_object("probability/probability_of_longitude_no_abs_in_next_step") 
probability_of_longitude_no_abs_in_next_next_step = load_object("probability/probability_of_longitude_no_abs_in_next_next_step") 
#print("probability/probability_of_longitude_no_abs", min(probability_of_longitude_no_abs.keys()), max(probability_of_longitude_no_abs.keys()))

predicted_latitude_no_abs = load_object("predicted/predicted_latitude_no_abs") 
probability_of_latitude_no_abs = load_object("probability/probability_of_latitude_no_abs") 
probability_of_latitude_no_abs_in_next_step = load_object("probability/probability_of_latitude_no_abs_in_next_step") 
probability_of_latitude_no_abs_in_next_next_step = load_object("probability/probability_of_latitude_no_abs_in_next_next_step") 
#print("probability/probability_of_latitude_no_abs", min(probability_of_latitude_no_abs.keys()), max(probability_of_latitude_no_abs.keys()))

predicted_direction = load_object("predicted/predicted_direction") 
probability_of_direction = load_object("probability/probability_of_direction") 
probability_of_direction_in_next_step = load_object("probability/probability_of_direction_in_next_step") 
probability_of_direction_in_next_next_step = load_object("probability/probability_of_direction_in_next_next_step") 
#print("probability/probability_of_direction", min(probability_of_direction.keys()), max(probability_of_direction.keys()))

predicted_direction_alternative = load_object("predicted/predicted_direction_alternative") 
probability_of_direction_alternative = load_object("probability/probability_of_direction_alternative") 
probability_of_direction_alternative_in_next_step = load_object("probability/probability_of_direction_alternative_in_next_step") 
probability_of_direction_alternative_in_next_next_step = load_object("probability/probability_of_direction_alternative_in_next_next_step") 
#print("probability/probability_of_direction_alternative", min(probability_of_direction_alternative.keys()), max(probability_of_direction_alternative.keys()))
 
predicted_speed = load_object("predicted/predicted_speed") 
probability_of_speed = load_object("probability/probability_of_speed") 
probability_of_speed_in_next_step = load_object("probability/probability_of_speed_in_next_step") 
probability_of_speed_in_next_next_step = load_object("probability/probability_of_speed_in_next_next_step") 
#print("probability/probability_of_speed", min(probability_of_speed.keys()), max(probability_of_speed.keys()))

predicted_speed_alternative = load_object("predicted/predicted_speed_alternative") 
probability_of_speed_alternative = load_object("probability/probability_of_speed_alternative") 
probability_of_speed_alternative_in_next_step = load_object("probability/probability_of_speed_alternative_in_next_step") 
probability_of_speed_alternative_in_next_next_step = load_object("probability/probability_of_speed_alternative_in_next_next_step") 
#print("probability/probability_of_speed_alternative", min(probability_of_speed_alternative.keys()), max(probability_of_speed_alternative.keys()))

predicted_x_speed_alternative = load_object("predicted/predicted_x_speed_alternative") 
probability_of_x_speed_alternative = load_object("probability/probability_of_x_speed_alternative") 
probability_of_x_speed_alternative_in_next_step = load_object("probability/probability_of_x_speed_alternative_in_next_step") 
probability_of_x_speed_alternative_in_next_next_step = load_object("probability/probability_of_x_speed_alternative_in_next_next_step") 
#print("probability/probability_of_x_speed_alternative", min(probability_of_x_speed_alternative.keys()), max(probability_of_x_speed_alternative.keys()))

predicted_y_speed_alternative = load_object("predicted/predicted_y_speed_alternative") 
probability_of_y_speed_alternative = load_object("probability/probability_of_y_speed_alternative") 
probability_of_y_speed_alternative_in_next_step = load_object("probability/probability_of_y_speed_alternative_in_next_step") 
probability_of_y_speed_alternative_in_next_next_step = load_object("probability/probability_of_y_speed_alternative_in_next_next_step") 
#print("probability/probability_of_y_speed_alternative", min(probability_of_y_speed_alternative.keys()), max(probability_of_y_speed_alternative.keys()))

predicted_x_speed_no_abs_alternative = load_object("predicted/predicted_x_speed_no_abs_alternative") 
probability_of_x_speed_no_abs_alternative = load_object("probability/probability_of_x_speed_no_abs_alternative") 
probability_of_x_speed_no_abs_alternative_in_next_step = load_object("probability/probability_of_x_speed_no_abs_alternative_in_next_step") 
probability_of_x_speed_no_abs_alternative_in_next_next_step = load_object("probability/probability_of_x_speed_no_abs_alternative_in_next_next_step") 
#print("probability/probability_of_x_speed_no_abs_alternative", min(probability_of_x_speed_no_abs_alternative.keys()), max(probability_of_x_speed_no_abs_alternative.keys()))

predicted_y_speed_no_abs_alternative = load_object("predicted/predicted_y_speed_no_abs_alternative") 
probability_of_y_speed_no_abs_alternative = load_object("probability/probability_of_y_speed_no_abs_alternative") 
probability_of_y_speed_no_abs_alternative_in_next_step = load_object("probability/probability_of_y_speed_no_abs_alternative_in_next_step") 
probability_of_y_speed_no_abs_alternative_in_next_next_step = load_object("probability/probability_of_y_speed_no_abs_alternative_in_next_next_step") 
#print("probability/probability_of_y_speed_no_abs_alternative", min(probability_of_y_speed_no_abs_alternative.keys()), max(probability_of_y_speed_no_abs_alternative.keys()))

all_subdirs = os.listdir() 

path_lengths = []

#pair 1: longitudes (no abs) + latitudes (no abs) 4
#pair 2: longitudes (no abs) + y_speed (no abs) * time 4
#pair 3: x_speed (no abs) * time + latitudes (no abs) 4
#pair 4: x_speed (no abs) * time + y_speed (no abs) * time 4
#pair 5: distance + heading (heading_alternative) 2
#pair 6: speed (speed_alternative) * time + heading (heading_alternative) 4

def get_sides_from_angle(longest, angle):
    return longest * np.cos(angle / 180 * np.pi), longest * np.sin(angle / 180 * np.pi)

def fill_gap(list_gap):
    list_no_gap = []
    last_val = 0
    for index_num in range(len(list_gap)):
        if list_gap[index_num] != -1:
            last_val = list_gap[index_num]
        list_no_gap.append(last_val)  
    return list_no_gap

def compare_traj_and_sample(sample_x, sample_y, sample_time, t1, metric_used): 
    if metric_used == "custom":
        return traj_dist(t1["long"], t1["lat"], sample_x, sample_y)  
    if metric_used == "dtw":
        return dtw(t1["long"], t1["lat"], sample_x, sample_y)    
    if metric_used == "trapz":
        return abs(np.trapz(t1["lat"], t1["long"]) - np.trapz(sample_y, sample_x)) 
    if metric_used == "simpson":
        return abs(simpson(t1["lat"], t1["long"]) - np.trapz(sample_y, sample_x))  
    if metric_used == "trapz x":
        return abs(np.trapz(t1["long"], t1["time"]) - np.trapz(sample_x, sample_time))
    if metric_used == "simpson x":
        return abs(simpson(t1["long"], t1["time"]) - np.trapz(sample_x, sample_time)) 
    if metric_used == "trapz y":
        return abs(np.trapz(t1["lat"], t1["time"]) - np.trapz(sample_y, sample_time))
    if metric_used == "simpson y":
        return abs(simpson(t1["lat"], t1["time"]) - np.trapz(sample_y, sample_time))  
    if metric_used == "euclidean":
        return euclidean(t1["long"], t1["lat"], sample_x, sample_y)
      
times_cumulative = []

long_cumulative = []
lat_cumulative = []

long_no_abs_cumulative = []
lat_no_abs_cumulative = []

x_speed_cumulative = []
y_speed_cumulative = []

x_speed_no_abs_cumulative = []
y_speed_no_abs_cumulative = []

longitude_from_distance_heading_alternative = []
latitude_from_distance_heading_alternative = []

longitude_from_distance_heading = []
latitude_from_distance_heading = []

longitude_from_speed_alternative_time_heading_alternative = []
latitude_from_speed_alternative_time_heading_alternative = []

longitude_from_speed_alternative_time_heading = []
latitude_from_speed_alternative_time_heading = []

longitude_from_speed_time_heading_alternative = []
latitude_from_speed_time_heading_alternative = []

longitude_from_speed_time_heading = []
latitude_from_speed_time_heading = []
i = 0
for subdir_name in all_subdirs: 
    if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
        continue 
    
    all_rides_cleaned = os.listdir(subdir_name + "/cleaned_csv/")
      
    all_files = os.listdir(subdir_name + "/cleaned_csv/") 
    bad_rides_filenames = set()
    if os.path.isfile(subdir_name + "/bad_rides_filenames"):
        bad_rides_filenames = load_object(subdir_name + "/bad_rides_filenames")
    train_rides = set()
    if os.path.isfile(subdir_name + "/train_rides"):
        train_rides= load_object(subdir_name + "/train_rides")
        
    for some_file in all_files:  
        if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or some_file in train_rides: 
            continue 
    
        file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
        longitudes = list(file_with_ride["fields_longitude"]) 
        latitudes = list(file_with_ride["fields_latitude"]) 
        longitudes, latitudes = preprocess_long_lat(longitudes, latitudes)
        longitudes, latitudes = scale_long_lat(longitudes, latitudes, 0.1, 0.1, True)

        time_no_gap = fill_gap(predicted_time[i])
        distance_no_gap = fill_gap(predicted_distance[i])
        longitudes_no_gap = fill_gap(predicted_longitude[i])
        latitudes_no_gap = fill_gap(predicted_latitude[i])
        longitudes_no_abs_no_gap = fill_gap(predicted_longitude_no_abs[i])
        latitudes_no_abs_no_gap = fill_gap(predicted_latitude_no_abs[i])
        direction_no_gap = fill_gap(predicted_direction[i])
        direction_alternative_no_gap = fill_gap(predicted_direction_alternative[i])
        speed_no_gap = fill_gap(predicted_speed[i])
        speed_alternative_no_gap = fill_gap(predicted_speed_alternative[i])
        x_speed_alternative_no_gap = fill_gap(predicted_x_speed_alternative[i]) 
        y_speed_alternative_no_gap = fill_gap(predicted_y_speed_alternative[i])
        x_speed_no_abs_alternative_no_gap = fill_gap(predicted_x_speed_no_abs_alternative[i])
        y_speed_no_abs_alternative_no_gap = fill_gap(predicted_y_speed_no_abs_alternative[i])

        x_dir = list(file_with_ride["fields_longitude"])[0] < list(file_with_ride["fields_longitude"])[-1]
        y_dir = list(file_with_ride["fields_latitude"])[0] < list(file_with_ride["fields_latitude"])[-1]

        times_cumulative.append([0])
        for time_index in range(len(time_no_gap)):
            times_cumulative[i].append(times_cumulative[i][-1] + time_no_gap[time_index])

        long_cumulative.append([longitudes[0]])
        lat_cumulative.append([latitudes[0]])
        for index_long in range(len(longitudes_no_gap)):
            long_cumulative[i].append(long_cumulative[i][-1] - longitudes_no_gap[index_long] + longitudes_no_gap[index_long] * 2 * predicted_longitude_sgn[i][index_long])
            lat_cumulative[i].append(lat_cumulative[i][-1] - latitudes_no_gap[index_long] + latitudes_no_gap[index_long] * 2 * predicted_latitude_sgn[i][index_long])

        long_no_abs_cumulative.append([longitudes[0]])
        lat_no_abs_cumulative.append([latitudes[0]])
        for index_long in range(len(longitudes_no_abs_no_gap)):
            long_no_abs_cumulative[i].append(long_no_abs_cumulative[i][-1] + longitudes_no_abs_no_gap[index_long])
            lat_no_abs_cumulative[i].append(lat_no_abs_cumulative[i][-1] + latitudes_no_abs_no_gap[index_long])
            
        x_speed_cumulative.append([longitudes[0]]) 
        y_speed_cumulative.append([latitudes[0]])   
        for index_long in range(len(x_speed_alternative_no_gap)):
            x_speed_cumulative[i].append(x_speed_cumulative[i][-1] - x_speed_alternative_no_gap[index_long] * time_no_gap[index_long] + x_speed_alternative_no_gap[index_long] * time_no_gap[index_long] * 2 * predicted_longitude_sgn[i][index_long])
            y_speed_cumulative[i].append(y_speed_cumulative[i][-1] - y_speed_alternative_no_gap[index_long] * time_no_gap[index_long] + y_speed_alternative_no_gap[index_long] * time_no_gap[index_long] * 2 * predicted_latitude_sgn[i][index_long])
            
        x_speed_no_abs_cumulative.append([longitudes[0]])    
        y_speed_no_abs_cumulative.append([latitudes[0]])   
        for index_long in range(len(x_speed_no_abs_alternative_no_gap)):
            x_speed_no_abs_cumulative[i].append(x_speed_no_abs_cumulative[i][-1] + x_speed_no_abs_alternative_no_gap[index_long])
            y_speed_no_abs_cumulative[i].append(y_speed_no_abs_cumulative[i][-1] + y_speed_no_abs_alternative_no_gap[index_long])
            
        longitude_from_distance_heading_alternative.append([longitudes[0]])  
        latitude_from_distance_heading_alternative.append([latitudes[0]])  
        cumulative_heading = 0
        for index_long in range(len(distance_no_gap)):
            cumulative_heading = direction_alternative_no_gap[index_long]
            new_long, new_lat = get_sides_from_angle(distance_no_gap[index_long], cumulative_heading)
            longitude_from_distance_heading_alternative[i].append(longitude_from_distance_heading_alternative[i][-1] + new_long)
            latitude_from_distance_heading_alternative[i].append(latitude_from_distance_heading_alternative[i][-1] + new_lat)
            
        longitude_from_distance_heading.append([longitudes[0]])  
        latitude_from_distance_heading.append([latitudes[0]])  
        for index_long in range(len(distance_no_gap)):
            new_dir = (90 - direction_no_gap[index_long] + 360) % 360 
            if not x_dir: 
                new_dir = (180 - new_dir + 360) % 360
            if not y_dir: 
                new_dir = 360 - new_dir 
            new_long, new_lat = get_sides_from_angle(distance_no_gap[index_long], new_dir)
            longitude_from_distance_heading[i].append(longitude_from_distance_heading[i][-1] + new_long)
            latitude_from_distance_heading[i].append(latitude_from_distance_heading[i][-1] + new_lat)
            
        longitude_from_speed_alternative_time_heading_alternative.append([longitudes[0]])  
        latitude_from_speed_alternative_time_heading_alternative.append([latitudes[0]])  
        cumulative_heading = 0
        for index_long in range(len(time_no_gap)):
            cumulative_heading = direction_alternative_no_gap[index_long]
            new_long, new_lat = get_sides_from_angle(speed_alternative_no_gap[index_long] * time_no_gap[index_long], cumulative_heading)
            longitude_from_speed_alternative_time_heading_alternative[i].append(longitude_from_speed_alternative_time_heading_alternative[i][-1] + new_long)
            latitude_from_speed_alternative_time_heading_alternative[i].append(latitude_from_speed_alternative_time_heading_alternative[i][-1] + new_lat)
            
        longitude_from_speed_alternative_time_heading.append([longitudes[0]])  
        latitude_from_speed_alternative_time_heading.append([latitudes[0]])  
        for index_long in range(len(time_no_gap)): 
            new_dir = (90 - direction_no_gap[index_long] + 360) % 360 
            if not x_dir: 
                new_dir = (180 - new_dir + 360) % 360
            if not y_dir: 
                new_dir = 360 - new_dir 
            new_long, new_lat = get_sides_from_angle(speed_alternative_no_gap[index_long] * time_no_gap[index_long], new_dir)
            longitude_from_speed_alternative_time_heading[i].append(longitude_from_speed_alternative_time_heading[i][-1] + new_long)
            latitude_from_speed_alternative_time_heading[i].append(latitude_from_speed_alternative_time_heading[i][-1] + new_lat) 
            
        longitude_from_speed_time_heading_alternative.append([longitudes[0]])  
        latitude_from_speed_time_heading_alternative.append([latitudes[0]])  
        cumulative_heading = 0
        for index_long in range(len(time_no_gap)):
            cumulative_heading = direction_alternative_no_gap[index_long]
            new_long, new_lat = get_sides_from_angle(speed_no_gap[index_long] / 111 / 0.1 / 3600 * time_no_gap[index_long], cumulative_heading)
            longitude_from_speed_time_heading_alternative[i].append(longitude_from_speed_time_heading_alternative[i][-1] + new_long)
            latitude_from_speed_time_heading_alternative[i].append(latitude_from_speed_time_heading_alternative[i][-1] + new_lat) 
            
        longitude_from_speed_time_heading.append([longitudes[0]])  
        latitude_from_speed_time_heading.append([latitudes[0]])   
        for index_long in range(len(time_no_gap)): 
            new_dir = (90 - direction_no_gap[index_long] + 360) % 360 
            if not x_dir: 
                new_dir = (180 - new_dir + 360) % 360
            if not y_dir: 
                new_dir = 360 - new_dir 
            new_long, new_lat = get_sides_from_angle(speed_no_gap[index_long] / 111 / 0.1 / 3600 * time_no_gap[index_long], new_dir)
            longitude_from_speed_time_heading[i].append(longitude_from_speed_time_heading[i][-1] + new_long)
            latitude_from_speed_time_heading[i].append(latitude_from_speed_time_heading[i][-1] + new_lat)  
        i += 1 
        
current_ride_index = 0

def offset_ride(array_ride_x, array_ride_y):
    return [x - min(array_ride_x) for x in array_ride_x], [y - min(array_ride_y) for y in array_ride_y]
metric_names = ["simpson", "trapz", "simpson x", "trapz x", "simpson y", "trapz y", "euclidean", "custom", "dtw"]
metric_names = ["simpson", "trapz", "simpson x", "trapz x", "simpson y", "trapz y", "euclidean", "custom"] 
distance_predicted = dict()
distance_array = dict()
 
count_best_longit = dict()
count_best_latit = dict()
count_best_longit_latit = dict()

count_best_longit_metric = dict()
count_best_latit_metric = dict()
count_best_longit_latit_metric = dict() 
for metric_name in metric_names:
    count_best_longit_metric[metric_name] = dict()
    count_best_latit_metric[metric_name] = dict()
    count_best_longit_latit_metric[metric_name] = dict()

for subdir_name in all_subdirs: 
    if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
        continue 
    
    distance_predicted[subdir_name] = dict()
    distance_array[subdir_name] = dict()

    all_rides_cleaned = os.listdir(subdir_name + "/cleaned_csv/")
      
    all_files = os.listdir(subdir_name + "/cleaned_csv/") 
    bad_rides_filenames = set()
    if os.path.isfile(subdir_name + "/bad_rides_filenames"):
        bad_rides_filenames = load_object(subdir_name + "/bad_rides_filenames")
    train_rides = set()
    if os.path.isfile(subdir_name + "/train_rides"):
        train_rides= load_object(subdir_name + "/train_rides")
        
    for some_file in all_files:  
        if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or some_file in train_rides: 
            continue 
    
        file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
        longitudes = list(file_with_ride["fields_longitude"]) 
        latitudes = list(file_with_ride["fields_latitude"]) 
        times = transform_time(list(file_with_ride["time"]))
        longitudes, latitudes = preprocess_long_lat(longitudes, latitudes)
        longitudes, latitudes = scale_long_lat(longitudes, latitudes, 0.1, 0.1, True) 

        longitude_cumulative, latitude_cumulative = long_cumulative[current_ride_index], lat_cumulative[current_ride_index]
        longitude_no_abs_cumulative, latitude_no_abs_cumulative= long_no_abs_cumulative[current_ride_index], lat_no_abs_cumulative[current_ride_index]
        x_cumulative, y_cumulative = x_speed_cumulative[current_ride_index], y_speed_cumulative[current_ride_index]
        x_no_abs_cumulative, y_no_abs_cumulative = x_speed_no_abs_cumulative[current_ride_index], y_speed_no_abs_cumulative[current_ride_index]
        long_dist_dir_alt, lat_dist_dir_alt = longitude_from_distance_heading_alternative[current_ride_index], latitude_from_distance_heading_alternative[current_ride_index]
        long_dist_dir, lat_dist_dir = longitude_from_distance_heading[current_ride_index], latitude_from_distance_heading[current_ride_index]
        long_speed_alt_dir_alt, lat_speed_alt_dir_alt = longitude_from_speed_alternative_time_heading_alternative[current_ride_index], latitude_from_speed_alternative_time_heading_alternative[current_ride_index]
        long_speed_alt_dir, lat_speed_alt_dir = longitude_from_speed_alternative_time_heading[current_ride_index], latitude_from_speed_alternative_time_heading[current_ride_index]
        long_speed_dir_alt, lat_speed_dir_alt = longitude_from_speed_time_heading_alternative[current_ride_index], latitude_from_speed_time_heading_alternative[current_ride_index]
        long_speed_dir, lat_speed_dir = longitude_from_speed_time_heading[current_ride_index], latitude_from_speed_time_heading[current_ride_index]   
 
        #plt.plot(longitudes, latitudes, label = "original")
        #plt.plot(longitudes[0], latitudes[0], 'ro', label = "original")

        long_dict = {
            "long": longitude_cumulative,
            "long no abs": longitude_no_abs_cumulative,
            "x speed": x_cumulative,
            "x speed no abs": x_no_abs_cumulative,
            #"long dist dir alt": long_dist_dir_alt,
            "long dist dir": long_dist_dir,
            #"long speed alt dir alt": long_speed_alt_dir_alt,
            "long speed alt dir": long_speed_alt_dir, 
            #"long speed dir alt": long_speed_dir_alt,
            "long speed dir": long_speed_dir, 
        }

        lat_dict = {
            "lat": latitude_cumulative,
            "lat no abs": latitude_cumulative,
            "y speed": y_cumulative,
            "y speed no abs": y_no_abs_cumulative,
            #"lat dist dir alt": lat_dist_dir_alt,
            "lat dist dir": lat_dist_dir,
            #"lat speed alt dir alt": lat_speed_alt_dir_alt,
            "lat speed alt dir": lat_speed_alt_dir, 
            #"lat speed dir alt": lat_speed_dir_alt,
            "lat speed dir": lat_speed_dir, 
        }
 
        distance_predicted[subdir_name][some_file] = dict()
        distance_array[subdir_name][some_file] = dict()
        for metric_name in metric_names: 
            distance_predicted[subdir_name][some_file][metric_name] = dict()
            distance_array[subdir_name][some_file][metric_name] = dict()
            for latit in lat_dict:
                for longit in long_dict: 
                    #plt.plot(long_dict[longit], lat_dict[latit], label = longit + " " + latit)
                    distance_predicted[subdir_name][some_file][metric_name][longit + "-" + latit] = compare_traj_and_sample(long_dict[longit], lat_dict[latit], times_cumulative[current_ride_index], {"long": longitudes, "lat": latitudes, "time": times}, metric_name)
                    if " " in metric_name:    
                        distance_array[subdir_name][some_file][metric_name][longit + "-" + latit] = compare_traj_and_sample(long_dict[longit], lat_dict[latit], range(len(times_cumulative[current_ride_index])), {"long": longitudes, "lat": latitudes, "time": times}, metric_name)

        if "long" not in count_best_longit:
            for latit in lat_dict:
                count_best_latit[latit] = 0
                count_best_latit[latit + "-array"] = 0
                for longit in long_dict:
                    count_best_longit[longit] = 0
                    count_best_longit[longit + "-array"] = 0
                    count_best_longit_latit[longit + "-" + latit] = 0
                    count_best_longit_latit[longit + "-" + latit + "-array"] = 0
                for metric_name in metric_names:
                    count_best_latit_metric[metric_name][latit] = 0
                    count_best_latit_metric[metric_name][latit + "-array"] = 0
                    for longit in long_dict:
                        count_best_longit_metric[metric_name][longit] = 0
                        count_best_longit_metric[metric_name][longit + "-array"] = 0
                        count_best_longit_latit_metric[metric_name][longit + "-" + latit] = 0
                        count_best_longit_latit_metric[metric_name][longit + "-" + latit + "-array"] = 0

        #print(subdir_name, some_file) 
        for metric_name in metric_names:  
            min_for_metric = 100000
            best_name = ""
            for latit in lat_dict:
                for longit in long_dict: 
                    if distance_predicted[subdir_name][some_file][metric_name][longit + "-" + latit] < min_for_metric:
                        min_for_metric = distance_predicted[subdir_name][some_file][metric_name][longit + "-" + latit]
                        best_name = longit + "-" + latit
                    if " " in metric_name: 
                        if distance_array[subdir_name][some_file][metric_name][longit + "-" + latit] < min_for_metric:
                            min_for_metric = distance_array[subdir_name][some_file][metric_name][longit + "-" + latit]
                            best_name = longit + "-" + latit + "-array"
            #print(metric_name, best_name)
            count_best_longit_latit[best_name] += 1
            count_best_longit_latit_metric[metric_name][best_name] += 1
            if "array" in best_name: 
                count_best_longit[best_name.split("-")[0] + "-array"] += 1
                count_best_latit[best_name.split("-")[1] + "-array"] += 1
                count_best_longit_metric[metric_name][best_name.split("-")[0] + "-array"] += 1
                count_best_latit_metric[metric_name][best_name.split("-")[1] + "-array"] += 1
            else:
                count_best_longit[best_name.split("-")[0]] += 1
                count_best_latit[best_name.split("-")[1]] += 1
                count_best_longit_metric[metric_name][best_name.split("-")[0]] += 1
                count_best_latit_metric[metric_name][best_name.split("-")[1]] += 1
 
        #plt.legend()
        #plt.show()
  
        current_ride_index += 1

print("count_best_longit_latit")
for x in dict(sorted(count_best_longit_latit.items(), key=lambda item: item[1], reverse=True)):
    if count_best_longit_latit[x] > 0:
        print(x, count_best_longit_latit[x]) 
 
print("count_best_latit")
for x in dict(sorted(count_best_latit.items(), key=lambda item: item[1], reverse=True)):
    if count_best_latit[x] > 0:
        print(x, count_best_latit[x]) 

print("count_best_longit")
for x in dict(sorted(count_best_longit.items(), key=lambda item: item[1], reverse=True)):
    if count_best_longit[x] > 0:
        print(x, count_best_longit[x]) 

for metric_name in metric_names:
    print(metric_name, "count_best_longit_latit")
    for x in dict(sorted(count_best_longit_latit_metric[metric_name].items(), key=lambda item: item[1], reverse=True)):
        if count_best_longit_latit_metric[metric_name][x] > 0:
            print(x, count_best_longit_latit_metric[metric_name][x]) 
    
    print(metric_name, "count_best_latit")
    for x in dict(sorted(count_best_latit_metric[metric_name].items(), key=lambda item: item[1], reverse=True)):
        if count_best_latit_metric[metric_name][x] > 0:
            print(x, count_best_latit_metric[metric_name][x]) 

    print(metric_name, "count_best_longit")
    for x in dict(sorted(count_best_longit_metric[metric_name].items(), key=lambda item: item[1], reverse=True)):
        if count_best_longit[x] > 0:
            print(x, count_best_longit_metric[metric_name][x])    