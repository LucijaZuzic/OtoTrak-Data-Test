from utilities import * 

def save_table(str_save, name_save):
    if not os.path.isdir("distribution"):
        os.makedirs("distribution")
    file_w = open("distribution/" + name_save + ".txt", "w")
    file_w.write(str_save)
    file_w.close()

def str_convert(val):
    if val == False:
        return "0"
    if val == True:
        return "1" 
    power_to = 0
    while abs(val) < 1 and val != 0.0:
        val *= 10
        power_to += 1 
    return_val = str(np.round(val, 2))
    if power_to == 1:
        return_val = str(np.round(val / 10, 2))
    if return_val[-2:] == '.0':
        return_val = return_val[:-2]
    if power_to > 1:
        if return_val != "1": 
            return_val += " \\times 10^{-" + str(power_to) + "}"
        else:
            return_val = "10^{-" + str(power_to) + "}"
    return return_val

def header_dict(dictio):
    str_pr = ""
    for k in dictio:
        str_pr += "$" + str(k) + "$ & "
    str_pr = str_pr[:-3]
    str_pr += "\\\\ \\hline\n"
    return str_pr
 
def print_1d(dictio, mul, name_save):
    str_pr = "\\begin{tabular}{|" + "c|" * len(dictio) + "}\n\\hline\n"
    str_pr += header_dict(dictio)
    for k in dictio:
        str_pr += "$" + str(np.round(dictio[k] * mul, 2)) + "\%$ & "
    str_pr = str_pr[:-3]
    str_pr += "\\\\ \\hline\n\\end{tabular}\n"
    save_table(str_pr, name_save)
    return str_pr

def print_2d(dictio, mul, name_save = ""):
    str_pr = "\\begin{tabular}{|" + "c|" * (len(dictio) + 1) + "}\n\\hline\n"
    str_pr += " & " + header_dict(dictio)
    for prev in dictio:
        if sum(list(dictio[prev].values())) > 0:
            str_pr += "$" + str(prev) + "$ & "
            for k in dictio:
                if k in dictio[prev]:
                    str_pr += "$" + str(np.round(dictio[prev][k] * mul, 2)) + "\\%$ & "
                else:
                    str_pr += "$" + str(np.round(0, 2)) + "\\%$ & "
            str_pr = str_pr[:-3]
            str_pr += "\\\\ \\hline\n"
    str_pr += "\\end{tabular}\n"
    if not name_save == "":
        save_table(str_pr, name_save)
    return str_pr

def print_3d(dictio, mul, name_save): 
    str_pr = ""
    for prev in dictio:
        if len(dictio[prev]) > 0:
            part1 = print_2d(dictio[prev], mul)
            part2 = "\\multicolumn{" + str(len(dictio) + 1) + "}{|c|}{$" + str(prev) + "$}\\\\ \\hline\n"
            part1 = part1.replace("}\n\\hline\n", "}\n\\hline\n" + part2)
            str_pr += part1
    save_table(str_pr, name_save)
    return str_pr

def convert_keys(new_bins, maxval, i):
        new_min = new_bins[i]
        new_max = maxval
        if i + 1 < len(new_bins):
            new_max = new_bins[i + 1]
        new_key = "[" + str_convert(new_min) + ", " + str_convert(new_max)
        if i + 1 < len(new_bins):
            new_key += ">"
        else:
            new_key += "]"
        return new_min, new_max, new_key

def summarize_dict(old_dict, new_bins, maxval): 
    new_dict = dict()
    for i in range(len(new_bins)): 
        new_min, new_max, new_key = convert_keys(new_bins, maxval, i)
        new_dict[new_key] = 0
        for k in old_dict:
            if k == "undefined":
                continue
            if k >= new_min and k < new_max:
                new_dict[new_key] += old_dict[k]
    for k in new_dict:   
        new_dict[k] = np.round(new_dict[k] * 100, 2)  
    return new_dict

