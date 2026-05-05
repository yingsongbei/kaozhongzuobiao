---
name: academic-stats-table
description: "Generate publication-ready academic statistics tables from raw data. When the user asks to create a two-group comparison table with means ± s.e., t-test significance, and English academic formatting, use this skill."
agent_created: true
---

# academic-stats-table — Academic Statistics Table Generator

Generate publication-ready English statistical tables from raw numeric data.
Outputs a two-group comparison table with mean ± s.e., sample size (n),
and one-tailed Welch's t-test significance markings.

## When to use

- User asks to create a statistical table from raw data
- User provides two groups of numeric data (screenshot, pasted numbers, CSV, etc.)
- User wants mean ± s.e. format with t-test significance
- User wants an English academic-style table matching journal format

## Workflow

### Step 1: Extract raw data

Read data from whatever input the user provides (image, text, file). Identify:
- Group 1 name and raw values for each trait
- Group 2 name and raw values for each trait
- Trait names (prefer English; translate common terms if needed)

### Step 2: Run the statistics script

Use the bundled Python script `scripts/academic_stats.py`. It reads JSON from
stdin and outputs HTML.

**Input JSON format:**

```json
{
  "title": "Table 1. Comparison of traits between groups",
  "group1_name": "Wild-type",
  "group2_name": "Mutant",
  "traits": [
    {
      "name": "Plant height (cm)",
      "data1": [10.2, 11.5, 9.8, ...],
      "data2": [14.3, 15.1, 13.9, ...]
    },
    {
      "name": "Grain weight (g)",
      "data1": [2.1, 2.3, 2.0, ...],
      "data2": [3.1, 3.3, 3.0, ...]
    }
  ]
}
```

**Fields:**
- `title`: Table caption (required)
- `group1_name`: Label for control / reference group (required)
- `group2_name`: Label for treatment / test group (required)
- `traits`: Array of trait objects, each with `name`, `data1` (group 1 values), `data2` (group 2 values)

**Run command:**

```bash
python scripts/academic_stats.py << 'JSON'
{
  "title": "...",
  "group1_name": "...",
  "group2_name": "...",
  "traits": [...]
}
JSON
```

### Step 3: Display the result

After the script outputs HTML, use `show_widget` to render the table inline.
Do NOT modify the HTML — use it as-is.

## Dependencies

- Python ≥ 3.8
- numpy, scipy

```bash
pip install numpy scipy
```

## Output format

The generated table uses a three-line academic table style:
- Top border: 2px solid
- Bottom border (last row): 2px solid
- Internal rows: 1px solid
- Header: light gray background
- Significance column: *** / ** / * / ns
- Footer: "n: biological replicates. Data are means ± s.e. Student's t-test; ***P < 0.001, **P < 0.01, *P < 0.05"

## Statistical methods

| Method | Detail |
|--------|--------|
| Mean | Arithmetic mean |
| s.e. | Standard error = SD / √n |
| t-test | Welch's t-test (unequal variance), one-tailed (group 2 > group 1) |
| Significance | *** P < 0.001, ** P < 0.01, * P < 0.05, ns: not significant |
| Rounding | Means and s.e. rounded to 2 decimal places |

## Notes

- Always use one-tailed t-test (assume group 2 > group 1)
- Keep trait names in English for publication readiness
- When data comes from an image, read it carefully and verify all values before running the script
