# -*- coding: utf-8 -*
'''事件类
'''
from blinker import Namespace  # type: ignore


_events = Namespace()

# event from estate
event_from_estate_bought = _events.signal("event-from-estate-bought")
event_from_estate_sold = _events.signal("event-from-estate-sold")
event_from_estate_upgraded = _events.signal("event-from-estate-upgraded")
event_from_estate_degraded = _events.signal("event-from-estate-degraded")
event_from_estate_pledged = _events.signal("event-from-estate-pledged")
event_from_estate_rebought = _events.signal("event-from-estate-rebought")

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

#event to estate
event_to_estate_upgrade = _events.signal("event-to-estate-upgrade")
event_to_estate_degrade = _events.signal("event-to-estate-degrade")
event_to_estate_pledge = _events.signal("event-to-estate-pledge")
event_to_estate_rebuy = _events.signal("event-to-estate-rebuy")
