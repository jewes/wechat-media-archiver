import json
import logging
import os.path
import threading
import time

from itchat.content import *


class DictToObject:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def format_unix_time_with_timezone(unix_time):
    from datetime import datetime, timezone

    utc_time = datetime.fromtimestamp(unix_time, timezone.utc)
    local_time = utc_time.astimezone()
    return local_time.strftime('%Y-%m-%d %H:%M:%S')


class GroupChatAssistant(object):

    def __init__(self, group_chat_name, download_dir):
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        self.group_chat_name = group_chat_name
        self.group_root = os.path.join(download_dir, group_chat_name)
        if not os.path.exists(self.group_root):
            os.makedirs(self.group_root, exist_ok=True)

        # load status file
        self.status = self.load_status()

    def load_status(self):
        status_file = os.path.join(self.group_root, "status.json")
        if os.path.exists(status_file):
            with open(status_file, "r") as f:
                raw_dict = json.load(f)
        else:
            raw_dict = json.loads('{"last_message_time": -1, "last_message_user": ""}')
        return DictToObject(**raw_dict)

    def update_status(self, last_message_time, last_message_user):
        self.status.last_message_time = last_message_time
        self.status.last_message_user = last_message_user

        status_file = os.path.join(self.group_root, "status.json")
        with open(status_file, "w") as f:
            json.dump(self.status.__dict__, f, ensure_ascii=False, indent=4)

    def get_status(self):
        if self.status.last_message_time < 0:
            return f"{self.group_chat_name}: 暂未保存任何照片"
        else:
            return f"{self.group_chat_name}: 最后一张照片来自于{self.status.last_message_user}, {format_unix_time_with_timezone(self.status.last_message_time)}"

    def handle_message(self, msg):
        send_user_name = msg.ActualNickName
        message_type = msg.Type
        content = msg.Content
        create_time = msg.CreateTime

        if message_type == TEXT:
            logging.info(f"{send_user_name} says in {self.group_chat_name}: {content}")
            return

        if self.status.last_message_time > 0 and create_time < self.status.last_message_time:
            logging.warning(f"ignore old message, last: {self.status.last_message_time}, current: {create_time}")
            logging.info(f"msg: {msg}")
            return

        # handle image and video
        logging.info(f"{send_user_name} sends a {message_type} in {self.group_chat_name}, create_time: {create_time}")

        file_path = os.path.join(self.group_root, msg.fileName)
        unique_path = self.get_unique_filename(file_path)

        t0 = time.time()
        msg.download(unique_path)
        self.update_status(create_time, send_user_name)
        logging.info(f"saved to {unique_path}, cost:{time.time() - t0}s")

    @staticmethod
    def get_unique_filename(filename):
        base_name, extension = os.path.splitext(filename)
        counter = 1
        new_filename = filename

        while os.path.exists(new_filename):
            new_filename = f"{base_name}-{counter:02}{extension}"
            counter += 1

        return new_filename


class AssistantManager(object):

    def __init__(self, download_dir):
        self.download_dir = download_dir
        self.objects = dict()
        self.lock = threading.Lock()
        for entry in os.listdir(self.download_dir):
            if entry.startswith("@") or entry.startswith("."):
                continue
            if os.path.isdir(os.path.join(self.download_dir, entry)):
                self.get_group_chat_assistant(entry, self.download_dir)
                logging.info(f"init {entry}")

    def get_group_chat_assistant(self, group_chat_name, download_dir) -> GroupChatAssistant:
        with self.lock:
            if group_chat_name not in self.objects:
                self.objects[group_chat_name] = GroupChatAssistant(group_chat_name, download_dir)
            return self.objects[group_chat_name]

    def get_status(self):
        with self.lock:
            arr = []
            for obj in self.objects.values():
                s = obj.get_status()
                if s:
                    arr.append(s)
            return arr
