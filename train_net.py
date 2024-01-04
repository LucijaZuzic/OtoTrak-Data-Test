from utilities import *

from keras.models import Sequential, load_model
from keras.layers import Dense, SimpleRNN, LSTM, ReLU

from sklearn.metrics import mean_squared_error

all_subdirs = os.listdir()

def get_keys():  

    data_to_cluster_train = dict()
    data_to_cluster_train["time"] = [] 
    data_to_cluster_train["xstep"] = []
    data_to_cluster_train["ystep"] = [] 
    data_to_cluster_train["abs xstep"] = []
    data_to_cluster_train["abs ystep"] = []
    data_to_cluster_train["xspeed"] = []
    data_to_cluster_train["yspeed"] = [] 
    data_to_cluster_train["abs xspeed"] = []
    data_to_cluster_train["abs yspeed"] = []
    data_to_cluster_train["xacceler"] = []
    data_to_cluster_train["abs xacceler"] = []
    data_to_cluster_train["xacceler abs"] = []
    data_to_cluster_train["abs xacceler abs"] = []
    data_to_cluster_train["yacceler"] = [] 
    data_to_cluster_train["abs yacceler"] = []
    data_to_cluster_train["yacceler abs"] = [] 
    data_to_cluster_train["abs yacceler abs"] = []
    data_to_cluster_train["dir"] = []
    data_to_cluster_train["dir diff"] = []
    data_to_cluster_train["dir diff time"] = [] 
    data_to_cluster_train["abs dir diff"] = []
    data_to_cluster_train["abs dir diff time"] = []
    data_to_cluster_train["speed traj"] = [] 
    data_to_cluster_train["speed"] = []
    data_to_cluster_train["acceler"] = [] 
    data_to_cluster_train["acceler ototrak"] = []
    data_to_cluster_train["abs acceler"] = [] 
    data_to_cluster_train["abs acceler ototrak"] = []
    data_to_cluster_train["heading"] = []
    data_to_cluster_train["abs heading"] = []
    data_to_cluster_train["heading diff"] = []
    data_to_cluster_train["abs heading diff"] = []
    data_to_cluster_train["heading diff time"] = []
    data_to_cluster_train["abs heading diff time"] = []
    data_to_cluster_train["dist"] = []
    data_to_cluster_train["xsgn"] = [] 
    data_to_cluster_train["ysgn"] = [] 
    return list(data_to_cluster_train.keys())

