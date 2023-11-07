import matplotlib.pyplot as plt
import os
import pandas as pd
from PIL import Image
import numpy as np
from sklearn import manifold
from sklearn.cluster import DBSCAN, KMeans
import pickle

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

def read_an_image(image_name):
    img = Image.open(image_name) 
    new_size = (100, 100)
    img = img.resize(new_size)
    img_data = img.getdata()

    lst = []
    for i in img_data: 
        # lst.append(i[0]*0.299+i[1]*0.587+i[2]*0.114) ### Rec. 609-7 weights
        lst.append(i[0]*0.2125+i[1]*0.7174+i[2]*0.0721) ### Rec. 709-6 weights

    new_img = Image.new("L", img.size)
    new_img.putdata(lst) 
    new_img = new_img.save(image_name, bbox_inches = 'tight') 
    return lst

def make_LocallyLinearEmbedding(data_matrix):
    df_data_matrix = pd.DataFrame(data = data_matrix)
    LLE_data_matrix = manifold.LocallyLinearEmbedding(n_neighbors = 6, n_components = 2)
    LLE_data_matrix.fit(df_data_matrix)
    return LLE_data_matrix

def make_manifold(LLE_data_matrix, data_matrix):
    manifold_2D_LLEa = LLE_data_matrix.transform(data_matrix)
    manifold_2D_LLE = pd.DataFrame(manifold_2D_LLEa, columns = ['Component 1', 'Component 2'])
    return manifold_2D_LLE
    
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
    
def plot_multi_LocallyLinearEmbedding(LLE_data_matrix, multi_data_matrix, save_name, title_LocallyLinearEmbedding, label_names):  
    random_color_list = random_colors(len(multi_data_matrix))
    plt.title(title_LocallyLinearEmbedding)
    for data_matrix_index in range(len(multi_data_matrix)):
        name_multi_manifold = save_name.replace(".png", "_" + label_names[data_matrix_index])  
        if not os.path.isfile(name_multi_manifold) or use_multi_LocallyLinearEmbedding:
            manifold_2D_LLEa = LLE_data_matrix.transform(multi_data_matrix[data_matrix_index]) 
            manifold_2D_LLE = pd.DataFrame(manifold_2D_LLEa, columns = ['Component 1', 'Component 2'])
            save_object(name_multi_manifold, manifold_2D_LLE)
        else: 
            manifold_2D_LLE = load_object(name_multi_manifold)
        plt.scatter(manifold_2D_LLE['Component 1'], manifold_2D_LLE['Component 2'], marker = '.', color = random_color_list[data_matrix_index], label = label_names[data_matrix_index])
         
    plt.legend()
    plt.savefig(save_name)
    plt.close()
    
