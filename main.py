from flask import Flask, request, render_template
from instagrapi import Client
import os
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def igluckyman():
    winners =[]
    #檢查請求方法是否為POST
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        post_URL = request.form.get('post_URL')
        specified_comment = request.form.get('specified_comment')
        winner_num = int(request.form.get('winner_num'))
        cl = login(username, password)
        result = scrape(cl, post_URL, specified_comment, winner_num)
        #是POST，返回winners列表
        return render_template('index.html', winners=result['winners'], total_comments=result['total_comments'], match_comments=result['match_comments'])
    
    #不是POST，也返回winners列表，但會是空的
    return render_template('index.html', winners=winners)

#登入IG帳號及密碼
def login(username, password):
    cl = Client()
    cl.login(username, password, relogin=True)
    return cl

#定義爬蟲
def scrape(cl, post_URL, specified_comment, winner_num):
    media_id = cl.media_pk_from_url(post_URL)
    comments = cl.media_comments(media_id, amount = 1000)

    #列表解析式，api中的comment包含username及text等屬性
    complete_message_list = [{'username': comment.user.username, 'text': comment.text} for comment in comments if specified_comment in comment.text]

    #不抽取重複的留言
    usernames = set()
    unique_comments = []
    for comment in comments:
        if specified_comment in comment.text and comment.user.username not in usernames:
            unique_comments.append({'username': comment.user.username, 'text': comment.text})
            usernames.add(comment.user.username)

    print(f'該篇貼文中共有{len(comments)}則留言')
    print(f'其中符合留言條件的有{len(complete_message_list)}則留言')

    #抽獎
    if len(unique_comments) <= winner_num:
        print('留言數不足以進行抽獎')
        return []
    
    return {
        'winners': random.sample(unique_comments, winner_num),
        'total_comments': len(comments),
        'match_comments': len(complete_message_list)
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
    #app.run(os.getenv('PORT'))