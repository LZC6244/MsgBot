# MsgBot
Python 实现的一个消息通知助手。可以使用钉钉群聊天机器人或者微信。

- 开发环境： `python 3.9`
- 环境需求： `python 3`

## 安装
```shell
pip install MsgBot
```

## DingTalkBot 
群机器人是钉钉群的高级扩展功能。群机器人可以将第三方服务的信息聚合到群聊中，实现自动化的信息同步。


### DingTalkBot 前置条件
起码拥有一个钉钉群聊天机器人（获取自定义机器人webhook`Webhook`）（[如何申请](#dingtalk)）


### DingTalkBot demo

```python
from MsgBot import DingTalkBot

# TestBot
dt_bot = DingTalkBot(
  web_hook='your web_hook',
  secret='your secret')

content_text = '今天天气真好，是么？'
dt_bot.send_text(content_text)
```

### DingTalkBot 消息类型及 demo
- text 类型  
  ![](https://github.com/LZC6244/DingTalkBot/blob/master/imgs/ding_talk/01.png)

- link 类型  
  ![](https://github.com/LZC6244/DingTalkBot/blob/master/imgs/ding_talk/02.png)
  
- markdown 类型  
  ![](https://github.com/LZC6244/DingTalkBot/blob/master/imgs/ding_talk/03.png)
  
  **ps:** 目前只支持md语法的子集，具体支持的元素如下（钉钉限定）
    
  ```text
  标题
  # 一级标题
  ## 二级标题
  ### 三级标题
  #### 四级标题
  ##### 五级标题
  ###### 六级标题
  
  引用
  > A man who stands for nothing will fall for anything.
  
  文字加粗、斜体
  **bold**
  *italic*
  
  链接
  [this is a link](http://name.com)
  
  图片
  ![](http://name.com/pic.jpg)
  
  无序列表
  - item1
  - item2
  
  有序列表
  1. item1
  2. item2
  ```  

- 整体跳转 ActionCard 类型  
  ![](https://github.com/LZC6244/DingTalkBot/blob/master/imgs/ding_talk/04.png)
  
- 独立跳转 ActionCard 类型  
  ![](https://github.com/LZC6244/DingTalkBot/blob/master/imgs/ding_talk/05.png)
  
- FeedCard 类型  
  ![](https://github.com/LZC6244/DingTalkBot/blob/master/imgs/ding_talk/06.png)
  


## WxComBot
利用企业微信应用给微信用户或者企业微信用户发送消息。  

### 使用微信接收企业微信消息助手消息，免安装企业微信客户端：
登陆企业微信后台[微信插件](https://work.weixin.qq.com/wework_admin/frame#profile/wxPlugin)，然后使用要接收消息的微信扫描二维码关注  
关注过后即可接收到消息助手消息  
如若要推广给他人，在微信进入该企业，点击【右上角➕号】-【设置】-【右上角`...`】-【推荐给朋友即可】

### WxComBot 前置条件
- 拥有/创建一个用于消息通知的应用  
  可以/建议自己[注册](https://work.weixin.qq.com/wework_admin/register_wx?from=myhome)一个企业，非常简单，不需要进行认证即可使用  
  或者管理员给你创建好应用然后给你 secret 、应用id 、用户id等相关信息（= = 太麻烦了不建议）  
- 关键参数的获取：  
  - [access_token](https://work.weixin.qq.com/api/doc/90000/90135/91039)
  - [corpid](https://work.weixin.qq.com/api/doc/90000/90135/91039#14953/corpid)
  - [corpsecret](https://work.weixin.qq.com/api/doc/90000/90135/91039#14953/secret)
  
### WxComBot 避免重复通知
若微信通过上述**微信插件**关注了企业，而手机上又安装了企业微信  

那么，同一条消息是会在微信和企业微信通知的  

在微信不取关或者卸载企业微信的情况下，要避免也很简单  

微信或者企业微信进入消息通知应用设置**消息免打扰**即可  

某一方配置的免打扰不会影响另一方的正常通知
  
### WxComBot demo
```python
from MsgBot import WxComBot

wx_com_bot = WxComBot('corp_id', 'corp_secret')
msg = '你的快递已到，请携带工卡前往邮件中心领取。\n出发前可查看<a href="http://work.weixin.qq.com">邮件中心视频实况</a>，聪明避开排队。'
wx_com_bot.send_msg_text(agent_id='agent_id', content=msg, to_user='to_user')
```

### WxComBot 消息类型及 demo
- text 文本类型（可使用超链、换行）  
  ![](https://github.com/LZC6244/MsgBot/blob/master/imgs/wx_com/01.png)
  
- Markdown 类型（该类型仅能在企业微信客户端查看）  
  ![](https://github.com/LZC6244/MsgBot/blob/master/imgs/wx_com/02.png)
  

**应用支持推送文本、图片、视频、文件、图文、小程序、模板卡片等类型**

目前**仅实现**了文本、Markdown类型，其余类型可根据实际需要和文档进行实现

# 参考链接

- <span id="dingtalk">[钉钉开发文档](https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq)</span>
- [企业微信服务端API开发指南](https://work.weixin.qq.com/api/doc/90000/90135/90664)
- [企业微信发送应用消息](https://work.weixin.qq.com/api/doc/90000/90135/90236)