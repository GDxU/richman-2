# -*- coding: utf-8 -*
'''map test
'''
from richman.map import BaseMap


from richman.estate import (
    Estate,
    EstateBlock
)
from richman.project import (
    ProjectNuclear,
    ProjectBuilder,
    ProjectStation,
    ProjectTv,
    ProjectAirport,
    ProjectSewerage,
    ProjectSeaport
)
from richman.event import (
    EventStart,
    EventNews,
    EventPrison,
    EventLuck,
    EventStock,
    EventGotoPrison,
    EventPark,
    EventTax
)

class MapTest(BaseMap):
    '''for test
    '''

    def __init__(self):
        super().__init__(name='map test', items=[])
        self._build()

    def _build(self):
        # block1 region
        self._blocks.append(EstateBlock('block1'))
        self._add_items(Estate(
            name='沈阳',
            fees=[400, 1000, 2500, 5500],
            buy_value=2400,
            pledge_value=1200,
            upgrade_value=600,
            block=self._blocks[0]
            ))
        self._add_items(Estate(
            name='天津',
            fees=[500, 1100, 3000, 6000],
            buy_value=2600,
            pledge_value=1300,
            upgrade_value=600,
            block=self._blocks[0]
            ))
        self._add_items(Estate(
            name='北京',
            fees=[400, 1000, 2500, 5500],
            buy_value=2300,
            pledge_value=1100,
            upgrade_value=600,
            block=self._blocks[0]
            ))
        self._add_items(Estate(
            name='大连',
            fees=[200, 500, 1000, 3000],
            buy_value=1200,
            pledge_value=600,
            upgrade_value=300,
            block=self._blocks[0]
            ))
        #block2 region
        self._blocks.append(EstateBlock('block2'))
        self._add_items(Estate(
            name='贵阳',
            fees=[200, 400, 1000, 2500],
            buy_value=1000,
            pledge_value=500,
            upgrade_value=300,
            block=self._blocks[1]
            ))
        self._add_items(Estate(
            name='长沙',
            fees=[300, 600, 1500, 3500],
            buy_value=1500,
            pledge_value=700,
            upgrade_value=300,
            block=self._blocks[1]
            ))
        self._add_items(Estate(
            name='银川',
            fees=[300, 700, 1500, 3500],
            buy_value=1800,
            pledge_value=900,
            upgrade_value=300,
            block=self._blocks[1]
            ))
        self._add_items(Estate(
            name='兰州',
            fees=[400, 1000, 2500, 5500],
            buy_value=2400,
            pledge_value=1200,
            upgrade_value=600,
            block=self._blocks[1]
            ))
        self._add_items(Estate(
            name='拉萨',
            fees=[400, 900, 2000, 5000],
            buy_value=2000,
            pledge_value=1000,
            upgrade_value=600,
            block=self._blocks[1]
            ))
        #block3 region
        self._blocks.append(EstateBlock('block3'))
        self._add_items(Estate(
            name='杭州',
            fees=[400, 1000, 2500, 5500],
            buy_value=2200,
            pledge_value=1100,
            upgrade_value=600,
            block=self._blocks[2]
            ))
        self._add_items(Estate(
            name='南京',
            fees=[700, 1600, 4500, 9000],
            buy_value=3800,
            pledge_value=1900,
            upgrade_value=900,
            block=self._blocks[2]
            ))
        self._add_items(Estate(
            name='苏州',
            fees=[700, 1500, 4000, 8500],
            buy_value=3500,
            pledge_value=1700,
            upgrade_value=900,
            block=self._blocks[2]
            ))
        self._add_items(Estate(
            name='厦门',
            fees=[800, 1900, 5000, 10500],
            buy_value=4000,
            pledge_value=2000,
            upgrade_value=1200,
            block=self._blocks[2]
            ))
        self._add_items(Estate(
            name='台北',
            fees=[800, 1900, 5000, 10500],
            buy_value=4000,
            pledge_value=2000,
            upgrade_value=1200,
            block=self._blocks[2]
            ))
