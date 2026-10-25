execute store result score bob_hp smoke run data get entity Bob Health 100
data modify storage herobot_smoke:d tag set value "attack_after_switch"
function herobot_smoke:attack_info
execute if score bob_hp smoke < bob_hp_before smoke run say SMOKE OK attack_damage
execute unless score bob_hp smoke < bob_hp_before smoke run say SMOKE FAIL attack_damage
# second hit with a fully charged sword from the same spot
tp Bob 0.5 -60 -2.5 facing 0.5 -58.4 0.5
schedule function herobot_smoke:combat_charged 25t
