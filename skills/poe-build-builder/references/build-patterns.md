# Build Patterns & Archetypes — Complete Reference

## Core Scaling Philosophies

Every PoE build scales damage through one of these primary axes. Understanding which axis your build uses determines your gear priorities, tree pathing, and support gem selection.

### 1. Gem Level Scaling (Spells & Minions)
- Base damage comes from skill gem level → +gem levels are your primary DPS stat
- Gear priority: +1 to [type] gems on weapon/amulet, Empower support
- Tree priority: Life/defense, some increased damage clusters
- Scaling ceiling: Very high — each gem level adds substantial base damage
- Examples: ED/Contagion, Absolution, Raise Spectre, Bane, Spark
- **Key insight**: A level 24 spell does ~50% more base damage than level 20. Three +1 sources and Empower 3 gets you there.

### 2. Weapon DPS Scaling (Attacks)
- Base damage comes from weapon → weapon DPS is your primary stat
- Gear priority: Highest pDPS or eDPS weapon you can afford, flat added damage on rings/amulet
- Tree priority: Weapon-specific damage nodes, crit if applicable
- Scaling ceiling: Tied to weapon quality — massive jumps when upgrading weapons
- Examples: Cyclone, Lightning Strike, Tornado Shot, Blade Flurry
- **Key insight**: Going from a 300 pDPS weapon to a 500 pDPS weapon is a ~67% damage increase before any modifiers.

### 3. Hit Damage × Speed Scaling (DPS Builds)
- Total DPS = damage per hit × hits per second
- Both axes matter — stacking one without the other leads to diminishing returns
- Speed builds: Cyclone, Flicker Strike, CoC (speed feeds trigger rate)
- Big hit builds: Slam skills, Elemental Hit (fewer hits but each is massive)
- **Key insight**: If you have 500% increased damage and 100% increased attack speed, adding another 50% attack speed gives you more DPS than adding 50% increased damage (because speed is less saturated).

### 4. DoT Multiplier Scaling (Damage over Time)
- DoT DPS = base DoT × (1 + increased%) × (1 + DoT multi%) × more multipliers
- DoT multi is its own multiplicative category → best DPS/point investment for DoT builds
- Gear priority: +DoT multi on gear (suffix), +gem levels for base damage
- Tree priority: DoT multi clusters, specific element DoT nodes
- Examples: Righteous Fire, Essence Drain, Toxic Rain, Vortex, Poisonous Concoction
- **Key insight**: 30% DoT multi is far more valuable than 30% increased damage for DoT builds because DoT multi is in its own multiplier pool.

### 5. Ailment Scaling (Ignite, Poison, Bleed)
- Ailment damage is based on the HIT that applied it, but scales separately
- Hit damage modifiers that don't specifically say "with hits" may not apply to ailments
- Key stats: "damage with ailments," DoT multi, ailment duration, hit damage of the applying type
- Crit gives +50% DoT multi on the applied ailment
- Examples: Ignite builds (Fireball, Armageddon Brand), Poison (Blade Vortex, Venom Gyre), Bleed (Lacerate, Puncture)
- **Key insight**: Ailment DPS is calculated from the BIGGEST single ailment instance, not the sum (except Poison, which stacks). For Ignite: one big hit > many small hits.

### 6. Minion Scaling
- Minions use THEIR OWN stats — your damage mods don't apply (except Spiritual Aid)
- Key stats: Minion damage, minion speed, minion gem level, aura effect on minions
- Tree priority: Minion clusters, life/defense for yourself
- Gear priority: +minion gem levels, minion damage mods, trigger weapons for utility
- Examples: Raise Zombie, Skeleton Mages, Spectres, Absolution, Summon Raging Spirit
- **Key insight**: Your job as a summoner is to stay alive and buff/debuff. Minion gem levels do the heavy lifting. See minions.md for full details.

---

## Common Build Archetypes

### Physical Attack — Impale
**How it works**: Stack physical damage, use Impale to add ~50-125% more sustained DPS.
**Core gear**: High pDPS weapon, flat phys on rings/amulet, armour-based defenses.
**Core links**: Main attack + Impale Support + Melee Phys + Brutality + (flex) + (flex).
**Ascendancy**: Champion (Master of Metal), Slayer (overleech), Berserker (raw damage).
**Defense**: Armour + Determination + Fortify (Champion gets free). Endurance charges.
**Scaling priority**: Weapon pDPS > flat phys > increased phys% > impale effect > attack speed.
**Boss check**: Impale needs 5-7 hits to reach full damage → slow hitters ramp slower.
**Warning**: Brutality kills ALL non-physical damage. Don't use with elemental auras/heralds.

