# -*- coding: utf-8 -*-
"""
BMI Calulator using pandas dataframe as data structure
"""

import pandas as pd
import numpy as np

import unittest

class TestBMI(unittest.TestCase):
    data_json_str = r'[{"Gender": "Male", "HeightCm": 171, "WeightKg": 96 },{ "Gender": "Male", "HeightCm": 161, "WeightKg": 85 },{ "Gender": "Male", "HeightCm": 180, "WeightKg": 77 },{ "Gender": "Female", "HeightCm": 166, "WeightKg": 62},{"Gender": "Female", "HeightCm": 150, "WeightKg": 70},{"Gender": "Female", "HeightCm": 167, "WeightKg": 82}]'
    BMI_categories = ['Moderately obese','Moderately obese','Normal Weight','Normal Weight','Moderately obese','Overweight']
    health_risks = ['Medium risk','Medium risk','Low risk','Low risk','Medium risk','Enhanced risk']    
    
    def test_bmi_categories(self):
        df = calculate_bmi_from_JSON(self.data_json_str)
        calc_cats = df['BMI Category'].tolist()
        self.assertEqual(calc_cats, self.BMI_categories)

    def test_health_risks(self):
        df = calculate_bmi_from_JSON(self.data_json_str)
        calc_cats = df['Health risk'].tolist()
        self.assertEqual(calc_cats, self.health_risks)

def calculate_bmi_from_JSON(data_json_str):
    '''
    Caluclates the Body Mass Index from supplied JSON data
    Parameters
    ----------
    data_json_str : string 
        A JSON string that is a list of patient records, with attributes "Gender", "HeightCm", "WeightKg". e.g.:
            [{"Gender": "Male", "HeightCm": 171, "WeightKg": 96 }]

    Returns
    -------
    df : pandas dataframe
        A dataframe with the following columns: "Gender","HeightCm","WeightKg","BMI","BMI Category","Health risk"

    '''
    # Definition of BMI ranges
    bmi_bin_edges = [0.0,18.5,25,30,35,40,np.inf];
    bmi_labels = ['Underweight','Normal Weight','Overweight','Moderately obese','Severely obese','Very severely obese']
    # Mapping of BMI risk
    cat_to_risk = {'Underweight':'Malnutrition risk','Normal Weight':'Low risk','Overweight':'Enhanced risk','Moderately obese':'Medium risk','Severely obese':'High risk','Very severely obese':'Very high risk'}
    
    df = pd.read_json(data_json_str,orient='records')

    df['BMI'] = df['WeightKg'] / (df['HeightCm']/100)**2
    
    df['BMI Category'] = pd.cut(df['BMI'], bins=bmi_bin_edges, labels=bmi_labels,right=True)
    
    df['Health risk'] = df['BMI Category'].apply(lambda x: cat_to_risk[x])
    return df

def count_overweight(df):
    # Count the number of overweight people
    n_over = (df['BMI']>25).sum()
    return n_over

if __name__ == '__main__':
    
    unittest.main()
    print()
    
    data_json_str = r'[{"Gender": "Male", "HeightCm": 171, "WeightKg": 96 },{ "Gender": "Male", "HeightCm": 161, "WeightKg": 85 },{ "Gender": "Male", "HeightCm": 180, "WeightKg": 77 },{ "Gender": "Female", "HeightCm": 166, "WeightKg": 62},{"Gender": "Female", "HeightCm": 150, "WeightKg": 70},{"Gender": "Female", "HeightCm": 167, "WeightKg": 82}]'
    df = calculate_bmi_from_JSON(data_json_str)
    print(df)
    print('Number overweight =',count_overweight(df))
    
    # Work out what the memory usage in Mb would be for a million patients to check we don't need to use something other than pandas
    mem_in_mb_1e6 = df.memory_usage(deep=True).sum()/df.shape[0]
    print('Approx. Memory Required for 1 million patients', mem_in_mb_1e6,'Mb')
    
    