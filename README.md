# 梅花易數 Meihua Yishu

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

**[English](README.md)** | **[繁體中文](README.zh-TW.md)**

**Meihua Yishu** (Plum Blossom Numerology) is a traditional Chinese I Ching divination method, attributed to Shao Yong (邵雍) of the Song Dynasty. This project provides a professional Meihua divination system that can be used as a Claude AI Skill.

## Features

### Casting Methods
- **Time-based Divination** — Cast hexagrams using current or specified time
- **Number-based Divination** — Cast hexagrams using numbers
- **Sound-based Divination** — Cast using the count of sounds heard
- **Color-based Divination** — Cast based on colors corresponding to five elements
- **Measurement-based Divination** — Cast using object dimensions
- **Direction-based Divination** — Cast based on the direction of a person or object

### Interpretation Functions
- **Ti-Yong Analysis** — Interpret the relationship between Ti (体) and Yong (用) trigrams
- **Tongguan Mediation** — Analyze five-element bridging to mitigate克 (controlling) relationships
- **64 Hexagrams Interpretation** — Detailed explanations of hexagram and line texts
- **Changing Lines Derivation** — Analyze the fortune of transformed hexagrams
- **Seasonal Strength (卦氣)** — Determine Ti trigram strength based on season
- **Timing Prediction (應期)** — Predict when events will manifest

### Specialized Readings
- **18 Specific Readings** — Marriage, illness, wealth, travel, and more
- **Ten Responses (十應)** — Environmental sign analysis
- **Bagua Correspondences** — Modern and traditional symbolic associations
- **Character Analysis (測字)** — Fortune telling by analyzing Chinese characters

### AI-Assisted Features
- **Photo Analysis** — Upload photos for AI to analyze environmental signs
- **Environmental Sensing** — Describe surrounding sounds, colors, people for enhanced readings

## Project Structure

```
meihua-yishu/
├── SKILL.md                      # Main skill documentation
├── README.md                     # This file
├── README.zh-TW.md              # Traditional Chinese README
├── LICENSE                       # MIT License
├── references/
│   ├── 64gua.md                 # 64 Hexagrams detailed guide
│   ├── yaoci.md                 # 384 Line texts
│   ├── zhouyi-zhuan.md          # Tuan & Xiang commentaries
│   ├── bagua-symbols.md         # Bagua correspondences
│   ├── case-studies-expanded.md # Classic divination cases
│   ├── waiying-guide.md         # External signs guide
│   ├── yingqi-calc.md           # Timing calculation guide
│   ├── 18-divinations.md        # 18 types of specific readings
│   ├── shiying-guide.md         # Ten responses detailed guide
│   ├── wanwu-fu.md              # Myriad things verses
│   └── cezi-method.md           # Character analysis (測字法)
└── scripts/
    └── meihua_calc.py           # Python calculation tool
```

## Usage

### As a Claude Skill

Place this folder in your Claude Skills directory to use.

### Using the Python Tool

```bash
# Cast hexagram using current time
python scripts/meihua_calc.py time

# Cast hexagram using two numbers
python scripts/meihua_calc.py num 6 8

# Cast hexagram using three numbers (third is changing line)
python scripts/meihua_calc.py num 6 8 3
```

Example output:

```
==================================================
📿 Meihua Yishu Divination Result
==================================================

【1. Calculation】
  Year: 10
  Month: 1
  Day: 17
  Hour: Hai (12)

【2. Primary Hexagram】
  #49: Ze Huo Ge (Revolution)
  Upper: Dui ☱
  Lower: Li ☲
  Binary: 011101
  Line 4 changing

【3. Ti-Yong Analysis】
  Ti Trigram: Li (lower) - Fire
  Yong Trigram: Dui (upper) - Metal
  Relationship: Ti controls Yong (Auspicious)

【4. Mutual Hexagram】
  Qian Wei Tian (Heaven over Heaven)

【5. Transformed Hexagram】
  #17: Ze Lei Sui (Following)
  Binary: 011001
==================================================
```

## Core Principles

Meihua Yishu uses **Early Heaven Bagua Numbers**:

| Trigram | Number | Element | Symbol |
|---------|--------|---------|--------|
| Qian (乾) | 1 | Metal | ☰ |
| Dui (兌) | 2 | Metal | ☱ |
| Li (離) | 3 | Fire | ☲ |
| Zhen (震) | 4 | Wood | ☳ |
| Xun (巽) | 5 | Wood | ☴ |
| Kan (坎) | 6 | Water | ☵ |
| Gen (艮) | 7 | Earth | ☶ |
| Kun (坤) | 8 | Earth | ☷ |

### Ti-Yong Theory

- **Ti (体)**: The subject, self, the querent
- **Yong (用)**: The object, matter, external environment
- **Mutual Hexagram (互卦)**: The development process
- **Transformed Hexagram (變卦)**: The final outcome

### Fortune Determination

| Situation | Fortune | Explanation |
|-----------|---------|-------------|
| Yong generates Ti | Very Auspicious | Gaining benefits, external assistance |
| Ti controls Yong | Auspicious | You control the situation, success likely |
| Ti-Yong in harmony | Auspicious | Same element, harmonious and smooth |
| Yong controls Ti | Inauspicious | Constrained by others, unfavorable |
| Ti generates Yong | Draining | Much effort, little return |

### Tongguan Mediation (通關化解)

When Ti and Yong are in a controlling relationship, a "bridging" element in the Mutual or Transformed hexagram can mitigate the inauspicious outcome:

| Controlling Relationship | Bridging Element |
|--------------------------|------------------|
| Metal controls Wood | Water |
| Wood controls Earth | Fire |
| Earth controls Water | Metal |
| Water controls Fire | Wood |
| Fire controls Metal | Earth |

## Divination Principles

1. **No question, no divination** — Don't divine without a specific question
2. **No more than three times** — Don't repeat divination for the same question more than three times
3. **No movement, no divination** — Don't divine without cause
4. **Interpret with reason** — Hexagrams must be interpreted in context

## References

- *Meihua Yishu (梅花易數)* — Shao Yong
- *Zhou Yi (I Ching / 周易)*
- *Introduction to I Ching Studies (易學啟蒙)*

## License

This work is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).

**You are free to:**
- Share — copy and redistribute the material
- Adapt — remix, transform, and build upon the material

**Under the following terms:**
- **Attribution** — You must give appropriate credit
- **NonCommercial** — You may not use the material for commercial purposes
- **ShareAlike** — Derivatives must be distributed under the same license

See [LICENSE](LICENSE) for details.

## Contributing

Issues and Pull Requests are welcome!

---

☯️ The Yi has Taiji, which generates the Two Forms, which generate the Four Images, which generate the Eight Trigrams.
