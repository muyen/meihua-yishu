# 梅花易數 Meihua Yishu

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

**[English](README.md)** | **[繁體中文](README.zh-TW.md)**

**Meihua Yishu** (梅花易數 / Plum Blossom Numerology / Plum Blossom I Ching) is a traditional Chinese I Ching divination method, attributed to Shao Yong (邵雍) of the Song Dynasty. This project provides a professional Meihua divination system as an **AI Skill** for Claude, ChatGPT, Gemini, DeepSeek, and other LLMs.

> **Also known as:** 梅花易数 (Simplified Chinese), Mei Hua Yi Shu, Plum Blossom Oracle, 梅花心易

## Why Meihua Yishu?

### A Decision-Making Framework, Not Fortune-Telling

Unlike popular misconceptions about divination, Meihua Yishu is a **structured thinking tool** rooted in 3,000 years of Chinese philosophical wisdom:

| Misconception | Reality |
|---------------|---------|
| "Predicts the future" | Analyzes present conditions and likely trajectories |
| "Superstition" | Systematic framework based on pattern recognition |
| "Magic" | Philosophical method for examining situations from multiple angles |

### Benefits

🎯 **Decision Clarity** — When facing complex choices, the hexagram structure forces you to consider factors you might overlook

🔄 **Multiple Perspectives** — The Ti-Yong (体用) framework systematically examines self vs. environment, action vs. reaction

⏱️ **Timing Awareness** — The 應期 (Yingqi) system encourages thinking about *when* to act, not just *what* to do

🌊 **Change Philosophy** — Based on the I Ching principle that everything changes; helps accept uncertainty and plan adaptively

💭 **Reflection Tool** — The divination process creates space for introspection and deeper thinking about your situation

### Who Uses It?

- **Entrepreneurs** — For strategic timing and partnership decisions
- **Individuals** — For major life choices (career, relationships, relocation)
- **Curious Minds** — To explore Eastern philosophy and symbolic thinking
- **Developers** — To integrate traditional wisdom into AI applications

### The Meihua Advantage

Compared to other I Ching methods:
- **Faster** — No coins or yarrow stalks needed; cast from time, numbers, or observation
- **More Intuitive** — Trigram-based (8 symbols) rather than full hexagram memorization (64 symbols)
- **Contextual** — Ti-Yong analysis relates directly to your specific situation
- **Practical** — Clear auspicious/inauspicious framework with actionable insights

> *"The Yi does not predict fate — it reveals patterns. Understanding patterns empowers better choices."*

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
├── ETHICS.md                     # Ethical guidelines (English)
├── ETHICS.zh-TW.md              # Ethical guidelines (繁體中文)
├── README.md                     # This file
├── README.zh-TW.md              # Traditional Chinese README
├── LICENSE                       # CC BY-NC-SA 4.0 License
├── references/
│   ├── 64gua.md                 # 64 Hexagrams detailed guide
│   ├── yaoci.md                 # 384 Line texts
│   ├── zhouyi-zhuan.md          # Tuan & Xiang commentaries
│   ├── bagua-wanwu.md           # Bagua correspondences + verses
│   ├── case-studies-expanded.md # Classic divination cases
│   ├── ying-guides.md           # Ten responses + external signs
│   ├── yingqi-calc.md           # Timing calculation guide
│   ├── 18-divinations.md        # 18 types of specific readings
│   └── cezi-method.md           # Character analysis (測字法)
└── scripts/
    └── meihua_calc.py           # Python calculation tool
```

## Usage

### As a Claude Code Skill

1. Clone this repository to your Claude Code skills directory:
   ```bash
   # Personal skills (works across all projects)
   git clone https://github.com/muyen/meihua-yishu.git ~/.claude/skills/meihua-yishu

   # Or for a specific project
   git clone https://github.com/muyen/meihua-yishu.git .claude/skills/meihua-yishu
   ```

2. Start a conversation and mention divination keywords like "占卦", "起卦", or "meihua" — the skill will activate automatically.

### Using with Other LLMs

This skill can be adapted for use with other AI platforms:

#### ChatGPT (Custom GPT)

1. Go to [ChatGPT](https://chat.openai.com) → Explore GPTs → Create
2. Copy the contents of `SKILL.md` into the **Instructions** field
3. Upload all files from `references/` to the **Knowledge** section
4. Configure: Enable Code Interpreter for calculations

#### Google Gemini (Gems)

For Gems UI navigation, see [official Gemini documentation](https://support.google.com/gemini/answer/14575153).

**Setup (10 files total):**

| Section | File | Description |
|---------|------|-------------|
| **Instructions** | `SKILL.md` | Paste full content into system instructions |
| **Knowledge** | `64gua.md` | 64 hexagrams guide |
| | `yaoci.md` | 384 line texts |
| | `zhouyi-zhuan.md` | Tuan & Xiang commentaries |
| | `bagua-wanwu.md` | Bagua correspondences + verses |
| | `ying-guides.md` | Ten responses + external signs |
| | `yingqi-calc.md` | Timing calculation |
| | `18-divinations.md` | 18 specific reading types |
| | `case-studies-expanded.md` | Classic divination cases |
| | `cezi-method.md` | Character analysis method |

All files are in the `references/` folder.

#### Chinese LLMs (中國大模型)

Supported models: **DeepSeek**, **Kimi (月之暗面)**, **Qwen (通义千问)**, **文心一言**, **ChatGLM (智谱清言)**, **豆包**

1. Copy the contents of `SKILL.md` into your conversation or system prompt
2. For lunar calendar conversion (without code execution):
   - The LLM can use web search to find lunar dates (e.g., search "2024年9月17日 農曆")
   - Then apply the calculation formulas from `SKILL.md`
3. Upload reference files from `references/` if the platform supports it

> 💡 Most Chinese LLMs have built-in web search, which can be used for accurate lunar date conversion even without code execution capability.

#### Other LLMs (General)

For any LLM that supports system prompts:

1. Use `SKILL.md` as the system prompt
2. Include relevant reference files based on context window size:
   - Essential: `64gua.md`, `bagua-symbols.md`
   - For line readings: `yaoci.md`
   - For specialized readings: `18-divinations.md`, `shiying-guide.md`
   - For character analysis: `cezi-method.md`

3. Or concatenate files for a single-file approach:
   ```bash
   cat SKILL.md references/*.md > meihua-complete.md
   ```

#### API Integration

Use `scripts/meihua_calc.py` as a standalone calculation tool:
```python
from scripts.meihua_calc import calculate_hexagram

result = calculate_hexagram(method="time")  # or method="num", nums=[6, 8]
```

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
