# -*- coding: utf-8 -*-
import json
import logging
import requests
from datetime import datetime, timedelta

logging.basicConfig(format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
                    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


class WxComBot(object):
    """
    企业微信消息通知机器人（利用应用）
    目前支持消息类型：
        1. 文本
    """
    # 企业 id
    corp_id: str
    # 应用的凭证密钥
    corp_secret: str
    # 企业微信应用 access_token
    token: str
    # access_token 过期时间，默认为 2 小时过期
    expires_at: datetime

    def __init__(self, corp_id: str, corp_secret: str):
        self.corp_id = corp_id
        self.corp_secret = corp_secret
        self.expires_at = datetime.now()

    def get_token(self):
        logger.info('开始获取 token')
        now = datetime.now()
        url = f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.corp_id}&corpsecret={self.corp_secret}'
        r = requests.get(url)
        data = json.loads(r.text)
        if data['errcode'] != 0:
            logger.error('获取 token 失败！请检查！')
        self.expires_at = now + timedelta(seconds=data['expires_in'])
        self.token = data['access_token']
        logger.info('获取 token 成功')

    def send_msg_text(self, agent_id: int, content: str, to_user: str = None, to_party: str = None, safe: int = 0,
                      to_tag: str = None, enable_id_trans: int = 0, enable_duplicate_check: int = 0,
                      duplicate_check_interval: int = 1800):
        """
        发送文本类型消息
        :param agent_id: 企业应用的id，整型。企业内部开发，可在应用的设置页面查看
        :param content: 消息内容，最长不超过2048个字节，超过将截断（支持id转译）
                        content 参数支持换行（\n）、以及 a 标签（打开自定义的网页）
        :param to_user: 指定接收消息的成员，成员ID列表（多个接收者用 | 分隔，最多支持1000个）。
                        特殊情况：指定为 @all ，则向该企业应用的全部成员发送
        :param to_party: 指定接收消息的部门，部门ID列表，多个接收者用 | 分隔，最多支持100个。
                         当 to_user 为 @all 时忽略本参数
        :param to_tag: 指定接收消息的标签，标签ID列表，多个接收者用 | 分隔，最多支持100个。
                       当 to_user 为 @all 时忽略本参数
        :param safe: 表示是否是保密消息，0表示可对外分享，1表示不能分享且内容显示水印，默认为0
        :param enable_id_trans: 表示是否开启id转译，0表示否，1表示是，默认0。仅第三方应用需要用到，企业自建应用可以忽略。
        :param enable_duplicate_check: 表示是否开启重复消息检查，0表示否，1表示是，默认0
        :param duplicate_check_interval: 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
        :return:
        """
        if not to_user and not to_party and not to_tag:
            raise ValueError('[to_user,to_party,to_tag] 不能同时为空')
        if len(content) > 2048:
            logger.warning(f'文本消息长度超出 2048 ，信息已截断')
            content = content[:2048]
        now = datetime.now()
        if now >= self.expires_at:
            self.get_token()

        form_data = {
            "touser": to_user,
            "toparty": to_party,
            "totag": to_tag,
            "msgtype": 'text',
            "agentid": agent_id,
            "text": {
                "content": content
            },
            "safe": safe,
            "enable_id_trans": enable_id_trans,
            "enable_duplicate_check": enable_duplicate_check,
            "duplicate_check_interval": duplicate_check_interval
        }

        url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.token}&debug=1'
        r = requests.post(url, data=json.dumps(form_data))
        data = json.loads(r.text)
        if data['errcode'] != 0:
            raise UserWarning(f'文本消息发送发送异常，请检查：{data}')
        logger.info('文本消息发送成功')
