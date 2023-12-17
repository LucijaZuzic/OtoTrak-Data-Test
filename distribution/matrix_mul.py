import numpy as np
def matirx_res(nsteps, beginprob, probs):
    probco = [x for x in beginprob]
    probso = [[y for y in x] for x in probs]
    probc = beginprob
    for i in range(nsteps):
        probc = np.dot(probc, probs)
        print(probc)
    for i in range(nsteps):
        print(probs)
        probss = np.dot(probco, probs)
        print(probss)
        probs = np.dot(probs, probso)
#(3, [0, 1], [[0.75, 0.25],[0.25, 0.75]])
#matirx_res(3, [1, 0], [[0.75, 0.25],[0.25, 0.75]])
#matirx_res(3, [0, 1], [[0.9624, 0.0376],[0.0431, 0.9569]])
matirx_res(3, [1, 0], [[0.9624, 0.0376],[0.0431, 0.9569]])
