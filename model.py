#! /opt/conda/envs/env/bin/python
import argparse
import os
from sklearn.linear_model import SGDClassifier
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--model-dir", default="/opt/ml/")
    parser.add_argument("--training", default="/opt/ml/input/data/training")
    parser.add_argument("--alpha", type=float, default=0.0001)
    
    args = parser.parse_args()
        
    
    df = pd.read_csv(os.path.join(args.training, 'transfusion.data'))

    predictors = ['Recency (months)', 'Time (months)', 'Frequency (times)', 'Monetary (c.c. blood)']

    target = 'whether he/she donated blood in March 2007'

    X = df[predictors]
    y = df[target]
    
    estimator = SGDClassifier(loss='log', alpha=args.alpha)
    
    estimator.fit(X,y)
    
    print(f"accuracy={accuracy_score(y, estimator.predict(X))};")
    
    joblib.dump(estimator, os.path.join(args.model_dir, 'model.mdl'))
    
    