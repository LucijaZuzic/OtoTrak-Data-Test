import os
for name_dir in ["all_probs_zero", "all_probs_max", "all_probs_zero_max"]:
    if not os.path.isdir(name_dir):
        continue
    if ".git" in name_dir:
        continue
    for subdirname in os.listdir(name_dir):
        if not os.path.isdir(name_dir + "/" + subdirname):
            continue
        for subdir2 in os.listdir(name_dir + "/" + subdirname):  
            if not os.path.isdir(name_dir + "/" + subdirname + "/" + subdir2):
                continue 
            for filename in os.listdir(name_dir + "/" + subdirname + "/" + subdir2): 
                if ".csv" not in filename: 
                    oldname = name_dir + "/" + subdirname + "/" + subdir2 + "/" + filename
                    newname = name_dir + "/" + subdirname + "/" + subdir2 + "/" + filename + ".csv"
                    print(oldname, newname)
                    os.rename(oldname, newname) 