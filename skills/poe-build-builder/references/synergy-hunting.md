# Synergy Hunting — Complete Reference

## What Is Synergy Hunting?

Synergy hunting is the art of finding non-obvious interactions between PoE's mechanics, items, skills, and passive nodes that combine to produce effects greater than the sum of their parts. This is where PoE build theory-crafting transcends "follow the guide" and becomes genuine creative engineering.

The best builds in PoE aren't the ones with the most raw stats — they're the ones where every piece reinforces every other piece. This file teaches you how to think about finding those reinforcements.

---

## The Five Types of Synergy

### 1. Feedback Loops (Self-Reinforcing Cycles)
A mechanic that feeds back into itself, creating escalating power:

**Pattern**: Action A → Result B → Enables more of Action A → More of Result B → ...

**Examples:**
- **Herald of Ice chain**: Kill frozen enemy → HoI shatters nearby → cold damage freezes nearby → they shatter on death → chain continues across screen
- **Poison proliferation**: Poison enemy → kill → poison spreads (Pathfinder) → kills nearby → spreads further → pack evaporates
- **Frenzy charge mapping**: Kill → frenzy charge → more damage → kill faster → charges never drop → permanent uptime
- **Overleech + damage**: Take damage → leech overflows to buffer → survive next hit → leech more → always have a life buffer
- **Flask sustain loop**: Kill → flask charges → flask effect → more damage → kill faster → more charges → permanent flask uptime

**How to find them**: Ask "What happens AFTER I kill an enemy? Does the kill enable more kills?" Any on-kill effect that improves your ability to get more kills is a feedback loop.

### 2. Mechanical Bridges (Connecting Unrelated Systems)
An item, passive, or mechanic that makes two normally unrelated systems interact:

**Pattern**: System A doesn't normally affect System B, but Item/Passive C makes them interact.

**Examples:**
- **Spiritual Aid** (passive): Minion damage modifiers now also apply to YOUR damage. Bridges minion scaling → player scaling.
- **Iron Will** (support/keystone): Strength bonus to melee damage now applies to spell damage. Bridges attribute → spell scaling.
- **Crown of Eyes** (unique helmet): Increases to spell damage also apply to attacks at 150% value. Bridges spell scaling → attack scaling.
- **Doryani's Prototype** (unique body): Enemy lightning resistance equals YOUR lightning resistance. Bridges your defense stat → enemy vulnerability.
- **Storm Secret** (unique ring): Herald of Thunder triggers on SHOCK (not kill). Bridges ailment application → herald activation.
- **Necromantic Aegis** (keystone): Shield stats apply to minions, not you. Bridges shield defense → minion scaling.
- **Shaper of Flames** (Elementalist): ALL damage types can ignite. Bridges lightning/cold/physical → fire ailment.

**How to find them**: Read unique items and keystones that say "X also applies to Y" or "X instead of Y." These are GGG explicitly creating bridges between systems. Every "also" or "instead" is a potential synergy.

### 3. Threshold Convergence (Multiple Stats Reaching Critical Mass Together)
When investing in one stat simultaneously pushes multiple mechanics past their thresholds:

**Pattern**: Stat X benefits Mechanic A, Mechanic B, AND Mechanic C. Investing in X gives triple returns.

**Examples:**
- **Intelligence stacking**: Int gives ES (defense), spell damage (offense via Transfiguration), satisfies gem requirements, and some items scale with total Int (Whispering Ice, Int stacker builds). One stat = four benefits.
- **Attack speed stacking**: More attacks → more hits → more impale stacks faster → more poison stacks → more CoC triggers → faster leech → faster movement (Shield Charge). Speed feeds EVERYTHING.
- **Armour stacking**: Armour reduces physical hits (defense), Molten Shell absorbs based on armour (guard skill), armour mastery converts to other stats, Transcendence makes armour reduce elemental (with Militant Faith keystone). One defensive stat → multiple defensive layers.
- **Gem level stacking**: +levels on spells increase base damage (offense), increase aura effect (utility), increase minion stats (minion builds), and can even increase skill duration. One source → cascading benefits.
- **Crit chance investment**: Higher crit → more damage (crit multi), guaranteed ailments on crit (shock/freeze/ignite), +50% DoT multi on crit ailments, Elusive generation (Assassin), power charge generation (PCoC), flask charge generation (crit flask charge). Crit feeds offense AND utility.

