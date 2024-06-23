from unittest import TestCase
import assistant


class TestGroupChatAssistant(TestCase):
    def test_load_status(self):
        g = assistant.GroupChatAssistant("chat1", "downloads")
        g.update_status(123, "bob")
        status = g.load_status()
        print(status.__dict__)
        assert status.last_message_user == "bob"
        assert status.last_message_time == 123

        g.update_status(456, "alice")
        status = g.load_status()
        print(status.__dict__)
        assert status.last_message_user == "alice"
        assert status.last_message_time == 456
