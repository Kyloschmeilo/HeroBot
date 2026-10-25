execute if entity Bob run say SMOKE OK respawn
execute unless entity Bob run say SMOKE FAIL respawn
player Alice disconnect
player Bob disconnect
schedule function herobot_smoke:finish 20t
