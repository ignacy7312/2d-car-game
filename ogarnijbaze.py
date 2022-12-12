import sqlite3
from sqlite3 import Error

from zrobbaze import create_connection

db_file = 'baza2.db'



def get_current_user_id(cur):
    ''' Funkcja zwraca id aktualnego użytkownika '''
    id_exec = '''SELECT user_id FROM mapowania
        '''
    return cur.execute(id_exec).fetchone()[0]


def get_coins(cur):
    ''' Funkcja zwraca ilość monet aktualnego użytkownika oraz jego id'''

    sql = '''SELECT coins FROM user WHERE id = ?
    '''
    idx = get_current_user_id(cur)
    
    return cur.execute(sql, (idx,)).fetchone()[0], idx

def update_coins(conn, coins):
    ''' Funckja dostaje ilość monet i o tyle zwiększa je w bazie danych dla danego użytkownika'''
    
    cur = conn.cursor()
    # dostaje z funkcji zarówno ilość  monet jak i indeks aktualnego użytkownika
    current_coins, idx = get_coins(cur)
    print(current_coins, idx)

    sql = ''' UPDATE user
            SET coins = ? WHERE id = ?
            '''
    
    cur.execute(sql, (current_coins + coins, idx ))
    conn.commit()



def get_highscore(cur):
    ''' Funkcja zwraca high score aktualnego użytkownika oraz jego id'''
    
    sql = '''SELECT high_score FROM user WHERE id = ?
    '''
    idx = get_current_user_id(cur)
    
    return cur.execute(sql, (idx,)).fetchone()[0], idx

def update_highscore(conn, score):
    ''' Funckja aktualizuje high score danego użytkownika'''

    cur = conn.cursor()

    # ponizsza funkcja zwraca tuple
    current_hs, idx = get_highscore(cur)
    
    if score > current_hs:
        sql = ''' UPDATE user
            SET high_score = ? WHERE id = ?'''
        cur.execute(sql, (score, idx ))
        conn.commit()


def main(db_file):
    conn = create_connection(db_file)
    cur = conn.cursor()
    print(get_coins(cur))
    update_coins(conn, 20)
    print(get_coins(cur))
    update_highscore(conn, 200)
    print(get_highscore(cur))
    

if __name__ == "__main__":
    main(db_file)