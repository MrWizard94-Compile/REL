# Crafting — Complete Reference

## Item Modifier Fundamentals

### Prefixes and Suffixes
- Rare items can have up to 3 prefixes + 3 suffixes (6 total explicit mods)
- Magic items can have 1 prefix + 1 suffix (2 total)
- Normal items have no explicit mods
- Unique items have fixed mods (not craftable except for specific mechanics)
- You can check an item's mod breakdown by holding Alt over it in-game, or using PoB/trade macro

### Item Level (ilvl)
- Determines the HIGHEST TIER of mods that can roll on an item
- Higher ilvl = access to better mod tiers
- Key breakpoints: ilvl 68 (low maps), ilvl 75 (mid maps), ilvl 83 (T16 maps), ilvl 84-86 (pinnacle content)
- Example: Tier 1 life on body armour requires ilvl 86
- Check poedb.tw for exact ilvl requirements per mod tier
- **Higher ilvl is not always better** — higher ilvl also unlocks MORE mods, diluting the pool. For some crafting strategies, lower ilvl with fewer possible mods can be better.

### Mod Tags
- Every modifier has tags (e.g., Life, Fire, Attack, Caster, Physical, Speed)
- Tags enable targeted crafting via Harvest reforges and Fossil weighting
- Example: "% increased Maximum Life" has the Life tag → Pristine Fossil boosts it, Harvest "reforge with Life mod" guarantees at least one Life-tagged mod
- Use craftofexile.com or poedb.tw to see tags on specific mods

### Mod Groups
- Mods belong to "groups" — an item cannot have two mods from the same group
- Example: You can't have two different tiers of "% increased Maximum Life" — they're the same mod group
- Crafting bench mods also belong to mod groups — a bench craft can BLOCK mods from its group
- This is a core mechanic for advanced crafting (blocking unwanted mods)

---

## Basic Currency Crafting

### Currency Items and Their Effects

