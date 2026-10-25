execute store result score bob_hp smoke run data get entity Bob Health 100
data modify storage herobot_smoke:d tag set value "attack_after_switch"
function herobot_smoke:attack_info
# The weak hit only deals about one heart, which peaceful regeneration may already have healed,
# so this check looks at the hurt animation; the charged hit below checks the damage.
execute store result score bob_hurt smoke run data get entity Bob HurtTime
execute if score bob_hurt smoke matches 1.. run say SMOKE OK attack_hit
execute unless score bob_hurt smoke matches 1.. run say SMOKE FAIL attack_hit
# second hit with a fully charged sword from the same spot
tp Bob 0.5 -60 -2.5 facing 0.5 -58.4 0.5
schedule function herobot_smoke:combat_charged 25t
