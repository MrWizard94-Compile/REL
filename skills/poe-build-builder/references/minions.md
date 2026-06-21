# Minions — Complete Reference

## Minion Fundamentals

Minions are allied creatures summoned by the player. They are fully independent entities with
their OWN stats — life, damage, resistances, accuracy, attack/cast speed — separate from yours.

### Core Principles
- **Gem level is king** — minion base damage and life scale primarily with the level of the minion skill gem
- **Your damage mods DON'T apply to minions** — "increased fire damage" on YOUR gear does nothing for your minions
- **Minion-specific mods DO apply** — "minions deal X% increased damage" is the correct stat to look for
- **Support gems linked to the minion skill** affect the minions directly (they inherit applicable supports)
- **Minions benefit from your auras** — Wrath, Anger, Hatred, Determination, etc. apply to minions within range
- **Minions do NOT benefit from your flasks** (rare exceptions: Mother's Embrace, Umbilicus Immortalis)
- **Minions CAN gain charges** (unlike totems) — through Necromantic Aegis + Victario's Charity, marks, etc.
- **Your IIQ/IIR applies** when minions get kills — minion kills use YOUR item find stats

### Spiritual Aid (IMPORTANT — Commonly Misunderstood)
- **What it does**: "Increases and Reductions to Minion Damage also affect YOU"
- This means: minion damage mods on tree/gear ALSO boost YOUR personal damage
- This does NOT make your personal damage mods apply to minions
- **Only works with "increased/reduced"** — NOT "more/less" multipliers
- Does NOT work with Minion Damage SUPPORT gem (that's a "more" multiplier on the support, not a global increased stat)
- Useful for hybrid builds where you AND your minions deal damage (e.g., Absolution, Dom Blow)

### Spiritual Command (Companion Notable)
- "Increases and Reductions to Minion Attack Speed also affect you"
- Same principle as Spiritual Aid but for attack speed

---

## How Minion Damage Actually Works

### The Minion Damage Calculation
```
Minion Hit DPS =
  Minion Base Damage (from monster template, scaled by gem level)
  + Flat Added Damage (from auras, Ghastly jewels, support gems)
  × (1 + sum of all applicable "increased" minion damage modifiers)
  × product of all "more" multipliers (from support gems, ascendancy, etc.)
  × Minion Hit Rate (attack/cast speed)
  × Crit Factor (if minion crits)
  × Enemy Resistance/Mitigation
```

### Key Differences from Player Damage
- Minion base damage comes from the **monster template** of the minion type, scaled by gem level
- Minions have their own accuracy (for attack-based minions) — can miss
- "Increased damage" on the passive tree only affects minions if it says "minion" or is generic damage WITH Spiritual Aid
- Support gems like Minion Damage Support provide "more" damage — the single biggest scaling lever after gem levels
- Flat added damage from auras and Ghastly Eye Jewels is added BEFORE multipliers — very powerful when minion base damage is low

### Minion Crit
- Minions CAN crit
- Minion crit is based on the minion's own base crit chance (from monster template)
- Default crit multi for minions: 130% (lower than player's 150%)
- "Minions have X% increased crit chance" and "minions have +X% to crit multiplier" scale this
- Minions crit DoT multi for ailments from crits: +30% (lower than player's +50%)
- **Controlled Destruction** on a minion link reduces the minion's crit chance, not yours
- **Fresh Meat Support**: Grants temporary massive crit chance + crit multi to newly summoned minions

---

## Minion Defenses & Resistances

### Base Resistances
Most minions start with:
- **40% all elemental resistances** (base)
- **20% chaos resistance** (base)

Exceptions:
- **Spectres**: +30% all elemental res from the gem → 70% base ele res (nearly capped)
- **Golems**: 70% for their respective element, 40% for others
- Animate Guardian: 40% ele / 20% chaos (like standard minions)

### Resistance Cap
- Minion resistance cap is **75%** (same as players)
- Minions do NOT suffer campaign resistance penalties
- To cap minions: need ~35% additional from tree/gear/ascendancy for most types
- Necromancer's ascendancy often provides +20% all res to minions
- Passive tree has "minions have +X% to all elemental resistances" nodes

### Minion Life
- Scales heavily with gem level (primary source)
- "+X% increased minion life" from tree, gear, and supports
- Minion Life Support: "more" minion life
- Animate Guardian has an enormous innate life pool
- Zombies have high base life (good meat shields); SRS have low base life (fragile)

### Minion Survivability Solutions
When minions die in hard content:
1. **Bone Offering**: Block chance for minions (and you with Mistress of Sacrifice)
2. **Meat Shield Support**: Defensive behavior + taunt + less damage taken for minions
3. **Minion Life Support**: Raw more life
4. **+Minion life on tree/gear**: Scales the base
5. **Convocation**: Emergency teleport to your position + life regen burst
6. **Elemental Army Support**: -10% exposure on enemies + less ele damage taken for minions
7. **Cap minion resistances**: Uncapped res = minions getting obliterated by ele damage
8. **Stone Golem**: Provides life regen to ALL nearby minions
9. **Feeding Frenzy buff**: Minions recover life on hit when you have the Feeding Frenzy buff
10. **For Animate Guardian specifically**: Invest in life regen on equipped items, keep it linked to Minion Life + Meat Shield. Losing AG gear is painful and expensive.

---

## Minion Scaling Levers (Priority Order)

### 1. Gem Level (+levels) — HIGHEST PRIORITY
- Each gem level increases minion base damage AND life significantly (often 10-15% per level)
- Sources of +gem levels:
  - Helmet: "+X to level of socketed minion gems" (enchant, influenced mod)
  - Weapon: "+X to level of all minion skill gems" (wand/sceptre craft or mod)
  - Amulet: "+X to level of all skill gems" or "+X to level of all intelligence skill gems"
  - Empower Support: Adds levels to linked active gems (+3 at level 4)
- A level 25+ minion gem is often 50-80% stronger than level 20
- This is the FIRST thing to invest in for any minion build

### 2. Support Gems (More Multipliers)
Each support is a separate "more" multiplier for your minions:

**Damage supports:**
- Minion Damage Support: Generic more damage for all minion types
- Melee Physical Damage: For melee minions (zombies, skeletons, AG)
- Elemental Damage with Attacks: For minions dealing elemental attack damage
- Spell Echo: For caster minions (spectres, Absolution sentinels) — repeats casts
- Multistrike: For melee minions — repeats attacks
- Predator: More damage + command minion to target specific enemy
- Concentrated Effect: More area damage (bossing swap)
- Vicious Projectiles: For projectile minions (certain spectres)
- Feeding Frenzy: Aggressive behavior + "Feeding Frenzy" buff grants more damage to ALL minions

**Behavior/Utility supports:**
- Feeding Frenzy: Makes supported minions AGGRESSIVE (wider aggro, pursue enemies)
- Meat Shield: Makes supported minions DEFENSIVE (stay close, taunt, less damage taken)
- Minion Speed: Movement + attack/cast speed (QoL and DPS)

**Note:** If a support says "Cannot modify the skills of minions" — it won't work on minion skills. Always check. Spell Cascade, for example, can't modify minion skills.

### 3. Auras (Hidden Multipliers)
Your auras affect minions in range — these are essentially free damage for minions:

**Offensive:**
- **Hatred**: ~36% of phys as extra cold damage → huge for physical minions
- **Wrath**: Flat lightning to attacks/spells → good for all minion types
- **Anger**: Flat fire to attacks/spells
- **Pride**: Nearby enemies take more physical damage (ramps up) — affects minion damage indirectly
- **Zealotry**: More spell damage + crit for caster minions

**Defensive:**
- **Determination**: Flat + more armour for minions → keeps them alive
- **Discipline**: Flat ES for ES-based minions
- **Vitality**: % life regen for minions

**Key interaction: Generosity Support**
- Aura no longer affects YOU, but has INCREASED EFFECT on allies (minions)
- Extremely efficient for pure summoner builds where the aura is only for minions
- Cannot be used with auras you need for yourself (Determination for your own defense, etc.)

### 4. Passive Tree
- Minion damage clusters: Lord of the Dead (Witch area), Sacrifice wheel, Gravepact, etc.
- +Maximum minion count nodes: More minions = more total DPS
- Minion life/resistances: Survivability investment
- **Key Masteries:**
  - "Minions penetrate 8% of cursed enemies' elemental resistances" — excellent DPS
  - "20% increased effect of Offerings" — boosts Bone/Flesh/Spirit Offering
  - "Minions have 30% increased Area of Effect" — clear speed
  - "Convocation has 40% increased Cooldown Recovery Rate" — repositioning QoL
  - "Minions Regenerate 1% of Life per second" — baseline sustain

### 5. Offerings
- **Bone Offering**: Block chance for minions (+ you with Mistress of Sacrifice). Key defensive layer.
- **Flesh Offering**: Attack/cast/movement speed for minions. DPS + clear speed.
- **Spirit Offering**: Grants ES based on minion life + extra chaos damage. Niche.
- Only ONE offering active at a time
- **Automate with trigger craft**: "Trigger a socketed spell when you use a skill" on weapon → auto-casts offering
- **Necromancer's Mistress of Sacrifice**: Offerings ALSO affect you. Bone Offering → you get block too.

---

## Minion Types

### Raise Zombie
- **Role**: Meat shield, aggro dilution, ailment application, moderate DPS
- Melee minions with decent life pools
- Maximum count: 3-6 base (scales with gem level), more from gear/tree
- **Persistent** — survive between zones and game sessions
- Great for: front-line tanking, applying bleeds/shocks/ignites via linked supports
- Support example: Melee Phys + Chance to Bleed + Elemental Proliferation → multi-ailment debuff engine
- Can also run pure DPS: Melee Phys + Multistrike + Minion Damage + Elemental Damage with Attacks

### Summon Skeletons
- **Role**: Expendable DPS army, strong single-target
- Summoned at target location, 20 second duration
- Maximum count: 5-7 base, up to 15+ with heavy investment
- Die easily but are instantly resummoned — designed to be disposable
- **Vaal Summon Skeletons**: Summons massive army for burst DPS phase
- Good single-target but slow clear without investment
- Skeleton Mages (from Dead Reckoning jewel): Ranged elemental casters, much better clear

### Raise Spectre
- **Role**: Highly customizable — depends entirely on which monster you raise
- Raises a COPY of a specific defeated monster type as your permanent minion
- Maximum count: 1-2 base (more with gem level and gear)
- Spectre level equals gem level (capped)
- **Persists between zones and sessions** (regular version) — log out and log back in, spectres remain
- **Spectre choice is everything**: Different monsters have completely different skills
- Popular spectres (verify current meta): Solar Guards (fire projectiles), Slave Drivers (lightning), Redemption Sentries (ranged physical/cold), various newer options
- **Raise Spectre of Transience**: Temporary duration version — more spectres + higher crit, but they don't persist
- Support gem selection must match the spectre's attack type (spell vs attack, melee vs ranged)

### Absolution
- **Role**: Hybrid caster/summoner — you deal damage AND summon minions
- You cast a lightning spell that debuffs enemies. Kills/rare hits summon Sentinels of Absolution.
- Sentinels cast their OWN copy of Absolution
- Maximum 3 Sentinels
- 50% physical to lightning conversion built-in (for both your cast and sentinel casts)
- Support gems affect BOTH your cast AND sentinel casts (if the support is compatible with both)
- Sentinel damage scales with gem level like all minions
- **Key mechanic**: Absolution quality grants "Increases and Reductions to Minion Damage also apply to this Skill's Damage at X% of their value" — built-in Spiritual Aid effect
- Primary ascendancies: Guardian (auras, defense, Unwavering Crusade) and Necromancer (offerings, +levels)

### Summon Raging Spirit (SRS)
- **Role**: Aggressive short-duration fire DPS
- Flying skulls that aggressively seek and attack enemies
- Maximum count: 20
- Short duration — need continuous casting to maintain the army
- Fire damage focused
- Scales well with cast speed (more casts per second = more skulls active)
- Good clear, needs investment for boss single-target
- SRS of Enormity (transfigured): Fewer, larger, harder-hitting skulls — better for bossing

### Summon Holy Relic
- **Role**: Support minion that heals you and nearby allies
- Nova damage on your melee hits
- Primarily used for its heal (regen aura that triggers when you hit)
- Maximum 1 by default (2 with specific investment)
- Pairs well with melee/minion hybrid builds (Dominating Blow, etc.)
- Guardian ascendancy synergizes naturally

### Summon Reaper
- **Role**: Single powerful minion (anti-army design)
- Very high damage single minion
- CONSUMES your other minions to heal and buff itself
- Anti-synergy with army-style builds — designed for builds that only use the Reaper
- Powerful but niche and requires building entirely around it

### Animate Guardian
- **Role**: Support aura bot — equips real gear for party-wide buffs
- You feed it actual gear items — **items are CONSUMED and cannot be recovered**
- Gains the stats and effects of all equipped items
- **IF IT DIES, ALL ITEMS ARE LOST** — invest in keeping it alive
- Used as a walking aura/debuff platform:
  - **Garb of the Ephemeral**: Enemies cannot gain charges, cannot crit; guardian cannot be slowed
  - **Leer Cast** (helmet): Nearby allies deal 15% increased damage
  - **Dying Breath** (weapon): Nearby allies deal 18% increased damage, nearby enemies take 18% increased damage
  - **Kingmaker** (weapon): Nearby allies have Fortify, cull, and crit multi — EXTREMELY powerful but expensive
  - **Mask of the Tribunal**: Nearby allies get block/crit/cast speed based on your attributes
- **Safety tips**: Always link AG to Minion Life + Meat Shield. Keep it defensive. If you can't afford to lose the items, don't equip expensive ones. In dangerous content, consider unlinking AG entirely.

### Golems
- **Role**: Buff providers (primarily) or DPS (Golemancer builds)
- One active by default, more with gear/passives/ascendancy
- Each provides a different buff to YOU:
  - **Stone Golem**: Life regeneration (also for minions in range)
  - **Chaos Golem**: Physical damage reduction
  - **Lightning Golem**: Increased attack/cast speed
  - **Ice Golem**: Increased accuracy + crit chance
  - **Flame Golem**: Increased damage
  - **Carrion Golem**: Flat added damage per non-golem minion nearby
- For most builds: pick one golem for its buff, don't invest further
- **Golemancer (Elementalist)**: Dedicated ascendancy nodes scale golem damage AND buff effect. Run 6-9 golems as primary DPS.

### Herald of Purity
- **Role**: Hybrid herald — flat damage buff + summons Sentinels of Purity
- Reserves 25% mana
- Summons Sentinels on kill or hit against rare/unique (maximum 4)
- Adds physical damage to your attacks and spells (Herald buff)
- Pairs naturally with Dominating Blow for massive combined armies
- Sentinels are temporary but refresh on kills

### Dominating Blow
- **Role**: Melee attack that creates a minion army from kills
- Killed normal/magic enemies become Sentinels of Dominance
- Killed rare/unique enemies also become dominated minions
- Maximum counts vary by enemy type
- Needs to be constantly killing to maintain the army — scales poorly on bosses without adds
- Pairs with Herald of Purity for larger combined army
- Guardian ascendancy is the natural home for this skill

---

## Minion AI & Behavior

### Default Behavior
- Minions follow you and attack enemies within a moderate aggro radius
- They prioritize targets you've recently attacked (soft targeting)
- Minions will NOT pursue enemies that run away unless aggressive

### Behavior-Modifying Supports
- **Feeding Frenzy**: Minions become AGGRESSIVE — wider aggro range, pursue enemies, attack proactively. Also grants "Feeding Frenzy" buff to you when minions hit, giving ALL your minions more damage.
- **Meat Shield**: Minions become DEFENSIVE — stay close to you, taunt nearby enemies, take less damage. Anti-synergy with aggression.
- **Predator**: Allows you to COMMAND a minion to attack a specific target. Target takes more damage from minion hits. Great for bossing.
- If both Feeding Frenzy and Meat Shield are linked (different minion groups), they cancel out — the affected minions return to default behavior but still get the stat bonuses.

### Convocation
- Instantly teleports ALL minions to your position
- Grants life regeneration to minions for a short duration
- **Critical for boss fights** — repositions your army when the boss moves
- Has a cooldown (reducible with mastery)
- Should be on your skill bar for every minion build

### Minion Targeting Tips
- Attack an enemy yourself to direct minion aggro (even a low-damage hit works)
- Use Predator support for precise boss targeting
- Flame Dash or movement skill near enemy packs to pull minions into aggro range
- Convocation to regroup scattered minions before a boss phase

---

## Necromantic Aegis (Keystone)

- **All modifiers on your equipped shield** are removed from YOU and applied to your MINIONS instead
- You lose: block chance, armour, ES, resistances, all explicit mods from the shield
- You KEEP: ability to use skills socketed in the shield, passive tree bonuses for "while holding a shield"
- You still suffer the shield's movement speed penalty

### Why Use It
- Equip a shield with powerful mods and give them ALL to your minions:
  - **Victario's Charity**: Minions generate their own frenzy and power charges (charges they normally can't generate)
  - **Aegis Aurora**: ES on block for minions (if they have block from other sources)
- Major trade-off: YOU lose all shield defenses. Build must compensate.

---

## Minion Damage Types & Ailments

Minions apply ailments just like players — this is a core part of many minion strategies:

### Enabling Minion Ailments
- **Ghastly Eye Jewels** (Abyss Jewels): "Minions deal X to Y additional [element] damage" — adds flat elemental to ALL minion hits, enabling shock/ignite/chill
- **Auras**: Wrath/Anger/Hatred add flat elemental damage to minion attacks
- **Chance to Bleed + Elemental Proliferation** on zombies: Creates a multi-ailment debuff engine where zombies apply bleed, shock, and ignite simultaneously, with prolif spreading them
- **Ghastly jewel ailment mods**: "Minions have X% chance to taunt/hinder/blind on hit"

### The Zombie Ailment Engine (Rob's Build Pattern)
This is a proven strategy from your Absolution Guardian build:
- Zombies linked with: Melee Phys + Chance to Bleed + Elemental Proliferation
- Ghastly Eye Jewel with: flat lightning, flat fire, flat chaos to minion damage
- Result: Zombies wade into packs, apply bleed + shock + ignite + hinder + chaos damage
- Elemental Proliferation spreads shocks and ignites to the entire pack
- By the time Absolution sentinels engage, the pack is pre-debuffed and half-dead

---

## Key Unique Items for Minions

### Weapons
- **Doryani's Catalyst**: Ele Prolif for socketed gems + 80-100% ele damage + 0.2% ele leech (sceptre)
- **Dying Breath**: Nearby allies/enemies damage increase (cheap AG weapon)
- **Kingmaker**: Fortify + crit multi + culling strike for nearby allies (expensive AG weapon)
- **Midnight Bargain**: +1 to max zombies, skeletons, spectres — reserves 30% life (wand)
- **Convoking Wand** (rare): Best in slot for minion builds — can roll +levels, minion damage, trigger craft

### Armour
- **Garb of the Ephemeral**: AG body armour — enemies can't gain charges or crit, guardian immune to slow
- **Fleshcrafter**: Minion chaos res converts life to ES — ignores enemy ele res when minion has enough chaos res (powerful but dangerous)
- **Bones of Ullr**: +1 to max zombies and spectres (boots)

### Shields
- **Victario's Charity** (with Necromantic Aegis): Minions generate frenzy + power charges
- **Atziri's Mirror/Reflection**: Various defensive benefits for minions

### Helmets
- **The Baron**: Half your Str added to minions, +1 zombie per 500 Str, zombie leech (Str-stacking builds)
- **Mask of the Tribunal**: Nearby allies gain block/crit/cast speed based on YOUR attributes (AG helmet)

### Jewels
- **Ghastly Eye Jewels**: THE most important jewel type for minion builds. Flat damage, movement speed, chance to taunt/hinder on hit.
- **Dead Reckoning**: Transforms Summon Skeletons into Skeleton Mages (ranged elemental casters)
- **To Dust**: Skeleton duration and speed (skeleton builds)

---

## Trigger Weapon for Automation

A crafted "trigger a socketed spell when you use a skill" mod on a weapon automates utility:
- Socket: Desecrate (creates corpses) + Offering (Bone/Flesh/Spirit) + Curse
- Result: Every time you use a skill, it automatically casts these in sequence
- Frees up keybinds and ensures 100% uptime on offerings and curses
- Available via crafting bench (veiled mod, then bench craft)
- One of the most important quality-of-life setups for any summoner build

---

## Build Archetypes: Army vs Elite

### Army Builds (Many Minions)
- Maximize minion COUNT: zombies + skeletons + spectres + HoP sentinels
- Each minion does moderate damage, but 15-20+ minions together = enormous combined DPS
- Massive aggro dilution — enemies target your army, not you
- Clear speed: minions spread across the screen, covering everything
- Weakness: socket-starved, complex to manage, each individual minion is weak
- Examples: Absolution Guardian army, Dominating Blow, skeleton army

### Elite Builds (Few Powerful Minions)
- Maximize individual minion POWER: +gem levels, strong supports, auras
- 3-5 minions each dealing very high damage
- Easier to manage, less socket pressure
- Weakness: less aggro dilution, single-target focused
- Examples: Spectre builds (2-3 spectres), Golemancer, Reaper

### Hybrid Builds
- You deal damage alongside your minions (not just supporting them)
- Spiritual Aid makes minion damage mods also scale your damage
- Absolution is the prime example — your cast + sentinels' casts
- Requires balancing investment between personal damage and minion power

---

## Practical Decision Framework

1. **Choose your primary minion type** — don't spread too thin unless doing army strategy intentionally
2. **Gem level is priority #1** — get +levels on helmet, weapon, amulet. Empower 4 is endgame.
3. **Support gem selection must match minion behavior** — melee vs spell, attack vs cast supports
4. **Auras are your hidden multipliers** — Hatred/Wrath/Anger are massive for minion DPS. Consider Generosity.
5. **Get a trigger weapon** — automate offerings, desecrate, and curses. Massive QoL.
6. **Minion survivability matters in red maps+** — cap resistances, use Bone Offering, invest before it becomes a problem
7. **AI behavior controls matter** — Feeding Frenzy for clear, Predator for bossing. Keep Convocation handy.
8. **Ghastly Eye Jewels are mandatory** — flat damage, ailment chance, movement speed for minions
9. **Don't neglect YOUR defenses** — your minions can't protect you from everything. Cap your own res, get a guard skill.
10. **Animate Guardian is high risk/reward** — don't equip items you can't afford to lose until the AG is tanky enough to survive
