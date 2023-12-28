from utilities import *

from keras.models import Sequential
from keras.layers import Dense, SimpleRNN, ReLU

from sklearn.metrics import mean_squared_error

all_subdirs = os.listdir()

def get_keys():  

    data_to_cluster_train = dict()
    data_to_cluster_train["xsgn"] = [] 
    data_to_cluster_train["ysgn"] = [] 
    data_to_cluster_train["speed"] = [] 
    data_to_cluster_train["speed ototrak"] = []
    data_to_cluster_train["acceler"] = [] 
    data_to_cluster_train["acceler ototrak"] = []
    data_to_cluster_train["abs acceler"] = [] 
    data_to_cluster_train["abs acceler ototrak"] = []
    data_to_cluster_train["dir diff"] = []
    data_to_cluster_train["abs dir diff"] = []
    data_to_cluster_train["dir diff time"] = []
    data_to_cluster_train["abs dir diff time"] = []
    data_to_cluster_train["xstep"] = []
    data_to_cluster_train["ystep"] = [] 
    data_to_cluster_train["abs xstep"] = []
    data_to_cluster_train["abs ystep"] = []
    data_to_cluster_train["xspeed"] = []
    data_to_cluster_train["yspeed"] = [] 
    data_to_cluster_train["abs xspeed"] = []
    data_to_cluster_train["abs yspeed"] = []
    data_to_cluster_train["heading"] = []
    data_to_cluster_train["abs heading"] = []
    data_to_cluster_train["dist"] = []
    return list(data_to_cluster_train.keys())

