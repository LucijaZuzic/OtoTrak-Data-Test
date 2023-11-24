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
    milisecond = int(time_as_str.split(".")[1])
    time_as_str = time_as_str.split(".")[0]
    epoch = datetime(1970, 1, 1)
    return (datetime.strptime(time_as_str, '%Y-%m-%d %H:%M:%S') - epoch).total_seconds() + milisecond / 1000

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
    times_ride = [time_one - times_ride[0] for time_one in times_ride] 
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
    
window_size = 20

def make_ray(radius, angle, sx, sy):
    return sx + np.cos(angle / 180 * np.pi) * radius, sy + np.sin(angle / 180 * np.pi) * radius


dotsx_original = []
dotsy_original = []
size = 8
for x in range(size):
	px, py = make_ray(0.5, 360 / size * x, 0.5, 0.5) 
	dotsx_original.append(px)
	dotsy_original.append(py)

def compare_traj_ray(test_x, test_y, scale = False, offset = False):
	
	dotsx = []
	dotsy = []
	for x in range(size):
		dotsx.append(dotsx_original[x])
		dotsy.append(dotsy_original[x])
		
	if scale:
		x_range = max(test_x) - min(test_x)
		y_range = max(test_y) - min(test_y)
		scaling_factor = max(x_range, y_range)
		
		for x1 in range(size): 
			if offset:
				dotsx[x1] = (min(test_x) + max(test_x)) / 2 - scaling_factor / 2 + dotsx[x1] * scaling_factor
				dotsy[x1] = (min(test_y) + max(test_y)) / 2 - scaling_factor / 2 + dotsy[x1] * scaling_factor 
			else:
				dotsx[x1] = min(test_x) + dotsx[x1] * scaling_factor
				dotsy[x1] = min(test_y) + dotsy[x1] * scaling_factor 
	'''
	for x1 in range(size):  
		for x2 in range(x1 + 1, size): 
			plt.plot([dotsx[x1], dotsx[x2]], [dotsy[x1], dotsy[x2]], 'g-')	 
	plt.plot(dotsx, dotsy, 'ro')
	if scale:
		if offset:
			plt.plot((min(test_x) + max(test_x)) / 2, (min(test_y) + max(test_y)) / 2, 'bo')
		else:
			plt.plot(min(test_x) + scaling_factor / 2, min(test_y) + scaling_factor / 2, 'bo')
	else:
		plt.plot(0.5, 0.5, 'bo')
	
	test_x = np.random.rand(window_size)  
	test_y = np.random.rand(window_size) 
	plt.plot(test_x, test_y, 'y-o')
	'''
	vectors_from_point = []
	intersections = []
	distances = []
	distancesx = []
	distancesy = []
	for x1 in range(size):
		vectors_from_point.append([])
		intersections.append([])
		distances.append([])
		distancesx.append([])
		distancesy.append([])
		for x2 in range(size):
			vectors_from_point[-1].append(0)
			intersections[-1].append([])
			distances[-1].append([])
			distancesx[-1].append([])
			distancesy[-1].append([])
			for t in range(window_size - 1):
				intersections[-1][-1].append(("Nan", "Nan"))
				distances[-1][-1].append(0)
				distancesx[-1][-1].append(0)
				distancesy[-1][-1].append(0) 
	'''
	vectors_all = []
	for x1 in range(size): 
		for x2 in range(x1 + 1, size):
			vector_new = get_vector(dotsx[x1], dotsx[x2], dotsy[x1], dotsy[x2])
			vectors_from_point[x1][x2] = vector_new
			vectors_from_point[x2][x1] = vector_new 
			vectors_all.append(vector_new)
			plt.plot([dotsx[x1], dotsx[x2]], [dotsy[x1], dotsy[x2]], 'g-')	
	''' 
	for x1 in range(size): 
		for x2 in range(x1 + 1, size): 
			sgnx12 = dotsx[x2] > dotsx[x1] 
			sgny12 = dotsy[x2] > dotsy[x1]  
			for t in range(window_size - 1): 
				xs, ys = get_intersection(test_x[t], test_x[t + 1], test_y[t], test_y[t + 1], dotsx[x1], dotsx[x2], dotsy[x1], dotsy[x2])
				if xs != "Nan":
					present = point_on_line(xs, ys, test_x[t], test_x[t + 1], test_y[t], test_y[t + 1])
					if present:
						#plt.plot(xs, ys, 'mo')
						
						d1x = abs(dotsx[x1] - xs)
						d1y = abs(dotsy[x1] - ys)
						
						d2x = abs(dotsx[x2] - xs)
						d2y = abs(dotsy[x2] - ys)
						
						d1 = np.sqrt(d1x ** 2 + d1y ** 2)
						d2 = np.sqrt(d2x ** 2 + d2y ** 2)
						
						sgnxs1 = dotsx[x1] > xs
						sgnys1 = dotsy[x1] > ys
						
						sgnxs2 = dotsx[x2] > xs 
						sgnys2 = dotsy[x2] > ys
						
						if sgnxs1 != sgnx12 and sgnys1 != sgny12:
							intersections[x1][x2][t] = (xs, ys) 
							distances[x1][x2][t] = d1 
							distancesx[x1][x2][t] = d1x
							distancesy[x1][x2][t] = d1y
							
						if sgnxs2 == sgnx12 and sgnys2 == sgny12:
							intersections[x2][x1][t] = (xs, ys) 
							distances[x2][x1][t] = d2 
							distancesx[x2][x1][t] = d2x
							distancesy[x2][x1][t] = d2y 
	'''
	for t in range(window_size - 1): 			
		for x1 in range(size):
			for x2 in range(size):
				print(intersections[x1][x2][t], distances[x1][x2][t])
			print()
	'''
	all_distances = 0	
	all_distancesx = 0	
	all_distancesy = 0		
	for t in range(window_size - 1): 	
		for x1 in range(size): 
			for x2 in range(size):
				all_distances += distances[x1][x2][t]
				all_distancesx += distancesx[x1][x2][t]
				all_distancesy += distancesy[x1][x2][t]
	all_distances /= (size ** 2) * window_size 
	all_distancesx /= (size ** 2) * window_size 
	all_distancesy /= (size ** 2) * window_size 
	if scale:
		all_distances /= scaling_factor	
		all_distancesx /= scaling_factor	
		all_distancesy /= scaling_factor	
	#print(all_distances, all_distancesx, all_distancesy)
	#plt.show()
	return all_distances, all_distancesx, all_distancesy

