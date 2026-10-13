# archive

Test scripts and work-in-progress kept from earlier stages of development. Nothing here
is loaded by the game. It is preserved because the ideas in it are not finished, not
because it is part of the engine.

## Python

### grenade.py
Scratch harness for a **parabolic aim-arc predictor** — the dotted arc you'd see
previewing where a thrown grenade would land. Run it with:

```
python archive/grenade.py
```

The real intent behind it is **parabolic projectiles / grenade throwing, which is not
implemented anywhere yet**. `scripts/rotation.py` already has a working 5-step
`draw_curve()` that `game.py` calls for the aiming arc; this file draws a 51-step one.
The arc math is the part worth keeping.

### test_scripts/
Scaffolding for the water physics that graduated into `scripts/water.py` and
`scripts/water_springs.py`. These were the experiments — springs, bounce, wave
propagation — before the behaviour moved into the engine.

Run any of them from the repo root, e.g.:

```
python archive/test_scripts/spring_t.py
```

`archive/test_scripts/spring_t.py` has a keyboard handler uncommented and
`Game().run()` re-enabled, so it is the most interactive of the set.

## Images

### images/test/
`bullets/` and `slash/` particle sheets. Only ever referenced by the commented-out
`run()` block in `scripts/rotation.py`.

### images/temp_player/
An earlier player sprite set, replaced by `data/images/entities/player/`. Same story —
only the commented-out `run()` block pointed at it.

Neither directory is in the asset registry and neither appears in `data/maps/map.json`.
