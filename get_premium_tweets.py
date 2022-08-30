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

def tw_search(api,keyword):
    #RTを除外して検索
    #sandboxはpremium検索が行える無料版API、search_30_dayは250回/月のリクエストが可能
    query = f"{keyword} - RT"
    label = os.environ.get('DEV_LABEL')
    tweets = api.search_30_day(label, query, maxResults=10)
    
    tw_ids = []
    for tweet in tweets:
        user_id: str = tweet.user.screen_name
        tw_id: str = str(tweet.id)
        tw_date = tweet.created_at
        favo: int = tweet.favorite_count
        text: str = tweet.text.replace('\n','')
        
        #検索を完全一致に
        if "魔女兵器" in text:
            #取得したツイートがデータベースに登録済みならスルー
            if tw_db.check_db(tw_id) == True:
                print(f"{tw_id} has already been registered")
                continue
            #未登録ツイートの処理、データベースにも登録
            else:
                #取得ツイート確認
                print(user_id,tw_date,text)
                tw_db.insert_db(tw_id, "no")

    return tw_ids

def main():
    api = get_api()
    #検索キーワード
    keyword = "魔女兵器"
 
    tw_search(api,keyword)
    
if __name__ == "__main__":
    main()
