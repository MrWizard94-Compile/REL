# Damage Pipeline — Complete Reference

## The Damage Formula

### Hit Damage
```
Final Hit DPS =
  Base Damage (weapon or gem)
  + Added Flat Damage (× damage effectiveness)
  × (1 + sum of all "increased/reduced" modifiers)
  × (1 + more_1) × (1 + more_2) × ... × (1 + more_N)
  × Hit Rate (attacks per second or casts per second)
  × Crit Factor [(1 - effective_crit) + (effective_crit × crit_multi / 100)]
  × Enemy Resistance/Mitigation Factor
```

### Damage over Time
```
DoT DPS =
  Base DoT (from gem, or from ailment hit calculation)
  × (1 + sum of all applicable "increased/reduced" modifiers)
  × (1 + more_1) × ... × (1 + more_N)
  × (1 + sum of all DoT multiplier sources)
  × Enemy Resistance Factor
```

**Key difference:** DoT has NO crit factor (unless from ailment applied by a crit — see below),
NO hit rate component, and has its own separate "DoT multiplier" category.

Every build optimization is about finding the weakest multiplier in the chain and improving it.

---

## Damage Types

PoE has five damage types. Each has its own mitigation:

| Type | Mitigated By | Notes |
|------|-------------|-------|
| Physical | Armour (hits) + Physical Damage Reduction | Most common from weapon attacks |
| Fire | Fire Resistance | Burning damage is fire DoT |
| Cold | Cold Resistance | Chill/Freeze associated |
| Lightning | Lightning Resistance | Shock associated; highest damage variance |
| Chaos | Chaos Resistance | Bypasses Energy Shield by default |

