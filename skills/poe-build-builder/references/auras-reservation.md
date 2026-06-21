# Auras, Curses & Reservation — Complete Reference

## Aura Fundamentals

Auras reserve a percentage of your mana (or life with Arrogance Support / Blood Magic) to
provide continuous buffs to you and nearby allies (including minions).

### Core Principles
- Auras are TOGGLED on — they persist until deactivated, mana/life is depleted, or you die
- Multiple auras can run simultaneously if you have enough unreserved resource
- Auras affect minions within their radius — core scaling lever for summoners
- No limit on number of active auras (only limited by reservation budget)
- Cannot have two copies of the same aura active on yourself
- If affected by multiple sources of the same aura, only the strongest applies
- Spell damage mods do NOT affect aura buffs — auras grant buffs, not spell damage
- Aura effects update every 250ms (server tick) — not instant when enemies enter range
- Skill tooltips do NOT reflect aura effect modifiers — shows base values only

### Aura Effect Scaling
Two key stats for increasing aura power:
- "% increased Effect of Non-Curse Auras from your Skills" — affects buff for you AND allies/minions
- "Auras from your Skills have % increased Effect on you" — only affects YOU, not allies
- These stack multiplicatively with each other
- Sources: passive tree, gear, Ichimonji sword, Champion ascendancy, some uniques
- Generosity Support: aura does not affect you, but has ~50% more effect on allies (minions love this)

---

## Mana Reservation

### How Reservation Works
- Percentage-based auras reserve a % of your maximum mana (50%, 35%, 25%)
- Flat-based skills reserve a flat amount of mana (Precision, Vitality, Clarity — scales with gem level)
- Reserved mana is UNAVAILABLE for spending but mana regen rate is unaffected
- You need some unreserved mana left to cast skills (unless using Eldritch Battery, Lifetap, or Blood Magic)

### Mana Reservation Efficiency
The primary stat for fitting more auras:
```
Actual Reservation = Base Reservation / (1 + sum of all efficiency modifiers)
```
Example: 50% base with 100% increased efficiency = 50% / 2.0 = 25% reserved

Sources of reservation efficiency:
- Passive tree: Sovereignty cluster (~30%), Influence cluster, Champion of the Cause, various masteries
- Enlighten Support (levels 2-4): Reduces reservation of ALL linked skills. Level 4 is a massive endgame investment.
- Gear: specific helmet enchants, influenced mods, unique items
- Anointing: some notable anointments grant efficiency
- Specific skill efficiency: "% increased Mana Reservation Efficiency of [specific aura] Skills"

### Reserving Life Instead of Mana
- Arrogance Support: Supported skills reserve LIFE instead of mana. Also grants increased aura effect (10-19%). Higher mana multiplier means the life cost is more than the mana equivalent.
- Blood Magic keystone: ALL skills cost life, ALL auras reserve life. Extreme — disables mana entirely.
- Used in Low Life builds: reserve ~50% of life with auras via Arrogance to trigger Low Life threshold (Pain Attunement for 30% more spell damage)

### Divine Blessing / Guardian's Blessing Support
- Divine Blessing Support: Converts an aura into a temporary buff that costs mana to cast instead of reserving. Duration-based, not permanent. Good for builds that cannot afford permanent reservation but want an aura during boss fights.
- Guardian's Blessing Support: Similar concept. Restricted to specific use cases.

---

## Offensive Auras

### Hatred (Cold) — 50% Reservation
- Grants allies ~36% of physical damage as extra cold damage (at gem level 20)
- Also adds flat cold damage to attacks
- Excellent for physical attack builds wanting cold conversion/extra damage
- Works on minions — their physical attacks gain extra cold
- One of the strongest offensive auras for physical builds

### Wrath (Lightning) — 50% Reservation
- Adds flat lightning damage to attacks AND spells
- Grants "% more lightning damage" to spells
- Great for lightning-based builds, minion builds (flat damage applies to minion attacks)
- Wide applicability — affects both attacks and spells

