# Ailments — Complete Reference

## Overview

Ailments are status effects typically applied by hits. Two main categories:
- **Damaging ailments**: Ignite, Bleed, Poison — deal damage over time
- **Non-damaging ailments**: Shock, Chill, Freeze, Scorch, Brittle, Sap — apply debuffs

A target can have any number of different ailments simultaneously. There is no limit to how
many distinct ailment types can be active on one enemy at once.

---

## How Ailments Are Applied

### Application Chances
- **Chill**: 100% chance on ANY hit that deals cold damage — no investment needed
- **Ignite**: 0% base chance. Guaranteed on critical strikes with fire damage. Otherwise needs explicit "chance to ignite"
- **Freeze**: 0% base chance. Guaranteed on critical strikes with cold damage. Must deal enough damage to meet minimum duration
- **Shock**: 0% base chance. Guaranteed on critical strikes with lightning damage. Otherwise needs "chance to shock"
- **Bleed**: 0% base chance. Requires "chance to bleed" AND must come from an ATTACK (spells cannot cause bleed)
- **Poison**: 0% base chance. Requires "chance to poison." Can come from physical OR chaos damage
- **Scorch/Brittle/Sap**: 0% base chance. Require specific enabling sources (see Alternative Ailments section)

### General Rules
- Enemy must take at least 1 point of the relevant damage type for the ailment to apply
- Damage over time cannot apply ailments (DoT doesn't hit)
- Ailment application is rolled per hit
- If damage is fully mitigated (0 damage taken), the ailment still applies as long as damage was DEALT

### On-Kill Timing Difference
- **Elemental ailments** (ignite, shock, chill, freeze): Killing an unaffected enemy with a hit that would apply the ailment DOES count as "killing an ignited/shocked/etc enemy" for on-kill triggers
- **Non-elemental ailments** (bleed, poison): Killing an enemy with a hit that applies bleed/poison does NOT count as "killing a bleeding/poisoned enemy" — the enemy must already have the ailment before the killing hit

---

## Ailment Threshold

Non-damaging ailment effects (shock, chill, freeze, scorch, brittle, sap) scale based on
damage dealt relative to the enemy's **ailment threshold**.

- For most monsters: ailment threshold = maximum life
- Pinnacle bosses have REDUCED thresholds to make ailments achievable
  - Sirus estimated threshold: ~25 million (~35% of boss life)
  - Shaper and similar have proportionally reduced thresholds
- The effect formula (for shock as an example):
  ```
  Shock Effect = 50% × (Damage / Ailment_Threshold)^0.4 × (1 + increased_shock_effect)
  ```
  Where the result is clamped between the minimum (5%) and maximum (50%)
- Chill uses a similar formula but with 30% maximum and different coefficient
- If the calculated effect falls below the minimum threshold, the ailment is discarded entirely
- **"Increased effect of X"** modifiers multiply the result — they make it easier to reach both the minimum and maximum caps

---

## The Ailment Damage Pipeline (Critical Concept)

Damaging ailment DPS is calculated SEPARATELY from hit DPS. They share the same base damage
but are then scaled by DIFFERENT modifier pools. This prevents "double-dipping."

### How It Works
```
Ailment Base = Skill's flat damage (base + added × effectiveness + conversion)
             → Only the damage types relevant to that ailment count
             → This is the SAME base used for hit calculation, but BEFORE increases/more
             
Ailment DPS = Ailment Base × Ailment Rate (e.g., 50% per second for ignite)
            × (1 + sum of all applicable "increased" modifiers for the AILMENT)
            × product of all "more" multipliers for the AILMENT
            × (1 + sum of all DoT multiplier sources)
            × (1 + crit DoT multi bonus, if from a crit)
```

### What DOES Scale Ailment Damage
- Generic "damage" and "damage over time"
- Matching OUTPUT damage type (fire for ignite, physical for bleed, chaos for poison)
- "Damage over time multiplier" (and type-specific DoT multi)
- Specific ailment modifiers ("burning damage" for ignite, "poison damage," "bleeding damage")
- "Damage with hits and ailments" — explicitly covers both (common on gear, Singularity, etc.)
- Cruelty buff (grants more DoT based on hit damage taken by enemy)

### What Does NOT Scale Ailment Damage
- Spell damage, attack damage (unless skill specifically says otherwise)
- Melee damage, projectile damage, area damage
- Weapon damage modifiers
- Penetration (only affects hits, not DoT)
- Double/triple damage (only affects the hit roll, not the ailment base)
- Critical strike multiplier (does NOT affect ailment damage — see crit section below)
- Lucky damage (only affects hit rolls)

### Conversion and Ailments
- Only the relevant portion of base damage contributes to the ailment
- Ignite: only FIRE damage in the base counts (after conversion). If you convert phys→fire, the converted fire counts.
- Bleed: only PHYSICAL damage counts
- Poison: physical AND chaos damage both count
- The enemy's resistance to the OUTPUT type mitigates the ailment, not the input type
  - Example: cold damage converted to fire → ignite → mitigated by enemy's FIRE resistance, not cold

---

## Damaging Ailments

### Ignite (Fire)
- Deals **burning damage** (fire damage over time)
- Base duration: **4 seconds**
- Base DPS: **50% of the base fire damage per second** (200% total over full duration)
  - *Note: verify this value via poedb.tw if building around ignite — GGG has adjusted this across patches*
- Only the STRONGEST ignite deals damage — multiple ignites exist but only the highest DPS one is active
  - Exception: Emberwake unique ring allows two ignites to deal damage simultaneously
- Crits: guaranteed ignite + the crit DoT multi bonus (see below)
- **Scaling priority**: Stack one massive hit. Slow, hard-hitting skills (slams, charged skills) excel for ignite.
- Key supports: Deadly Ailments, Burning Damage, Swift Affliction, Ignite Proliferation, Combustion
- Ignite can be inflicted by non-fire damage IF you have enabling effects:
  - Shaper of Flames (Elementalist): ALL damage can ignite
  - Stormfire ring: lightning damage can ignite
  - Hrimburn gloves: cold damage can ignite
  - Three Dragons: changes which elements apply which ailments

### Bleed (Physical)
- Deals physical damage over time
- Base duration: **5 seconds**
- Base DPS: **70% of base physical damage over the full duration** (14% per second)
  - *Verify via poedb.tw — values may have been adjusted*
- **Deals 100% more damage while the target is MOVING** — enormous for mapping, weaker on stationary bosses
- Only ATTACKS can inflict bleed — spells cannot
- By default: only strongest bleed deals damage (no stacking)
- **Crimson Dance keystone**: Up to 8 bleeds stack simultaneously, BUT the moving bonus is disabled
  - Decision: Crimson Dance for fast-hitting attack builds; single bleed for slow slams that force movement
- Scaled by: physical damage, damage over time, DoT multiplier, physical DoT multiplier
- Key supports: Brutality (if pure physical), Deadly Ailments, Swift Affliction, Chance to Bleed (early only)

### Poison (Chaos)
- Deals chaos damage over time
- Base duration: **2 seconds**
- Base DPS: **30% of combined base physical + chaos damage over the full duration** (15% per second)
  - *Verify via poedb.tw*
- **STACKS INFINITELY** — every application of poison is its own independent instance with its own duration
- This makes poison scale with **hit frequency** — fast attacks with high chance to poison = massive stacking
- Scaled by: chaos damage, damage over time, DoT multiplier, chaos DoT multiplier, poison damage
- Physical damage only matters for BASE calculation — "increased physical damage" does NOT scale poison DPS
- Poison always deals CHAOS damage regardless of what damage types caused it
  - Therefore: only Chaos DoT multi applies, never Physical DoT multi or Lightning DoT multi etc.
- Key supports: Deadly Ailments, Void Manipulation, Swift Affliction, Greater Multiple Projectiles (for more hits)
- Duration matters: longer poison = more total damage per stack. "Increased poison duration" is a DPS increase for stacking builds.

---

## Non-Damaging Ailments

### Shock (Lightning)
- Causes target to take **increased damage from ALL sources**
- Default maximum effect: **50% increased damage taken**
- Minimum effect: **5%** (below this, shock is discarded)
- Base duration: **2 seconds**
- Effect formula: 50% × (D/T)^0.4 × (1 + M) where D = lightning damage, T = ailment threshold, M = increased shock effect
- **Shock effect modifiers** reduce the damage needed to reach minimum AND maximum
  - 100% increased shock effect: minimum requires only ~0.06% of threshold; maximum requires ~17.68%
- Multiple shocks can exist on one enemy but only the strongest applies
- Shocks applied without dealing damage (Shocked Ground, Skitterbots) have a base effect of **15%**
- Key interaction: **Elementalist's Shaper of Storms** guarantees ALL hits shock with minimum 15% effect regardless of damage type or amount
- **Herald of Thunder note**: HoT storm damage CANNOT inflict shock. Storm Secret changes trigger condition from kill→shock, but the shock must come from another source.

### Chill (Cold)
- Reduces target's **action speed** (attack speed, cast speed, movement speed all slowed)
- Default maximum effect: **30% reduced action speed**
- Minimum effect: **5%**
- Base duration: **2 seconds**
- Applied by ANY hit that deals cold damage — 100% base chance, no investment needed
- Defensive AND offensive: slowed enemies are less dangerous and easier to kite
- **Bonechill Support**: enemies take increased cold DoT equal to the chill effect on them
- Chill is independent from freeze — an enemy can be chilled without being frozen, and vice versa
- Sources without damage (Chilled Ground, Skitterbots) apply base 10% chill

### Freeze (Cold)
- **Completely immobilizes** the target — zero action speed
- Duration (not effect) scales with cold damage relative to ailment threshold
- **Minimum freeze duration: 0.3 seconds** — below this, freeze doesn't apply at all
- Frozen enemies can be **shattered** on kill → destroys corpse, prevents on-death effects (extremely valuable)
- Incredibly powerful defensive layer but very hard to apply on bosses (huge ailment thresholds)
- Many bosses have partial or full freeze immunity
- Freeze does NOT have an "effect" like shock/chill — it's binary (frozen or not), only duration varies

---

## Alternative Ailments (Scorch, Brittle, Sap)

These replace the DEFAULT ailment for their element. They are NOT automatically available — you
need specific sources that enable them.

### How to Access Alt Ailments
- **Elementalist ascendancy nodes** can enable alt ailments
- Specific unique items (e.g., Polaric Devastation for scorch)
- Secrets of Suffering keystone (from specific unique jewels): replaces ALL default elemental ailments with their alternates — you lose ignite/shock/chill/freeze but gain scorch/sap/brittle
- Each enabling source specifies what it replaces

### Scorch (Fire — Replaces Ignite)
- Reduces target's **ALL elemental resistances**
- Maximum effect: **-30% to all elemental resistances**
- Minimum effect: **2%**
- Base duration: 4 seconds
- Effect scales with fire damage relative to ailment threshold (similar formula to shock/chill)
- Maximum requires ~28% of ailment threshold as fire damage
- Extremely powerful — effectively free penetration as an ailment

### Brittle (Cold — Replaces Chill/Freeze)
- Increases **base critical strike chance** against the target
- Maximum effect: **+15% to base critical strike chance**
- Minimum effect: ??? (low)
- If your build crits, Brittle is often MORE valuable than Shock because it multiplicatively affects your crit chance
- Can trivially cap crit chance for builds that invest in crit

### Sap (Lightning — Replaces Shock)
- Reduces target's **damage dealt**
- Maximum effect: **20% reduced damage dealt**
- Purely defensive — less raw DPS value than Shock, but great for survivability
- Particularly useful in hardcore or builds facing dangerous bosses

### Alt Ailment Trade-off
Enabling alt ailments means LOSING the default ailment. Secrets of Suffering gives you all three alternates but you lose ignite (no burning damage), shock (no increased damage taken), chill/freeze (no slow, no shatter). This is a significant trade-off that must be evaluated per build.

---

## Crit Interaction with Ailments

### For Application
- Critical strikes guarantee ignite, freeze, and shock (100% chance)
- Crits do NOT guarantee bleed or poison (still need explicit chance)
- Crits do guarantee alt ailments IF the enabling source is present

### For Damaging Ailment Damage
- Ailments from critical strikes gain **+50% to Damage over Time Multiplier**
- This is ADDITIVE with other DoT multi sources, NOT a separate "more" multiplier
- This is SEPARATE from the hit's critical strike multiplier — crit multi does NOT affect ailment damage
- Example: 50% base crit DoT multi + 40% fire DoT multi from tree = 90% total DoT multi
- **Perfect Agony keystone**: Causes a portion of your crit multi modifiers to apply to ailment DoT multi instead
  - Trade-off: your hit damage is reduced, but ailment damage benefits from crit multi investment
  - Good for builds that scale ailments through crits
- **Elemental Overload**: Prevents ailments from EVER counting as being from critical strikes → removes the +50% DoT multi bonus entirely. Bad for ailment builds that crit.
- **Critical Strike Affliction Support**: Adds significant additional DoT multi for ailments from crits

---

## Ailment Duration Modifiers

### Increasing Duration
- "% increased duration of X" — longer ailment = more total damage (for damaging ailments at same DPS)
- For poison stacking builds: longer duration = more simultaneous stacks = more total DPS
- For bleed: longer duration means the moving bonus has more time to apply
- For ignite: longer duration is mostly QoL (single ignite deals same DPS, just lasts longer)

### "Faster" Mechanics
- "Ailments deal damage X% faster" / "Ignited Enemies Burn Y% faster"
- This INCREASES DPS but DECREASES duration proportionally
- Total damage dealt remains the same — it's compressed into a shorter window
- For non-stacking ailments (ignite, bleed): faster = higher DPS but shorter duration. Good if you can reapply.
- For stacking ailments (poison): faster has minimal net effect over time since stacks fall off faster too
- **Key distinction**: "faster" is NOT "more damage." Same total, shorter time.

### Temporal Chains Interaction
- Temporal Chains slows ailment expiration on cursed enemies
- Effectively extends ailment duration without changing DPS → more total damage
- Extremely powerful for all ailment builds, especially poison stacking

---

## Elemental Proliferation

Spreads elemental ailments from one enemy to nearby enemies.

### Mechanics
- When an enemy with an elemental ailment is killed, the ailment spreads to nearby enemies within a radius
- The proliferated ailment is a COPY — same magnitude, same remaining duration
- Does NOT create new ailments from scratch — requires an existing source
- Only spreads ELEMENTAL ailments (ignite, shock, chill, freeze, scorch, brittle, sap). NOT bleed or poison.
- Radius of spread matters — larger radius = better pack coverage

### Sources
- **Elemental Proliferation Support**: linkable support gem, moderate radius
- **Doryani's Catalyst**: built-in Level 20 Ele Prolif for socketed gems (sceptre)
- **Beacon of Ruin (Elementalist)**: proliferates ailments in an area around enemies you hit
- **Berek's Respite**: on killing a shocked/ignited enemy, inflicts equivalent ailment on nearby enemies
- **Ignite Proliferation Support**: specifically for ignite, larger radius

### Practical Impact
One good ailment application + proliferation = entire pack affected. This is what makes shock
proliferation so powerful for builds like HoT autobombers — shock one enemy, the pack is shocked,
HoT storms activate on all shocked enemies.

---

## Ailment Immunity & Avoidance

### Player-side Defenses
- "Cannot be affected by X" = full immunity to that ailment
- "X% chance to avoid elemental ailments" = probabilistic, per-hit check
- 100% avoidance = effective immunity
- **Purity of Elements aura**: grants full elemental ailment immunity to you and allies
- Flasks: can remove ailments + grant temporary immunity during flask effect
- Specific Pantheon powers reduce ailment effect or duration (e.g., Soul of the Brine King for stun/freeze)
- Freeze immunity is particularly important — getting frozen in a pack is often instant death

### Enemy-side Defenses  
- Some bosses have partial or full immunity to specific ailments (freeze immunity is common)
- Map mods: "Monsters have X% chance to avoid elemental ailments" — reduces your ailment application
- **Hexproof**: prevents CURSE application, but does NOT affect ailments (common confusion)

---

## "Damage with Hits and Ailments" — Stat Wording

This is a specific modifier category that explicitly covers BOTH hit damage AND ailment damage:
- "Increased damage with hits and ailments against [condition]" — both components benefit
- Found on: gear, support gems (Hypothermia, Ruthless), Singularity, various sources
- Contrast with "increased damage" (generic, also covers both) vs "increased attack damage" (hits only)
- Reading modifier wording carefully is essential for ailment builds — one word changes everything

---

## Practical Decision Framework

When building around ailments:

1. **Pick ONE primary ailment** and scale it hard — spreading across ailment types is inefficient
2. **For ignite builds**: Stack one massive hit. Slow, hard-hitting skills excel. Elementalist or Chieftain.
3. **For poison builds**: Stack hit frequency. Fast, multi-hit skills (Blade Vortex, Cobra Lash, Viper Strike). Assassin or Pathfinder.
4. **For bleed builds**: Force movement where possible (Puncture for single target). Gladiator. Choose Crimson Dance vs single bleed intentionally.
5. **For shock as utility**: Shaper of Storms (Elementalist) trivializes shock application. Even a 15% minimum shock is a huge damage boost for your whole build.
6. **Proliferation transforms clear speed** — one good ailment application covers the entire pack
7. **Boss ailment thresholds are HIGH** — you need either significant damage, high ailment effect, or both to matter on pinnacle content
8. **Conversion enables ailments on unexpected skills** — physical skill → convert to fire → ignite build
9. **DoT multiplier is often the most efficient scaling category** — fewer builds invest heavily in it, so each point of DoT multi is worth more than another point of "increased"
10. **Always check if "faster" is actually better than "more damage"** — faster doesn't increase total damage, just compresses it. Only valuable if you can reapply consistently.
