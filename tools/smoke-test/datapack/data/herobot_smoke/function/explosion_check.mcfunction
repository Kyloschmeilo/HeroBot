difficulty peaceful
execute store result score bob_hp smoke run data get entity Bob Health
execute store result score bob_x smoke run data get entity Bob Pos[0] 100
execute if score bob_hp smoke < bob_hp_before smoke run say SMOKE OK explosion_damage
execute unless score bob_hp smoke < bob_hp_before smoke run say SMOKE FAIL explosion_damage
execute if score bob_x smoke < bob_x_before smoke run say SMOKE OK explosion_knockback
execute unless score bob_x smoke < bob_x_before smoke run say SMOKE FAIL explosion_knockback
# mining with an empty hand
tp Alice 0.5 -60 0.5
player Alice hotbar 6
player Alice look down
player Alice attack continuous
schedule function herobot_smoke:mine_check 60t
