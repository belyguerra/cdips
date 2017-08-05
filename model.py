import pandas as pd
import numpy as np
import xgboost as xgb
import settings

import sklearn
from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

"""
feature extraction and modeling
"""

class cust_regression_vals(BaseEstimator, TransformerMixin):
    def fit(self, x, y=None):
        return self
    def transform(self, x):
        #could use list(df.columns) instead?
        to_drop = [settings.text_colname, settings.var_colname, settings.gene_colname, settings.id_colname]
        x = x.drop(to_drop,axis=1).values
        return x

class cust_txt_col(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key
    def fit(self, x, y=None):
        return self
    def transform(self, x):
        return x[self.key].apply(str)


if __name__ == '__main__':
    """extract features"""
    train = pd.read_csv(settings.train)
    y = train[settings.y]
    train = train.drop([settings.y], axis=1)

    test = pd.read_csv(settings.test)
    pid = test[settings.id_colname]

    feat_p = Pipeline([
        ('union', FeatureUnion(
            n_jobs = -1,
            transformer_list = [
                ('standard', cust_regression_vals()),
                ('p1', Pipeline([
                    ('Text', cust_txt_col(settings.text_colname)),
                    ('tfidf_Text', TfidfVectorizer(ngram_range=(1, 2), )),
                    ('tsvd', TruncatedSVD(n_components=50, n_iter=25, random_state=12))
                ]))
            ])
        )])

    train = feat_p.fit_transform(train); print(train.shape)
    test = feat_p.transform(test); print(test.shape)


    """ init and run model"""
    y = y - 1 #fix for zero bound array
    denom = 0
    fold = 20
    for i in range(fold):
        params = {
            'eta': 0.03333,
            'max_depth': 4,
            'objective': 'multi:softprob',
            'eval_metric': 'mlogloss',
            'num_class': 9,
            'seed': i,
            'silent': True
        }

        x1, x2, y1, y2 = train_test_split(train, y, test_size=0.18, random_state = i)
        watchlist = [(xgb.DMatrix(x1, y1), 'train'), (xgb.DMatrix(x2, y2), 'valid')]

        model = xgb.train(
            params, xgb.DMatrix(x1, y1), 1000,
            watchlist, verbose_eval = 50, early_stopping_rounds=100
        )

        score = metrics.log_loss(
            y2, model.predict(xgb.DMatrix(x2),
            ntree_limit = model.best_ntree_limit),
            labels = list(range(9))
        )
        print(score)

        if denom != 0:
            pred = model.predict(xgb.DMatrix(test), ntree_limit = model.best_ntree_limit+80)
            preds += pred
        else:
            pred = model.predict(xgb.DMatrix(test), ntree_limit = model.best_ntree_limit+80)
            preds = pred.copy()
        denom += 1
        submission = pd.DataFrame(pred, columns = ['class'+str(c+1) for c in range(9)])
        submission[settings.id_colname] = pid
        submission.to_csv('submission_xgb_fold_' + str(i) + '.csv', index=False)

    preds /= denom
    submission = pd.DataFrame(preds, columns=['class' + str(c + 1) for c in range(9)])
    submission[settings.id_colname] = pid
    submission.to_csv('submission_xgb.csv', index=False)
