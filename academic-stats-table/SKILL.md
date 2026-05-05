---
name: academic-stats-table
description: "Generate publication-ready academic statistics tables from raw data. When the user asks to create a two-group comparison table with means ± s.e., t-test significance, and strict three-line English academic formatting, use this skill."
agent_created: true
---

# academic-stats-table — Academic Statistics Table Generator

Generate publication-ready English statistical tables from raw numeric data.
Outputs a two-group comparison table with mean ± s.e., sample size (n),
and one-tailed Student's t-test significance markings.

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

### Step 3: Output format

Determine the output format based on user request:
- **HTML (default)**: Run the script, capture its HTML output, render with `show_widget`.
- **Excel**: Import `calc_stats` from `scripts/academic_stats.py`, use it with `openpyxl` to build a strict three-line table (see Excel output rules below). Write a self-contained Python script that reads the CSV, groups data, calls `calc_stats`, and writes the Excel file.

### Step 4: Display the result

- HTML: Use `show_widget` to render inline. Do NOT modify the HTML.
- Excel: Use `open_result_view` to present the file. Clean up temporary scripts after running.

## Dependencies

- Python ≥ 3.8
- numpy, scipy
- openpyxl (for Excel output)

```bash
pip install numpy scipy openpyxl
```

## Output format

The generated table must use a strict three-line academic table style:
- Top thick rule: place above the group-name/header row (e.g. above `HHZ | n | HHZ-25Q | n`).
- Middle thin rule: place directly below the group-name/header row.
- Bottom thick rule: place below the last phenotype/trait row.
- Do not draw any other rules: no vertical borders, no inner horizontal rules between phenotype rows, no borders around footnotes, and no grid-style table lines.
- Put `mean ± s.e.` in one cell, then `n` in a separate column: `Trait | Group 1 | n | Group 2 | n | Sig.`.
- Prefer Times New Roman for Excel/table outputs when matching manuscript supplementary table style.
- Significance column: *** / ** / * / ns, unless the target journal/example uses a different display.
- Footer example: "n: Number of biological replicates. Data are presented as means ± s.e.. Student's t-test; *P < 0.05, **P < 0.01".

## Statistical methods

| Method | Detail |
|--------|--------|
| Mean | Arithmetic mean |
| s.e. | Standard error = SD / √n |
| t-test | Student's t-test (equal variance, `equal_var=True`), one-tailed (group 2 > group 1) |
| Significance | *** P < 0.001, ** P < 0.01, * P < 0.05, ns: not significant |
| Rounding | Means and s.e. rounded to 2 decimal places |

## Excel output rules

When creating an Excel version with `openpyxl`, apply the same strict three-line table style to the statistics sheet:
- Clear all existing borders in the table and footnote area first.
- Apply `top=thick` and `bottom=thin` only to the group-name/header row.
- Apply `bottom=thick` only to the final phenotype/trait row.
- Leave all other cells borderless, including phenotype rows between the header and final row, empty separator rows, and footnotes.
- Avoid merged mean/s.e. subheaders unless explicitly requested; default to `mean ± s.e.` in one cell and `n` in a separate column.
- Use Times New Roman for all cells (headers, data, footnotes).
- After generating, clean up any temporary Python scripts.

## Notes

- Always use one-tailed t-test (assume group 2 > group 1)
- Keep trait names in English for publication readiness
- When data comes from an image, read it carefully and verify all values before running the script
