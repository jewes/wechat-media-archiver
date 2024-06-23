## 介绍

这是一个简单的微信机器人，它监听微信群中视频和图片保存到本地硬盘上。 我的主要使用场景是将微信家族群聊的照片和视频归档到我的群辉NAS上。
这是一个为个人使用的周末项目。尽管它可能并不能百分之百满足你的需求，但你可以将它作为一个起点。

## 如何使用
### 环境准备
准备一个微信账号（后文简称小号），该账号必须通过实名验证。如果要长期使用，建议注册一个微信小号，避免因为未知原因导致账号被禁用。

安装相关依赖，MacOS和Linux均可，Windows未验证

```shell
pip3 install -r requirements.txt
```

### 本机验证

参考目录中config_debug.ini文件，其中download_dir指定文件保存目录

```shell
[default]
download_dir=downloads
log_dir=logs
debug=1
admin_nickname="<your_name>"
```

执行`./debug_start.sh`，控制台中将出现一个二维码，用小号扫码完成登录，就像登录微信网页或者桌面版本一样。 将微信小号添加到微信群聊中，然后群聊中的图片和视频会自动保存到上面配置的下载目录中。

### 部署到群辉
将代码拷贝到群辉中，参考config_debug.ini，新建配置文件`config.ini`，然后执行`start-prod.sh`将程序运行到后台。执行完成后打开stdout.log，用小号扫里面的二维码完成登录即可。

#### 查看小号工作状态

将你的微信主号昵称配置到配置文件中，然后用主号给小号发消息（消息中包含`状态`），如果一切工作正常的话，小号会回复一条消息。

## 如何工作的
项目的难点是如何设置环境以获取微信消息。一旦获取到了微信消息，就可以根据自己的需求来处理。我们使用的是开源库[itchat-uos](https://github.com/why2lyj/ItChat-UOS)来模拟微信客户端登录微信的。
我将itchat-uos的代码放到了代码库中，是为了方便调试登录失败的问题，并没有修改里面的逻辑。主要的代码是在app.py和src/assistant目录中。

## FAQ
1. 稳定吗？差不多稳定运行20多天后，然后微信因为未知原因就退出了，需要重新登陆一下。

## 致谢
1. https://github.com/littlecodersh/ItChat
2. https://github.com/why2lyj/ItChat-UOS
3. https://github.com/yikang-li/CalAgent