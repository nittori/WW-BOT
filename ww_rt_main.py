import tweepy
import time
import os
import tw_db
import random 

def get_api():
    #API_KEYとかはWEB上に公開すると無効になるので、環境変数に登録して使う
    API_KEY = os.environ.get('API_KEY')
    API_SECRET = os.environ.get('API_SECRET')
    ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api

def get_tw_indb():
    #RTしてないツイートをデータベースから取得
    tw_ids = tw_db.get_no_retwed()
    return tw_ids

def tw_retweet(api,tw_id):
    try:
        api.retweet(tw_id)
        tw_db.update_retwed(tw_id,"yes")
        #念のためtime.sleep
        print(f"RT {tw_id}")
        time.sleep(10)
        return True
    except:
        print("retweet error")
        time.sleep(10)
        return False

def main():
    api = get_api()
    
    tw_ids = get_tw_indb()
    #取得したtw_idの1つだけをRT、その他は次回に回す。
    for tw_id in tw_ids:
        tw_retweet(api, tw_id)
        break
            
if __name__ == "__main__":
    main()