def plot_LocallyLinearEmbedding(manifold_2D_LLE, longs_matrix, lats_matrix, save_name):  
    maxx = max(manifold_2D_LLE['Component 1'])
    maxy = max(manifold_2D_LLE['Component 2'])
    minx = min(manifold_2D_LLE['Component 1'])
    miny = min(manifold_2D_LLE['Component 2'])
    
    top_left = np.sqrt((maxx - minx) ** 2 + (maxy - miny) ** 2)
    top_center = np.sqrt((maxx - minx) ** 2 + (maxy - miny) ** 2)
    top_right = np.sqrt((maxx - minx) ** 2 + (maxy - miny) ** 2)
    mid_left = np.sqrt((maxx - minx) ** 2 + (maxy - miny) ** 2)
    mid_center = np.sqrt((maxx - minx) ** 2 + (maxy - miny) ** 2)
    mid_right = np.sqrt((maxx - minx) ** 2 + (maxy - miny) ** 2)
    bottom_left = np.sqrt((maxx - minx) ** 2 + (maxy - miny) ** 2)
    bottom_center = np.sqrt((maxx - minx) ** 2 + (maxy - miny) ** 2)
    bottom_right = np.sqrt((maxx - minx) ** 2 + (maxy - miny) ** 2) 
    
    top_left_index = 0
    top_center_index = 0
    top_right_index = 0
    mid_left_index = 0
    mid_center_index = 0
    mid_right_index = 0
    bottom_left_index = 0
    bottom_center_index = 0
    bottom_right_index = 0
    
    for x in range(len(manifold_2D_LLE['Component 1'])):
        x_dist_right = maxx - manifold_2D_LLE['Component 1'][x]
        x_dist_left = manifold_2D_LLE['Component 1'][x] - minx
        x_dist_center = abs(manifold_2D_LLE['Component 1'][x] - (maxx + minx) / 2)
        y_dist_top = maxy - manifold_2D_LLE['Component 2'][x]
        y_dist_mid = abs(manifold_2D_LLE['Component 2'][x] - (maxy + miny) / 2)
        y_dist_bottom = manifold_2D_LLE['Component 2'][x] - miny
        
        top_left_tmp = np.sqrt(y_dist_top ** 2 + x_dist_left ** 2)
        
        if top_left_tmp < top_left:
            top_left_index = x
            top_left = top_left_tmp
            
        top_center_tmp = np.sqrt(y_dist_top ** 2 + x_dist_center ** 2)
        
        if top_center_tmp < top_center:
            top_center_index = x
            top_center = top_center_tmp

        top_right_tmp = np.sqrt(y_dist_top ** 2 + x_dist_right ** 2)
        
        if top_right_tmp < top_right:
            top_right_index = x
            top_right = top_right_tmp
            mid_left_tmp = np.sqrt(y_dist_mid ** 2 + x_dist_left ** 2)
            
        mid_left_tmp = np.sqrt(y_dist_mid ** 2 + x_dist_left ** 2)
        
        if mid_left_tmp < mid_left:
            mid_left_index = x
            mid_left = mid_left_tmp
            
        mid_center_tmp = np.sqrt(y_dist_mid ** 2 + x_dist_center ** 2)

        if mid_center_tmp < mid_center:
            mid_center_index = x
            mid_center = mid_center_tmp

        mid_right_tmp = np.sqrt(y_dist_mid ** 2 + x_dist_right ** 2)

        if mid_right_tmp < mid_right:
            mid_right_index = x
            mid_right = mid_right_tmp
        
        bottom_left_tmp = np.sqrt(y_dist_bottom ** 2 + x_dist_left ** 2)
        
        if bottom_left_tmp < bottom_left:
            bottom_left_index = x
            bottom_left = bottom_left_tmp
            
        bottom_center_tmp = np.sqrt(y_dist_bottom ** 2 + x_dist_center ** 2)

        if bottom_center_tmp < bottom_center:
            bottom_center_index = x
            bottom_center = bottom_center_tmp

        bottom_right_tmp = np.sqrt(y_dist_bottom ** 2 + x_dist_right ** 2)

        if bottom_right_tmp < bottom_right:
            bottom_right_index = x
            bottom_right = bottom_right_tmp
            
    # Left with 2 dimensions
    print(manifold_2D_LLE.head())

    # Show 2D components plot
    plt.figure(figsize = (20, 20))
    plt.subplot(3, 4, 1)
    plt.title(save_name.split("/")[0])
    plt.scatter(manifold_2D_LLE['Component 1'], manifold_2D_LLE['Component 2'], marker = '.', color = 'cyan')
    plt.scatter(manifold_2D_LLE['Component 1'][top_left_index], manifold_2D_LLE['Component 2'][top_left_index], color = 'blue', marker='.', linewidth = 5) 
    plt.scatter(manifold_2D_LLE['Component 1'][top_center_index], manifold_2D_LLE['Component 2'][top_center_index], color = 'orange', marker='.', linewidth = 5) 
    plt.scatter(manifold_2D_LLE['Component 1'][top_right_index], manifold_2D_LLE['Component 2'][top_right_index], color = 'green', marker='.', linewidth = 5) 
    plt.scatter(manifold_2D_LLE['Component 1'][mid_left_index], manifold_2D_LLE['Component 2'][mid_left_index], color = 'red', marker='.', linewidth = 5) 
    plt.scatter(manifold_2D_LLE['Component 1'][mid_center_index], manifold_2D_LLE['Component 2'][mid_center_index], color = 'purple', marker='.', linewidth = 5) 
    plt.scatter(manifold_2D_LLE['Component 1'][mid_right_index], manifold_2D_LLE['Component 2'][mid_right_index], color = 'brown', marker='.', linewidth = 5) 
    plt.scatter(manifold_2D_LLE['Component 1'][bottom_left_index], manifold_2D_LLE['Component 2'][bottom_left_index], color = 'pink', marker='.', linewidth = 5) 
    plt.scatter(manifold_2D_LLE['Component 1'][bottom_center_index], manifold_2D_LLE['Component 2'][bottom_center_index], color = 'gray', marker='.', linewidth = 5)  
    plt.scatter(manifold_2D_LLE['Component 1'][bottom_right_index], manifold_2D_LLE['Component 2'][bottom_right_index], color = 'olive', marker='.', linewidth = 5)  
      
    plt.subplot(3, 4, 2)
    plt.title("Top left")
    plt.xticks([min(longs_matrix[top_left_index]), max(longs_matrix[top_left_index])], [np.round(min(longs_matrix[top_left_index]), 3), np.round(max(longs_matrix[top_left_index]), 3)]) 
    plt.yticks([min(lats_matrix[top_left_index]), max(lats_matrix[top_left_index])], [np.round(min(lats_matrix[top_left_index]), 3), np.round(max(lats_matrix[top_left_index]), 3)])
    plt.plot(longs_matrix[top_left_index], lats_matrix[top_left_index], color = 'blue', linewidth = 10)
    plt.subplot(3, 4, 3)
    plt.title("Top center")
    plt.xticks([min(longs_matrix[top_center_index]), max(longs_matrix[top_center_index])], [np.round(min(longs_matrix[top_center_index]), 3), np.round(max(longs_matrix[top_center_index]), 3)]) 
    plt.yticks([min(lats_matrix[top_center_index]), max(lats_matrix[top_center_index])], [np.round(min(lats_matrix[top_center_index]), 3), np.round(max(lats_matrix[top_center_index]), 3)])
    plt.plot(longs_matrix[top_center_index], lats_matrix[top_center_index], color = 'orange', linewidth = 10)
    plt.subplot(3, 4, 4)
    plt.title("Top right")
    plt.xticks([min(longs_matrix[top_right_index]), max(longs_matrix[top_right_index])], [np.round(min(longs_matrix[top_right_index]), 3), np.round(max(longs_matrix[top_right_index]), 3)]) 
    plt.yticks([min(lats_matrix[top_right_index]), max(lats_matrix[top_right_index])], [np.round(min(lats_matrix[top_right_index]), 3), np.round(max(lats_matrix[top_right_index]), 3)])
    plt.plot(longs_matrix[top_right_index], lats_matrix[top_right_index], color = 'green', linewidth = 10)
    
    plt.subplot(3, 4, 6)
    plt.title("Mid left")
    plt.xticks([min(longs_matrix[mid_left_index]), max(longs_matrix[mid_left_index])], [np.round(min(longs_matrix[mid_left_index]), 3), np.round(max(longs_matrix[mid_left_index]), 3)]) 
    plt.yticks([min(lats_matrix[mid_left_index]), max(lats_matrix[mid_left_index])], [np.round(min(lats_matrix[mid_left_index]), 3), np.round(max(lats_matrix[mid_left_index]), 3)])
    plt.plot(longs_matrix[mid_left_index], lats_matrix[mid_left_index], color = 'red', linewidth = 10)
    plt.subplot(3, 4, 7)
    plt.title("Mid center")
    plt.xticks([min(longs_matrix[mid_center_index]), max(longs_matrix[mid_center_index])], [np.round(min(longs_matrix[mid_center_index]), 3), np.round(max(longs_matrix[mid_center_index]), 3)]) 
    plt.yticks([min(lats_matrix[mid_center_index]), max(lats_matrix[mid_center_index])], [np.round(min(lats_matrix[mid_center_index]), 3), np.round(max(lats_matrix[mid_center_index]), 3)])
    plt.plot(longs_matrix[mid_center_index], lats_matrix[mid_center_index], color = 'purple', linewidth = 10)
    plt.subplot(3, 4, 8)
    plt.title("Mid right")
    plt.xticks([min(longs_matrix[mid_right_index]), max(longs_matrix[mid_right_index])], [np.round(min(longs_matrix[mid_right_index]), 3), np.round(max(longs_matrix[mid_right_index]), 3)]) 
    plt.yticks([min(lats_matrix[mid_right_index]), max(lats_matrix[mid_right_index])], [np.round(min(lats_matrix[mid_right_index]), 3), np.round(max(lats_matrix[mid_right_index]), 3)])
    plt.plot(longs_matrix[mid_right_index], lats_matrix[mid_right_index], color = 'brown', linewidth = 10)

    plt.subplot(3, 4, 10)
    plt.title("Bottom left")
    plt.xticks([min(longs_matrix[bottom_left_index]), max(longs_matrix[bottom_left_index])], [np.round(min(longs_matrix[bottom_left_index]), 3), np.round(max(longs_matrix[bottom_left_index]), 3)]) 
    plt.yticks([min(lats_matrix[bottom_left_index]), max(lats_matrix[bottom_left_index])], [np.round(min(lats_matrix[bottom_left_index]), 3), np.round(max(lats_matrix[bottom_left_index]), 3)])
    plt.plot(longs_matrix[bottom_left_index], lats_matrix[bottom_left_index], color = 'pink', linewidth = 10)
    plt.subplot(3, 4, 11)
    plt.title("Bottom center")
    plt.xticks([min(longs_matrix[bottom_center_index]), max(longs_matrix[bottom_center_index])], [np.round(min(longs_matrix[bottom_center_index]), 3), np.round(max(longs_matrix[bottom_center_index]), 3)]) 
    plt.yticks([min(lats_matrix[bottom_center_index]), max(lats_matrix[bottom_center_index])], [np.round(min(lats_matrix[bottom_center_index]), 3), np.round(max(lats_matrix[bottom_center_index]), 3)])
    plt.plot(longs_matrix[bottom_center_index], lats_matrix[bottom_center_index], color = 'gray', linewidth = 10)
    plt.subplot(3, 4, 12)
    plt.title("Bottom right")
    plt.xticks([min(longs_matrix[bottom_right_index]), max(longs_matrix[bottom_right_index])], [np.round(min(longs_matrix[bottom_right_index]), 3), np.round(max(longs_matrix[bottom_right_index]), 3)]) 
    plt.yticks([min(lats_matrix[bottom_right_index]), max(lats_matrix[bottom_right_index])], [np.round(min(lats_matrix[bottom_right_index]), 3), np.round(max(lats_matrix[bottom_right_index]), 3)])
    plt.plot(longs_matrix[bottom_right_index], lats_matrix[bottom_right_index], color = 'olive', linewidth = 10)

    plt.savefig(save_name)
    plt.close()

