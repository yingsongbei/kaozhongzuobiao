# academic-stats-table

从原始数据生成学术论文风格统计表格的 Python 工具，可作为 WorkBuddy Skill 使用。
支持 HTML 和 Excel 两种输出格式。

## 功能

输入两组实验数据，自动计算：

- **均值** (mean)
- **标准误** (s.e. = SD / sqrt(n))
- **Student's t 检验**（单尾，等方差）
- **显著性标注**（***/ **/ * / ns）

输出英文学术三线表格式的 HTML 或 Excel，可直接用于论文、补充表或报告。

## 三线表格式

默认采用严格三线表格式：

1. **表头/基因名上方**：粗线
2. **表头/基因名下方**：细线
3. **最后一个表型/性状下方**：粗线
4. 其他地方不加线条：
   - 不要竖线
   - 不要表型行之间的内部横线
   - 不要注释区边框
   - 不要类似 Excel 网格的全表格线

表格结构为：

| Trait | Group 1 | n | Group 2 | n | Sig. |
|-------|---------|---|---------|---|------|
| Trait name | mean ± s.e. | n | mean ± s.e. | n | * |

- HTML 输出：表头上方 2px 横线、表头下方 1px 横线、最后一个性状下方 2px 横线，字体为 Times New Roman
- Excel 输出：表头行 `top=medium, bottom=thin`，最后一行 `bottom=medium`，中间行无边框，全局 Times New Roman

## 依赖

- Python >= 3.8
- numpy
- scipy
- openpyxl（Excel 输出用）

```bash
pip install numpy scipy openpyxl
```

## 用法

### 输入格式（JSON）

```json
{
  "title": "Table 1. Comparison of traits between groups",
  "group1_name": "Wild-type",
  "group2_name": "Mutant",
  "traits": [
    {
      "name": "Plant height (cm)",
      "data1": [10.2, 11.5, 9.8],
      "data2": [14.3, 15.1, 13.9]
    },
    {
      "name": "Grain weight (g)",
      "data1": [2.1, 2.3, 2.0],
      "data2": [3.1, 3.3, 3.0]
    }
  ]
}
```

### HTML 输出

```bash
python scripts/academic_stats.py << 'JSON'
{
  "title": "Table 1. Comparison of traits between groups",
  "group1_name": "Wild-type",
  "group2_name": "Mutant",
  "traits": [
    {
      "name": "Plant height (cm)",
      "data1": [10.2, 11.5, 9.8],
      "data2": [14.3, 15.1, 13.9]
    }
  ]
}
JSON
```

### Excel 输出

在 Python 中导入 `calc_stats` 函数，结合 `openpyxl` 生成 Excel 文件：

```python
import sys
sys.path.insert(0, "scripts")
from academic_stats import calc_stats
import openpyxl

# 计算统计量
result = calc_stats(data_group1, data_group2, "Trait name")

# result 包含: trait, n1, n2, mean1, mean2, sem1, sem2, p_one, sig, t_stat
```

### 输出示例

```text
Table 1. Comparison of traits between groups

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Trait                 Wild-type   n   Mutant      n   Sig.
────────────────────────────────────────
Plant height (cm)     10.50 ± 0.49 3   14.43 ± 0.35 3   *
Grain weight (g)       2.13 ± 0.09 3    3.13 ± 0.09 3   **
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

n: biological replicates.
Data are means ± s.e. (standard error). Student's t-test; ***P < 0.001, **P < 0.01, *P < 0.05
```

## 字段说明

| 字段 | 必填 | 说明 |
|------|:----:|------|
| `title` | Yes | 表格标题 |
| `group1_name` | Yes | 对照/参考组名称 |
| `group2_name` | Yes | 处理/测试组名称 |
| `traits` | Yes | 性状数组，每个含 `name`（性状名）、`data1`（组1数据）、`data2`（组2数据） |

## 统计方法

| 方法 | 说明 |
|------|------|
| 均值 | 算术平均值 |
| 标准误 | 标准差 / sqrt(n) |
| t 检验 | Student's t-test（等方差，`equal_var=True`），单尾检验（假设组2 > 组1） |
| 显著性 | *** P < 0.001, ** P < 0.01, * P < 0.05, ns 不显著 |
| 舍入 | 均值和标准误保留两位小数 |

## 文件结构

```
academic-stats-table/
├── SKILL.md                    # Skill 定义和工作流说明
└── scripts/
    └── academic_stats.py       # 统计计算 + HTML 输出
```

## 与 WorkBuddy 配合

本工具支持作为 [WorkBuddy](https://www.codebuddy.cn/) 的 Skill 使用。将整个 `academic-stats-table/` 目录放入 `~/.workbuddy/skills/` 下即可自动注册。

## 许可

MIT
