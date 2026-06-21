# Build Diagnostics — Complete Reference

## How to Use This File

When a build "feels bad," the problem almost always falls into one of a few categories. This file maps SYMPTOMS to CAUSES to FIXES. Start with what you're experiencing, find the matching symptom, then work through the causes.

---

## Symptom: "I Keep Dying"

### Cause 1: Uncapped Elemental Resistances
**Check**: Character sheet → Resistances. Are all three at 75%?
**Why it matters**: Each 1% below cap = ~4% more elemental damage taken. At 50% fire res vs 75%, you take DOUBLE fire damage.
**Fix**: Replace gear with life + resistance rares. Use Two-Stone Rings, Amethyst Flask for chaos. Craft resistances on open suffixes via bench. See gear-slots.md.
**Priority**: THIS IS ALMOST ALWAYS THE PROBLEM FOR NEW PLAYERS. Fix this first before looking at anything else.

### Cause 2: Not Enough Life / Energy Shield
**Check**: Character sheet → Life total. Are you above 4000 in maps? 4500+ for red maps?
**Why it matters**: Low life pool means even mitigated hits kill you. No buffer for mistakes.
**Fix**: Get life on EVERY gear slot (prefix). Take more life nodes on tree. Aim for 160-180% increased max life from tree (softcore). See passive-tree.md for life balance.
**Benchmarks**: White maps: 3500+. Yellow: 4000+. Red: 4500+ (SC) / 5500+ (HC). Bosses: 5000+.

### Cause 3: Single Defense Layer
**Check**: What's your defense BESIDES life? If the answer is "nothing" or "just evasion," that's the problem.
**Why it matters**: Every defense layer has gaps. Evasion fails eventually (entropy system). Armour doesn't stop elemental. Block is probabilistic. You need MULTIPLE layers.
**Fix**: Add a second and third defense layer. Common combos: Armour + Block + Fortify. Evasion + Spell Suppression + Wind Dancer. ES + Block + Ghost Dance. See defenses.md for full layer cake.

### Cause 4: No Ailment Immunity
**Check**: Are you dying to: Freeze (stuck in place → hit), Shock (taking 50% more damage), Bleed (moving = death), Corrupted Blood (rapid stacking DoT)?
**Why it matters**: Ailments are multiplicative death amplifiers. Shock + hit = death. Freeze + follow-up = death. Bleed + movement = death.
**Fix**: Flask suffixes (of Heat, of Staunching, of Grounding). Purity of Elements aura (full ailment immunity for 35% reservation). Corrupted Blood immunity jewel corruption. Pantheon (Brine King for freeze, Shakari for poison). See flasks.md.

