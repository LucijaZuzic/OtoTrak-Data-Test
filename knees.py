
from kneed import KneeLocator
from sklearn.neighbors import NearestNeighbors

def kneefind(NN, X_embedded):
	nbrs = NearestNeighbors(n_neighbors = NN).fit(X_embedded)
	distances, indices = nbrs.kneighbors(X_embedded)
	distance_desc = sorted(distances[:,NN-1], reverse=True)
	#plt.plot(list(range(1,len(distance_desc)+1)), distance_desc)
	#plt.show()
	#plt.close()
	kl = KneeLocator(list(range(1,len(distance_desc )+1)), distance_desc, curve = "convex", direction = "decreasing") 
	return kl.knee_y 