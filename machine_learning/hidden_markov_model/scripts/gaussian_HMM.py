import numpy as np
from hmmlearn import hmm

import warnings

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()
  

warnings.filterwarnings("ignore")


np.random.seed(42)

model = hmm.GaussianHMM(n_components=3, covariance_type="full")
print model
model.startprob_ = np.array([0.6, 0.3, 0.1])
model.transmat_ = np.array([[0.7, 0.2, 0.1],[0.3, 0.5, 0.2],  [0.3, 0.3, 0.4]])
model.means_ = np.array([[0.0, 0.0], [3.0, -3.0], [5.0, 10.0]])
model.covars_ = np.tile(np.identity(2), (3, 1, 1))
X, Z = model.sample(100)




#model = hmm.MultinomialHMM
