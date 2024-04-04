import configparser
import logging
import os
import sys
import time

import itchat
from itchat.content import *

# load config
config_file_path = os.getenv('PA_CONFIG_PATH', './config.ini')
print(f"Using config file: {config_file_path}")
config = configparser.ConfigParser()
config.read(config_file_path, encoding='utf-8')

# init critical directories
download_dir = config.get("default", "download_dir", fallback="downloads")
log_dir = config.get("default", "log_dir", fallback="logs")

if not os.path.exists(download_dir):
    os.makedirs(download_dir, exist_ok=True)

if not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

if os.path.isfile(download_dir) or os.path.isfile(log_dir):
    print(f"download dir: {download_dir} or log_dir ({log_dir}) is a file, a folder is expected")
    sys.exit(1)

# set logging level
logging.basicConfig(filename=f"{log_dir}/assistant.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


@itchat.msg_register([TEXT, PICTURE, VIDEO], isGroupChat=True)
def handle_group_chat_message(msg: itchat.Message):
    logging.debug(f"received message: {msg}")
    if msg is None:
        return

    group_chat_id = msg.FromUserName
    group_chat = itchat.search_chatrooms(userName=group_chat_id)
    if group_chat is None:
        logging.error(f"failed to find group chat: {group_chat_id}")
        return

    group_chat_name = group_chat.NickName
    send_user_name = msg.ActualNickName
    content = msg.Content

    message_type = msg.Type
    if message_type == "Text":
        logging.info(f"{send_user_name} says in {group_chat_name}: {content}")
        return

    # handle image and video
    logging.info(f"{send_user_name} sends a {message_type} in {group_chat_name}")

    group_dir = os.path.join(download_dir, group_chat_name)
    if not os.path.exists(group_dir):
        os.makedirs(group_dir)
    file_path = os.path.join(group_dir, msg.fileName)
    if not os.path.exists(file_path):
        t0 = time.time()
        msg.download(file_path)
        logging.info(f"saved to {file_path}, cost:{time.time() - t0}s")


# main function
if __name__ == "__main__":
    # 默认通过环境变量来配置config.ini文件路径， 默认采用./config.ini
    # export PA_CONFIG_PATH=./config_server.ini

    # 登录
    itchat.auto_login(hotReload=True, enableCmdQR=2)
    itchat.run(True)