### Cause 5: No Stun Prevention
**Check**: Are you getting stun-locked? (Character freezes in place repeatedly from successive hits)
**Why it matters**: Each stun interrupts your actions. Multiple stuns in succession = stun-lock → death without being able to react.
**Fix**: Brine King Pantheon (prevents stun-lock). Unwavering Stance (cannot be stunned but can't evade). Juggernaut Unstoppable. Boot craft "Cannot be Stunned if you've used a Skill Recently." High life pool reduces stun chance naturally.

### Cause 6: Chaos Damage Vulnerability
**Check**: Chaos resistance on character sheet. If -60% or below, chaos damage destroys you.
**Why it matters**: Chaos damage bypasses Energy Shield (unless CI or Coruscating Elixir). At -60% chaos res, you take 160% of chaos damage.
**Fix**: Get chaos res on 2-3 gear pieces (rings, belt, amulet). Amethyst Flask. Aim for 0%+ by yellow maps, 30%+ by red maps.

### Cause 7: Dangerous Map Mods
**Check**: Did you READ the map mods before running? Reflect, no regen, -max res, extra crit, etc.
**Why it matters**: Some map mods are LETHAL for specific builds. Reflect kills self-damage builds instantly. No regen kills RF. -Max res makes elemental damage spike.
**Fix**: Read every map before running. Reroll maps with mods your build can't handle. Know your build's "cannot run" list.

### Cause 8: Boss Mechanics (Not Gear)
**Check**: Are you dying specifically to boss attacks, not trash mobs?
**Why it matters**: Most boss deaths are MECHANICAL — you got hit by an avoidable attack. No amount of gear fixes standing in the Searing Exarch beam.
**Fix**: Watch a boss guide video before attempting. Learn attack telegraphs. Practice dodging. Bring appropriate flasks (Ruby for fire bosses, Amethyst for chaos). See endgame-content.md for boss-specific tips.

---

## Symptom: "My Damage Is Too Low"

### Cause 1: Wrong Support Gems
**Check**: Are all 5 support gems actually providing "more" multipliers? Are tags compatible?
**Why it matters**: A support gem with incompatible tags gives ZERO benefit. One dead support in a 6-link is like running a 5-link.
**Fix**: Verify every support in Path of Building. Replace any support that shows 0% DPS contribution. Prioritize "more damage" supports over "increased damage" supports. See gem-system.md.

### Cause 2: Low Gem Levels (Spells/Minions)
**Check**: What level is your main skill gem? For spells and minions, gem level IS your base damage.
**Why it matters**: A level 18 spell does ~30% less damage than level 20. A level 20 does ~50% less than level 24. Each level is a massive base damage increase.
**Fix**: Level your gems to 20. Get +gem level mods on weapon and amulet. Use Empower support (level 3+ = +2 gem levels). See gem-system.md for +level stacking.

### Cause 3: Bad Weapon (Attacks)
**Check**: What's your weapon's pDPS or eDPS? For attack builds, weapon DPS is THE primary damage stat.
**Why it matters**: Going from a 300 pDPS to a 500 pDPS weapon is a ~67% damage increase BEFORE any modifiers. No passive tree or support gem change comes close.
**Fix**: Buy or craft a better weapon. Search trade by pDPS/eDPS. This is almost always the single highest-impact upgrade for attack builds. See gear-slots.md.

### Cause 4: No Penetration / Exposure
**Check**: Do you have any way to reduce enemy resistances? Penetration gems, exposure skills, curses?
**Why it matters**: Bosses have 40-50% elemental resistance. Without penetration, nearly half your damage is mitigated. With 40% penetration, you effectively deal ~67% more damage to bosses.
**Fix**: Add penetration support gem (Fire/Cold/Lightning Penetration). Apply exposure (Wave of Conviction, Frost Bomb, Elemental Army, Mastermind of Discord). Curse (Flammability, Conductivity, Frostbite). See auras-reservation.md for exposure mechanics.

### Cause 5: All "Increased," No "More"
**Check**: In PoB, what's your total "increased damage" vs how many "more" multipliers do you have?
**Why it matters**: 800% increased damage with 0 "more" multipliers = less DPS than 400% increased with 3 "more" multipliers. "Increased" is additive and suffers diminishing returns. "More" is multiplicative.
**Fix**: Replace "increased damage" sources with "more" sources. Support gems are the primary "more" source. Ensure your 5-6 supports each provide a "more" multiplier. See damage-pipeline.md.

### Cause 6: Crit Without Commitment (or EO Without Crits)
**Check**: What's your effective crit chance? If below 40% with crit investment, you're in no-man's-land.
**Why it matters**: Half-invested crit is worse than either full crit OR Elemental Overload. You spend points on crit that don't pay off, AND you miss the free 40% more from EO.
**Fix**: Either commit to crit (60%+ chance, 300%+ multi) OR take Elemental Overload (just need occasional crits). Don't sit in between. See crit-charges.md for the decision threshold.

### Cause 7: Missing Auras
**Check**: How much mana are you reserving? Are you running appropriate offensive AND defensive auras?
**Why it matters**: Auras are massive multipliers. Determination alone can double your armour. Hatred can add 36% of physical as cold. Zealotry adds more spell damage + crit.
**Fix**: Run at least 1 offensive aura + 1 defensive aura + Defiance Banner. Check auras-reservation.md for setup recommendations by archetype.

### Cause 8: Flask Downtime on Bosses
**Check**: Do your damage flasks run out during boss fights?
**Why it matters**: If your DPS is calculated with Diamond Flask + Atziri's Promise active but they're empty during the boss, your actual DPS is much lower.
**Fix**: Flagellant's flask prefix (gain charges when hit). Flask charge on crit from tree. Pathfinder passive generation. Don't rely on flasks for boss DPS if you can't sustain them. See flasks.md.

---

## Symptom: "Mapping Feels Slow"

### Cause 1: Not Enough AoE / Clear Mechanic
**Check**: Are you killing packs in 1-2 hits, or are stragglers surviving?
**Why it matters**: Map clear speed is determined by how quickly you eliminate entire packs, not single targets.
**Fix**: Add a clear mechanic: Herald of Ice shatters, Profane Bloom explosions, Gratuitous Violence bleed explosions, Ignite Proliferation, Plague Bearer. Increase AoE (tree nodes, Increased AoE support for mapping). Swap GMP in for clear, Slower Proj for bosses.

### Cause 2: Low Movement Speed
**Check**: Do you have 25-30% MS on boots? A Quicksilver Flask? A movement skill (Flame Dash, Shield Charge)?
**Why it matters**: Time spent walking between packs is time not killing. Movement speed is directly proportional to map completion time.
**Fix**: 25%+ MS boots (mandatory). Quicksilver Flask (mandatory). Movement skill on left click or bound to accessible key. Consider Onslaught (Silver Flask, Raider, kill-based). See flasks.md and gear-slots.md.

### Cause 3: Too Much Backtracking
**Check**: Are you full-clearing every zone? Going back for missed corners?
**Why it matters**: Maps have diminishing returns — the last 10% of monsters takes disproportionate time to find.
**Fix**: Don't full-clear. Follow the general map flow, kill what's in your path, and move to the boss. ~80% completion is the efficiency sweet spot. Learn common map layouts.

### Cause 4: Stopping to Loot Too Much
**Check**: Are you picking up every rare and identifying it?
**Why it matters**: In endgame, most rares are vendor trash. Time spent identifying = time not mapping.
**Fix**: Use a strict loot filter (NeverSink's "Semi-Strict" or "Strict" for red maps). Only pick up currency, 6-links, and filtered highlights. Loot filter saves hours per league.

### Cause 5: Mana Problems
**Check**: Are you running out of mana mid-pack? Stopping to regen?
**Why it matters**: If you can't cast your main skill continuously, your effective DPS drops to zero during mana gaps.
**Fix**: Mana leech (0.4% is usually enough), mana on hit (Clarity Watcher's Eye, rings), Clarity aura (low level), mana flask (if nothing else works), reduced mana cost craft on rings/amulet. Check mana multiplier of support gems — 6 aggressive supports can make costs unmanageable. See gem-system.md.

---

## Symptom: "Bosses Take Forever"

### Cause 1: Build Is Clear-Focused, Not Boss-Focused
**Check**: Is your build optimized for AoE/packs but lacks single-target?
**Why it matters**: Many clear skills (Tornado Shot, Chain setups, Prolif builds) have weak single-target by design.
**Fix**: Gem swap for bosses (Conc Effect in, Increased AoE out. Slower Proj in, GMP out). Use Vaal skills for burst. Consider a second character for bossing. Some builds genuinely can't boss well — that's OK, play to your build's strength.

### Cause 2: No Boss-Specific Debuffs
**Check**: Are you applying curses, exposure, Wither stacks (chaos DoT), marks on the boss?
**Why it matters**: A boss with Vulnerability + Conductivity + Lightning Exposure takes massively more damage than one with no debuffs.
**Fix**: Self-cast a curse for full effect (no penalty since 3.20 — see auras-reservation.md). Apply mark (Assassin's Mark for crit, Sniper's Mark for projectiles). Apply exposure via skill or Eldritch implicit. For chaos DoT: Wither totem for 15 stacks.

### Cause 3: Charges Lost on Bosses
**Check**: Do you have Frenzy/Power charges during mapping but lose them against bosses (no adds to kill)?
**Why it matters**: 3 Frenzy charges = 12% more damage. Losing them on bosses = 12% DPS drop at the worst possible time.
**Fix**: Use non-kill charge generation: Frenzy skill (on hit), Enduring Cry (no kill needed), minimum charges from gear, Farrul's Fur, Assassin's Mark quality (on-hit power charges). See crit-charges.md for full boss sustain solutions.

### Cause 4: Impale Not at Full Stacks
**Check**: If impale build — do you have 100% impale chance? How many hits to reach steady state?
**Why it matters**: Missing impales breaks the stacking rhythm. At <100% chance, you lose significant steady-state DPS.
**Fix**: Reach 100% impale chance (Impale Support + Dread Banner + tree). For slow hitters, accept the ramp time or switch to a faster-hitting skill for bosses. See crit-charges.md for impale math.

---

## Symptom: "Build Feels Clunky"

### Cause 1: Too Many Buttons
**Check**: How many active skills do you press during normal mapping? More than 2-3?
**Why it matters**: PoE mapping should be smooth: move + attack/cast + occasional utility. If you're pressing 5+ buttons per pack, the build is over-manual.
**Fix**: Automate utility with trigger setups. CWDT for guard skills. Trigger weapon for Desecrate + Offering + Curse. Arcanist Brand for curses. Instilling Orbs on flasks for auto-use. See utility-automation.md (when available). Goal: 1-2 buttons for mapping.

### Cause 2: Mana Sustain Issues
**Check**: Do you run out of mana frequently, forcing you to wait?
**Fix**: See "Mana Problems" under Mapping Feels Slow above. Same solutions apply.

### Cause 3: Animation Lock / Cast Speed
**Check**: Does your character feel "stuck" during attack/cast animations?
**Why it matters**: Long animations leave you vulnerable and slow down clear speed.
**Fix**: Increase attack/cast speed (tree, gear, support gems). Use Multistrike (attacks) or Spell Echo (spells) to front-load actions. Use movement skills (Flame Dash) to cancel animations. Channelling skills (Cyclone) avoid this problem entirely.

### Cause 4: Minion AI Problems
**Check**: Are your minions standing around, attacking the wrong targets, or not following you?
**Why it matters**: Minions with bad AI = zero DPS. They need to be where the enemies are.
**Fix**: Use Feeding Frenzy support (makes minions aggressive). Predator support (direct targeting). Convocation skill (teleports minions to you). Ensure minions have enough movement speed. Some minion types (Spectres) have better AI than others (Zombies).

### Cause 5: Totem/Brand Placement Friction
**Check**: Are you constantly repositioning totems or reattaching brands?
**Why it matters**: Every moment spent placing is a moment not dealing damage.
**Fix**: Totem placement speed (tree, gear, Hierophant). More totems = less repositioning needed. Brands: use Brand Recall to snap brands back. Storm Brand has better auto-attach than Armageddon Brand.

---

## Symptom: "I Can't Afford Gear Upgrades"

### Cause 1: Not Running Maps Efficiently
**Check**: How many maps per hour are you running? Are you sitting in hideout?
**Why it matters**: Currency comes from killing monsters. Every minute in hideout is a minute not generating income.
**Fix**: Alch and go. Don't over-roll maps. Pick a comfortable map layout and chain it. Use a strict loot filter. Sell in bulk (use trade site bulk tool). Map faster, think less.

### Cause 2: Overspending on Incremental Upgrades
**Check**: Did you buy a 50c ring that's only 5% better than your 5c ring?
**Why it matters**: Marginal upgrades drain currency that could go toward meaningful upgrades.
**Fix**: Focus spending on items that represent a SIGNIFICANT upgrade (>20% DPS or >500 life). Save up for the big purchases rather than buying 10 small sidegrades.

### Cause 3: Not Using Crafting Bench
**Check**: Does your gear have empty prefix/suffix slots? Are they bench-crafted?
**Why it matters**: An empty mod slot is wasted stats. The crafting bench provides cheap, guaranteed mods.
**Fix**: Craft life, resistances, or damage on every open slot. Cost: usually just a few Chaos Orbs worth of materials. See crafting.md.

### Cause 4: Ignoring Free Power Sources
**Check**: Have you done all labs? Anointed your amulet? Filled jewel sockets? Upgraded Pantheon?
**Why it matters**: These are massive power gains that cost nothing or very little.
**Fix checklist**:
- [ ] All 4 labs completed (8 ascendancy points)
- [ ] Amulet anointed (free notable passive)
- [ ] All tree jewel sockets filled (even cheap 1-5c jewels)
- [ ] Pantheon upgraded (Divine Vessel + specific boss maps)
- [ ] Mastery nodes allocated at every relevant cluster
- [ ] Quality on all gems (vendor recipe: level 20 gem + 1 GCP)

---

## The Universal Diagnostic Checklist

When ANYTHING feels wrong, run through this list in order. The problem is almost always in the first 5 items.

1. **Elemental resistances capped?** (75% all three after -60% penalty)
2. **Enough life/ES?** (4000+ for yellow maps, 4500+ for red, 5000+ for bosses)
3. **Main skill in 5-link or 6-link?** (with correct, compatible supports)
4. **Gem levels appropriate?** (level 19-20 for mapping, +levels for spells/minions)
5. **Weapon appropriate?** (decent pDPS for attacks, +gem levels for spells)
6. **All 4 labs done?** (8 ascendancy points allocated)
7. **Amulet anointed?** (free notable passive)
8. **Flasks crafted?** (bleed + freeze removal at minimum)
9. **At least 1 offensive + 1 defensive aura running?**
10. **Movement speed on boots + Quicksilver Flask?**
11. **Chaos resistance above -30%?** (above 0% preferred)
12. **Defensive layers beyond just life?** (armour/evasion/block/suppress/fortify)
13. **Jewel sockets filled?**
14. **Masteries allocated?**
15. **Pantheon selected and upgraded?**

If all 15 pass and you still feel weak, the problem is build design (wrong ascendancy, wrong scaling axis, fundamental archetype mismatch) — at that point, consult build-patterns.md or consider following an established build guide.

---

## Quick Diagnostic by Content Level

**Struggling in Acts**: You're undergeared. Get life + res on every slot. Use vendor recipe +1 gem wand. Get a 4-link.

**Struggling in White Maps (T1-5)**: Resistances aren't capped. Get them to 75%. Buy cheap resist gear.

**Struggling in Yellow Maps (T6-10)**: Missing defensive layers or gem levels are too low. Do Merciless Lab. Get a 5-link.

**Struggling in Red Maps (T11-16)**: Build needs real investment now. 6-link, proper weapon, layered defenses, full flask setup, Eternal Lab done. This is where "good enough" stops working.

**Struggling with Bosses**: Learn mechanics (watch videos). Add penetration/exposure/curses. Ensure flask sustain. Gem swap for single target.

**Struggling with Uber Bosses**: This is expected. These require 50+ Divine investment and mechanical mastery. Don't feel bad — most players never complete these.
