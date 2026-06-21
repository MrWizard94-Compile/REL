# Passive Skill Tree — Complete Reference

## Tree Overview

The passive skill tree is shared by all 7 classes. Each class starts at a different position on the tree. The tree contains ~1,300+ nodes including small passives, notables, keystones, masteries, and jewel sockets.

### Total Passive Points Available
- **99 points** from leveling (level 2 through 100)
- **22-24 points** from quest rewards (depends on bandit choice — see bandits-pantheon.md)
- **Total: ~121-123 points** for most builds
- Scion Ascendant can gain up to 5 additional points from ascendancy
- Scion Reliquarian can gain up to 5-6 additional points from ascendancy
- In practice, most builds use 110-120 points (many don't reach level 100)

### Respeccing
- **Orb of Regret**: Each orb grants 1 passive refund point
- **Quest refund points**: ~20 refund points from quest rewards throughout the campaign
- Can only refund one point at a time — must unallocate from the "edges" of your tree (can't remove a node that would disconnect other allocated nodes)
- Full tree resets are not possible — you must refund point by point
- Respeccing is expensive for large changes — plan your tree before allocating

---

## Tree Sectors and Class Starting Positions

The tree is roughly circular, divided into three attribute sectors with a central hub:

### North (Intelligence/Blue) — Witch, Templar (right edge), Shadow (left edge)
- Energy Shield, spell damage, elemental damage, minion stats, mana, crit for spells
- Key clusters: Spell damage, ES, minion damage, curse effect, lightning/cold/fire spell clusters

### Southwest (Strength/Red) — Marauder, Duelist (right edge), Templar (left edge)
- Life, armour, physical damage, melee, fire damage, endurance charges
- Key clusters: Life, armour, melee physical, two-handed, mace/axe/sword, fire, fortify

### Southeast (Dexterity/Green) — Ranger, Shadow (right edge), Duelist (left edge)
- Evasion, attack speed, projectile damage, crit chance/multi, frenzy charges, accuracy
- Key clusters: Evasion, bow, claw/dagger, projectile, crit, poison, flask, spell suppression

### Center (Scion) — Starting point for Scion
- The inner ring connects all class starting areas
- Scion starts at the very center with access to all directions
- Contains attribute nodes (+10 Str/Dex/Int) that serve as highways between sectors
- Several jewel sockets near the center are valuable (Might of the Meek, Unnatural Instinct)

### Hybrid Zones (Between Sectors)
- **Str/Int boundary (Templar area)**: Elemental damage, auras, totem, brand, mana reservation
- **Str/Dex boundary (Duelist area)**: Attack damage, leech, impale, block, dual wield
- **Dex/Int boundary (Shadow area)**: Crit, traps/mines, DoT, poison, evasion/ES hybrid

---

## Node Types

### Small Passives (Travel Nodes)
- Grant minor bonuses: +10 attribute, small % increased damage, small % life/ES
- Primarily used for PATHING — connecting your start to the clusters you want
- The +10 attribute nodes form "highways" that are the most point-efficient way to cross the tree
- **Efficiency tip**: Count travel nodes between clusters. If a cluster requires 5+ travel nodes to reach, evaluate whether it's worth the investment.

### Notable Passives
- Larger nodes at the end of clusters that grant significant bonuses
- These are the primary "targets" when planning a tree — you path TOWARD notables
- Examples: "Herbalism" (+life, +life regen), "Throatseeker" (+crit multi), "Whispers of Doom" (+1 curse)
- Allocating a notable in a cluster unlocks the cluster's Mastery (see below)

### Keystone Passives
- Major game-changing nodes that fundamentally alter character mechanics
- Always have both a significant upside AND a significant downside
- Key examples:
  - **Resolute Technique**: Can't miss, can't crit
  - **Elemental Overload**: 40% more ele damage on crit, but crits deal no extra damage
  - **Mind over Matter (MoM)**: 40% of damage taken from mana before life
  - **Chaos Inoculation (CI)**: Immune to chaos damage, maximum life is 1
  - **Pain Attunement**: 30% more spell damage on Low Life
  - **Iron Reflexes**: Evasion rating is converted to armour
  - **Ghost Dance**: Gain Ghost Shrouds that recover ES when hit
  - **Crimson Dance**: Bleeds can stack, but no moving bonus
  - **Avatar of Fire**: 50% of non-fire converted to fire, deal no non-fire damage
  - **Eldritch Battery**: ES protects mana instead of life
  - **Zealot's Oath**: Life regen applies to ES instead
  - **Vaal Pact**: Life leech is doubled but life regen is zero
  - **Ancestral Bond**: Can't deal damage with skills yourself, +1 totem
  - **Necromantic Aegis**: Shield stats apply to minions instead of you
- Some keystones are only available via Timeless Jewels (see jewels.md)
- Plan around keystones early — they shape your entire build

### Jewel Sockets
- 21 sockets total on the tree: 15 regular + 6 Large (for cluster jewels)
- Allocating a socket costs 1 passive point but grants no stats by itself
- Value comes entirely from the jewel you socket into it
- Regular sockets accept: Normal jewels, Abyss jewels, Timeless jewels, unique jewels
- Large sockets (outer ring): Accept only Large Cluster Jewels
- See jewels.md for full jewel details

---

## Mastery System

### How Masteries Work
- Most passive clusters (outside class starting areas) contain a Mastery node
- After allocating a NOTABLE in that cluster, you can allocate the Mastery for 1 additional point
- Each mastery offers a CHOICE of several thematic bonuses (pick one)
- The mastery category is determined by the cluster type (e.g., Fire cluster → Fire Mastery)

### Key Rules
- **One bonus per mastery node**: You pick one option from the list when allocating
- **Same bonus can't be taken twice**: If you pick "Determination has 25% increased Reservation Efficiency" from one Armour Mastery, you can't pick it again from another Armour Mastery
- **Different bonuses from same category CAN be taken**: You can take two different Armour Mastery bonuses from two different Armour clusters
- **Requires connected notable**: Anointed notables, Thread of Hope notables, and other "unconnected" allocations do NOT unlock masteries
- **Costs 1 passive point**: The mastery itself costs a point on top of the notable

### Powerful Mastery Examples by Category

**Life Mastery:**
- +50 to maximum Life
- 10% increased maximum Life, 10% reduced maximum Energy Shield
- 15% increased maximum Life if there are no Life Modifiers on Equipped Body Armour

**Armour Mastery:**
- Determination has 25% increased Mana Reservation Efficiency
- You take 30% reduced Extra Damage from Critical Strikes

**Evasion Mastery:**
- Grace has 25% increased Mana Reservation Efficiency
- +15% chance to Suppress Spell Damage

**Spell Suppression Mastery:**
- Chance to Suppress Spell Damage is Lucky (rolls twice, takes better result)

**Elemental Mastery:**
- Hits have 25% chance to treat Enemy Monster Elemental Resistance as Inverted (EXTREMELY powerful — effectively turns 50% res into -50% res on proc)

**Leech Mastery:**
- 10% of Leech is Instant (provides instant recovery alongside normal leech)

**Fire/Cold/Lightning Mastery:**
- Element-specific penetration, damage bonuses, ailment scaling
- Exposure application methods
- Reservation efficiency for element-specific auras

**Minion Mastery:**
- Minions have +100% to Critical Strike Multiplier
- Minions Leech 1% of Damage as Life

**Crit Mastery:**
- +3 to Level of all Critical Support Gems
- +25% to Critical Strike Multiplier against Unique Enemies

### Mastery Strategy
1. When pathing to a notable, check if the cluster's mastery has a useful option
2. One extra point for a powerful mastery is often the best single-point investment on the tree
3. Plan masteries in PoB — they're easy to overlook but add significant power
4. Some masteries are build-defining (Spell Suppression Lucky, Elemental Resistance Inversion)

---

## Anointments

### How Anointing Works
- Combine 3 specific Oils (dropped from Blight encounters) at the Anointing bench
- Apply to an AMULET to gain any Notable passive from the tree WITHOUT allocating it
- The notable does NOT need to be connected to your tree
- Each notable requires a specific combination of 3 oils (check poedb.tw or PoB for recipes)

### Why Anointments Matter
- You gain a FULL notable passive for free — no passive points spent
- Can grab notables from the opposite side of the tree
- Some notables are only practical via anointment (too far to path to)
- This is essentially a free notable that doesn't cost any passive points

### Key Rules
- **Amulet only**: Only amulets can be anointed with tree notables (rings and other slots have different anoint effects)
- **One anoint per amulet**: Anointing replaces any previous anoint
- **Does NOT unlock mastery**: Since the notable isn't connected to your tree, you can't take the cluster's mastery
- **Works on unique amulets**: You can anoint unique amulets too
- **Allocates the notable**: The notable counts as "allocated" for purposes of radius jewels and other effects

### Oil Tiers (Cheapest to Most Expensive)
Clear, Sepia, Amber, Verdant, Teal, Azure, Indigo, Violet, Crimson, Black, Opalescent, Silver, Golden

- Cheap notables use 3 low-tier oils (Clear/Sepia/Amber)
- Expensive notables use high-tier oils (Silver, Golden)
- The most powerful notables often require Golden Oils

### Popular Anointments
- **Whispers of Doom** (+1 curse limit): Extremely popular — saves many passive points
- **Tranquility** (increased damage based on max ES): Popular for ES/damage builds
- **Heart of Thunder/Ice/Flame** (elemental penetration notables): Strong for elemental builds
- **Charisma** (reservation efficiency): Helps fit more auras
- **Constitution** (+life): Good defensive option
- **Corruption** (chaos damage + wither): Chaos DoT builds
- Always check what the best anoint is for your specific build in PoB

### Ring Anointments (Blight-Specific)
- Rings can be anointed too, but with different effects (Blight tower enhancements)
- These affect Blight encounters only — not general gameplay
- Less universally important than amulet anointments

---

## Tattoos

### How Tattoos Work
- Tattoos transform existing allocated passive nodes into different passives
- Most tattoos replace +10 attribute nodes (the travel/highway nodes)
- Some tattoos replace +30 attribute notables
- Up to 50 tattoos can be applied per character
- Obtained from Legion encounters and related content

### Tattoo Types
- **Attribute tattoos**: Replace a +10 attribute node with a different small bonus (e.g., replace +10 Str with +5% fire resistance)
- **Functional tattoos**: Replace attributes with utility (e.g., replace +10 Dex with +2% movement speed)
- **Keystone tattoos**: Some unique tattoos grant keystone-like effects

### Practical Usage
- Tattoos are primarily a min-max endgame system
- Most impactful when you have many +10 attribute nodes that you'd like to be something else
- Common use: Replace unneeded attribute nodes with resistances, life, or damage
- Budget: Most tattoos are cheap individually, but applying 20-30 adds up

---

## Runegrafts

### How Runegrafts Work
- Runegrafts replace an allocated Mastery passive with a different effect
- Each Runegraft provides a unique modifier not found in normal mastery options
- Only one of each Runegraft type can be applied
- Applied by right-clicking the Runegraft item then clicking an allocated mastery
- Introduced in 3.26, expanded in 3.27-3.28

### Why They Matter
- Some Runegraft effects are extremely powerful and not available elsewhere
- They transform a mastery point you've already spent into something potentially better
- Check available Runegrafts each league — the pool changes

---

## Tree Planning Principles

### Efficiency: Points Per Power
The fundamental tree planning question: "Is this cluster worth the travel cost?"

**Good investments** (2-3 travel nodes to a notable):
- Core damage clusters matching your build
- Life/ES clusters near your pathing
- Jewel sockets with good jewels

**Questionable investments** (4-5 travel nodes):
- Clusters far from your natural path
- Clusters that only provide "increased" damage when you already have lots
- Niche utility clusters

**Bad investments** (6+ travel nodes):
- Anything requiring extensive travel just for one notable
- Consider anointment or Thread of Hope instead

### The "Life vs Damage" Balance
- **Softcore rule of thumb**: ~160-180% increased maximum life from tree for mapping, more for bossing
- **Hardcore rule of thumb**: ~200%+ increased maximum life from tree
- ES builds: Equivalent ES investment from tree + gear
- After reaching your life target, remaining points go to damage
- Most builds take too much damage and not enough life during planning — always add more life than you think

### Pathing Strategies

**Hub-and-spoke**: Start from class area, path outward to specific clusters, return to hub for next cluster. Most common pattern.

**Highway pathing**: Use +10 attribute highways to cross from one area to another cheaply. The Str/Dex/Int highways can save many points vs going through clusters.

**Cluster jewel substitution**: Instead of pathing far for tree notables, invest in cluster jewels that provide the same or better bonuses in fewer points. Often more efficient for builds that need specific stat combinations.

**Thread of Hope**: Socket in a jewel socket, grab nearby unconnected notables. Can save 5-10 travel points. Trade-off: -10 to -20% all ele res.

### Common Planning Mistakes
1. **Too many damage clusters, not enough life**: Your tree needs a balance. Use PoB to check.
2. **Inefficient pathing**: Taking 5 small nodes to reach one mediocre notable. Count your travel nodes.
3. **Ignoring masteries**: Free power for 1 point each. Always check what masteries are available along your path.
4. **Forgetting anointment**: One free notable on your amulet. Don't leave it empty.
5. **Not using jewel sockets**: Even cheap jewels outperform most individual passive nodes.
6. **Overvaluing one area of tree**: It's often better to take 80% of each important cluster than 100% of one and 0% of another. Diminishing returns.
7. **Not verifying in PoB**: The tree tooltip DPS doesn't account for many mechanics. Always verify your tree in Path of Building.

---

## Practical Decision Framework

### Building a Tree from Scratch
1. **Start with your class position and ascendancy** — this determines your general tree direction
2. **Path to core notables** for your damage type (use PoB to identify which notables provide the most DPS)
3. **Ensure sufficient life/ES** — aim for 160-180% increased max life from tree (softcore) or equivalent ES
4. **Pick up jewel sockets** along your path (4-6 sockets is typical)
5. **Allocate masteries** at every cluster you path through that offers a useful option
6. **Check keystone needs** — if your build requires a keystone (CI, MoM, EO, RT), path to it early
7. **Evaluate cluster jewel setup** — would a Large cluster + Mediums be more efficient than distant tree notables?
8. **Anoint your amulet** — pick the best notable you can't efficiently path to
9. **Consider Thread of Hope** — would one save enough travel points to be worth the res penalty?
10. **Final check**: Verify in PoB that your defenses, damage, and sustain all meet minimum thresholds
