import numpy as np
import matplotlib.pyplot as plt
x = [v for v in np.arange(0, 2 * np.pi, 0.01)]
f = [np.cos(v / np.pi / 2) * v * 4 + 23 for v in x]
g = [np.cos(v * 0.87) * v * 3 + 23 for v in x]
while f[-1] > g[-1]:
    v = x[-1] + 0.01
    x.append(v)
    f.append(np.cos(v / np.pi / 2) * v * 4 + 23)
    g.append(np.cos(v * 0.87) * v * 3 + 23)
l1 = [i for i in np.arange(0, f[0] + 0.001, 0.001)]
x1 = [0 for i in np.arange(0, f[0] + 0.001, 0.001)]
l2 = [i for i in np.arange(0, f[-1] + 0.001, 0.001)]
x2 = [x[-1] for i in np.arange(0, f[-1]  + 0.001, 0.001)]
x3 = [v for v in np.arange(x[0] - 1, x[-1] + 1 + 0.001, 0.001)]
s = [0 for v in x3]
df = [f[i] - g[i] for i in range(len(x))]
plt.subplot(1, 2, 1)
plt.rcParams['font.family'] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.axis('off')
plt.plot(x, f, label = "f", c = "r")
ix = int(len(x) / 4)
plt.text(x[ix], f[ix] + 2, '$f$', size=15, color='r')
plt.plot(x, g, label = "g", c = "b")
ix = int(g.index(min(g))) - 30  
plt.text(x[ix], g[ix] - 5, '$g$', size=15, color='b')
plt.text(x[ix], g[ix] + 5, '$A_{1}$', size=15, color='k')
plt.plot(x3, s, c = "k")
plt.plot(x1, l1, c = "k") 
plt.plot(x2, l2, c = "k")
plt.plot() 
plt.subplot(1, 2, 2) 
plt.axis('off')
plt.plot(x, df, c = "magenta")
plt.ylim(-1.71, max(max(f), max(g)))
ix = int(df.index(max(df))) - 30  
plt.text(x[ix], df[ix] / 2, '$A_{2}$', size=15, color='k')
plt.text(x[ix], df[ix] + 5, '$f-g$', size=15, color='magenta')
plt.plot(x3, s, c = "k")
plt.show()
plt.close()