**Orb of Transmutation**: Normal → Magic (adds 1-2 mods)
**Orb of Augmentation**: Adds a mod to magic item (if it has room for one more)
**Orb of Alteration**: Rerolls a magic item's mods randomly
**Regal Orb**: Magic → Rare (adds 1 random mod, keeping existing mods)
**Orb of Alchemy**: Normal → Rare (adds 4-6 random mods)
**Chaos Orb**: Rerolls a rare item completely (new random mods)
**Exalted Orb**: Adds 1 random mod to a rare item (if there's an open slot)
**Divine Orb**: Rerolls the VALUES (not tiers) of existing mods. Extremely valuable currency.
**Orb of Annulment**: Removes 1 random mod from an item (risky — can remove the good one)
**Orb of Scouring**: Rare/Magic → Normal (removes all mods)
**Vaal Orb**: Corrupts the item — random outcome, item becomes unmodifiable afterward

### Basic Crafting Flow
1. **Alteration spam**: Roll magic item until desired 1-2 mods appear
2. **Regal**: Upgrade to rare (adds 1 mod — hope for something useful)
3. **Crafting bench**: Fill remaining slots with bench-crafted mods
4. This produces a functional 3-4 mod item cheaply

### When to Chaos Spam vs Alt-Regal
- **Chaos spam**: When you need many specific mods and don't care about perfection. Cheap but fully random.
- **Alt-Regal**: When you need ONE specific mod guaranteed, then build around it. More controlled.
- **Neither is efficient for endgame crafting** — Essences, Fossils, and Harvest are almost always better.

---

## Essence Crafting

### How Essences Work
- Using an essence on a Normal item creates a Rare item with ONE GUARANTEED MOD (the essence's mod) plus random other mods
- Using a high-tier essence on a Rare item rerolls it completely but guarantees the essence mod
- 25 different essence types, each guaranteeing a different mod
- The guaranteed mod depends on the ITEM SLOT (weapon vs armour vs ring etc.)

### Essence Tiers
From lowest to highest: Whispering → Muttering → Weeping → Wailing → Screaming → Shrieking → **Deafening**
- Only Deafening tier (highest) can reroll Rare items
- Lower tiers can only be used on Normal items
- Higher tiers give better versions of the guaranteed mod
- Essences can be upgraded 3-to-1 to the next tier

### Corrupted Essences (from Essence Monsters)
Four special essences only obtainable from corrupting essence monsters in maps:
- **Essence of Hysteria**: Grants unique "when hit" or "on kill" mods not available elsewhere
- **Essence of Insanity**: Grants unique trigger/automation mods
- **Essence of Horror**: Grants powerful unique mods (e.g., socketed gems supported by level 20 [support])
- **Essence of Delirium**: Grants unique DoT/decay mods
- These are expensive but provide ACCESS to mods you can't get any other way

### When to Use Essences
- When you NEED one specific mod and will work around whatever else rolls
- Great for resistance-capping rings/amulets (Essence of specific res type)
- Essential for crafting items with mods only available from essences
- Better than Chaos spam for targeted crafting
- Can be combined with metacrafting (lock prefixes → reroll suffixes) for advanced results

---

## Fossil Crafting

### How Fossils Work
- Socket 1-4 Fossils into a Resonator (1-4 socket depending on resonator type)
- Use the resonator on a Normal/Rare item → rerolls the item like a Chaos Orb, but with weighted mods
- Each fossil has two effects: it INCREASES weight of certain mod tags and DECREASES weight of others
- Some fossils grant access to EXCLUSIVE mods not available through other crafting methods
- Fossils IGNORE metamods like "Prefixes Cannot Be Changed" — they always reroll everything

### Key Fossils

**Pristine Fossil**: More Life mods, no Energy Shield mods. THE go-to for life-based crafting.
**Jagged Fossil**: More Physical mods, no Chaos mods. Great for physical weapons.
**Metallic Fossil**: More Lightning mods, no Physical mods. Lightning-specific crafting.
**Scorched Fossil**: More Fire mods, no Cold mods. Fire-specific crafting.
**Frigid Fossil**: More Cold mods, no Fire mods. Cold-specific crafting.
**Aberrant Fossil**: More Chaos mods, no Elemental mods. Poison/chaos crafting.
**Dense Fossil**: More ES mods, no Life mods. ES gear crafting.
**Corroded Fossil**: No Physical, no Attack mods. Good for caster items (removes unwanted mods from pool).
**Lucent Fossil**: More Mana mods, no Speed mods. Niche for mana builds.
**Bound Fossil**: More Minion mods. Core for minion gear crafting.
**Hollow Fossil**: Creates an Abyss socket on the item. Enables Abyss jewel socketing on gear.
**Perfect Fossil**: Rerolls item quality with a range of 15-30% (normally capped at 20%).
**Bloodstained Fossil**: Has a Corrupted implicit modifier. Enables corruption mods without Vaal Orb risk.
**Faceted Fossil**: More Gem Level mods. For +gem level weapons/shields.
**Glyphic Fossil**: Has a Corrupt Essence modifier. Extremely rare.

### Resonator Types
- **Primitive Resonator** (1 socket): Cheapest, use for single-fossil crafting
- **Potent Resonator** (2 sockets): Two fossils combined
- **Powerful Resonator** (3 sockets): Three fossils — powerful targeted crafting
- **Prime Resonator** (4 sockets): Four fossils — extremely rare and expensive

### When to Use Fossils
- When you want to WEIGHT the mod pool toward specific tags while REMOVING unwanted tags
- Example: Pristine + Jagged on a weapon = more Life + Physical mods, no ES + no Chaos mods
- Better than Chaos spam for any targeted crafting project
- First step for many advanced crafting projects (fossil for initial mods → metacraft to finish)
- Use craftofexile.com to simulate expected outcomes before spending

---

## Crafting Bench

### How It Works
- Located in your hideout
- Recipes are unlocked by finding them throughout the game (maps, Delve, Syndicate, etc.)
- Adds a CRAFTED modifier to an item (takes an open prefix or suffix slot)
- Crafted mods are generally weaker than dropped/rolled mods of the same type
- Only ONE crafted mod per item by default
- Items show crafted mods in a slightly different color

### Key Bench Recipes

**Offensive:**
- Flat added damage to attacks (by element)
- % increased damage
- Attack speed / Cast speed
- Critical strike chance / multiplier
- +1 to level of [type] gems (weapons)

**Defensive:**
- +maximum Life
- +maximum Energy Shield
- Elemental resistances
- Chaos resistance
- % increased Armour/Evasion

**Utility:**
- Movement speed (boots)
- % increased Mana Reservation Efficiency (helmets, specific types)
- Trigger socketed spells craft (weapons)

### Metacraft Bench Recipes (Advanced — Expensive)

**"Prefixes Cannot Be Changed"** (2 Divine Orbs):
- When you reroll the item (Harvest reforge, Orb of Scouring, etc.), prefixes are protected
- Core technique: Lock good prefixes → reroll suffixes with Harvest/Chaos/etc.
- Does NOT protect against Fossils or Essences — they ignore metamods

**"Suffixes Cannot Be Changed"** (2 Divine Orbs):
- Same but protects suffixes
- Lock good suffixes → reroll prefixes

**"Can Have Up To 3 Crafted Modifiers"** (2 Divine Orbs):
- Allows you to bench-craft up to 3 mods on one item instead of 1
- Called "multimod" — a crafting benchmark for many items
- The multimod itself takes a suffix slot, so you get multimod + 2 other crafted mods
- Total: 3 crafted mods (multimod + 2 chosen mods)

### Bench Crafting Strategy
1. Roll an item with 2-3 good natural mods
2. If item has open slots, bench-craft to fill them
3. For advanced items: use metacrafts to protect good mods while rerolling the rest
4. Multimod when you have 1-2 perfect natural mods and want to finish the item

---

## Harvest Crafting

### How Harvest Works
- Encounter Harvest groves in maps
- Kill monsters, collect Lifeforce (three colors: Yellow/Vivid, Purple/Wild, Blue/Primal)
- Spend Lifeforce on crafting options at the Harvest bench
- Options are randomized each encounter — not all crafts are always available

### Key Harvest Crafts

**Reforge with [Tag]** (e.g., "Reforge with at least one Life modifier"):
- Rerolls the item like a Chaos Orb, but GUARANTEES at least one mod with the specified tag
- RESPECTS "Prefixes/Suffixes Cannot Be Changed" metamods (unlike Fossils)
- This is enormous — lock prefixes, reforge for guaranteed tagged suffix

**Reforge [Tag] More Likely**:
- Same as reforge, but the tagged mod has 10× weight boost
- Even more targeted — much higher chance of hitting desired mod

**Augment [Tag]** (rare craft):
- Adds a mod with the specified tag to an item with an open slot
- Acts like a targeted Exalted Orb — extremely powerful
- Very rare to find — when you see one, use it wisely

**Reforge keeping Prefixes/Suffixes**:
- Rerolls one half of the item while keeping the other
- Similar effect to metamod + chaos, but doesn't cost 2 Divine Orbs

**Other useful Harvest crafts:**
- Change a mod's numeric values (like a targeted Divine Orb for one mod)
- Add/remove influence from an item
- Exchange currency types (e.g., convert Fossils to other Fossils)
- Reroll cluster jewels
- Enchant items with quality or socket bonuses

### Why Harvest Is So Powerful
- Harvest reforges RESPECT metamods — this is the key differentiator from Fossils/Essences
- This means: Lock prefixes with bench → Harvest reforge for targeted suffix = safe, repeatable crafting
- Harvest augments can add exactly the mod you need
- Combined with metacrafts, Harvest enables deterministic endgame crafting

---

## Influenced Items

### Conqueror Influences (Shaper, Elder, Hunter, Crusader, Redeemer, Warlord)
- Items dropped in influenced maps can have one of 6 influence types
- Influenced items can roll EXCLUSIVE mods not available on normal items
- Each influence type has its own exclusive mod pool (element-themed or defense-themed)
- Example: Hunter-influenced body armour can roll "% increased maximum Life" (prefix) — not possible on non-influenced
- Example: Shaper-influenced weapon can roll "Socketed Gems supported by Level 20 [Support]"

### Key Influence Mods by Slot (Selected Examples)
- **Helmet**: -9% elemental resistance to nearby enemies (Elder), +gem levels (Elder/Shaper)
- **Body Armour**: % max life as ES (Hunter), +1 curse (Hunter), frenzy charge on hit (Redeemer)
- **Gloves**: Slower proj/faster attacks for socketed gems (Elder/Shaper), culling strike (Hunter)
- **Boots**: Tailwind (Redeemer), Elusive (Hunter), cooldown recovery (Shaper)
- **Weapon**: Socketed gems supported by [Support] (Shaper/Elder), DoT multi (Hunter)
- **Ring/Amulet**: Curse on hit (various), +gem levels (various)

### Combining Two Influences (Awakener's Orb)
- Awakener's Orb: Destroys one influenced item and transfers its influence to another
- Result: Item with TWO influences and guaranteed one mod from each
- The rest of the mods are rerolled randomly
- Expensive but enables powerful dual-influence combinations
- Example: Hunter + Crusader body armour for % max life as ES + additional curse

### Eldritch Influences (Searing Exarch / Eater of Worlds)
- Apply to helmets, gloves, boots, and body armour
- Replace the item's IMPLICIT mods with Eldritch Implicits
- Two tiers of influence that compete for "dominance" on the item
- Use Eldritch currency (Embers for Exarch, Ichors for Eater) to add/upgrade implicits
- Can have BOTH Exarch and Eater implicits on the same item

**Eldritch Currency:**
- **Lesser/Greater/Grand/Exceptional Eldritch Ember**: Add/upgrade Searing Exarch implicit
- **Lesser/Greater/Grand/Exceptional Eldritch Ichor**: Add/upgrade Eater of Worlds implicit
- **Orb of Conflict**: 50/50 chance to upgrade the dominant implicit by one tier OR downgrade the non-dominant by one tier
- **Eldritch Chaos Orb**: Rerolls explicit mods while keeping Eldritch implicits
- **Eldritch Exalted Orb**: Adds an explicit mod — only adds prefix if Exarch dominant, suffix if Eater dominant

**Key Eldritch Implicits:**
- Helmet: Mana reservation efficiency, +level to specific gems
- Gloves: Unnerve on hit, fire/cold/lightning exposure on hit
- Boots: Cooldown recovery rate, action speed, ailment avoidance
- Body Armour: Various defensive and offensive options

### Synthesised Items
- Items with UNIQUE implicit mods not found on any normal base
- Obtained from Synthesis league content (Cortex boss, Delirium, etc.)
- Examples: +1 to level of all [type] skill gems as implicit, % increased movement speed as implicit
- Cannot be combined with Conqueror influences (mutually exclusive)
- Can be combined with Eldritch influences

### Fractured Items
- Items with one or more LOCKED mods that cannot be changed by any crafting method
- The fractured mod is permanent — scour, reroll, whatever, it stays
- This makes fractured items ideal bases for crafting: the fractured mod is your guaranteed start
- Example: Fractured "+1 to Level of All Physical Spell Skill Gems" on a weapon = guaranteed gem level, craft the rest
- Drop from various league mechanics

---

## Advanced Crafting Techniques

### The Lock-and-Reroll Technique
1. Craft or roll an item with good prefixes (or suffixes)
2. Bench craft "Prefixes Cannot Be Changed" (or "Suffixes Cannot Be Changed")
3. Harvest reforge for a guaranteed tagged mod on the unlocked half
4. Repeat step 2-3 until the unlocked half is satisfactory
5. This is the backbone of endgame crafting

### Veiled Mods and Aisling Craft
- Jun's Syndicate members drop items with "Veiled" mods
- Unveil at the crafting bench to choose from 3 random options
- Veiled mods are often STRONGER than bench-crafted mods of the same type
- Example: Veiled movement speed on boots = +35% (vs bench craft +25%)
- **Aisling T4 (Research)**: Adds a random veiled mod to an item. Powerful because veiled mods are stronger than bench.
- Combining Aisling with metacrafts: Lock prefixes → Aisling adds a veiled suffix → unveil for a strong suffix

### Recombinators (Legacy)
- Merge two items together, potentially keeping mods from both
- Extremely powerful but unpredictable — can create items impossible through other methods
- Originally from Sentinel league, may appear in some form in newer content

### Beastcrafting
- Sacrifice captured beasts at the Blood Altar in the Menagerie
- Various recipes: Split an item into two (rare), add/remove mods, create uniques, etc.
- Key recipe: "Split an item in two" — creates two copies with split mods (useful for duplicating expensive bases)
- Beastcrafting recipes require specific beast combinations

---

## Catalysts (Jewelry Quality)

- Apply to rings, amulets, and belts to add quality that INCREASES the effectiveness of specific mod categories
- 20% quality maximum
- Each catalyst type boosts a different category: Life, Resistance, Attribute, Physical, Elemental, Caster, Speed, etc.
- Example: Fertile Catalyst on a ring with +75 life → the life roll becomes more effective
- Catalysts are consumed on use (like Glassblower's Baubles for flasks)
- Quality is removed when the item is rerolled — apply catalysts AFTER crafting is done

---

## Practical Crafting Framework

### When to Craft vs When to Buy
- **Buy** when the item exists on trade at a reasonable price — crafting has variance and can cost more
- **Craft** when: the item you need is very specific, doesn't exist on trade, or crafting is demonstrably cheaper on average
- Use craftofexile.com to estimate crafting costs before starting
- Rule of thumb: If expected crafting cost > 70% of purchase price, just buy it

### Crafting by Budget Tier

**Budget (1-20c per item):**
- Essence spam for guaranteed key mod
- Alteration → Regal → bench craft for weapons
- Buy cheap fractured bases and essence/fossil them
- Bench craft to fill gaps

**Mid Budget (20c-5 divine per item):**
- Fossil crafting for weighted mod pools
- Harvest reforges for targeted mods
- Metacraft + Harvest lock-and-reroll
- Aisling veiled mod on final suffix/prefix

**High Budget (5+ divine per item):**
- Awakener's Orb for dual-influence
- Repeated metacraft + Harvest cycles
- Eldritch crafting for optimal implicits
- Veiled Orb for veiled mod addition
- Perfect Fossil for 30% quality weapons

### Essential Crafting Tools
- **craftofexile.com**: Simulate crafting outcomes, calculate odds, compare methods
- **poedb.tw**: Complete mod database, shows all possible mods by item base, ilvl, and influence
- **Path of Building**: Import items to verify whether a crafted mod actually helps your build
- **Trade site**: Compare crafting cost vs purchase price before committing

### Common Crafting Mistakes
1. **Not checking mod tags before Harvest/Fossil crafting**: If you don't know the tags, you can't target the right mods
2. **Using Fossils/Essences with metamods active**: They IGNORE "Prefixes/Suffixes Cannot Be Changed" — only Harvest respects them
3. **Overcrafting cheap items**: If an item costs 10c to buy, spending 50c trying to craft it is a waste
4. **Ignoring fractured bases**: A fractured item with the right locked mod is the best crafting base you can start with
5. **Applying catalysts before finishing crafting**: Catalysts are removed on reroll — apply LAST
6. **Not understanding mod groups**: Trying to roll two mods from the same group (impossible) or not using bench crafts to block unwanted groups
7. **Exalting items recklessly**: Exalted Orbs are better used as currency or for metacrafts than blindly slamming
