from utilities import *
from sklearn.manifold import TSNE

def save_complex():
    all_feats_fourier_scaled_to_max = pd.read_csv("all_feats_fourier/all_feats_fourier_scaled_to_max.csv")
    header_of_file = ["window_size", "vehicle", "ride", "start"]

    longitude_train_complex = []
    latitude_train_complex = []
    times_train_complex = []
    wtrain = []
    vtrain = []
    rtrain = []
    strain = []

    longitude_test_complex = []
    latitude_test_complex = []
    times_test_complex = []
    wtest = []
    vtest = []
    rtest = []
    stest = []

    longitude_complex = []
    latitude_complex = []

    longitude_test_complex_dict = dict()
    latitude_test_complex_dict = dict()
    longitude_train_complex_dict = dict()
    latitude_train_complex_dict = dict()
    longitude_complex_dict = dict()
    latitude_complex_dict = dict()

    for index in range(len(all_feats_fourier_scaled_to_max["window_size"])):
        subdir_name = all_feats_fourier_scaled_to_max["vehicle"][index]
        filename = "events_" + str(all_feats_fourier_scaled_to_max["ride"][index]) + ".csv" 
        x = all_feats_fourier_scaled_to_max["start"][index]
        ws = all_feats_fourier_scaled_to_max["window_size"][index]
        file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + filename)
        times = list(file_with_ride["time"])  
        times_tmp = times[x:x + ws]  

        if ws not in longitude_complex_dict:
            longitude_complex_dict[ws] = dict()
        if subdir_name not in longitude_complex_dict[ws]:
            longitude_complex_dict[ws][subdir_name] = dict()
        if filename not in longitude_complex_dict[ws][subdir_name]:
            longitude_complex_dict[ws][subdir_name][filename] = dict()
        if x not in longitude_complex_dict[ws][subdir_name][filename]:
            longitude_complex_dict[ws][subdir_name][filename][x] = dict()
        longitude_complex_dict[ws][subdir_name][filename][x]["all"] = []
            
        if ws not in latitude_complex_dict:
            latitude_complex_dict[ws] = dict()
        if subdir_name not in latitude_complex_dict[ws]:
            latitude_complex_dict[ws][subdir_name] = dict()
        if filename not in latitude_complex_dict[ws][subdir_name]:
            latitude_complex_dict[ws][subdir_name][filename] = dict()
        if x not in latitude_complex_dict[ws][subdir_name][filename]:
            latitude_complex_dict[ws][subdir_name][filename][x] = dict()
        latitude_complex_dict[ws][subdir_name][filename][x]["all"] = []
        
        train_rides = set()
        if os.path.isfile(subdir_name + "/train_rides"):
            train_rides = load_object(subdir_name + "/train_rides") 
            
        test_rides = set()
        if os.path.isfile(subdir_name + "/test_rides"):
            test_rides = load_object(subdir_name + "/test_rides")

        longitude_complex.append([])
        latitude_complex.append([])

        if filename in train_rides:
            times_train_complex.append(times_tmp)
            wtrain.append(ws)
            vtrain.append(subdir_name)
            rtrain.append(filename)
            strain.append(x)
            longitude_train_complex.append([])
            latitude_train_complex.append([])
            
            if ws not in longitude_train_complex_dict:
                longitude_train_complex_dict[ws] = dict()
            if subdir_name not in longitude_train_complex_dict[ws]:
                longitude_train_complex_dict[ws][subdir_name] = dict()
            if filename not in longitude_train_complex_dict[ws][subdir_name]:
                longitude_train_complex_dict[ws][subdir_name][filename] = dict()
            if x not in longitude_train_complex_dict[ws][subdir_name][filename]:
                longitude_train_complex_dict[ws][subdir_name][filename][x] = dict()
            longitude_train_complex_dict[ws][subdir_name][filename][x]["all"] = []
                
            if ws not in latitude_train_complex_dict:
                latitude_train_complex_dict[ws] = dict()
            if subdir_name not in latitude_train_complex_dict[ws]:
                latitude_train_complex_dict[ws][subdir_name] = dict()
            if filename not in latitude_train_complex_dict[ws][subdir_name]:
                latitude_train_complex_dict[ws][subdir_name][filename] = dict()
            if x not in latitude_train_complex_dict[ws][subdir_name][filename]:
                latitude_train_complex_dict[ws][subdir_name][filename][x] = dict()
            latitude_train_complex_dict[ws][subdir_name][filename][x]["all"] = []
            
        if filename in test_rides:
            times_test_complex.append(times_tmp)
            wtest.append(ws)
            vtest.append(subdir_name)
            rtest.append(filename)
            stest.append(x)
            longitude_test_complex.append([])
            latitude_test_complex.append([])

            if ws not in longitude_test_complex_dict:
                longitude_test_complex_dict[ws] = dict()
            if subdir_name not in longitude_test_complex_dict[ws]:
                longitude_test_complex_dict[ws][subdir_name] = dict()
            if filename not in longitude_test_complex_dict[ws][subdir_name]:
                longitude_test_complex_dict[ws][subdir_name][filename] = dict()
            if x not in longitude_test_complex_dict[ws][subdir_name][filename]:
                longitude_test_complex_dict[ws][subdir_name][filename][x] = dict()
            longitude_test_complex_dict[ws][subdir_name][filename][x]["all"] = []
                
            if ws not in latitude_test_complex_dict:
                latitude_test_complex_dict[ws] = dict()
            if subdir_name not in latitude_test_complex_dict[ws]:
                latitude_test_complex_dict[ws][subdir_name] = dict()
            if filename not in latitude_test_complex_dict[ws][subdir_name]:
                latitude_test_complex_dict[ws][subdir_name][filename] = dict()
            if x not in latitude_test_complex_dict[ws][subdir_name][filename]:
                latitude_test_complex_dict[ws][subdir_name][filename][x] = dict()
            latitude_test_complex_dict[ws][subdir_name][filename][x]["all"] = []

        for feat in all_feats_fourier_scaled_to_max.head():
            if feat in header_of_file:
                continue
            complex_number = complex(all_feats_fourier_scaled_to_max[feat][index])
            
            if "long" in feat:
                longitude_complex[-1].append(complex_number)
                longitude_complex_dict[ws][subdir_name][filename][x][feat] = complex_number
                longitude_complex_dict[ws][subdir_name][filename][x]["all"].append(complex_number)
            if "lat" in feat:
                latitude_complex[-1].append(complex_number) 
                latitude_complex_dict[ws][subdir_name][filename][x][feat] = complex_number
                latitude_complex_dict[ws][subdir_name][filename][x]["all"].append(complex_number)

            if filename in train_rides:
                if "long" in feat:
                    longitude_train_complex[-1].append(complex_number)
                    longitude_train_complex_dict[ws][subdir_name][filename][x][feat] = complex_number
                    longitude_train_complex_dict[ws][subdir_name][filename][x]["all"].append(complex_number)
                if "lat" in feat:
                    latitude_train_complex[-1].append(complex_number) 
                    latitude_train_complex_dict[ws][subdir_name][filename][x][feat] = complex_number
                    latitude_train_complex_dict[ws][subdir_name][filename][x]["all"].append(complex_number)

            if filename in test_rides:
                if "long" in feat:
                    longitude_test_complex[-1].append(complex_number)
                    longitude_test_complex_dict[ws][subdir_name][filename][x][feat] = complex_number
                    longitude_test_complex_dict[ws][subdir_name][filename][x]["all"].append(complex_number)
                if "lat" in feat:
                    latitude_test_complex[-1].append(complex_number)
                    latitude_test_complex_dict[ws][subdir_name][filename][x][feat] = complex_number
                    latitude_test_complex_dict[ws][subdir_name][filename][x]["all"].append(complex_number)

    if not os.path.isdir("complex"):
        os.makedirs("complex")

    save_object("complex/latitude_complex_dict", latitude_complex_dict) 
    save_object("complex/longitude_complex_dict", longitude_complex_dict) 
    save_object("complex/latitude_complex", latitude_complex) 
    save_object("complex/longitude_complex", longitude_complex) 

    save_object("complex/latitude_test_complex_dict", latitude_test_complex_dict)
    save_object("complex/latitude_test_complex", latitude_test_complex)
    save_object("complex/longitude_test_complex_dict", longitude_test_complex_dict)
    save_object("complex/longitude_test_complex", longitude_test_complex) 

    save_object("complex/latitude_train_complex_dict", latitude_train_complex_dict)
    save_object("complex/latitude_train_complex", latitude_train_complex)
    save_object("complex/longitude_train_complex_dict", longitude_train_complex_dict)
    save_object("complex/longitude_train_complex", longitude_train_complex) 