### Elemental Attack — Conversion
**How it works**: Start with physical damage, convert to elemental, scale the elemental portion.
**Core mechanic**: Phys → Cold (Hatred, gear) → Cold + Fire (Avatar of Fire, Cold to Fire support).
**Core gear**: High pDPS weapon + conversion sources (gloves, tree, support gems).
**Ascendancy**: Inquisitor (ignore res on crit), Elementalist (exposure), Raider (speed + ailment immunity).
**Why convert?**: Physical scales with both physical AND elemental modifiers after conversion. Double-dipping on modifier pools.
**Scaling priority**: Weapon pDPS > conversion% (100% is ideal) > elemental penetration > crit > added flat elemental.
**Warning**: Impale only works on the PHYSICAL portion before conversion. Full conversion = no impale.

### Elemental Spell — Crit
**How it works**: Scale spell gem level for base damage, invest in crit for massive multiplier.
**Core gear**: +gem level weapon/amulet, crit multi on gear, Bottled Faith flask.
**Core links**: Spell + Controlled Destruction or Increased Crit Damage + Elemental penetration + (flex).
**Ascendancy**: Inquisitor (Inevitable Judgement ignores res), Assassin (highest crit ceiling), Elementalist (ailment application).
**Defense**: Typically evasion/ES hybrid, or armour with Determination.
**Scaling priority**: Gem levels > crit chance to ~60%+ > crit multi > penetration > increased spell damage.
**Boss check**: Penetration or res-ignore is crucial. Bosses have 40-50% ele res baseline.

### Chaos DoT
**How it works**: Apply chaos damage over time effects that stack or persist. Scale with DoT multi and gem levels.
**Core skills**: Essence Drain + Contagion (ED/C), Bane, Soulrend, Blight, Toxic Rain.
**Core gear**: +chaos gem levels, chaos DoT multi on gear, Despair curse application.
**Ascendancy**: Occultist (Withering Presence +60% chaos DoT multi, Profane Bloom clear), Trickster (hybrid defense + DoT scaling).
**Defense**: ES or hybrid life/ES. Occultist Vile Bastion for ES regen.
**Scaling priority**: Gem levels > chaos DoT multi > increased chaos damage > Wither stacks on enemy (up to 15) > skill effect duration.
**Strength**: DoTs keep damaging while you dodge. Excellent for learning boss mechanics.

### Ignite
**How it works**: Land one big hit to apply a strong ignite, which deals 50% of the hit's base fire damage per second for 4 seconds (200% total).
**Core mechanic**: Ignite damage is set by the SINGLE BIGGEST hit. More hits don't stack — only refresh with a bigger ignite.
**Core skills**: Fireball, Armageddon Brand, Hexblast, Flame Surge, Divine Ire.
**Ascendancy**: Elementalist (Shaper of Flames — ALL damage ignites), Chieftain (fire conversion + fire damage).
**Core support**: Combustion, Deadly Ailments, Burning Damage, Swift Affliction, Ignite Proliferation.
**Scaling priority**: Base hit damage of fire type > fire DoT multi > increased burning/fire damage > ignite duration > combustion debuff.
**Key insight**: Elemental Focus KILLS ignite (cannot inflict ailments). Never use with ignite.

### Poison
**How it works**: Apply many poison stacks that each deal damage independently. Poisons STACK (unlike ignite).
**Core mechanic**: Each poison instance = 20% of combined physical + chaos damage per second for 2 seconds (40% total per stack). Stack many poisons.
**Core skills**: Blade Vortex, Venom Gyre, Poisonous Concoction, Cobra Lash, Plague Bearer.
**Ascendancy**: Pathfinder (poison prolif, flask sustain), Assassin (Toxic Delivery, Noxious Strike).
**Core support**: Deadly Ailments, Unbound Ailments, Void Manipulation, Added Chaos.
**Scaling priority**: Poison application speed (more stacks/sec) > increased poison damage > chaos DoT multi > poison duration > base hit damage.
**Key insight**: Fast-hitting skills are king for poison because stacks accumulate. A skill hitting 10 times/sec at low damage outperforms one hitting 2 times/sec at moderate damage.

