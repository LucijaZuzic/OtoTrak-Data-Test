from utilities import *
from sklearn.metrics import normalized_mutual_info_score, homogeneity_score
labels_window_size_zero_dict = load_object("labels_window_size_zero_dict")
percents_window_size_zero_dict = load_object("percents_window_size_zero_dict")
labels_window_size_max_dict = load_object("labels_window_size_max_dict")
percents_window_size_max_dict = load_object("percents_window_size_max_dict")

total_probs_zero_mul_dict = load_object("total_probs_zero_mul_dict")
total_probs_zero_sum_dict = load_object("total_probs_zero_sum_dict")
total_probs_max_mul_dict = load_object("total_probs_max_mul_dict")
total_probs_max_sum_dict = load_object("total_probs_max_sum_dict")
 
total_labels_zero_sum_dict = load_object("total_labels_zero_sum_dict") 
total_labels_max_sum_dict = load_object("total_labels_max_sum_dict")

entries_all = {"labels_window_size_zero_dict": labels_window_size_zero_dict,
               "percents_window_size_zero_dict": percents_window_size_zero_dict,
               "labels_window_size_max_dict": labels_window_size_max_dict,
               "percents_window_size_max_dict": percents_window_size_max_dict,
               "total_probs_zero_mul_dict": total_probs_zero_mul_dict,
               "total_probs_zero_sum_dict": total_probs_zero_sum_dict,
               "total_probs_max_mul_dict": total_probs_max_mul_dict,
               "total_probs_max_sum_dict": total_probs_max_sum_dict, 
               "total_labels_zero_sum_dict": total_labels_zero_sum_dict, 
               "total_labels_max_sum_dict": total_labels_max_sum_dict}

def make_list_labels(part1, subdirnames = [], filenames = [], subdirnames_skip = [], filenames_skip = []):
    for subdirname in os.listdir(part1):
        skipping = False
        for s in subdirnames:
            if s not in subdirname:
                skipping = True
                break
        for s in subdirnames_skip:
            if s in subdirname:
                skipping = True
                break
        if skipping:
            continue
        print(part1 + subdirname)
        largest_nmi_all, largest_h_all = (0, ""), (0, "")
        for filename in os.listdir(part1 + subdirname + "/filenames"):
            skipping = False
            for f in filenames:
                if f not in filename:
                    skipping = True
                    break
            for f in filenames_skip:
                if f in filename:
                    skipping = True
                    break
            if skipping:
                continue
            print(part1 + subdirname + "/filenames/" + filename)
            fname = load_object(part1 + subdirname + "/filenames/" + filename)
            largest_nmi, largest_h = (0, ""), (0, "")
            #cluster_test = load_object(part1 + subdirname + "/clus_test/" + filename.replace("filenames_in_cluster_test ", "clus_test_"))
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
                    if h > largest_h_all[0]:
                        largest_h_all = (h, p, filename) 
                    if nmi > largest_nmi_all[0]:
                        largest_nmi_all = (nmi, p, filename)
            print(largest_nmi, largest_h)
        print("TOTAL", largest_nmi_all, largest_h_all)
 
subdirnames = ["all", "poly", "heading", "acceler", "no_xy"]
filenames = ["KMeans", "nclus 8"]
subdirnames_skip = ["flags"]
filenames_skip = ["_train"] 

subdirnames = []
filenames = []
subdirnames_skip = []
filenames_skip = ["_train"] 

part1 = "all_clus/"
part2 = "/output_clus/"
make_list_labels(part1, subdirnames, filenames, subdirnames_skip, filenames_skip)
part1 = "all_isomap/"
part2 = "/output_iso/"
make_list_labels(part1, subdirnames, filenames, subdirnames_skip, filenames_skip)