longitude_test_complex = load_object("complex/longitude_test_complex") 
latitude_test_complex = load_object("complex/latitude_test_complex")
longitude_train_complex = load_object("complex/longitude_train_complex") 
latitude_train_complex = load_object("complex/latitude_train_complex")

def compare(signal_test_y, name):
 
    fft_sig = np.fft.fft(signal_test_y)
    #fft_sig_real = [fft_val.real for fft_val in fft_sig]
    #fft_sig_imag = [fft_val.imag for fft_val in fft_sig]

    results_x_test = []
    results_y_test = []  
    results_xy_test = []  
    for i, xfft in enumerate(longitude_test_complex):
        yfft = latitude_test_complex[i]
        rx = sum([abs(xfft[i] * fft_sig[i]) for i in range(len(xfft))])
        ry = sum([abs(yfft[i] * fft_sig[i]) for i in range(len(yfft))])
        results_x_test.append(rx)
        results_y_test.append(ry) 
        results_xy_test.append([rx, ry]) 

    results_x_train = []
    results_y_train = []  
    results_xy_train = []  
    for i, xfft in enumerate(longitude_train_complex):
        yfft = latitude_train_complex[i]
        rx = sum([abs(xfft[i] * fft_sig[i]) for i in range(len(xfft))])
        ry = sum([abs(yfft[i] * fft_sig[i]) for i in range(len(yfft))])
        results_x_train.append(rx)
        results_y_train.append(ry) 
        results_xy_train.append([rx, ry]) 

    plt.title(name)
    plt.scatter(results_x_train, results_y_train)
    plt.show()
    plt.close()

