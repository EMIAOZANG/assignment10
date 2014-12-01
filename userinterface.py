'''
Created on Nov 28, 2014

@author: luchristopher
'''
from superio import *
from pandas import *
from userexcps import *
from utilities import *
import sys
import os

def get_data():
    '''
    Get data from source file
    '''
    filename = safeInput('Please enter the path of the importing file:\n',['exit','quit'],csv_validator)
    
    try:
        raw_data = pd.read_csv(filename)
    except (MemoryError):
        print >> sys.stderr, 'Memory Limit Exceeded\n'
        sys.exit()
    except:
        print >> sys.stderr, 'Failed to Read Data From File\n'
        sys.exit()
    return raw_data

    