execute store result score alice_y smoke run data get entity Alice Pos[1] 100
execute if score alice_y smoke > alice_y_before smoke run say SMOKE OK wind_charge_jump
execute unless score alice_y smoke > alice_y_before smoke run say SMOKE FAIL wind_charge_jump
# boat on a small pond
fill -2 -61 3 3 -61 14 minecraft:water
tp Bob 0.5 -60 6.5
summon minecraft:oak_boat 0.5 -60.6 6.5
schedule function herobot_smoke:boat 10t