### Anger (Fire) — 50% Reservation
- Adds flat fire damage to attacks AND spells
- Good for fire builds and minion builds
- Less universally powerful than Hatred/Wrath but strong when fire is your primary type

### Zealotry (Spell Crit) — 50% Reservation
- Grants % more spell damage and increased spell critical strike chance
- Creates Consecrated Ground near enemies you hit (rare/unique) — grants life regen + damage bonuses to those standing on it
- Core aura for spell-based crit builds
- Does NOT affect attacks or minion attacks

### Pride (Physical, Enemy Debuff) — 50% Reservation
- Nearby enemies take increased physical damage (ramps from ~19% to ~39% over 4 seconds)
- Unique mechanic: affects ENEMIES, not you — it is a debuff aura
- Works with minion physical damage — enemies near you take more from everything physical
- Effectively a "more" multiplier for physical builds
- Cannot be enhanced by Generosity (it does not buff allies)

### Malevolence (DoT) — 50% Reservation
- Grants % more damage over time and increased skill effect duration
- Core for ALL DoT builds: poison, bleed, ignite, chaos DoT (Bane, ED, Blight)
- The "more DoT" is a direct multiplier — very powerful
- Duration increase helps with ailment and debuff uptime

### Haste (Speed) — 50% Reservation
- Grants increased attack speed, cast speed, and movement speed
- Pure speed aura — no damage type restriction
- Good for builds that scale heavily with speed (Cyclone, CoC builds)
- Vaal Haste: temporary massive speed boost (great for burst phases)

### Precision (Accuracy/Crit) — Flat Reservation (scales with gem level)
- Grants flat accuracy and % increased critical strike chance
- Flat reservation = very cheap at low levels. Often kept at level 1 for minimal cost (~22 mana).
- Also activates Watcher's Eye mods tied to Precision (common endgame strategy)
- Attack builds that need accuracy and/or crit can run this cheaply

---

## Defensive Auras

### Determination (Armour) — 50% Reservation
- Grants flat armour AND "% more armour" to you and allies
- THE single most impactful defensive aura for armour-based builds
- The "more" armour multiplier makes this scale incredibly well with other armour sources
- Essentially mandatory for any build using armour as primary defense
- Affects minions too — keeps them alive in hard content

### Grace (Evasion) — 50% Reservation
- Grants flat evasion AND "% more evasion" to you and allies
- Core for evasion-based builds (Ranger, Shadow, Trickster, Raider)
- Same multiplicative scaling as Determination but for evasion
- Pairs with Spell Suppression for a complete defensive package

### Discipline (Energy Shield) — 35% Reservation
- Grants flat energy shield AND faster start of energy shield recharge
- Essential for any ES-based build (Occultist, CI, Low Life)
- The faster recharge start is often more valuable than the flat ES
- 35% reservation = easier to fit than 50% auras

### Purity of Elements — 35% Reservation
- Grants all elemental resistances to you and allies
- Grants AILMENT IMMUNITY (cannot be chilled, frozen, shocked, ignited, scorched, etc.)
- Incredible quality of life — solves all elemental ailment concerns in one gem
- The resistance bonus helps with gearing flexibility
- Commonly used as a defensive crutch while gearing, or permanently for ailment immunity

### Purity of Fire / Cold / Lightning — 35% Reservation Each
- Grants resistance to the specific element + increased MAXIMUM resistance for that element
- Each 1% max res above 75% is extremely powerful (see defenses.md)
- Used in builds that stack max resistance for specific damage type defense
- Watcher's Eye mods tied to these purities can add "X% of [element] damage taken as [other element]" — core for Doryani's Prototype and other damage-shifting builds

### Tempest Shield — 25% Reservation
- Grants % chance to block spell damage + shock immunity
- Essentially free spell block for shield builds
- The shock immunity alone is worth the reservation for many builds