def make_dataset_train():  

    ids_to_cluster_train = []
    data_to_cluster_train = dict()
    data_to_cluster_train["xsgn"] = [] 
    data_to_cluster_train["ysgn"] = [] 
    data_to_cluster_train["speed"] = [] 
    data_to_cluster_train["speed ototrak"] = []
    data_to_cluster_train["acceler"] = [] 
    data_to_cluster_train["acceler ototrak"] = []
    data_to_cluster_train["abs acceler"] = [] 
    data_to_cluster_train["abs acceler ototrak"] = []
    data_to_cluster_train["dir diff"] = []
    data_to_cluster_train["abs dir diff"] = []
    data_to_cluster_train["dir diff time"] = []
    data_to_cluster_train["abs dir diff time"] = []
    data_to_cluster_train["xstep"] = []
    data_to_cluster_train["ystep"] = [] 
    data_to_cluster_train["abs xstep"] = []
    data_to_cluster_train["abs ystep"] = []
    data_to_cluster_train["xspeed"] = []
    data_to_cluster_train["yspeed"] = [] 
    data_to_cluster_train["abs xspeed"] = []
    data_to_cluster_train["abs yspeed"] = []
    data_to_cluster_train["heading"] = []
    data_to_cluster_train["abs heading"] = []
    data_to_cluster_train["dist"] = []

    ids_to_cluster_test = []
    data_to_cluster_test = dict()
    data_to_cluster_test["xsgn"] = [] 
    data_to_cluster_test["ysgn"] = [] 
    data_to_cluster_test["speed"] = [] 
    data_to_cluster_test["speed ototrak"] = []
    data_to_cluster_test["acceler"] = [] 
    data_to_cluster_test["acceler ototrak"] = []
    data_to_cluster_test["abs acceler"] = [] 
    data_to_cluster_test["abs acceler ototrak"] = []
    data_to_cluster_test["dir diff"] = []
    data_to_cluster_test["abs dir diff"] = []
    data_to_cluster_test["dir diff time"] = []
    data_to_cluster_test["abs dir diff time"] = []
    data_to_cluster_test["xstep"] = []
    data_to_cluster_test["ystep"] = [] 
    data_to_cluster_test["abs xstep"] = []
    data_to_cluster_test["abs ystep"] = []
    data_to_cluster_test["xspeed"] = []
    data_to_cluster_test["yspeed"] = [] 
    data_to_cluster_test["abs xspeed"] = []
    data_to_cluster_test["abs yspeed"] = []
    data_to_cluster_test["heading"] = []
    data_to_cluster_test["abs heading"] = []
    data_to_cluster_test["dist"] = []
    
    ids_to_cluster_val = []
    data_to_cluster_val = dict()
    data_to_cluster_val["xsgn"] = [] 
    data_to_cluster_val["ysgn"] = [] 
    data_to_cluster_val["speed"] = [] 
    data_to_cluster_val["speed ototrak"] = []
    data_to_cluster_val["acceler"] = [] 
    data_to_cluster_val["acceler ototrak"] = []
    data_to_cluster_val["abs acceler"] = [] 
    data_to_cluster_val["abs acceler ototrak"] = []
    data_to_cluster_val["dir diff"] = []
    data_to_cluster_val["abs dir diff"] = []
    data_to_cluster_val["dir diff time"] = []
    data_to_cluster_val["abs dir diff time"] = []
    data_to_cluster_val["xstep"] = []
    data_to_cluster_val["ystep"] = [] 
    data_to_cluster_val["abs xstep"] = []
    data_to_cluster_val["abs ystep"] = []
    data_to_cluster_val["xspeed"] = []
    data_to_cluster_val["yspeed"] = [] 
    data_to_cluster_val["abs xspeed"] = []
    data_to_cluster_val["abs yspeed"] = []
    data_to_cluster_val["heading"] = []
    data_to_cluster_val["abs heading"] = []
    data_to_cluster_val["dist"] = []
 
    for subdir_name in all_subdirs:
        if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
            continue
        print(subdir_name)
        
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
 
        if len(train_rides) > 1: 
            X_train, X_val, Y_train, Y_val = train_test_split(list(train_rides), list(range(len(train_rides))), test_size = 0.33, random_state = 42)
        
        if len(train_rides) == 1: 
            X_train = list(train_rides)
            X_val = []

        if len(train_rides) == 0: 
            X_train = []
            X_val = []

        save_object(subdir_name + "/val_rides", X_val) 

        val_rides = load_object(subdir_name + "/val_rides")

        test_rides = set()
        if os.path.isfile(subdir_name + "/test_rides"):
            test_rides = load_object(subdir_name + "/test_rides")

        for some_file in all_files:  
            if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames:
                #print("Skipped ride", some_file)
                continue
            #print("Used ride", some_file)
        
            file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file) 
            times = list(file_with_ride["time"])  
            times_tmp_transform = transform_time(times)

            speeds_tmp = list(file_with_ride["fields_speed"])  
            accelers_ototrak_trajs = return_acceler_speeds(speeds_tmp, times_tmp_transform) 
            accelers_abs_ototrak_trajs = return_acceler_speeds(speeds_tmp, times_tmp_transform, True) 

            headings = list(file_with_ride["fields_direction"])   
            longitudes = list(file_with_ride["fields_longitude"])
            latitudes = list(file_with_ride["fields_latitude"])  
            times = list(file_with_ride["time"])  
            times_tmp_transform = transform_time(times) 

            xsteps, ysteps, absxsteps, absysteps = return_steps_by_axis(longitudes, latitudes, times_tmp_transform)  
            x_speeds_trajs, y_speeds_trajs, abs_x_speeds_trajs, abs_y_speeds_trajs = return_speeds_by_axis(longitudes, latitudes, times_tmp_transform)

            angles = return_angle_diffs_no_abs(headings)    
            angles_abs = return_angle_diffs(headings)  
            angles_time = return_angle_diffs_no_abs_time(headings, times_tmp_transform)    
            angles_abs_time = return_angle_diffs_time(headings, times_tmp_transform)  

            speeds_trajs = return_speeds_long_lat(longitudes, latitudes, times_tmp_transform)
            accelers_trajs = return_acceler_speeds(speeds_trajs, times_tmp_transform)  
            accelers_abs_trajs = return_acceler_speeds(speeds_trajs, times_tmp_transform, True)  
            
            headings_trajs = return_angles(longitudes, latitudes)
            headings_abs_trajs = return_angles_abs(longitudes, latitudes) 

            distances = return_euclid_by_axis(longitudes, latitudes)

            if some_file in val_rides: 
                for i in range(len(accelers_trajs)):  
                    data_to_cluster_val["xsgn"].append(int(longitudes[i + 1] > longitudes[i]))
                    data_to_cluster_val["ysgn"].append(int(latitudes[i + 1] > latitudes[i]))
                    data_to_cluster_val["speed"].append(speeds_tmp[i])
                    data_to_cluster_val["speed ototrak"].append(speeds_trajs[i])
                    data_to_cluster_val["acceler"].append(accelers_trajs[i])
                    data_to_cluster_val["acceler ototrak"].append(accelers_ototrak_trajs[i])
                    data_to_cluster_val["abs acceler"].append(accelers_abs_trajs[i])
                    data_to_cluster_val["abs acceler ototrak"].append(accelers_abs_ototrak_trajs[i])
                    data_to_cluster_val["dir diff"].append(angles[i])
                    data_to_cluster_val["abs dir diff"].append(angles_abs[i])
                    data_to_cluster_val["dir diff time"].append(angles_time[i])
                    data_to_cluster_val["abs dir diff time"].append(angles_abs_time[i])
                    data_to_cluster_val["xstep"].append(xsteps[i])
                    data_to_cluster_val["ystep"].append(ysteps[i])
                    data_to_cluster_val["abs xstep"].append(absxsteps[i])
                    data_to_cluster_val["abs ystep"].append(absysteps[i])
                    data_to_cluster_val["xspeed"].append(x_speeds_trajs[i])
                    data_to_cluster_val["yspeed"].append(y_speeds_trajs[i])
                    data_to_cluster_val["abs xspeed"].append(abs_x_speeds_trajs[i])
                    data_to_cluster_val["abs yspeed"].append(abs_y_speeds_trajs[i])
                    data_to_cluster_val["heading"].append(headings_trajs[i])
                    data_to_cluster_val["abs heading"].append(headings_abs_trajs[i])
                    data_to_cluster_val["dist"].append(distances[i])
                    ids_to_cluster_val.append([subdir_name, some_file, i])
            elif some_file in train_rides: 
                for i in range(len(accelers_trajs)):  
                    data_to_cluster_train["xsgn"].append(int(longitudes[i + 1] > longitudes[i]))
                    data_to_cluster_train["ysgn"].append(int(latitudes[i + 1] > latitudes[i]))
                    data_to_cluster_train["speed"].append(speeds_tmp[i])
                    data_to_cluster_train["speed ototrak"].append(speeds_trajs[i])
                    data_to_cluster_train["acceler"].append(accelers_trajs[i])
                    data_to_cluster_train["acceler ototrak"].append(accelers_ototrak_trajs[i])
                    data_to_cluster_train["abs acceler"].append(accelers_abs_trajs[i])
                    data_to_cluster_train["abs acceler ototrak"].append(accelers_abs_ototrak_trajs[i])
                    data_to_cluster_train["dir diff"].append(angles[i])
                    data_to_cluster_train["abs dir diff"].append(angles_abs[i])
                    data_to_cluster_train["dir diff time"].append(angles_time[i])
                    data_to_cluster_train["abs dir diff time"].append(angles_abs_time[i])
                    data_to_cluster_train["xstep"].append(xsteps[i])
                    data_to_cluster_train["ystep"].append(ysteps[i])
                    data_to_cluster_train["abs xstep"].append(absxsteps[i])
                    data_to_cluster_train["abs ystep"].append(absysteps[i])
                    data_to_cluster_train["xspeed"].append(x_speeds_trajs[i])
                    data_to_cluster_train["yspeed"].append(y_speeds_trajs[i])
                    data_to_cluster_train["abs xspeed"].append(abs_x_speeds_trajs[i])
                    data_to_cluster_train["abs yspeed"].append(abs_y_speeds_trajs[i])
                    data_to_cluster_train["heading"].append(headings_trajs[i])
                    data_to_cluster_train["abs heading"].append(headings_abs_trajs[i])
                    data_to_cluster_train["dist"].append(distances[i])
                    ids_to_cluster_train.append([subdir_name, some_file, i])
            elif some_file in test_rides: 
                for i in range(len(accelers_trajs)):   
                    data_to_cluster_test["xsgn"].append(int(longitudes[i + 1] > longitudes[i]))
                    data_to_cluster_test["ysgn"].append(int(latitudes[i + 1] > latitudes[i]))
                    data_to_cluster_test["speed"].append(speeds_tmp[i])
                    data_to_cluster_test["speed ototrak"].append(speeds_trajs[i])
                    data_to_cluster_test["acceler"].append(accelers_trajs[i])
                    data_to_cluster_test["acceler ototrak"].append(accelers_ototrak_trajs[i])
                    data_to_cluster_test["abs acceler"].append(accelers_abs_trajs[i])
                    data_to_cluster_test["abs acceler ototrak"].append(accelers_abs_ototrak_trajs[i])
                    data_to_cluster_test["dir diff"].append(angles[i])
                    data_to_cluster_test["abs dir diff"].append(angles_abs[i])
                    data_to_cluster_test["dir diff time"].append(angles_time[i])
                    data_to_cluster_test["abs dir diff time"].append(angles_abs_time[i])
                    data_to_cluster_test["xstep"].append(xsteps[i])
                    data_to_cluster_test["ystep"].append(ysteps[i])
                    data_to_cluster_test["abs xstep"].append(absxsteps[i])
                    data_to_cluster_test["abs ystep"].append(absysteps[i])
                    data_to_cluster_test["xspeed"].append(x_speeds_trajs[i])
                    data_to_cluster_test["yspeed"].append(y_speeds_trajs[i])
                    data_to_cluster_test["abs xspeed"].append(abs_x_speeds_trajs[i])
                    data_to_cluster_test["abs yspeed"].append(abs_y_speeds_trajs[i])
                    data_to_cluster_test["heading"].append(headings_trajs[i])
                    data_to_cluster_test["abs heading"].append(headings_abs_trajs[i])
                    data_to_cluster_test["dist"].append(distances[i])
                    ids_to_cluster_test.append([subdir_name, some_file, i])
    for k in data_to_cluster_train:
        data_to_cluster_train[k] = np.array(data_to_cluster_train[k])
    for k in data_to_cluster_val:
        data_to_cluster_val[k] = np.array(data_to_cluster_val[k])
    for k in data_to_cluster_test:
        data_to_cluster_test[k] = np.array(data_to_cluster_test[k])
    return data_to_cluster_train, data_to_cluster_test, data_to_cluster_val, ids_to_cluster_train, ids_to_cluster_test, ids_to_cluster_val

