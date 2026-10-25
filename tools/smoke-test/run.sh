#!/usr/bin/env bash
# Starts a dev server with HeroBot and the smoke-test data pack, which spawns two bots, puts them
# through combat, movement, blocks, explosions, a slime piston, a boat and a respawn, then stops
# the server. Usage: tools/smoke-test/run.sh fabric|paper
set -u
platform=$1
root=$(cd "$(dirname "$0")/../.." && pwd)
case "$platform" in
  fabric) run="$root/herobot-mod/run"; task=":herobot-mod:runServer" ;;
  paper) run="$root/herobot-plugin/run"; task=":herobot-plugin:runServer" ;;
  *) echo "usage: $0 fabric|paper"; exit 2 ;;
esac

rm -rf "$run/world" "$run/logs"
mkdir -p "$run/world/datapacks"
pack="$run/world/datapacks/herobot_smoke"
cp -r "$root/tools/smoke-test/datapack" "$pack"
if [ "$platform" = paper ]; then
  # /delayed only exists in the Fabric mod
  rm "$pack/data/herobot_smoke/function/fabric_only.mcfunction"
  sed -i '/fabric_only/d' "$pack"/data/herobot_smoke/function/*.mcfunction
  # Paper registers plugin commands after the data packs load, so functions using /player fail
  # to parse on the first load. Start the test only after a data reload.
  cat > "$pack/data/herobot_smoke/function/load.mcfunction" <<'MCF'
scoreboard objectives add smoke dummy
execute if score paper_reloaded smoke matches 1 run function herobot_smoke:start
execute unless score paper_reloaded smoke matches 1 run schedule function herobot_smoke:paper_reload 40t
MCF
  cat > "$pack/data/herobot_smoke/function/paper_reload.mcfunction" <<'MCF'
scoreboard players set paper_reloaded smoke 1
minecraft:reload
MCF
fi

cat > "$run/server.properties" <<'PROPS'
online-mode=false
level-type=minecraft\:flat
difficulty=peaceful
spawn-protection=0
function-permission-level=4
view-distance=4
simulation-distance=4
max-tick-time=-1
generate-structures=false
PROPS
echo "eula=true" > "$run/eula.txt"

timeout 600 "$root/gradlew" -p "$root" "$task" --console=plain < /dev/null
echo "server exited with code $?"
