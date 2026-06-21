# Flasks — Complete Reference

## Flask Fundamentals

Flasks are rechargeable potions that provide recovery (life/mana) or temporary buffs (utility). Every character has 5 flask slots. Flasks are one of the most impactful systems in PoE — a well-crafted flask setup can be the difference between dying and surviving.

### Core Mechanics
- Flasks consume CHARGES when used and provide an effect for a duration
- Charges are gained by KILLING enemies (each kill grants charges to all equipped flasks)
- All flasks fully recharge when entering town or hideout
- Flasks can be Normal, Magic, or Unique rarity (never rare)
- Magic flasks have one prefix and one suffix
- Flask charges DO NOT generate from DoT kills — the killing blow must be a hit
- Flask charges can also be generated from taking damage (some suffixes), critting (tree/gear), or passively (Pathfinder)
- Flasks cannot gain charges while their effect is active (by default — some modifiers bypass this)

### Charge System
- Each flask has: Maximum Charges, Charges per Use, and Charges Gained per kill
- Example: A Granite Flask might have 60 max charges, use 30 per activation, and gain ~5 charges per kill
- This means ~6 kills fully recharges one use, and the flask can store 2 uses
- Charge gain scales with monster rarity: rare/unique monsters grant more charges
- Boss fights with no adds are the hardest to sustain flasks — plan accordingly

### Flask Effect Duration
- Each flask type has a base duration (typically 4-6 seconds for utility flasks)
- "% increased Flask Effect Duration" extends the duration
- "% increased Flask Charges Gained" helps sustain
- Flask quality (0-20%) typically increases duration or charges gained
- Some suffixes give "used when charges reach full" — auto-use for convenience

---

## Recovery Flasks (Life, Mana, Hybrid)

### Life Flasks
- Recover life over time (not instant by default)
- Recovery stops when you reach full life
- Higher tier = more total recovery, longer duration
- Divine Life Flask is the highest tier (level 65+)

**Key Prefixes:**
- **Seething**: Instant recovery, 66% less recovery amount. Use when you need burst healing NOW.
- **Bubbling**: 50% instant, 50% over time, shorter duration. Good middle ground.
- **Catalysed**: Increased recovery speed (faster over-time, not instant). More total healing per second.
- **Saturated**: Increased recovery amount but longer duration.

**Key Suffixes:**
- **of Staunching**: Removes bleeding and grants bleed immunity during flask effect. ESSENTIAL — bleeding kills builds that don't have it.
- **of Dousing**: Removes ignite. Less critical but useful in ignite-heavy content.
- **of Heat**: Removes chill/freeze. Critical if you don't have freeze immunity elsewhere.

### Mana Flasks
- Same mechanics as life flasks but for mana
- Recovery stops when mana is full
- Less commonly used endgame — mana leech/regen usually handles sustain
- Still useful for: Archmage builds, builds with very high mana costs, MoM builds

### Hybrid Flasks
- Recover both life AND mana simultaneously
- Lower individual recovery than dedicated flasks
- Niche use — occasionally valuable in builds that need both

### When to Use Life Flasks
- **Campaign through early maps**: Always have one life flask
- **Mid-endgame**: Many builds drop the life flask once leech/regen is sufficient
- **Hardcore**: Often keep a panic life flask (Seething) permanently
- **Boss fights**: Even with good sustain, a panic flask saves lives

---

## Utility Flask Base Types

Each utility flask grants a specific base effect when active:

### Granite Flask — Armour
- Grants +3000 armour during effect
- Core defensive flask for any build using armour
- Pairs with Determination for massive armour stacking
- Quality: +1% increased Armour during effect per 1% quality

### Jade Flask — Evasion
- Grants +3000 evasion rating during effect
- Core for evasion-based builds (Ranger, Shadow, Trickster)
- Pairs with Grace for evasion stacking
- Quality: +1% increased Evasion Rating during effect per 1% quality

### Basalt Flask — Physical Damage Reduction
- Grants 15% additional physical damage reduction during effect
- Stacks with armour's physical reduction — very strong against physical damage
- Less effective against the very large hits where armour falls off
- Quality: +0.5% increased effect per 1% quality

### Quartz Flask — Phasing + Dodge
- Grants Phasing (walk through enemies) and 10% chance to Dodge attacks/spells
- Phasing is underrated — walking through enemies prevents getting body-blocked
- The dodge is a nice defensive bonus
- Quality: +0.5% chance to Dodge per 1% quality

### Quicksilver Flask — Movement Speed
- Grants 40% increased Movement Speed during effect
- Nearly universal — almost every build runs one
- Quality: +0.5% increased Movement Speed per 1% quality

