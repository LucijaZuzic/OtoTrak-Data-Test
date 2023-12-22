from utilities import *  
 
def commitfv(str_extension, ws, vehicle, shortfile, x):     
    retstr = str("all_closest/closest_ids/" + str_extension + "/" + ws + "/" + vehicle + "/" + shortfile + "/" + x + "/closest_ids_" + str_extension+ "_" + ws + "_" + vehicle + "_" + shortfile + "_" + x)
    retstr_dist = retstr.replace("closest_ids", "closest_dist")
    os.system("git add " + retstr)
    os.system("git add " + retstr_dist)
    os.system('git commit -a -m "Closest ' + str_extension + " " + ws + " " + vehicle + " " + shortfile + " " + x + '"')
    os.system("git push")
    return "git add " + retstr + "\ngit add " + retstr_dist + '\ngit commit -a -m "Closest ' + str_extension + " " + ws + " " + vehicle + " " + shortfile + " " + x + '"\ngit push\n'
       
str_pr = ""
for method in os.listdir("all_closest/closest_dist"):
    for ws in os.listdir("all_closest/closest_dist/" + method):
        for veh in os.listdir("all_closest/closest_dist/" + method + "/" + ws):
            for ride in os.listdir("all_closest/closest_dist/" + method + "/" + ws + "/" + veh):
                for x in os.listdir("all_closest/closest_dist/" + method + "/" + ws + "/" + veh + "/" + ride):
                    str_pr += commitfv(method, ws, veh, ride, x)
print(str_pr)
fileopen = open("gitsave.txt", "w")
fileopen.write(str_pr)
fileopen.close()