import json
import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from src.TransBaidu import TransBaidu

logger = logging.getLogger(__name__)


class TransExtension(Extension):

    def __init__(self):
        super(TransExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        arg = event.get_argument() or str()
        # 处理空输入
        if len(arg.strip()) == 0:
            return RenderResultListAction(
                [
                    ExtensionResultItem(
                        icon="images/logo.jpg",
                        name="No input",
                        on_enter=HideWindowAction(),  # 停止触发
                    )
                ]
            )
        #
        items = []
        logger.info("arg:%s" % arg)
        logger.info("preferences %s" % json.dumps(extension.preferences))
        trans = TransBaidu(extension.preferences)
        results = trans.trans(arg)
        baidu_url = "https://fanyi.baidu.com/?aldtype=16047#en/zh/"
        for i in results:
            res = i.get("dst")
            items.append(
                ExtensionResultItem(
                    icon="images/icon.png",
                    name="%s %s" % (i.get("src"), i.get("dst")),
                    description="",
                    # 复制内容到剪切板
                    on_enter=CopyToClipboardAction(res),
                    # on_enter=OpenUrlAction(
                    #     baidu_url + i.get("src")
                    # ),  # 原先版本使用的是打开网页
                )
            )
        return RenderResultListAction(items)


if __name__ == "__main__":
    TransExtension().run()
