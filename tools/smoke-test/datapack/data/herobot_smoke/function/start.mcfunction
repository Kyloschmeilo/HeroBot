# Sets up the test area and spawns the bots. Every check prints "SMOKE OK <name>" or "SMOKE FAIL <name>".
say SMOKE START
forceload add -16 -16 16 16
time set noon
fill -12 -61 -12 12 -61 12 minecraft:grass_block
fill -12 -60 -12 12 -50 12 minecraft:air
schedule function herobot_smoke:spawn 40t
