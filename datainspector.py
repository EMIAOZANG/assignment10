'''
Created on Nov 23, 2014

@author: luchristopher
'''
from utilities import *
from dataclean import *
import matplotlib.pyplot as plt

class DataInspector():
    '''
    This is the class definition for a data inspector, which provides functions for solving problems in assignment 10
    
    In class DataInspector:
    >>>>
    Attributes:
        self.__data : a data frame for the cleaned data set
    Methods:
        __test_restaurants_grades : returns the general trend of the grading of the restaurant represented by the CAMIS
        __cumulate_grade : returns the total number of restaurants of each grade within specific range over time
        test_restaurants_grades_shell : returns a data frame containing 2 columns 'CAMIS' and 'IMPROVEMENT'(which is the result of test_restaurants_grades)
        gradesum_by_borough : returns the sum of grades for each borough
        plotdata_by_range : creates a graph that shows the total number of restaurants within specific range(NYC or one of the 5 boroughs)
    '''


    def __init__(self, raw_dataframe):
        '''
        Constructor : cleans and stores the raw data as a dataframe
        '''
        cleaner = DataCleaner(clean_rawdata)
        self.__data = cleaner.clean(raw_dataframe)
    
    def __test_restaurants_grades(self,camis_id):
        '''
        returns the general trend of the grading by restaurants
        '''
        restaurant_data = self.__data[self.__data['CAMIS']==camis_id]  #TAKE CARE!!!!
        restaurant_data = restaurant_data.sort_index(by = 'GRADE DATE')
        restaurant_grade_list = list(restaurant_data['GRADE'])
        return test_grades(restaurant_grade_list)
    
    def test_restaurants_grades_shell(self):
        '''
        returns a data frame containing 2 columns 'CAMIS' and 'IMPROVEMENT'(which is the result of test_restaurants_grades)
        '''
        camis_list = list(self.__data['CAMIS'].unique())
#         print camis_list
        trend_list = map(self.__test_restaurants_grades,camis_list)  #calculate the grades trend for all restaurants
        return pd.DataFrame(np.array([camis_list,trend_list]).T,columns=['CAMIS','IMPROVEMENT'])
    
    def gradesum_by_borough(self):
        '''
        returns the sum of the grades for each borough
        '''
        trend_data = self.test_restaurants_grades_shell()
        boro_data = self.__data[['CAMIS','BORO']].drop_duplicates()
        merged_data = pd.merge(trend_data,boro_data,on='CAMIS')
        return merged_data.groupby('BORO').sum().drop('CAMIS',1)
        
    def __cumulate_grades(self,range_data):
        '''
        returns the total number of restaurants of each grade within specific range over time
        '''
        recent_grade = {}   #recent grade up to date for each restaurant
        count = {'A':0,'B':0,'C':0} #number of restaurants in each grade
        count_by_date = []
        range_data.sort('GRADE DATE',axis = 0,inplace = True)
        previous_dates = []
        previous_dates.append(range_data['GRADE DATE'].iloc[0])
        for record in range(len(range_data)):
            current_date = range_data.iloc[record]['GRADE DATE']
            if current_date != previous_dates[-1]:
                previous_dates.append(current_date)
                count_by_date.append(count.copy())
            #if the same restaurant has been identified, we have to check if the grading has changed 
            current_grade = range_data.iloc[record]['CAMIS']
            if current_grade in recent_grade: 
                count[recent_grade[current_grade]] -= 1
            recent_grade[current_grade]=range_data.iloc[record]['GRADE']
            count[range_data.iloc[record]['GRADE']] += 1
        count_by_date.append(count.copy())  #push the last day in
        total_grades = pd.DataFrame(count_by_date, index = previous_dates)
        total_grades.columns.name='GRADE'
        return total_grades
    
    def plotdata_by_range(self,plot_range):
        '''
        creates a graph that shows the total number of restaurants within specific range(NYC or one of the 5 boroughs)
        '''
        if plot_range != 'NYC':
            range_data = self.__data[self.__data['BORO']==plot_range]
        else:
            range_data = self.__data
        total_grades = self.__cumulate_grades(range_data)
        plt.style.use('ggplot') #use R-ggplot sytle
        fig = plt.figure()
        axes = fig.add_subplot(1,1,1)
        axes.set_title('Number of Restaurants in Each Grade Over Time, {}'.format(plot_range),fontsize=12,color='grey')
        total_grades.plot(ax=axes,grid = False)
        plt.savefig('grade_improvement_{}.pdf'.format(plot_range.lower()))
        plt.show()
        
    def __inspection_frequency_trend(self):
        '''
        calculate the frequency of inspection conducted per week over time
        '''
        date_list = self.__data['GRADE DATE'].copy()
        print date_list
        week_list = date_list.dt.weekofyear
        year_list = date_list.dt.year
        year_and_week = pd.DataFrame([year_list,week_list]).T
        year_and_week.columns=['Year','Week']
        year_and_week['GRADES']=list(date_list.index)
        print year_and_week
        return year_and_week.groupby(['Year','Week']).count()
    
    def plot_inspection_frequency(self):
        '''
        calculate the frequency of inspection conducted per week over time
        '''
        frequency_by_week = self.__inspection_frequency_trend()
#         print frequency_by_week
        plt.style.use('ggplot')
        fig=plt.figure()
        axes = fig.add_subplot(1,1,1)
        axes.set_title('Inspection Frequencies By Week Over Time',fontsize=12,color='grey')
        axes.set_ylabel('Number of Inspections')
        axes.set_xlabel('Time')
        frequency_by_week.plot(ax = axes,grid=False)
        plt.savefig('inspection_freq.pdf')
        plt.show()
        
        
        
        
        
        
        
        