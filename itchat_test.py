# _*_ coding:utf-8 _*_
"""
想要实现的功能：
1. 给固定好友发消息
2. 自动回复消息
3. 自动下载图片
"""
import itchat
import time
from itchat.content import *


def log():
    itchat.auto_login(hotReload=True)  # 开启热登录，会生成一个文件用来保存登录信息，这样就不用每次运行需要扫码登录了
    friends = itchat.get_friends(update=True)[0:]  # true 表示获取云端所有的朋友列表
    chatroom = itchat.get_chatrooms(update=True)[0:]  # 仅获取保存在通讯录中的群聊名称
    return friends, chatroom


def send_message(item, name, msg):
    if item == 1:
        if name in friend_nickname:
            user_name = itchat.search_friends(name=name)[0]['UserName']
        res = itchat.send_msg(msg=msg, toUserName=user_name)
    else:
        if name in chatroom_nickname:
            chatroom_name = itchat.search_chatrooms(name=name)[0]['UserName']
            res = itchat.send_msg(msg=msg, toUserName=chatroom_name)
    if res:
        print("发送成功！")
    else:
        print("发送失败!")


@itchat.msg_register([TEXT])
def auto_reply(msg):
    reply_ocntent = "已经收到您于{0}发送的消息。".format(time.strftime("%Y %m %d %H:%M:%S", time.localtime(time.time())))
    itchat.send_msg(msg=reply_ocntent, toUserName=msg['FromUserName'])
    print("已经收到{0}于{1}发送的消息。".format(msg['FromUserName'], time.strftime("%Y %m %d %H:%M:%S", time.localtime(time.time()))))


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def auto_download(msg):
    msg.download(msg['FileName'])


if __name__ == '__main__':
    friends, chatrooms = log()
    friend_nickname = [i['NickName'] for i in friends]  # 返回所有的朋友昵称
    chatroom_nickname = [j['NickName'] for j in chatrooms]  # 返回所有保存在通讯录中的群聊名称
    while True:  # 通过while循环实现某一流程的重复执行
        try:
            item = input("item:(发消息给用户请输入1，给群聊请输入2)")
            if item == 'break':
                break
            name = input("请输入用户或群聊名称：")  # 这里要求用户名必须存在
            msg = input("请输入想发送的消息：")
            send_message(int(item), name, msg)
        except Exception as e:
            print("出现错误：", e)
        finally:
            print("退出请在item输入break")