### Arctic Armour — 25% Reservation
- While stationary: take less fire and physical damage from hits
- While moving: no damage reduction effect
- Niche but strong for builds that stand still to cast/channel
- Also leaves chilled ground behind you while moving (minor utility)

### Flesh and Stone — 35% Reservation (Stance)
- Sand Stance: Nearby enemies are blinded. You take less damage from far enemies.
- Blood Stance: Nearby enemies are maimed (slowed). You deal more melee damage to nearby enemies.
- Can swap stances freely during gameplay
- Sand Stance blind is a powerful defensive layer

### Vitality — Flat Reservation (scales with gem level)
- Flat life regeneration per second for you and allies
- Good for minion builds (minions benefit from it) and RF builds
- Often used at low level purely to activate Watcher's Eye mods

### Clarity — Flat Reservation (scales with gem level)
- Flat mana regeneration per second for you and allies
- Often kept low-level for mana sustain without big reservation
- Watcher's Eye Clarity mods can be powerful (e.g., "damage taken from mana before life")

---

## Banners

Banners are a sub-group of aura skills with a unique mechanic:
- While ACTIVE (held), they provide a passive aura effect and gain Valour from melee combat
- When PLACED (used again), they consume all Valour and provide a stronger burst aura at the placed location for a duration
- More Valour = stronger placed effect + larger radius
- Only one banner can be active at a time

### War Banner — ~10% Reservation
- Active: nearby enemies take increased physical damage, you gain accuracy
- Placed: enemies in area take significantly more physical damage
- Great for physical melee/attack builds — very cheap reservation

### Dread Banner — ~10% Reservation
- Active: nearby enemies have less accuracy, you and allies have increased chance to impale
- Placed: stronger versions of both effects in the area
- Core for impale builds (Champion, melee physical)

### Defiance Banner — ~10% Reservation
- Active: you and allies gain armour and evasion, nearby enemies have reduced crit chance
- Placed: stronger version of all effects
- Extremely efficient — almost always worth running on any build. Cheap reservation, solid defense.

---

## Heralds

Heralds reserve 25% mana and provide two effects: a passive buff and a triggered effect.

### Herald of Ash
- Buff: Grants physical damage as extra fire damage (15-21%)
- Trigger: Killing an enemy causes nearby enemies to burn (overkill damage as DoT)
- Good for physical builds transitioning to fire

### Herald of Thunder
- Buff: Adds flat lightning damage to attacks and spells
- Trigger: When you KILL a shocked enemy (or SHOCK an enemy with Storm Secret ring), creates a lightning storm that hits nearby enemies
- Storm damage is SECONDARY — not affected by "spell damage"
- Storm CANNOT shock — it cannot self-sustain its own trigger
- Core for HoT autobomber builds

### Herald of Ice
- Buff: Adds flat cold damage to attacks and spells
- Trigger: Shattering a frozen enemy causes an ice explosion dealing cold damage to nearby enemies
- The explosion can chain-shatter packs — extremely satisfying clear speed

### Herald of Purity
- Buff: Adds flat physical damage to attacks and spells
- Trigger: Summons Sentinels of Purity on kill or hit against rare/unique enemies (max 4)
- Sentinels are actual minions — benefit from minion damage modifiers

### Herald of Agony
- Buff: Chance to poison
- Trigger: Summons Agony Crawler at max Virulence stacks — powerful projectile minion
- Crawler damage scales with Virulence stacks (gained by you poisoning enemies)

### Lone Messenger (Keystone from Calamitous Visions)
- You can only have ONE herald, but it has 100%+ more buff effect
- Disables ALL aura skills — no Determination, no Grace, nothing
- Used in herald-focused builds where the single massively buffed herald is the entire engine

---

## Summon Skitterbots — 35% Reservation

