# Bots join a few seconds after /playerspawn. Like real players they cannot be hurt during the
# first 60 ticks (until the "client" counts as loaded), so the combat checks start 80 ticks later.
scoreboard players add spawn_wait smoke 1
execute if entity Alice if entity Bob run return run schedule function herobot_smoke:combat 80t
execute if score spawn_wait smoke matches 60.. run return run schedule function herobot_smoke:combat 1t
schedule function herobot_smoke:wait_bots 10t
