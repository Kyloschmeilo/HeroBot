execute unless entity Alice unless entity Bob run say SMOKE OK disconnect
execute if entity Alice run say SMOKE FAIL disconnect
# reload the data packs; load.mcfunction then runs reload_check
scoreboard players set reloaded smoke 1
reload