def get_XY(dat, time_steps, num_props): 
    Y_ind = np.arange(time_steps, len(dat), time_steps)
    print(time_steps)
    print(Y_ind)
    Y = dat[Y_ind] 
    rows_x = len(Y)
    print(rows_x)
    X = dat[range(time_steps * rows_x)]
    X = np.reshape(X, (rows_x, time_steps, num_props))   
    print(np.shape(X), np.shape(Y)) 
    return X, Y

def print_error(trainY, valY, testY, train_predict, val_predict, test_predict, title, range_val):  
    train_rmse = math.sqrt(mean_squared_error(trainY, train_predict))
    val_rmse = math.sqrt(mean_squared_error(valY, val_predict)) 
    test_rmse = math.sqrt(mean_squared_error(testY, test_predict)) 
    print(title, 'Train RMSE: %.3f RMSE' % (train_rmse / range_val))
    print(title, 'Validation RMSE: %.3f RMSE' % (val_rmse / range_val))
    print(title, 'Test RMSE: %.3f RMSE' % (test_rmse / range_val))    

def create_RNN(hidden_units, dense_units, input_shape, activation, relu_use = ""):
    model = Sequential()
    model.add(SimpleRNN(hidden_units, input_shape=input_shape, 
                        activation=activation[0]))
    model.add(Dense(units=dense_units, activation=activation[1]))
    if relu_use != "":
        model.add(relu_use)
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

