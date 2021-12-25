# -*- coding: utf-8 -*-

import re
import hmac
import json
import queue
import base64
import logging
import hashlib
import requests
from time import sleep
from urllib import parse
from datetime import datetime, timedelta
from MsgBot.exceptions import SendError, DingTalkError

logger = logging.getLogger(__name__)


class DingTalkBot(object):
    """
    钉钉群聊天机器人
    只能在在钉钉PC端生成和设置
    每个机器人每分钟限制最多发送20条消息
    钉钉官方文档：https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq/404d04c3
    """

    def __init__(self, web_hook: str, secret: str = None):
        """
        初始化聊天机器人
        聊天机器人可设置三种安全设置：
                                1. 关键词（消息中必须包含关键词，最多设置10个）
                                2. 加签（web_hook url 和 加签后参数组成新 url）
                                3. IP地址、段白名单
        :param web_hook: 钉钉机器人 Webhook 地址
        :param secret:
        """
        self.web_hook = web_hook
        self.web_hook_raw = web_hook
        self.secret = secret
        # 上次加签时间（钉钉限定请求所带时间戳与发送请求时的时间间隔不能超过 1 小时）
        self.sign_time = datetime.now() - timedelta(hours=1)
        # 存储发送消息时的时间的队列
        self.time_queue = queue.Queue(maxsize=20)
        # 钉钉限定发起POST请求时，必须将字符集编码设置成UTF-8。
        self.headers = {'Content-Type': 'application/json; charset=utf-8'}

    def update_web_hook(self, now: datetime):
        """
        计算加签，更新 web_hook （加上时间戳和签名参数）
        :param now: 当前时间
        :return:
        """
        timestamp = str(round(now.timestamp() * 1000))
        if not isinstance(self.secret, str) or not self.secret.startswith('SEC'):
            raise ValueError(f'Please check the secret: {self.secret}')
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = parse.quote_plus(base64.b64encode(hmac_code))
        # print(timestamp)
        # print(sign)
        self.web_hook = f'{self.web_hook_raw}&timestamp={timestamp}&sign={sign}'
        self.sign_time = now

    def _send_msg(self, form_data: dict, q_timeout: int = 60, r_timeout: int = 60):
        now = datetime.now()
        if self.secret:
            # 提前 2 分钟更换，避免过于极限
            if (now - self.sign_time).seconds >= 3480:
                self.update_web_hook(now)
        self.time_queue.put(now, timeout=q_timeout)
        if self.time_queue.full():
            # 当队列已满20条时，取20条消息中最早的时间
            earliest_time = self.time_queue.get(timeout=q_timeout)
            time_diff = (now - earliest_time).seconds
            # 判断提前 2 秒，避免过于极限
            if time_diff <= 58:
                sleep(60 - time_diff)
        try:
            r = requests.post(url=self.web_hook, data=json.dumps(form_data), headers=self.headers, timeout=r_timeout)
        except Exception as e:
            raise SendError(f'发送 post 请求失败，详情如下：\n{e}')
        response = json.loads(r.content.decode('utf-8'))
        errcode = response.get('errcode', 1)
        if errcode != 0:
            raise DingTalkError(f'{response}\n请查阅钉钉文档 [ https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq ]')

        return response

    def send_text(self, content: str, at_mobiles: list = None, at_all=False, q_timeout: int = 60,
                  r_timeout: int = 60):
        """
        发送 text 类型消息
        可以 @某人 ，将被@者的手机号放入 at_mobiles 列表中即可
        可以自定义 @某人 的位置，@xx手机号 即可（该手机号需在群聊中）
        :param content: 消息内容
        :param at_mobiles: 如  ['156xxxx8827', '189xxxx8325']
        :type at_mobiles: list
        :param at_all: 是否@所有人
        :param q_timeout: 队列等待超时时间
        :param r_timeout: requests 超时时间
        :return: 发送钉钉消息后返回的响应
        """
        if not isinstance(content, str):
            raise ValueError('[content] type must be string...')
        at_mobiles = [] if not isinstance(at_mobiles, list) else at_mobiles
        # 自动从文本内容中匹配出 @某人 的地方将其加入 at_mobiles
        at_mobiles_from_content = re.findall('@(\\d+)', content)
        msg = {
            'msgtype': 'text',
            'text': {
                'content': content
            },
            'at': {
                'atMobiles': at_mobiles + at_mobiles_from_content,
                'isAtAll': at_all
            }
        }
        return self._send_msg(msg, q_timeout, r_timeout)

    def send_link(self, title: str, text: str, msg_url: str, pic_url: str = None,
                  q_timeout: int = 60, r_timeout: int = 60):
        """
        发送 link 类型消息
        :param title: str,消息标题
        :param text: str,消息内容（如果太长只会部分展示）
        :param msg_url: str,点击消息跳转的 URL
        :param pic_url: str,展示图片的 URL
        :param q_timeout: 队列等待超时时间
        :param r_timeout: requests 超时时间
        :return: 发送钉钉消息后返回的响应
        """
        if not isinstance(title, str) or not isinstance(text, str) or not isinstance(msg_url, str):
            raise ValueError('[title, text, msg_url] type must be string...')
        msg = {
            'msgtype': 'link',
            'link': {
                'text': text,
                'title': title,
                'picUrl': pic_url,
                'messageUrl': msg_url
            }
        }
        return self._send_msg(msg, q_timeout, r_timeout)

    def send_markdown(self, title: str, text: str, at_mobiles: list = None, at_all=False,
                      q_timeout: int = 60, r_timeout: int = 60):
        """
        发送 markdown 类型消息 （钉钉目前仅支持部分 Markdown 语法，详情请看官方文档）
        可以 @某人 ，将被@者的手机号放入 at_mobiles 列表中即可
        可以自定义 @某人 的位置，@xx手机号 即可（该手机号需在群聊中）
        :param title: 首屏会话透出的展示内容
        :param text: markdown 格式的消息
        :param at_mobiles: 如  ['156xxxx8827', '189xxxx8325']
        :type at_mobiles: list
        :param at_all: 是否@所有人
        :param q_timeout: 队列等待超时时间
        :param r_timeout: requests 超时时间
        :return: 发送钉钉消息后返回的响应
        """
        if not isinstance(title, str) or not isinstance(text, str):
            raise ValueError('[title, text] type must be string...')
        at_mobiles = [] if not isinstance(at_mobiles, list) else at_mobiles
        # 自动从文本内容中匹配出 @某人 的地方将其加入 at_mobiles
        at_mobiles_from_text = re.findall('@(\\d+)', text)
        msg = {
            'msgtype': 'markdown',
            'markdown': {
                'title': title,
                'text': text
            },
            'at': {
                'atMobiles': at_mobiles + at_mobiles_from_text,
                'isAtAll': at_all
            }
        }
        return self._send_msg(msg, q_timeout, r_timeout)

    def send_entire_action_card(self, title: str, text: str, single_title: str, single_url: str,
                                q_timeout: int = 60, r_timeout: int = 60):
        """
        发送 整体跳转ActionCard 类型消息
        btnOrientation 参数按官方文档设置无效，故在此不对其进行配置（此类型消息就该无效按其文档意思）
        :param title: 首屏会话透出的展示内容
        :param text: markdown格式的消息
        :param single_title: 单个按钮的标题(设置此项和 ingleURL 后 btns 无效)
        :param single_url: 点击 single_title 按钮触发的URL
        :param q_timeout: 队列等待超时时间
        :param r_timeout: requests 超时时间
        :return: 发送钉钉消息后返回的响应
        """
        if not isinstance(title, str) or not isinstance(text, str) or not isinstance(single_title, str) \
                or not isinstance(single_url, str):
            raise ValueError('[title, text, single_title, single_url] type must be string...')
        msg = {
            'msgtype': 'actionCard',
            'actionCard': {
                'title': title,
                'text': text,
                'singleTitle': single_title,
                'singleURL': single_url,
                # 'btnOrientation': '0'

            }

        }
        return self._send_msg(msg, q_timeout, r_timeout)

    def send_alone_action_card(self, title: str, text: str, btn_li: list,
                               btn_orientation: str = '0', q_timeout: int = 60, r_timeout: int = 60):
        """
        发送 独立跳转ActionCard 类型消息
        :param title: 首屏会话透出的展示内容
        :param text: markdown格式的消息
        :param btn_li: list,按钮列表,如：[{'title': 'xx', 'actionURL': 'xx'},... ]
                        （必须包含'title','actionURL'，可以多不能少）
                        title,按钮标题
                        actionURL,点击按钮触发的URL
        :param btn_orientation: 0-按钮竖直排列，1-按钮横向排列（按钮超过两个则自动竖排）
        :param q_timeout: 队列等待超时时间
        :param r_timeout: requests 超时时间
        :return: 发送钉钉消息后返回的响应
        """
        if not isinstance(title, str) or not isinstance(text, str):
            raise ValueError('[title, text] type must be string...')
        if not isinstance(btn_li, list):
            raise ValueError('[btn_li] type must be list...')
        btn_li_correct = True
        for i in btn_li:
            if 'title' not in i or 'actionURL' not in i:
                btn_li_correct = False
                break
        if not btn_li_correct:
            raise ValueError('The "btn_li" must be a list like [{"title": "xx", "actionURL": "xx"},... ]')

        msg = {
            "msgtype": "actionCard",
            "actionCard": {
                "title": title,
                "text": text,
                "btnOrientation": btn_orientation,
                "btns": btn_li
            }
        }
        return self._send_msg(msg, q_timeout, r_timeout)

    def send_feed_card(self, link_li: list, q_timeout: int = 60, r_timeout: int = 60):
        """
        发送 FeedCard 类型消息
        :param link_li: list,链接列表,如：[{'title': 'xx', 'messageURL': 'xx', 'picURL': 'xx'},... ]
                        （必须包含'title','messageURL','picURL'，可以多不能少）
                        title,消息标题文本
                        messageURL,消息跳转链接
                        picURL,该消息图片 URL
        :param q_timeout: 队列等待超时时间
        :param r_timeout: requests 超时时间
        :return: 发送钉钉消息后返回的响应
        """
        if not isinstance(link_li, list):
            raise ValueError('[link_li] type must be list...')
        link_li_correct = True
        for i in link_li:
            if 'title' not in i or 'messageURL' not in i or 'picURL' not in i:
                link_li_correct = False
                break
        if not link_li_correct:
            raise ValueError(
                'The "link_li" must be a list like [{"title": "xx", "messageURL": "xx", "picURL": "xx"},... ]')
        msg = {
            'msgtype': 'feedCard',
            'feedCard': {
                'links': link_li
            }
        }

        return self._send_msg(msg, q_timeout, r_timeout)
