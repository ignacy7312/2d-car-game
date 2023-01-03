import sqlite3
from sqlite3 import Error


class DatabaseUtil():
    
    db_file = 'db/baza2.db'
    
    def __init__(self):
        self.connection = self.create_connection()
        self.cursor = self.connection.cursor()
        
    def create_connection(self):
        '''create a connection to a SQLite database'''
        conn = None
        try:
            # fcja connect zwraca obiekt Connection
            # na którym można wykonać operacje
            conn = sqlite3.connect(DatabaseUtil.db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)
        
        return conn
    
    def create_user(self, ud):
        '''stworz nowego uzytkownika - nowy save'''
        sql = ''' INSERT INTO user(id, name, high_score, coins, games_played, time_spent)
                VALUES(?,?,?,?,?,?) '''

        self.cursor.execute(sql, ud)
        self.connection.commit()

    def create_car(self, cd):
        '''Dodaj nowe auto'''
        sql = ''' INSERT INTO cars(id, name, price, is_unlocked, path_to_graphics)
                VALUES(?,?,?,?,?) '''
        self.cursor.execute(sql, cd)
        self.connection.commit()


    def get_current_user_id(self):
        ''' Funkcja zwraca id aktualnego użytkownika '''
        id_exec = '''SELECT user_id FROM mapowania
            '''
        return self.cursor.execute(id_exec).fetchone()[0]
    
    def get_coins(self):
        ''' Funkcja zwraca ilość monet aktualnego użytkownika oraz jego id'''

        sql = '''SELECT coins FROM user WHERE id = ?
        '''
        idx = self.get_current_user_id()
        
        return self.cursor.execute(sql, (idx,)).fetchone()[0], idx
    
    def set_coins(self, coins):
        '''funckja która USTAWIA ilosc monet, a nie aktualizuje'''
        
        sql = ''' UPDATE user
                SET coins = ? WHERE id = ?
                '''
        idx = self.get_current_user_id()
        self.cursor.execute(sql, (coins, idx))
        self.connection.commit()

    def update_coins(self, coins):
        ''' Funckja dostaje ilość monet i o tyle zwiększa je w bazie danych dla danego użytkownika'''
        
        # dostaje z funkcji zarówno ilość  monet jak i indeks aktualnego użytkownika
        current_coins, idx = self.get_coins()
        print(current_coins, idx)

        sql = ''' UPDATE user
                SET coins = ? WHERE id = ?
                '''
        
        self.cursor.execute(sql, (current_coins + coins, idx ))
        self.connection.commit()
        
    def get_highscore(self):
        ''' Funkcja zwraca high score aktualnego użytkownika oraz jego id'''
        
        sql = '''SELECT high_score FROM user WHERE id = ?
        '''
        idx = self.get_current_user_id()
        return self.cursor.execute(sql, (idx,)).fetchone()[0], idx

    def update_highscore(self, score):
        ''' Funckja aktualizuje high score danego użytkownika'''


        # ponizsza funkcja zwraca tuple
        current_hs, idx = self.get_highscore()
        
        if score > current_hs:
            sql = ''' UPDATE user
                SET high_score = ? WHERE id = ?'''
            self.cursor.execute(sql, (score, idx ))
            self.connection.commit()
            
    def get_games_played(self):
        ''' Funkcja zwraca liczbe zagranych gier aktualnego użytkownika oraz jego id'''
        
        sql = '''SELECT games_played FROM user WHERE id = ?
        '''
        idx = self.get_current_user_id()
        
        return self.cursor.execute(sql, (idx,)).fetchone()[0], idx
    
    def update_games_played(self):
        '''Zaktualizuj liczbę zagranych gier'''
        games_played, idx  = self.get_games_played()
        sql = ''' UPDATE user
                SET games_played = ? WHERE id = ?'''
        self.cursor.execute(sql, (games_played + 1, idx))
        self.connection.commit()

    def get_total_time_ig(self):
        ''' Funkcja zwraca calkowity czas gry aktualnego użytkownika oraz jego id'''
        
        sql = '''SELECT time_spent FROM user WHERE id = ?
        '''
        idx = self.get_current_user_id()
        
        return self.cursor.execute(sql, (idx,)).fetchone()[0], idx

    def update_total_time_ig(self, time):
        '''dostaje czas w ms, przelicza na sekundy i dodaje do calkowitego
        i wpisuje to do bazy'''
        ttig, idx = self.get_total_time_ig()
        time_updated = ttig + round(time, -3)/1000
        sql = ''' UPDATE user
                SET time_spent = ? WHERE id = ?'''
        self.cursor.execute(sql, (time_updated, idx ))
        self.connection.commit()

    def get_username(self):
        ''' Funkcja zwraca nazwe aktualnego użytkownika oraz jego id'''
        
        sql = '''SELECT name FROM user WHERE id = ?
        '''
        idx = self.get_current_user_id()
        
        return self.cursor.execute(sql, (idx,)).fetchone()[0]
    
    def set_username(self, name):
        '''ustawia nazwe aktualnego uzytkownika'''
        sql = ''' UPDATE user
                SET name = ? WHERE id = ?'''
        idx = self.get_current_user_id()
        self.cursor.execute(sql, (name, idx ))
        self.connection.commit()
        
    def is_car_unlocked(self, car_id) ->bool:
        '''zwraca True jezeli auto jest odblokowane lub False jezeli nie jest'''
        return self.cursor.execute("SELECT is_unlocked FROM cars WHERE id = ?", (car_id,)).fetchone()[0]

    def unlock_car(self, car_id: int):
        '''dostaje id auta do odblokowania, sprawdza czy auto nie jest juz odblokowane i odblokowuje.
        zwraca True jezeli odblokowano i False jezeli nie odblokowano'''
        is_unlocked = self.is_car_unlocked(car_id)
        if not is_unlocked:
            sql = f''' UPDATE cars
                SET is_unlocked = ? WHERE id = ?'''
            self.cursor.execute(sql, (1, car_id ))
            self.connection.commit()
            
    def get_path_to_car_image(self, car_id):
        ''' Funkcja zwraca sciezke do obrazka dla samochodu o danym id'''
        
        sql = '''SELECT path_to_graphics FROM cars WHERE id = ?
        '''
        
        return self.cursor.execute(sql, (car_id,)).fetchone()[0]
    
    def get_car_name(self, car_id):
        ''' Funkcja zwraca nazwe auta o danym id'''
        
        sql = '''SELECT name FROM cars WHERE id = ?
        '''
        
        return self.cursor.execute(sql, (car_id,)).fetchone()[0]
    
    
    '''ponizej funkcje do mapowania'''
    def get_current_car(self):
        ''' Funkcja zwraca aktualnie wybrane auto przez aktualnego uzytkownika'''
        
        sql = '''SELECT car_id FROM mapowania'''
        
        return self.cursor.execute(sql).fetchone()[0]
    
    def set_current_car(self, car_id):
        ''' Funkcja ustawia auto wybrane przez aktualnego uzytkownika'''
        sql = ''' UPDATE mapowania
                SET car_id = ?'''
        self.cursor.execute(sql, (car_id, ))
        self.connection.commit()
    
    ''' TYCH PONIZEJ UZYWAC TYLKO W SKRAJNYCH WYPADKACH '''

    def lock_cars(self):
        sql = f''' UPDATE cars
                SET is_unlocked = ? WHERE id = ?'''
        self.cursor.execute(sql, (0, 1 ))
        self.cursor.execute(sql, (0, 2 ))
        self.connection.commit()

if __name__ == '__main__':
    sd = DatabaseUtil()
    #sd.lock_cars()
    #sd.set_coins(300)
    sd.set_username('uzytkownik')
    print('123')
    #sd.update_highscore(200)
    