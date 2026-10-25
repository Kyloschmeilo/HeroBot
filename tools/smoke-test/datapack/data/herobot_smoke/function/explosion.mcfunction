execute store result score bob_hp_before smoke run data get entity Bob Health
execute store result score bob_x_before smoke run data get entity Bob Pos[0] 100
execute at Bob run summon minecraft:tnt ~4 ~ ~ {fuse:1}
schedule function herobot_smoke:explosion_check 15t