**How to find them**: When you see a stat that appears in multiple formulas (damage, defense, utility), that's a convergence point. Stack it.

### 4. Conditional Chaining (Triggering Cascading Effects)
When one action triggers a condition that triggers another effect, which triggers another:

**Pattern**: Action → Condition 1 met → Effect 1 fires → Condition 2 met → Effect 2 fires → ...

**Examples:**
- **CWDT chain**: Take damage → CWDT triggers Molten Shell (defense) + Wave of Conviction (exposure) + Blade Blast (damage) — one damage event → three defensive/offensive effects
- **HoT + Storm Secret + Doryani's Catalyst**: Hit enemy → shock → HoT storm activates (Storm Secret) → storm hits nearby → Elemental Proliferation (Catalyst) spreads shock to pack → HoT storms activate on THEM → chain continues
- **Kill → multiple on-kill effects**: Kill enemy → Profane Bloom explosion (clear) + Frenzy Charge (damage) + Onslaught (speed) + Herald of Ice shatter (chain clear) + flask charges (sustain). One kill = five simultaneous benefits.
- **Asenath's Gentle Touch gloves**: Kill cursed enemy → corpse explodes → explosion can kill nearby → those corpses explode → chain reaction. The curse from the gloves + explosion + Temporal Chains slowdown = entire screen melts.

**How to find them**: Map out your "on hit," "on kill," "on crit," and "when hit" triggers. How many of these fire simultaneously? Can you add more? Each additional trigger is multiplicative clear speed.

### 5. Inverse Scaling (Turning Weaknesses Into Strengths)
Mechanics that make a normally bad stat beneficial:

**Pattern**: Stat X is normally a downside, but Mechanic Y makes it an upside.

**Examples:**
- **Doryani's Prototype**: Normally, low lightning resistance = you take more lightning damage. With Prototype, YOUR lightning resistance is applied to ENEMIES. Tank your own lightning res to -200% → enemies have -200% lightning res → astronomical damage. Your "weakness" becomes their weakness.
- **Pain Attunement + Low Life**: Being at low life is normally dangerous. Pain Attunement gives 30% more spell damage while on low life. Reserve life with auras (Arrogance Support) to intentionally stay at low life → danger becomes power.
- **Chaos Inoculation**: Maximum life becomes 1. Normally lethal. But: immune to chaos damage, and now ALL your "% increased maximum life" investment can go to ES instead (via Energy From Within jewels). The "1 life" downside is irrelevant because you never take life damage.
- **The Traitor** (Timeless keystone): Flasks lose charges over time. Normally bad. But: gain flask charges every 5 seconds automatically. For builds that don't generate charges from kills (boss fights), the passive charge gain outweighs the loss.
- **Self-damage for benefit**: Blood Rage deals physical DoT to you. Normally bad. But: triggers "when you stop taking DoT" recovery bonuses (Arakaali Pantheon), generates Frenzy Charges on kill, gives attack speed. The degen is a feature, not a bug.

**How to find them**: When you see a downside on a keystone, unique, or ascendancy node, ask: "Is there a way to make this downside irrelevant or beneficial?" PoE is designed around this thinking.

---

## The Synergy Hunting Process

### Step 1: Identify Your Build's Core Mechanic
What is the ONE thing your build does? Not "deals fire damage" — be specific:
- "Applies a single massive ignite via Fireball"
- "Stacks 30+ poisons per second via Blade Vortex"
- "Maintains 15 permanent minions that attack independently"
- "Triggers spells via Cyclone crits at 10.10 per second"

