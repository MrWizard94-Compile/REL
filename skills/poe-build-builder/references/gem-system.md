# Gem System — Complete Reference

## Skill Gem Fundamentals

All active abilities in PoE come from skill gems. Two types:
- **Skill Gems (Active)** — grant usable skills (attacks, spells, auras, heralds, warcries, etc.)
- **Support Gems** — modify skill gems they're linked to (must be in LINKED sockets)

A skill gem does nothing without being socketed in gear. A support gem does nothing unless linked to a compatible active skill gem.

---

## Sockets & Links

### Socket Basics
- Items can have 1-6 sockets depending on item type
- **Body armour and 2-handed weapons**: Up to 6 sockets
- **1-handed weapons, shields, helmets, gloves, boots**: Up to 4 sockets
- **Rings, amulets, belts**: 0 sockets (but can have "socketed gems supported by" mods via crafting/influence)
- Sockets must be LINKED (shown by a bar between them) for supports to apply to skills
- A support affects ALL compatible skill gems in the same link group

### Socket Colors
- **Red** — associated with Strength
- **Green** — associated with Dexterity
- **Blue** — associated with Intelligence
- **White** — accepts any gem color (rare, from corruption or specific crafting)

Socket color rolling is WEIGHTED by the item's attribute requirements:
- A pure Strength chest (e.g., Astral Plate) heavily favors red sockets
- A Dex/Int base (e.g., Assassin's Garb) favors green and blue
- Getting "off-color" sockets (colors not matching item requirements) is harder and costs more chromes

### Off-Color Socket Methods
- **Chromatic Orbs**: Random reroll, weighted by item requirements. Cheap for on-color, expensive for off-color.
- **Crafting Bench (Vorici recipes)**: "At least X [color] sockets" — guarantees minimum colors. More expensive per use but deterministic. Best method for 1-2 off-colors.
- **Jeweller's method**: On items with very low socket count requirements, repeatedly rolling 1-2 sockets then adding more can force off-colors
- **Harvest crafting**: Can recolor specific sockets to specific colors
- **Corruption**: Can randomly add white sockets (Vaal Orb or Locus of Corruption)

### "Socketed Gems Are Supported By" Mods
Some gear can grant built-in support gem effects:
- **Influenced gear**: Can roll mods like "Socketed Gems are Supported by Level 20 [Support]"
- **Crafting bench**: Some support mods are benchcraftable
- **Unique items**: Some grant built-in supports (e.g., a body armour granting Level 1 Maim to socketed gems)
- **Doryani's Catalyst**: Built-in Level 20 Elemental Proliferation to socketed gems
- These count toward the support limit but don't take a socket — effectively giving you a 7-link or 8-link

---

## Gem Levels

### How Leveling Works
- Gems gain experience as YOUR character gains experience (proportional)
- Gems level from 1 to 20 by default (some cap lower)
- Each level requires a minimum CHARACTER level to equip
- When a gem is ready to level, a "+" icon appears next to your health globe
- You can CHOOSE not to level a gem — right-click the "+" to dismiss (important for CWDT setups)
- Gems continue to gain XP even if you don't click the level-up
- Dead characters don't gain XP → gems don't gain XP

### Gem Level Scaling — Spells vs Attacks
This is one of the most fundamental distinctions in PoE:

**Spells**: Base damage comes from the GEM LEVEL. Higher gem level = more base damage.
- A level 20 Fireball deals ~1640-2460 fire damage
- A level 21 Fireball deals significantly more
- "+1 to level of fire skill gems" on gear directly increases spell base damage
- This makes gem levels THE primary scaling axis for spells

**Attacks**: Base damage comes from your WEAPON, not the gem.
- Attack gem levels mainly increase: % damage effectiveness, flat added damage (small), utility bonuses
- Weapon DPS matters far more than attack gem level
- "+1 to level of [type] gems" on gear helps attacks much less than spells

**Minions**: Base stats (life, damage, resistances) come from the GEM LEVEL.
- Minion gem levels are critically important — similar to spells
- "+1 to level of minion skill gems" is extremely valuable for summoners

**Auras**: Effect strength scales with gem level.
- Higher level Determination = more armour granted
- Flat reservation auras (Precision, Vitality, Clarity) also increase their reservation cost with level

### +Gem Level Sources and Stacking
"+X to level of [type] skill gems" is one of the most powerful stats for spell/minion builds:

Sources:
- **Weapon/shield mods**: "+1 to level of all [element] spell skill gems" (crafted or dropped)
- **Amulet mods**: "+1 to level of all skill gems" (very expensive and powerful)
- **Body armour**: "+1 to level of socketed gems" (corruption implicit or influenced mod)
- **Empower Support**: +2 to level of supported gems at level 3 (see Exceptional Gems section)
- **Specific uniques**: Various level bonuses
- **Corruption implicits**: "+1 to level of socketed gems" on body armour or weapon

Stacking: All +level sources ADD together. Example:
- Level 20 base gem + Empower 3 (+2) + "+1 all spell gems" weapon + "+1 all gems" amulet = Level 24 gem
- The damage difference between level 20 and level 24 for a spell can be 40-60% more base damage

### The Level 20/20% Quality Vendor Recipe
- Vendor a level 20 gem + 1 Gemcutter's Prism → receive that gem at Level 1 with 20% quality
- This is the standard way to get 20% quality on all your gems without spending 20 GCPs each
- Only works with level 20 gems — not level 21 or corrupted gems

---

## Gem Quality

### How Quality Works
- Quality ranges from 0% to 20% (23% with specific alternate quality methods or double corruption)
- Each gem has a specific quality bonus listed in its description
- Quality bonuses vary wildly per gem — some are damage, some are AoE, some are utility
- Quality is added with Gemcutter's Prism (GCP): each GCP adds 1% quality
- The vendor recipe (see above) is much more efficient than using 20 GCPs

### Alternative Quality Gems
Three alternative quality types exist, each with a different quality bonus:
- **Anomalous** (cyan): Different quality bonus, often utility-focused
- **Divergent** (magenta/pink): Different quality bonus, can be build-enabling
- **Phantasmal** (green): Different quality bonus, often niche but powerful

Example: Regular Determination quality might give increased armour, while Anomalous Determination quality might give increased aura effect. Always check what the alternative quality does — sometimes it's transformative.

Sources: Heist reward rooms (primarily), some league content

### Quality vs Level Priority
- **For spells/minions**: Gem LEVEL >>> Quality. Always prioritize +level first.
- **For attacks**: Quality and level are both minor compared to weapon DPS
- **For supports**: Quality is a nice bonus but rarely build-changing
- Rule: Get all gems to 20% quality (via vendor recipe), then focus on +levels for your main skill

---

## Damage Effectiveness

Every skill gem has a "Damage Effectiveness" stat (shown as "Effectiveness of Added Damage: X%").

### What It Does
- Multiplies ALL flat added damage applied to that skill
- Includes: added damage from gear, auras (Wrath, Anger), supports (Added Lightning), Heralds
- Does NOT affect the gem's own base damage

### Why It Matters
- High effectiveness (200%+): Flat added damage supports and auras are very powerful
- Low effectiveness (50-80%): Flat added damage is heavily penalized — scale base damage instead
- Example: A skill with 300% effectiveness turns "+10 to 20 lightning damage" from gear into "+30 to 60"
- Example: A skill with 50% effectiveness turns that same "+10 to 20" into "+5 to 10"

### Practical Impact
- Check your main skill's effectiveness before choosing supports
- High effectiveness → Added Fire/Cold/Lightning supports, flat damage auras, added damage on gear are excellent
- Low effectiveness → Focus on "more" multiplier supports and gem level scaling instead

---

## Mana Cost Multiplier

Every support gem has a "Cost & Reservation Multiplier" listed on it.

### How It Works
- Multiplies the mana cost of the supported skill
- Multiple supports multiply together (not additive)
- Example: Skill costs 20 mana. Support A has 130% multiplier. Support B has 140% multiplier.
  - Final cost: 20 × 1.30 × 1.40 = 36.4 mana per use
- Also affects reservation for aura skills — this is how Enlighten reduces reservation

### Why It Matters
- A 6-link with aggressive supports can make skill costs unmanageable
- Mana sustain must be planned: mana leech, mana on hit, Clarity, mana flask, reduced mana cost crafts
- Some supports have multipliers BELOW 100% (Enlighten, Inspiration) — they reduce costs
- "Socketed gems supported by" mods on gear do NOT add their mana multiplier (free supports!)

---

## Support Gem Selection

### The "More" Multiplier Priority
Support gems are the primary source of "more" damage multipliers. Selection priority:
1. Highest applicable "more damage" multiplier
2. Tags must be compatible (verify!)
3. Consider utility (AoE, chain, speed) vs raw damage
4. Watch mana multiplier — don't make the skill unusable

### Key Damage Supports (grouped by function)

**Generic More Damage:**
- Controlled Destruction: More spell damage, reduced crit chance
- Elemental Focus: More elemental damage, CANNOT inflict elemental ailments (trap!)
- Concentrated Effect: More area damage, less AoE radius (boss swap)
- Increased AoE: Larger area, can swap with Conc Effect for clearing

**Physical Specific:**
- Brutality: More physical damage, CANNOT deal any non-physical damage (kills all elemental/chaos)
- Melee Physical Damage: More melee physical damage
- Impale Support: Chance to impale + increased impale effect

**Elemental Specific:**
- Elemental Damage with Attacks: More elemental damage for attacks
- Added Fire/Cold/Lightning Damage: Flat added damage (scales with damage effectiveness)
- Fire/Cold/Lightning Penetration: Penetrates resistance (very strong for bosses)

**Chaos/DoT Specific:**
- Void Manipulation: More chaos damage, CANNOT deal elemental damage
- Deadly Ailments: More ailment damage, less hit damage
- Swift Affliction: More DoT damage, less skill duration
- Unbound Ailments: More ailment damage, increased ailment duration

**Minion Specific:**
- Minion Damage: More minion damage
- Minion Speed: Faster minion movement and attack/cast speed
- Predator: Can direct minion targeting, more damage against marked target
- Feeding Frenzy: Minions are aggressive, more minion damage when recently fed

**Speed/Mechanic Supports:**
- Spell Echo: Spells repeat (more casts per animation, slight less damage per repeat)
- Multistrike: Attacks repeat (more hits per animation, first repeat deals less, last deals more)
- Greater Multiple Projectiles (GMP): +4 projectiles, significant less damage per projectile
- Lesser Multiple Projectiles (LMP): +2 projectiles, moderate less damage
- Chain/Pierce/Fork: Projectile behavior — chain bounces between enemies, pierce goes through, fork splits
- Unleash: Store seals, release multiple casts at once

### Supports That RESTRICT Your Build (Read Carefully!)
- **Elemental Focus**: Cannot inflict elemental ailments. Kills shock, ignite, freeze, chill. Do NOT use if your build needs ailments.
- **Brutality**: Cannot deal non-physical damage. Kills all elemental and chaos damage from all sources including auras and heralds. If you use Hatred or Herald of Ash with Brutality, the elemental portion is deleted.
- **Void Manipulation**: Cannot deal elemental damage. Same principle as Brutality but for chaos.
- **Avatar of Fire** (keystone, not support, but same principle): Converts all damage to fire, cannot deal non-fire damage.

---

## Exceptional Support Gems (Empower, Enhance, Enlighten)

Three special support gems that modify the SUPPORTED GEM'S STATS rather than its effects:

### Empower Support
- **Effect**: +X to level of supported skill gems
- Level 1: No effect. Level 2: +1. Level 3: +2. Level 4 (corrupted): +3.
- **Critical for spell/minion builds** — each gem level is a major damage increase
- Drop-only gem, requires ~5× normal gem XP to reach level 3
- Corruption can push to level 4 (+3 levels) — expensive but extremely powerful
- Does NOT provide a "more" multiplier — but the gem levels it grants may exceed what any single "more" support provides for spells
- Only affects SKILL GEMS, not skills granted by items

### Enlighten Support
- **Effect**: Reduces mana cost/reservation multiplier of supported gems
- Level 1: 100% (no effect). Level 2: 96%. Level 3: 92%. Level 4 (corrupted): 88%.
- Used to fit more auras by reducing their reservation
- Primarily linked with auras, not damage skills
- Same drop-only and XP requirements as Empower

### Enhance Support
- **Effect**: +X% to quality of supported skill gems
- Level 1: No effect. Level 2: +8%. Level 3: +16%. Level 4 (corrupted): +24%.
- Niche — only valuable when the supported gem's quality bonus is particularly powerful
- Same drop-only and XP requirements as Empower

### Awakened Variants (Sunsetted but Still in Game)
- Awakened Empower/Enhance/Enlighten exist with a level cap of 4 (+3 levels at max for Empower)
- Drop from Uber Maven exclusively
- The Awakened support gem system was largely replaced by the Exceptional gem system in 3.28
- Existing Awakened gems still function but are no longer obtainable from most sources

---

## Trigger Gems & Mechanics

### Cast When Damage Taken (CWDT)
- Auto-casts linked spells when you take a CUMULATIVE amount of damage
- Damage threshold scales with gem level (higher level = more damage needed before trigger)
- **Level restriction**: Can only support skill gems up to a certain REQUIRED LEVEL based on CWDT's level
- Common setups:
  - **Low level CWDT (level 1-5)**: Triggers frequently. Link with low-level guard skill (Molten Shell, Steelskin) and utility (Tempest Shield, curse)
  - **High level CWDT (level 20)**: Triggers rarely but can support high-level skills
- **DO NOT level CWDT past your intended threshold** — right-click the "+" to dismiss level-ups
- Multiple CWDT setups can coexist (different link groups)
- CWDT has its own cooldown per link group

### Cast on Critical Strike (CoC)
- Linked spells trigger when you crit with a linked attack skill
- Base cooldown: **150ms** per spell (0.15 seconds)
- The cooldown is per SPELL, not per CoC gem — different linked spells have independent cooldowns
- Multiple copies of the SAME spell share a cooldown

**CoC Breakpoints (Critical Knowledge):**
Server ticks are 33ms. Cooldowns round up to the nearest tick. This creates breakpoints:

| Cooldown Recovery Rate | Effective Cooldown | Max Trigger Rate | Max APS |
|----------------------|-------------------|-----------------|---------|
| 0% (base) | 0.165s (5 ticks) | ~6.06/sec | 6.06 |
| 14%+ | 0.132s (4 ticks) | ~7.57/sec | 7.57 |
| 52%+ | 0.099s (3 ticks) | ~10.10/sec | 10.10 |

- **Any CDR between breakpoints is WASTED** — 13% CDR has the same effect as 0%
- Attack speed MUST NOT significantly exceed the trigger rate — going over causes missed procs
- It's better to be slightly BELOW the APS breakpoint than above it
- Awakened CoC grants CDR per level — at high level it provides enough to hit 14% breakpoint
- Cyclone is the most popular CoC attack due to consistent multi-hitting

### Cast on Melee Kill
- Triggers linked spells when you kill with a linked melee attack
- Less popular than CoC — requires kills, not just hits
- No cooldown breakpoint concerns

### Hextouch Support
- Linked attacks apply linked curses on hit
- 35% less curse effect penalty (see auras-reservation.md)
- Commonly linked with a fast-hitting attack to automate curse application

### Arcanist Brand
- Creates a brand that attaches to enemies and periodically triggers linked spells
- No curse effect penalty (unlike Hextouch and Blasphemy)
- Good for automating curse application at full effect

### Trigger Weapon Craft ("Trigger a Socketed Spell")
- Crafting bench mod on weapons: "Trigger a Socketed Spell when you Use a Skill, with a X second Cooldown"
- Auto-casts socketed spells in rotation
- Common automation: Desecrate + Offering + Curse in a trigger weapon
- All socketed spells share the weapon's trigger cooldown
- Cannot trigger Vaal skills, channelling skills, or reservation skills

---

## Vaal Skill Gems

### How They Work
- A Vaal gem grants BOTH the regular skill AND a Vaal (powered-up) version
- Vaal version requires souls to activate (collected by killing enemies nearby)
- Each Vaal skill has a soul cost and a "Soul Gain Prevention" timer (prevents rapid reuse)
- Vaal skills are extremely powerful burst abilities — save for bosses, breaches, dangerous rares

### Soul Mechanics
- Souls are gained when enemies die near you (within a radius)
- Boss kills grant more souls
- Soul gain prevention starts when you USE the Vaal skill (not when it becomes available)
- Soul gain prevention timer varies per skill (4-12 seconds typically)
- Cannot gain souls during soul gain prevention period
- Map mods can reduce/prevent soul gain

### Obtaining Vaal Gems
- Corrupting a regular skill gem with a Vaal Orb (random chance)
- Vaal side areas and Vaal skill gem rewards
- Some vendor from specific NPCs

### Key Limitation
- Vaal gems are CORRUPTED — cannot be modified with currency
- Cannot be vendored for the 20/20 quality recipe
- Quality and level must be set before corrupting

---

## Transfigured Gems (3.23+)

### What They Are
- Alternative versions of existing gems with modified mechanics
- Same base skill concept but changed behavior
- Examples: different projectile patterns, built-in conversion, altered AoE, changed scaling
- Can fundamentally change how a skill plays and builds around it

### How to Obtain
- Divine Font in the Labyrinth (end of each Lab difficulty)
- The font offers a choice of transfigured gem options
- Can also be traded between players

### Build Implications
- Always check if a transfigured version exists for your main skill
- Some transfigured gems enable entirely new build archetypes
- The "of [descriptor]" naming tells you what changed (e.g., "Fireball of Showering" changes projectile behavior)

---

## Tag System

### How Tags Work
Every gem has tags that determine what modifiers affect it:
- Tags are listed on the gem description
- Modifiers must match tags to apply: "% increased spell damage" only affects gems tagged "Spell"
- Some modifiers are generic: "% increased damage" applies to everything with damage
- Tags can be: Attack, Spell, Melee, Projectile, AoE, Fire, Cold, Lightning, Chaos, Physical, Duration, Minion, Critical, Bow, Wand, etc.

### Common Tag Mistakes
- **Herald of Thunder storms are SECONDARY damage** — not affected by "spell damage" or "attack damage"
- **Minion damage is THEIR damage** — your "% increased fire damage" doesn't affect minion fire damage (unless Spiritual Aid)
- **DoT from ailments has its own scaling** — "attack damage" doesn't scale bleed DoT (bleed scales with physical DoT multi, not attack damage)
- **"Damage with weapons" applies to attacks** — not spells, even if you hold a weapon
- **Totem/Mine/Trap damage modifiers** — these are specific and don't scale your direct damage
- **"Socketed gems" mods on weapons** — only affect gems literally in that weapon's sockets, not gems elsewhere

### Checking Tag Compatibility
Before linking a support to your skill:
1. Look at the support gem's description — it says what it supports (e.g., "Supports attack skills")
2. Check the skill gem's tags match what the support requires
3. If a support is greyed out or shows no effect in tooltip, tags probably don't match
4. Use Path of Building to verify — it highlights incompatible supports

---

## Gem Corruption

### Corruption Outcomes (Vaal Orb on a Gem)
Corrupting a skill gem has four possible outcomes:
1. **+1 to gem level** (e.g., level 20 → 21) — powerful, especially for spells/minions
2. **+23% quality** (if below 23%) or set to 23% quality — minor upgrade
3. **Transform into Vaal version** (if one exists) — gives both regular and Vaal skill
4. **No change** — gem becomes corrupted but stats are the same

All outcomes make the gem CORRUPTED — it can no longer be modified with currency.

### Strategy
- Level a gem to 20, use vendor recipe for 20% quality, level back to 20, THEN corrupt
- Best corruption: Level 21 with 20% quality (need luck — corrupt at 20/20, hope for +1 level)
- For Empower/Enlighten/Enhance: Corrupt at level 3 hoping for level 4 — massive upgrade
- Corrupted gems can still gain XP and level up if they have room
- Double corruption (Locus of Corruption in Temple of Atzoatl) can give TWO corruption outcomes simultaneously

---

## Awakened Support Gems

### What They Were
- Upgraded versions of regular support gems with stronger bonuses
- Originally dropped from Maven-witnessed map bosses and Maven herself
- Level 1-5, with level 5 often granting a bonus effect (like an additional mod)
- Example: Awakened Melee Physical Damage at level 5 grants "Supported Skills deal Intimidating Hit"

### 3.28 Changes
- The Awakened gem system has been largely replaced by the **Exceptional support gem** system
- Some Awakened gems became Exceptional gems with modified behavior
- Awakened Empower/Enhance/Enlighten still drop from Uber Maven specifically
- Existing Awakened gems continue to function in permanent leagues
- New Exceptional support gems drop from various endgame content and have "Greater" versions that override regular counterparts

---

## Practical Decision Framework

### Building Your Main 6-Link
1. **Slot 1**: Your main skill gem (active skill)
2. **Slots 2-6**: Support gems, prioritized by:
   - Highest "more" damage multiplier that applies
   - Verify tag compatibility
   - Consider gem swap for bosses (Conc Effect for clear → boss, GMP for clear → Slower Proj for boss)
   - Check mana cost — can you sustain casting?
   - Don't use restricting supports (Elemental Focus, Brutality) if they conflict with your build

### Gem Level Priority
- **Spell/minion main skill**: Maximize gem level above all else (+level gear, Empower)
- **Auras**: Level matters for effect strength, but mana cost also rises (especially flat reservation auras)
- **CWDT setup**: Keep at intended level — do NOT auto-level
- **Attack skills**: Level is less critical — weapon DPS matters more
- **Support gems**: Level increases "more" multiplier — worth leveling but less impactful than main skill level

### Utility Gem Setups
- **Movement skill**: Flame Dash, Shield Charge, Leap Slam, Whirling Blades (based on weapon type)
- **Guard skill in CWDT**: Molten Shell (armour builds), Steelskin (generic), Immortal Call (endurance charge builds)
- **Aura setup**: See auras-reservation.md for full breakdown
- **Curse application**: Self-cast, CWDT, Hextouch, Arcanist Brand, trigger weapon (see trigger section above)
- **Offering automation**: Desecrate + Offering in trigger weapon (necromancers)

### Quality Optimization
1. Use vendor recipe (level 20 gem + 1 GCP → level 1 / 20% quality) for all gems
2. Level them back to 20 during mapping
3. Check alternative quality versions — some are transformative
4. 20% quality on every gem in a 6-link is a meaningful total bonus
5. GCP is too expensive to add quality point-by-point — always use vendor recipe

### Common Mistakes
- Using Elemental Focus when you need ailments (shock, ignite, freeze)
- Using Brutality with elemental auras or heralds
- Not verifying support tag compatibility before investing
- Over-leveling CWDT beyond intended threshold
- Ignoring mana cost multipliers until the build can't sustain
- Thinking attack gem level matters as much as spell gem level
- Not checking transfigured gem variants before committing to a build
- Linking Empower to attack skills (minimal benefit vs a real "more" support)
