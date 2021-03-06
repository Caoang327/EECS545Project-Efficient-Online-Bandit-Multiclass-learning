import numpy as np
from scipy import sparse
import scipy.io as sio

'''
Second Order Banditron Algorithm
Diagonal version
'''
X = sparse.load_npz("Reuters4_datasetX.npz")
Y = sparse.load_npz("Reuters4_datasetY.npz")
Y = Y + np.zeros(Y.shape)
y = np.array(Y)
y = y.flatten()
d = X.shape[0]  # number of features
K = 4  # number of classes

# initialization
a = 1  # regularization parameter
gamma = 0.01  # exploration parameter

##n = len(y)  # number of data
n = 200000
T = n  # number of rounds
# SOBA algorithm
gamma_list = [1,0.5, 0.1, 0.05, 0.01, 0.005, 0.001, 0.0005, 0.0001]
gamma_performance = np.zeros([len(gamma_list)])
best_accuracy = 0
best_gamma = 0
print_fre = 5000
for gamma_index in range(len(gamma_list)):
    W = np.zeros([K, d])
    A = a * np.ones([K * d])
    theta = np.zeros([K * d])
    E = np.eye(K)
    cumulative_margin = 0
    z = np.zeros([K * d])
    g = np.zeros([K * d])
    correct = 0
    gamma = gamma_list[gamma_index]
    for t in range(T):
        x = X[:,t]
        x = np.array(x + np.zeros(x.shape))
        x = x.flatten()
        Wx = W.dot(x)
        yhat = np.argmax(Wx) + 1
        p = (1-gamma) * E[:, yhat-1] + gamma / K * np.ones([K])
        rand_num = np.random.random()
        for i in range(K):
            if sum(p[:i+1]) >= rand_num:
                ytilde = i+1
                break
        nt = 0
        if ytilde == y[t]:
            correct += 1
            Wx_bar = np.zeros([K-1])
            Wx_bar[:ytilde-1] = Wx[:ytilde-1]
            Wx_bar[ytilde-1:] = Wx[ytilde:]
            ybar = np.argmax(Wx)+1
            g = 1 / p[ytilde-1] * np.kron(E[:, ybar-1]-E[:, ytilde-1], x)
            z = np.sqrt(p[ytilde-1]) * g
            m = (sum(W.reshape(-1, 1)*z.reshape(-1, 1))**2 + 2*sum(W.reshape(-1, 1)*g.reshape(-1, 1))) / (1 + sum(z*z/A))
            if cumulative_margin+m >= 0:
                nt = 1
            cumulative_margin += nt*m
        A += nt*z*z
        theta -= nt*g
        W = (theta/A).reshape(K, d)
        if t%print_fre == 0:
            print(t)
            print(correct/(t+1))
file_name = 'SOBA_accu_Reuters4_g_'+str(gamma)+'.mat'
sio.savemat(file_name,{'accu':accu})


n = len(y)  # number of data
T = n  # number of rounds
W = np.zeros([K, d])
A = a * np.ones([K*d])
theta = np.zeros([K*d])
E = np.eye(K)
cumulative_margin = 0
z = np.zeros([K*d])
g = np.zeros([K*d])
correct = 0
print_fre = 10
accu = np.zeros([T])
# SOBA algorithm
for t in range(T):
    x = X[:,t]
    x = np.array(x + np.zeros(x.shape))
    x = x.flatten()
    Wx = W.dot(x)
    yhat = np.argmax(Wx) + 1
    p = (1-gamma) * E[:, yhat-1] + gamma / K * np.ones([K])
    rand_num = np.random.random()
    for i in range(K):
        if sum(p[:i+1]) >= rand_num:
            ytilde = i+1
            break
    nt = 0
    if ytilde == y[t]:
        correct += 1
        Wx_bar = np.zeros([K-1])
        Wx_bar[:ytilde-1] = Wx[:ytilde-1]
        Wx_bar[ytilde-1:] = Wx[ytilde:]
        ybar = np.argmax(Wx)+1
        g = 1 / p[ytilde-1] * np.kron(E[:, ybar-1]-E[:, ytilde-1], x)
        z = np.sqrt(p[ytilde-1]) * g
        m = (sum(W.reshape(-1, 1)*z.reshape(-1, 1))**2 + 2*sum(W.reshape(-1, 1)*g.reshape(-1, 1))) / (1 + sum(z*z/A))
        if cumulative_margin+m >= 0:
            nt = 1
        cumulative_margin += nt*m
    A += nt*z*z
    theta -= nt*g
    W = (theta/A).reshape(K, d)
    accu[t] = correct / (t+1)
    if t%print_fre == 0:
        print(t)
        print(correct/(t+1))
file_name = 'SOBA_accu_Reuters4_g_'+str(gamma)+'.mat'
sio.savemat(file_name,{'accu':accu})