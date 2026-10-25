player Bob stop
execute store result score boat_z smoke run data get entity @e[type=minecraft:oak_boat,limit=1] Pos[2] 100
execute if score boat_z smoke > boat_z_before smoke run say SMOKE OK boat_paddle
execute unless score boat_z smoke > boat_z_before smoke run say SMOKE FAIL boat_paddle
ride Bob dismount
kill @e[type=minecraft:oak_boat]
# ping delays knockback
player Bob ping delay 100
tp Bob 0.5 -60 -2.5
player Alice hotbar 1
player Alice look upon Bob
player Alice attack once
function herobot_smoke:fabric_only
schedule function herobot_smoke:respawn 20t
