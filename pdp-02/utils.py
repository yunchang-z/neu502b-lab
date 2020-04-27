import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import numpy as np
import torch

def plot_decision_regions(
    predict, X, y, resolution=0.02, size=100, ax=None,
    title=None,
    # This parameter forces the decision region plot to be PNG due to issues with SVG display.
    # This should be removed for notebooks that prefer only PNG display.
    force_matplotlib_output_png_hack=True):
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
    if force_matplotlib_output_png_hack:
        from IPython.display import set_matplotlib_formats
        set_matplotlib_formats('png')

    ## HACK Adapting sizes from CGC's code to work with this piece of SZ's code
    X = X.T
    ## HACK Force arrays to numpy
    if torch.is_tensor(X):
        X = X.numpy()
    if torch.is_tensor(y):
        y = y.numpy()

    ## Define markers / colormap.
    markers = ('x', 'o', 's', '^', 'v')
    colors = ('gray', 'lightgreen', 'blue', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])

    # plot the decision surface
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution).astype(np.float32),
                           np.arange(x2_min, x2_max, resolution).astype(np.float32))
    #Z = predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = predict(torch.tensor([xx1.ravel(), xx2.ravel()])).detach()
    Z = Z.reshape(xx1.shape)

    if ax is None:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1,1,figsize=(5,5))
    if title is not None:
        ax.set(title=title)
    ax.contourf(xx1, xx2, Z, alpha=0.4, cmap=cmap)
    ax.set(xlim=(xx1.min(), xx1.max()), ylim=(xx2.min(), xx2.max()))

    # plot class samples
    for idx, cl in enumerate(np.unique(y)):
        ax.scatter(x=X[y == cl, 0], y=X[y == cl, 1], s=size, alpha=0.9,
                    marker=markers[idx], color=colors[idx], label=cl)

    if force_matplotlib_output_png_hack:
        import matplotlib.pyplot as plt
        plt.show()
        set_matplotlib_formats('svg')

    return ax

def animate_decision_regions(X, Y, predict_history, *, Xhistory=None, ax=None, filename=None, interval=50):
    '''
    make_predict: function that takes parameters
    '''
    import matplotlib.pyplot as plt
    if ax is None: f, ax = plt.subplots()
    f = ax.figure

    # HACK HACK comment this
    if Xhistory is None:
        Xhistory = [X] * len(predict_history)

    kw = dict(force_matplotlib_output_png_hack=False)

    plot_decision_regions(predict_history[0], Xhistory[0], Y, ax=ax, **kw)

    def update(t):
        for a in ax.lines + ax.collections:
            a.remove()
        plot_decision_regions(predict_history[t], Xhistory[t], Y, ax=ax, **kw)
        return []

    a = animation.FuncAnimation(
        f, update, frames=len(predict_history), interval=interval, blit=True, repeat=False)
    plt.close()

    if filename is not None:
        assert filename.endswith('.gif') or filename.endswith('.mp4'), 'Only supports exporting to .gif or .mp4'
        if filename.endswith('.mp4'):
            Writer = animation.writers['ffmpeg']
            writer = Writer(fps=1000./interval, bitrate=1800)
            a.save(filename, writer=writer)
            from IPython.display import Video
            return Video(filename)
        else:
            a.save(filename, writer='imagemagick')
            from IPython.display import Image
            return Image(filename)

    from IPython.display import HTML
    return HTML(a.to_jshtml())

def torch_cov(x):
    '''
    Compute np.cov() of a torch.tensor.
    '''
    x = x - x.mean(axis=1, keepdims=True)
    return x@x.T / (x.shape[1] - 1)

def torch_corrcoef(x):
    '''
    Compute np.corrcoef() of a torch.tensor.
    '''
    cov = torch_cov(x)
    diag_cov_rsqrt = torch.diag(cov).rsqrt()
    return cov * diag_cov_rsqrt[:, None] * diag_cov_rsqrt[None, :]

def fit(loss, parameters, *, lr=0.1, num_epochs=100, plot_loss=True, opt_fn=torch.optim.SGD):
    history, parameter_history = [], []
    parameters = list(parameters)
    opt = opt_fn(parameters, lr=lr)

    for t in range(num_epochs):
        J = loss()

        opt.zero_grad()
        J.backward()
        opt.step()

        history.append(J)
        parameter_history.append([p.detach().clone() for p in parameters])

    if plot_loss:
        import matplotlib.pyplot as plt
        plt.plot(history)
        plt.xlabel('# epochs')
        plt.ylabel('training loss')

    return history, parameter_history
