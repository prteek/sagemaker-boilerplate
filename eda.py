import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier, LogisticRegressionCV
from sklearn.inspection import PartialDependenceDisplay
from sklearn.decomposition import PCA, KernelPCA
from sklearn.preprocessing import *
from sklearn.pipeline import make_pipeline

load_dotenv('local_credentials.env')


data = 'transfusion.data'
df = pd.read_csv(data)

df.head()

df.info()

target = 'whether he/she donated blood in March 2007'
features = df.columns.difference([target])

ax = sns.pairplot(df.rename({target:'target'}, axis=1), hue='target', height=1.5)
ax.savefig('resources/data-pairplot.png', bbox_inches='tight')

# Model variable relationship to target using no-parametric estimate 
X, y = df[features], df[target]
estimator = RandomForestClassifier()

estimator.fit(X,y)

fig, ax = plt.subplots(figsize=(9,3))
pdp = PartialDependenceDisplay.from_estimator(estimator, X, features, target=target,kind='both', n_cols=len(features), ax=ax,
                                        ice_lines_kw={'alpha':0.2, 'linewidth':0.5},
                                        pd_line_kw={'color':'k', 'linestyle':'-'},
                                        subsample=200,
                                       grid_resolution=20, n_jobs=-1)

pdp.figure_.savefig('resources/feature-relationship.png', bbox_inches='tight')


# Model PCA versions of variables
pca = PCA(whiten=True, n_components=3) # Drop the redundant component
Xt = pca.fit_transform(X)

dft = pd.DataFrame(np.c_[Xt,y]).rename({Xt.shape[1]:'target'}, axis=1)
ax = sns.pairplot(dft, hue='target', height=1.5)

ax.savefig('resources/pca_features.png', bbox_inches='tight')

estimator = make_pipeline(pca, RandomForestClassifier())
estimator.fit(X,y)

fig, ax = plt.subplots(figsize=(9,3))
pdp = PartialDependenceDisplay.from_estimator(estimator, X, features, target=target,kind='both', n_cols=len(features), ax=ax,
                                        ice_lines_kw={'alpha':0.2, 'linewidth':0.5},
                                        pd_line_kw={'color':'k', 'linestyle':'-'},
                                        subsample=200,
                                       grid_resolution=20, n_jobs=-1)

pdp.figure_.savefig('resources/pca-transformed-relationship.png', bbox_inches='tight')

estimator = RandomForestClassifier()
estimator.fit(Xt,y)
fig, ax = plt.subplots(figsize=(9,3))
pdp = PartialDependenceDisplay.from_estimator(estimator, Xt, range(Xt.shape[1]), target=target,kind='both', n_cols=Xt.shape[1], ax=ax,
                                        ice_lines_kw={'alpha':0.2, 'linewidth':0.5},
                                        pd_line_kw={'color':'k', 'linestyle':'-'},
                                        subsample=200,
                                       grid_resolution=20, n_jobs=-1)

pdp.figure_.savefig('resources/decomposed-variables-relationship.png', bbox_inches='tight')

# Modelling features as splines and using logistic model
estimator = make_pipeline(SplineTransformer(n_knots=10,knots='quantile', extrapolation='linear'), 
                          LogisticRegressionCV(Cs=np.logspace(1/10000,1000),
                                               max_iter=10000,
                                               n_jobs=-1, 
                                               class_weight=None, 
                                               scoring='neg_log_loss', 
                                               cv=5))

estimator.fit(Xt,y)
fig, ax = plt.subplots(figsize=(9,3))
pdp = PartialDependenceDisplay.from_estimator(estimator, Xt, range(Xt.shape[1]), target=target,kind='both', n_cols=Xt.shape[1], ax=ax,
                                        ice_lines_kw={'alpha':0.2, 'linewidth':0.5},
                                        pd_line_kw={'color':'k', 'linestyle':'-'},
                                        subsample=200,
                                       grid_resolution=20, n_jobs=-1)

pdp.figure_.savefig('resources/linear-model-with-splines.png', bbox_inches='tight')
