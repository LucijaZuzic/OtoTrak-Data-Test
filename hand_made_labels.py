from utilities import *
from sklearn.metrics import normalized_mutual_info_score, homogeneity_score
from numpy.linalg import solve
all_subdirs = os.listdir()
MIN_VAL_SPEED = 0
MAX_VAL_SPEED = 85 
MIN_VAL_ANGLE = 0
MAX_VAL_ANGLE = 180 
labels_by_hand = {
    2: [('s', 27, 1)],
    3: [('a', 22, 2), ('s', 27, 1)],
    4: [('a', 23, 3), ('s', 40, 0), ('s', 19, 2)], 
    5: [('a', 42, 2), ('s', 41, 1), ('a', 13, 3), ('s', 19, 4)],
    6: [('a', 47, 4), ('s', 47, 2), ('s', 30, 1), ('a', 14, 0), ('s', 15, 5)],
    7: [('a', 54, 4), ('s', 47, 3), ('a', 20, 5), ('s', 30, 0), ('s', 15, 6), ('a', 9, 2)],
    8: [('a', 70, 6), ('a', 31, 4), ('sa', [16, 9], 7), ('a', 9, 0), ('s', 47, 2), ('s', 30, 3), ('s', 15, 1)],
    9: [('a', 70, 3), ('a', 31, 4), ('sa', [15, 9], 6), ('a', 9, 5), ('s', 52, 7), ('s', 37, 1), ('s', 25, 8), ('s', 12, 0)],
    10: [('a', 70, 1), ('a', 31, 5), ('sa', [15, 9], 6), ('a', 9, 0), ('s', 54, 8), ('s', 41, 2), ('s', 30, 7), ('s', 20, 4), ('s', 11, 3)],
    11: [('a', 81, 7), ('a', 41, 3), ('sa', [17, 8], 6), ('a', 21, 10), ('a', 8, 0), ('s', 54, 4), ('s', 41, 8), ('s', 30, 1), ('s', 20, 5), ('s', 11, 9)],
    12: [('a', 82, 6), ('a', 42, 11), ('sa', [23, 7], 1), ('a', 22, 2), ('sa', [12, 7], 10), ('a', 7, 3), ('s', 54, 8), ('s', 42, 5), ('s', 31, 4), ('s', 20, 9), ('s', 11, 0)],
    13: [('a', 88, 7), ('a', 45, 2), ('sa', [9, 20], 12), ('a', 20, 5), ('sa', [28, 6], 10), ('sa', [11, 6], 4), ('a', 6, 9), ('s', 54, 3), ('s', 42, 6), ('s', 31, 1), ('s', 20, 8), ('s', 11, 11)],
    14: [('a', 88, 13), ('a', 46, 2), ('sa', [11, 22], 10), ('a', 22, 6), ('sa', [28, 8], 3), ('sa', [11, 8], 12), ('a', 8, 4), ('s', 56, 7), ('s', 45, 11), ('s', 35, 1), ('s', 25, 5), ('s', 16, 9), ('s', 9, 0)],
    15: [('a', 96, 14), ('a', 57, 10), ('a', 33, 2), ('sa', [15, 17], 7), ('a', 17, 8), ('sa', [29, 7], 12), ('sa', [12, 7], 5), ('a', 7, 4), ('s', 56, 3), ('s', 44, 11), ('s', 34, 1), ('s', 25, 6), ('s', 16, 0), ('s', 9, 13)],
}