def make_cluster(manifold_2D_LLE):
    X_clus = []
    for x in range(len(manifold_2D_LLE['Component 1'])):
        X_clus.append([manifold_2D_LLE['Component 1'][x], manifold_2D_LLE['Component 2'][x]])
    X_clus = np.array(X_clus)	  
    clustering_DBSCAN_LLE = DBSCAN(eps = 1000, min_samples = 2).fit(X_clus)
    return clustering_DBSCAN_LLE

def make_cluster_KMeans(manifold_2D_LLE):
    X_clus = []
    for x in range(len(manifold_2D_LLE['Component 1'])):
        X_clus.append([manifold_2D_LLE['Component 1'][x], manifold_2D_LLE['Component 2'][x]])
    X_clus = np.array(X_clus)	  
    clustering_KMeans_LLE = KMeans(n_clusters=2, random_state=0, n_init="auto").fit(X_clus)
    return clustering_KMeans_LLE
    
def make_multi_cluster(manifold_2D_LLE_multiple):
    X_clus = []
    for manifold_2D_LLE in manifold_2D_LLE_multiple:
        for x in range(len(manifold_2D_LLE['Component 1'])):
            X_clus.append([manifold_2D_LLE['Component 1'][x], manifold_2D_LLE['Component 2'][x]])
    X_clus = np.array(X_clus)	  
    clustering_DBSCAN_LLE = DBSCAN(eps = 1000, min_samples = 2).fit(X_clus)
    return clustering_DBSCAN_LLE

