# -*- coding: utf-8 -*
'''
'''
import random
import datetime


class RichmanCpu:

    __is_finished = False

    def __init__(self):
        random.seed(datetime.datetime.now())
        self.__func_switch = dict()
        self.__func_switch[1] = self._dice
        self.__func_switch[2] = self._buy_estate
        self.__func_switch[3] = self._upgrade_estate
        self.__func_switch[4] = self._buy_project
        self.__func_switch[5] = self._get_money
        self.__func_switch[6] = self._lose_money
        self.__func_switch[7] = self._pledge
        self.__func_switch[0] = self._quit
        self.__help_display = \
'''
功能选择：
    1. 掷筛子
    2. 买地
    3. 升级
    4. 买项目
    5. 得到金钱
    6. 失去金钱
    7. 抵押
    0. 退出
'''

    def _random_bool(self)->bool:
        return random.choice([True, False])

    def _dice(self):
        print('筛子数：{}。'.format(random.randrange(1, 7)))

    def _buy_estate(self):
        if self._random_bool():
            print('土地买卖：买进。')
        else:
            print('土地买卖：不买。')

    def _upgrade_estate(self):
        if self._random_bool():
            print('土地升级：升级。')
        else:
            print('土地升级：不升级。')

    def _buy_project(self):
        if self._random_bool():
            print('项目买卖：买进。')
        else:
            print('项目买卖：不买。')

    def _get_money(self):
        print('该功能暂未实现，请重新选择。')

    def _lose_money(self):
        print('该功能暂未实现，请重新选择。')

    def _pledge(self):
        print('该功能暂未实现，请重新选择。')

    def _quit(self):
        print('退出。')
        self.__is_finished = True

    def run(self):
        while not self.__is_finished:
            raw_input = input(self.__help_display)
            try:
                func_code = int(raw_input)
                self.__func_switch[func_code]()
            except ValueError:
                print('请输入功能数字。')
            except KeyError:
                print('功能选择错误')


def main():
    cpu = RichmanCpu()
    cpu.run()

if __name__ == "__main__":
    main()