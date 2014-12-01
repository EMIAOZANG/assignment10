'''
Created on Nov 24, 2014

@author: luchristopher
'''
import pandas as pd
import numpy as np
from sklearn import linear_model
import statsmodels.api as sm
from superio import *


def clean_rawdata(raw_data):
    '''
    Cleans the data by:
        1.Remove entries with invalid grades(any value excepts A,B,C)
        2.Remove redundant entries
        3.Remove columns that are not required for solving problems
        4.Convert the time data to correct datetime format
        5.Reindex the data frame by the id of restaurants(CAMIS)
    '''
    clean_data = raw_data.dropna()   #this is because dropna is faster than regular indexing
    clean_data = clean_data[(clean_data['GRADE']=='A') | (clean_data['GRADE']=='B') | (clean_data['GRADE']=='C')]
    clean_data.drop_duplicates(inplace=True)
    clean_data = clean_data[['CAMIS','BORO','GRADE','GRADE DATE']]
    clean_data.set_index('CAMIS')
    clean_data['GRADE DATE'] = pd.to_datetime(clean_data['GRADE DATE'])
    return clean_data

def numerical_conversion(grade_list):
    '''
    convert grade A B C to 2 1 0
    '''
    ordinal_list = map(ord,grade_list)
    ordinal_list = map(lambda x:abs(x-67),ordinal_list)
    return map(float,ordinal_list)

def test_grades(grade_list):
    '''
    Test if a time series in stationary, use ADF test method, and for those series that has negative outputs, fit with a linear regression model
    to see if the trend is ascending or descending
    '''
    numerical_grade_list = numerical_conversion(grade_list)
    #return 0 for lists with only 1 grade; return sigma(gradelist[1]-gradelist[0])) for lists with 2 grades
    if len(numerical_grade_list) == 1:
        return 0
    if len(numerical_grade_list) == 2:
        if numerical_grade_list[1] > numerical_grade_list[0]:
            return 1
        elif numerical_grade_list[1] < numerical_grade_list[0]:
            return -1
        else:
            return 0
    adf_result = sm.tsa.adfuller(numerical_grade_list,0) #adf test for unit-root, setting maxlag = 0
    #if the t-statistic value of adf test is below the 95% confidence interval, the list will be accepted as stationary, otherwise the list has a trend
    if adf_result[0] > adf_result[4]['5%']:
        linear_test = linear_model.LinearRegression()   #built a linear regression model for trend analysis
        x = np.arange(len(numerical_grade_list)).reshape(len(numerical_grade_list),1)
        y = np.array(numerical_grade_list).reshape(len(numerical_grade_list),1)
        linear_test.fit(x,y)
        if linear_test.coef_ > 0:
            return 1
        elif linear_test.coef_ <0:
            return -1
    return 0

def csv_validator(input_string):
    if os.path.isfile(input_string) == False:
        raise ValueError()
        return None
    elif not os.path.basename(input_string).endswith('.csv'): 
        raise FileExtensionError()
        return None
    else:
        return input_string
    


        
    
    
    
    