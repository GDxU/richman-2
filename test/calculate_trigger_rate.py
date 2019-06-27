# -*- coding: utf-8 -*
import pprint

import richman.utility as util


map_topo = util.MapTopology(None)
map_stat = util.MapStatistics(map_topo)

rsts = map_stat.calculate_trigger_rate(rounds=1000000)
pp = pprint.PrettyPrinter(indent=4)
pp.pprint([r'{} : {:.2%}'.format(index, num) for index, num in enumerate(rsts)])