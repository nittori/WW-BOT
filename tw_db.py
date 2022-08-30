#https://qiita.com/hoto17296/items/0ca1569d6fa54c7c4732
#https://tdoc.info/blog/2012/12/05/psycopg2.html
import os
import psycopg2
import time


def get_connection():
    dsn = os.environ.get('DATABASE_URL')
    return psycopg2.connect(dsn)


def create_db_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            #tabel の作成
            cur.execute('CREATE TABLE twids(tw_id varchar);')
        conn.commit()
        
def insert_db(tw_id,retwed):
    with get_connection() as conn:
        with conn.cursor() as cur:
            #dataのレコード
            cur.execute('INSERT INTO twids (tw_id , retwed ) VALUES (%s ,%s)', (f'{tw_id}',f'{retwed}'))
            
            print(f"\ninsert {tw_id}\n")
        conn.commit()
            
def remove_db(tw_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM twids WHERE tw_id=%s',(f'{tw_id}',))
            
            print(f"\nremove {tw_id}\n")
        conn.commit()
        
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
                print(row)
            
def count_db():    
    with get_connection() as conn:
        with conn.cursor() as cur:            
            cur.execute('SELECT * FROM twids')
            cnt = len(cur.fetchall())
            print(cnt)
    return cnt
            
def add_column():#ALTER TABLE テーブル名 ADD COLUMN カラム名 データ型;
    with get_connection() as conn:
        with conn.cursor() as cur:            
            cur.execute('ALTER TABLE twids ADD COLUMN retwed varchar;')
        conn.commit()
        
def update_retwed(tw_id,retwed):#UPDATE テーブル名 SET 列名 = 式 WHERE 条件式;
    with get_connection() as conn:
        with conn.cursor() as cur:            
            cur.execute(f"UPDATE twids SET retwed = '{retwed}' WHERE tw_id = '{tw_id}';")
            #cur.execute("UPDATE twids SET retwed = 'yes';")
        conn.commit()
        
def get_no_retwed():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM twids WHERE retwed = 'no';")
            colnames = [col.name for col in cur.description]
            print(colnames)
            tws = []
            for row in cur:
                tws.append(row[0])
            return tws
            
        
if __name__ == "__main__":
    #create_db_table()
    #update_retwed()
    #tw_id = "dammy2"
    #retwed = "yes"
    #insert_db(tw_id, retwed)
    print(check_db("dammy2"))
    print_db()
    count_db()
    