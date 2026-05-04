# SMS 论文编码智能体

基于 LangGraph 的智能体，用于系统映射研究（SMS）中对 **Agentic Software Systems** 相关论文进行自动编码。

## 环境要求

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- SiliconFlow API Key（使用 DeepSeek-V3 模型）

## 安装

```bash
cd coding-agent
uv sync
# 在 config.py 中填入你的 API Key
```

## 使用方法

### 单篇论文

```bash
uv run python main.py path/to/paper.pdf
```

### 批量处理

```bash
uv run python main.py paper1.pdf paper2.pdf paper3.pdf
```

支持格式：`.pdf`、`.docx`、`.txt`

## 输出

| 文件 | 说明 |
|------|------|
| `result/<论文标题>.json` | 每篇论文的完整编码结果 |
| `result/summary.csv` | 所有已编码论文的汇总表 |

### JSON 结构

```json
{
  "paper_info": { "title", "authors", "year", "venue", "publication_type", "peer_reviewed", "open_source_artifact", "affiliation_region" },
  "included": true,
  "exclusion_reason": null,
  "coding": {
    "RQ1": {
      "Perception_ContextAcquisition": ["论文原文逐字引用..."],
      "Environment_Interaction": [],
      "Tool_CapabilityUse": [],
      "Memory_StateManagement": [],
      "Reasoning_Planning": [],
      "Action_Execution": [],
      "Feedback_Reflection": [],
      "Human_Collaboration": [],
      "Role_MultiagentCoordination": [],
      "Governance_Traceability": []
    },
    "RQ2": { "primary_form": "...", "secondary_form": null },
    "RQ3": { "application_domain", "task_context", "target_users", "digital_artifacts", "domain_tools" },
    "RQ4": { "evaluation_type", "benchmarks_datasets", "baselines", "metrics", "reproducibility", "validity_discussion", "domain_validation", "statistical_analysis" }
  }
}
```

RQ1 中的引用为**论文原文逐字摘录**，不做意译或改写。

## 项目结构

```
coding-agent/
├── config.py          # LLM 配置（API Key、模型名）
├── system_prompt.py   # SMS 编码框架系统提示词
├── tools.py           # read_paper + save_coding_result 工具
├── agent.py           # LangGraph 智能体
├── main.py            # 命令行入口（支持单篇/批量）
└── result/            # 输出目录（JSON + CSV）
```
