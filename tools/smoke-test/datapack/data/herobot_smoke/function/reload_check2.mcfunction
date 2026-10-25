execute if entity Carol run say SMOKE OK commands_after_reload
execute unless entity Carol run say SMOKE FAIL commands_after_reload
function herobot_smoke:reload_cleanup
schedule function herobot_smoke:done 20t
