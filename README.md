# Connecting Language Models to Data Systems in the Energy Sector – An Evaluation of the Model Context Protocol (MCP)

[![](https://img.shields.io/badge/Lund_University-LTH-000080?labelColor=9C6114&logoColor=auto&logo=data:image/svg%2Bxml;base64,PHN2ZyB2aWV3Qm94PSIwIDAgMjAwIDIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSIxMDAiIGN5PSIxMDAiIHI9Ijg4IiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjYiLz48Y2lyY2xlIGN4PSIxMDAiIGN5PSIxMDAiIHI9Ijc3IiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiLz48dGV4dCB4PSIxMDAiIHk9IjExOCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1mYW1pbHk9InNlcmlmIiBmb250LXNpemU9IjcyIiBmb250LXdlaWdodD0iYm9sZCIgZmlsbD0iIzAwMDA4MCI+TFU8L3RleHQ+PC9zdmc+)](http://lup.lub.lu.se/student-papers/record/9224412)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![MCP Protocol](https://img.shields.io/badge/MCP-Protocol-green)](https://github.com/anthropics/mcp)

## Overview

MCP-Bench is an evaluation framework for assessing LLM tool-use capabilities via the Model Context Protocol (MCP). It connects LLMs to domain-specific MCP servers and measures their ability to discover, plan, and execute tool calls to solve complex tasks.

## MCP-Bench [![arXiv](https://img.shields.io/badge/arXiv-2508.20453-b31b1b.svg)](https://arxiv.org/abs/2508.20453)

This repository is an internal fork of the upstream MCP-Bench framework, extended with custom MCP servers, task sets, and model provider integrations. 

## Quick Start

### Installation

1. **Clone the repository**
```
git clone <repo-url>
cd mcp-bench-energy
```

2. **Install dependencies**
```
conda create -n mcpbench python=3.10
conda activate mcpbench
cd mcp_servers
bash ./install.sh
cd ..
```

3. **Set up environment variables**

Create a `.env` file in the project root:

```
# Judge model (always required — hardcoded to o4-mini in benchmark/runner.py)
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_API_KEY=...

# AI Gateway subject model
AI_GATEWAY_URL=...
AI_GATEWAY_API_KEY=...
AI_GATEWAY_DEPLOYMENT=...

# LM Studio local model
LOCAL_LLM_BASE_URL=http://localhost:1234/v1/
LOCAL_LLM_MODEL_NAME=phi-4-mini-instruct

# Databricks subject models
DATABRICKS_TOKEN=...
DATABRICKS_HOST=...
DATABRICKS_WORKSPACE_ID=...

# MCP server credentials
UK_POWERNETWORKS_API_KEY=...
```

### Basic Usage

```
# List available models (depends on which env vars are set)
python run_benchmark.py --list-models

# Run all tasks with a model
python run_benchmark.py --models ai-gateway

# Run a specific task file
python run_benchmark.py --models ai-gateway \
  --tasks-file tasks/uk/server_A_test_tasks.json

# Run UK multi-server tasks
python run_benchmark.py --models ai-gateway \
  --tasks-file tasks/uk/multiserver.json
```

### Key CLI Flags

| Flag | Purpose |
|---|---|
| `--models MODEL` or `all` | Which model(s) to benchmark |
| `--tasks-file PATH` | Specific task file (default: all task files) |
| `--output PATH` | Output file for results |
| `--distraction-count N` | Number of distraction servers per task |
| `--disable-judge-stability` | Skip multi-run LLM judge averaging |
| `--disable-fuzzy` | Use concrete task descriptions instead of fuzzy |
| `--enable-cache` | Enable tool call result caching |
| `--cache-ttl HOURS` | Cache TTL (0 = permanent) |
| `--verbose` | Extra logging |

## Model Providers

Four providers are supported. The model names shown are what you pass to `--models`.

| Provider | Model name(s) | Env vars required |
|---|---|---|
| **AI Gateway** | `ai-gateway` | `AI_GATEWAY_URL`, `AI_GATEWAY_API_KEY`, `AI_GATEWAY_DEPLOYMENT` |
| **LM Studio (local)** | `Phi-4-mini-instruct` | `LOCAL_LLM_BASE_URL`, `LOCAL_LLM_MODEL_NAME` |
| **Databricks** | `databricks-claude-sonnet-4-5`, `databricks-claude-sonnet-4` | `DATABRICKS_TOKEN`, `DATABRICKS_HOST`, `DATABRICKS_WORKSPACE_ID` |
| **Azure OpenAI** | judge only (hardcoded) | `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY` |

The judge model is hardcoded to `o4-mini` via Azure OpenAI in `benchmark/runner.py`. The Azure env vars are therefore always required regardless of which subject model is used.

To add a new model, edit `llm/factory.py` and add a `ModelConfig` entry in `get_model_configs()`:

```python
configs["my-model"] = ModelConfig(
    name="my-model",
    provider_type="openai",   # or "azure", "ai_gateway", "local", "databricks"
    api_key=os.getenv("MY_API_KEY"),
    base_url="https://...",
    model_name="provider/model-id"
)
```

## MCP Servers

This fork uses 6 custom local MCP servers. Server startup commands and working directories are defined in `mcp_servers/commands.json`.

| Server | Domain | Credentials required |
|---|---|---|
| `Server_X_test` | UK Power Networks | `UK_POWERNETWORKS_API_KEY` |

To verify all servers are reachable:
```
python utils/collect_mcp_info.py
```

## Task Files

Tasks are organized by domain under `tasks/`:

```
tasks/
├── uk/
│   ├── server_A_test_tasks.json
│   ├── server_B_test_tasks.json
│   ├── server_C_test_tasks.json
│   └── multiserver.json
```

Each task has a `task_description` (ground truth), a `fuzzy_description` (shown to the agent), `target_servers`, and a schema of expected tool calls.

## Caching

**Tool call cache** (`mcp_modules/tool_cache.py`): SQLite-based cache for individual MCP tool call results. Keyed by server name + tool name + arguments. Enabled with `--enable-cache`; TTL set with `--cache-ttl HOURS` (0 = permanent).

**Task cache** (`benchmark/task_cache.py`): SQLite-based cache for complete task execution results, so expensive benchmark tasks do not need to be re-run.

## Results and Analysis

- Results are written to timestamped JSON files in the project root by default.
- `average_script/script.py`: Combines results across multiple benchmark run JSON files with weighted averaging.
- `Graphs/`: Matplotlib scripts for generating bar charts from result JSON files.

## Project Structure

```
mcp-bench-energy/
├── agent/
│   ├── executor.py                  # Multi-round task executor
│   └── execution_context.py         # Execution state accumulation
├── benchmark/
│   ├── evaluator.py                 # LLM-as-judge evaluation
│   ├── runner.py                    # Benchmark orchestrator (judge hardcoded here)
│   ├── task_cache.py                # Task-level result cache
│   ├── results_aggregator.py        # Post-run statistics
│   └── results_formatter.py         # Results display
├── config/
│   ├── benchmark_config.yaml        # All tunable parameters
│   └── config_loader.py             # Config singleton
├── llm/
│   ├── factory.py                   # Model configs for all providers
│   └── provider.py                  # Unified async LLM interface
├── mcp_modules/
│   ├── connector.py                 # Per-server MCP connection
│   ├── server_manager_persistent.py # Persistent multi-server manager
│   └── tool_cache.py                # Tool call result cache
├── utils/
│   ├── collect_mcp_info.py          # Server discovery and verification
│   └── local_server_config.py       # Loads commands.json and api_key
├── tasks/                           # Benchmark task files (see above)
├── mcp_servers/
│   ├── commands.json                # Server startup commands
│   ├── install.sh                   # Dependency installer
│   └── api_key                      # Server-level API keys (not committed)
├── Graphs/                          # Bar chart generation scripts
├── average_script/
│   └── script.py                    # Multi-run result averaging
├── cache/                           # Auto-created cache directory
└── run_benchmark.py                 # Main entry point
```

## Acknowledgments

Built on the [Model Context Protocol](https://github.com/anthropics/mcp) by Anthropic and the upstream [MCP-Bench](https://github.com/accenture/mcp-bench) framework.
