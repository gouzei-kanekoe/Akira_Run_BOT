from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import random
import time

app = Flask(__name__)

# LINE API 設定
LINE_ACCESS_TOKEN = "你的 LINE Channel Access Token"
LINE_SECRET = "你的 LINE Channel Secret"

LINE_BOT_API = os.getenv("LINE_BOT_API")
LINE_SECRET = os.getenv("LINE_SECRET")

# 真木的逃避對話庫
stage1_replies = [
    "這件事，對我來說好像……有點遙遠。",
    "這件事已經過去了，誰也無法改變。",
    "那不重要。因為……那件事，已經過去了。",
    "有些事，說了也沒用。",
    "每個人都有選擇的自由。",
    "知惠子……對不起……",
    "抱歉，知惠子。我不能告訴你原因。",
]

stage2_replies = [
    "你依然沒有給過我喘息的機會，一次又一次！",
    "你根本不理解我的心境……",
    "我有選擇面對的自由，亦有選擇逃避痛苦的自由！",
]

stage3_replies = [
    "這樣的我……不值得被任何人愛……",
    "我傷害了很多人，知惠子。甚至連你……我也不知道，自己是否真的有資格承擔這份愛。",
]

final_replies = [
    "知惠子，你可以……陪著我，一起面對嗎？",
    "如果有一天，我不再逃避了……你還會在嗎？",
]

angry_replies = [
    "你她媽的石川明！",
    "那件事我不想提起！！",
    "你夠了，知惠子！！！",
]

urgent_reply = "知惠子，等等！"

# 記錄用戶發送的次數
user_message_count = {}

def get_reply(user_id, message_text):
    if any(trigger in message_text for trigger in ["幸福", "放棄"]):
        return urgent_reply
    
    count = user_message_count.get(user_id, 0)
    
    if count >= 10:
        return random.choice(stage3_replies) + "（真木已消失 1 小時）"
    elif count >= 5:
        return random.choice(stage2_replies)
    else:
        return random.choice(stage1_replies)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return jsonify({"status": "error", "message": "Invalid Signature"}), 400
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    message_text = event.message.text.strip()
    
    if user_id not in user_message_count:
        user_message_count[user_id] = 0
    
    user_message_count[user_id] += 1
    
    # 觸發真木暴怒
    if any(trigger in message_text for trigger in ["停職信", "三野望", "石川明"]):
        reply_text = random.choice(angry_replies)
    else:
        reply_text = get_reply(user_id, message_text)
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
