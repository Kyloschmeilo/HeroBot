#!/usr/bin/env bash
# Starts a Fabric dev server with HeroBot and the smoke-test data pack, which spawns two bots, puts
# them through combat, movement, blocks, explosions, a slime piston, a boat and a respawn, reloads
# the data packs, checks the commands still work and then stops the server.
# Usage: tools/smoke-test/run.sh
set -u
root=$(cd "$(dirname "$0")/../.." && pwd)
run="$root/herobot-mod/run"

rm -rf "$run/world" "$run/logs"
mkdir -p "$run/world/datapacks"
cp -r "$root/tools/smoke-test/datapack" "$run/world/datapacks/herobot_smoke"

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

timeout 600 "$root/gradlew" -p "$root" :herobot-mod:runServer --console=plain < /dev/null
echo "server exited with code $?"
