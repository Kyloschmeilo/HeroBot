execute if block 2 -60 0 minecraft:cobblestone run say SMOKE OK place_block
execute unless block 2 -60 0 minecraft:cobblestone run say SMOKE FAIL place_block
kill @e[type=minecraft:item]
player Alice drop once
schedule function herobot_smoke:drop_check 10t