def make_multi_cluster_KMeans(manifold_2D_LLE_multiple):
    X_clus = []
    for manifold_2D_LLE in manifold_2D_LLE_multiple:
        for x in range(len(manifold_2D_LLE['Component 1'])):
            X_clus.append([manifold_2D_LLE['Component 1'][x], manifold_2D_LLE['Component 2'][x]])
    X_clus = np.array(X_clus)	  
    clustering_KMeans_LLE = KMeans(n_clusters=2, random_state=0, n_init="auto").fit(X_clus)
    return clustering_KMeans_LLE
    
def plot_cluster_LLE(manifold_2D_LLE, clustering_DBSCAN_LLE, save_name):
    x_labs = clustering_DBSCAN_LLE.labels_
    set_cluster = dict()
    for x in x_labs:
        set_cluster[x] = set()
    colors_set = random_colors(len(set_cluster) + 1)
    for x in set_cluster:
    	for i in range(len(x_labs)):
    	    if x_labs[i] == x:
                set_cluster[x].add(i) 
    counter = 0
    plt.scatter(manifold_2D_LLE['Component 1'], manifold_2D_LLE['Component 2'], color = colors_set[counter], marker='.', label = save_name.split("/")[0], alpha = 0.2) 
    for x in set_cluster:
        num_in_cluster = 0
        counter += 1 
        for i in set_cluster[x]: 
            if num_in_cluster > 0:
                plt.scatter(manifold_2D_LLE['Component 1'][i], manifold_2D_LLE['Component 2'][i], color = colors_set[counter], marker='.')  
            else:
                plt.scatter(manifold_2D_LLE['Component 1'][i], manifold_2D_LLE['Component 2'][i], color = colors_set[counter], marker='.', label = x)  
            num_in_cluster += 1
        
    plt.legend(ncol = 5, loc = 'lower center', bbox_to_anchor=(0.5, -0.5)) 
    plt.title(save_name.split("/")[0])
    plt.savefig(save_name, bbox_inches = 'tight')
    plt.close()
    
