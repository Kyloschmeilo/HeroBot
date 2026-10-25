player Alice look upon Bob
execute store result score bob_hp_before smoke run data get entity Bob Health 100
player Alice attack once
schedule function herobot_smoke:combat_charged_check 5t
