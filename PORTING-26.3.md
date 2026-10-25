# HeroBot → Minecraft 26.3

Basis: Upstream-Branch `26.2` (HeroBot 2.7.2). Der `master`-Branch ist noch 1.21.11.

## Bauen

Voraussetzung: JDK 25.

```
gradlew buildAll
```

Die fertigen Jars landen in `build/libs/<mc-version>-<version>+v<datum>/`:
`herobot-fabric-…jar` (Fabric-Mod) und `herobot-paper-…jar` (Paper-Plugin).

## Versionen

| | 26.2 | 26.3 |
|---|---|---|
| Minecraft | 26.2 | 26.3 |
| Fabric Loader | 0.19.3 | 0.20.1 |
| Fabric API | 0.158.0+26.2 | 0.165.0+26.3 |
| Carpet (compileOnly) | 26.2 | 26.3 |
| Paper Dev-Bundle | 26.2.build.121-stable | 26.3.build.209-stable |
| paperweight-userdev | 2.0.0-beta.23 | 2.0.0-beta.24 |
| Simple Voice Chat (nur Dev-Runs) | 2.6.21 | 2.6.25 |
| `minecraft` in fabric.mod.json | >=26 <27 | ~26.3 |

## Code-Änderungen

**Server/Bot (Fabric + Paper)**
- Armschwung: `swing(hand)` / `swing(hand, bool)` gibt es nicht mehr, jeder Schwung braucht eine `SwingAnimation`.
  Neue Hilfsklasse `Swings` (je Modul): Angriff/Abbauen nutzt die Angriffs-Animation des Items,
  Benutzen die Interaktions-Animation, Droppen die Standard-Animation – wie Vanilla.
- `Entity.hurtMarked` → `syncVelocity` (PlayerMixin).
- `invulnerableTime` → `damageCooldownTime` für den Treffer-Cooldown (BotPlayer, LivingEntityMixin, LivingEntityHurtMixin).
- `blockUsingItem` hat einen zusätzlichen Parameter `fullyBlocked` (BotPlayer-Override).
- Explosions-Rückstoß läuft über `pushFromExplosion` statt `push` (ServerExplosionMixin, verzögerter Push im BotPlayer).
- `PushReaction.IGNORE` → `IGNORE_ENTITY` (ShulkerBoxBlockEntityMixin).
- `CommandSourceStack`-Konstruktor ohne Text-/Anzeigenamen (DelayedQueue).
- `ClientboundPlayerChatPacket.unsignedContent()` ist jetzt ein `Optional` (ChatCapture).

**Client (nur Fabric)**
- 26.3 nutzt SDL3 statt GLFW: alle `GLFW_KEY_*`, `GLFW_MOD_*`, `GLFW_MOUSE_BUTTON_*` auf
  SDL-Scancodes / `SDL_KMOD_*` / `InputConstants.MOUSE_BUTTON_*` umgestellt, `InputConstants.Type.KEYSYM` → `KEYBOARD`.
- Kommentar-Bearbeitung im HeroScript-Editor schaltet die SDL-Texteingabe ein/aus (sonst kommen keine Zeichen an).
- Tasten-/Mausklick-Simulation im ClientPlayerController wie in Fabrics eigenem 26.3-Test-Input.
- `LocalPlayer.drop` ist weg → Drop wird direkt per Paket gesendet; Linksklick in die Luft sendet `ServerboundPunchPacket`.
- Minecart-Geister-Rendering (AbstractMinecartRendererMixin) an das neue `submitModel` ohne Crumbling-Overlay angepasst
  und mit `require = 0` abgesichert; `EntityRenderDispatcher.shouldRender` hat einen zusätzlichen Partial-Tick-Parameter.
- `RenderPipeline` liegt jetzt in `com.mojang.renderpearl.api.pipeline`, `ConfirmLinkScreen` will eine `URI`.

## Tests (nur Fabric)

Die GitHub-Action baut nur noch die Fabric-Mod (`gradlew buildFabric`) und testet sie:

- **Mixin-Ziele:** `tools/check-mixin-targets-ci.py` prüft jedes Mixin gegen die echten 26.3-Klassen.
- **Server-Smoke-Test:** `tools/smoke-test/run.sh` startet einen Fabric-Dev-Server mit dem Datenpaket aus
  `tools/smoke-test/datapack`. Zwei Bots spawnen und durchlaufen diese Prüfungen:
  - Schwert-Treffer, Axt gegen Schild
  - Laufen/Springen, Schleimblock-Kolben, TNT-Schaden und -Rückstoß
  - Abbauen, Platzieren, Droppen, Windladung, Boot
  - `/delayed`, Respawn, Disconnect, Befehle nach `/reload`

  Jede Prüfung schreibt `SMOKE OK|FAIL <name>` ins Log.
- **Client-Test:** `gradlew :herobot-mod:runClientGameTest` (Quellcode in `herobot-mod/src/gametest`) startet das echte Spiel
  mit einer Einzelspielerwelt. Geprüft werden alle Mixins, Bots auf dem Client, die Fernsteuerung des Spielers
  (Springen, Droppen, Schwingen) und der HeroScript-Editor: Öffnen, Kommentar tippen, Strg+Z, Schließen.

Frisch gespawnte Bots sind wie echte Spieler die ersten 60 Ticks unverwundbar (Vanilla wartet, bis der „Client“ geladen ist).

Das Paper-Plugin wird in diesem Fork nicht gebaut oder getestet.
