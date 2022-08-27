import tweepy
import time
import os
import tw_db 

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
    tweets = api.search_tweets(q=q, count=50 ,result_type="mixed", tweet_mode='extended')
    
    tw_ids = []
    for tweet in tweets:
        user_id: str = tweet.user.screen_name
        tw_id: str = str(tweet.id)
        tw_date = tweet.created_at
        favo: int = tweet.favorite_count
        text: str = tweet.full_text.replace('\n','')
        
        #リクエスト過多を防ぐためのsleep
        time.sleep(1)
        #検索を完全一致に
        if keyword in text:
            #取得したツイートがデータベースに登録済みならスルー
            if tw_db.check_db(tw_id) == True:
                print(f"{tw_id} has already been registered")
                continue
            #未登録ツイートの処理、データベースにも登録
            else:
                #取得ツイート確認
                print(user_id,tw_date,text)
                tw_ids.append(tw_id)
                tw_db.insert_db(tw_id)

    #Heroku Postgres無料版はデータを10000行まで登録できる
    #余裕をもって1000行まで行ったら、前から900行分削除
    if tw_db.count_db()>1000:
        tw_db.del_900()
    return tw_ids

def tw_retweet(api,tw_id):
    try:
        api.retweet(tw_id)
    except:
        print("retweet error")

def tw_favo(api,tw_id):
    try:    
        api.create_favorite(id=tw_id)
    except:
        print("favorite error")
     
def main():
    api = get_api()
    # 「#魔女兵器」はRTもいいねもする
    keyword = "#魔女兵器"
    retw_ids = tw_search(api,keyword)
    for retw_id in retw_ids:
        tw_retweet(api,retw_id)
        #tw_favo(api,retw_id)
    
    # 「魔女兵器」はなぜか完全一致検索にならず関係ないツイートもひっかかるので、いいねのみ
    keyword = "魔女兵器"
    favotw_ids = tw_search(api,keyword)
    for favotw_id in favotw_ids:
        tw_retweet(api,favotw_id)
        #tw_favo(api,favotw_id)
    
if __name__ == "__main__":
    main()