def make_dataset_train():  

    ids_to_cluster = dict()

    ids_to_cluster["train"] = dict()
    ids_to_cluster["val"] = dict()
    ids_to_cluster["test"] = dict()

    data_to_cluster = dict()

    data_to_cluster["train"] = dict()
    data_to_cluster["val"] = dict()
    data_to_cluster["test"] = dict()

    for k in get_keys():

        data_to_cluster["train"][k] = []
        data_to_cluster["val"][k] = []
        data_to_cluster["test"][k] = []

        ids_to_cluster["train"][k] = []
        ids_to_cluster["val"][k] = []
        ids_to_cluster["test"][k] = []

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
            arr_for_key = dict()

            time_diffs = [times_tmp_transform[i] - times_tmp_transform[i - 1] for i in range(1, len(times_tmp_transform))]
            arr_for_key["time"] = time_diffs

            xsteps, ysteps, absxsteps, absysteps = return_steps_by_axis(longitudes, latitudes, times_tmp_transform)  

            arr_for_key["xstep"] = xsteps
            arr_for_key["ystep"] = ysteps
            arr_for_key["abs xstep"] = absxsteps
            arr_for_key["abs ystep"] = absysteps

            x_speeds_trajs, y_speeds_trajs, abs_x_speeds_trajs, abs_y_speeds_trajs = return_speeds_by_axis(longitudes, latitudes, times_tmp_transform)

            arr_for_key["xspeed"] = x_speeds_trajs
            arr_for_key["yspeed"] = y_speeds_trajs
            arr_for_key["abs xspeed"] = abs_x_speeds_trajs
            arr_for_key["abs yspeed"] = abs_y_speeds_trajs

            x_accelers_trajs = return_acceler_speeds(x_speeds_trajs, times_tmp_transform) 
            x_accelers_trajs_abs = return_acceler_speeds(x_speeds_trajs, times_tmp_transform, True) 

            abs_x_accelers_trajs = return_acceler_speeds(abs_x_speeds_trajs, times_tmp_transform) 
            abs_x_accelers_trajs_abs = return_acceler_speeds(abs_x_speeds_trajs, times_tmp_transform, True) 

            arr_for_key["xacceler"] = x_accelers_trajs
            arr_for_key["abs xacceler"] = x_accelers_trajs_abs
            arr_for_key["xacceler abs"] = abs_x_accelers_trajs
            arr_for_key["abs xacceler abs"] = abs_x_accelers_trajs_abs
 
            y_accelers_trajs = return_acceler_speeds(y_speeds_trajs, times_tmp_transform) 
            y_accelers_trajs_abs = return_acceler_speeds(y_speeds_trajs, times_tmp_transform, True) 

            abs_y_accelers_trajs = return_acceler_speeds(abs_y_speeds_trajs, times_tmp_transform) 
            abs_y_accelers_trajs_abs = return_acceler_speeds(abs_y_speeds_trajs, times_tmp_transform, True) 
            
            arr_for_key["yacceler"] = y_accelers_trajs
            arr_for_key["abs yacceler"] = y_accelers_trajs_abs
            arr_for_key["yacceler abs"] = abs_y_accelers_trajs
            arr_for_key["abs yacceler abs"] = abs_y_accelers_trajs_abs
             
            angles = return_angle_diffs_no_abs(headings)    
            angles_abs = return_angle_diffs(headings)  
            angles_time = return_angle_diffs_no_abs_time(headings, times_tmp_transform)    
            angles_abs_time = return_angle_diffs_time(headings, times_tmp_transform) 
  
            arr_for_key["dir"] = headings
            arr_for_key["dir diff"] = angles
            arr_for_key["dir diff time"] = angles_time 
            arr_for_key["abs dir diff"] = angles_abs
            arr_for_key["abs dir diff time"] = angles_abs_time 

            speeds_trajs = return_speeds_long_lat(longitudes, latitudes, times_tmp_transform)
            accelers_trajs = return_acceler_speeds(speeds_trajs, times_tmp_transform)  
            accelers_abs_trajs = return_acceler_speeds(speeds_trajs, times_tmp_transform, True)  

            arr_for_key["speed traj"] = speeds_trajs
            arr_for_key["speed"] = speeds_tmp
            arr_for_key["acceler"] = accelers_trajs
            arr_for_key["acceler ototrak"] = accelers_ototrak_trajs
            arr_for_key["abs acceler"] = accelers_abs_trajs
            arr_for_key["abs acceler ototrak"] = accelers_abs_ototrak_trajs
            
            headings_trajs = return_angles(longitudes, latitudes)
            headings_abs_trajs = return_angles_abs(longitudes, latitudes) 

            headings_trajs_diff = return_angle_diffs_no_abs(headings_trajs)    
            headings_trajs_diff_abs = return_angle_diffs(headings_trajs)  
            headings_trajs_time = return_angle_diffs_no_abs_time(headings_trajs, times_tmp_transform)    
            headings_trajs_abs_time = return_angle_diffs_time(headings_trajs, times_tmp_transform)  

            arr_for_key["heading"] = headings_trajs
            arr_for_key["abs heading"] = headings_abs_trajs

            arr_for_key["heading diff"] = headings_trajs_diff
            arr_for_key["abs heading diff"] = headings_trajs_diff_abs
            arr_for_key["heading diff time"] = headings_trajs_time
            arr_for_key["abs heading diff time"] = headings_trajs_abs_time

            distances = return_euclid_by_axis(longitudes, latitudes)
            arr_for_key["dist"] = distances

            xsgns = [int(longitudes[i + 1] > longitudes[i]) for i in range(len(longitudes) - 1)]
            ysgns = [int(latitudes[i + 1] > latitudes[i]) for i in range(len(latitudes) - 1)]
            arr_for_key["xsgn"] = xsgns 
            arr_for_key["ysgn"] = ysgns


            if some_file in val_rides: 
                mark = "val"
            elif some_file in train_rides: 
                mark = "train"
            elif some_file in test_rides: 
                mark = "test"
            
            for ak in arr_for_key:
                for ixpos in range(len(arr_for_key[ak])):  
                    data_to_cluster[mark][ak].append(arr_for_key[ak][ixpos])  
                    ids_to_cluster[mark][ak].append([subdir_name, some_file, ixpos]) 

    for k in data_to_cluster["train"]:
        data_to_cluster["train"][k] = np.array(data_to_cluster["train"][k])
    for k in data_to_cluster["val"]:
        data_to_cluster["val"][k] = np.array(data_to_cluster["val"][k])
    for k in data_to_cluster["test"]:
        data_to_cluster["test"][k] = np.array(data_to_cluster["test"][k])
        
    return data_to_cluster["train"], data_to_cluster["test"], data_to_cluster["val"], ids_to_cluster["train"], ids_to_cluster["test"], ids_to_cluster["val"]