### Step 2: List Every Stat That Feeds That Mechanic
For the ignite example:
- Fire damage (increases ignite base)
- Gem level (increases Fireball base damage → bigger ignite)
- Fire DoT multiplier (directly multiplies ignite DPS)
- Ignite duration (more total damage)
- Burning damage (increased category for ignite)
- Enemy fire resistance reduction (curse, exposure, penetration)
- Cast speed (more attempts to land big crits for crit-ignite builds)
- Shock on enemy (enemy takes increased damage → ignite deals more)

### Step 3: Find Items/Passives That Provide MULTIPLE Stats From Your List
The best synergy items are the ones that provide 2+ stats from your list simultaneously:
- A weapon with "+1 fire gems" (gem level) + "fire DoT multi" (DoT multi) + "fire damage" (increased) = three stats from one item
- An ascendancy node that gives "all damage ignites" (Shaper of Flames) + "exposure on herald" (Mastermind of Discord) = fire ignite + fire resistance reduction from the same class

### Step 4: Check for Unintended Interactions
This is where the real magic happens. Ask:
- "Does this mechanic interact with that mechanic in a way the tooltip doesn't mention?"
- "If I convert my damage from X to Y, do I benefit from BOTH X and Y modifiers?"
- "Does this 'on hit' effect trigger from my minions/totems/brands, or only from me?"
- "Does this 'nearby enemies' debuff stack with my curse? With my exposure?"
- Use the wiki and community resources — many interactions are documented by players who discovered them

