import sqlite3 
from db import sqliteogar


class StorageDriver(sqliteogar.DatabaseUtil):
    
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.coins = None
        self.score = None
        self.user_id = None
        self.car_id = None
        self.name = None
        self.set_and_save_values(kwargs)
        
    def set_and_save_values(self, kwargs):
        '''
        Funkcja pobiera dowolne argumenty i jeżeli takie istnieją w bazie danych, to je 
        w sensie zapisuje itp
        '''
        for arg in kwargs.keys():
            if arg == 'coins':
                self.coins = kwargs[arg]
                self.update_coins(self.coins)
            elif arg == 'score':
                self.score = kwargs[arg]
                self.update_highscore(self.score)
            elif arg == 'name':
                self.name = kwargs[arg]
                self.set_username(self.name)
            elif arg == 'user_id':
                self.user_id = kwargs[arg]
            elif arg == 'car_id':
                self.car_id = kwargs[arg]
            else:
                continue
            
            