def plot_multi_cluster(manifold_2D_LLE_multiple, clustering_DBSCAN_LLE, save_name, cluster_names):
    x_labs = clustering_DBSCAN_LLE.labels_
    set_cluster = dict()
    for x in x_labs:
        set_cluster[x] = set()
    colors_set = random_colors(len(set_cluster) + len(manifold_2D_LLE_multiple))
    for x in set_cluster:
    	for i in range(len(x_labs)): 
    	    if x_labs[i] == x:
                set_cluster[x].add(i) 
    counter = 0
    X_clus = []
    for manifold_2D_LLE in manifold_2D_LLE_multiple: 
        for x in range(len(manifold_2D_LLE['Component 1'])):
            X_clus.append([manifold_2D_LLE['Component 1'][x], manifold_2D_LLE['Component 2'][x]])
        plt.scatter(manifold_2D_LLE['Component 1'], manifold_2D_LLE['Component 2'], color = colors_set[counter], marker='.', label = cluster_names[counter], alpha = 0.2) 
        counter += 1 
    for x in set_cluster:
        num_in_cluster = 0
        for i in set_cluster[x]: 
            if num_in_cluster > 0:
                plt.scatter(X_clus[i][0], X_clus[i][1], color = colors_set[counter], marker='.') 
            else:
                plt.scatter(X_clus[i][0], X_clus[i][1], color = colors_set[counter], marker='.', label = x) 
            num_in_cluster += 1
        counter += 1 
        
    plt.legend(ncol = 5, loc = 'lower center', bbox_to_anchor=(0.5, -0.5)) 
    plt.title(save_name.split("/")[0])
    plt.savefig(save_name, bbox_inches = 'tight')
    plt.close()
    
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

    quadrant = 0

    if x_dir == True and y_dir == True:
        quadrant = 1
    if x_dir == False and y_dir == True:
        quadrant = 2
    if x_dir == False and y_dir == False:
        quadrant = 3
    if x_dir == True and y_dir == False:
        quadrant = 4
 
    long_list2 = [x - min(long_list) for x in long_list]
    lat_list2 = [y - min(lat_list) for y in lat_list]
    if x_dir == False: 
        long_list2 = [max(long_list2) - x for x in long_list2]
    if y_dir == False:
        lat_list2 = [max(lat_list2) - y for y in lat_list2]

    return long_list2, lat_list2, quadrant
 
