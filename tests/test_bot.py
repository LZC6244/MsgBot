# -*- coding: utf-8 -*-
import os
from DingTalkBot.bot import DingTalkBot


class TestDingTalkBot(object):
    bot: DingTalkBot

    @classmethod
    def setup_class(cls):
        env = os.environ
        web_hook = env.get('web_hook')
        secret = env.get('secret')
        cls.bot = DingTalkBot(web_hook, secret)

    def test_send_text(self):
        assert isinstance(self.bot.send_text('测试：发送 [ text ] 类型消息成功 ...'), dict)

    def test_send_link(self):
        title = '测试-标题'
        text = '测试文本-我一直都在你身边 ，一直都在。'
        msg_url = 'https://www.dingtalk.com/'
        pic_url = 'https://gw.alicdn.com/tfs/TB1ut3xxbsrBKNjSZFpXXcXhFXa-846-786.png'
        assert isinstance(self.bot.send_link(title, text, msg_url, pic_url), dict)

    def test_send_markdown(self):
        title = '测试-Markdown消息'
        text = '#### Markdown标题 @138XXXXXXXX \n> xxxx文本内容\n> ![screenshot](' \
               'https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png)'
        assert isinstance(self.bot.send_markdown(title, text), dict)

    def test_send_entire_action_card(self):
        title = '测试-整体跳转ActionCard'
        text = '#### Markdown标题 @138XXXXXXXX \n> xxxx文本内容\n> ![screenshot](' \
               'https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png)'
        single_title = '阅读全文'
        single_url = 'https://www.dingtalk.com/'
        assert isinstance(self.bot.send_entire_action_card(title, text, single_title, single_url), dict)

    def test_send_alone_action_card(self):
        title = '测试-独立跳转ActionCard'
        text = '#### Markdown标题 @138XXXXXXXX \n> xxxx文本内容\n> ![screenshot](' \
               'https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png)'
        btn_li = [
            {'title': 'option-1', 'actionURL': 'https://www.dingtalk.com/'},
            {'title': 'option-2', 'actionURL': 'https://www.dingtalk.com/'},
            # 测试带入非必要字段 'test' （结果为：无影响）
            {'title': 'option-3', 'actionURL': 'https://www.dingtalk.com/', 'test': 'test'}
        ]
        btn_orientation = '0'
        assert isinstance(self.bot.send_alone_action_card(title, text, btn_li, btn_orientation), dict)

    def test_send_feed_card(self):
        link_li = [
            {
                'title': '测试-FeedCard_1',
                'messageURL': 'https://www.dingtalk.com',
                'picURL': 'https://gw.alicdn.com/tfs/TB1ayl9mpYqK1RjSZLeXXbXppXa-170-62.png'
            },
            {
                'title': '测试-FeedCard_2',
                'messageURL': 'https://www.dingtalk.com',
                'picURL': 'https://gw.alicdn.com/tfs/TB1ayl9mpYqK1RjSZLeXXbXppXa-170-62.png'
            },
            {
                'title': '测试-FeedCard_3',
                'messageURL': 'https://www.dingtalk.com',
                'picURL': 'https://gw.alicdn.com/tfs/TB1ayl9mpYqK1RjSZLeXXbXppXa-170-62.png'
            },
        ]
        assert isinstance(self.bot.send_feed_card(link_li), dict)


if __name__ == '__main__':
    bot = TestDingTalkBot()
    bot.setup_class()
    bot.test_send_text()
