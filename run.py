# -*- coding: utf-8 -*
import logging

from richman.game import GameImplement
from richman.maps.map_test import MapTest
from richman.place import PlaceEstate, PlaceEstateBlock
from richman.player import PlayerSimple


def _set_logger():
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
    formatter = logging.Formatter('[%(levelname)s %(asctime)s] [%(module)s %(lineno)d] %(message)s')
    console.setFormatter(formatter)
    logger.addHandler(console)
    # set progate
    logger.propagate = False


def main():
    _set_logger()
    # player
    init_money = 20000
    player1 = PlayerSimple(name='邓哲', money=init_money)
    player2 = PlayerSimple(name='戎萍', money=init_money)
    # map
    map = MapTest()
    # game
    game = GameImplement(map, [player1, player2])
    # start
    game.run()


if __name__ == "__main__":
    main()