# -*- coding: utf-8 -*
import time
from typing import Any, List
import logging
from logging.handlers import RotatingFileHandler

import richman.event as ev
from richman.game import Game
from richman.map import BaseMap
from richman.maps.map_test import MapTest
from richman.place import Estate
from richman.player import BasePlayer, PlayerSimple, PlayerPersonCommandLine
from richman.cmdline_display import CmdlineDisplay


def set_estate_owner(map: BaseMap, player: BasePlayer,
                     estate_name: str, level: int)->None:
    estates = [estate for estate in map.items
                if isinstance(estate, Estate)]
    for estate in estates:
        if estate.name == estate_name:
            estate._BasePlace__owner = player
            estate._Estate__current_level = level
            player._estates.append(estate)

def _set_logger(text_log_on=False)->None:
    logger = logging.getLogger()
    # logger.setLevel(logging.CRITICAL)
    # logger.setLevel(logging.WARNING)
    logger.setLevel(logging.INFO)
    # logger.setLevel(logging.DEBUG)
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
    dengyanxiu = PlayerPersonCommandLine(name='邓彦修', money=init_money)
    # dengyanxiu = PlayerSimple(name='邓彦修', money=init_money)
    # dengzhe = PlayerPersonCommandLine(name='邓哲', money=init_money)
    # rongping = PlayerPersonCommandLine(name='戎萍', money=init_money)
    limingzhe = PlayerSimple(name='李明珍', money=init_money)
    # players:List[BasePlayer] = [dengyanxiu, dengzhe, rongping, limingzhe]
    players:List[BasePlayer] = [dengyanxiu, limingzhe]
    # map
    map = MapTest()
    # display
    cmdline = CmdlineDisplay(map)
    # game
    game = Game(map, players, cmdline)
    # do something cheat
    set_estate_owner(map, dengyanxiu, '钓鱼岛', 0)
    # set_estate_owner(map, dengzhe, '长沙', 1)
    # set_estate_owner(map, rongping, '杭州', 1)
    set_estate_owner(map, limingzhe, '三亚', 0)
    # start
    game.run()


if __name__ == "__main__":
    main(log_on=True, text_log_on=True)
