from utilities import *
from scipy.stats import spearmanr

feat_array = load_object("feat_array")
feat_names = load_object("feat_names")
dict_corrcoef = dict()
dict_spearman = dict()
for feat1 in feat_names: 
    dict_corrcoef[feat1] = dict()
    dict_spearman[feat1] = dict()
    for feat2 in feat_names:
        if feat1 == feat2:
            continue
        dict_corrcoef[feat1][feat2] = abs(np.corrcoef(feat_array[feat1], feat_array[feat2])[0][1])
        dict_spearman[feat1][feat2] = abs(spearmanr(feat_array[feat1], feat_array[feat2]).statistic)

set_feats = dict()
set_feats_overlap = dict()
for feat1 in feat_names:
    set_feats[feat1] = set()
    set_feats[feat1].add(feat1)
    set_feats_overlap[feat1] = set()
    set_feats_overlap[feat1].add(feat1)

for feat1 in feat_names:
    for feat2 in dict_corrcoef[feat1]:
        if dict_corrcoef[feat1][feat2] > 0.5 or dict_spearman[feat1][feat2] > 0.5:
            set_feats[feat1].add(feat2)
            set_feats[feat2].add(feat1)
            set_feats_overlap[feat1].add(feat2)
            set_feats_overlap[feat2].add(feat1)

for feat1 in feat_names:
    changed = True
    while changed:
        old_len = len(set_feats_overlap[feat1])
        changed = False
        for feat2 in set_feats_overlap[feat1]: 
            set_feats_overlap[feat1] = set_feats_overlap[feat1].union(set_feats_overlap[feat2])
            set_feats_overlap[feat2] = set_feats_overlap[feat1]
        changed = old_len != len(set_feats_overlap[feat1])

seen = set()
for feat1 in feat_names:
    if feat1 in seen:
        continue
    print(feat1, len(set_feats_overlap[feat1]) / len(feat_names))
    seen = seen.union(set_feats_overlap[feat1])
#print("PEARSON")
#for feat1 in feat_names:
    #set_correlated = [dict_corrcoef[feat1][feat2] > 0.5 or dict_spearman[feat1][feat2] > 0.5 for feat2 in dict_corrcoef[feat1]]
    #print(feat1, sum(set_correlated) / len(set_correlated))
    #set_correlated = [dict_corrcoef[feat1][feat2] > 0.5 for feat2 in dict_corrcoef[feat1]]
    #print(feat1, sum(set_correlated) / len(set_correlated))
    #for feat2 in dict(sorted(dict_corrcoef[feat1].items(), key = lambda item: item[1], reverse = True)):
        #print(feat1, feat2, dict_corrcoef[feat1][feat2])
        #break

#print("SPEARMAN")
#for feat1 in feat_names:
    #set_correlated = [dict_corrcoef[feat1][feat2] > 0.5 for feat2 in dict_spearman[feat1]]
    #print(feat1, sum(set_correlated) / len(set_correlated))
    #for feat2 in dict(sorted(dict_spearman[feat1].items(), key = lambda item: item[1], reverse = True)):
        #print(feat1, feat2, dict_spearman[feat1][feat2])
        #break

dict_for_clustering = load_object("dict_for_clustering")

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

feats_dict = dict()
entries_dict = dict()  

for window_size in dict_for_clustering:
    if window_size not in labels_window_size_zero_dict:
        continue
    for subdir_name in dict_for_clustering[window_size]:
        if subdir_name not in labels_window_size_zero_dict[window_size]:
            continue
        for some_file in dict_for_clustering[window_size][subdir_name]:
            if some_file not in labels_window_size_zero_dict[window_size][subdir_name]:
                continue
            for x in dict_for_clustering[window_size][subdir_name][some_file]:
                if x not in labels_window_size_zero_dict[window_size][subdir_name][some_file]:
                    continue
                for feat in dict_for_clustering[window_size][subdir_name][some_file][x]:
                    if "same" in feat:
                        continue
                    if feat not in feats_dict:
                        feats_dict[feat] = []
                    feats_dict[feat] = add_key(feat, dict_for_clustering[window_size][subdir_name][some_file][x][feat], feats_dict[feat])

