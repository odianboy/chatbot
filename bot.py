#!/usr/bin/env python3

import logging
import random

try:
    import settings
except ImportError:
    exit('DO cp settings.py default settings.py and set token!')

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

log = logging.getLogger('bot')


def configure_logging():

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(fmt='%(levelname)s %(message)s '))
    stream_handler.setLevel(logging.INFO)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler(filename='bot.log', encoding='UTF-8')
    file_handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s',  datefmt='%d-%m-%Y %H:%M'))
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)

    log.setLevel(logging.DEBUG)


class Bot:
    """
    Echo bot for vk.com

    Use python 3.7
    """
    def __init__(self, group_id, token):
        """
        :param group_id: group id from the group vk
        :param  token: secret token
        """
        self.group_id = group_id
        self.token = token

        self.vk = vk_api.VkApi(token=token)
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)

        self.api = self.vk.get_api()

    def run(self):
        """Bot launch."""
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                log.exception('error in event handling')

    def on_event(self, event):
        """Send message back, if it is text.

        :param event: VkBotMessageEvent object
        :return: None
        """
        if event.type == VkBotEventType.MESSAGE_NEW:
            log.debug('send a message back')
            self.api.messages.send(
                message=event.object.text,
                random_id=random.randint(0, 2 ** 20),
                peer_id=event.object.peer_id,
            )
        else:
            log.info('We are not yet able to handle events of this type. %s', event.type)


if __name__ == '__main__':
    configure_logging()
    bot = Bot(settings.GROUP_ID, settings.TOKEN)
    bot.run()
