from utilities import *
 
window_size = 20
deg = 5
maxoffset = 0.005
step_size = window_size
#step_size = 1
max_trajs = 100
name_extension = "_window_" + str(window_size) + "_step_" + str(step_size) + "_segments_" + str(max_trajs)

all_subdirs = os.listdir() 
    
all_feats_trajs = dict()   
all_feats_trajs[window_size] = dict()

all_feats_scaled_trajs = dict()   
all_feats_scaled_trajs[window_size] = dict()

all_feats_scaled_to_max_trajs = dict()   
all_feats_scaled_to_max_trajs[window_size] = dict()
  
xvals = np.arange(0, 2 * np.pi, 10 ** -1)
yvals = [np.sin(xval) for xval in xvals]   
fftyvals = np.fft.fft(yvals)
ifftyvals = np.fft.ifft(fftyvals)
plt.subplot(1, 3, 1)
plt.title("original")
plt.plot(xvals, yvals)
plt.subplot(1, 3, 2)
plt.title("fft")
plt.plot(xvals, fftyvals)
plt.subplot(1, 3, 3)
plt.title("iftt")
plt.plot(xvals, ifftyvals)
plt.show()
fftfreqs = np.fft.fftfreq(len(yvals))
newfftyvals = [(fftyvals[i].real * np.cos(fftfreqs[i] * 2 * np.pi) - fftyvals[i].imag * np.sin(fftfreqs[i] * 2 * np.pi)) / len(yvals) for i in range(len(yvals))]
plt.subplot(1, 4, 1)
plt.title("fft")
plt.plot(xvals, fftyvals)
plt.subplot(1, 4, 2)
plt.title("Reconstruct ftt")
plt.plot(xvals, newfftyvals) 
newfftyvalsreal = [fftyvals[i].real * np.cos(fftfreqs[i] * 2 * np.pi) / len(yvals) for i in range(len(yvals))]
plt.subplot(1, 4, 3)
plt.title("Real ftt")
plt.plot(xvals, newfftyvalsreal) 
newfftyvalsimag = [- fftyvals[i].imag * np.sin(fftfreqs[i] * 2 * np.pi) / len(yvals) for i in range(len(yvals))]
plt.subplot(1, 4, 4)
plt.title("Imaginary fft")
plt.plot(xvals, newfftyvalsimag)
plt.show() 
plt.subplot(1, 3, 1)
plt.title("Reconstruct real")
sum_real = [0 for xval in xvals]
for i in range(len(fftfreqs)):
    ampl = fftyvals[i].real 
    if ampl == 0:
        continue
    freq = fftfreqs[i] 
    vals_plot = [ampl * np.cos(xval * freq * 2 * np.pi) / len(yvals) for xval in xvals]
    for j in range(len(xvals)):
        sum_real[j] += vals_plot[j]
    #plt.title(str(freq))
    plt.plot(xvals, vals_plot)
plt.plot(xvals, sum_real, label = "all")
plt.legend() 
plt.subplot(1, 3, 2)
plt.title("Reconstruct imaginary")
sum_im = [0 for xval in xvals]
for i in range(len(fftfreqs)):
    ampl = fftyvals[i].imag 
    if ampl == 0:
        continue
    freq = fftfreqs[i] 
    vals_plot = [- ampl * np.sin(xval * freq * 2 * np.pi) / len(yvals) for xval in xvals]
    for j in range(len(xvals)):
        sum_im[j] += vals_plot[j]
    #plt.title(str(freq))
    plt.plot(xvals, vals_plot)
plt.plot(xvals, sum_im, label = "all")
plt.legend() 
plt.subplot(1, 3, 3)
plt.title("Reconstruct all")
sum_all = [0 for xval in xvals]
for i in range(len(fftfreqs)):
    amplre = fftyvals[i].real 
    amplim = fftyvals[i].imag 
    freq = fftfreqs[i] 
    vals_plot = [(amplre * np.cos(xval * freq * 2 * np.pi) - amplim * np.sin(xval * freq * 2 * np.pi)) / len(yvals) for xval in xvals] 
    for j in range(len(xvals)):
        sum_all[j] += vals_plot[j]
    #plt.title(str(freq))
    plt.plot(xvals, vals_plot)
plt.plot(xvals, sum_all, label = "all")
plt.legend()
plt.show()  

