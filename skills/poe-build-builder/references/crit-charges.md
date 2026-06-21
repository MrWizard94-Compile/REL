# Critical Strikes, Charges & Impale — Complete Reference

## Critical Strike System

### How Crits Work — The Roll
1. When you use a skill, the game generates ONE random crit roll (a number) for that entire use
2. That roll is compared against each target's effective crit chance — if your effective crit chance exceeds the roll, the hit against that target is a crit
3. In practice, since the roll is made once, all targets hit by the same skill use will almost always either all crit or all not crit (unless conditional modifiers like Assassin's Mark differ per target)
4. Crit damage = base hit damage × (critical strike multiplier / 100)
5. Default crit multi: 150% (crits deal 1.5× damage, i.e. 50% MORE damage than normal)

### Accuracy Confirmation Roll (Attacks Only)
- For ATTACKS (not spells), a successful crit requires a SECOND accuracy check
- If the second accuracy check fails, the crit is "downgraded" to a normal hit
- This means low-accuracy attack builds lose significant crit value
- Formula: Effective crit chance (attacks) = crit_chance × accuracy_chance
- Example: 50% crit chance with 85% accuracy = 50% × 85% = 42.5% effective crits
- Spells ALWAYS bypass this — spells cannot miss, so crit rolls are final
- Resolute Technique makes this moot (see below)

### Critical Strike Chance

#### Base Crit Chance
- Comes from the SKILL GEM (for spells) or WEAPON (for attacks)
- Typical ranges: 5-7% for most skills, some outliers at 8-9%
- This is the foundation — all scaling multiplies this value
- LOW base crit = hard to reach high effective crit even with heavy investment

#### Additional Base Crit Chance (Added to Base — VERY Powerful)
These sources add directly to the base before increased% modifiers apply:
- **Brittle** (alternative cold ailment): Up to +6% base crit (capped, was +15% pre-3.19). Scales with cold damage of the inflicting hit. Even +2-3% is enormous.
- **Assassin's Mark**: +1.5% base crit against marked target
- **Bottled Faith** (unique Sulphur Flask): +2% base crit against enemies on Consecrated Ground
- **Assassin ascendancy** (Deadly Infusion): +2% base crit while at max power charges
- **Increased Critical Strikes Support**: +1.5% base crit to supported skills
- Why this matters: Going from 6% base to 8% base is a 33% more multiplier to ALL your crit scaling. Base crit additions are the most efficient way to reach high crit.

#### Increased Critical Strike Chance
- All "% increased critical strike chance" sources are ADDITIVE with each other
- Formula: Effective crit = base_crit × (1 + sum_of_all_increased_crit%)
- Cap: 100% (cannot exceed)
- Example: 7% base × (1 + 500% increased) = 7% × 6.0 = 42% effective crit
- Sources: passive tree, gear, power charges, support gems, flasks
- Diminishing returns: adding 50% increased to an existing 500% pool is only ~8% relative gain

#### Local vs Global Crit Chance on Weapons
- "% increased Critical Strike Chance" on a WEAPON is LOCAL — it multiplies that weapon's base crit
- Example: Weapon with 7% base crit and "30% increased Critical Strike Chance" local = 7% × 1.30 = 9.1% base crit for calculations
- This happens BEFORE global increased crit is applied
- Spell crit is always from the gem, never from the weapon's base crit (even for wands)

### Critical Strike Multiplier
- Base: 150% (crits deal 50% more damage than non-crits)
- "+X% to Critical Strike Multiplier" adds to this base value
- Example: 150% base + 200% additional = 350% total (crits deal 3.5× normal)
- NO CAP on crit multi — you can stack it as high as your build allows
- Sources: passive tree, gear mods, support gems (Increased Critical Damage), Assassin's Mark (+30-49%), Assassin ascendancy
- Crit multi does NOT affect ailment damage (see Ailment Interaction section below)

### Effective DPS Formula with Crits
```
Crit DPS Multiplier = 1 + (effective_crit_chance × (crit_multi/100 - 1))
```
Example: 60% effective crit, 400% crit multi:
```
1 + (0.60 × (4.0 - 1)) = 1 + (0.60 × 3.0) = 1 + 1.8 = 2.8× base DPS
```
This means crits contribute 2.8× total DPS, or 180% MORE damage than no-crit.

Breakeven analysis: If you could get 40% more damage from another source instead of investing in crit, you need your crit multiplier to exceed:
```
crit_multi > 1 + (0.40 / effective_crit_chance)
```

### Diamond Flask (Changed in 3.15)
- **Current effect**: 100% increased Global Critical Strike Chance during flask effect
- **Old effect (pre-3.15)**: Made crit rolls "Lucky" (rolled twice, took better result). This was extremely powerful and is no longer how the flask works.
- The current 100% increased is still strong but is additive with all other increased crit sources
- At high existing increased crit (500%+), the Diamond Flask's relative contribution diminishes
- Still a good flask for crit builds that aren't already swimming in increased crit chance

### Lucky Crit Mechanic (Still Exists, Just Not on Diamond Flask)
- "Lucky" means the crit roll happens twice, and the better result is used
- Formula: Lucky crit chance = 1 - (1 - crit_chance)²  or equivalently  2×crit - crit²
- Most effective at 50% crit chance (jumps to 75%)
- At 70% crit → 91% lucky crit. At 30% crit → 51% lucky crit.
- Sources: some uniques, Assassin's "Ambush" node (lucky crits against full life enemies)
- "Unlucky" is the inverse — rolls twice, takes worse result

---

## Crit Keystones

### Elemental Overload (EO)
- When you crit, gain 40% more elemental damage for 8 seconds
- Your critical strikes deal NO extra damage (crit multi is ignored entirely)
- The 40% more is a massive free multiplier for minimal investment
- Ideal for: builds with some natural crit chance (5-15%) but no crit multi investment
- NOT ideal for: builds that invest heavily in crit multi (the 40% more pales compared to a good crit build's total crit DPS multiplier)
- **Decision threshold**: If your crit DPS multiplier (from formula above) would exceed 1.40, go full crit. If not, EO is better.
- Practical rule: If you can't reach 40%+ effective crit AND 300%+ crit multi, EO wins.
- Works with any hit that can crit — including totems, traps, and mines
- Refresh: Any crit refreshes the 8-second timer, so even low crit chance keeps it up reliably

### Resolute Technique (RT)
- Your hits can't be evaded (100% hit chance)
- You CANNOT deal critical strikes (ever)
- Eliminates the need for accuracy investment entirely
- Used by: Builds that want zero crit, zero accuracy, and invest everything into flat/more damage
- Common on: Melee attack builds (Earthquake, Slam builds), some minion builds for their own hits
- Incompatible with: Any crit scaling, Elemental Overload, any "on crit" effects
- Located in the Marauder area of the tree

### Perfect Agony
- 150% of your Critical Strike Multiplier applies to ailment Damage over Time Multiplier
- 30% less Damage with Hits
- Only useful for ailment builds that also crit
- How it works in practice:
  - The keystone causes "Modifiers to Critical Strike Multiplier also apply to Damage over Time Multiplier for Ailments from Critical Strikes, at 150% of their value"
  - If you have +250% crit multi (total 400%), the added DoT multi from Perfect Agony = 250% × 1.5 = +375% DoT multi for crit ailments
  - This is ADDITIVE with other DoT multi sources
  - The 30% less hit damage is a real cost — your hits deal much less, only ailments benefit
- Best for: Poison builds (Assassin), ignite builds that crit naturally
- Skip if: You don't have high crit multi, or if your ailments already have enough DoT multi from other sources

### Controlled Destruction Support
- Grants significant "more spell damage"
- But applies "X% reduced critical strike chance" to the supported skill
- The "reduced" is applied AFTER all increased crit — it's effectively a multiplier downward
- Good for EO builds: You still crit occasionally to trigger EO, but get big more damage
- Bad for crit builds: The reduced crit directly cuts your effective crit chance

---

## Ailment Interaction with Crits

### Guaranteed Ailments on Crit
- Critical strikes have 100% chance to inflict the associated elemental ailment:
  - Fire crit → guaranteed Ignite
  - Cold crit → guaranteed Chill/Freeze (if threshold met)
  - Lightning crit → guaranteed Shock (if threshold met)
- This is ONLY for application chance — ailment magnitude still depends on damage dealt

### Crit DoT Multiplier Bonus
- Damaging ailments (ignite, bleed, poison) from critical strikes gain **+50% to Damage over Time Multiplier**
- This is NOT a 150% multiplier on ailment damage — it's +50% added to your existing DoT multi pool
- Example: If you have +80% DoT multi from other sources and your ailment crits, total = 80% + 50% = 130% DoT multi
- This stacks ADDITIVELY with other sources of DoT multi
- Monsters and minions have an inherent +30% DoT multi for crit ailments (not +50%)
- Crit MULTIPLIER (the hit scaling stat) does NOT affect ailments by default — only Perfect Agony bridges this

### Implications for Ailment Builds
- Even if your hit damage doesn't matter, critting to apply the ailment is valuable for the +50% DoT multi
- This is why some ignite builds still take moderate crit investment
- EO + crit ailments work together: EO says crits deal no extra HIT damage, but the +50% DoT multi from crit ailments is a SEPARATE mechanic that DOES still apply. You crit (triggering EO's 40% more elemental) and the ailment from that crit gets +50% DoT multi. Both work simultaneously.

---

## Charge System

### Core Mechanics (All Charges)
- Charges are temporary stacking buffs, visualized as colored orbs around your character
- Default maximum: 3 of each type for all characters
- Default duration: **10 seconds** — refreshed whenever you gain a new charge of that type
- Gaining a charge at max stacks: no new charge, but duration of ALL charges of that type resets
- Charges are lost on death
- Duration can be extended by "% increased Charge Duration" modifiers
- Each charge type is associated with a core attribute
- Most skills are limited to granting 1 of each charge type per skill use

### Power Charges (Blue — Intelligence)
- **+40% increased critical strike chance** per charge (additive with other increased crit)
- Default max: 3 (total: +120% increased crit)
- Primary generation methods:
  - Assassin's Mark (on kill)
  - Power Charge on Critical Support (on crit, 5 second cooldown per enemy)
  - Orb of Storms (generates on crit within its area)
  - Assassin ascendancy (various sources)
  - Unique items: Void Battery (+1 max, large spell damage per charge), Romira's Banquet
- Key for crit builds — the increased crit chance helps reach higher effective crit
- Additional max from: passive tree (+1), Void Battery (+1 each, wields two = +2), some uniques

### Frenzy Charges (Green — Dexterity)
- **+4% increased attack speed** per charge
- **+4% increased cast speed** per charge
- **+4% more damage** per charge (THIS IS A MORE MULTIPLIER — extremely powerful)
- Default max: 3 (total: +12% more damage at 3 charges)
- The "more damage" is per-charge and multiplicative with everything else — best damage-per-charge of any charge type
- Primary generation methods:
  - Blood Rage (grants on kill, also gives attack speed and phys degen)
  - Frenzy skill (grants on hit — works on bosses!)
  - Poacher's Mark (on kill)
  - Raider ascendancy (generates during Onslaught, various)
  - Ice Bite Support (on kill against frozen enemies)
  - Farrul's Fur (automatic generation via Aspect of the Cat)
- Additional max from: passive tree (multiple +1 nodes in Ranger/Shadow area), Darkray Vectors, some uniques
- Stacking max frenzy charges is a legitimate build strategy — each additional charge is another 4% more

### Endurance Charges (Red — Strength)
- **+4% to all physical damage reduction** per charge
- **+4% to all elemental resistances** per charge
- Default max: 3 (total: +12% phys reduction, +12% all ele res)
- Primary generation methods:
  - Enduring Cry (warcry — generates on use, no kill required, works on bosses)
  - Juggernaut ascendancy (generates passively, cannot be reduced below max)
  - Warlord's Mark (on kill)
  - Endurance Charge on Melee Stun support
  - Some unique items
- Consumed by:
  - Immortal Call (consumes charges for extended duration)
  - Molten Shell benefits from armour, which endurance charges supplement indirectly
  - Discharge (consumes all charges for damage)
- The resistance bonus can free up gear affixes — especially useful during gearing

### Minimum Charges
- Some gear and passives grant "+X to Minimum [Type] Charges"
- You ALWAYS have at least this many charges — they never expire
- **Critical limitation**: Skills and effects that CONSUME charges CANNOT consume minimum charges
- Example: Immortal Call with +1 minimum endurance charges and 3 total endurance charges → IC can only consume 2
- If max charges is reduced to 0 but minimum is also 0: you are considered "at maximum charges" (0/0 = at max). Modifiers with "at maximum charges" are permanently active.
- However, 0/0 does NOT trigger "on reaching maximum charges" effects since you never transition from below-max to max
- Max charges takes priority over minimum charges (e.g., -2 max and +2 min = 1 charge)

### Alternative Charges (Maven Belts)
Three alternative charge types accessed via unique belts dropped from Maven fights:
- **Brutal Charges** (replaces Endurance): Different defensive bonuses
- **Affliction Charges** (replaces Frenzy): Different offensive bonuses
- **Absorption Charges** (replaces Power): Different utility bonuses
- These are niche and build-specific — the replacement is permanent while the belt is equipped
- All sources of the replaced charge type now generate the alternative instead

### Charge Generation for Bosses — Critical Concern
- Most on-kill charge generation DOES NOT WORK on bosses (no adds to kill in phases)
- This is one of the most common build-breaking oversights for new players
- Reliable boss charge generation:
  - **Frenzy skill** (grants on hit — always works)
  - **Enduring Cry** (generates without kills)
  - **Minimum charges** from gear (always active)
  - **Farrul's Fur** (automatic Frenzy + Power cycling)
  - **Assassin's Mark** (on hit quality bonus generates power charges)
  - **Raider ascendancy** (generates frenzy during Onslaught, which you can self-apply)
  - **Juggernaut** (endurance charges cannot be reduced below max — permanent)
- Rule: If your build needs charges for core DPS, verify you have a non-kill source

### Charge Duration and Management
- Base duration: 10 seconds for all three basic types
- Extended by: "% increased Charge Duration" (tree, gear, some support gems)
- Charge duration mods affect ALL charge types simultaneously
- Temporal Chains on enemies does NOT extend your charge duration (it affects enemy buffs/debuffs)
- Badge of the Brotherhood: Makes your max frenzy charges equal to your max power charges (or vice versa)
- Discharge: Consumes ALL charges of all types to deal massive damage — build-defining skill
- Totems can gain Endurance charges but NOT Frenzy or Power charges (their max is set to 0 for those)
- However, totems use YOUR stats — so your Frenzy/Power charges affect totem skills indirectly

---

## Impale — Physical Damage Stacking System

### How Impale Works
1. When a hit with "chance to impale" successfully impales an enemy, **10% of the hit's physical damage** is recorded (pre-mitigation — before the enemy's armour reduces it)
2. This creates an "Impale" debuff on the enemy
3. Each subsequent HIT against the impaled enemy triggers ALL active impale debuffs, dealing their recorded damage as reflected physical damage
4. Each impale debuff lasts for **5 hits** by default (or 8 seconds, whichever comes first)
5. A target can have MULTIPLE impale stacks simultaneously

### Damage Ramp-Up (Steady State)
Assuming 100% impale chance, the damage ramps up over successive hits:
```
Hit 1: 0% impale damage (first impale applied, nothing to trigger yet)
Hit 2: 10% (one impale active)
Hit 3: 20% (two impales active)
Hit 4: 30% (three impales active)
Hit 5: 40% (four impales active)
Hit 6+: 50% (five impales active — steady state with default 5-hit duration)
```
At steady state with 5 impale stacks: **+50% of your physical hit damage as extra reflected physical damage per hit**

With +2 max impales (Champion + tree): 7 stacks = **+70% at steady state**

### Impale Effect
- "% increased Impale Effect" increases the recorded damage per impale
- Base is 10% — with 50% increased impale effect, each impale records 15% instead
- Example: 7 impales with 79% increased effect: 70% × 1.79 = 125.3% extra damage at steady state
- Sources: Impale Support gem (up to ~59%), passive tree nodes, Champion ascendancy, Dread Banner (placed)

### Key Mechanical Details
- Impale damage is classified as **reflected damage** — NOT a hit from you
- It CANNOT: stun, apply on-hit effects, leech, trigger on-hit events
- It CAN be mitigated by: armour (applied when impale triggers, NOT when recorded), damage reduction, damage taken modifiers
- All impale debuffs on a target combine into a single reflected damage hit per trigger
- Impale cannot be evaded, blocked, dodged, or spell suppressed
- Only PHYSICAL damage from the initial hit is recorded — elemental/chaos damage in the same hit is ignored
- Conversion matters: If you convert physical to elemental BEFORE the hit, the converted portion does NOT get impaled

### Impale Support Gem
- 60% chance to impale on hit at gem level 20
- Up to +28% increased impale effect at gem level 20
- Quality adds more impale effect
- To reach 100% impale chance: combine Impale Support (60%) + Dread Banner active (~20%) + passive tree (~20%)
- 100% impale chance is strongly recommended for impale builds — missing impales breaks the stacking rhythm

### Champion and Impale
Champion is THE impale ascendancy:
- Master of Metal: +2 to maximum impale stacks (7 total), impale inherently on hits, flat phys added per impale on enemy
- Inspirational or First to Strike synergize with the overall physical framework
- Champion impale builds are among the highest sustained physical DPS archetypes in the game

### When Impale Matters
- Physical attack builds only — impale records physical damage exclusively
- Fast-hitting builds benefit most (reach steady state quickly)
- Slow hitters take longer to ramp but each impale records more damage
- Does NOT work with: spells (normally), DoTs, elemental/chaos damage
- Exception: Entropic Devastation gloves allow spell crits to impale (niche)

---

## Practical Decision Frameworks

### Crit vs Elemental Overload vs Resolute Technique

| Strategy | When to Use | Investment Required |
|----------|-------------|-------------------|
| Full Crit | 50%+ effective crit AND 300%+ crit multi achievable | Heavy — tree, gear, supports |
| Elemental Overload | Elemental build with some natural crit (5-15%) | Minimal — just need occasional crits |
| Resolute Technique | Non-crit attack build, no ele damage to speak of | None — saves accuracy AND crit investment |
| No keystone (low crit) | Build has neither crit scaling nor elemental damage | Default — just deal damage normally |

### Key decision points:
1. Calculate your crit DPS multiplier: `1 + (crit_chance × (multi/100 - 1))`
2. If it exceeds 1.40, crit beats EO
3. If you're an attack build with no crit and no elemental, RT saves massive investment
4. Brittle (+6% base crit) can push borderline builds firmly into crit territory
5. Diamond Flask's 100% increased crit chance helps but has diminishing returns at high existing increased%

### Charge Priority by Build Type
- **Attack builds**: Frenzy charges (4% more each) > Endurance charges (defense) > Power charges (only if crit)
- **Spell crit builds**: Power charges (crit chance) ≈ Frenzy charges (more damage) > Endurance charges
- **DoT builds**: Frenzy charges (4% more applies to DoT) > Endurance charges > Power charges (irrelevant unless crit)
- **Minion builds**: Frenzy charges if you can give them to minions (some mechanics) > your own charges for defense
- **Boss-focused**: Always verify non-kill charge generation exists

### Impale Checklist
1. Are you dealing physical attack damage? (If no → skip impale entirely)
2. Can you reach 100% impale chance? (If no → impale loses significant value)
3. Is Champion available as ascendancy? (If yes → impale is almost certainly worth it)
4. Are you converting most physical to elemental? (If yes → impale is weakened proportionally)
5. Is the build fast-hitting? (If yes → reaches steady state quickly, impale is great)
