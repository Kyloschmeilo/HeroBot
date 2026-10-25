player Alice attack
execute unless block 0 -61 0 minecraft:grass_block run say SMOKE OK mining
execute if block 0 -61 0 minecraft:grass_block run say SMOKE FAIL mining
setblock 0 -61 0 minecraft:grass_block
tp Alice 0.5 -60 0.5
player Alice hotbar 2
player Alice look at 2.5 -60.0 0.5
schedule function herobot_smoke:place 10t