def plot_limits(number_label):
    print(number_label)
    xy_range_label = dict()  
    free_space = [[[MIN_VAL_SPEED, MAX_VAL_SPEED], [MIN_VAL_ANGLE, MAX_VAL_ANGLE]]]
    for limit in labels_by_hand[number_label]:
        if limit[0] == 's': 
            xy_range_label[limit[2]] = []
            for i, fs in enumerate(free_space):
                if fs[0][1] > limit[1]:
                    new_fs = [[p[0], p[1]] for p in fs]
                    new_fs[0][0] = limit[1]
                    xy_range_label[limit[2]].append(new_fs)
                    free_space[i][0][1] = limit[1]
        if limit[0] == 'a': 
            xy_range_label[limit[2]] = []
            for i, fs in enumerate(free_space):
                if fs[1][1] > limit[1]:
                    new_fs = [[p[0], p[1]] for p in fs]
                    new_fs[1][0] = limit[1]
                    xy_range_label[limit[2]].append(new_fs)
                    free_space[i][1][1] = limit[1]
        if limit[0] == 'sa': 
            xy_range_label[limit[2]] = []
            to_add = []
            for i, fs in enumerate(free_space):
                if fs[0][1] > limit[1][0] and fs[1][1] > limit[1][1]:
                    new_fs = [[p[0], p[1]] for p in fs]
                    new_fs[0][0] = limit[1][0]
                    new_fs[1][0] = limit[1][1]
                    xy_range_label[limit[2]].append(new_fs) 
                    fs2 = [[p[0], p[1]] for p in fs]
                    free_space[i][0][1] = limit[1][0]
                    fs2[0][0] = limit[1][0]
                    fs2[1][1] = limit[1][1]
                    to_add.append(fs2)
            for t in to_add:
                free_space.append(t) 
        for i, t1 in enumerate(free_space):
            for t2 in free_space[i + 1:]: 
                if t1[0] == t2[0] and (t1[1][0] == t2[1][1] or t1[1][1] == t2[1][0]):
                    t1[1] = [min(t1[1][0], t2[1][0]), max(t1[1][1], t2[1][1])]
                    t2[1] = t1[1] 
                if t1[1] == t2[1] and (t1[0][0] == t2[0][1] or t1[0][1] == t2[0][0]):
                    t1[0] = [min(t1[0][0], t2[0][0]), max(t1[0][1], t2[0][1])]
                    t2[0] = t1[0] 
        to_remove = set()
        for i, t1 in enumerate(free_space):
            for t2 in free_space[i + 1:]:
                if t1 == t2:
                    to_remove.add(i)  
        new_free = []
        for i, t1 in enumerate(free_space):
            if i not in to_remove:
                new_free.append(t1)
        free_space = new_free 
    for limit in range(number_label):
        if limit not in xy_range_label:
            xy_range_label[
                limit] = free_space
    plt.title(number_label)
    rcs = random_colors(number_label + 2)
    yx_range_label = dict()
    for limit in xy_range_label:
        yx_range_label[limit] = [[xy_range_label[limit][0][1][1], xy_range_label[limit][0][0][1]], [xy_range_label[limit][0][1][0], xy_range_label[limit][0][0][0]]]
    for limit in dict(sorted(yx_range_label.items(), key=lambda item: item[1])):
        minx, maxx = xy_range_label[limit][0][0]
        miny, maxy = xy_range_label[limit][0][1]
        xrange = range(minx, maxx + 1)  
        plt.fill_between(xrange, [miny for x in xrange], [maxy for x in xrange], label = limit, color = rcs[limit])
    num_points = 1000
    x_vals = np.arange(MIN_VAL_SPEED, MAX_VAL_SPEED + 1, (MAX_VAL_SPEED - MIN_VAL_SPEED) / num_points)
    #y_vals1 = np.arange(MAX_VAL_ANGLE, MIN_VAL_ANGLE, - (MAX_VAL_ANGLE - MIN_VAL_ANGLE) / num_points)
    #plt.plot(x_vals, y_vals1, color = rcs[number_label])
    point_on_line = (41, 45)
    A = np.array([[MAX_VAL_SPEED ** 2, MAX_VAL_SPEED, 1], [point_on_line[0] ** 2, point_on_line[0], 1], [MIN_VAL_SPEED ** 2, MIN_VAL_SPEED, 1]])
    b = np.array([MIN_VAL_ANGLE, point_on_line[1], MAX_VAL_ANGLE])
    solution = solve(A, b)
    y_vals2 = [solution[0] * (x ** 2) + solution[1] * x + solution[2] for x in x_vals]
    #plt.plot(x_vals, y_vals2, color = rcs[number_label + 1])
    plt.fill_between(x_vals, y_vals2, [MAX_VAL_ANGLE + 1 for x in x_vals], color = "w")
    plt.legend()
    if not os.path.isdir("all_location_clus/interpret/"):
        os.makedirs("all_location_clus/interpret/")
    plt.savefig("all_location_clus/interpret/all_labels_" + str(number_label) + ".png", bbox_inches = "tight")
    plt.close()