### Silver Flask — Onslaught
- Grants Onslaught (20% increased attack/cast/movement speed) during effect
- Very strong for builds that don't have permanent Onslaught from other sources
- Redundant if you have Onslaught from Raider, Silver Tongue, etc.
- Quality: +0.5% increased Onslaught effect per 1% quality

### Diamond Flask — Critical Strike Chance
- Grants 100% increased Global Critical Strike Chance during effect
- Core for crit builds that aren't already drowning in increased crit
- Changed in 3.15 from "Lucky crit" to "100% increased" — still strong but additive
- Quality: +0.5% increased Global Critical Strike Chance per 1% quality

### Sulphur Flask — Consecrated Ground + Damage
- Creates Consecrated Ground on use, grants 40% increased Damage during effect
- Consecrated Ground: life regen, increased damage to enemies standing on it
- Great general-purpose offensive flask
- Quality: +0.5% increased Damage per 1% quality

### Amethyst Flask — Chaos Resistance
- Grants +35% Chaos Resistance during effect
- Extremely valuable in early endgame when chaos res is -60%
- Often replaced once you get chaos res on gear
- Quality: +0.5% increased Chaos Resistance per 1% quality

### Ruby / Sapphire / Topaz Flask — Elemental Resistance
- Grants +6% to maximum Fire/Cold/Lightning resistance during effect
- The MAX RESISTANCE bonus is extremely powerful (see defenses.md for max res math)
- Going from 75% to 81% fire res = 24% less fire damage taken
- Core for elemental damage-heavy encounters (Atziri, Shaper phases)
- Quality: +0.25% increased max resistance per 1% quality

### Stibnite Flask — Smoke Cloud + Blind
- Creates a Smoke Cloud on use that blinds enemies passing through it
- Blind: 50% less accuracy for enemies (effectively halves their chance to hit you with attacks)
- Niche but powerful — good for melee builds standing in groups of enemies
- Quality: +0.5% increased Blind effect per 1% quality

---

## Flask Modifiers (Magic Flasks)

### Important Prefixes (Utility Flasks)
- **Experimenter's**: Increased effect duration (more uptime)
- **Chemist's**: Reduced charges used (more activations per fill)
- **Alchemist's**: Increased effect + reduced duration (stronger but shorter)
- **Flagellant's**: Gain charges when hit (sustain during boss fights — very valuable)

### Important Suffixes (Utility Flasks)
- **of the Armadillo**: Increased armour during effect
- **of the Deer**: Increased movement speed during effect
- **of the Cheetah**: Increased attack speed during effect
- **of Warding**: Removes curses, curse immunity during effect. ESSENTIAL — cursed maps and boss curses can be deadly.
- **of the Owl**: Chance to avoid being stunned during effect
- **of Grounding**: Removes shock, shock immunity during effect
- **of Heat**: Removes chill/freeze, immunity during effect
- **of Dousing**: Removes ignite, ignite immunity during effect
- **of Staunching**: Removes bleeding, bleed immunity during effect

### The "Immunity" Suffixes — Critical Flask Crafting
Several suffixes provide ailment/curse removal AND immunity during the flask effect:
- **of Warding**: Curse immunity — run this on at least ONE flask
- **of Heat**: Freeze immunity — MANDATORY if you don't have it from tree/gear
- **of Staunching**: Bleed immunity — MANDATORY, bleeding is lethal
- **of Grounding**: Shock immunity — very important, shock increases all damage you take

These four "removal" suffixes are the highest priority for flask crafting. Every build should have at least: Staunching, Heat, and Warding covered. Grounding is highly recommended.

---

## Key Unique Flasks

### Offensively Focused

**Atziri's Promise** (Amethyst Flask):
- Gain % of physical damage as extra chaos damage
- Gain % of elemental damage as extra chaos damage
- Chaos damage leech
- One of the cheapest and most universally useful unique flasks. Works on almost every build.

**Bottled Faith** (Sulphur Flask):
- Creates Consecrated Ground that gives enemies -10% increased damage taken
- +2% to base critical strike chance against enemies on Consecrated Ground
- The +2% base crit is additive to base — extremely powerful for crit builds
- Very expensive. Endgame investment.

**Dying Sun** (Ruby Flask):
- +2 additional projectiles during effect
- Increased AoE during effect
- Core for projectile builds (Tornado Shot, Ice Shot, Spark)
- Projectiles have no damage penalty (unlike GMP)

**Lion's Roar** (Granite Flask):
- More melee physical damage during effect (huge multiplier)
- Knockback on melee hit
- Core for melee physical builds. The "more" damage is a direct multiplier.
- Knockback can be annoying for some builds (pushes enemies away)