for e in entries_all:
    ed = entries_all[e]
    entries_dict[e] = dict()
    for window_size in dict_for_clustering:
        if window_size not in ed:
            continue
        for subdir_name in dict_for_clustering[window_size]:
            if subdir_name not in ed[window_size]:
                continue
            for some_file in dict_for_clustering[window_size][subdir_name]:
                if some_file not in ed[window_size][subdir_name]:
                    continue
                for x in dict_for_clustering[window_size][subdir_name][some_file]:
                    if x not in ed[window_size][subdir_name][some_file]:
                        continue
                    for entry in ed[window_size][subdir_name][some_file][x]:
                        if entry not in entries_dict[e]:
                            entries_dict[e][entry] = []
                        entries_dict[e][entry].append(ed[window_size][subdir_name][some_file][x][entry])

for e in entries_all:
    print(e)
    dict_corrcoef = dict()
    dict_spearman = dict()
    for feat1 in feats_dict: 
        dict_corrcoef[feat1] = dict()
        dict_spearman[feat1] = dict()
        for feat2 in entries_dict[e]:
            if feat1 == feat2:
                continue 
            dict_corrcoef[feat1][feat2] = abs(np.corrcoef(feats_dict[feat1], entries_dict[e][feat2])[0][1])
            dict_spearman[feat1][feat2] = abs(spearmanr(feats_dict[feat1], entries_dict[e][feat2]).statistic)
    
    #print("PEARSON")
    #for feat1 in feats_dict: 
        #for feat2 in dict(sorted(dict_corrcoef[feat1].items(), key = lambda item: item[1], reverse = True)):
            #if dict_corrcoef[feat1][feat2] > 0.5:  
                #print(feat1, feat2, dict_corrcoef[feat1][feat2])
            #break 
    
    #print("SPEARMAN")
    #for feat1 in feats_dict: 
        #for feat2 in dict(sorted(dict_spearman[feat1].items(), key = lambda item: item[1], reverse = True)): 
            #if dict_spearman[feat1][feat2] > 0.5:  
                #print(feat1, feat2, dict_spearman[feat1][feat2])
            #break 

    set_feats = dict()
    set_feats_overlap = dict()
    similar_to = dict()
    for feat1 in feats_dict:
        set_feats[feat1] = set() 
        set_feats_overlap[feat1] = set() 
        similar_to[feat1] = set()
        similar_to[feat1].add(feat1)

    for feat1 in feats_dict:
        for feat2 in entries_dict[e]:
            if dict_corrcoef[feat1][feat2] > 0.5 or dict_spearman[feat1][feat2] > 0.5:
                set_feats[feat1].add(feat2) 
                set_feats_overlap[feat1].add(feat2)

    for feat1 in feats_dict:
        changed = True 
        while changed:
            old_len = len(set_feats_overlap[feat1])
            changed = False
            for feat2 in feats_dict: 
                if len(set_feats_overlap[feat1].intersection(set_feats_overlap[feat2])) > 0:
                    similar_to[feat1].add(feat2)
                    similar_to[feat2].add(feat1)
                    set_feats_overlap[feat1] = set_feats_overlap[feat1].union(set_feats_overlap[feat2])
                    set_feats_overlap[feat2] = set_feats_overlap[feat1]
            changed = old_len != len(set_feats_overlap[feat1])

    seen = set()
    for feat1 in feats_dict:
        if feat1 in seen:
            continue
        if len(set_feats_overlap[feat1]) == 0:
            continue
        print(feat1, len(similar_to[feat1]) / len(feats_dict), len(set_feats_overlap[feat1]) / len(entries_dict[e]))
        print(similar_to[feat1])
        print(set_feats_overlap[feat1])
        seen = seen.union(similar_to[feat1])

    for feat1 in feats_dict:
        for feat2 in set_feats[feat1]:
            if "speed_labels_max" == feat2:
                print(feat2, "TO", feat1)
                break
            if "speed_labels_zero" == feat2:
                print(feat2, "TO", feat1)
                break
            if "speed_probs_max" == feat2:
                print(feat2, "TO", feat1)
                break
            if "speed_probs_zero" == feat2:
                print(feat2, "TO", feat1)
                break

    for feat1 in feats_dict:
        for feat2 in set_feats[feat1]:
            if "speed_alternative_labels_max" == feat2:
                print(feat2, "TO", feat1)
                break
            if "speed_alternative_labels_zero" == feat2:
                print(feat2, "TO", feat1)
                break
            if "speed_alternative_probs_max" == feat2:
                print(feat2, "TO", feat1)
                break
            if "speed_alternative_probs_zero" == feat2:
                print(feat2, "TO", feat1)
                break