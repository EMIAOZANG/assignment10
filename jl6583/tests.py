'''
Created on Nov 24, 2014

@author: luchristopher
'''
import unittest
from utilities import *
from datainspector import *
import time



 
class Test_TestGrades(unittest.TestCase):
 
 
    def setUp(self):
        self.lists = [['A','B','C','C','C']
                      ,['A','B','A','B','A','B']
                      ,['A','B','B','B','A','A','A']
                      ,['C','B','A']
                      ,['A','B']
                      ,['A']]
 
 
    def tearDown(self):
        self.lists = None
 
 
    def test(self):
        for list in self.lists:
            print test_grades(list)
 
 
class Test_CleanRawData(unittest.TestCase):
     
    def setUp(self):
        self.df = pd.read_csv('data.csv')
         
    def tearDown(self):
        self.df = None
         
    def test(self):
        start_time = time.time()
        print clean_rawdata(self.df)
        end_time = time.time()
        print end_time - start_time
           
class Test_GradeSumByBorough(unittest.TestCase):
     
    def setUp(self):
        self.df = pd.read_csv('data.csv')
        self.data_inspector = DataInspector(self.df)
         
    def tearDown(self):
        self.df = None
         
    def test(self):
        self.data_inspector.gradesum_by_borough()
 
class Test_PlotdataByRange(unittest.TestCase):
     
    def setUp(self):
        self.df = pd.read_csv('data.csv')
        self.data_inspector = DataInspector(self.df)
     
    def tearDown(self):
        self.df= None
         
    def test(self):
        self.data_inspector.plotdata_by_range('NYC')    #test the plot without any borough specification
        self.data_inspector.plotdata_by_range('BROOKLYN')   #test the functionality with specified borough name
         
class Test_RestaurantsGradesShell(unittest.TestCase):
       
    def setUp(self):
        self.df = pd.read_csv('data.csv')
        self.data_inspector = DataInspector(self.df)
          
       
    def tearDown(self):
        self.df = None
        self.data_inspector = None
           
    def test(self):
        print self.data_inspector.test_restaurants_grades_shell()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()