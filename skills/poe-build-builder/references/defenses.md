# Defenses — Complete Reference

## Defense Philosophy

PoE defenses work in layers. No single defense is sufficient. The question is always
"what kills this build?" — then add the missing layer.

Three categories of defense:
1. **Avoidance** — prevent being hit or taking damage (evasion, block, suppress)
2. **Mitigation** — reduce the damage you DO take (armour, resistances, fortification, guard skills)
3. **Recovery** — restore your HP/ES after damage (leech, regen, recoup, flasks)

The order of operations for incoming damage (simplified):
```
Hit occurs → Evasion check (attacks only) → if hit lands:
  → Damage shift ("taken as") → Resistance/Armour mitigation
  → Flat reduction ("reduced damage taken") → "Less damage taken" multipliers
  → Guard skill absorb → Block check → Spell Suppression check
  → Stun check → Final life/ES loss
```

---

## Hit Point Pools

### Life

**The Life Formula:**
```
Max Life = (38 + Character_Level × 12 + Strength / 2 + sum of all flat added life)
         × (1 + sum of all "increased maximum life")
         × product of all "more/less maximum life" multipliers
```

Key facts:
- Base: 38 at level 1
- **+12 life per character level**
- **+1 maximum life per 2 Strength** (0.5 per point)
- Flat "+X to maximum life" from gear, tree, jewels is added to the base before % scaling
- Target life pools: 3,500+ for early mapping, 4,500+ for red maps, 5,500+ for pinnacle content
- Life builds are the most common and easiest to gear

### Mind over Matter (MoM)
- Keystone: 40% of damage taken from hits is taken from mana before life (base value)
- Effectively increases your EHP by extending it into your mana pool
- Requires UNRESERVED mana — if your mana is all reserved for auras, MoM does nothing
- Typically need mana ≥ 43% of life for optimal ratio (so MoM never runs out before life does)
- Clarity aura and mana regen are critical for sustaining MoM
- Agnostic keystone: sacrifices ES, drains mana to recover life continuously

### Eldritch Battery (EB)
- Keystone: Energy Shield protects MANA instead of Life
- Commonly paired with MoM — ES → protects mana → mana absorbs damage via MoM → layered defense
- Also used to spend ES on skill costs instead of mana (freeing mana for auras)
- Your life pool becomes your only HP buffer, so life stacking is essential

