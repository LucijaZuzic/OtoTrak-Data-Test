from utilities import *
from sklearn.metrics import normalized_mutual_info_score, homogeneity_score
labels_window_size_zero_dict = load_object("labels_window_size_zero_dict")
percents_window_size_zero_dict = load_object("percents_window_size_zero_dict")
labels_window_size_max_dict = load_object("labels_window_size_max_dict")
percents_window_size_max_dict = load_object("percents_window_size_max_dict") 
entries_all = {"labels_window_size_zero_dict": labels_window_size_zero_dict,
               "percents_window_size_zero_dict": percents_window_size_zero_dict,
               "labels_window_size_max_dict": labels_window_size_max_dict,
               "percents_window_size_max_dict": percents_window_size_max_dict}

for subdirname in os.listdir("all_isomap/"):
    print("all_isomap/" + subdirname)
    largest_h = (0, "")
    largest_nmi = (0, "")
    for filename in os.listdir("all_isomap/" + subdirname + "/filenames"): 
        if not "test nclus " in filename:
            continue
        if not "_test" in filename:
            continue 
        fname = load_object("all_isomap/" + subdirname + "/filenames/" + filename)
        cluster_test = load_object("all_isomap/" + subdirname + "/clus_test/" + filename.replace("filenames_in_cluster_test ", "clus_test_"))
        labels_true = dict()
        labels_new = []
        for cluster in fname:
            for index in range(len(fname[cluster])):
                name_file = fname[cluster][index]["short_name"]
                name_file_long = name_file.replace("/", "/cleaned_csv/")  
                wnd = fname[cluster][index]["window"] 
                pos = fname[cluster][index]["start"]
                labels_new.append(cluster)
                for entry in entries_all:
                    if entry not in labels_true:
                        labels_true[entry] = dict()
                    for prop in entries_all[entry][wnd][name_file_long.split("/")[0]][name_file_long.split("/")[-1]][pos]:
                        if prop not in labels_true[entry]:
                            labels_true[entry][prop] = []
                        labels_true[entry][prop].append(float(entries_all[entry][wnd][name_file_long.split("/")[0]][name_file_long.split("/")[-1]][pos][prop]))
        
        labels_new.append(0)
        labels_new.append(1)
        for e in labels_true:
            for p in labels_true[e]:
                labels_true[e][p].append(1)
                labels_true[e][p].append(0)
        for e in labels_true:
            for p in labels_true[e]:
                nmi = normalized_mutual_info_score(labels_true[e][p], labels_new)
                h = homogeneity_score(labels_true[e][p], labels_new)
                if h > largest_h[0]:
                    largest_h = (h, p, filename) 
                if nmi > largest_nmi[0]:
                    largest_nmi = (nmi, p, filename)
    print(largest_nmi, largest_h)
 