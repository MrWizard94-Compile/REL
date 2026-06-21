# Path of Building Literacy — Complete Reference

## What Is Path of Building (PoB)?

Path of Building (Community Fork) is a third-party offline build planner and the single most important tool for PoE build theory-crafting. It simulates your entire character — passive tree, gear, gems, flasks, buffs — and calculates accurate DPS, defense, and sustain numbers.

**Download**: Search "Path of Building Community Fork" — it's the actively maintained version (not the original by Openarl, which is outdated).

### Why PoB Matters
- In-game tooltips are WRONG for many builds — they miss support interactions, conditional damage, DoT calculations, and more
- PoB calculates actual DPS including: all "more" multipliers, conversion chains, penetration, crit calculations, ailment DPS, minion damage, impale, and conditional modifiers
- Every serious build guide includes a PoB link — import it to see the full picture
- You can plan gear upgrades BEFORE buying/crafting by simulating items in PoB
- You can compare two setups side-by-side to see which is actually better

---

## Core PoB Sections

### Skills Tab
- Shows all your skill setups (main skill + supports in each link group)
- **Main Skill Selection**: The dropdown at the top selects WHICH skill PoB calculates DPS for. Make sure the right one is selected.
- Each support gem shows its DPS contribution — if a support shows ~0% contribution, it's either incompatible or redundant
- Gem levels and quality are editable — useful for simulating upgrades

### Tree Tab
- Full passive skill tree editor
- Shows allocated points, pathing, jewel sockets, masteries
- You can search for nodes by name or stat
- Point counter shows how many points you've used vs how many are available
- **Power Report**: Ranks every unallocated notable by DPS per point — use this to find your next best passive upgrade

### Items Tab
- All equipped gear, jewels, flasks
- Import items from your character or create custom items
- **Edit items**: Click an item to modify it — add/remove mods, change values. Essential for simulating upgrades.
- **Create custom items**: Test hypothetical gear before buying/crafting
- **Jewel sockets**: Assign jewels to specific tree sockets

### Calcs Tab
- The detailed calculation breakdown
- Shows EVERY modifier affecting your character and how they combine
- Sections: Offense (DPS, hit damage, crit), Defense (life, ES, resistances, mitigation), Sustain (regen, leech), Misc
- This is where you debug problems — if a modifier isn't applying, this tab shows why

### Config Tab
- **THE MOST IMPORTANT TAB FOR HONEST DPS**
- Controls conditional modifiers: "Is enemy a Boss?", "Are you on Low Life?", "Do you have Frenzy Charges?", etc.
- Incorrect config = misleading DPS. See "Honest Configuration" section below.

### Notes Tab
- Free-text notes for the build
- Build guide authors often put leveling instructions, gear priority, and playstyle notes here

---

## Reading DPS Numbers Correctly

### Which DPS Number Matters?

PoB shows multiple damage numbers. The right one depends on your build:

**Hit-Based Builds (attacks, spells that hit):**
- Look at: **Total DPS** (includes crit averaging) or **Average Damage** × hits per second
- The "Combined DPS" at the top includes all sources — this is usually what you want
- For multi-hit skills (Barrage, Ball Lightning): multiply per-hit damage × number of hits per cast/attack

**DoT Builds (RF, ED, Bane, bleed, poison):**
- Look at: **Total DoT DPS** or the specific DoT line (Ignite DPS, Poison DPS, Bleed DPS)
- Hit DPS is irrelevant for pure DoT builds — a hit that deals 100 damage but ignites for 500k DPS/sec is fine
- For Poison: PoB shows "Total DPS inc. Poison" which accounts for stacking — this is your real number

**Ignite Builds:**
- Look at: **Ignite DPS** specifically
- The hit DPS doesn't matter — only the ignite it applies matters
- PoB calculates ignite from your biggest hit, which is correct

**Minion Builds:**
- Look at: **Combined Total DPS** (includes all active minions)
- Make sure the right minion types are enabled in the skills dropdown
- Check that minion count is set correctly (e.g., 11 zombies, 4 spectres, etc.)

