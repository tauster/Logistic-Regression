import numpy as np
from utils import sigmoid

"""
Changes:
    - Finished logistic_predict()
    - Finished evaluate()
    - Finished logistic()
    - Finished logistic_per()
"""

def logistic_predict(weights, data):
    """
    Compute the probabilities predicted by the logistic classifier.

    Note: N is the number of examples and 
          M is the number of features per example.

    Inputs:
        weights:    (M+1) x 1 vector of weights, where the last element
                    corresponds to the bias (intercepts).
        data:       N x M data matrix where each row corresponds 
                    to one data point.
    Outputs:
        y:          :N x 1 vector of probabilities of being second class. This is the output of the classifier.
    """

    N, M = data.shape
    wI = weights[0:M]
    w0 = weights[M,0]
    w1N, w1M = wI.shape

    z1 = (np.dot(np.transpose(wI), np.transpose(data)))
    z = z1 + w0

    y = np.transpose((sigmoid(z)))

    return y


def evaluate(targets, y):
    """
    Compute evaluation metrics.
    Inputs:
        targets : N x 1 vector of targets.
        y       : N x 1 vector of probabilities.
    Outputs:
        ce           : (scalar) Cross entropy. CE(p, q) = E_p[-log q]. Here we want to compute CE(targets, y)
        frac_correct : (scalar) Fraction of inputs classified correctly.
    """
    
    preSum = np.multiply(targets, np.log(y))
    ce = -1*np.sum(preSum)

    fracCount = 0
    for i in range(len(targets)):
        if (targets[i] == 1) and (y[i] >= 0.5):
            fracCount += 1
        if (targets[i] == 0) and (y[i] < 0.5):
            fracCount += 1
        
    frac_correct = fracCount/float(len(targets))
    
    return ce, frac_correct


def logistic(weights, data, targets, hyperparameters):
    """
    Calculate negative log likelihood and its derivatives with respect to weights.
    Also return the predictions.

    Note: N is the number of examples and 
          M is the number of features per example.

    Inputs:
        weights:    (M+1) x 1 vector of weights, where the last element
                    corresponds to bias (intercepts).
        data:       N x M data matrix where each row corresponds 
                    to one data point.
        targets:    N x 1 vector of targets class probabilities.
        hyperparameters: The hyperparameters dictionary.

    Outputs:
        f:       The sum of the loss over all data points. This is the objective that we want to minimize.
        df:      (M+1) x 1 vector of accumulative derivative of f w.r.t. weights, i.e. don't need to average over number of sample
        y:       N x 1 vector of probabilities.
    """

    y = logistic_predict(weights, data)
    N, M = data.shape
    wI = weights[0:M]
    w0 = weights[M,0]

    if hyperparameters['weight_regularization'] is True:
        f, df = logistic_pen(weights, data, targets, hyperparameters)
    else:
        f1 = np.sum(np.multiply(targets, np.log(y)))
        f2 = np.sum(np.multiply((1 - targets), (np.log(1 - y))))
        f = (-1*f1) - f2
        
        ones = np.ones((N,1))
        data1 = np.column_stack((data, ones))
 
        df = np.dot(np.transpose(data1), (sigmoid(np.dot(data1, weights)) - targets))

    return f, df, y


def logistic_pen(weights, data, targets, hyperparameters):
    """
    Calculate negative log likelihood and its derivatives with respect to weights.
    Also return the predictions.

    Note: N is the number of examples and
          M is the number of features per example.

    Inputs:
        weights:    (M+1) x 1 vector of weights, where the last element
                    corresponds to bias (intercepts).
        data:       N x M data matrix where each row corresponds
                    to one data point.
        targets:    N x 1 vector of targets class probabilities.
        hyperparameters: The hyperparameters dictionary.

    Outputs:
        f:             The sum of the loss over all data points. This is the objective that we want to minimize.
        df:            (M+1) x 1 vector of accumulative derivative of f w.r.t. weights, i.e. don't need to average over number of sample
    """
    
    N, M = data.shape
    wI = weights[0:M]
    w0 = weights[M,0]
    alpha = hyperparameters['weight_decay']
    I = np.identity(M + 1)

    y = logistic_predict(weights, data)
    ones = np.ones((N, 1))
    data1 = np.column_stack((data, ones))

    f1 = np.sum(np.multiply(targets, np.log(y)))
    f2 = np.sum(np.multiply((1 - targets), (np.log(1 - y))))
    f3 = np.sum(0.5*(np.log((2*np.pi/alpha)) - (np.square(weights)*alpha)))
    f = f3 + f2 + f1

    df1 = np.dot(np.transpose(data1), (sigmoid(np.dot(data1, weights)) - targets))
    df2 = weights*(alpha)

    df = df1 + df2

    return f, df
