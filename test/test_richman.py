# -*- coding: utf-8 -*
import unittest

import run_the_game


class TestRichMan(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_run_the_game_should_not_raise_exceptions(self):
        for _ in range(10):
            run_the_game.main(log_on=False)