for l in labels_by_hand:
    plot_limits(l)
     
def assign_label(number_label, files_in_cluster):
    print(filename) 
    all_labels = dict()
    num_different_hand_label = dict()
    num_total_dict_hand_label = dict()
    for i in range(number_label):
        num_different_hand_label[i] = 0
        num_total_dict_hand_label[i] = 0
    points_from_traj_labels = dict()
    num_different = dict()
    num_total_dict = dict()
    num_total = 0
    for cluster in files_in_cluster: 
        num_different[cluster] = 0
        num_total_dict[cluster] = 0
        for entry in files_in_cluster[cluster]:
            name_file = entry["short_name"]
            name_file_long = name_file.replace("/", "/cleaned_csv/") 
            pos = entry["start"]
            if name_file_long not in points_from_traj_labels:
                points_from_traj_labels[name_file_long] = dict()
            points_from_traj_labels[name_file_long][pos] = cluster
    label_list_cluster = []
    label_list_hand = []
    for subdir_name in all_subdirs:
        if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
            continue 
        all_labels[subdir_name] = dict()
        all_files = os.listdir(subdir_name + "/cleaned_csv/") 
        bad_rides_filenames = dict()
        if os.path.isfile(subdir_name + "/bad_rides_filenames"):
            bad_rides_filenames = load_object(subdir_name + "/bad_rides_filenames")
        gap_rides_filenames = dict()
        if os.path.isfile(subdir_name + "/gap_rides_filenames"):
            gap_rides_filenames = load_object(subdir_name + "/gap_rides_filenames")
        train_rides = set()
        if os.path.isfile(subdir_name + "/train_rides"):
            train_rides = load_object(subdir_name + "/train_rides") 
            
        test_rides = set()
        if os.path.isfile(subdir_name + "/test_rides"):
            test_rides = load_object(subdir_name + "/test_rides")

        for some_file in all_files:  
            if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames:
                #print("Skipped ride", some_file)
                continue
            if some_file in train_rides and "_test" in filename:
                continue
            if some_file in test_rides and "_train" in filename:
                continue 
            all_labels[subdir_name][some_file] = dict()
            file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)  
            speeds_tmp = list(file_with_ride["fields_speed"])  
            headings = list(file_with_ride["fields_direction"])    
            angles = return_angle_diffs(headings)   
            name_longer = subdir_name + "/cleaned_csv/" + some_file  

            set_unlabeled = set([i for i in range(len(angles))])
            set_labeled = dict()
            for possible_label in range(number_label):
                set_labeled[possible_label] = set()
            empty_labels = set([x for x in range(number_label)])
            for rule in labels_by_hand[number_label]:
                set_to_label = set()
                for unlabeled in set_unlabeled:
                    if rule[0] == "s":
                        if speeds_tmp[unlabeled] >= rule[1]:
                            set_to_label.add(unlabeled)
                    if rule[0] == "a":
                        if angles[unlabeled] >= rule[1]:
                            set_to_label.add(unlabeled)
                    if rule[0] == "sa":
                        if speeds_tmp[unlabeled] >= rule[1][0] and angles[unlabeled] >= rule[1][1]:
                            set_to_label.add(unlabeled)
                set_labeled[rule[2]] = set([x for x in set_to_label])
                set_unlabeled = set_unlabeled.difference(set_to_label)
                empty_labels.remove(rule[2])
                #print(rule[2], len(set_labeled[rule[2]]))
            set_labeled[list(empty_labels)[0]] = set([x for x in set_unlabeled])
            #print(list(empty_labels)[0], len(set_labeled[list(empty_labels)[0]]))
            for label_some in set_labeled:
                for ind in set_labeled[label_some]:
                    actual_label = points_from_traj_labels[name_longer][ind]
                    if actual_label != label_some:
                        num_different[actual_label] += 1
                        num_different_hand_label[label_some] += 1
                    num_total_dict[actual_label] += 1
                    num_total_dict_hand_label[label_some] += 1
                    num_total += 1
                    all_labels[subdir_name][some_file][ind] = label_some
                    label_list_cluster.append(actual_label)
                    label_list_hand.append(label_some) 
    new_different = dict()
    for l in num_different:
        new_different[l] =  num_different[l] / num_total_dict[l]
    new_different_hand_label = dict()
    for l in num_different_hand_label:
        new_different_hand_label[l] =  num_different_hand_label[l] / num_total_dict_hand_label[l]
    nmi = normalized_mutual_info_score(label_list_hand, label_list_cluster)
    h = homogeneity_score(label_list_hand, label_list_cluster)
    print(nmi, h)
    print(dict(sorted(new_different.items(), key = lambda item: item[1], reverse = True)))
    print(dict(sorted(new_different_hand_label.items(), key = lambda item: item[1], reverse = True)))
    return all_labels
                 
