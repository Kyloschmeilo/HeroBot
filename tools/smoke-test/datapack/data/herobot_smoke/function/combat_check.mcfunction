execute store result score bob_hp smoke run data get entity Bob Health
execute if score bob_hp smoke < bob_hp_before smoke run say SMOKE OK attack_damage
execute unless score bob_hp smoke < bob_hp_before smoke run say SMOKE FAIL attack_damage
item replace entity Bob weapon.offhand with minecraft:shield
tp Bob 0.5 -60 -1.5
tp Alice 0.5 -60 0.5
player Alice hotbar 4
player Alice look upon Bob
player Bob look upon Alice
player Bob use continuous
schedule function herobot_smoke:shield 30t
