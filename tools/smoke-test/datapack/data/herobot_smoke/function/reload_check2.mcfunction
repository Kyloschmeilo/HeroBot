# The bot joins a few seconds after /playerspawn, so wait for it (up to 20 seconds).
scoreboard players add carol_wait smoke 1
execute if entity Carol run return run function herobot_smoke:reload_ok
execute if score carol_wait smoke matches 40.. run return run function herobot_smoke:reload_fail
schedule function herobot_smoke:reload_check2 10t
