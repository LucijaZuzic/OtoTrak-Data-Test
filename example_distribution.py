from utilities import *

def get_var(name_of):
    print(name_of)
    predicted = load_object("predicted/predicted_" + name_of)   

    probability_of_in_next_next_step = load_object("probability/probability_of_" + name_of + "_in_next_next_step")   
    probability_of_in_next_step = load_object("probability/probability_of_" + name_of + "_in_next_step")   
    probability_of = load_object("probability/probability_of_" + name_of) 
  
    print(len(probability_of_in_next_next_step))
    print(len(probability_of_in_next_step))
    print(len(probability_of)) 

    if "sgn" in name_of:
        for curr in probability_of:
            print(curr, str(np.round(probability_of[curr] * 100, 2)))
                 
        for prev in probability_of_in_next_step:
            strpr = str(prev) + " "
            for curr in probability_of_in_next_step:
                if curr in probability_of_in_next_step[prev]:
                    strpr += str(np.round(probability_of_in_next_step[prev][curr] * 100, 2)) + " "
                else:
                    strpr += str(np.round(probability_of_in_next_step[prev]["undefined"] * 100, 2)) + " "
            print(strpr)
            
        for prevprev in probability_of_in_next_next_step:
            print(prevprev)
            for prev in probability_of_in_next_next_step[prevprev]:
                strpr = str(prev) + " "
                for curr in probability_of_in_next_next_step[prevprev]:
                    if curr in probability_of_in_next_next_step[prevprev][prev]:
                        strpr += str(np.round(probability_of_in_next_next_step[prevprev][prev][curr] * 100, 2)) + " "
                    else:
                        strpr += str(np.round(probability_of_in_next_next_step[prevprev][prev]["undefined"] * 100, 2)) + " "
                print(strpr)

name_of_var = os.listdir("predicted")
for v in name_of_var: 
    if v == "predicted_time_half":
        continue
    if v == "predicted_time_ten":
        continue
    get_var(v.replace("predicted_", ""))