for filename in os.listdir("all_location_clus/filenames/"):
    number_label = int(filename.split(" ")[-1])
    all_labels = assign_label(number_label, load_object("all_location_clus/filenames/" + filename))
    if not os.path.isdir("all_location_clus/hand_made_labels/"):
        os.makedirs("all_location_clus/hand_made_labels/")
    save_object("all_location_clus/hand_made_labels/all_labels_" + filename, all_labels)

def limit_of_location_cluster(files_in_cluster, filename):
    print(filename)  
    
    points_from_traj_labels = dict()
    minx = dict()
    miny = dict()
    maxx = dict()
    maxy = dict()
 
    for cluster in files_in_cluster:
        minx[cluster] = MAX_VAL_SPEED
        miny[cluster] = MAX_VAL_SPEED
        maxx[cluster] = MIN_VAL_ANGLE
        maxy[cluster] = MAX_VAL_ANGLE
        for entry in files_in_cluster[cluster]:
            name_file = entry["short_name"]
            name_file_long = name_file.replace("/", "/cleaned_csv/") 
            pos = entry["start"]
            if name_file_long not in points_from_traj_labels:
                points_from_traj_labels[name_file_long] = dict()
            points_from_traj_labels[name_file_long][pos] = cluster 
            
    for subdir_name in all_subdirs:
        if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
            continue 
        
        all_files = os.listdir(subdir_name + "/cleaned_csv/") 
        bad_rides_filenames = dict()
        if os.path.isfile(subdir_name + "/bad_rides_filenames"):
            bad_rides_filenames = load_object(subdir_name + "/bad_rides_filenames")
        gap_rides_filenames = dict()
        if os.path.isfile(subdir_name + "/gap_rides_filenames"):
            gap_rides_filenames = load_object(subdir_name + "/gap_rides_filenames")
        train_rides = set()
        if os.path.isfile(subdir_name + "/train_rides"):
            train_rides = load_object(subdir_name + "/train_rides") 
            
        test_rides = set()
        if os.path.isfile(subdir_name + "/test_rides"):
            test_rides = load_object(subdir_name + "/test_rides")

        for some_file in all_files:  
            if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames:
                #print("Skipped ride", some_file)
                continue
            if some_file in train_rides and "_test" in filename:
                continue
            if some_file in test_rides and "_train" in filename:
                continue
    
            file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)  
            speeds_tmp = list(file_with_ride["fields_speed"])  
            headings = list(file_with_ride["fields_direction"])    
            angles = return_angle_diffs(headings)   
            name_longer = subdir_name + "/cleaned_csv/" + some_file  
            for i in range(len(angles)):
                if name_longer in points_from_traj_labels and i in points_from_traj_labels[name_longer]: 
                    class_label = points_from_traj_labels[name_longer][i]
                    xval = speeds_tmp[i]
                    yval = angles[i]
                    if xval < minx[class_label]:
                        minx[class_label] = xval
                    if xval > maxx[class_label]:
                        maxx[class_label] = xval
                    if yval < miny[class_label]:
                        miny[class_label] = yval
                    if yval > maxy[class_label]:
                        maxy[class_label] = yval

    for cluster in files_in_cluster:
        print(cluster, minx[cluster], maxx[cluster], miny[cluster], maxy[cluster])
         
for filename in os.listdir("all_location_clus/filenames/"): 
    if "nclus 15" not in filename:
        continue
    limit_of_location_cluster(load_object("all_location_clus/filenames/" + filename), filename)