def plot_result(trainY, valY, testY, train_predict, val_predict, test_predict, title):
    actual = np.append(trainY, valY) 
    actual = np.append(actual, testY) 
    predictions = np.append(train_predict, val_predict)
    predictions = np.append(predictions, test_predict)
    rows = len(actual)
    plt.figure(figsize = (15, 6), dpi = 80)
    plt.plot(range(rows), actual, color = "b") 
    plt.plot(range(rows), predictions, color = "orange") 
    plt.axvline(x = len(trainY), color = 'r')
    plt.axvline(x = len(trainY) + len(valY), color = 'g')
    plt.legend(['Actual', 'Predictions'])
    plt.xlabel('Observation number after given time steps')
    plt.ylabel(title)
    plt.title('Actual and Predicted Values.\nThe Red Line Separates The Training And Validation Examples.\nThe Red Line Separates The Validation And Testing Examples.\n') 
    if not os.path.isdir("train_net/" + title.replace("_", "/") + "/predictions"):
        os.makedirs("train_net/" + title.replace("_", "/") + "/predictions")
    plt.savefig("train_net/" + title.replace("_", "/") + "/predictions/" + title + "_actual_predicted.png", bbox_inches = "tight")
    plt.close()
    
def plot_actual(trainY, valY, testY, title):
    actual = np.append(trainY, valY) 
    actual = np.append(actual, testY) 
    rows = len(actual)
    plt.figure(figsize = (15, 6), dpi = 80)
    plt.plot(range(rows), actual, color = "b") 
    plt.axvline(x = len(trainY), color = 'r')
    plt.axvline(x = len(trainY) + len(valY), color = 'g')
    plt.legend(['Predictions'])
    plt.xlabel('Observation number after given time steps')
    plt.ylabel(title)
    plt.title('Actual Values.\nThe Red Line Separates The Training And Validation Examples.\nThe Red Line Separates The Validation And Testing Examples.\n') 
    if not os.path.isdir("train_net/" + title.replace("_", "/") + "/predictions"):
        os.makedirs("train_net/" + title.replace("_", "/") + "/predictions")
    plt.savefig("train_net/" + title.replace("_", "/") + "/predictions/" + title + "_actual.png", bbox_inches = "tight")
    plt.close()