Not technically an aura, but functions like one:
- Summons a Chilling Skitterbot and a Shocking Skitterbot
- Skitterbots apply chill and shock to nearby enemies without dealing damage
- Base shock: 15% increased damage taken. Base chill: 10% reduced action speed.
- Scales with shock/chill effect modifiers
- Also grants 10% more trap and mine damage
- Fantastic utility — free shock and chill application with no investment

---

## Watcher's Eye Interaction

Watcher's Eye is one of the most powerful jewels in the game, directly tied to which auras you run.

### How It Works
- Unique Prismatic Jewel (limited to 1 socketed)
- Has 2-3 random aura-specific modifiers
- Each mod is conditional: "while affected by [Aura Name]" — only active when that aura is running
- 2-mod variant drops from Elder, 3-mod variant drops from Uber Elder

### Why It Matters for Aura Selection
- Some Watcher's Eye mods are build-defining:
  - "% of physical damage taken as [element] while affected by Purity of [Element]" — core for damage shifting builds (Doryani's Prototype)
  - "Damage penetrates X% resistance while affected by [offensive aura]"
  - "X% of damage leeched as life while affected by Vitality"
  - "Unaffected by [ailment] while affected by [aura]"
- Sometimes you run a cheap flat-reservation aura (Vitality, Clarity, Precision) primarily to activate a powerful Watcher's Eye mod
- When planning a build, check what Watcher's Eye mods exist for your aura combination — it can change aura selection entirely

---

## Curses — Hexes and Marks

Curses debuff enemies. Since 3.12, they are split into Hexes (AoE) and Marks (single-target).

### System Changes in 3.20 (CRITICAL — Outdated Info is Common)
- Boss curse penalties REMOVED — hexes now apply at full effect against ALL monsters
- Doom mechanic REMOVED — hexes no longer gain Doom over time
- Automated curse application now has penalties to keep self-cast competitive:
  - Blasphemy Support: 25% less effect of supported curses
  - Hextouch Support: 35% less effect of supported curses
  - Bane: 25% less effect of applied curses
  - Curse-on-hit item mods: No longer apply with increased effect
- Self-cast hexes have NO penalty — full effect. This is the intended trade-off.

### Hexes (AoE Curses)

Offensive:
- Flammability: Reduces fire resistance, increases chance to ignite
- Frostbite: Reduces cold resistance, increases chance to freeze
- Conductivity: Reduces lightning resistance, increases chance to shock
- Elemental Weakness: Reduces ALL elemental resistances (less per element than single-element curses)
- Despair: Reduces chaos resistance, adds chaos DoT, enemies take increased DoT
- Vulnerability: Enemies take increased physical damage, increased chance to bleed
- Punishment: Enemies grant buffs to you when hit; enemies take more damage on low life

Defensive:
- Temporal Chains: Enemies have reduced action speed. Other effects expire slower on cursed enemies (extends ailment durations!). Incredibly powerful for ailment builds.
- Enfeeble: Enemies deal less damage, have less accuracy, reduced crit chance/multi. Strong defensive hex.

### Marks (Single-Target Curses)

Marks have their own separate rules:
- Only ONE mark at a time on an enemy (separate from hex limit)
- Marks are NOT affected by hexproof
- Marks applied to an enemy can potentially jump to a new target on kill

Available Marks:
- Assassin's Mark: Increased crit chance and crit multi against marked target. Power charge on kill. Core for crit builds.
- Sniper's Mark: Splits projectiles on hitting marked enemy, increased damage taken. Projectile builds.
- Poacher's Mark: Life/mana on hit against marked target. Frenzy charge on kill. Flask charge on hit.
- Warlord's Mark: Life/mana leech against marked target. Endurance charge on kill.

### Curse Limit
- Default: 1 curse at a time on an enemy
- Hexes and Marks share the same limit by default
- Additional curse sources: Whispers of Doom (passive, +1), Windscream boots (+1), Doedre's Damning ring (+1), Occultist ascendancy (+1), some influenced gear
- Hexproof map mod: Enemies are immune to HEXES (but Marks still work!)

### Curse Application Methods (Ranked by Effectiveness)

| Method | Penalty | Notes |
|--------|---------|-------|
| Self-cast | None | Full effect. Slow, uses mana, active play |
| Arcanist Brand | None | Brand auto-casts. Good automation + full effect |
| Curse-on-Hit ring | None (lvl 1) | Automatic, convenient. Weaker curse level. |
| CWDT + curse | None (limited lvl) | Automatic via self-damage. Low gem level. |
| Hextouch Support | 35% less | Links curse to attack. Automatic on hit. |
| Blasphemy Support | 25% less | Turns curse into aura (reserves 35% mana). |
| Bane | 25% less | Applies linked curses + chaos DoT. |

---

## Exposure

Exposure reduces enemy resistance to a specific element. Separate from curses and penetration.

### Mechanics
- Reduces resistance by -10% to -25% depending on source
- Only ONE exposure per element can be active (strongest wins)
- Stacks with curses and penetration (all separate systems)
- Does NOT affect chaos resistance (only fire, cold, lightning)

### Sources
- Wave of Conviction: -15% exposure to element dealing most damage in the hit
- Hydrosphere: -10% cold and lightning exposure
- Frost Bomb: -15% cold exposure
- Fire/Cold/Lightning Exposure masteries on passive tree
- Mastermind of Discord (Elementalist): -25% exposure (strongest easily accessible source)
- Elemental Army Support: Minions apply -10% exposure on hit
- Corrosion mastery

### Doryani's Prototype Interaction
Prototype OVERRIDES enemy lightning resistance (equals YOUR lightning res). Exposure cannot further reduce it. However, lightning penetration DOES still work because penetration treats the resistance as lower without changing it.

---

## Typical Aura Setups by Archetype

### Physical Attack (Champion, Gladiator, Berserker)
Determination + Pride + Dread Banner + Precision (low level)
Optional: War Banner, Flesh and Stone (Blood Stance)

### Spell Caster (Elementalist, Inquisitor, Occultist)
Determination or Grace + Zealotry + Defiance Banner
Element-specific: Wrath (lightning), Anger (fire), or Hatred (phys conversion)
Optional: Precision (low level), Purity of Elements

### DoT Build (Trickster, Occultist, Pathfinder)
Determination or Grace + Malevolence + Defiance Banner
Optional: Purity of Elements, Vitality (regen + Watcher's Eye)

### Minion Build (Necromancer, Guardian)
Determination + offensive aura matching minion damage type (Hatred/Wrath/Anger)
Consider Generosity on offensive aura for increased effect on minions
Defiance Banner + Vitality or Precision for Watcher's Eye

### Aura Stacker (Scion, Guardian, Champion)
8-12+ auras via heavy reservation efficiency investment
Requires massive tree investment + Enlighten 4 + reservation gear
One of the most expensive but most powerful archetypes

---

## Practical Decision Framework

1. Pick 1-2 offensive auras matching your damage type
2. Always run at least 1 defensive aura — Determination or Grace
3. Defiance Banner is almost always worth it — tiny reservation, solid defense
4. Fit utility with remaining budget — Precision (low level), Vitality, Purity of Elements
5. Consider Watcher's Eye when choosing auras — a cheap aura might be worth running solely for its Watcher's Eye mod
6. Enlighten 4 is endgame investment — allows one more aura to fit
7. Curses are free damage — self-cast or Arcanist Brand gives full effect (no penalty since 3.20)
8. Blasphemy/Hextouch have 25-35% less curse effect — self-cast or brand application is stronger
9. Purity of Elements solves ailment immunity — one aura fixes freeze/shock/ignite
10. Check reservation math in PoB before committing
11. Generosity on offensive auras for minion builds — you lose buff but minions get ~50% more effect
12. For Low Life builds: Reserve life via Arrogance Support to trigger Pain Attunement
