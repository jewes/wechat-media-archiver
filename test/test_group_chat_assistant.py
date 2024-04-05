from unittest import TestCase
import assistant


class TestGroupChatAssistant(TestCase):
    def test_load_status(self):
        g = assistant.GroupChatAssistant("chat1", "downloads")
        g.update_status(123, "fannong")
        status = g.load_status()
        print(status.__dict__)
        assert status.last_message_user == "fannong"
        assert status.last_message_time == 123

        g.update_status(456, "凡农")
        status = g.load_status()
        print(status.__dict__)
        assert status.last_message_user == "凡农"
        assert status.last_message_time == 456
