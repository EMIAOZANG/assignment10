'''
Created on Nov 22, 2014

@author: luchristopher
'''
from datainspector import *
from dataclean import *
from utilities import *
from userinterface import *
import sys

def main():
    raw_data = get_data()
    data_viewer = DataInspector(raw_data)
    #4: print the sum of the improvement info
#     sum_data = data_viewer.gradesum_by_borough()
#     print sum_data
#     writeToTextfile(sum_data, 'grade_improvements_by_borough', 'txt')
    #5: plot the grading data
#     boroughs = ['STATEN ISLAND','MANHATTAN','BROOKLYN','QUEENS','BRONX','NYC']
#     for borough in boroughs:
#         data_viewer.plotdata_by_range(borough)
    #6: find the trends for number of inspections over time
    data_viewer.plot_inspection_frequency()
        

if __name__ == '__main__':
    main()