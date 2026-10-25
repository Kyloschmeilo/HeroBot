execute store result score bob_hp smoke run data get entity Bob Health 100
data modify storage herobot_smoke:d tag set value "attack_charged"
function herobot_smoke:attack_info
# a charged iron sword deals 6 damage (600 here); peaceful regeneration may give one heart back
scoreboard players operation bob_hp_before smoke -= bob_hp smoke
execute if score bob_hp_before smoke matches 400.. run say SMOKE OK attack_damage
execute unless score bob_hp_before smoke matches 400.. run say SMOKE FAIL attack_damage
item replace entity Bob weapon.offhand with minecraft:shield
tp Bob 0.5 -60 -1.5
tp Alice 0.5 -60 0.5
player Alice hotbar 4
player Alice look upon Bob
player Bob look upon Alice
player Bob use continuous
schedule function herobot_smoke:shield 30t