def summarize_2d_dict(old_dict, new_bins, maxval): 
    new_1d_fixed = dict()
    for k in old_dict:
        new_1d_fixed[k] = summarize_dict(old_dict[k], new_bins, maxval)  
    new_dict = dict()
    num_in_old_dict = dict()
    for i in range(len(new_bins)):
        new_min, new_max, new_key = convert_keys(new_bins, maxval, i)
        new_dict[new_key] = dict()
        num_in_old_dict[new_key] = 0 
        for k in old_dict:
            if k == "undefined":
                continue 
            if k >= new_min and k < new_max:
                num_in_old_dict[new_key] += 1  
                for new_key2 in new_1d_fixed[k]:
                    if new_key2 not in new_dict[new_key]:
                        new_dict[new_key][new_key2] = 0 
                    new_dict[new_key][new_key2] += new_1d_fixed[k][new_key2]  
    for k in new_dict:
        for k2 in new_dict[k]:
            new_dict[k][k2] /= num_in_old_dict[k]    
            new_dict[k][k2] = np.round(new_dict[k][k2], 2)  
    return new_dict

def summarize_3d_dict(old_dict, new_bins, maxval): 
    new_2d_fixed = dict()
    for k in old_dict:
        new_2d_fixed[k] = summarize_2d_dict(old_dict[k], new_bins, maxval)  
    new_dict = dict()
    for i in range(len(new_bins)):
        new_min, new_max, new_key = convert_keys(new_bins, maxval, i)
        new_dict[new_key] = dict() 
        for k in old_dict:
            if k == "undefined":
                continue 
            if k >= new_min and k < new_max:
                for new_key2 in new_2d_fixed[k]:
                    if new_key2 not in new_dict[new_key]:
                        new_dict[new_key][new_key2] = dict() 
                        for new_key3 in new_2d_fixed[k][new_key2]:
                            if new_key3 not in new_dict[new_key][new_key2]:
                                new_dict[new_key][new_key2][new_key3] = 0 
                            new_dict[new_key][new_key2][new_key3] += new_2d_fixed[k][new_key2][new_key3]
    for k in new_dict:
        for k2 in new_dict[k]:
            for k3 in new_dict[k][k2]:  
                new_dict[k][k2][k3] = np.round(new_dict[k][k2][k3], 2)  
    return new_dict

def get_bins(keys_list, num_bins): 
    if max(keys_list) == 359:
        return np.arange(0, 360, 360 / (num_bins))
    print(min(keys_list), max(keys_list), (max(keys_list) - min(keys_list)) / (num_bins))
    return np.arange(min(keys_list), max(keys_list), (max(keys_list) - min(keys_list)) / (num_bins))
    
def get_var(name_of):
    print(name_of)
    #predicted = load_object("predicted/predicted_" + name_of)   

    probability_of_in_next_next_step = load_object("probability/probability_of_" + name_of + "_in_next_next_step")   
    probability_of_in_next_step = load_object("probability/probability_of_" + name_of + "_in_next_step")   
    probability_of = load_object("probability/probability_of_" + name_of) 
  
    print(len(probability_of_in_next_next_step))
    print(len(probability_of_in_next_step))
    print(len(probability_of)) 

    keys_list = list(probability_of.keys())
    if "undefined" in keys_list:
        keys_list.remove("undefined") 
    keys_list = sorted(keys_list) 
    nbins = 6
    mul = 1
    if "sgn" in name_of: 
        n1 = probability_of
        n2 = probability_of_in_next_step
        n3 = probability_of_in_next_next_step
        mul = 100
    else:
        n1 = summarize_dict(probability_of, get_bins(keys_list, nbins), max(keys_list))
        n2 = summarize_2d_dict(probability_of_in_next_step, get_bins(keys_list, nbins), max(keys_list))
        n3 = summarize_3d_dict(probability_of_in_next_next_step, get_bins(keys_list, nbins), max(keys_list))
    
    p1 = print_1d(n1, mul, name_of + "_1d")
    p2 = print_2d(n2, mul, name_of + "_2d")
    p3 = print_3d(n3, mul, name_of + "_3d")
    save_table(p1 + p2 + p3, name_of + "_all")
    print(p1)
    print(p2)
    print(p3)

name_of_var = os.listdir("predicted")
for v in name_of_var: 
    if v == "predicted_time_half":
        continue
    if v == "predicted_time_ten":
        continue
    get_var(v.replace("predicted_", ""))