### Step 5: Test in PoB
Before committing currency to a theory:
1. Build the theory in Path of Building
2. Check if the interaction actually works (some don't — PoB will show 0% contribution)
3. Compare the synergy version to a straightforward version — is the synergy actually better?
4. Some synergies are clever but numerically worse than simple stacking

---

## Common Synergy Patterns to Look For

### The Damage Conversion Chain
**Physical → Cold → Fire**: Each conversion step lets you benefit from the previous type's modifiers AND the new type's modifiers.
- Physical damage increases apply to the full original damage
- Cold damage increases apply to the cold portion after conversion
- Fire damage increases apply after final conversion to fire
- Result: Stacking all three modifier types = massive total multiplier
- Key: Conversion only flows forward (Phys → Ele → Chaos). 100% conversion at each step is ideal.

### The Ailment Multi-Stack
**Apply multiple different ailments simultaneously for compounding effects:**
- Shock (enemy takes up to 50% increased damage) + Ignite (DoT) + Chill (slow) + Freeze (stun)
- Elementalist can apply ALL ailments from ANY damage type (Shaper nodes)
- Skitterbots apply shock + chill for free (no damage needed)
- Each ailment independently benefits you — shock alone is a ~15-50% more multiplier

### The Defense-Offense Bridge
**A defensive investment that simultaneously boosts offense:**
- Determination (armour aura) → more armour → bigger Molten Shell → survive longer → deal more damage over time
- Block chance → Bone Offering block → life on block → sustain → stay in melee range → more DPS uptime
- Spell Suppression → take less spell damage → survive → don't need to dodge as much → more stationary DPS time
- The best builds don't trade defense for offense — they find stats that provide both.

### The Reservation Efficiency Cascade
**Each point of reservation efficiency unlocks exponentially more power:**
- 10% more efficiency → fit one more aura → that aura provides offense + defense → enables different gear → opens new build paths
- Enlighten 4 + tree efficiency + helmet Eldritch implicit + Charisma anoint = potentially 2-3 extra auras
- Each extra aura is a new multiplier layer

### The Trigger Chain
**Automate everything so your "rotation" is one button:**
- CWDT → guard skill + utility spell
- Trigger weapon → Desecrate + Offering + Curse
- Arcanist Brand → curse + exposure skill
- Instilling Orbs → auto-flask on conditions
- Result: Press main skill button → everything else happens automatically → maximum DPS uptime with minimum cognitive load

---

## Real-World Synergy Case Studies

### Case Study 1: Rob's Zombie Ailment Engine (Guardian Absolution)
**Core Insight**: Zombies don't need to deal high damage if their JOB is to apply debuffs, not kill.

**Synergy chain:**
1. Zombies with Chance to Bleed + Elemental Army Support → zombies apply bleed (physical) + elemental exposure (-10% res)
2. Zombie hits proc Elemental Proliferation (from Doryani's Catalyst or support) → ailments spread to nearby enemies
3. Pack is now pre-debuffed: bleeding, exposed, and potentially shocked
4. Absolution sentinels engage the pre-debuffed pack → sentinels deal massively amplified damage
5. Storm Secret triggers HoT on shock → additional AoE damage layer
6. Herald of Thunder storms further shock enemies → feeds back into Step 3

**Why it works**: The zombies are a SUPPORT army, not a damage army. Their value comes from the debuff ecosystem they create, which multiplies the main damage source (Absolution sentinels + HoT storms).

**Synergy types used**: Feedback Loop (shock → HoT → more shock), Conditional Chaining (zombie hit → bleed + exposure → amplified sentinel damage), Mechanical Bridge (Storm Secret turning shock into HoT triggers).

### Case Study 2: Doryani's Storm Concept (HoT Autobomber)
**Core Insight**: Three unrelated uniques create a self-sustaining lightning damage engine when combined.

**Synergy chain:**
1. Doryani's Prototype: Enemy lightning resistance equals YOUR lightning resistance. Tank your own to -200%.
2. Doryani's Catalyst: Built-in Elemental Proliferation on socketed gems → shock spreads to entire pack.
3. Storm Secret: HoT triggers on shock (not kill) → storms are triggered by shock application, not kills.
4. Elementalist Shaper of Storms: ALL hits shock with minimum 15% effect → guaranteed shock source.
5. Orb of Storms (in Catalyst) → hits enemies → Ele Prolif spreads shock → HoT triggers → HoT storms hit nearby → shock spreads further → more HoT → chain reaction.

**Inverse Scaling**: Your lightning resistance being -200% is normally suicidal. Prototype converts this from "I take massive lightning damage" to "enemies take massive lightning damage" because armour handles the self-damage (armour applies to lightning damage taken instead of lightning resistance with Prototype).

**Synergy types used**: Inverse Scaling (negative res = enemy vulnerability), Mechanical Bridge (Storm Secret enabling non-kill HoT), Feedback Loop (shock → HoT → more shock → more HoT), Threshold Convergence (armour simultaneously handles defense AND enables the negative-res offense).

### Case Study 3: CoC Ice Nova Inquisitor
**Core Insight**: Cyclone's constant hits + 100% crit chance = maximum CoC trigger rate = Ice Nova machine gun.

**Synergy chain:**
1. Cyclone hits many times per second (high APS with fast weapon)
2. 100% effective crit chance (Assassin's Mark + tree + gear) → every hit triggers CoC
3. CoC triggers Ice Nova at the 14% CDR breakpoint → 7.57 casts/sec
4. Inquisitor's Inevitable Judgement → crits ignore enemy elemental resistance → Ice Nova hits for full damage against bosses
5. Pious Path → Consecrated Ground provides life + ES regen + ailment immunity → sustain while spinning

**Threshold Convergence**: Crit chance investment simultaneously enables CoC triggers (must crit to trigger), activates Inevitable Judgement (crits ignore res), generates power charges, and applies freeze/chill from cold crits. ONE stat (crit) enables the entire build.

---

## The Anti-Synergy Checklist (Things That Break Synergies)

Not every combination works. Watch for these:

1. **Elemental Focus + Ailment Build**: Elemental Focus provides "more elemental damage" but prevents ailment application. If your build needs shock, ignite, or freeze, this support KILLS your synergy.

2. **Brutality + Elemental Auras/Heralds**: Brutality prevents non-physical damage. ALL elemental damage from auras (Hatred, Anger, Wrath) and heralds is deleted.

3. **Resolute Technique + Any Crit Investment**: RT prevents crits entirely. Any points spent on crit are wasted.

4. **Avatar of Fire + Chaos/Cold/Lightning Damage**: AoF converts 50% of non-fire to fire and prevents dealing non-fire. If your build has significant cold/lightning/chaos sources, AoF deletes them.

5. **Ancestral Bond + Self-Damage**: Ancestral Bond prevents YOU from dealing damage. Totems deal damage instead. If you planned to deal damage yourself AND use totems, AB breaks the self-damage half.

6. **Full Conversion + Impale**: Impale only records PHYSICAL damage. If you convert 100% physical to elemental, there's no physical damage left to impale. These are mutually exclusive scaling systems.

7. **Lone Messenger + Any Aura**: Lone Messenger massively buffs your ONE herald but disables ALL aura skills. No Determination, no Grace, no Hatred — only the herald. Make sure the tradeoff is worth it.

---

## How to Think Like a Synergy Hunter

### Read Everything Twice
First read: "What does this item/passive DO?"
Second read: "What does this item/passive ENABLE that wasn't possible before?"

The second question is where synergies live. An item that "adds 50 fire damage" does one thing. An item that "converts cold damage to fire" enables an entirely new scaling pathway.

### Question Every "Downside"
PoE's designers intentionally create items with downsides that can be mitigated or inverted:
- "Cannot deal non-physical damage" → What if my build is pure physical?
- "Take 10% increased damage" → What if I have enough mitigation that 10% more is negligible?
- "Maximum life is 1" → What if I don't need life because I have 15,000 Energy Shield?
- "Cannot use helmets" → What if I gain more from the offensive bonus than I lose from a helmet slot?

### Follow the Keyword
When you see a keyword in PoE, search for EVERY source of that keyword:
- "Shock" → Who applies shock? (Elementalist, Skitterbots, HoT, Lightning skills) → What happens on shock? (Storm Secret HoT, Shock effect scaling, enemy takes more damage) → What scales shock effect? (increased effect of non-damaging ailments, lightning damage for threshold)
- Following one keyword through every system it touches reveals the full web of possible synergies.

### Use CraftOfExile and PoeDB
- CraftOfExile shows which mods can roll on which items → find mods that bridge two systems
- PoeDB shows every modifier in the game → search by keyword to find all sources of a specific stat
- The wiki's "related items" sections often link to synergy partners

### Build Around the Weird Stuff
The most interesting synergies come from the weirdest mechanics:
- Items with "Your X is treated as Y" — these are synergy bridges by definition
- Keystones with dramatic tradeoffs — the tradeoff IS the synergy opportunity
- Ascendancy nodes that change fundamental rules — these rewrite what's possible
- Unique items with completely novel effects — if it does something no other item does, there's probably a build waiting to be discovered around it

---

## Practical Framework: Finding Your Next Synergy

1. **Start with one mechanic you want to build around** (e.g., Herald of Thunder storms)
2. **List every condition that activates it** (shock on enemy — from what sources?)
3. **List every stat that scales it** (lightning damage, gem level, increased effect)
4. **Find items/passives that satisfy MULTIPLE conditions or stats simultaneously**
5. **Check for feedback loops** (does the output of this mechanic feed back into its input?)
6. **Verify in PoB** (does the theory actually produce more DPS/defense than a straightforward approach?)
7. **Check for anti-synergies** (does any part of this combo break another part?)
8. **Iterate** — if it works, ask "what ELSE can I add to this chain?"

The goal isn't to find one clever interaction. It's to build a web of interactions where every piece amplifies every other piece. When your build reaches that state, it's not just strong — it's *emergent*. The whole becomes greater than the sum of its parts, and that's the deepest satisfaction PoE offers.
