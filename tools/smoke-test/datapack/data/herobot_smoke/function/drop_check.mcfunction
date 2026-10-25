execute if entity @e[type=minecraft:item] run say SMOKE OK drop_item
execute unless entity @e[type=minecraft:item] run say SMOKE FAIL drop_item
player Alice swing once
# wind charge at the feet
execute store result score alice_y_before smoke run data get entity Alice Pos[1] 100
player Alice hotbar 3
player Alice look down
player Alice use once
schedule function herobot_smoke:wind_check 10t
