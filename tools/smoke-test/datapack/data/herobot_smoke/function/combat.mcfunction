execute if entity Alice run say SMOKE OK spawn_alice
execute unless entity Alice run say SMOKE FAIL spawn_alice
execute if entity Bob run say SMOKE OK spawn_bob
execute unless entity Bob run say SMOKE FAIL spawn_bob
item replace entity Alice hotbar.0 with minecraft:iron_sword
item replace entity Alice hotbar.1 with minecraft:cobblestone 16
item replace entity Alice hotbar.2 with minecraft:wind_charge 4
item replace entity Alice hotbar.3 with minecraft:iron_axe
# first hit right after switching to the sword: weak, but it has to land
player Alice hotbar 1
player Alice look upon Bob
execute store result score bob_hp_before smoke run data get entity Bob Health 100
player Alice attack once
schedule function herobot_smoke:combat_check 5t