def plot_predict(trainY, valY, testY, title):
    actual = np.append(trainY, valY) 
    actual = np.append(actual, testY) 
    rows = len(actual)
    plt.figure(figsize = (15, 6), dpi = 80)
    plt.plot(range(rows), actual, color = "orange") 
    plt.axvline(x = len(trainY), color = 'r')
    plt.axvline(x = len(trainY) + len(valY), color = 'g')
    plt.legend(['Predictions'])
    plt.xlabel('Observation number after given time steps')
    plt.ylabel(title)
    plt.title('Predicted Values.\nThe Red Line Separates The Training And Validation Examples.\nThe Red Line Separates The Validation And Testing Examples.\n') 
    if not os.path.isdir("train_net/" + title.replace("_", "/") + "/predictions"):
        os.makedirs("train_net/" + title.replace("_", "/") + "/predictions")
    plt.savefig("train_net/" + title.replace("_", "/") + "/predictions/" + title + "_predicted.png", bbox_inches = "tight")
    plt.close()

def process_predict(preds, mini, maxi):
    new_preds = []
    for p in preds:
        if p < mini:
            new_preds.append(mini)
            continue
        if p > maxi:
            new_preds.append(maxi)
            continue
        new_preds.append(p)
    return new_preds

def binary_pred(preds):
    return [int(p >= 0.5) for p in preds]