### Energy Shield (ES)
- Sits ON TOP of life — damage hits ES first by default
- **Chaos damage bypasses ES by default** (critical! — need Shavronne's or CI to prevent this)
- Recharges after a **2-second delay** of not taking damage to ES (or the resource ES protects)
- Every 10 Intelligence = **2% increased maximum ES**
- Does NOT have life flasks — recovery comes from recharge, leech, regen, or on-hit
- **Wicked Ward** (Occultist): ES recharge cannot be interrupted by damage (extremely powerful)

#### Key ES Keystones
- **Chaos Inoculation (CI)**: Life set to 1, IMMUNE to chaos damage, ES is your entire HP pool
- **Ghost Reaver**: Life leech applies to ES instead, but ES recharge rate is halved
- **Zealot's Oath**: Life regeneration applies to ES instead
- **Vaal Pact + Ghost Reaver**: Double ES leech rate, but no regen and reduced recharge

#### Low Life / ES Hybrid
- Low Life threshold: **50% of maximum life** (or lower with certain mods)
- While on Low Life: Pain Attunement grants 30% more spell damage
- Typical approach: reserve life with Arrogance-supported auras → permanently on Low Life → Pain Attunement active
- Shavronne's Wrappings prevents chaos bypassing ES (mandatory for LL/ES builds without CI)
- Petrified Blood (see below) enables life-based Low Life builds

### Petrified Blood
- Reserves 35% mana. While on Low Life (below 50% HP):
  - 40% of life loss from hits below the low life threshold is **prevented** and instead applied as a DoT over 4 seconds
  - At gem level 20+, only ~75-80% of the prevented life loss is actually dealt as the DoT (net damage reduction)
  - Non-flask life recovery cannot bring you above 50% — only flasks can
- Effectively turns big hits into survivable damage-over-time
- Synergizes with: Recoup (30% recoup counters the delayed life loss), overleech (leech never stops because you're never at full life), Pain Attunement
- **Does NOT protect against DoT** — only hit damage
- Complex mechanic — evaluate carefully in PoB before committing

### Ward
- Introduced in 3.16, from Expedition items
- Absorbs a fixed amount of damage from each hit, then goes on cooldown
- Niche — primarily used in Wardloop builds (abuse the cooldown for CWDT triggers)
- Not a mainstream defense layer for most builds

---

## Avoidance Layers

### Evasion
- Chance to evade ATTACKS only — NOT spells, NOT DoT
- **Entropy system** (deterministic): The game tracks a counter. Each attack adds the hit chance to the counter; when it reaches 100, the attack hits and the counter resets. This means:
  - You will NEVER get hit by many attacks in a row at high evasion
  - You will ALWAYS eventually get hit — evasion is not immunity
  - The system prevents streaks of bad luck, unlike pure random chance
- Cap: **95% chance to evade** (cannot reach 100%)
- **Crit downgrade**: If an attack crits, evasion does a SECOND check. If this check succeeds, the crit becomes a normal hit (but you still take the hit damage). Huge defensive value.
- Scaled by: Dexterity (1% increased per 5 Dex), Grace aura (flat + % more), evasion gear, Jade Flask
- **Iron Reflexes** keystone: Converts ALL evasion rating to armour (gives up evasion for armour)
- Weakness: Zero protection against spells and DoTs — must pair with Spell Suppression

### Block
- Separate chances for **attack block** and **spell block**
- Max attack block: **75%** (can be raised by specific sources)
- Max spell block: **75%**
- Blocked hit deals **ZERO damage** by default
- **Glancing Blows** keystone: Doubles your block chance, but blocked hits deal **65% damage**
  - Great for builds that stack "life/ES gained on block" — the recovery triggers even on glancing blocks
- Sources: Shields (base 20-30%+), dual wielding (15% base attack block), Bone Offering, Tempest Shield, passive tree
- **"Recover X life/ES when you block"** mods: Extremely powerful recovery. Stacking this is a build archetype.
- **Versatile Combatant** (Gladiator): Your maximum chance to block attack damage is applied to spells
- Block is rolled AFTER damage mitigation — if you block, you take zero (or 65% with Glancing Blows) of the MITIGATED damage

### Spell Suppression
- Replaced dodge in 3.16
- When you suppress a spell hit: take **50% less damage** from that hit (base — was 40% in earlier patches, verify current value)
- Cap: **100% chance to suppress** — at 100%, ALL spell hits are halved
- Can increase the prevented damage with "Prevent +X% of Suppressed Spell Damage" mods
- Found on: evasion-based gear, Dex-area passive tree, Ranger/Shadow ascendancies
- Pairs perfectly with evasion: evasion handles attacks, suppression handles spells
- Also reduces ailment damage from suppressed spell hits proportionally

### Elusive
- Grants chance to avoid all damage from hits + increased movement speed
- Effect **degrades over time** after gaining it (starts high, fades to zero)
- Cannot stack — reapplication refreshes the timer at the current maximum
- Sources: Nightblade support, Withering Step, Mistwalker (Assassin), some gear
- Good supplemental layer but unreliable as primary defense

---

## Mitigation Layers

### Armour
- Reduces **PHYSICAL damage from hits** only (by default)
- **Formula**: `Damage Reduction = Armour / (Armour + 5 × Raw_Physical_Damage)`
- Key insight: Armour is MORE effective against **small hits**, LESS effective against **big hits**
  - 10,000 armour vs 1,000 hit → 67% reduction (takes 333 damage)
  - 10,000 armour vs 5,000 hit → 29% reduction (takes 3,571 damage)
  - 10,000 armour vs 10,000 hit → 17% reduction (takes 8,333 damage)
  - 50,000 armour vs 10,000 hit → 50% reduction (takes 5,000 damage)
- **Determination** aura: Flat armour + "% more armour" — the single biggest armour source for most builds
- **Granite Flask**: Large flat armour boost during effect
- **Molten Shell**: Guard skill that absorbs damage equal to 20% of your armour. AT 50K ARMOUR = 10,000 ABSORB. This is why armour stacking is so powerful.

#### Special Armour Interactions
- **Doryani's Prototype**: Armour applies to LIGHTNING damage from hits instead of lightning resistance
- **Transcendence** keystone: Armour applies to ELEMENTAL damage from hits, but NO LONGER applies to physical
- **The Fourth Vow**: Armour also applies to CHAOS damage from hits
- **Iron Reflexes**: Converts evasion to armour

### Elemental Resistances
- Fire, Cold, Lightning: Default cap **75%**
- Chaos: Default cap **75%** (but much harder to gear for)
- **Campaign penalty**: -30% after Act 5 Kitava, additional -30% after Act 10 Kitava (total -60% to all elemental res)
- **ALWAYS cap elemental resistances at 75%.** This is non-negotiable. Uncapped res is the #1 reason new players die.

#### Maximum Resistance
- The 75% cap can be raised up to **90% absolute hard cap**
- Each 1% of max res above 75% is EXTREMELY powerful due to how percentages work:
  - 75% res → you take 25% of incoming elemental damage
  - 80% res → you take 20% → that's **20% less damage taken** compared to 75%
  - 85% res → you take 15% → **40% less damage** compared to 75%
  - 90% res → you take 10% → **60% less damage** compared to 75%
- Sources: Purity of Fire/Cold/Lightning auras, certain ascendancy nodes, specific uniques
- Max res stacking is one of the most powerful defensive strategies in the game

#### Overcapping Resistances
- Curses (like Elemental Weakness map mod) reduce your uncapped resistance
- If you're at exactly 75% and get cursed with -30%, you drop to 45% effective res
- Overcap by 30-50% above 75% to stay capped during cursed maps
- Your character sheet shows both capped and uncapped values

### Chaos Resistance
- Often neglected but increasingly important in endgame
- After campaign penalties, most builds are at -60% chaos res or worse
- **Target**: At minimum 0%, ideally 30-50%, 75%+ for chaos-heavy content
- Chaos damage bypasses ES by default — even ES builds need chaos res
- **Divine Flesh** keystone: 50% of elemental damage taken as chaos instead. +5% max chaos res. Extremely powerful but requires 80%+ chaos res to be effective.

### Physical Damage Reduction
- Flat percentage reduction that applies equally to ALL physical hit sizes (unlike armour)
- Sources: Endurance Charges (4% per charge), passive tree, ascendancy nodes, certain flasks
- **Stacks additively with armour's reduction** (both contribute to total phys reduction)
- **Cap: 90% total physical damage reduction** (armour contribution + flat reduction combined)
- Important: this is calculated AFTER armour's formula, they share the same 90% cap

### Fortification
- **Stackable buff**: Each stack grants **1% less damage taken from hits**
- Default maximum: **20 stacks** (= 20% less damage from hits at full stacks)
- Base duration: **5-6 seconds** (varies by source, has been adjusted across patches)
- Stacks gained per hit scale with the damage of the fortifying hit relative to the enemy's ailment threshold
- Only applies to damage from HITS — not DoT
- Sources:
  - **Fortify Support**: Linked to melee attacks, melee hits fortify (also gives more melee damage)
  - **Fortify Mastery**: "Melee Hits Fortify" at the cost of -3 maximum Fortification (cap becomes 17)
  - **Champion ascendancy**: "Fortitude" grants permanent 20 Fortification
  - **Vigilant Strike**: Specifically grants fortification with longer duration
- Champion gets this for free — other melee builds need to invest

### "Reduced Extra Damage from Critical Strikes"
- When enemies crit you, they deal 150% damage by default (130% for monsters)
- "Reduced extra damage from critical strikes" reduces the EXTRA portion
- At 100% reduced: crits deal normal damage (enemy crits are effectively neutralized)
- Sources: Body armour implicit, shield implicit, passive tree, Sanctum of Thought notable
- Extremely valuable for survivability, especially in crit-heavy content (Expedition, certain bosses)

---

## Guard Skills

Only ONE guard skill can be active at a time. They provide temporary damage absorption.

### Molten Shell
- Absorbs damage equal to **20% of your armour** as a shield
- At 30k armour: absorbs 6,000. At 50k: absorbs 10,000. At 80k: absorbs 16,000.
- Also grants additional flat armour while active
- **Best guard skill for armour builds by a massive margin**
- Vaal Molten Shell: Much larger absorb, but requires souls

### Steelskin
- Flat damage absorb (does NOT scale with stats) — ~2,000-3,000 at high gem level
- Grants **bleed immunity** during effect
- Better for low-armour builds (evasion characters)

### Immortal Call
- Grants physical and elemental damage reduction for a short duration
- Consumes Endurance Charges for increased duration and stronger effect
- Extremely powerful burst protection when paired with endurance charge generation

### Bone Armour (Necromancer only)
- From Bone Barrier ascendancy node
- Absorb for you AND your minions
- Stronger version of Steelskin for Necromancers

### CWDT Automation
- Cast When Damage Taken (CWDT) support triggers linked guard skills automatically
- CWDT level determines the damage threshold — **lower level = triggers more often but can only support lower-level gems**
- Common: Level 1-3 CWDT + low-level Molten Shell for frequent auto-triggers
- Alternative: Keep a HIGH-level guard skill on manual keybind for boss encounters
- CWDT can also trigger other utility spells (curses, Tempest Shield, etc.) alongside the guard skill

---

## Recovery

### Life Leech
- Recover a percentage of damage DEALT as life
- Each hit creates a leech instance. Multiple instances run simultaneously.
- **Total leech rate cap**: 20% of max life per second (all instances combined)
- **Individual instance rate**: 2% of max life per second per instance
- Even tiny leech percentages (0.2-0.4%) are sufficient because hit damage is so high relative to life
- **Vaal Pact**: Doubles maximum leech rate to 40% of max life/second, but **disables all life regeneration**
- Elemental leech sources: Doryani's Catalyst (0.2%), Atziri's Promise flask, Doryani's Lesson notable, some gear mods
- **Overleech** (Slayer's "Brutal Fervour" or Petrified Blood interaction): Leech instances don't stop at full life — they persist, giving continuous recovery even between hits

### Life Regeneration
- Flat life/second or % of max life/second
- Works **constantly**, including during boss phases with no enemies to hit
- Always running = always recovering. The most reliable form of recovery.
- Sources: Stone Golem (flat regen), Vitality aura (% regen), passive tree, Consecrated Ground (+6% life regen or more depending on source)
- **Zealot's Oath**: Life regen applies to ES instead of life
- **Righteous Fire** costs 90% of life+ES as burning damage per second — must out-regen this to sustain

### Recoup
- "Recoup X% of damage taken as life/ES/mana over 4 seconds"
- NOT leech — triggers off damage TAKEN, not damage dealt
- Works against ALL damage types including DoT and chaos
- The bigger the hit, the more you recoup — scales with incoming damage
- Stacks from multiple sources (tree, gear)
- 30% recoup directly counters Petrified Blood's delayed life loss
- Extremely powerful and underrated defensive layer

### Life Gain on Hit
- Flat life gained per hit against an enemy
- Scales with **hit frequency** — fast multi-hit skills (Cyclone, Blade Vortex, etc.) recover enormous amounts
- Claws have innate life gain on hit implicit
- Poacher's Mark also provides life on hit
- Does NOT work with DoTs, minion hits, or totems (unless specifically stated)

### ES Recovery Methods
- **ES Recharge**: After 2 seconds of not taking damage to ES (or the resource it protects), ES begins recharging rapidly
  - "Faster start of ES recharge" reduces the delay
  - "Faster ES recharge rate" speeds the recharge itself
  - Wicked Ward (Occultist): Recharge cannot be interrupted once started
  - Dissolution of Flesh: interesting interaction with recharge timing
- **ES Leech**: Works like life leech. Default cap: 10% of max ES per second (lower than life leech cap to compensate for larger ES pools)
  - Ghost Reaver: Life leech applies to ES instead
- **ES on Hit**: Similar to life gain on hit but for ES. Sources exist on some unique items and passives.

### Flask-Based Recovery and Defense
Flasks are a critical defense layer that many new players undervalue:

#### Life Flasks
- Instant or over-time recovery of life
- Can roll "instant recovery" or "recover on low life" for emergency heals
- Flask effectiveness scales the amount recovered

#### Utility Flasks (Defensive)
- **Granite Flask**: Large flat armour boost — huge for Molten Shell
- **Jade Flask**: Large flat evasion boost
- **Quartz Flask**: Phasing (walk through enemies) + chance to suppress spells or dodge
- **Basalt Flask**: Flat physical damage reduction
- **Amethyst Flask**: +35% chaos resistance during effect
- **Bismuth Flask**: +35% all elemental resistances during effect (great for gearing flexibility)
- **Sulphur Flask**: Creates Consecrated Ground (life regen + damage)
- **Topaz/Ruby/Sapphire**: Specific elemental resistance + reduced damage taken of that element

#### Flask Modifiers
- "Gain X charges when hit" — sustains flasks during boss fights
- "Used when charges reach full" — auto-triggers without pressing
- Ailment removal: flasks can remove and grant immunity to specific ailments during effect
- **Pathfinder ascendancy** makes flask-based defense incredibly powerful (flask effect, duration, charge generation)

---

## Damage Taken As / Damage Shifting

"X% of Y damage taken as Z damage" — one of the most powerful defensive mechanics:

- The shifted portion is mitigated by the NEW damage type's resistance/defense
- Does NOT count as damage conversion — no double-dipping
- Occurs BEFORE mitigation — the shifted damage type determines which resistance applies
- Cannot chain-shift in a single step (A→B→C doesn't work; only A→B and A→C independently)

### Key Applications
- **Dawnbreaker** shield: Lightning/Cold/Physical damage taken as Fire → stack fire res/max fire res
- **Taste of Hate** flask: Physical damage taken as Cold → cold res mitigates the shifted portion
- **Lightning Coil**: Physical taken as Lightning → capped lightning res handles it
- **Tempered by War** (Lethal Pride): 50% of cold/lightning damage taken as fire, but cold/lightning res is zero
- **Divine Flesh** (Glorious Vanity): 50% of elemental damage taken as chaos → need 80%+ chaos res
- Critical for Doryani's Prototype builds: shifting lightning damage to other types you can actually resist

---

## Stun

Stun is an underrated danger that kills builds:
- Every hit has a chance to stun based on damage relative to your maximum life
- While stunned: you cannot act (no movement, no skills, no flasks)
- Getting stunlocked in a pack = death
- **ES builds are extra vulnerable**: stun is calculated against LIFE, not ES. Low life = easy stuns.

### Stun Immunity/Mitigation
- **Unwavering Stance** keystone: Cannot be stunned, but cannot evade (trade-off)
- Stun immunity during certain effects (Cyclone, Leap Slam while mid-air, etc.)
- "X% chance to avoid being stunned" — 100% = immunity
- **Brine King Pantheon**: Cannot be stunned if you were stunned recently (prevents chainlocking)
- High life pool naturally reduces stun chance
- Specific gear mods: "Cannot be stunned" on some uniques

---

## What Kills Builds (Common Death Causes)

1. **Uncapped elemental resistances** — below 75% ele res = fix immediately, always
2. **Physical one-shots** — need armour + endurance charges + guard skill + fortification for melee
3. **Spell damage with no suppression** — evasion builds without 100% suppress die to spells constantly
4. **Chaos damage** — bypasses ES, most builds have negative chaos res after campaign. Get at least 0%.
5. **Damage over Time** — bypasses evasion, armour, block, suppression. Need regen + recoup + flasks.
6. **Lightning DoT with Doryani's Prototype** — armour doesn't help with DoT, res is treated as 0%. Build-specific weakness.
7. **Stun-locking** — getting stunned in packs and unable to react. Unwavering Stance or Brine King.
8. **Corrupted Blood** — stacking physical DoT. Need "corrupted blood cannot be inflicted on you" jewel implicit.
9. **Critical strike spikes** — enemies critting you for 150% damage. Get "reduced extra crit damage taken."
10. **Curse map mods without overcapping** — Elemental Weakness map drops your res by 30%+. Overcap.

---

## Defensive Archetypes (Common Combinations)

### Armour + Block (Str builds: Guardian, Juggernaut, Champion)
- Determination + high armour gear → Molten Shell absorbs huge amounts
- Shield with block + "recover life on block" → sustained recovery
- Endurance charges for physical reduction + ele res overcap
- Fortification for melee builds
- Weakness: spell damage, DoT

### Evasion + Suppression (Dex builds: Trickster, Raider, Deadeye)
- Grace + evasion gear → high evade chance against attacks
- 100% spell suppression → halves all spell hit damage
- Acrobatics area of tree naturally supports this
- Often paired with Elusive for additional avoidance
- Weakness: DoT, chaos damage, inevitable hits that get through

### ES + Block (Int builds: Occultist, Guardian)
- Discipline + high ES gear → 6,000-12,000+ ES pool
- Block with "recover ES on block" → sustained ES recovery
- Wicked Ward (Occultist) makes ES recharge uninterruptible
- CI or Shavronne's for chaos protection
- Weakness: must solve chaos damage, stun vulnerability with low life

### Low Life + Petrified Blood (Hybrid)
- Petrified Blood at 50% life threshold + Pain Attunement (30% more spell damage)
- Recoup to counter delayed life loss
- Overleech from leech never stopping (can't reach full life)
- Often combined with armour and block for physical mitigation
- Weakness: DoT bypasses Petrified Blood entirely

---

## Practical Decision Framework

1. **Cap elemental resistances first** — 75% minimum, overcap by 30%+ for curse maps
2. **Pick a primary defense archetype** — armour+block OR evasion+suppression. Don't split investment.
3. **Layer mitigation** — guard skill + endurance charges + fortification (for melee) + max res if possible
4. **Ensure recovery** — leech OR regen OR recoup. Without recovery, you die to accumulating chip damage.
5. **Address chaos resistance** — at minimum 0%, target 30-50% for comfortable endgame
6. **Get a guard skill** — Molten Shell for armour builds, Steelskin for evasion builds. Automate with CWDT.
7. **Solve stun** — Unwavering Stance, Brine King, or stun avoidance. Especially for ES builds.
8. **Get Corrupted Blood immunity** — jewel implicit. Non-negotiable for red maps+.
9. **Reduce crit damage taken** — body armour/shield implicits, passive tree
10. **When you die, ask: what killed me?** — identify the damage type and add the missing layer
