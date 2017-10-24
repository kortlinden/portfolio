

#!/usr/bin/python

import matplotlib.pyplot as plt
import sys
import numpy
import pickle
from sklearn import preprocessing
from time import time
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.grid_search import GridSearchCV
import pandas

import sklearn

import matplotlib
from feature_format import featureFormat
from feature_format import targetFeatureSplit
sys.path.append("../tools/")





### features_list is a list of strings, each of which is a feature name
### first feature must be "poi", as this will be singled out as the label


### I'm looking for a feature most related to POI's

# The financial features may be related to in some combination to illegal payments to POIs.

features_list = ['poi', 'salary', 'to_messages', 'deferral_payments',
                 'total_payments', 'loan_advances', 'bonus',
                 'restricted_stock_deferred', 'deferred_income',
                 'total_stock_value', 'expenses',
                 'from_poi_to_this_person', 'exercised_stock_options',
                  'from_messages', 'other', 'from_this_person_to_poi',
                  'long_term_incentive', 'shared_receipt_with_poi',
                  'restricted_stock', 'ratio_to_poi', 'ratio_from_poi',
                  'total_poi_ratio']


NAN_value = 'NaN'

### load the dictionary containing the dataset
data_dict = pickle.load(open("final_project_dataset.pkl", "r") )
data_dict.pop("TOTAL", 0)
data_dict.pop('LOCKHART EUGENE E', 0)
data_dict.pop('THE TRAVEL AGENCY IN THE PARK', 0)

### look at data
print len(data_dict.keys())
print data_dict['BUY RICHARD B']
#print data_dict.values()

df = pandas.DataFrame.from_records(list(data_dict.values()))
print df.head()

df.replace(to_replace='NaN', value=numpy.nan, inplace=True)

# Print a count of NaNs per variable
print df.isnull().sum()

# Create framework to eliminate variables with too many NaNs
print df.shape
for column, series in df.iteritems():
    if series.isnull().sum() > 65:
        df.drop(column, axis=1, inplace=True)
#Removed those with more than 65 nan values
# Email addresses carry no useful info since we already have a key identifier.
df_noemail = df
if 'email_address' in list(df_noemail.columns.values):
    df_noemail.drop('email_address', axis=1, inplace=True)
if 'director_fees' in list(df_noemail.columns.values):
    df_noemail.drop('director_fees', axis=1, inplace=True)


df_ko = df.replace(to_replace=numpy.nan, value=0)
df_ko = df.fillna(0).copy(deep=True)
df_ko.columns = list(df.columns.values)
print df_ko.isnull().sum()
print df_ko.head()

df_ko.describe()

#Creating some new variables to hopefully increase the accuarcy and recall_score
#The reasoning is that the more a person communicates with a known POI the
#more likely they will themselves be POIs.

total_poi_ratio = (df_ko['from_poi_to_this_person'] +
 df_ko['from_this_person_to_poi']) / (df_ko['from_messages'] + df_ko['to_messages'])
ratio_to_poi = (df_ko['from_this_person_to_poi']) / (df_ko['from_messages'])
ratio_from_poi = (df_ko['from_poi_to_this_person']) / (df_ko['to_messages'])


df_ko['total_poi_ratio'] = pandas.Series(total_poi_ratio) * 100
df_ko['ratio_to_poi'] = pandas.Series(ratio_to_poi) * 100
df_ko['ratio_from_poi'] = pandas.Series(ratio_from_poi) * 100

df_ko.describe()


labels = df_ko['poi'].copy(deep=True).astype(int).as_matrix()
features = (df_ko.drop('poi', axis=1)).fillna(0).copy(deep=True).as_matrix()
shuffle = sklearn.cross_validation.StratifiedShuffleSplit(labels, 4,
    test_size=0.3, random_state=0)

from sklearn.ensemble import AdaBoostClassifier


from sklearn import grid_search

cv = sklearn.cross_validation.StratifiedShuffleSplit(labels, n_iter=20)

def scoring(estimator, features_test, labels_test):
     labels_pred = estimator.predict(features_test)
     p = sklearn.metrics.precision_score(labels_test, labels_pred, average='micro')
     r = sklearn.metrics.recall_score(labels_test, labels_pred, average='micro')
     if p > 0.3 and r > 0.3:
            return sklearn.metrics.f1_score(labels_test, labels_pred, average='macro')
     return 0

from sklearn import grid_search
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
parameters = {'n_estimators' : [5, 10, 30, 40, 50, 75, 100,150], 'learning_rate' :
    [.001, 0.1, 0.5, 1, 1.5, 2, 2.5], 'algorithm' : ('SAMME', 'SAMME.R')}
adab_clf = AdaBoostClassifier(DecisionTreeClassifier(max_depth=8))
adabclf = GridSearchCV(adab_clf, parameters, scoring = scoring, cv = cv)
adabclf.fit(features, labels)

print adabclf.best_estimator_
print adabclf.best_score_

from tester import test_classifier, dump_classifier_and_data
adab_best_clf = adabclf.best_estimator_
list_cols = list(df_ko.columns.values)
list_cols.remove('poi')
list_cols.insert(0, 'poi')
data = df_ko[list_cols].fillna(0).to_dict(orient='records')
enron_data_sub = {}
counter = 0
for item in data:
    enron_data_sub[counter] = item
    counter += 1

test_classifier(adab_best_clf, enron_data_sub, list_cols)
clf = adab_best_clf
my_dataset = enron_data_sub
poi = ["poi"]
features_list = list_cols
dump_classifier_and_data(clf, my_dataset, features_list)