**Lightning damage variance:** Lightning damage ranges are the widest (e.g., 1-500 vs cold's 200-300).
This makes "Damage is Lucky" (rolls twice, takes higher) especially powerful for lightning builds.

---

## Damage Sources (The Four Categories)

Every instance of damage is exactly ONE of these four categories. They are mutually exclusive.

### 1. Attacks
- Base damage comes from your **weapon** (or unarmed base for specific skills)
- Weapon damage range is modified by the skill's **attack damage** percentage
- Added flat damage (from gear, auras, gems) is added, then everything is multiplied by **damage effectiveness**
- Attacks require **accuracy** to hit (exceptions: Resolute Technique, "hits can't be evaded" mods)
- Dual wielding alternates attacks between main hand and off hand
- **Local vs Global weapon mods** (see section below)

### 2. Spells
- Base damage comes from the **skill gem's level** (NOT your weapon)
- Gem level is THE most important scaling lever for spells
- Added flat damage is multiplied by the gem's **damage effectiveness** percentage, then added to base
- Spells always hit (no accuracy needed)
- Weapon mods marked "local" (flat phys, % increased phys on weapons) do NOT affect spells
- Weapon mods marked "global" ("+1 to level of spell skill gems," "% increased spell damage") DO affect spells

### 3. Secondary Damage
- Examples: Herald of Thunder storms, Molten Shell explosion, Detonate Dead corpse explosion
- NOT classified as attack or spell damage
- Cannot be modified by "spell damage" or "attack damage" specific stats
- CAN be modified by generic damage, elemental damage, specific element damage
- This is why Herald of Thunder damage is hard to scale — "spell damage" doesn't work on it

### 4. Damage over Time (DoT)
- All DoT is a debuff, not a hit — it does NOT hit
- Because it doesn't hit: no crit, no accuracy, no block, no evasion, no armour (for ele/chaos)
- Two sub-categories:
  - **Ailment DoT**: Ignite, Bleed, Poison — triggered by a hit, damage based on the hit
  - **Skill DoT**: Blight, Essence Drain, Righteous Fire, Scorching Ray — damage from gem level
- Scaled by: base DoT, increased damage, more damage, **DoT multiplier** (its own category)
- "Modifiers to spell damage apply to this skill's DoT" — some skills explicitly allow spell damage to scale their DoT (e.g., Vortex, Death Aura). Read the gem carefully.
- Attack/cast speed does NOT directly affect DoT DPS (but can affect how fast you APPLY ailments)

---

## "More" vs "Increased" — The Critical Distinction

### Increased / Reduced (Additive within category)
- All sources of "increased X damage" ADD TOGETHER into ONE multiplier
- "Reduced" subtracts from the same pool
- Example: 100% increased fire + 50% increased elemental + 30% increased damage = 180% total increased → ×2.8 multiplier
- **Diminishing returns**: going from 0% to 100% increased = 100% more DPS. Going from 400% to 500% = only 20% more DPS.
- Sources: passive tree, gear mods, some ascendancy nodes, flask effects

### More / Less (Multiplicative between sources)
- Each "more" modifier multiplies INDEPENDENTLY with everything else
- Each "less" modifier divides independently
- Example: 40% more × 30% more = 1.4 × 1.3 = 1.82 (82% more total)
- **NO diminishing returns** between separate "more" sources
- Sources: support gems (primary source), keystones, some ascendancy nodes, certain auras
- This is why support gem selection matters so much — each is a separate multiplier

### The Practical Rule
If you have 500% increased damage, adding another 50% increased is only ~8% more DPS.
But adding a new 30% more multiplier is a full 30% more DPS.
**Always diversify scaling categories.** Once you have heavy "increased" investment, seek "more" multipliers, flat damage, penetration, or crit.

---

## Damage over Time Multiplier

DoT Multiplier (often "DoT multi") is a SEPARATE damage category that ONLY affects DoT:
- All sources of DoT multi are **additive with each other** (like "increased")
- But the total is **multiplicative with everything else** (like a "more" multiplier)
- Specific variants exist: Fire DoT multi, Chaos DoT multi, Physical DoT multi — these only affect DoTs of that type
- For ailments: DoT multi only scales the OUTPUT damage type, NOT the input. Poison always uses Chaos DoT multi regardless of what damage type caused the poison.
- **Crit bonus**: Ailments from critical strikes gain an inherent +50% DoT multiplier (separate from the hit's crit multi). This is NOT the same as the hit crit multiplier.
- Elemental Overload disables this crit ailment bonus
- Perfect Agony keystone causes crit multi to apply to ailments instead of the normal DoT multi bonus

---

## Conversion Chain

Damage converts in a fixed, one-directional order:
```
Physical → Lightning → Cold → Fire → Chaos
```

### Key Rules
- Conversion happens BEFORE increases/multipliers are applied
- Converted damage benefits from modifiers to BOTH the original AND final damage type
- You cannot convert backwards (fire cannot become cold, cold cannot become lightning)
- Total conversion FROM one type cannot exceed 100%
- If conversion sources exceed 100%, they are normalized proportionally
  - Example: 60% phys to lightning + 60% phys to cold = 120% total → normalized to 50%/50%
- Skill gem conversion is applied first, then other sources

### Conversion Example
100 physical damage, 50% converted to lightning:
- With 100% increased physical AND 100% increased lightning:
  - 50 physical remains → ×(1 + 1.0 phys) = 100 physical
  - 50 converted to lightning → ×(1 + 1.0 phys + 1.0 lightning) = 150 lightning
  - **Total: 250 damage** (vs 200 without conversion double-dipping)

The converted portion benefits from BOTH modifier pools. This is why conversion builds are powerful.

---

## "Gain X% as Extra" Damage

- Works like conversion but does NOT remove the original damage
- Same modifier inheritance rules — the "extra" portion benefits from both original and new type modifiers
- Can exceed 100% (no cap)
- Stacks with actual conversion
- Sources: Hatred (phys as extra cold), Herald of Ash, support gems, gear mods
- Extremely powerful because it's effectively free additional base damage

---

## Local vs Global Modifiers

This distinction matters enormously for weapons and armour:

### Local Modifiers (affect the ITEM itself)
- On weapons: "% increased Physical Damage," "Adds X to Y Physical Damage," "% increased Attack Speed" — these modify the weapon's displayed stats directly
- On armour: "% increased Armour," "% increased Evasion" — these modify the armour's displayed stats
- **Test**: if the item's top-section stats change color (showing modification), the mod is local

### Global Modifiers (affect your CHARACTER)
- On weapons: "+1 to level of all Spell Skill Gems," "% increased Spell Damage," "Adds X to Y Fire Damage to Spells"
- On any gear: "% increased Global Physical Damage" (note the word "global")
- On non-weapon gear: ALL flat damage mods are global (e.g., "Adds X to Y Lightning Damage to Attacks" on a ring)

### Why This Matters
- Local "% increased Physical Damage" on a weapon scales the weapon's base damage (huge for attacks)
- Global "% increased Physical Damage" from the tree is additive with all other "increased" sources
- Flat damage on a weapon is LOCAL (added to weapon base before % scaling) — much more valuable than flat damage on a ring (which is global)
- Spellcasters using a weapon care about global mods only — local weapon damage does nothing for spells

---

## Dual Wielding

- Attacks alternate between main hand and off hand (unless the skill specifies otherwise)
- Each hand calculates damage independently using its own weapon stats
- Dual wield bonuses: +10% more attack speed, +15% additional block chance, +20% more physical attack damage (total, not per hand)
- Spells with dual wield: gem-level spells use the GLOBAL stats from both weapons but don't alternate
- Shield users sacrifice dual wield bonuses for block chance and shield-specific mods

---

## Penetration vs Resistance Reduction vs Exposure

These are three DIFFERENT mechanics for overcoming enemy resistances:

### Penetration
- Applies only to HITS (not DoT)
- Calculated at the moment of the hit — treats enemy resistance as lower
- Does NOT actually change the enemy's resistance value
- All penetration sources are additive with each other
- **Still works on enemies with negative resistance** (makes it even more negative)
- Sources: support gems (Lightning Pen, Fire Pen, etc.), passive tree, gear mods

### Resistance Reduction (Curses, etc.)
- Actually CHANGES the enemy's resistance value
- Affects both hits AND DoT
- Hex curses: Conductivity, Flammability, Frostbite — reduce respective resistances
- **Since 3.20, curse boss penalties are REMOVED** — curses now apply at full effect against all enemies
- However, non-curse application methods (Blasphemy, Hextouch, etc.) apply 25% less curse effect
- Self-casting hexes gives full value

### Exposure
- -10% to -25% resistance depending on source
- Only ONE exposure per element can apply (strongest wins)
- Sources: Wave of Conviction (element that deals most damage), Hydrosphere, Frost Bomb,
  Mastermind of Discord (Elementalist, -25%), various masteries
- Stacks with curses and penetration — they're separate systems

### How They Stack (Example)
Enemy with 40% fire resistance:
- Flammability curse: -30% → 10% fire res
- Fire Exposure: -15% → -5% fire res (enemy now NEGATIVE)
- 37% fire penetration on hit → treated as -42% fire res for the hit
- Result: the hit acts as if enemy has -42% resistance → enemy takes 142% of base fire damage

---

## Enemy Resistance Values (For Planning)

| Enemy Type | Elemental Res | Chaos Res | Notes |
|-----------|--------------|-----------|-------|
| Normal monsters | 0% | 0% | Trivial |
| Magic/Rare monsters | 0-30% | 0-20% | Varies by mods |
| Map bosses | ~40% | ~25% | Innate boss resistances |
| Pinnacle bosses | ~40-50% | ~30% | Shaper, Elder, Sirus, etc. |
| Uber pinnacle bosses | ~50%+ | ~30%+ | Higher tier, higher resists |

**Note**: Exact values vary by boss. Always verify specific boss resistances via poedb.tw if planning
a bossing build. These are approximations for planning purposes.

---

## Damage Effectiveness of Added Damage

Every damage-dealing skill gem displays a "damage effectiveness" percentage:

### For Attacks
- ALL base + added flat damage is combined first
- Then multiplied by the skill's attack damage percentage (shown as "deals X% of base attack damage")
- Example: 200% base attack damage with 100 flat from weapon + 50 flat from ring = 150 × 2.0 = 300

### For Spells
- Added flat damage is multiplied by the gem's damage effectiveness FIRST
- Then added to the gem's base damage
- Example: 500 base spell damage + (50 flat added × 130% effectiveness) = 500 + 65 = 565
- Skills with high effectiveness (190%+ like Absolution) benefit enormously from flat added damage

---

## Accuracy (Attacks Only)

- Chance to hit formula: Attacker's Accuracy / (Attacker's Accuracy + (Defender's Evasion / 4)^0.8)
- Target: 100% chance to hit (every % below 100 is a direct % DPS loss)
- Solutions for imperfect accuracy: Resolute Technique (always hit, never crit), "hits can't be evaded" mods
- Crits have a SECOND accuracy check — if this confirmation roll misses, crit becomes a normal hit
- Spells always hit — no accuracy needed ever

---

## Lucky Damage

"Damage is Lucky" means the game rolls damage twice and takes the HIGHER roll.
- Most impactful for damage types with high variance (lightning damage has the widest ranges)
- Effectively increases average damage by a significant amount
- Sources: Diamond Flask (for crits), certain unique items
- "Hits against you are Unlucky" exists as a defensive version on some enemies

---

## Damage Taken As (Shifting)

"X% of Y damage taken as Z damage" on the RECEIVING side:
- The shifted portion is mitigated by the NEW damage type's resistance/defense
- This is NOT conversion — the shifted damage does NOT retain its original properties
- Example: 50% of lightning damage taken as fire + 80% fire res = massive lightning defense
- Key items: Dawnbreaker, Taste of Hate, Lightning Coil, Watcher's Eye mods
- Crucial for Doryani's Prototype builds — shifting lightning damage to fire/cold/chaos for mitigation

---

## Practical Decision Framework

When evaluating damage upgrades, ask:
1. **What's my weakest multiplier?** If you have 500% increased but only 2 "more" mods, add a "more" source
2. **Am I scaling the right damage type?** Check gem tags — only matching modifiers apply
3. **Is my base damage high enough?** Flat added damage is huge when base is low and effectiveness is high
4. **Am I converting efficiently?** Conversion lets you benefit from two modifier pools simultaneously
5. **Is penetration/reduction worth it?** Against high-res enemies, pen is effectively a "more" multiplier
6. **Am I at 100% hit chance?** For attacks — every % below 100 is a direct % DPS loss
7. **Am I diversifying correctly?** Flat damage → increased → more → pen → crit — spread investment across categories for maximum returns
8. **Is DoT multi available?** For DoT builds, DoT multi is often the most efficient scaling category because few builds stack it heavily
