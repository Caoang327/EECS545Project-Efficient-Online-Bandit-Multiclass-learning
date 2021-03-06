import numpy as np
import scipy.io as sio
import scipy.sparse as sparse
X = sparse.load_npz("Reuters4_datasetX.npz")
Y = sparse.load_npz("Reuters4_datasetY.npz")
Y = Y + np.zeros(Y.shape)
Y = np.array(Y)
Y = Y.flatten()
def predict_label(W,x):
    out = np.dot(W,x)
    return np.argmax(out)[0]+1
def random_sample(P,p):
    P_accu  = 0
    index = 0
    for i in range(P.shape[0]):
        P_accu = P_accu + P[i,0]
        if P_accu > p:
            index = i+1
            break
    return index
n = 200000 # number of data
k = 4
d = X.shape[0]

print_fre = 5000
gamma_list = [1,0.5, 0.1, 0.05, 0.01, 0.005, 0.001, 0.0005, 0.0001]
gamma_performance = np.zeros([len(gamma_list)])
best_accuracy = 0
best_gamma = 0
for gamma_index in range(len(gamma_list)):
    gamma = gamma_list[gamma_index]
    correct = 0
    W = np.zeros([k, d])
    U = W
    np.random.seed(0)
    counter = 0
    for i in range(n):
        counter = counter + 1
        x = X[:, i]
        x = np.array(x + np.zeros(x.shape))
        x = x.reshape(-1, 1)
        y = int(Y[i])
        y_hat = predict_label(W,x)
        P = np.zeros([k,1])
        P[y_hat-1,0]=1
        P = P*(1-gamma)+gamma/k
        random_p = np.random.random()
        y_slide = random_sample(P,random_p)
        if y_slide == y:
            flag = 1
            correct = correct+1
        else:
            flag = 0
        for j in range(W.shape[0]):
            r = j+1
            coe = (flag*(y_slide == r)*1/P[j,0] - 1*(y_hat == r))
            U[j,:] = coe*x.flatten()
        W = W + U
        if counter%print_fre ==1:
            print(gamma)
            print(counter)
    gamma_performance[gamma_index] = correct/(i+1)
    if correct/(i+1) >= best_accuracy:
        best_accuracy = correct/(i+1)
        best_gamma = gamma
print('The best gamma is ')
print(best_gamma)
file_name = 'Banditron_Reuster_find_gamma.mat'
sio.savemat(file_name,{'performance':gamma_performance})


gamma = best_gamma
correct = 0
W = np.zeros([k,d])
U = W
np.random.seed(0)
counter = 0
accu = np.zeros([X.shape[1],1])
print_fre = 5000
for i in range(X.shape[1]):
    counter = counter + 1
    x = X[:, i]
    x = np.array(x + np.zeros(x.shape))
    x = x.reshape(-1, 1)
    y = int(Y[i])
    y_hat = predict_label(W,x)
    P = np.zeros([k,1])
    P[y_hat-1,0]=1
    P = P*(1-gamma)+gamma/k
    random_p = np.random.random()
    y_slide = random_sample(P,random_p)
    if y_slide == y:
        flag = 1
        correct = correct+1
    else:
        flag = 0
    for j in range(W.shape[0]):
        r = j+1
        coe = (flag*(y_slide == r)*1/P[j,0] - 1*(y_hat == r))
        U[j,:] = coe*x.flatten()
    W = W + U
    accu[i,0] = correct*1.0/counter
    if counter%print_fre ==1:
        print(correct*1.0/counter)
file_name = 'Banditron_accu_Reuster_g_'+str(gamma)+'.mat'
sio.savemat(file_name,{'accu':accu})