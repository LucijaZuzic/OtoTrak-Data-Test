import os
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def save_object(file_name, std1):       
    with open(file_name, 'wb') as file_object:
        pickle.dump(std1, file_object) 
        file_object.close()

def load_object(file_name): 
    with open(file_name, 'rb') as file_object:
        data = pickle.load(file_object) 
        file_object.close()
        return data
    
probability_of_time = load_object("probability_of_time") 
print("probability_of_time", min(probability_of_time.keys()), max(probability_of_time.keys()))

probability_of_distance = load_object("probability_of_distance") 
print("probability_of_distance", min(probability_of_distance.keys()), max(probability_of_distance.keys()))
probability_of_longitude = load_object("probability_of_longitude") 
print("probability_of_longitude", min(probability_of_longitude.keys()), max(probability_of_longitude.keys()))
probability_of_latitude = load_object("probability_of_latitude") 
print("probability_of_latitude", min(probability_of_latitude.keys()), max(probability_of_latitude.keys()))

probability_of_direction = load_object("probability_of_direction") 
print("probability_of_direction", min(probability_of_direction.keys()), max(probability_of_direction.keys()))
probability_of_direction_alternative = load_object("probability_of_direction_alternative") 
print("probability_of_direction_alternative", min(probability_of_direction_alternative.keys()), max(probability_of_direction_alternative.keys()))
 
probability_of_speed = load_object("probability_of_speed") 
print("probability_of_speed", min(probability_of_speed.keys()), max(probability_of_speed.keys()))
probability_of_speed_alternative = load_object("probability_of_speed_alternative") 
print("probability_of_speed_alternative", min(probability_of_speed_alternative.keys()), max(probability_of_speed_alternative.keys()))
probability_of_x_speed_alternative = load_object("probability_of_x_speed_alternative") 
print("probability_of_x_speed_alternative", min(probability_of_x_speed_alternative.keys()), max(probability_of_x_speed_alternative.keys()))
probability_of_y_speed_alternative = load_object("probability_of_y_speed_alternative") 
print("probability_of_y_speed_alternative", min(probability_of_y_speed_alternative.keys()), max(probability_of_y_speed_alternative.keys()))
 