**Taste of Hate** (Sapphire Flask):
- % of physical damage taken as cold damage (defensive — shifts damage type)
- Gain % of physical damage as extra cold damage (offensive)
- Dual-purpose: offense + defense in one flask
- Very strong for physical attack builds

**Sin's Rebirth** (Stibnite Flask):
- Gain % of physical damage as extra chaos damage
- Creates Smoke Cloud (blind)
- Offense + defense combo. Good for physical builds.

### Defensively Focused

**Rumi's Concoction** (Granite Flask):
- +% chance to block attacks and spells during effect
- Core for block builds — can push block chance to cap during flask
- Less valuable if you're already block-capped

**Coruscating Elixir** (Ruby Flask):
- Chaos damage does not bypass Energy Shield during effect
- Normally chaos damage goes straight to life, bypassing ES. This flask prevents that.
- Core for CI (Chaos Inoculation) builds that face heavy chaos damage, or Low Life builds

**Forbidden Taste** (Quartz Flask):
- Instant full life recovery on use
- You take 8% of max life as chaos damage per second during effect
- Panic button — instant full heal but the degen can kill you if you're not careful

### Utility / Niche

**Cinderswallow Urn** (Silver Flask):
- Recovery on kill during effect (life, mana, or ES depending on variant)
- Enemies killed during effect grant Onslaught
- Good mapping flask — sustain on kill

**The Wise Oak** (Bismuth Flask):
- Penetrate resistance of your HIGHEST uncapped elemental resistance
- Reduced damage taken from your LOWEST uncapped elemental resistance
- Requires balancing your resistances: if all three are equal, you get both effects for all elements
- Very powerful when balanced. Requires careful gearing.

**Divination Distillate** (Hybrid Flask):
- Increased rarity and quantity of items found during effect
- +max all elemental resistances during effect
- Effect ends when life AND mana are full — MoM builds or builds with incomplete mana regen keep it active longest
- Core for magic find builds

---

## Flask Sustain Mechanics

### How Charges Are Gained
1. **Killing enemies**: Base charge gain per kill. Most common source.
2. **Flask charge gain on hit**: Some gear/tree nodes grant charges on hit. Works on bosses.
3. **Flask charge gain on crit**: "Gain a Flask Charge when you deal a Critical Strike" — tree nodes, gear. ~0.132s cooldown per proc.
4. **Pathfinder Nature's Boon**: Gain flask charges passively over time. Works everywhere, including boss fights with no adds.
5. **Flagellant's prefix**: Gain charges when hit. Works on bosses that hit frequently.
6. **Reduced charges used**: Makes each activation cheaper → more uses per fill.
7. **Increased charges gained**: More charges per kill → faster refill.

### Boss Fight Sustain
Flask sustain during boss fights (no adds to kill) is a real concern:
- **Pathfinder**: Passive charge gain solves this entirely
- **Flagellant's prefix**: Gain charges when hit — works if the boss attacks frequently
- **Flask charge on crit**: Works if you're hitting the boss with crits
- **Reduced charges used**: Fewer charges needed = more activations from stored charges
- **Multiple uses stored**: Flasks with 2-3 stored uses can sustain through longer fights
- **Traitor keystone** (timeless jewel): Gain charges over time at the cost of reduced flask effect
- **Enduring suffix on mana flasks**: Flask effect doesn't end when mana is full → longer duration

### Permanent Flask Uptime
Some builds achieve permanent flask uptime:
- **Pathfinder**: Nature's Boon + Nature's Adrenaline + increased flask duration = permanent
- **Fast mapping**: Kill speed keeps flasks permanently charged via kills
- **Increased flask effect duration**: Extends uptime, bridges gaps between charge generation
- **Auto-use on full charges**: Suffix "used when charges reach full" maintains uptime automatically

---

## Ailment Immunity via Flasks

### The Flask Immunity Approach
Before investing in permanent ailment immunity from gear/tree, flasks can cover ailments:
- **Freeze**: of Heat suffix (removes + immunity during effect)
- **Bleed**: of Staunching suffix (removes + immunity)
- **Shock**: of Grounding suffix (removes + immunity)
- **Curse**: of Warding suffix (removes + immunity)
- **Ignite**: of Dousing suffix (removes + immunity)
- **Poison**: of the Antidote suffix (removes + immunity)

### Flask Immunity vs Permanent Immunity
- Flask immunity only works DURING flask effect — if flask runs out, you're vulnerable
- Flask immunity requires pressing the flask when the ailment hits (reactive, not proactive)
- Permanent immunity (from tree, gear, or ascendancy) is always better but costs more investment
- Typical progression: Use flask immunity early → transition to permanent immunity as gear improves