def make_nets():
    data_to_cluster_train, data_to_cluster_test, data_to_cluster_val, ids_to_cluster_train, ids_to_cluster_test, ids_to_cluster_val = make_dataset_train()
    if not os.path.isdir("train_net/ids/train"):
        os.makedirs("train_net/ids/train")
    save_object("train_net/ids/train/ids_to_cluster_train", ids_to_cluster_train)
    if not os.path.isdir("train_net/ids/test"):
        os.makedirs("train_net/ids/test")
    save_object("train_net/ids/test/ids_to_cluster_test", ids_to_cluster_test)
    if not os.path.isdir("train_net/ids/val"):
        os.makedirs("train_net/ids/val")
    save_object("train_net/ids/val/ids_to_cluster_val", ids_to_cluster_val)
    num_props = 1
    for prop_name in data_to_cluster_train:
        if not os.path.isdir("train_net/" + prop_name + "/data/train"):
            os.makedirs("train_net/" + prop_name + "/data/train")
        save_object("train_net/" + prop_name + "/data/train/data_to_cluster_train_" + prop_name, data_to_cluster_train[prop_name])
        if not os.path.isdir("train_net/" + prop_name + "/data/test"):
            os.makedirs("train_net/" + prop_name + "/data/test")
        save_object("train_net/" + prop_name + "/data/test/data_to_cluster_test_" + prop_name, data_to_cluster_test[prop_name])
        if not os.path.isdir("train_net/" + prop_name + "/data/val"):
            os.makedirs("train_net/" + prop_name + "/data/val")
        save_object("train_net/" + prop_name + "/data/val/data_to_cluster_val_" + prop_name, data_to_cluster_val[prop_name])
        min_val = min(min(data_to_cluster_train[prop_name]), min(data_to_cluster_test[prop_name]))
        min_val = min(min_val, min(data_to_cluster_val[prop_name]))
        max_val = max(max(data_to_cluster_train[prop_name]), max(data_to_cluster_test[prop_name]))
        max_val = max(max_val, max(data_to_cluster_val[prop_name]))
        if max_val >= 359 and max_val <= 360:
            max_val = 360
        if max_val >= 358 and max_val <= 359:
            max_val = 359 
        if max_val > 90 and max_val <= 180:
            max_val = 180 
        if min_val >= -360 and min_val <= -359:
            min_val = -360
        if min_val >= -359 and min_val <= -358:
            min_val = -359
        if min_val >= -180 and min_val < -90:
            min_val = -180
        range_val = max_val - min_val
        for window_size in range(2, 21):
            xtrain, ytrain = get_XY(data_to_cluster_train[prop_name], window_size, num_props)
            xtest, ytest = get_XY(data_to_cluster_test[prop_name], window_size, num_props)
            xval, yval = get_XY(data_to_cluster_val[prop_name], window_size, num_props)
            if not os.path.isdir("train_net/" + str(window_size) + "/" + prop_name + "/data_reshaped"):
                os.makedirs("train_net/" + str(window_size) + "/" + prop_name + "/data_reshaped")
            save_object("train_net/" + str(window_size) + "/" + prop_name + "/data_reshaped/trainX_" + str(window_size) + "_" + prop_name, xtrain)
            save_object("train_net/" + str(window_size) + "/" + prop_name + "/data_reshaped/testX_" + str(window_size) + "_" + prop_name, xtest)
            save_object("train_net/" + str(window_size) + "/" + prop_name + "/data_reshaped/valX_" + str(window_size) + "_" + prop_name, xval)
            save_object("train_net/" + str(window_size) + "/" + prop_name + "/data_reshaped/trainY_" + str(window_size) + "_" + prop_name, ytrain)
            save_object("train_net/" + str(window_size) + "/" + prop_name + "/data_reshaped/testY_" + str(window_size) + "_" + prop_name, ytest)
            save_object("train_net/" + str(window_size) + "/" + prop_name + "/data_reshaped/valY_" + str(window_size) + "_" + prop_name, yval)
            act = ['linear', 'linear']
            relu_layer = ""
            if min_val >= 0:
                if "dist" not in prop_name and "speed" not in prop_name and "acceler" not in prop_name and "step" not in prop_name:
                    relu_layer = ReLU(
                        max_value = max_val,
                        negative_slope = 0,
                        threshold = 0,
                    )
                else:
                    relu_layer = ReLU( 
                        negative_slope = 0,
                        threshold = 0,
                    )
            for n_layers in range(2, 21):
                print(prop_name, window_size, n_layers)
                demo_model = create_RNN(n_layers, 1, (window_size, num_props), act, relu_layer)   
                if not os.path.isdir("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/model"):
                    os.makedirs("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/model")
                save_object("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/model/demo_model_" + str(window_size) + "_" + str(n_layers) + "_" + prop_name, demo_model)
                history = demo_model.fit(xtrain, ytrain, verbose = 1)  
                save_object("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/model/history_" + str(window_size) + "_" + str(n_layers) + "_" + prop_name, history)
                predict_train = demo_model.predict(xtrain)
                predict_val = demo_model.predict(xval) 
                predict_test = demo_model.predict(xtest) 
                if not os.path.isdir("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/predictions"):
                    os.makedirs("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/predictions")
                save_object("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/predictions/train_predict_" + str(window_size) + "_" + str(n_layers) + "_" + prop_name, predict_train) 
                save_object("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/predictions/val_predict_" + str(window_size) + "_" + str(n_layers) + "_" + prop_name, predict_val) 
                save_object("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/predictions/test_predict_" + str(window_size) + "_" + str(n_layers) + "_" + prop_name, predict_test)
                print_error(ytrain, yval, ytest, predict_train, predict_val, predict_test, str(window_size) + "_" + str(n_layers) + "_" + prop_name, range_val)
                plot_predict(predict_train, predict_val, predict_test, str(window_size) + "_" + str(n_layers) + "_" + prop_name) 
                plot_actual(ytrain, yval, ytest, str(window_size) + "_" + str(n_layers) + "_" + prop_name)
                plot_result(ytrain, yval, ytest, predict_train, predict_val, predict_test, str(window_size) + "_" + str(n_layers) + "_" + prop_name)

