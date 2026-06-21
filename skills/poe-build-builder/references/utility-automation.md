# Utility & Automation — Complete Reference

## Philosophy: Minimize Active Buttons

The best PoE builds reduce manual actions during mapping to 1-2 buttons: your main skill and a movement skill. Everything else should be automated via triggers, CWDT, brands, or flask enchantments. Reserve manual complexity for boss fights where precision matters.

---

## Movement Skills

Every build needs a movement skill. The right one depends on your weapon type and build.

### Flame Dash
- **Type**: Spell, Blink (teleport)
- **Requires**: Nothing — works with any weapon
- **Charges**: Stores up to 3 charges, recharges over time (~3 sec per charge)
- **Strengths**: Crosses gaps, passes through obstacles, works while weapon-swapping, no targeting required
- **Weaknesses**: Charge-limited (can't spam infinitely), brief animation
- **Best for**: Casters, minion builds, any build not using Shield Charge or Leap Slam
- **Link with**: Second Wind Support (extra stored charge + faster recharge), Arcane Surge (low level — triggers mana-based spell buff on use)
- **THE default movement skill** — if you don't know what to use, use Flame Dash

### Shield Charge
- **Type**: Attack, Movement
- **Requires**: Shield equipped
- **Speed**: Scales with attack speed AND movement speed (both matter)
- **Strengths**: No charge limit — spam freely. Scales with attack speed. Can stun/hit enemies in path.
- **Weaknesses**: Requires a shield. Can get stuck on terrain. Target-aimed (must click on ground).
- **Best for**: Shield-based melee or caster builds with good attack speed
- **Link with**: Faster Attacks Support, Fortify Support (gain Fortification on hit — NOTE: Fortify on movement skills was nerfed, may not stack efficiently)

### Leap Slam
- **Type**: Attack, Movement, Melee, Slam
- **Requires**: Melee weapon (axe, mace, sword, staff, etc.)
- **Strengths**: Crosses gaps and obstacles. No charge limit. AoE on landing.
- **Weaknesses**: Slow animation unless you invest in attack speed. Can feel clunky at low speed.
- **Best for**: Melee builds with 2H weapons or sword/axe. Staff builds.
- **Link with**: Faster Attacks Support

### Whirling Blades
- **Type**: Attack, Movement
- **Requires**: Dagger or claw
- **Strengths**: Very fast with high attack speed. Horizontal dash. No charge limit.
- **Weaknesses**: Can't cross gaps or obstacles. Requires dagger/claw. Can desync in rough terrain.
- **Best for**: Fast-hitting dagger/claw builds (Lightning Strike, Venom Gyre)
- **Link with**: Faster Attacks Support

### Frostblink
- **Type**: Spell, Blink
- **Requires**: Nothing
- **Strengths**: Instant cast (no animation lock), creates chilled ground at origin and destination, short cooldown
- **Weaknesses**: Very short range. Cooldown-based (not charge-based).
- **Best for**: Builds that want instant repositioning without animation lock. RF builds.
- **Note**: The "instant" property makes it usable mid-cast/attack without interrupting

### Dash
- **Type**: Movement, Travel, Blink
- **Requires**: Nothing
- **Strengths**: Fast animation, travels through enemies, stores 2 charges
- **Weaknesses**: Shorter distance than Flame Dash, doesn't cross gaps as reliably
- **Best for**: Builds wanting a responsive non-spell movement option

### Movement Skill Selection Guide
| Weapon Type | Best Movement Skill | Alternative |
|------------|-------------------|-------------|
| Wand + Shield | Flame Dash | Shield Charge |
| Sceptre + Shield | Shield Charge | Flame Dash |
| Dagger / Claw | Whirling Blades | Flame Dash |
| 2H Sword/Axe/Mace | Leap Slam | Flame Dash |
| Staff | Leap Slam | Flame Dash |
| Bow | Flame Dash | Dash |
| Unarmed | Flame Dash | Frostblink |
| Any (RF/Caster) | Flame Dash | Frostblink |

---

## Guard Skills

Guard skills provide a temporary defensive buffer when activated. Only ONE guard skill can be active at a time (they share a cooldown category).

### Molten Shell
- **Effect**: Absorbs damage up to a cap based on your ARMOUR value. While active, damage is reduced.
- **Cap formula**: 20% of your armour as damage absorption (at gem level 20)
- **Duration**: ~3 seconds base
- **Best for**: Armour-based builds (with Determination + Granite Flask, your Molten Shell can absorb 10,000+ damage)
- **THE default guard skill for armour builds** — if you have 30k+ armour, Molten Shell is almost always best
- **Vaal Molten Shell**: Massively increased absorption. Save for dangerous moments.

### Steelskin
- **Effect**: Absorbs a FLAT amount of damage (not based on any stat). Also prevents bleeding during effect.
- **Cap**: ~2000-2500 damage at gem level 20
- **Duration**: ~1.5 seconds base
- **Best for**: Builds without armour investment (evasion builds, ES builds)
- **Note**: The bleed prevention during effect is a nice bonus
- **Less powerful than Molten Shell for armour builds**, but works on anyone

### Immortal Call
- **Effect**: Brief physical + elemental damage reduction. Consumes Endurance Charges for increased duration and effect.
- **Duration**: Very short base (~1 sec), extended significantly by consuming Endurance Charges
- **Best for**: Endurance charge builds (Juggernaut, Gladiator) where charges are reliably generated
- **Downside**: Consumes your endurance charges — trades sustained phys reduction for burst immunity
- **Minimum charges**: Cannot consume minimum endurance charges (see crit-charges.md)

### Bone Armour (Necromancer Only)
- **Effect**: Granted by Bone Barrier ascendancy node. Absorbs damage based on minion life.
- **Best for**: Necromancers specifically — it's free from the ascendancy

### Guard Skill Automation
Guard skills are almost ALWAYS automated via CWDT (see below). Manual guard skills are only used in specific situations (Vaal Molten Shell for boss burst phases).

---

## Cast When Damage Taken (CWDT) Setups

CWDT is the backbone of build automation. It auto-casts linked skills when you take cumulative damage.

### How CWDT Works
- Tracks CUMULATIVE damage taken (not per-hit)
- When the damage threshold is reached, ALL linked compatible skills trigger simultaneously
- Has an internal cooldown (~250ms) before it can trigger again
- **Level restriction**: CWDT can only support gems with a required level AT OR BELOW a limit determined by CWDT's level
- Higher CWDT level = higher damage threshold needed to trigger = can support higher-level gems

### Low-Level CWDT Setup (Most Common)

**CWDT Level 1-3** (triggers after ~500-600 damage taken):
- Triggers frequently — almost every time you get hit
- Can only support gems requiring level ≤ 38 (approximately)
- **Standard setup**: CWDT (lvl 1-3) + Molten Shell/Steelskin (low level) + [optional utility]
- DO NOT level CWDT or the linked gems past your intended level — right-click the "+" to dismiss level-ups

**Why low-level is best for guard skills:**
- Low CWDT triggers more often = guard skill is up more often
- A level 1 Molten Shell still absorbs based on your ARMOUR (which is high), not gem level
- The gem level mainly affects the absorption cap — even low-level Molten Shell with 40k armour absorbs ~8000 damage
- Triggering every ~500 damage means your guard skill is almost always active

### High-Level CWDT Setup (Niche)

**CWDT Level 20** (triggers after ~3200 damage taken):
- Triggers less frequently — only after significant damage
- Can support high-level gems
- **Use case**: Linking with high-level utility gems that need max level (some curses, some utility spells)
- Less common than low-level setup

### Common CWDT Links

**The Standard 4-Link:**
```
CWDT (lvl 1) + Molten Shell (lvl 10) + [Optional] + [Optional]
```
or
```
CWDT (lvl 1) + Steelskin (lvl 10) + [Optional] + [Optional]
```

**Optional slots for CWDT link:**
- **Tempest Shield**: Spell block + shock immunity. Great if you have block investment.
- **Cold Snap** (low level): Creates chilled ground, generates Frenzy Charges on kill
- **Wave of Conviction** (low level): Applies exposure to enemies. Useful if you need automated exposure.

### Multiple CWDT Setups
- You CAN have multiple CWDT setups in different link groups
- Each has its own independent cooldown and damage tracking
- Example: Low CWDT + Guard Skill in one 3-link, High CWDT + Curse in another
- Don't overdo it — 2 setups maximum is practical

### CWDT Level Table (Key Thresholds)
| CWDT Level | Damage Threshold | Max Supported Gem Req Level |
|-----------|------------------|---------------------------|
| 1 | 528 | 38 |
| 2 | 583 | 40 |
| 3 | 642 | 42 |
| 5 | 774 | 46 |
| 10 | 1222 | 56 |
| 15 | 1886 | 66 |
| 20 | 3272 | 74+ |

---

## Curse Application Methods

Curses are powerful debuffs. The method of application determines both convenience and effectiveness (see auras-reservation.md for curse penalty details).

### Self-Cast (Full Effect, Manual)
- Cast the curse yourself as an active skill
- **No penalty** to curse effect (post-3.20)
- Downside: Requires a button press, mana cost, cast time
- Best for: Boss fights where curse effect matters most

### Arcanist Brand (Full Effect, Semi-Automated)
- Link curse to Arcanist Brand
- Brand attaches to enemy and periodically casts the linked curse
- **No penalty** to curse effect
- Good balance of automation and full power
- Costs a link group (typically 3-link: Arcanist Brand + Curse 1 + Curse 2)

### CWDT + Curse (Automated, Level-Limited)
- Link curse to CWDT
- Curse auto-applies when you take damage
- **No explicit penalty** from CWDT, but curse gem level is limited by CWDT level restriction
- Lower gem level = less effective curse

### Hextouch Support (Automated on Hit, Penalized)
- Link curse to an attack skill via Hextouch Support
- Curse applies when the attack hits
- **35% less curse effect** penalty
- Good for attack builds that hit frequently

### Blasphemy Support (Aura-Style, Penalized)
- Turns a curse into an aura (reserves mana, affects nearby enemies)
- **25% less curse effect** penalty
- Reserves 35% mana — significant cost
- Always-on within range — no button press needed

### Curse on Hit Ring Mods (Automated, Convenient)
- Some rings roll "Curse Enemies with [Curse] on Hit" (influenced mod)
- Automatically applies a level ~8-12 curse on hit
- Very convenient — frees up gem sockets and link groups

### Curse Application Priority
For most builds:
1. **Mapping**: Automate via CWDT, Hextouch, or curse-on-hit ring. Convenience > power for trash.
2. **Bossing**: Self-cast or Arcanist Brand for full effect. Curse effectiveness matters against bosses.
3. **If reservation budget allows**: Blasphemy is zero-effort, always-on.

---

## Offering Automation (Necromancer)

Offerings are powerful buff skills for minion builds. They consume corpses and provide temporary bonuses to you (via Mistress of Sacrifice) and your minions.

### The Three Offerings (pick one — only one can be active)

**Bone Offering**: +Block chance for you and minions. Life recovery on block.
- Best for: Defensive setups. With Mistress of Sacrifice, gives YOU block chance.
- The default choice for most Necromancers.

**Flesh Offering**: Increased attack/cast/movement speed for minions. Speed bonus for you (via Mistress of Sacrifice at 50%).
- Best for: Aggressive/DPS-focused setups.

**Spirit Offering**: Grants flat Energy Shield based on corpse life. Chaos resistance.
- Best for: ES-based minion builds. Niche.

### Trigger Weapon Automation
The standard method for automating offerings:

**Setup**: Craft "Trigger a Socketed Spell when you Use a Skill" on your weapon (crafting bench). Socket:
1. **Desecrate** — creates corpses (offerings need corpses to consume)
2. **Offering of choice** — consumes the corpses Desecrate created
3. **Curse or utility spell** — a third automated skill (Vulnerability, Conductivity, etc.)

**How it works**: Every time you use ANY skill, the trigger weapon casts one socketed spell in rotation. Over 3 skill uses, all three spells fire once each. This keeps your offering permanently active with zero button presses.

### Arcanist Brand Alternative
If you don't have the trigger weapon craft:
- Arcanist Brand + Desecrate + Offering (3-link)
- Brand attaches to enemy and cycles through Desecrate → Offering
- Works but less consistent than trigger weapon

---

## Flask Automation

### Instilling Orb Enchantments (Key Auto-Use Options)
- **"Used when Charges reach Full"**: Flask activates automatically at max charges. Great for maintaining uptime.
- **"Used when you become Frozen"**: Auto-removes freeze. Frees you from needing to react.
- **"Used when you become Bleeding"**: Auto-removes bleed. Critical for builds without other bleed immunity.
- **"Used when an adjacent Flask is used"**: Chain-triggers — press one flask, adjacent ones auto-fire. Reduces "flask piano" to 1-2 buttons.
- **"Used at the start of each Flask Effect"**: Triggers whenever any flask is used. Good for utility flasks.

### Practical Flask Automation Setup
1. **Life Flask**: Enchant with "Used when you become Bleeding" (auto-purge bleed + instant heal)
2. **Freeze Immunity Flask**: Enchant with "Used when you become Frozen" (auto-purge freeze)
3. **Quicksilver Flask**: Enchant with "Used when Charges reach Full" (permanent uptime while mapping)
4. **Remaining flasks**: "Used when an adjacent Flask is used" to chain-trigger from one button press
5. Result: Press ONE flask button → chain-trigger hits adjacent flasks → all utility active.

---

## Other Utility Automation

### Blood Rage (Attack Speed + Frenzy Generation)
- Toggle skill that grants attack speed and Frenzy Charges on kill
- Deals physical damage over time to you (degen)
- Usually activated manually once and left running (refreshes on kill)
- Most players just press it once at the start of each map

### Warcries (Berserker / Slam Builds)
- Enduring Cry: Generates endurance charges, life regen burst.
- Intimidating Cry: Exerts next attacks for double damage.
- Seismic Cry: Exerts next attacks for more AoE + damage.
- **Call to Arms keystone**: Makes warcries instant (no cast time) but adds a shared cooldown. Great QoL.

### Convocation (Minion Builds)
- Teleports all minions to your location + heals them
- Bind to an accessible key — you'll use this constantly
- Can link to CWDT for auto-summon when you take damage

### Phase Run / Withering Step
- **Phase Run**: Phasing + movement speed. Cancelled by other skills. Good for pure movement.
- **Withering Step**: Phasing + Elusive + applies Withered. Self-cancels. Good for chaos DoT builds.
- Both can be bound to left-click for automatic activation while moving

### Left-Click Binding Trick
Bind certain skills to left-click (the "move" button):
- The skill activates automatically as you move
- Works well with: Phase Run, Withering Step, movement skills
- To set: Drag the skill to the left-click slot, check "Always Attack Without Moving"

---

## Standard Automation Loadouts

### Generic Life/Armour Build
- **CWDT 4-Link**: CWDT (lvl 1) + Molten Shell (lvl 10) + [utility] + [utility]
- **Auras**: Determination + Defiance Banner + [offensive aura]
- **Movement**: Flame Dash + Second Wind (or Shield Charge)
- **Flasks**: Instilling Orbs for auto-use
- **Manual**: Main skill + movement skill only

### Minion Build (Necromancer)
- **CWDT**: CWDT (lvl 1) + Bone Armour/Steelskin
- **Trigger Weapon**: Desecrate + Bone Offering + Vulnerability
- **Movement**: Flame Dash
- **Utility**: Convocation (manual)
- **Auras**: Determination + Hatred/Wrath (Generosity) + Defiance Banner

### DoT Caster (Occultist)
- **CWDT**: CWDT (lvl 1) + Steelskin + Tempest Shield
- **Curse**: CWDT for mapping, self-cast Despair for bosses
- **Movement**: Flame Dash + Second Wind
- **Left-click**: Withering Step (free Wither + phasing)
- **Auras**: Grace/Determination + Malevolence + Defiance Banner

### CoC Build
- **CWDT**: CWDT (lvl 1) + Molten Shell
- **Main 6-Link**: Cyclone + CoC + spells (this IS your gameplay)
- **Movement**: Flame Dash (gap crossing only — Cyclone IS movement)
- **Auras**: Determination/Grace + Zealotry/Hatred + Precision + Defiance Banner

---

## Common Automation Mistakes

1. **Over-leveling CWDT or linked gems**: RIGHT-CLICK the "+" to dismiss. High CWDT = less frequent triggers.
2. **Linking incompatible gems to CWDT**: CWDT triggers SPELLS only, not attacks. Check gem level restriction.
3. **Two guard skills simultaneously**: Only ONE can be active. Pick one.
4. **Forgetting to reactivate auras after death**: Check if all auras are running.
5. **Not using Instilling Orbs**: Flask auto-use is huge QoL. Use it.
6. **Manual curse for trash mobs**: Automate for mapping, self-cast for bosses only.
7. **No movement skill**: Always have one. Both QoL and defensive.
8. **Trigger weapon cooldown gaps**: Be aware that offering may have brief downtime between trigger cycles.
