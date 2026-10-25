execute store result score shield_cd smoke run player Bob itemCd minecraft:shield
execute if score shield_cd smoke matches 1.. run say SMOKE OK shield_disabled_by_axe
execute unless score shield_cd smoke matches 1.. run say SMOKE FAIL shield_disabled_by_axe
player Bob use
player Bob stop
execute store result score bob_z_before smoke run data get entity Bob Pos[2] 100
player Bob look north
player Bob sprint
player Bob move forward
player Bob jump continuous
schedule function herobot_smoke:move_check 30t
