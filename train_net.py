from utilities import *

from keras.models import Sequential
from keras.layers import Dense, SimpleRNN

from sklearn.metrics import mean_squared_error

all_subdirs = os.listdir()

def get_keys():  

    data_to_cluster_train = dict()
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

    data_to_cluster_train = dict()
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

    data_to_cluster_test = dict()
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

            if some_file in train_rides: 
                for i in range(len(accelers_trajs)):  
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
            if some_file in test_rides: 
                for i in range(len(accelers_trajs)):   
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
    for k in data_to_cluster_train:
        data_to_cluster_train[k] = np.array(data_to_cluster_train[k])
    for k in data_to_cluster_test:
        data_to_cluster_test[k] = np.array(data_to_cluster_test[k])
    return data_to_cluster_train, data_to_cluster_test

def get_XY(dat, time_steps, num_props): 
    Y_ind = np.arange(time_steps, len(dat), time_steps)
    print(time_steps)
    print(Y_ind)
    Y = dat[Y_ind] 
    rows_x = len(Y)
    print(rows_x)
    X = dat[range(time_steps*rows_x)]
    X = np.reshape(X, (rows_x, time_steps, num_props))   
    print(np.shape(X), np.shape(Y)) 
    return X, Y

def print_error(trainY, testY, train_predict, test_predict, title, range_val):  
    train_rmse = math.sqrt(mean_squared_error(trainY, train_predict))
    test_rmse = math.sqrt(mean_squared_error(testY, test_predict)) 
    print(title, 'Train RMSE: %.3f RMSE' % (train_rmse / range_val))
    print(title, 'Test RMSE: %.3f RMSE' % (test_rmse / range_val))    
    if not os.path.isdir("train_net/" + title + "/predictions"):
        os.makedirs("train_net/" + title + "/predictions")
    save_object("train_net/" + title + "/predictions/trainY_" + title, trainY)
    save_object("train_net/" + title + "/predictions/testY_" + title, testY)
    save_object("train_net/" + title + "/predictions/train_predict_" + title, train_predict) 
    save_object("train_net/" + title + "/predictions/test_predict_" + title, test_predict)
 
def create_RNN(hidden_units, dense_units, input_shape, activation):
    model = Sequential()
    model.add(SimpleRNN(hidden_units, input_shape=input_shape, 
                        activation=activation[0]))
    model.add(Dense(units=dense_units, activation=activation[1]))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

def plot_result(trainY, testY, train_predict, test_predict, title):
    actual = np.append(trainY, testY)
    predictions = np.append(train_predict, test_predict)
    rows = len(actual)
    plt.figure(figsize=(15, 6), dpi=80)
    plt.plot(range(rows), actual)
    plt.plot(range(rows), predictions)
    plt.axvline(x=len(trainY), color='r')
    plt.legend(['Actual', 'Predictions'])
    plt.xlabel('Observation number after given time steps')
    plt.ylabel(title)
    plt.title('Actual and Predicted Values. The Red Line Separates The Training And Test Examples') 
    if not os.path.isdir("train_net/" + title + "/predictions"):
        os.makedirs("train_net/" + title + "/predictions")
    plt.savefig("train_net/" + title + "/predictions/" + title + ".png", bbox_inches = "tight")
    plt.close()
    
def plot_actual(trainY, testY, title):
    actual = np.append(trainY, testY) 
    rows = len(actual)
    plt.figure(figsize=(15, 6), dpi=80)
    plt.plot(range(rows), actual) 
    plt.axvline(x=len(trainY), color='r')
    plt.legend(['Actual'])
    plt.xlabel('Observation number after given time steps')
    plt.ylabel(title)
    plt.title('Actual Values. The Red Line Separates The Training And Test Examples') 
    if not os.path.isdir("train_net/" + title + "/predictions"):
        os.makedirs("train_net/" + title + "/predictions")
    plt.savefig("train_net/" + title + "/predictions/" + title + "_actual.png", bbox_inches = "tight")
    plt.close()

def plot_predict(trainY, testY, title):
    actual = np.append(trainY, testY) 
    rows = len(actual)
    plt.figure(figsize=(15, 6), dpi=80)
    plt.plot(range(rows), actual) 
    plt.axvline(x=len(trainY), color='r')
    plt.legend(['Predictions'])
    plt.xlabel('Observation number after given time steps')
    plt.ylabel(title)
    plt.title('Predicted Values. The Red Line Separates The Training And Test Examples') 
    if not os.path.isdir("train_net/" + title + "/predictions"):
        os.makedirs("train_net/" + title + "/predictions")
    plt.savefig("train_net/" + title + "/predictions/" + title + "_predicted.png", bbox_inches = "tight")
    plt.close()

def make_nets():
    window_size = 20 
    data_to_cluster_train, data_to_cluster_test = make_dataset_train()
    num_props = 1
    for prop_name in data_to_cluster_train:
        if not os.path.isdir("train_net/" + prop_name + "/model"):
            os.makedirs("train_net/" + prop_name + "/model")
        min_val = min(min(data_to_cluster_train[prop_name]), min(data_to_cluster_test[prop_name]))
        max_val = max(max(data_to_cluster_train[prop_name]), max(data_to_cluster_test[prop_name]))
        range_val = max_val - min_val
        xtrain, ytrain = get_XY(data_to_cluster_train[prop_name], window_size, num_props)
        xtest, ytest = get_XY(data_to_cluster_test[prop_name], window_size, num_props)
        demo_model = create_RNN(2, 1, (window_size, num_props), activation=['linear', 'linear'])   
        save_object("train_net/" + prop_name + "/model/demo_model_" + prop_name, demo_model)
        history = demo_model.fit(xtrain, ytrain, verbose = 1)  
        save_object("train_net/" + prop_name + "/model/history_" + prop_name, history)
        predict_train = demo_model.predict(xtrain)
        predict_test = demo_model.predict(xtest)
        print_error(ytrain, ytest, predict_train, predict_test, prop_name, range_val)
        plot_result(ytrain, ytest, predict_train, predict_test, prop_name)

def make_net_all():
    window_size = 20 
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

#make_nets()
make_net_all()
        
def read_nets(): 
    for prop_name in get_keys():    
        ytrain = load_object("train_net/" + prop_name + "/predictions/trainY_" + prop_name)
        ytest = load_object("train_net/" + prop_name + "/predictions/testY_" + prop_name)
        predict_train = load_object("train_net/" + prop_name + "/predictions/train_predict_" + prop_name)
        predict_test = load_object("train_net/" + prop_name + "/predictions/test_predict_" + prop_name)  
        plot_predict(predict_train, predict_test, prop_name) 
        plot_actual(ytrain, ytest, prop_name)

read_nets()