**Impale Builds:**
- PoB now calculates impale DPS automatically
- Look at: **Total DPS inc. Impale** — this includes the impale stacking damage
- Make sure "Impale Stacks" is configured correctly in Config tab

### Numbers That Are Misleading

**Tooltip DPS (in-game)**: Almost always wrong. Doesn't account for many mechanics. Never trust it for build evaluation.

**Shaper DPS**: An old convention where people set the enemy to "Shaper/Guardian" in config. Now less meaningful because boss resistances and stats have changed across patches. Still used as a rough benchmark.

**"X million DPS" without context**: DPS depends heavily on config settings. 5M DPS with honest config is better than 20M with inflated config.

---

## Honest PoB Configuration

The Config tab is where DPS gets inflated or kept honest. Here's how to set it correctly:

### Enemy Settings

**"Is the enemy a Boss?"**
- For mapping DPS: Leave unchecked or set to "Standard" (normal monsters have lower resistances)
- For bossing DPS: Set to "Pinnacle Boss" (Shaper/Elder/Exarch/Eater/Maven — they have ~40-50% ele res, higher life)
- **Honest benchmark**: Use "Pinnacle Boss" for your bossing DPS number. This is the number that matters for endgame viability.

**Enemy Resistance Override:**
- PoB lets you manually set enemy resistances
- Don't set to 0% or negative unless your build genuinely reduces them that far (via curses, exposure, pen)
- Pinnacle bosses: ~40% ele res, ~25% chaos res as baseline (before your reductions)

### Conditional Buffs — Check These Carefully

**Frenzy/Power/Endurance Charges:**
- Only check "at maximum charges" if you have RELIABLE generation that works on bosses
- Blood Rage gives frenzy on kill — doesn't work on bosses with no adds
- If your only frenzy source is kill-based, UNCHECK for boss DPS
- Minimum charges from gear are always active — those are fine

**Flasks Active:**
- Only check flasks you can realistically keep up during the content you're measuring
- For mapping: all flasks active is fine (kill sustain)
- For bossing: only check flasks you can sustain (Pathfinder = all, most builds = maybe 1-2)
- Diamond Flask + Atziri's Promise both active adds significant DPS — are you sustaining them on bosses?

**Onslaught:**
- Check only if you have a permanent/reliable source (Raider, Silver Flask with good sustain, kill-based for mapping only)
- Don't check for boss DPS unless you have non-kill Onslaught

**"Is the enemy on Consecrated Ground?":**
- Only if your build creates Consecrated Ground reliably (Inquisitor, Bottled Faith, Zealotry)

**"Have you killed Recently?":**
- "Recently" means within 4 seconds
- Mapping: usually true. Bossing: usually FALSE (bosses take longer than 4 seconds between add spawns)
- Many conditional damage bonuses depend on "recently" — unchecking them for boss DPS is more honest

**"Are you on Low Life?":**
- Only relevant for Pain Attunement builds that intentionally reserve life below 50%
- Don't check unless your build actually operates at Low Life

**"Is enemy Intimidated?":**
- Only if your build applies Intimidate (Champion, specific gear mods, Unnerve from Exarch implicit)

**"Is enemy Covered in Ash / Frost / Lightning?":**
- Only if your build applies these debuffs (Chieftain for Ash, specific sources for others)

### The "Honest Boss DPS" Config
For a realistic endgame boss DPS number, use these settings:

