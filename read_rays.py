from utilities import *
size = 36
all_distances_trajs = pd.read_csv("all_distances_trajs_" + str(size) + ".csv", index_col=False)
all_distances_preprocessed_trajs = pd.read_csv("all_distances_preprocessed_trajs_" + str(size) + ".csv", index_col=False)
all_distances_scaled_trajs = pd.read_csv("all_distances_scaled_trajs_" + str(size) + ".csv", index_col=False)
all_distances_scaled_to_max_trajs = pd.read_csv("all_distances_scaled_to_max_trajs_" + str(size) + ".csv", index_col=False)
'''
for colname in all_distances_trajs.head():
    if "scale" in colname or "offset" in colname:
        plt.title("all_distances_trajs " + colname)
        plt.hist(all_distances_trajs[colname])
        plt.show()
for colname in all_distances_preprocessed_trajs.head():
    if "scale" in colname or "offset" in colname:
        plt.title("all_distances_preprocessed_trajs " + colname)
        plt.hist(all_distances_preprocessed_trajs[colname])
        plt.show()
for colname in all_distances_scaled_trajs.head():
    if "scale" in colname or "offset" in colname:
        plt.title("all_distances_scaled_trajs " + colname)
        plt.hist(all_distances_scaled_trajs[colname])
        plt.show()
        
def get_index(index, name_plot):
        vehicle = all_distances_scaled_to_max_trajs["vehicle"][index]
        ride = all_distances_scaled_to_max_trajs["ride"][index]
        window_size = all_distances_scaled_to_max_trajs["window_size"][index]
        start = all_distances_scaled_to_max_trajs["start"][index]
        max_traj_long, max_traj_lat, max_traj_time = load_traj(vehicle, ride)
        plt.title(name_plot)
        plt.plot(max_traj_long[start:start + window_size], max_traj_lat[start:start + window_size])
        plt.show()

for colname in all_distances_scaled_to_max_trajs.head(): 
    if "scale" in colname or "offset" in colname:
        list_vals = list(all_distances_scaled_to_max_trajs[colname])
        max_val= max(list_vals)
        index_max = list_vals.index(max_val)
        get_index(index_max, "max all_distances_scaled_to_max_trajs " + colname)
        min_val= min(list_vals)
        index_min = list_vals.index(min_val)
        get_index(index_min, "min all_distances_scaled_to_max_trajs " + colname)
        plt.title("all_distances_scaled_to_max_trajs " + colname)
        plt.hist(list_vals)
        plt.show()
''' 
plt.scatter(all_distances_scaled_to_max_trajs["offset_x"], all_distances_scaled_to_max_trajs["offset_y"])
plt.show()
plt.scatter(all_distances_scaled_to_max_trajs["scale_x"], all_distances_scaled_to_max_trajs["scale_y"])
plt.show()
plt.scatter(all_distances_scaled_to_max_trajs["no_scale_x"], all_distances_scaled_to_max_trajs["no_scale_y"])
plt.show()