#decompose_fft(xnnnn) 
for subdir_name in all_subdirs:

    trajs_in_dir = 0
    
    if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
        continue
      
    all_feats_trajs[window_size][subdir_name] = dict() 
    all_feats_scaled_trajs[window_size][subdir_name] = dict() 
    all_feats_scaled_to_max_trajs[window_size][subdir_name] = dict()  

    all_files = os.listdir(subdir_name + "/cleaned_csv/") 
    bad_rides_filenames = set()
    if os.path.isfile(subdir_name + "/bad_rides_filenames"):
        bad_rides_filenames = load_object(subdir_name + "/bad_rides_filenames")
    gap_rides_filenames = set()
    if os.path.isfile(subdir_name + "/gap_rides_filenames"):
        gap_rides_filenames = load_object(subdir_name + "/gap_rides_filenames")
        
    for some_file in all_files:  
        if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames:
            #print("Skipped ride", some_file)
            continue
        #print("Used ride", some_file)

        only_num_ride = some_file.replace(".csv", "").replace("events_", "")
        
        trajs_in_ride = 0
 
        all_feats_trajs[window_size][subdir_name][only_num_ride] = dict()
        all_feats_scaled_trajs[window_size][subdir_name][only_num_ride] = dict()
        all_feats_scaled_to_max_trajs[window_size][subdir_name][only_num_ride] = dict()  
    
        file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
        longitudes = list(file_with_ride["fields_longitude"])
        latitudes = list(file_with_ride["fields_latitude"]) 
        times = list(file_with_ride["time"])  
        flags_dict = dict() 
  
        for x in range(0, len(longitudes) - window_size + 1, step_size):
            longitudes_tmp = longitudes[x:x + window_size]
            latitudes_tmp = latitudes[x:x + window_size]
            times_tmp = times[x:x + window_size]  

            set_longs = set()
            set_lats = set()
            set_points = set()
            for tmp_long in longitudes_tmp:
                set_longs.add(tmp_long)
            for tmp_lat in latitudes_tmp:
                set_lats.add(tmp_lat)
            for some_index in range(len(latitudes_tmp)):
                set_points.add((latitudes_tmp[some_index], longitudes_tmp[some_index]))
                
            if len(set_lats) == 1 or len(set_longs) == 1:
                continue
            if len(set_points) < 3:
                continue
            
            longitudes_tmp_transform, latitudes_tmp_transform = preprocess_long_lat(longitudes_tmp, latitudes_tmp)
            
            longitudes_scaled, latitudes_scaled = scale_long_lat(longitudes_tmp_transform, latitudes_tmp_transform)
            
            longitudes_scaled_to_max, latitudes_scaled_to_max = scale_long_lat(longitudes_tmp_transform, latitudes_tmp_transform, xmax = maxoffset, ymax = maxoffset, keep_aspect_ratio = True)

            times_tmp_transform = transform_time(times_tmp)
 
            trajs_in_ride += 1
            trajs_in_dir += 1 
  
            long_sgn = set()
            for long_ind in range(len(longitudes_tmp_transform) - 1):
                long_sgn.add(longitudes_tmp_transform[long_ind + 1] > longitudes_tmp_transform[long_ind])
                if len(long_sgn) > 1:
                    break

            lat_sgn = set()
            for lat_ind in range(len(latitudes_tmp_transform) - 1):
                lat_sgn.add(latitudes_tmp_transform[lat_ind + 1] > latitudes_tmp_transform[lat_ind])
                if len(lat_sgn) > 1:
                    break

            x_poly, y_poly = get_poly_xt_yt(longitudes_tmp_transform, latitudes_tmp_transform, times_tmp_transform, deg)
            xy_poly = []
            if len(lat_sgn) == 1 and len(long_sgn) == 1:
                xy_poly = np.polyfit(longitudes_tmp_transform, latitudes_tmp_transform, deg)
                
            x_poly_scaled, y_poly_scaled = get_poly_xt_yt(longitudes_scaled, latitudes_scaled, times_tmp_transform, deg)
            xy_poly_scaled = []
            if len(lat_sgn) == 1 and len(long_sgn) == 1:
                xy_poly_scaled = np.polyfit(longitudes_scaled, latitudes_scaled, deg)

            x_poly_scaled_to_max, y_poly_scaled_to_max = get_poly_xt_yt(longitudes_scaled_to_max, latitudes_scaled_to_max, times_tmp_transform, deg)
            xy_poly_scaled_to_max = []
            if len(lat_sgn) == 1 and len(long_sgn) == 1:
                xy_poly_scaled_to_max = np.polyfit(longitudes_scaled_to_max, latitudes_scaled_to_max, deg)

            xt, yt, xn, yn, fftx, ffty = get_fft_xt_yt(longitudes_scaled_to_max, latitudes_scaled_to_max, times_tmp_transform, deg)
            #decompose_fft(xn)
            #decompose_fft(yn)
            plt.plot(times_tmp_transform, longitudes_scaled_to_max)
            plt.show()
            plt.plot(times_tmp_transform, np.fft.fft(longitudes_scaled_to_max))
            plt.show()
            plt.plot(times_tmp_transform, np.fft.ifft(np.fft.fft(longitudes_scaled_to_max)))
            plt.show()
            found_fft = True
            break
        if found_fft:
            break
    if found_fft:
        break 