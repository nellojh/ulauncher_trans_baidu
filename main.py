import json
import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from src.TransBaidu import TransBaidu

logger = logging.getLogger(__name__)


class TransExtension(Extension):

    def __init__(self):
        super(TransExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
        arg = event.get_argument();
        logger.info('arg:%s' % arg)
        logger.info('preferences %s' % json.dumps(extension.preferences))
        trans = TransBaidu(extension.preferences)        
        results = trans.trans(arg)
        baidu_url = 'https://fanyi.baidu.com/?aldtype=16047#en/zh/'
        for i in results:
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name='%s %s' % (i.get('src'), i.get('dst')),
                                             description='',
                                             on_enter=OpenUrlAction(baidu_url+i.get('src'))))

        return RenderResultListAction(items)

if __name__ == '__main__':
    TransExtension().run()