def get_XY(dat, time_steps, num_props): 
    Y_ind = np.arange(time_steps, len(dat), time_steps) 
    Y = dat[Y_ind] 
    rows_x = len(Y) 
    X = dat[range(time_steps * rows_x)]
    X = np.reshape(X, (rows_x, time_steps, num_props))    
    return X, Y

def print_error(trainY, valY, testY, train_predict, val_predict, test_predict, title, range_val):  
    train_rmse = math.sqrt(mean_squared_error(trainY, train_predict))
    val_rmse = math.sqrt(mean_squared_error(valY, val_predict)) 
    test_rmse = math.sqrt(mean_squared_error(testY, test_predict)) 
    #print(title, 'Train RMSE: %.6f RMSE' % (train_rmse / range_val))
    #print(title, 'Validation RMSE: %.6f RMSE' % (val_rmse / range_val))
    #print(title, 'Test RMSE: %.6f RMSE' % (test_rmse / range_val))   
    return train_rmse, val_rmse, test_rmse

def create_RNN(hidden_units, dense_units, input_shape, act_layer = "linear"):
    model = Sequential()
    model.add(LSTM(hidden_units, input_shape = input_shape, activation = act_layer))
    model.add(Dense(units = dense_units, activation = act_layer))
    model.compile(loss = 'mean_squared_error', optimizer = 'adam')
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
    num_props = 1
    for prop_name in data_to_cluster_train:
        
        if "heading" not in prop_name:
            continue

        if not os.path.isdir("train_net/" + prop_name + "/data/train"):
            os.makedirs("train_net/" + prop_name + "/data/train")
        save_object("train_net/" + prop_name + "/data/train/data_to_cluster_train_" + prop_name, data_to_cluster_train[prop_name])
        if not os.path.isdir("train_net/" + prop_name + "/data/test"):
            os.makedirs("train_net/" + prop_name + "/data/test")
        save_object("train_net/" + prop_name + "/data/test/data_to_cluster_test_" + prop_name, data_to_cluster_test[prop_name])
        if not os.path.isdir("train_net/" + prop_name + "/data/val"):
            os.makedirs("train_net/" + prop_name + "/data/val")
        save_object("train_net/" + prop_name + "/data/val/data_to_cluster_val_" + prop_name, data_to_cluster_val[prop_name])

        if not os.path.isdir("train_net/" + prop_name + "/ids/train"):
            os.makedirs("train_net/" + prop_name + "/ids/train")
        save_object("train_net/" + prop_name + "/ids/train/ids_to_cluster_train_" + prop_name, ids_to_cluster_train[prop_name])
        if not os.path.isdir("train_net/" + prop_name + "/ids/test"):
            os.makedirs("train_net/" + prop_name + "/ids/test")
        save_object("train_net/" + prop_name + "/ids/test/ids_to_cluster_test_" + prop_name, ids_to_cluster_test[prop_name])
        if not os.path.isdir("train_net/" + prop_name + "/ids/val"):
            os.makedirs("train_net/" + prop_name + "/ids/val")
        save_object("train_net/" + prop_name + "/ids/val/ids_to_cluster_val_" + prop_name, ids_to_cluster_val[prop_name])
        print(len(data_to_cluster_train[prop_name]), len(data_to_cluster_test[prop_name]), len(data_to_cluster_val[prop_name]))
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

        act_layer = "linear"
        if min_val >= 0:
            if "dist" not in prop_name and "speed" not in prop_name and "acceler" not in prop_name and "step" not in prop_name and "time" not in prop_name:
                act_layer = ReLU(
                    max_value = max_val,
                    negative_slope = 0,
                    threshold = 0,
                )
                print("Relu max", max_val, prop_name)
            else:
                act_layer = ReLU( 
                    negative_slope = 0,
                    threshold = 0,
                )
                print("Relu no max", prop_name)
                
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
                  
            for n_layers in range(2, 21):
                print(prop_name, window_size, n_layers)
                demo_model = create_RNN(n_layers, 1, (window_size, num_props), act_layer)   
                if not os.path.isdir("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/model"):
                    os.makedirs("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/model")
                demo_model.save("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/model/demo_model_" + str(window_size) + "_" + str(n_layers) + "_" + prop_name + '.h5')
                history = demo_model.fit(xtrain, ytrain, verbose = 1)  
                save_object("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/model/history_" + str(window_size) + "_" + str(n_layers) + "_" + prop_name, history.history)
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
             
