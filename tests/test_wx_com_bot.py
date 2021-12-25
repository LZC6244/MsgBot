# -*- coding: utf-8 -*-
import os
from MsgBot import WxComBot


class TestWxComBot(object):
    bot: WxComBot
    agent_id: int
    to_user: str

    @classmethod
    def setup_class(cls):
        env = os.environ
        corp_id = env.get('WX_COM_CORP_ID')
        corp_secret = env.get('WX_COM_CORP_SECRET')
        cls.agent_id = int(env.get('WX_COM_AGENT_ID'))
        cls.to_user = env.get('WX_COM_TO_USER')
        cls.bot = WxComBot(corp_id, corp_secret)

    def test_send_text(self):
        content = '【WxComBot测试】发送 [text] 类型消息成功 ...'
        assert isinstance(self.bot.send_msg_text(agent_id=self.agent_id, content=content, to_user=self.to_user), dict)

    def test_send_md(self):
        content = '【WxComBot测试】发送 `[markdown]` 类型消息**成功** ...'
        assert isinstance(self.bot.send_msg_text(agent_id=self.agent_id, content=content, to_user=self.to_user), dict)
