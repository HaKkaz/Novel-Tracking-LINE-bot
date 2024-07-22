from utils.messaging import reply_message


def subscribe(event):
    msg: str = event.message.text
    msg = msg.split()
    if len(msg) != 2:
        reply_message(event.reply_token, "訂閱小說請輸入指令: 訂閱 <novel_id>")
        return

    with open('subscribers.txt', 'a') as f:
        user_id = event.source.user_id
        novel_id = msg[1]
        f.write(f'{user_id} {novel_id}\n')

def unsubscribe(event):
    pass