make_nets() 
       
def read_predictions(prop_name_range = get_keys(), ws_range = range(2, 21), n_layer_range = range(2, 21), rmse_prop = []):
    for prop_name in prop_name_range:  
        ids_train = load_object("train_net/" + prop_name + "/ids/train/ids_to_cluster_train_" + prop_name) 
        ids_val = load_object("train_net/" + prop_name + "/ids/val/ids_to_cluster_val_" + prop_name) 
        ids_test = load_object("train_net/" + prop_name + "/ids/test/ids_to_cluster_test_" + prop_name) 
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
        nonzero = []
        for window_size in ws_range:
            ytrain = load_object("train_net/" + str(window_size) + "/" + prop_name + "/data_reshaped/trainY_" + str(window_size) + "_" + prop_name)
            yval = load_object("train_net/" + str(window_size) + "/" + prop_name + "/data_reshaped/valY_" + str(window_size) + "_" + prop_name) 
            ytest = load_object("train_net/" + str(window_size) + "/" + prop_name + "/data_reshaped/testY_" + str(window_size) + "_" + prop_name) 
            for n_layers in n_layer_range:
                predict_train = load_object("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/predictions/train_predict_" + str(window_size) + "_" + str(n_layers) + "_" + prop_name)
                predict_val = load_object("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/predictions/val_predict_" + str(window_size) + "_" + str(n_layers) + "_" + prop_name)  
                predict_test = load_object("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/predictions/test_predict_" + str(window_size) + "_" + str(n_layers) + "_" + prop_name)
                #if max(predict_train) == 0 or max(predict_val) == 0 or max(predict_test) == 0:
                    #print(prop_name, window_size, n_layers)
                    #print(min(ytrain), max(ytrain), min(predict_train), max(predict_train))
                    #print(min(yval), max(yval), min(predict_val), max(predict_val))
                    #print(min(ytest), max(ytest), min(predict_test), max(predict_test))
                if not max(predict_train) == 0 and not max(predict_val) == 0 and not max(predict_test) == 0:
                    nonzero.append([window_size, n_layers])
        print(prop_name, len(nonzero))
        
        if len(nonzero) == 0:
            nonzero = []
            rmse_values = []
            for window_size in range(2, 21):
                for n_layers in range(2, 21):
                    predict_train = load_object("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/predictions/train_predict_" + str(window_size) + "_" + str(n_layers) + "_" + prop_name)
                    predict_val = load_object("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/predictions/val_predict_" + str(window_size) + "_" + str(n_layers) + "_" + prop_name)  
                    predict_test = load_object("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/predictions/test_predict_" + str(window_size) + "_" + str(n_layers) + "_" + prop_name)
                    if not max(predict_train) == 0 and not max(predict_val) == 0 and not max(predict_test) == 0:
                        nonzero.append([window_size, n_layers])
                        rmse_values.append(rmse_prop[window_size][n_layers - 2])
            print(prop_name, len(nonzero)) 
            if len(nonzero) > 0:
                print(nonzero[np.argmin(rmse_values)])
                print(min(rmse_values))
            else:
                print("Error", prop_name)

