import os
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import random
import psycopg2


app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    msg = event.message.text;
    userid = event.source.user_id;
    dbtimestamp = event.timestamp;
    from django.db import transaction, DatabaseError
    try:
        conn = psycopg2.connect(database="dcd5jca9btqeoi", user="azmkghqpoeannh", password="9a117f2c22ec39525492ef4c21c9c6d09ce2a3758336b3fa6581c87b564980b6", host="ec2-52-1-20-236.compute-1.amazonaws.com", port="5432")
        cur = conn.cursor();
        sql = "INSERT INTO linebotmsg (name, msg,date) VALUES (%s, %s , %s)"
        val = (userid, msg,dbtimestamp)
        cur.execute(sql,val);
        conn.commit();
        conn.close();
    except DatabaseError:
        transaction.rollback()
    if userid=="U3c822c99099ebc65694c3b8401be9707" :
        get_message = "哈囉~阿旻"
    else:
        textInt = random.randint(1, 9);
        if textInt == 1:
            get_message = "欸!真的~~"
        if textInt == 2:
            get_message = "哇，對耶，妳很棒喔!"
        if textInt == 3:
            get_message = "是喔!哇真的是很酷耶"
        if textInt == 4:
            get_message = "哈哈，我也這麼覺得耶"
        if textInt == 5:
            get_message = "沒事啦，都會好的"
        if textInt == 6:
            get_message = "😎😎😎"
        if textInt == 7:
            get_message = "哇太誇張了吧QAQ"
        if textInt == 8:
            get_message = "我都不知道耶，我好震驚喔"
        if textInt == 9:
            get_message = "摁....有道理餒"
        
    
    
    
    # Send To Line
    reply = TextSendMessage(text=f"{get_message}")
    line_bot_api.reply_message(event.reply_token, reply)
