execute store result score bob_y smoke run data get entity Bob Pos[1] 100
scoreboard players operation bob_y smoke -= bob_y_before smoke
execute if score bob_y smoke matches 150.. run say SMOKE OK slime_piston_launch
execute unless score bob_y smoke matches 150.. run say SMOKE FAIL slime_piston_launch
setblock 7 -61 6 minecraft:grass_block
tp Bob -6.5 -60 -6.5
schedule function herobot_smoke:explosion 40t
