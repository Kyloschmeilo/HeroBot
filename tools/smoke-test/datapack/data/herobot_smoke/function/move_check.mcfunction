player Bob stop
execute store result score bob_z smoke run data get entity Bob Pos[2] 100
execute if score bob_z smoke < bob_z_before smoke run say SMOKE OK walk_and_jump
execute unless score bob_z smoke < bob_z_before smoke run say SMOKE FAIL walk_and_jump
# slime block piston launch
setblock 6 -61 6 minecraft:piston[facing=up]
setblock 6 -60 6 minecraft:slime_block
tp Bob 6.5 -59 6.5
schedule function herobot_smoke:piston 20t