def make_net_all():
    window_size = 3 
    data_to_cluster_train, data_to_cluster_test = make_dataset_train()
    key_vals = list(data_to_cluster_train.keys())
    num_props = len(key_vals)
    all_data_train = []
    for i in range(len(data_to_cluster_train[key_vals[0]])):
        all_data_train.append([])
        for prop_name in data_to_cluster_train:
            all_data_train[-1].append(data_to_cluster_train[prop_name][i])
        all_data_train[-1] = np.array(all_data_train[-1])
    all_data_train = np.array(all_data_train)
    print(np.shape(all_data_train))
    xtrain, ytrain = get_XY(all_data_train, window_size, num_props)
    print(np.shape(xtrain), np.shape(ytrain))
    all_data_test = []
    for i in range(len(data_to_cluster_test[key_vals[0]])):
        all_data_test.append([])
        for prop_name in data_to_cluster_test:
            all_data_test[-1].append(data_to_cluster_test[prop_name][i])
        all_data_test[-1] = np.array(all_data_test[-1])
    all_data_test = np.array(all_data_test)
    xtest, ytest = get_XY(all_data_test, window_size, num_props)
    demo_model = create_RNN(2, 1, (window_size, num_props), activation=['linear', 'linear'])   
    history = demo_model.fit(xtrain, ytrain, verbose = 1)  
    predict_train = demo_model.predict(xtrain) 
    predict_test = demo_model.predict(xtest)
    print(predict_test[:10], xtest[:10])

make_nets()
#make_net_all()
        
