# -*- coding: utf-8 -*
'''项目类
'''
import logging

import richman.interface as itf


class BaseProject(itf.IPlayerForProject):

    def __init__(self, name: str, buy_value: int, sell_value: int):
        '''init

        :param name: name of place
        :param buy_value: value to buy
        :param sell_value: value to sell
        '''
        self.__name = name
        self.__buy_value = buy_value
        self.__sell_value = sell_value
        # init others
        self.__owner = None

    @property
    def name(self):
        return self.__name
    @property
    def owner(self):
        return self.__owner
    @property
    def buy_value(self):
        return self.__buy_value
    @property
    def sell_value(self):
        return self.__sell_value

    def buy(self, player: itf.IProjectForPlayer):
        assert not self.__owner, '该项目已经卖出，无法购买！'
        player.add_money(-self.buy_value)
        self.__owner = player
        logging.info('{} 购买项目 {}，花费 {} 元。'.format(player.name, self.name, self.buy_value))

    def sell(self):
        assert self.owner, '该项目无主，不能卖！'
        self.owner.add_money(self.sell_value)
        logging.info('{} 变卖项目 {}，获得 {} 元。'.format(self.owner.name, self.name, self.sell_value))
        self.__owner = None

    def trigger(self, player: itf.IProjectForPlayer):
        '''take the effect of the place, triggered by the player

        :param player: IProjectForPlayer
        '''
        if self.owner:
            self._take_effect(player)
        else:
            player.trigger_buy(self)
    
    def _take_effect(self, player: itf.IProjectForPlayer):
        '''take the effect of the place, triggered by the player

        :param player: IProjectForPlayer
        '''
        raise NotImplementedError('override is needed.')

    def __eq__(self, obj):
        return self.name == obj.name

    def __str__(self):
        '''display project info
        '''
        return self.name


class ProjectNuclear(BaseProject):

    def __init__(self, buy_value: int, sell_value: int):
        super().__init__(name='核能发电站',
                         buy_value=buy_value,
                         sell_value=sell_value)

    def _take_effect(self, player: itf.IProjectForPlayer):
        '''收取500元，若对方拥有1级/2级/3级地产，额外收取500/1000/1500元。

        :param player: IProjectForPlayer
        '''
        fine = 500 + 500 * player.estate_max_level
        player.add_money(fine)

class ProjectBuilder(BaseProject):

    def _take_effect(self, player: itf.IProjectForPlayer):
        '''每当玩家升级地产时，获得500元。
        当任意玩家到建筑公司时，可将一处地产升一级（需支付升级费用）。

        :param player: IProjectForPlayer
        '''
        fine = 500
        player.add_money(fine)
        player.trigger_upgrade_any_estate()

class ProjectTransportation(BaseProject):

    def _take_effect(self, player: itf.IProjectForPlayer):
        '''当你拥有1/2/3项运输项目时，收取500/1000/2000元。
        下回合开始时，你可以放弃投骰子，改为给本项目拥有着500元（无人拥有则给银行），
        立即到任意一个地产处。

        :param player: IProjectForPlayer
        '''
        raise NotImplementedError('override is needed.')

class ProjectTvStation(BaseProject):

    def _take_effect(self, player: itf.IProjectForPlayer):
        '''当任何人走到运气和新闻时，你获得500元奖励。

        :param player: IProjectForPlayer
        '''
        raise NotImplementedError('override is needed.')

class ProjectSewerage(BaseProject):

    def _take_effect(self, player: itf.IProjectForPlayer):
        '''收取500元，若对方每拥有3块地产，额外收取500元。

        :param player: IProjectForPlayer
        '''
        raise NotImplementedError('override is needed.')

