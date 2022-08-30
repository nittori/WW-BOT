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
    q = f"{keyword} exclude:retweets"
    #無料版スタンダードAPIは1秒で50ツイートを取得できる
    #result_typeは取得するツイートをrecentとpopularityの両観点から選択
    tweets = api.search_tweets(q=q, count=10 ,result_type="mixed", tweet_mode='extended')
    
    tw_ids = []
    for tweet in tweets:
        user_id: str = tweet.user.screen_name
        tw_id: str = str(tweet.id)
        tw_date = tweet.created_at
        favo: int = tweet.favorite_count
        text: str = tweet.full_text.replace('\n','')
        
        #BDへのリクエスト過多を防ぐためのsleep
        time.sleep(1)
        #誤RTをなくすためテキストに魔女兵器が入っていることを確認
        if "魔女兵器" in text:
            #取得したツイートがデータベースに登録済みならスルー
            if tw_db.check_db(tw_id) == True:
                print(f"{tw_id} has already been registered")
                continue
            
            #未登録ツイートの処理、データベースにも登録
            else:
                #取得ツイート確認
                print(user_id,tw_date,text)
                tw_db.insert_db(tw_id,"no")
     
def main():
    api = get_api()
    #検索キーワード
    keyword = "#魔女兵器"
    tw_search(api,keyword)
    
            
if __name__ == "__main__":
    main()
