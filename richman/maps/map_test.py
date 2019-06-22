# -*- coding: utf-8 -*
'''map test
'''
from richman.map import BaseMap


from richman.place import (
    Estate,
    EstateBlock,
    ProjectNuclear,
    ProjectBuilder,
    ProjectTransportation,
    ProjectTvStation,
    ProjectSewerage
)
from richman.public import (
    PublicStart,
    PublicNews,
    PublicPrison,
    PublicLuck,
    PublicStock,
    PublicGotoPrison,
    PublicPark,
    PublicTax
)

class MapTest(BaseMap):
    '''for test
    '''

    def __init__(self):
        super().__init__(name='map test')
        self._build()

    def _build(self):
        # block1 region
        block = EstateBlock('block1')
        self.add_items(PublicStart(name='起点'))
        self.add_items(Estate(
            name='沈阳',
            fees=[400, 1000, 2500, 5500],
            buy_value=2400,
            pledge_value=1200,
            upgrade_value=600,
            block=block
        ))
        self.add_items(Estate(
            name='天津',
            fees=[500, 1100, 3000, 6000],
            buy_value=2600,
            pledge_value=1300,
            upgrade_value=600,
            block=block
        ))
        self.add_items(ProjectNuclear(name='核能发电厂'))
        self.add_items(Estate(
            name='北京',
            fees=[400, 1000, 2500, 5500],
            buy_value=2300,
            pledge_value=1100,
            upgrade_value=600,
            block=block
        ))
        self.add_items(PublicNews(name='新闻1'))
        self.add_items(Estate(
            name='大连',
            fees=[200, 500, 1000, 3000],
            buy_value=1200,
            pledge_value=600,
            upgrade_value=300,
            block=block
        ))
        #block2 region
        block = EstateBlock('block2')
        self.add_items(Estate(
            name='贵阳',
            fees=[200, 400, 1000, 2500],
            buy_value=1000,
            pledge_value=500,
            upgrade_value=300,
            block=block
        ))
        self.add_items(ProjectBuilder(name='建筑公司'))
        self.add_items(Estate(
            name='长沙',
            fees=[300, 600, 1500, 3500],
            buy_value=1500,
            pledge_value=700,
            upgrade_value=300,
            block=block
        ))
        public_prison = PublicPrison(name='监狱')
        self.add_items(public_prison)
        self.add_items(Estate(
            name='银川',
            fees=[300, 700, 1500, 3500],
            buy_value=1800,
            pledge_value=900,
            upgrade_value=300,
            block=block
        ))
        self.add_items(Estate(
            name='兰州',
            fees=[400, 1000, 2500, 5500],
            buy_value=2400,
            pledge_value=1200,
            upgrade_value=600,
            block=block
        ))
        self.add_items(ProjectTransportation('大陆运输'))
        self.add_items(Estate(
            name='拉萨',
            fees=[400, 900, 2000, 5000],
            buy_value=2000,
            pledge_value=1000,
            upgrade_value=600,
            block=block
        ))
        self.add_items(PublicLuck('运气1'))
        #block3 region
        block = EstateBlock('block3')
        self.add_items(Estate(
            name='杭州',
            fees=[400, 1000, 2500, 5500],
            buy_value=2200,
            pledge_value=1100,
            upgrade_value=600,
            block=block
        ))
        self.add_items(ProjectTvStation(name='电视台'))
        self.add_items(Estate(
            name='南京',
            fees=[700, 1600, 4500, 9000],
            buy_value=3800,
            pledge_value=1900,
            upgrade_value=900,
            block=block
        ))
        self.add_items(Estate(
            name='苏州',
            fees=[700, 1500, 4000, 8500],
            buy_value=3500,
            pledge_value=1700,
            upgrade_value=900,
            block=block
        ))
        self.add_items(PublicStock(name='证券中心'))
        self.add_items(Estate(
            name='厦门',
            fees=[800, 1900, 5000, 10500],
            buy_value=4000,
            pledge_value=2000,
            upgrade_value=1200,
            block=block
        ))
        self.add_items(Estate(
            name='台北',
            fees=[800, 1900, 5000, 10500],
            buy_value=4000,
            pledge_value=2000,
            upgrade_value=1200,
            block=block
        ))
        prison_pos = self.get_item_position(public_prison)
        public_goto_prison = PublicGotoPrison('入狱', prison_pos=prison_pos)
        self.add_items(public_goto_prison)
        #block4 region
        block = EstateBlock('block4')
        self.add_items(ProjectTransportation('航空运输'))
        self.add_items(PublicNews(name='新闻2'))
        self.add_items(Estate(
            name='重庆',
            fees=[600, 1400, 3500, 7500],
            buy_value=3000,
            pledge_value=1500,
            upgrade_value=900,
            block=block
        ))
        self.add_items(Estate(
            name='成都',
            fees=[600, 1500, 4000, 8500],
            buy_value=3300,
            pledge_value=1600,
            upgrade_value=900,
            block=block
        ))
        self.add_items(PublicPark(name='公园'))
        #block5 region
        block = EstateBlock('block5')
        self.add_items(Estate(
            name='深圳',
            fees=[600, 1400, 4000, 8000],
            buy_value=3100,
            pledge_value=1500,
            upgrade_value=900,
            block=block
        ))
        self.add_items(ProjectSewerage('污水处理厂'))
        self.add_items(Estate(
            name='广州',
            fees=[800, 2000, 5500, 11000],
            buy_value=4400,
            pledge_value=2200,
            upgrade_value=1200,
            block=block
        ))
        self.add_items(Estate(
            name='三亚',
            fees=[800, 2000, 5500, 11000],
            buy_value=4400,
            pledge_value=2200,
            upgrade_value=1200,
            block=block
        ))
        self.add_items(ProjectTransportation('大洋运输'))
        #block6 region
        block = EstateBlock('block6')
        self.add_items(Estate(
            name='香港',
            fees=[900, 2100, 5500, 12000],
            buy_value=4800,
            pledge_value=2400,
            upgrade_value=1200,
            block=block
        ))
        self.add_items(PublicLuck('运气2'))
        self.add_items(Estate(
            name='澳门',
            fees=[1000, 2400, 6000, 13000],
            buy_value=5000,
            pledge_value=2500,
            upgrade_value=1500,
            block=block
        ))
        self.add_items(PublicTax('税务中心'))
        self.add_items(Estate(
            name='上海',
            fees=[1000, 2400, 6500, 13500],
            buy_value=5100,
            pledge_value=2500,
            upgrade_value=1500,
            block=block
        ))
        self.add_items(Estate(
            name='钓鱼岛',
            fees=[1100, 2500, 6500, 14000],
            buy_value=5500,
            pledge_value=2700,
            upgrade_value=1500,
            block=block
        ))