deg = 5
maxoffset = 0.005
step_size = window_size
#step_size = 1
max_trajs = 100
name_extension = "_window_" + str(window_size) + "_step_" + str(step_size) + "_segments_" + str(max_trajs)

all_subdirs = os.listdir()  

all_distances_trajs = dict()   
all_distances_trajs[window_size] = dict()

all_distances_preprocessed_trajs = dict()   
all_distances_preprocessed_trajs[window_size] = dict()

all_distances_scaled_trajs = dict()   
all_distances_scaled_trajs[window_size] = dict()

all_distances_scaled_to_max_trajs = dict()   
all_distances_scaled_to_max_trajs[window_size] = dict()

total_possible_trajs = 0
  
for subdir_name in all_subdirs:

    trajs_in_dir = 0
    
    if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
        continue
    print(subdir_name)  
    all_distances_trajs[window_size][subdir_name] = dict() 
    all_distances_preprocessed_trajs[window_size][subdir_name] = dict() 
    all_distances_scaled_trajs[window_size][subdir_name] = dict() 
    all_distances_scaled_to_max_trajs[window_size][subdir_name] = dict()  

    all_rides_cleaned = os.listdir(subdir_name + "/cleaned_csv/")
    
    all_files = os.listdir(subdir_name + "/cleaned_csv/") 
    bad_rides_filenames = set()
    if os.path.isfile(subdir_name + "/bad_rides_filenames"):
        bad_rides_filenames = load_object(subdir_name + "/bad_rides_filenames")
        
    for some_file in all_files:  
        if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames:
            #print("Skipped ride", some_file)
            continue
        #print("Used ride", some_file)

        only_num_ride = some_file.replace(".csv", "").replace("events_", "")
        
        trajs_in_ride = 0
 
        all_distances_trajs[window_size][subdir_name][only_num_ride] = dict()
        all_distances_preprocessed_trajs[window_size][subdir_name][only_num_ride] = dict()
        all_distances_scaled_trajs[window_size][subdir_name][only_num_ride] = dict()
        all_distances_scaled_to_max_trajs[window_size][subdir_name][only_num_ride] = dict() 
        
        file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
        longitudes = list(file_with_ride["fields_longitude"])
        latitudes = list(file_with_ride["fields_latitude"]) 
        times = list(file_with_ride["time"])  
  
        for x in range(0, len(longitudes) - window_size + 1, step_size):
            longitudes_tmp = longitudes[x:x + window_size]
            latitudes_tmp = latitudes[x:x + window_size]
            times_tmp = times[x:x + window_size] 

            set_longs = set()
            set_lats = set()
            set_points = set()
            for tmp_long in longitudes_tmp:
                set_longs.add(tmp_long)
            for tmp_lat in latitudes_tmp:
                set_lats.add(tmp_lat)
            for some_index in range(len(latitudes_tmp)):
                set_points.add((latitudes_tmp[some_index], longitudes_tmp[some_index]))
                
            if len(set_lats) == 1 or len(set_longs) == 1:
                continue   
            if len(set_points) < 3:
                continue   
            
            longitudes_tmp_transform, latitudes_tmp_transform = preprocess_long_lat(longitudes_tmp, latitudes_tmp)
            
            longitudes_scaled, latitudes_scaled = scale_long_lat(longitudes_tmp_transform, latitudes_tmp_transform)
            
            longitudes_scaled_to_max, latitudes_scaled_to_max = scale_long_lat(longitudes_tmp_transform, latitudes_tmp_transform, xmax = maxoffset, ymax = maxoffset, keep_aspect_ratio = True)
		
            #times_tmp_transform = transform_time(times_tmp)

            total_possible_trajs += 1
            trajs_in_ride += 1
            trajs_in_dir += 1
            
            all_distances_trajs[window_size][subdir_name][only_num_ride][x] = {"scale": compare_traj_ray(longitudes_tmp, latitudes_tmp, True, False), "offset": compare_traj_ray(longitudes_tmp, latitudes_tmp, True, True), "no scale": compare_traj_ray(longitudes_tmp, latitudes_tmp, False, False)}
            all_distances_preprocessed_trajs[window_size][subdir_name][only_num_ride][x] = {"scale": compare_traj_ray(longitudes_tmp_transform, latitudes_tmp_transform, True, False), "offset": compare_traj_ray(longitudes_tmp_transform, latitudes_tmp_transform, True, True), "no scale": compare_traj_ray(longitudes_tmp_transform, latitudes_tmp_transform, False, False)}
            all_distances_scaled_trajs[window_size][subdir_name][only_num_ride][x] = {"scale": compare_traj_ray(longitudes_scaled, latitudes_scaled, True, False), "offset": compare_traj_ray(longitudes_scaled, latitudes_scaled, True, True), "no scale": compare_traj_ray(longitudes_scaled, latitudes_scaled, False, False)} 
            all_distances_scaled_to_max_trajs[window_size][subdir_name][only_num_ride][x] = {"scale": compare_traj_ray(longitudes_scaled_to_max, latitudes_scaled_to_max, True, False), "offset": compare_traj_ray(longitudes_scaled_to_max, latitudes_scaled_to_max, True, True), "no scale": compare_traj_ray(longitudes_scaled_to_max, latitudes_scaled_to_max, False, False)}
  
def process_csv(some_dict, save_name): 
    new_csv_content = "window_size,vehicle,ride,start,scale,scale_x,scale_y,offset,offset_x,offset_y,no_scale,no_scale_x,no_scale_y\n"
    for vehicle1 in some_dict[window_size].keys():  
        for r1 in some_dict[window_size][vehicle1]:
            for x1 in some_dict[window_size][vehicle1][r1]: 
                new_csv_content += str(window_size) + "," + str(vehicle1) + "," + str(r1) + "," + str(x1) + ","  
                for feat_name in some_dict[window_size][vehicle1][r1][x1]:  
                	for val in some_dict[window_size][vehicle1][r1][x1][feat_name]:  
                		new_csv_content += str(val) + "," 
                new_csv_content += "\n"
    csv_file = open(save_name, "w")
    csv_file.write(new_csv_content)
    csv_file.close()
  
process_csv(all_distances_trajs, "all_distances_trajs.csv")
process_csv(all_distances_preprocessed_trajs, "all_distances_preprocessed_trajs.csv")
process_csv(all_distances_scaled_trajs, "all_distances_scaled_trajs.csv")
process_csv(all_distances_scaled_to_max_trajs, "all_distances_scaled_to_max_trajs.csv")