window_size = 20
step_size = window_size
max_trajs = 1000
name_extension = "_window_" + str(window_size) + "_step_" + str(step_size) + "_segments_" + str(max_trajs)

all_subdirs = os.listdir() 

use_LocallyLinearEmbedding = False 
draw_LocallyLinearEmbedding = False 

use_DBSCAN = False 
draw_DBSCAN = False 

use_KMeans = True 
draw_KMeans = True 

use_multi_LocallyLinearEmbedding = False
draw_multi_LocallyLinearEmbedding = False

use_multi_DBSCAN = False
draw_multi_DBSCAN = False

use_multi_KMeans = False
draw_multi_KMeans = False
 
image_matrix_list = []  
LocallyLinearEmbedding_list = [] 
subdir_names = []

for subdir_name in all_subdirs: 
    if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
        continue
    if not use_LocallyLinearEmbedding:
        if os.path.isfile(subdir_name + "/manifold_2D_LLE" + name_extension):
            longs_matrix = load_object(subdir_name + "/longs_matrix" + name_extension)
            lats_matrix = load_object(subdir_name + "/lats_matrix" + name_extension)
            image_matrix = load_object(subdir_name + "/image_matrix" + name_extension)  
            image_matrix_list.append(image_matrix)
            LLE_matrix = load_object(subdir_name + "/LLE_matrix" + name_extension) 
            LocallyLinearEmbedding_list.append(LLE_matrix)
            manifold_2D_LLE = load_object(subdir_name + "/manifold_2D_LLE" + name_extension)  
            
            if draw_LocallyLinearEmbedding:
                plot_LocallyLinearEmbedding(manifold_2D_LLE, longs_matrix, lats_matrix, subdir_name + "/plot_LocallyLinearEmbedding" + name_extension + ".png")   
        
            if use_DBSCAN:
                clustering_DBSCAN_LLE = make_cluster(manifold_2D_LLE)
                save_object(subdir_name + "/clustering_DBSCAN_LLE" + name_extension, clustering_DBSCAN_LLE)
                
            if not use_DBSCAN and os.path.isfile(subdir_name + "/clustering_DBSCAN_LLE" + name_extension):
                clustering_DBSCAN_LLE = load_object(subdir_name + "/clustering_DBSCAN_LLE" + name_extension)
                
            if draw_DBSCAN:
                plot_cluster_LLE(manifold_2D_LLE, clustering_DBSCAN_LLE, subdir_name + "/plot_cluster_LLE" + name_extension + ".png")    
                 
            if use_KMeans:
                clustering_KMeans_LLE = make_cluster(manifold_2D_LLE)
                save_object(subdir_name + "/clustering_KMeans_LLE" + name_extension, clustering_KMeans_LLE)
                
            if not use_KMeans and os.path.isfile(subdir_name + "/clustering_KMeans_LLE" + name_extension):
                clustering_KMeans_LLE = load_object(subdir_name + "/clustering_KMeans_LLE" + name_extension)
                
            if draw_KMeans:
                plot_cluster_LLE(manifold_2D_LLE, clustering_KMeans_LLE, subdir_name + "/plot_cluster_KMeans_LLE" + name_extension + ".png")  
                
        continue
    
    image_matrix = []
    longs_matrix = []
    lats_matrix = []
    
    all_rides_cleaned = os.listdir(subdir_name + "/cleaned_csv/")
    
    num_trajs = 0   
    total_frames_all = 0
    skipped_frames_all = 0
    
    all_files = os.listdir(subdir_name + "/cleaned_csv/") 
    bad_rides_filenames = set()
    if os.path.isfile(subdir_name + "/bad_rides_filenames"):
        bad_rides_filenames = load_object(subdir_name + "/bad_rides_filenames")
        
    for some_file in all_files:  
        if some_file in bad_rides_filenames:
            print("Skipped ride", some_file)
            continue
        print("Used ride", some_file)
    
        file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
        longitudes = list(file_with_ride["fields_longitude"])
        latitudes = list(file_with_ride["fields_latitude"]) 
        total_frames = 0
        skipped_frames = 0
        for x in range(0, len(longitudes) - window_size + 1, step_size):
            longitudes_tmp = longitudes[x:x + window_size]
            latitudes_tmp = latitudes[x:x + window_size]
            set_longs = set()
            set_lats = set()
            for tmp_long in longitudes_tmp:
                set_longs.add(tmp_long)
            for tmp_lat in latitudes_tmp:
                set_lats.add(tmp_lat)
            total_frames_all += 1
            total_frames += 1
            if len(set_lats) == 1 and len(set_longs) == 1: 
                skipped_frames_all += 1
                skipped_frames += 1
                continue 
            longitudes_tmp, latitudes_tmp, quadrant = preprocess_long_lat(longitudes_tmp, latitudes_tmp) 
            new_dir_img = subdir_name + "/images/" + some_file.replace("events_", "").replace(".csv", "/" + str(window_size) + "/")   
            if not os.path.isdir(new_dir_img):
                os.makedirs(new_dir_img)
            image_name = new_dir_img + str(x) + ".png"
            if not os.path.isfile(image_name):
                save_plot_longitude_latitudes_for_ride(longitudes_tmp, latitudes_tmp, image_name)
                lst = read_an_image(image_name) 
            else:
                img_tmp = Image.open(image_name)  
                lst = list(img_tmp.getdata()) 
            image_matrix.append(lst)
            longs_matrix.append(longitudes_tmp)
            lats_matrix.append(latitudes_tmp)  
            num_trajs += 1
            if max_trajs == num_trajs:
                break
        if max_trajs == num_trajs:
            break  
    
    if len(image_matrix) < max_trajs:
        print("Skipping", subdir_name)
        continue
    subdir_names.append(subdir_name)
    print(subdir_name)
            
    print(total_frames_all, skipped_frames_all)   
 
    save_object(subdir_name + "/longs_matrix" + name_extension, longs_matrix)
    save_object(subdir_name + "/lats_matrix" + name_extension, lats_matrix)
    save_object(subdir_name + "/image_matrix" + name_extension, image_matrix) 
    image_matrix_list.append(image_matrix)
     
    LLE_matrix = make_LocallyLinearEmbedding(image_matrix)
    save_object(subdir_name + "/LLE_matrix" + name_extension, LLE_matrix)
    LocallyLinearEmbedding_list.append(LLE_matrix)
    
    manifold_2D_LLE = make_manifold(LLE_matrix, image_matrix) 
    save_object(subdir_name + "/manifold_2D_LLE" + name_extension, manifold_2D_LLE) 
  
    if draw_LocallyLinearEmbedding:
        plot_LocallyLinearEmbedding(manifold_2D_LLE, longs_matrix, lats_matrix, subdir_name + "/plot_LocallyLinearEmbedding" + name_extension + ".png")  
     
    if use_DBSCAN:
        clustering_DBSCAN_LLE = make_cluster(manifold_2D_LLE)
        save_object(subdir_name + "/clustering_DBSCAN_LLE" + name_extension, clustering_DBSCAN_LLE) 
        
    if draw_DBSCAN:
        plot_cluster_LLE(manifold_2D_LLE, clustering_DBSCAN_LLE, subdir_name + "/plot_cluster_LLE" + name_extension + ".png") 

    if use_KMeans:
        clustering_KMeans_LLE = make_cluster(manifold_2D_LLE)
        save_object(subdir_name + "/clustering_KMeans_LLE" + name_extension, clustering_KMeans_LLE) 
        
    if draw_KMeans:
        plot_cluster_LLE(manifold_2D_LLE, clustering_KMeans_LLE, subdir_name + "/plot_cluster_KMeans_LLE" + name_extension + ".png") 

