'''
Created on 14 Eyl 2023

@author: yusuf
'''

import requests


class rest(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.url = 'http://localhost:5000/'
        self.headers={"X-API-Key":"API_KEY_1"}
       
   
    def put(self, apiUrl):        
        Url = f"{self.url}{apiUrl}"        
        response = requests.put(Url, headers=self.headers)
        return response.status_code


    def delete(self, apiUrl):       
        Url = f"{self.url}{apiUrl}"
        response = requests.delete(Url, headers=self.headers)
        return response.status_code   
    
    
    def get(self, apiUrl, untilStatus200=True):        
        Url = f"{self.url}{apiUrl}"
        response = requests.get(Url, headers=self.headers)
        
        if untilStatus200 & (response.status_code != 200):
            for i in range(5):
                response = requests.get(Url, headers=self.headers)
                if response.status_code == 200:
                    break
        
        return response.status_code, response.json()  
    
restObject = rest()  