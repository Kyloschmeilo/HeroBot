ride Bob mount @e[type=minecraft:oak_boat,limit=1]
execute store result score boat_z_before smoke run data get entity @e[type=minecraft:oak_boat,limit=1] Pos[2] 100
player Bob look south
player Bob move forward
schedule function herobot_smoke:boat_check 40t
