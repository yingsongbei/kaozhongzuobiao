# academic-stats-table

从原始数据生成学术论文风格统计表格的 Python 工具。

## 功能

输入两组实验数据，自动计算：
- **均值** (mean)
- **标准误** (s.e. = SD / sqrt(n))
- **Welch t 检验**（单尾，不等方差）
- **显著性标注**（***/ **/ * / ns）

输出英文学术三线表格式的 HTML，可直接用于论文或报告。

## 依赖

- Python >= 3.8
- numpy
- scipy

```bash
pip install numpy scipy
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

### 运行

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

### 输出示例

| Trait | Wild-type | n | Mutant | n | |
|-------|-----------|---|--------|---|---|
| Plant height (cm) | 11.20 ± 0.58 | 5 | 15.40 ± 0.51 | 5 | *** |
| Grain weight (g) | 2.20 ± 0.07 | 5 | 3.10 ± 0.07 | 5 | *** |

*n: biological replicates. Data are means ± s.e. Student's t-test; ***P < 0.001, **P < 0.01, *P < 0.05*

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
| t 检验 | Welch's t-test（不等方差），单尾检验（假设组2 > 组1） |
| 显著性 | *** P < 0.001, ** P < 0.01, * P < 0.05, ns 不显著 |
| 舍入 | 均值和标准误保留两位小数 |

## 与 WorkBuddy 配合

本工具支持作为 [WorkBuddy](https://www.codebuddy.cn/) 的 Skill 使用。将整个目录放入 `~/.workbuddy/skills/` 下即可自动注册。

## 许可

MIT
