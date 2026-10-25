# Logs the numbers behind an attack check (storage tag must be set by the caller).
execute store result storage herobot_smoke:d before int 1 run scoreboard players get bob_hp_before smoke
execute store result storage herobot_smoke:d after int 1 run scoreboard players get bob_hp smoke
execute store result storage herobot_smoke:d hurt int 1 run data get entity Bob HurtTime
execute store result storage herobot_smoke:d az int 1 run data get entity Alice Pos[2] 100
execute store result storage herobot_smoke:d bz int 1 run data get entity Bob Pos[2] 100
execute store result storage herobot_smoke:d yaw int 1 run data get entity Alice Rotation[0] 100
execute store result storage herobot_smoke:d pitch int 1 run data get entity Alice Rotation[1] 100
function herobot_smoke:attack_info_say with storage herobot_smoke:d