def read_nets(): 
    rmse_train = dict()
    rmse_val = dict()
    rmse_test = dict()

    data_to_cluster_train = dict()
    data_to_cluster_val = dict()
    data_to_cluster_test = dict()

    for prop_name in get_keys():
        rmse_train[prop_name] = dict()
        rmse_val[prop_name] = dict()
        rmse_test[prop_name] = dict()  
        
        data_to_cluster_train[prop_name] = load_object("train_net/" + prop_name + "/data/train/data_to_cluster_train_" + prop_name)
        data_to_cluster_val[prop_name] = load_object("train_net/" + prop_name + "/data/val/data_to_cluster_val_" + prop_name)
        data_to_cluster_test[prop_name] = load_object("train_net/" + prop_name + "/data/test/data_to_cluster_test_" + prop_name)

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
            rmse_train[prop_name][window_size] = []
            rmse_val[prop_name][window_size] = []
            rmse_test[prop_name][window_size] = [] 

            ytrain = load_object("train_net/" + str(window_size) + "/" + prop_name + "/data_reshaped/trainY_" + str(window_size) + "_" + prop_name)
            yval = load_object("train_net/" + str(window_size) + "/" + prop_name + "/data_reshaped/valY_" + str(window_size) + "_" + prop_name) 
            ytest = load_object("train_net/" + str(window_size) + "/" + prop_name + "/data_reshaped/testY_" + str(window_size) + "_" + prop_name) 

            for n_layers in range(2, 21):
                #print(prop_name, window_size, n_layers)
                predict_train = load_object("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/predictions/train_predict_" + str(window_size) + "_" + str(n_layers) + "_" + prop_name)
                predict_val = load_object("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/predictions/val_predict_" + str(window_size) + "_" + str(n_layers) + "_" + prop_name)  
                predict_test = load_object("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/predictions/test_predict_" + str(window_size) + "_" + str(n_layers) + "_" + prop_name)  
                
                train_rmse, val_rmse, test_rmse = print_error(ytrain, yval,  ytest, predict_train, predict_val, predict_test, str(window_size) + "_" + str(n_layers) + "_" + prop_name, range_val)
                rmse_train[prop_name][window_size].append(train_rmse / range_val)
                rmse_val[prop_name][window_size].append(val_rmse / range_val)
                rmse_test[prop_name][window_size].append(test_rmse / range_val)
                
                #plot_predict(predict_train, predict_val, predict_test, str(window_size) + "_" + str(n_layers) + "_" + prop_name) 
                #plot_actual(ytrain, yval, ytest, str(window_size) + "_" + str(n_layers) + "_" + prop_name)
                #plot_result(ytrain, yval, ytest, predict_train, predict_val, predict_test, str(window_size) + "_" + str(n_layers) + "_" + prop_name)

    rcs = random_colors(len(range(2, 21)))
    for prop_name in get_keys():
        min_rmse_all = []
        min_rmse_all_pos = []
        plt.title(prop_name)
        for window_size in range(2, 21): 
            min_rmse_all.append(min(rmse_val[prop_name][window_size]))
            min_rmse_all_pos.append(np.argmin(rmse_val[prop_name][window_size]) + 2)
            plt.plot(range(2, 21), rmse_val[prop_name][window_size], label = window_size, color = rcs[window_size - 2])
            plt.scatter(np.argmin(rmse_val[prop_name][window_size]) + 2, rmse_val[prop_name][window_size][np.argmin(rmse_val[prop_name][window_size])], color = rcs[window_size - 2])
        plt.legend()
        #plt.show()
        plt.close()
        print(prop_name, min(min_rmse_all), np.argmin(min_rmse_all) + 2, min_rmse_all_pos[np.argmin(min_rmse_all)])
        read_predictions([prop_name], [np.argmin(min_rmse_all) + 2], [min_rmse_all_pos[np.argmin(min_rmse_all)]], rmse_val[prop_name])
        #read_predictions([prop_name])

read_nets()
        
read_predictions()
        
def read_model_type(window_size, n_layers, prop_name):
    hist = load_object("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/model/history_" + str(window_size) + "_" + str(n_layers) + "_" + prop_name)
    model_obj = load_model("train_net/" + str(window_size) + "/" + str(n_layers) + "/" + prop_name + "/model/demo_model_" + str(window_size) + "_" + str(n_layers) + "_" + prop_name + ".h5")
    print(hist["loss"])
    for layer in model_obj.layers:
        print(layer.__class__.__name__)

read_model_type(2, 2, "ysgn")