1. Enemy: Pinnacle Boss
2. Charges: Only minimum charges + reliably sustained charges on bosses
3. Flasks: Only flasks with boss-sustainable charges (Flagellant's, Pathfinder passive, flask on crit)
4. "Recently" conditions: Unchecked (no recent kills on single-target boss)
5. Onslaught: Only if permanent source
6. All debuffs/buffs: Only if your build reliably applies them
7. This gives you your REAL boss DPS — use it to evaluate whether you can kill content

---

## Detecting PoB Warrior Inflation

A "PoB warrior" is someone who inflates their DPS number through unrealistic config settings, making their build look stronger than it actually performs. Here's how to spot it:

### Red Flags in a Build Guide PoB

**1. All flasks checked, including Diamond + Atziri's + unique flasks:**
- Ask: Can these be sustained on a boss? If the build isn't Pathfinder or doesn't have Flagellant's prefix, the answer is often no.

**2. Maximum Frenzy/Power charges checked without reliable boss generation:**
- If Blood Rage is the only frenzy source and there are no adds → charges won't be up on bosses
- If Power Charge on Crit is the source but crit chance is only 50% → charges might drop

**3. "Recently" conditions checked for boss DPS:**
- "Killed Recently" doesn't apply to most boss fights (no adds to kill)
- "Killed a Rare/Unique Recently" is almost never true mid-boss

**4. Enemy resistance set to 0% or negative:**
- Unless the build has enough curses + exposure + penetration to actually achieve this
- Check the math: -Conductivity (44%) + Exposure (-25%) + Pen (37%) = -106% from 40% base = genuine negative res. This is valid. But many builds just set enemy res to 0 without the investment.

**5. Custom modifiers in the item or config:**
- PoB lets you add custom modifiers to items. Check for suspicious lines like "100% more damage" or modifiers that don't exist on any real item.
- Import the build, then check each item for custom/phantom mods.

**6. Level 100 tree with 124 points:**
- Most players reach level 90-95. A level 100 tree has 5-10 extra points over what you'll actually have for weeks/months.
- Check what those extra points give — if removing 5-10 points kills the build, it's not realistic.

**7. Unrealistically expensive gear:**
- Mirror-tier items in every slot. If the build "requires" 500 Divines of gear to function, that's not a viable build for most players.

### How to Audit a PoB
1. Import the build
2. Go to Config tab → check what's ticked
3. Ask: "Is every ticked condition realistic for boss fights?"
4. Untick anything that isn't → see what DPS drops to
5. That remaining number is the REAL boss DPS
6. Check items for unrealistic mods or custom additions
7. Check if the tree uses level 100 — subtract 5-10 points for a realistic level 92-95 tree

---

## Using PoB to Plan Upgrades

### The "Swap Item" Method
1. Find your current DPS in PoB
2. Edit a gear piece with the mods you're considering buying/crafting
3. Check the new DPS
4. Calculate: (New DPS - Old DPS) / Old DPS = % improvement
5. Compare the % improvement to the cost of the upgrade
6. Buy the upgrade that gives the most DPS per Chaos spent

### The Power Report
- In the Tree tab, there's a "Power Report" button
- It ranks every unallocated notable by how much DPS it adds per point invested
- Use this to find your next best passive point allocation
- Also works for removing allocated nodes — shows which current nodes give the least

### The Comparison Feature
- PoB can manage multiple item sets and tree configurations
- Use "Manage Trees" to save different tree versions
- Use "Item Sets" to compare gear configurations
- Toggle between them to see exact DPS/defense differences

### Simulating +Gem Levels
For spell/minion builds, one of the most valuable PoB exercises:
1. Set your main gem to level 20
2. Note the DPS
3. Set it to level 21 → note DPS increase
4. Set to 22, 23, 24 → note each increase
5. This tells you EXACTLY how much +1 gem level is worth in DPS
6. Compare that to the cost of +1 level sources (weapon, amulet, Empower)
7. Often reveals that +1 gem level is worth more than any other single upgrade

---

## Common PoB Mistakes

### Build Import Mistakes
1. **Importing a character without updating tree**: PoB sometimes imports an old tree version. Verify the tree matches the guide.
2. **Missing jewels**: Jewel sockets might import empty even if the character has jewels. Check manually.
3. **Wrong main skill selected**: PoB defaults to alphabetical order, not your actual main skill. Select the right one.
4. **Aura/buff effects not applied**: Some auras need to be toggled on in the skills tab. Check that Determination, Hatred, etc. show as active.

### DPS Reading Mistakes
1. **Looking at per-hit damage instead of DPS**: A slow 2H slam build does 500k per hit at 2 APS = 1M DPS. A fast claw build does 50k per hit at 12 APS = 600k DPS. The slam build does more DPS despite lower APS.
2. **Ignoring ailment DPS for ailment builds**: If you're an ignite build, your hit DPS is irrelevant. Look at Ignite DPS.
3. **Not accounting for ramp-up**: Impale builds need 5-7 hits to reach full DPS. The "Total DPS inc. Impale" number is steady-state, not burst.
4. **Forgetting conditional DPS**: If 40% of your damage comes from "killed recently" bonuses, your boss DPS is 40% lower than the number shown.

### Config Mistakes
1. **Leaving "Is enemy a Boss?" unchecked**: Default is normal monster, which has ~0% res. Bosses have 40%+ res. Your DPS against bosses is much lower than shown.
2. **Checking all charges without sustain**: See PoB Warrior section above.
3. **Leaving enemy curse effect at 100%**: Boss curse penalties were removed in 3.20, but automated curse application (Hextouch, Blasphemy) has its own less-effect modifiers. Make sure these are reflected.

### Defense Reading Mistakes
1. **Looking at only total armour/evasion**: These numbers are meaningless without context. What matters is the % physical damage reduction AT A SPECIFIC HIT VALUE. PoB's "Estimated Physical Damage Reduction" is more useful.
2. **Ignoring effective HP**: A character with 5000 life + 40% phys reduction + 75% block has way more survivability than one with 7000 life + 0% phys reduction + 0% block. Look at "Effective Hit Pool" in Calcs.
3. **Not checking max hit taken**: PoB can show the maximum hit you can survive. Check this against the content you're running.

---

## PoB Benchmarks (Rough Guidelines)

These are approximate numbers for comfortable gameplay at each level. Measured with honest Pinnacle Boss config.

### DPS Benchmarks (Boss DPS, Honest Config)
- **Early mapping (T1-5)**: 100k+ is comfortable
- **Yellow maps (T6-10)**: 300k-500k
- **Red maps (T11-16)**: 500k-1M for comfortable boss kills, 1M+ for fast kills
- **Pinnacle bosses**: 1M minimum (slow but doable), 2-3M comfortable, 5M+ fast
- **Uber bosses**: 5M minimum, 10M+ comfortable
- **Simulacrum 30**: 3M+ with good defense, or 10M+ to brute force it

### Defense Benchmarks
- **Life**: 4000+ yellow maps, 4500+ red, 5000+ bosses (softcore)
- **Max Res**: 75% minimum. 76-78% is noticeable. 80%+ is strong.
- **Spell Suppression**: 100% is the goal if you're an evasion build. Below 100% the chance is unreliable.
- **Block**: 50%+ to feel it, 75% (cap) for block-focused builds
- **Armour**: 30k+ for meaningful phys reduction. 50k+ with Determination for comfortable red maps.
- **Evasion**: 30k+ for meaningful evasion chance. Combined with Grace.

### Sustain Benchmarks
- **Life regen**: 500+/sec for comfortable mapping (RF needs much more)
- **Leech**: Should show "leeching" almost always during combat
- **Mana sustain**: Main skill cost < mana recovery per second (check in Calcs tab)

---

## Practical Framework: How to Use PoB for Every Decision

1. **Before choosing a build**: Import 3-4 build guides into PoB. Set them all to honest Pinnacle Boss config. Compare DPS AND defenses. The build with the best balance at YOUR budget wins.

2. **Before buying gear**: Simulate the item in PoB first. If it doesn't improve DPS or defenses by a meaningful amount, don't buy it.

3. **Before allocating passives**: Check the Power Report. Allocate the highest-DPS-per-point node next. Don't guess.

4. **Before switching support gems**: Swap them in PoB first. Some gems that LOOK good provide less DPS than you think (Elemental Focus on an ailment build = disaster).

5. **When something feels wrong**: Import your character into PoB. Run the diagnostic checklist from diagnostics.md. Check if PoB shows any glaring issues (wrong supports, uncapped res, low life).

6. **When planning endgame**: Set PoB to Pinnacle Boss config. If DPS is below 1M with honest settings, you need more investment before attempting pinnacle bosses. If defenses show <4500 life, fix that first.
