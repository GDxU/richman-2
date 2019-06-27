# -*- coding: utf-8 -*
import pprint
import logging
from logging.handlers import RotatingFileHandler

import richman.utility as util


def _set_logger(text_log_on:bool = False)->None:
    logger = logging.getLogger()
    # logger.setLevel(logging.CRITICAL)
    # logger.setLevel(logging.WARNING)
    # logger.setLevel(logging.INFO)
    logger.setLevel(logging.DEBUG)
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
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logger.addHandler(console)
    # add txt log
    if text_log_on:
        rt_handler = RotatingFileHandler(r"log.txt", maxBytes=1*1024*1024, backupCount=5)
        rt_handler.setLevel(logging.WARNING)
        rt_handler.setFormatter(formatter)
        logger.addHandler(rt_handler)
    # set progate
    logger.propagate = False


# None means divert to anywhere
# turn_points = {
#     13: None,
#     23: 10,
#     24: None,
#     33: None
# }
# map_len = 40
turn_points = {
    9: None,
    10: None,
    11: None,
    12: None,
    13: None,
    14: None,
    15: None,
    16: None
}
map_len = 17
map_topology = util.MapTopology(name='map_topology', turn_points=turn_points, map_len=map_len)
map_stat = util.MapStatistics(map_topology)

# _set_logger()
rsts = map_stat.calculate_trigger_rate(rounds=200000)
# rsts = map_stat.calculate_trigger_rate(rounds=100)
pp = pprint.PrettyPrinter(indent=4)
pp.pprint([r'{} : {:.1%}'.format(index, num) for index, num in enumerate(rsts)])