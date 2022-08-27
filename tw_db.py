#https://qiita.com/hoto17296/items/0ca1569d6fa54c7c4732
#https://tdoc.info/blog/2012/12/05/psycopg2.html
import os
import psycopg2
import time


def get_connection():
    dsn = os.environ.get('DATABASE_URL')
    return psycopg2.connect(dsn)

#最初にデータベースのテーブルを作るためだけの関数
def create_db_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            #tabel の作成
            cur.execute('CREATE TABLE twids(tw_id varchar);')
        conn.commit()
        
def insert_db(tw_id="dammy"):
    with get_connection() as conn:
        with conn.cursor() as cur:
            #dataのレコード
            cur.execute('INSERT INTO twids (tw_id) VALUES (%s)', (f'{tw_id}',))
            
            print(f"\ninsert {tw_id}\n")
        conn.commit()
            
def remove_db(tw_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM twids WHERE tw_id=%s',(f'{tw_id}',))
            
            print(f"\nremove {tw_id}\n")
        conn.commit()

#データのオーバーフローを防ぐために900行分削除する関数
def del_900():
    del_id_list = []
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM twids')
            
            for idx,row in enumerate(cur):
                if idx >= 900:
                    break
                print(row[0])
                del_id_list.append(row[0])
        conn.commit()
        
    for tw_id in del_id_list:
        remove_db(tw_id)
        time.sleep(1)
        
def check_db(tw_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            #ひとつずつ取得
            tw_id_list = []
            cur.execute('SELECT * FROM twids')
            for row in cur:
                tw_id_list.append(row[0])
        conn.commit()
    return tw_id in tw_id_list

def print_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM twids')
            colnames = [col.name for col in cur.description]
            print(colnames)
            for row in cur:
                print(row[0])
            
def count_db():    
    with get_connection() as conn:
        with conn.cursor() as cur:            
            cur.execute('SELECT * FROM twids')
            cnt = len(cur.fetchall())
            print(cnt)
    return cnt
            
            
if __name__ == "__main__":
    #create_db_table()
    remove_db("1562838315044577287")
    print_db()
    count_db()
