"""
Created on Sun Sep 17 07:26:03 2017

@author: dariocorral
"""

from datetime import datetime, date, timedelta
import pytz


class Hour(object):
    """
    Auxiliary class for converting GMT - NY - local time hours
    """
    #Local time hour property
    @property
    def current_local(self):
        """
        Returns local current hour
        
        :return:integer
        
        """
        
        return datetime.now().hour

    
    #New York current hour property
    @property
    def current_NY(self):
        """
        Returns New York current hour
        
        :return:integer
        """
        
        return datetime.now(tz=pytz.timezone('US/Eastern')).hour
    
    
    #GMT current hour property
    @property
    def current_GMT(self):
        """
        Returns GMT current hour
        
        :return:integer
        """
        
        return datetime.now(tz=pytz.timezone('utc')).hour
    
    #New York hour - GMT hour
    @property
    def offset_NY_GMT(self):
        """
        Returns New York current hour GMT current hour difference
        
        :return: integer
        
        """
        return self.current_NY - self.current_GMT
    
    #New York hour - GMT hour
    @property
    def offset_local_GMT(self):
        """
        Returns Local current hour  vs GMT current hour difference
        
        :return: integer
        
        """
        return self.current_local - self.current_GMT
    
    def hour_offset_calculate(self, hour, delta):
        """
        Operate with hours
        """
        year = date.today().year
        month = date.today().month
        day = date.today().day
        
        dt_hour = datetime(year, month, day, hour)
        dt_hour_offset = dt_hour + timedelta(hours= delta)
        
        return dt_hour_offset.hour
        
        