### Bleed
**How it works**: Apply bleeding that deals physical DoT. Only the strongest bleed counts (doesn't stack like poison).
**Core mechanic**: Bleed = 70% of base physical damage per second for 5 seconds. Enemies moving take 50% more bleed damage (Crimson Dance changes this).
**Core skills**: Lacerate, Bladestorm, Puncture (bow), Earthquake.
**Ascendancy**: Gladiator (bleed explosions, block), Champion (impale + bleed hybrid is niche).
**Crimson Dance keystone**: Bleeds can stack (up to 8) but lose the "moving" bonus. Changes bleed from "one big hit" to "many hits."
**Scaling priority**: Base physical hit damage > physical DoT multi > bleed duration > increased physical damage > attack speed (with Crimson Dance).

### Minion Army
**How it works**: Summon many minions that attack independently. You support them with auras, offerings, and curses.
**Core skills**: Raise Zombie + Raise Spectre + Summon Skeletons or Skeleton Mages + Animate Guardian (utility).
**Ascendancy**: Necromancer (always). +2 gem levels from Unnatural Strength is irreplaceable.
**Core automation**: Trigger weapon with Desecrate + Flesh/Bone Offering + Vulnerability/Conductivity.
**Defense**: High block (Bone Offering via Mistress of Sacrifice), Determination, life/ES hybrid.
**Scaling priority**: Minion gem levels > minion damage > minion speed > aura effect > your own defense.
**Key insight**: Your gear is for YOUR survival. Minions scale from gem levels and aura effects, not your personal damage stats.

### Totem / Brand
**How it works**: Place totems or brands that cast skills for you. You stay at safe range.
**Core skills**: Freezing Pulse Totems, Holy Flame Totem, Ballista totems (attack), Storm Brand, Armageddon Brand.
**Ascendancy**: Hierophant (most totems, totem damage), Chieftain (fire totems).
**Defense**: Safe playstyle inherently (you're not in melee). Block or evasion depending on class.
**Scaling priority**: Totem damage > totem placement speed > number of totems > your own defense.
**Playstyle note**: Love-it-or-hate-it. Totems have AI and positioning quirks. Brands are smoother (auto-attach to enemies).

### Cast on Crit (CoC)
**How it works**: Attack with a fast weapon (usually Cyclone), crits trigger linked spells automatically.
**Core mechanic**: CoC has a 150ms base cooldown per spell. Server tick breakpoints determine actual trigger rate (see gem-system.md).
**Core links**: Cyclone + CoC + Spell 1 + Spell 2 (if room) + supports.
**Ascendancy**: Inquisitor (ignore res on crit), Assassin (crit ceiling), Scion (flexible).
**Critical requirement**: Must hit the APS breakpoint for your CDR bracket. Going over = lost procs.
**Core gear**: High crit weapon, CDR on belt/boots, accuracy if not Lycosidae/Resolute.
**Scaling priority**: Crit chance (must be near 100%) > CDR breakpoint > spell damage > attack speed (to breakpoint, NOT over).
**Warning**: This is one of the most gear-intensive archetypes. Not recommended for league start.

### Aura Stacker
**How it works**: Run 8-12+ auras simultaneously via heavy reservation efficiency investment. Each aura is scaled by increased aura effect.
**Core mechanic**: Reservation efficiency from tree + Enlighten 4 + gear → fit many auras. Aura effect scaling → each aura provides disproportionate buffs.
**Ascendancy**: Guardian (Radiant Faith for ES), Scion/Ascendant (tree start point flexibility), Champion (Inspirational).
**Core gear**: Reservation efficiency on gear (helmets, rings, amulet), Enlighten 4, March of the Legion or Prism Guardian.
**Defense**: Layer many defensive auras (Determination, Grace, Discipline, Purity of Elements).
**Scaling priority**: Reservation efficiency > aura effect > number of auras > individual aura level.
**Warning**: Extremely expensive. One of the highest investment builds. Not a league starter.

### RF (Righteous Fire)
**How it works**: Toggle on Righteous Fire — burns you and enemies around you. You regenerate more than the burn kills you.
**Core mechanic**: RF deals burning damage per second = % of your max life + ES as fire damage. You take 90% of that damage to yourself. Outsustain with regen.
**Ascendancy**: Inquisitor (Consecrated Ground regen + ailment immunity), Juggernaut (max life regen, tankiness), Chieftain (fire damage, fire res).
**Core gear**: Max fire res (reducing self-damage), life regen on gear, +gem levels.
**Defense**: High max fire res (reduce self-damage to trivial levels), life regen, endurance charges.
**Scaling priority**: Max fire res > life regen (must exceed self-damage) > max life (RF damage scales with it) > increased burning/fire damage > gem levels.
**League start friendly**: Yes — RF works with minimal gear. Just need to outpace the self-burn.

---

## League Start Planning

### What Makes a Good League Starter?
1. **Low gear dependency**: Works with self-found or cheap items through Acts and early maps
2. **Smooth campaign leveling**: Doesn't hit a wall at specific acts or require specific uniques to function
3. **Scales into maps**: Can handle T1-T10 maps without major gear upgrades
4. **Clear path to endgame**: Knows what gear upgrades to target and when
5. **Resilient to bad RNG**: Doesn't rely on one drop or craft to function

### League Start Tier List (General Principles)

**S-Tier Starters** (work every league):
- **Minion builds** (Necromancer): Gem levels scale cheap, minions don't need your gear to be good
- **DoT builds** (Occultist ED/C, Trickster): Damage ticks while you dodge, scales with gem levels
- **RF Inquisitor/Juggernaut**: Needs only fire res and regen to start, very tanky

**A-Tier Starters** (reliable with minor planning):
- **Champion impale melee**: Permanent Fortify carries bad gear, impale adds free damage
- **Saboteur mines/traps**: Traps are self-sufficient, blind + regen for defense
- **Elementalist ignite**: Shaper of Flames works with 1 point, scales with gem levels
- **Totem Hierophant**: Totems do the work, you stay safe

**B-Tier Starters** (work but have rough patches):
- **Lightning Strike Raider**: Needs a decent claw by maps, but Raider speed carries
- **Poisonous Concoction Pathfinder**: No weapon needed (!), flask sustain is free, but damage ceiling is moderate
- **Absolution Guardian/Necromancer**: Minion-based, but Absolution has a ramp-up learning curve

**Avoid for League Start**:
- CoC builds (need crit gear + CDR + accuracy)
- Aura stackers (need massive investment)
- Most bow builds (need expensive weapons)
- Int/attribute stackers (need specific rares everywhere)

### League Start Progression Milestones

**Acts 1-4** (levels 1-40):
- Use whatever skill feels smooth. Most builds use a leveling skill, not their final skill.
- Common leveling skills: Freezing Pulse, Stormblast Mine, Absolution, Splitting Steel, Caustic Arrow
- Get 3-link by Act 2, 4-link by Act 4
- Prioritize life and elemental resistances on gear
- Pick up every rare and ID it — look for life + res

**Acts 5-10** (levels 40-68):
- After Act 5 Kitava: You lose 30% all res. FIX THIS before continuing.
- After Act 10 Kitava: You lose another 30% all res (60% total penalty).
- Transition to your intended main skill around Act 3-6 depending on build
- Get your first ascendancy (Normal Lab around level 33-36)
- Cruel Lab around level 55-60
- Get a 5-link body armour (cheap from vendors or drops)

**Early Maps (T1-T5)** (levels 68-78):
- Cap all elemental resistances at 75% (after the -60% penalty = need 135% on gear)
- Get enough life to survive (4000+ for softcore, 5000+ for hardcore)
- Complete Merciless Lab for third ascendancy
- Start trading for your core unique items (if needed)
- Run maps alch-and-go (alch the map, run it, don't overthink mods)

**Mid Maps (T6-T10)** (levels 78-85):
- Upgrade weapon/gem levels — this is where DPS starts mattering
- Get a 6-link (buy or craft via Prophecy/div cards)
- Push for Eternal Lab (uber lab) for final ascendancy
- Start identifying which map mods your build CANNOT run (e.g., "no regen" kills RF)
- Begin Atlas passive investment

**Late Maps (T11-T16)** (levels 85-90):
- Gear upgrades become targeted — specific influenced mods, specific uniques
- Layer defenses properly (see defenses.md)
- Start bossing (Conquerors, Elder, Shaper)
- Currency generation becomes serious — fund your next upgrades via consistent mapping

### Build Progression: When to Pivot
- If your build feels bad at T5 maps → check resistances, life, and gem levels first (80% of "my build sucks" is gear/res)
- If damage is fine but you die constantly → add defensive layers (see diagnostics.md when available)
- If mapping is fine but bosses take forever → you may need a boss-specific setup (gem swap, flask swap, or second character)
- If you hit a wall at T14+ → this is normal. Endgame requires targeted investment. Identify your weakest link and upgrade it.

---

## Build Synergy Patterns to Recognize

### The Feedback Loop
A build mechanic that feeds itself:
- Kill → Frenzy charge → more damage → kill faster → more charges
- Herald of Ice shatter → chain explosions → more shatters
- Poison prolif → kill → spread → more kills
- When you see a loop, amplify it — that's your clear speed engine.

### The Threshold Breakpoint
A stat that does nothing until it reaches a critical mass, then transforms the build:
- 100% impale chance (missing impales breaks the stacking)
- Crit chance above 60% (below this, crit investment isn't worth it vs EO)
- Ailment threshold (need enough damage to actually shock/freeze bosses)
- Block chance (75% cap is where block becomes reliable)
- 100% elemental ailment avoidance/immunity
- When you're below a threshold, the investment feels wasted. Plan to hit it or don't invest at all.

### The Conversion Chain
Converting damage from one type to another lets you benefit from BOTH types' modifier pools:
- Physical → Cold → Fire: Benefits from phys, cold, AND fire modifiers
- Conversion only goes one direction (phys → ele → chaos, never backwards)
- 100% conversion is ideal — leftover unconverted damage is wasted potential
- Hatred (phys as extra cold) + fire conversion = triple-dipping on a single physical base

### The Automation Stack
Reducing manual actions to focus on core gameplay:
- Trigger weapon: Desecrate + Offering + Curse (3 skills automated)
- CWDT: Guard skill + utility automatically
- Arcanist Brand: Curse + Exposure skill automatically
- Movement skill: Flame Dash or Shield Charge for positioning only
- Goal: Your "rotation" should be 1-2 buttons max during mapping. Save complexity for bosses.

### The Defense Layer Cake
No single defense is enough. Layer multiple:
- Layer 1: Avoidance (evasion, block, dodge, spell suppression)
- Layer 2: Mitigation (armour, endurance charges, fortify, max res)
- Layer 3: Recovery (life regen, leech, ES recharge, life on hit)
- Layer 4: Prevention (ailment immunity, stun immunity, curse immunity)
- Each layer catches what the previous one missed. See defenses.md for full breakdown.

---

## Common Build Mistakes

### Offense Mistakes
1. **All increased, no more**: Stacking 800% increased damage is less effective than 400% increased + 3 "more" multipliers. Diversify multiplier types.
2. **Ignoring penetration/exposure**: Against bosses with 40%+ res, penetration is often your biggest DPS gain.
3. **Wrong support gems**: Using Elemental Focus on an ignite build. Using Brutality with elemental auras. Always read the restriction clause.
4. **Neglecting gem levels for spells**: +1 gem level on a spell build is often worth more than any single gear upgrade.
5. **Crit without commitment**: 30% crit chance with 200% crit multi is worse than Elemental Overload. Either invest fully or don't invest at all.

### Defense Mistakes
1. **Uncapped resistances**: #1 cause of death. You need 75% all ele res AFTER the -60% penalty. That means 135%+ on gear.
2. **No life/ES**: Damage nodes are tempting, but you need 4500+ life (softcore) or 5500+ (hardcore) by maps. ES builds need equivalent.
3. **Single defense layer**: "I have 50% evasion" isn't enough. You'll still get hit regularly. Add armour, suppression, or block.
4. **No chaos resistance**: -60% chaos res means chaos damage destroys you. Get at least 0% by maps, higher for endgame.
5. **Ignoring stun**: Low-life characters get stunned constantly without stun immunity or high stun threshold.

### Progression Mistakes
1. **Upgrading offense before defense**: If you die, your DPS is zero. Survive first, then optimize damage.
2. **Not reading map mods**: "Monsters reflect X% elemental damage" WILL kill elemental builds. Read before running.
3. **Hoarding currency instead of investing**: A 5c upgrade now is worth more than saving for a 5 divine upgrade later. Invest early and often.
4. **Skipping lab**: Ascendancy points are the biggest power spikes in the game. Do each lab difficulty as soon as you can.
5. **Trying to do everything with one character**: Some builds map well but boss poorly (or vice versa). Having a second character for the other role is efficient.