sample_names = dict() 
window_size = 20  
scale = 0.005

#down_edge_y = [0 * scale for x in range(window_size)] 
#sample_names["down"] = down_edge_y 
   
diagonal_edge_y = [x * 1 / (window_size - 1) * scale for x in range(window_size)] 
sample_names["diagonal"] = diagonal_edge_y 
   
#down_circle_y = [np.sqrt(- x * (x - 1)) * scale for x in range(window_size)] 
#sample_names["down_circle"] = down_circle_y 
   
sin_y = [np.sin(x * np.pi * 2) * scale for x in range(window_size)]  
sample_names["sin"] = sin_y

sin_reverse_y = [np.sin(x * np.pi * 2 + np.pi)* scale for x in range(window_size)] 
sample_names["sin_reverse"] = sin_reverse_y
 
sin_half_y = [np.sin(x * np.pi) * scale for x in range(window_size)] 
sample_names["sin_half"] = sin_half_y
 
sin_half_reverse_y = [np.sin(x * np.pi + np.pi)* scale for x in range(window_size)] 
sample_names["sin_half_reverse"] = sin_half_reverse_y
 
cos_y = [np.cos(x * np.pi * 2) * scale for x in range(window_size)] 
sample_names["cos"] = cos_y

cos_reverse_y = [np.cos(x * np.pi * 2 + np.pi) * scale for x in range(window_size)] 
sample_names["cos_reverse"] = cos_reverse_y
 
cos_half_y = [np.cos(x * np.pi)* scale for x in range(window_size)] 
sample_names["cos_half"] = cos_half_y
 
cos_half_reverse_y = [np.cos(x * np.pi + np.pi)* scale for x in range(window_size)] 
sample_names["cos_half_reverse"] = cos_half_reverse_y

for name in sample_names:
    compare(sample_names[name], name)