### Purity of Elements Alternative
The Purity of Elements aura grants complete elemental ailment immunity (freeze, shock, ignite, chill, scorch, brittle, sap) for 35% mana reservation. This frees up 3-4 flask suffix slots but costs significant reservation. Often used as a gearing crutch while building toward permanent immunity on gear.

---

## Flask Crafting Guide

### Priority Order for Flask Suffixes
1. **of Staunching** (bleed removal) — on life flask or any utility flask
2. **of Heat** (freeze removal) — MANDATORY unless immune via tree/gear
3. **of Warding** (curse removal) — one flask needs this
4. **of Grounding** (shock removal) — highly recommended
5. Remaining suffixes: defensive or offensive as needed

### How to Craft
- **Alteration + Augmentation**: Roll magic flasks until desired prefix + suffix
- **Instilling Orb**: Adds an "enchantment" that auto-uses the flask under conditions ("used when you become Frozen," "used when charges reach full," etc.)
- **Enkindling Orb**: Adds an enchantment that increases flask effect but prevents charge gain during effect
- **Glassblower's Bauble**: Adds quality (increases base effect of the flask type)
- **Hillock bench craft** (Fortification): Can add 26-28% quality to flasks (beyond 20%)

### Instilling Orb Enchantments (Auto-Use)
- "Used when Charges reach Full" — permanent uptime if you generate charges fast enough
- "Used when you become Frozen" — reactive freeze removal
- "Used when you become Bleeding" — reactive bleed removal
- "Used when an adjacent Flask is used" — chain-triggers with other flasks
- "Used at the start of each Flask Effect" — triggers when any flask activates
- These are extremely quality of life — reduces flask piano to one or two buttons

### Enkindling Orb Enchantments (Stronger Effect)
- Increased effect of the flask
- Increased duration of the flask
- Increased charges gained (but cannot gain charges during effect)
- Use Enkindling on flasks you don't need permanent uptime on — the "cannot gain charges during effect" downside matters less for burst flasks

---

## Standard Flask Setups by Archetype

### Generic Melee (Physical)
1. Divine Life Flask of Staunching (or Seething for instant heal)
2. Granite Flask of Heat (armour + freeze immunity)
3. Lion's Roar (or Basalt Flask) — more melee damage / phys reduction
4. Quicksilver Flask of Warding (movement + curse removal)
5. Diamond Flask of Grounding (crit + shock removal) — or Sulphur Flask for non-crit

### Generic Caster (Elemental)
1. Divine Life Flask of Staunching
2. Jade or Granite Flask of Heat (defense + freeze)
3. Quicksilver Flask of Warding (movement + curse)
4. Bottled Faith or Sulphur Flask of Grounding (damage + shock removal)
5. Diamond Flask or Atziri's Promise (crit or extra damage)

### DoT / Minion Build
1. Divine Life Flask of Staunching
2. Granite or Jade Flask of Heat
3. Quicksilver Flask of Warding
4. Quartz Flask of Grounding (phasing helps positioning)
5. Sulphur Flask or Amethyst Flask (damage or chaos res)

### Evasion / Dodge Build
1. Divine Life Flask of Staunching
2. Jade Flask of Heat (evasion + freeze)
3. Quartz Flask of Grounding (phasing + dodge + shock removal)
4. Quicksilver Flask of Warding
5. Diamond Flask or Silver Flask (crit or onslaught)

### Pathfinder (Permanent Flasks)
1-5: All unique flasks or specialized utility flasks. Pathfinder's passive sustain means you can run expensive unique flasks permanently. Build-specific.

---

## Practical Decision Framework

1. **First flask slot**: Always cover bleed removal (of Staunching) — bleeding is the #1 flask-preventable death
2. **Second priority**: Freeze removal (of Heat) — being frozen = being dead against any follow-up damage
3. **Third priority**: Curse removal (of Warding) — cursed with Vulnerability or Elemental Weakness is extremely dangerous
4. **Fourth priority**: Shock removal (of Grounding) — shock increases all damage you take by up to 50%
5. **Movement**: Nearly every build wants a Quicksilver Flask — movement speed is both offensive (faster mapping) and defensive (dodging)
6. **Offensive flask**: At least one damage flask (Diamond for crit, Sulphur for generic, Lion's Roar for melee, Atziri's Promise for everyone)
7. **Quality all flasks to 20%**: Free stats. Use Glassblower's Baubles before rolling magic.
8. **Instilling Orbs**: Automate bleed/freeze removal flasks ("Used when you become Frozen/Bleeding") — this is massive QoL
9. **Endgame transition**: Replace ailment flasks with permanent immunity from tree/gear, then use those slots for more offensive or defensive unique flasks
10. **Always have a plan for boss flask sustain** — if you can't kill adds, consider Flagellant's prefix or flask charge on crit
