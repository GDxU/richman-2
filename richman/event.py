# -*- coding: utf-8 -*
'''事件类
'''
from typing import Any, List, Tuple, Optional

from blinker import Namespace  # type: ignore


def check_event_result_is_true(results: List[Tuple[Any, Optional[bool]]])->bool:
    '''check whether any result of the event returns True

    :param results: results of event, with struct of [(function, rst)]
    :return: True if any of results is True
    '''
    for _, rst in results:
        if rst:
            return True
    else:
        return False


_events = Namespace()

# event from map
event_from_map_finish = _events.signal("event-from-game-finish")
event_from_map_start_round = _events.signal("event-from-map-start-round")
event_from_map_finish_round = _events.signal("event-from-map-finish-round")

# event from place
event_from_place_bought = _events.signal("event-from-place-bought")
event_from_place_sold = _events.signal("event-from-place-sold")

# event from estate
event_from_estate_upgraded = _events.signal("event-from-estate-upgraded")
event_from_estate_degraded = _events.signal("event-from-estate-degraded")
event_from_estate_pledged = _events.signal("event-from-estate-pledged")
event_from_estate_rebought = _events.signal("event-from-estate-rebought")

# event from player
event_from_player_start_turn = _events.signal("event-from-player-start-turn")
event_from_player_finish_turn = _events.signal("event-from-player-finish-turn")
event_from_player_after_dice = _events.signal("event-from-player-after-dice")
event_from_player_pass_start_line = _events.signal("event-from-player-pass-start-line")
event_from_player_block_before_add_money = _events.signal("event-from-player-block-before-add-money")
event_from_player_block_before_turn = _events.signal("event-from-player-block-before-turn")

# event from public
event_from_public_news_or_luck_triggered = _events.signal("event-from-public-news-triggered")


# event to game
event_to_game_rollback = _events.signal("event-to-game-rollback")

# event to player
event_to_player_add_money = _events.signal("event-to-player-add-money")
event_to_player_move_to = _events.signal("event-to-player-move-to")
event_to_player_buy_place = _events.signal("event-to-player-buy-place")
event_to_player_upgrade_estate = _events.signal("event-to-player-upgrade-estate")
event_to_player_jump_to_estate = _events.signal("event-to-player-jump-to-estate")
event_to_player_upgrade_any_estate = _events.signal("event-to-player-upgrade-any-estate")

# event to place
event_to_place_buy = _events.signal("event-to-place-buy")
event_to_place_sell = _events.signal("event-to-place-sell")

# event to estate
event_to_estate_upgrade = _events.signal("event-to-estate-upgrade")
event_to_estate_degrade = _events.signal("event-to-estate-degrade")
event_to_estate_pledge = _events.signal("event-to-estate-pledge")
event_to_estate_rebuy = _events.signal("event-to-estate-rebuy")

# event to project

# event to display
event_to_display_list_of_dict = _events.signal("event-to-display-list-of-dict")
