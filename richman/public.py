# -*- coding: utf-8 -*
'''公用土地类，例如 新闻，公园 等无法买卖的公共地方
'''
import logging

import richman.event as ev
import richman.interface as itf


class BasePublic(itf.IMapForPublic,  itf.IPlayerForPublic):
    
    def __init__(self, name: str)->None:
        self.__name:str = name

    @property
    def name(self)->str:
        return self.__name

    def trigger(self, player: itf.IPublicForPlayer):
        '''trigger the effect of the item in the map

        :param player: the player that trigger the effect
        '''
        raise NotImplementedError('override is needed.')

    def destroy(self)->None:
        '''destroy
        '''
        pass

    def __eq__(self, obj):
        return False


class PublicStart(BasePublic):
    def __init__(self, name='起点')->None:
        super().__init__(name)

    @staticmethod
    @ev.event_from_player_pass_start_line.connect
    def event_handler_add_money_when_player_pass_start_line(sender: itf.IPublicForPlayer):
        '''经过时领取奖励4000元，

        :param sender: the player that trigger the effect
        '''
        player = sender
        gain = 4000
        ev.event_to_player_add_money.send(None, receiver=player, money_delta=gain)
        logging.info('{} 经过起点，得到资金 {} 元。'.format(player.name, gain))

    def trigger(self, player: itf.IPublicForPlayer):
        '''经过时领取奖励4000元，
        若刚好到达起点，可将自己任意一处地产升一级（仍需支付升级费用）。

        :param player: the player that trigger the effect
        '''
        logging.info('{} 可选择一处地产升级。'.format(player.name))
        ev.event_to_player_upgrade_any_estate.send(self, receiver=player)


class PublicNews(BasePublic):
    def __init__(self, name='新闻')->None:
        super().__init__(name)

    def trigger(self, player: itf.IPublicForPlayer):
        '''抽取1张新闻卡。

        :param player: the player that trigger the effect
        '''
        ev.event_from_public_news_or_luck_triggered.send(self)
        logging.info('{} 抽取一张新闻卡。'.format(player.name))

class PublicPrison(BasePublic):
    def __init__(self)->None:
        super().__init__('监狱')

class PublicLuck(BasePublic):
    def __init__(self, name='运气')->None:
        super().__init__(name)

    def trigger(self, player: itf.IPublicForPlayer):
        '''抽取1张运气卡。

        :param player: the player that trigger the effect
        '''
        ev.event_from_public_news_or_luck_triggered.send(self)
        logging.info('{} 抽取一张幸运卡。'.format(player.name))

class PublicStock(BasePublic):
    def __init__(self)->None:
        super().__init__('证券中心')

class PublicGotoPrison(BasePublic):
    def __init__(self)->None:
        super().__init__('入狱')

class PublicPark(BasePublic):
    def __init__(self, name='公园')->None:
        super().__init__(name)

    def trigger(self, player: itf.IPublicForPlayer):
        '''拾到300元。

        :param player: the player that trigger the effect
        '''
        gain = 300
        logging.info('{} 在公园捡到 {} 元。'.format(player.name, gain))
        ev.event_to_player_add_money.send(self, receiver=player,
                                          money_delta=gain)

class PublicTax(BasePublic):
    def __init__(self)->None:
        super().__init__('税务中心')