if draw_multi_LocallyLinearEmbedding:
    for index_LocallyLinearEmbedding in range(len(LocallyLinearEmbedding_list)):
        plot_multi_LocallyLinearEmbedding(LocallyLinearEmbedding_list[index_LocallyLinearEmbedding], image_matrix_list, subdir_names[index_LocallyLinearEmbedding] + "/multi_LocallyLinearEmbedding" + name_extension + "_" + subdir_names[index_LocallyLinearEmbedding] + ".png", subdir_names[index_LocallyLinearEmbedding], subdir_names)

multi_manifold_list = dict()
 
if use_multi_DBSCAN or draw_multi_DBSCAN:
    for name1 in subdir_names:
        multi_manifold_list[name1] = [] 
        for name2 in subdir_names:
            multi_manifold_list[name1].append(load_object(name1 + "/multi_LocallyLinearEmbedding" + name_extension + "_" + name1 + "_" + name2)) 
	
if use_multi_DBSCAN:
    for subdir_name in subdir_names:
        clustering_DBSCAN_LLE_multi = make_multi_cluster(multi_manifold_list[subdir_name])
        save_object(subdir_name + "/clustering_DBSCAN_LLE_multi" + name_extension, clustering_DBSCAN_LLE_multi) 

if draw_multi_DBSCAN:
    for subdir_name in subdir_names: 
        clustering_DBSCAN_LLE_multi = load_object(subdir_name + "/clustering_DBSCAN_LLE_multi" + name_extension)
        plot_multi_cluster(multi_manifold_list[subdir_name], clustering_DBSCAN_LLE_multi, subdir_name + "/plot_cluster_LLE_multi" + name_extension + ".png", subdir_names) 

if use_multi_KMeans or draw_multi_KMeans:
    for name1 in subdir_names:
        multi_manifold_list[name1] = [] 
        for name2 in subdir_names:
            multi_manifold_list[name1].append(load_object(name1 + "/multi_LLE" + name_extension + "_" + name1 + "_" + name2)) 
	
if use_multi_KMeans:
    for subdir_name in subdir_names:
        clustering_KMeans_LLE_multi = make_multi_cluster(multi_manifold_list[subdir_name])
        save_object(subdir_name + "/clustering_KMeans_LLE_multi" + name_extension, clustering_KMeans_LLE_multi) 

if draw_multi_KMeans:
    for subdir_name in subdir_names: 
        clustering_KMeans_LLE_multi = load_object(subdir_name + "/clustering_KMeans_LLE_multi" + name_extension)
        plot_multi_cluster(multi_manifold_list[subdir_name], clustering_KMeans_LLE_multi, subdir_name + "/plot_cluster_KMeans_LLE_multi" + name_extension + ".png", subdir_names)  