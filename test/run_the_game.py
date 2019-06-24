# -*- coding: utf-8 -*
from typing import List
import logging
from logging.handlers import RotatingFileHandler

from richman.game import Game
from richman.maps.map_test import MapTest
from richman.player import PlayerSimple, PlayerPersonCommandLine


def _set_logger(text_log_on=False)->None:
    logger = logging.getLogger()
    #logger.setLevel(logging.CRITICAL)
    #logger.setLevel(logging.WARNING)
    logger.setLevel(logging.INFO)
    #logger.setLevel(logging.DEBUG)
    # clear handlers
    handlers = logger.handlers
    for handler in handlers:
        logger.removeHandler(handler)
    # add filter
    #logger_filter = LoggerFilter()
    #logger.addFilter(logger_filter)
    # add stream handler
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('[%(levelname)s %(asctime)s] [%(module)s %(lineno)d] %(message)s')
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logger.addHandler(console)
    # add txt log
    if text_log_on:
        rt_handler = RotatingFileHandler(r"log.txt", maxBytes=1*1024*1024, backupCount=5)
        rt_handler.setLevel(logging.INFO)
        rt_handler.setFormatter(formatter)
        logger.addHandler(rt_handler)
    # set progate
    logger.propagate = False


def main(log_on:bool = False, text_log_on:bool = True)->None:
    if log_on:
        _set_logger(text_log_on)
    # player
    init_money = 20000
    players:List[PlayerSimple] = []
    # players.append(PlayerPersonCommandLine(name='邓哲', money=init_money))
    players.append(PlayerPersonCommandLine(name='邓彦修', money=init_money))
    players.append(PlayerSimple(name='邓哲', money=init_money))
    # players.append(PlayerPersonCommandLine(name='戎萍', money=init_money))
    # players.append(PlayerSimple(name='外婆', money=init_money))
    # map
    map = MapTest()
    # game
    game = Game(map, players)
    # start
    game.run()


if __name__ == "__main__":
    main(log_on=True, text_log_on=True)