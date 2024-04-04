class Message:

    def __init__(self):
        self.FromUserName = ""
        self.ToUserName = ""
        self.Content = ""
        self.StatusNotifyUserName = ""
        self.ImgWidth = 0
        self.PlayLength = 0
        self.RecommendInfo = {}
        self.StatusNotifyCode = 0
        self.NewMsgId = ""
        self.Status = 0
        self.VoiceLength = 0
        self.ForwardFlag = 0
        self.AppMsgType = 0
        self.Ticket = ""
        self.AppInfo = {}
        self.Url = ""
        self.ImgStatus = 0
        self.MsgType = 0
        self.ImgHeight = 0
        self.MediaId = ""
        self.MsgId = ""
        self.FileName = ""
        self.HasProductId = 0
        self.FileSize = ""
        self.CreateTime = 0
        self.SubMsgType = 0

        # for group chat only
        self.isAt = False
        self.ActualNickName = ""
        self.Content = ""

