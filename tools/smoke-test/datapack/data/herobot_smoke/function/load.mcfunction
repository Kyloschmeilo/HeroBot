# Runs when the test world loads and again after every data pack reload.
scoreboard objectives add smoke dummy
execute if score reloaded smoke matches 1 run schedule function herobot_smoke:reload_check 20t
execute unless score reloaded smoke matches 1 run function herobot_smoke:start