def read_nets(): 
    for prop_name in get_keys():  
           for window_size in range(2, 21):
            xtrain = load_object("train_net/" + str(window_size) + "/" + prop_name + "/data_reshaped/trainX_" + str(window_size) + "_" + prop_name)
            xval = load_object("train_net/" + str(window_size) + "/" + prop_name + "/data_reshaped/valX_" + str(window_size) + "_" + prop_name)
            xtest = load_object("train_net/" + str(window_size) + "/" + prop_name + "/data_reshaped/testX_" + str(window_size) + "_" + prop_name)
            ytrain = load_object("train_net/" + str(window_size) + "/" + prop_name + "/data_reshaped/trainY_" + str(window_size) + "_" + prop_name)
            yval = load_object("train_net/" + str(window_size) + "/" + prop_name + "/data_reshaped/valY_" + str(window_size) + "_" + prop_name)
            ytest = load_object("train_net/" + str(window_size) + "/" + prop_name + "/data_reshaped/testY_" + str(window_size) + "_" + prop_name) 
            for n_layers in range(2, 21):
                print(prop_name, window_size, n_layers)
                predict_train = load_object("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/predictions/train_predict_" + str(window_size) + "_" + str(n_layers) + "_" + prop_name)
                predict_val = load_object("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/predictions/val_predict_" + str(window_size) + "_" + str(n_layers) + "_" + prop_name)  
                predict_test = load_object("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/predictions/test_predict_" + str(window_size) + "_" + str(n_layers) + "_" + prop_name)  
                min_val = min(min(np.max(xtrain), np.max(xtest)), min(min(ytrain), min(ytest)))
                min_val = min(min_val, min(np.min(xval), min(yval)))
                max_val = max(max(np.max(xtrain), np.max(xtest)), max(max(ytrain), max(ytest)))
                max_val = max(max_val, max(np.max(xval), max(yval)))
                if max_val >= 359 and max_val <= 360:
                    max_val = 360
                if max_val >= 358 and max_val <= 359:
                    max_val = 359 
                if max_val > 90 and max_val <= 180:
                    max_val = 180 
                if min_val >= -360 and min_val <= -359:
                    min_val = -360
                if min_val >= -359 and min_val <= -358:
                    min_val = -359
                if min_val >= -180 and min_val < -90:
                    min_val = -180
                range_val = max_val - min_val
                print_error(ytrain, yval,  ytest, predict_train, predict_val, predict_test, str(window_size) + "_" + str(n_layers) + "_" + prop_name, range_val)
                plot_predict(predict_train, predict_val, predict_test, str(window_size) + "_" + str(n_layers) + "_" + prop_name) 
                plot_actual(ytrain, yval, ytest, str(window_size) + "_" + str(n_layers) + "_" + prop_name)
                plot_result(ytrain, yval, ytest, predict_train, predict_val, predict_test, str(window_size) + "_" + str(n_layers) + "_" + prop_name)

read_nets()
        
def read_predictions():
    ids_train = load_object("train_net/ids/train/ids_to_cluster_train") 
    ids_val = load_object("train_net/ids/val/ids_to_cluster_val")
    ids_test = load_object("train_net/ids/test/ids_to_cluster_test")
    rides = []
    last_end = 0
    while last_end < len(ids_test):
        start_ride = last_end
        end_ride = start_ride
        while end_ride < len(ids_test) and ids_test[start_ride][:2] == ids_test[end_ride][:2]: 
            end_ride += 1
        #print(start_ride, end_ride, ids_test[start_ride][:2], ids_test[end_ride - 1][:2])
        last_end = end_ride
        rides.append([start_ride, end_ride]) 
    for prop_name in get_keys():   
        for window_size in range(2, 21):
            ytrain = load_object("train_net/" + str(window_size) + "/" + prop_name + "/data_reshaped/trainY_" + str(window_size) + "_" + prop_name)
            ytest = load_object("train_net/" + str(window_size) + "/" + prop_name + "/data_reshaped/testY_" + str(window_size) + "_" + prop_name) 
            for n_layers in range(2, 21):
                print(prop_name, window_size, n_layers)
                predict_train = load_object("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/predictions/train_predict_" + str(window_size) + "_" + str(n_layers) + "_" + prop_name)
                predict_test = load_object("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/predictions/test_predict_" + str(window_size) + "_" + str(n_layers) + "_" + prop_name)
                print(prop_name, window_size, n_layers, min(ytest), max(ytest), min(predict_test), max(predict_test), min(ytrain), max(ytrain), min(predict_train), max(predict_train))
            
read_predictions()