from utilities import *

def random_sample_of_fourier(files_in_cluster, nrow, ncol, filename):
    print(filename)
    for cluster in files_in_cluster:
        if len(files_in_cluster[cluster]) > 0:
            print(cluster, len(files_in_cluster[cluster]))
            if nrow * ncol > len(files_in_cluster[cluster]):
                ncol = int(np.sqrt(len(files_in_cluster[cluster])))
                nrow = ncol
            indexes = set([x for x in range(len(files_in_cluster[cluster]))])
            while len(indexes) > nrow * ncol:
                index_remove = np.random.randint(0, len(files_in_cluster[cluster]))
                if index_remove in indexes:
                    indexes.remove(index_remove)
            long1 = []
            lat1 = []
            titles = []
            for index in indexes:
                name_file = files_in_cluster[cluster][index]["short_name"]
                name_file_long = name_file.replace("/", "/cleaned_csv/") 
                long, lat, time = load_traj_window_name(name_file_long, files_in_cluster[cluster][index]["start"], files_in_cluster[cluster][index]["window"])
                long, lat = preprocess_long_lat(long, lat) 
                long, lat = scale_long_lat(long, lat, 0.005, 0.005, True) 
                long1.append(long)
                lat1.append(lat)
                titles.append(filename + "_cluster_" + str(cluster) + name_file)
            if not os.path.isdir("all_fourier_clus/samples"):
                os.makedirs("all_fourier_clus/samples")
            composite_image_random_cluster(long1, lat1, titles, nrow, ncol, "all_fourier_clus/samples/" + filename + "_cluster_" + str(cluster))
 
def read_fourier_clusters():
    for filename in os.listdir("all_fourier_clus/filenames"):
        random_sample_of_fourier(load_object("all_fourier_clus/filenames/" + filename), 1000, 1000, filename)

read_fourier_clusters()