#!/usr/bin/env python
"""
Academic statistics table generator.

Computes mean ± s.e. and one-tailed Student's t-test for two-group comparisons
across multiple traits, then outputs an HTML table in publication-ready format.
"""

import numpy as np
from scipy import stats
import json
import sys


def calc_stats(data1, data2, trait_name):
    """Calculate statistics for a single trait."""
    n1, n2 = len(data1), len(data2)
    mean1, mean2 = np.mean(data1), np.mean(data2)
    std1, std2 = np.std(data1, ddof=1), np.std(data2, ddof=1)
    sem1, sem2 = std1 / np.sqrt(n1), std2 / np.sqrt(n2)

    # One-tailed Student's t-test (equal variance assumed)
    t_stat, p_two = stats.ttest_ind(data2, data1, equal_var=True)
    p_one = p_two / 2 if t_stat > 0 else 1 - p_two / 2

    if p_one < 0.001:
        sig = "***"
    elif p_one < 0.01:
        sig = "**"
    elif p_one < 0.05:
        sig = "*"
    else:
        sig = "ns"

    return {
        "trait": trait_name,
        "n1": n1,
        "n2": n2,
        "mean1": round(mean1, 2),
        "mean2": round(mean2, 2),
        "sem1": round(sem1, 2),
        "sem2": round(sem2, 2),
        "p_one": p_one,
        "sig": sig,
        "t_stat": t_stat,
    }


def generate_html_table(results, title, group1_name, group2_name):
    """Generate HTML table in academic publication format."""
    html_parts = []

    html_parts.append(
        '<table style="width:100%; border-collapse:collapse;'
        'font-family:Times New Roman, serif; font-size:13px;">'
    )
    html_parts.append(
        f'  <caption style="font-size:14px; font-weight:500;'
        f'margin-bottom:12px; text-align:left;">{title}</caption>'
    )
    html_parts.append("  <thead>")
    html_parts.append(
        '    <tr style="border-top:2px solid #333; border-bottom:1px solid #333;">'
    )
    html_parts.append(
        '      <th style="padding:10px; text-align:left;'
        'font-weight:600;">Trait</th>'
    )
    html_parts.append(
        f'      <th style="padding:10px; text-align:center;'
        f'font-weight:600;">{group1_name}</th>'
    )
    html_parts.append(
        '      <th style="padding:10px; text-align:center;'
        'font-weight:600;">n</th>'
    )
    html_parts.append(
        f'      <th style="padding:10px; text-align:center;'
        f'font-weight:600;">{group2_name}</th>'
    )
    html_parts.append(
        '      <th style="padding:10px; text-align:center;'
        'font-weight:600;">n</th>'
    )
    html_parts.append(
        '      <th style="padding:10px; text-align:center;'
        'font-weight:600;"></th>'
    )
    html_parts.append("    </tr>")
    html_parts.append("  </thead>")
    html_parts.append("  <tbody>")

    for i, r in enumerate(results):
        # Strict three-line table: no inner horizontal rules; only bottom rule on the last trait row.
        border = "2px solid #333" if i == len(results) - 1 else "none"
        html_parts.append(f'    <tr style="border-bottom:{border};">')
        html_parts.append(
            f'      <td style="padding:10px; text-align:left;'
            f'font-weight:500;">{r["trait"]}</td>'
        )
        html_parts.append(
            f'      <td style="padding:10px; text-align:center;">'
            f'{r["mean1"]:.2f} ± {r["sem1"]:.2f}</td>'
        )
        html_parts.append(
            f'      <td style="padding:10px; text-align:center;">'
            f'{r["n1"]}</td>'
        )
        html_parts.append(
            f'      <td style="padding:10px; text-align:center;">'
            f'{r["mean2"]:.2f} ± {r["sem2"]:.2f}</td>'
        )
        html_parts.append(
            f'      <td style="padding:10px; text-align:center;">'
            f'{r["n2"]}</td>'
        )
        html_parts.append(
            f'      <td style="padding:10px; text-align:center;'
            f'font-weight:bold; font-size:15px;">{r["sig"]}</td>'
        )
        html_parts.append("    </tr>")

    html_parts.append("  </tbody>")
    html_parts.append("</table>")

    html_parts.append(
        '<p style="font-size:12px; color:#666; margin-top:12px;'
        'line-height:1.6;">'
    )
    html_parts.append("n: biological replicates.<br>")
    html_parts.append(
        "Data are means ± s.e. (standard error)."
        " Student's t-test; ***P < 0.001, **P < 0.01, *P < 0.05"
    )
    html_parts.append("</p>")

    return "\n".join(html_parts)


def main():
    """Read JSON input from stdin, output HTML."""
    input_data = json.load(sys.stdin)

    title = input_data.get("title", "Table 1. Comparison of traits between groups")
    group1_name = input_data.get("group1_name", "Group 1")
    group2_name = input_data.get("group2_name", "Group 2")
    traits = input_data["traits"]  # list of {name, data1, data2}

    results = []
    for trait in traits:
        r = calc_stats(trait["data1"], trait["data2"], trait["name"])
        results.append(r)

    html = generate_html_table(results, title, group1_name, group2_name)
    print(html)


if __name__ == "__main__":
    main()
