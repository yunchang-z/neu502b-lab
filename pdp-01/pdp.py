import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def inv_logit(x):
    return 1 / (1 + np.exp(-x))

def inv_logit_derivative(x):
    fx = inv_logit(x)
    return fx * (1-fx)

def tanh(x):
    return (1.0 - np.exp(-2*x))/(1.0 + np.exp(-2*x))

def tanh_derivative(x):
    return (1 + tanh(x))*(1 - tanh(x))

class NeuralNetwork:
    """Simple neural network object.
    
    Parameters
    ----------
    net_arch: list
        List specifying the network architecture. See notes for details.
    activation: tanh | logistic
        Activation function for the hidden layer.
    seed : int
        Seed used by the random number generator.
    
    Attributes
    ----------
    arch : list
        Network architecture.
    layers : int
        Number layers in network (including input/output).
    steps_per_epoch : int
        Number of steps per training epoch.
    weights : array
        Values of network weights.
        
    Notes
    -----
    The network architecture (net_arch) specifies the network configuration,
    including the input and ouput layers. For example, net_arch=[2,2,1] specifies
    a network of comprised of:
    
    - Input layer: (2 nodes)
    - Hidden layer: (2 nodes)
    - Output lyaer: (1 node)
    
    References
    ----------
    [1] https://chih-ling-hsu.github.io/2017/08/30/NN-XOR
    [2] https://chih-ling-hsu.github.io/2018/08/19/NN-XOR
    """
    def __init__(self, net_arch, activation='tanh', seed=47404):
        
        if seed is not None: np.random.seed(seed)
        
        ## Define activation functions.
        if activation == 'tanh':
            self.activity = tanh
            self.activity_derivative = tanh_derivative
        elif activation == 'logistic':
            self.activity = inv_logit
            self.activity_derivative = inv_logit_derivative
        else:
            raise ValueError('activation must be "tanh" or "logistic".')
            
        ## Initialize network.
        self.layers = len(net_arch)
        self.steps_per_epoch = 1
        self.arch = net_arch
        self.weights = []

        ## Randomly initialize weights in range (-1,1).
        for layer in range(self.layers - 1):
            w = np.random.uniform(-1, 1, size=(net_arch[layer]+1, net_arch[layer+1]))
            self.weights.append(w)
    
    def _forward_prop(self, x):
        """Forward propagation step."""
        
        y = x

        ## Iterate over layers.
        for i in range(len(self.weights)-1):
            
            ## Compute (unthresholded) activation.
            activation = np.dot(y[i], self.weights[i])
            
            ## Threshold activation.
            activity = self.activity(activation)

            ## Add activation bias. 
            activity = np.concatenate((np.ones(1), np.array(activity)))
            
            y.append(activity)

        ## Output layer.
        activation = np.dot(y[-1], self.weights[-1])
        activity = self.activity(activation)
        y.append(activity)
        
        return y
    
    def _back_prop(self, y, target, alpha):
        """Back propagation step."""
        
        ## Compute error.
        error = target - y[-1]
        
        ## Compute error with respect to ouputs.
        delta_vec = [error * self.activity_derivative(y[-1])]

        ## Iteratively compute error (backwards across layers).
        for i in range(self.layers-2, 0, -1):
            error = delta_vec[-1].dot(self.weights[i][1:].T)
            error = error*self.activity_derivative(y[i][1:])
            delta_vec.append(error)
        
        ## Adjust the weights using back-propagation.
        delta_vec.reverse()
        for i in range(len(self.weights)):
            
            ## Proper layer shaping.
            layer = y[i].reshape(1, self.arch[i]+1)
            delta = delta_vec[i].reshape(1, self.arch[i+1])
            
            ## Update weights.
            self.weights[i] += alpha*layer.T.dot(delta)
    
    def fit(self, data, labels, alpha=0.1, epochs=100):
        """Fit neural network to training data.
        
        Parameters
        ----------
        data : list of lists
            The set of all Boolean pairs.
        labels : list
            The corresponding XOR labels.
        alpha : float
            Learning rate.
        epochs : int
            Number of training epochs.
        """
        
        ## Add bias to input layer.
        ones = np.ones((1, data.shape[0]))
        Z = np.concatenate((ones.T, data), axis=1)
        
        ## Main loop.
        for k in range(epochs):
        
            ## Randomly sample.
            sample = np.random.randint(data.shape[0])

            ## Feed-forward propagation.
            x = [Z[sample]]
            y = self._forward_prop(x)

            ## Back-propagation.
            target = labels[sample]
            self._back_prop(y, target, alpha)
    
    def predict_single_data(self, x):
        """Predict single datum."""
        
        val = np.concatenate((np.ones(1).T, np.array(x)))
        for i in range(0, len(self.weights)):
            val = self.activity(np.dot(val, self.weights[i]))
            val = np.concatenate((np.ones(1).T, np.array(val)))
        return val[1]
    
    def predict(self, X):
        """Predict set of data."""
        Y = np.array([]).reshape(0, self.arch[-1])
        for x in X:
            y = np.array([[self.predict_single_data(x)]])
            Y = np.vstack((Y,y))
        return Y
    
    def plot_decision_regions(self, X, y, resolution=0.02, size=100, ax=None):
        """Plot decision boundaries.
        
        Parameters
        ----------
        X : array
            The set of all Boolean pairs.
        y : array
            The corresponding XOR labels.
        resolution : float
            Resolution of decision contour plots.
        size : int
            Marker size.
        ax : Matplotlib object.
            Canvas to plot onto.
        """
        
        ## Define markers / colormap.
        markers = ('s', 'x', 'o', '^', 'v')
        colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
        cmap = ListedColormap(colors[:len(np.unique(y))])

        # plot the decision surface
        x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
        xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                               np.arange(x2_min, x2_max, resolution))
        Z = self.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
        Z = Z.reshape(xx1.shape)
        
        if ax is None: fig, ax = plt.subplots(1,1,figsize=(5,5))
        ax.contourf(xx1, xx2, Z, alpha=0.4, cmap=cmap)
        ax.set(xlim=(xx1.min(), xx1.max()), ylim=(xx2.min(), xx2.max()))

        # plot class samples
        for idx, cl in enumerate(np.unique(y)):
            ax.scatter(x=X[y == cl, 0], y=X[y == cl, 1], s=size, alpha=0.8,
                        marker=markers[idx], color=colors[idx], label=cl)
            
        return ax