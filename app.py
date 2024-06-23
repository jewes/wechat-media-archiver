import configparser
import logging
import os
import sys
import time

import assistant
import itchat
from itchat.content import *

# load config
config_file_path = os.getenv('PA_CONFIG_PATH', './config.ini')
print(f"Using config file: {config_file_path}")
config = configparser.ConfigParser()
config.read(config_file_path, encoding='utf-8')

admin_nickname = config.get("default", "admin_nickname", fallback=None)

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
enabled_debug = config.get("default", "debug", fallback="0")
log_level = logging.DEBUG if enabled_debug == "1" else logging.INFO
logging.basicConfig(filename=f"{log_dir}/assistant.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=log_level)

start_time = time.time()
assistant_mgr = assistant.AssistantManager(download_dir)

@itchat.msg_register([TEXT, PICTURE, VIDEO], isGroupChat=True)
def handle_group_chat_message(msg: itchat.Message):
    logging.debug(f"received group chat message: {msg}")
    if msg is None:
        return

    group_chat_id = msg.FromUserName
    group_chat = itchat.search_chatrooms(userName=group_chat_id)
    if group_chat is None:
        logging.error(f"failed to find group chat: {group_chat_id}")
        return

    group_chat_name = group_chat.NickName
    group_assistant = assistant_mgr.get_group_chat_assistant(group_chat_name, download_dir)
    group_assistant.handle_message(msg)


@itchat.msg_register([TEXT])
def handle_text_message(msg: itchat.Message):
    logging.debug(f"received single chat message: {msg}")
    if msg is None:
        return

    nickName = msg.user.NickName
    text: str = msg.text
    logging.info(f"received message from: {nickName}: {text}")

    # only allow admin to get the status
    if admin_nickname is None or nickName != admin_nickname:
        return

    # special handling status
    if "状态" in text:
        results = []

        secs = time.time() - start_time
        results.append(f"服务状态：已运行 {seconds_to_human_readable(secs)}")

        group_chat_status = assistant_mgr.get_status()
        if not group_chat_status:
            results.append("群相册状态：暂未保存任何群的照片")
        else:
            results.append("群相册状态：")
            for s in group_chat_status:
                results.append(f"- {s}")
        return "\n".join(results)


def seconds_to_human_readable(seconds):
    days = int(seconds // (3600 * 24))
    hours = int((seconds // 3600) % 24)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = int(seconds % 60)

    if days > 0:
        return f"{days}天{hours}小时{minutes}分钟{remaining_seconds}秒"
    elif hours > 0:
        return f"{hours}小时{minutes}分钟{remaining_seconds}秒"
    elif minutes > 0:
        return f"{minutes}分钟{remaining_seconds}秒"
    else:
        return f"{remaining_seconds}秒"


# main function
if __name__ == "__main__":
    # 默认通过环境变量来配置config.ini文件路径， 默认采用./config.ini
    # export PA_CONFIG_PATH=./config_server.ini

    # 登录
    itchat.auto_login(hotReload=True, enableCmdQR=2)
    itchat.run(True)
