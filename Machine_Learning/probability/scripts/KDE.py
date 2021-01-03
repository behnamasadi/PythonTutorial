import numpy as np
from scipy import stats
import matplotlib.pylab as plt


n_basesample = 1000
np.random.seed(8765678)
xn = np.random.randn(n_basesample)
gkde=stats.gaussian_kde(xn)

#linspace will create a list with the size of 100 items, from -7 to 7 with
#evaluate the estimated pdf on a provided set of points
#gkde.evaluate()
ind = np.linspace(-7,7,101)
kdepdf = gkde.evaluate(ind)


plt.figure()
# plot histgram of sample
plt.hist(xn, bins=20, normed=1)
# plot data generating density
plt.plot(ind, stats.norm.pdf(ind), color="r", label='Original Function')
# plot estimated density
plt.plot(ind, kdepdf, label='kde estimation', color="g")
plt.title('Kernel Density Estimation')
plt.legend()
plt.show()
