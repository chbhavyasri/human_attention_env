#  Human Attention Optimization Environment (HAOE)

**A Production-Grade OpenEnv simulation for AI-driven cognitive load management.**

##  The Vision
In the modern "Attention Economy," the primary bottleneck to productivity is not computing power—it's human cognitive bandwidth. **HAOE** is a sophisticated simulation environment designed to train and evaluate AI agents that act as "Cognitive Air Traffic Controllers." Instead of just managing tasks, the agent must optimize for a human's **Flow State** and **Fatigue Levels**.

##  Key Technical Features
- **Cognitive Fidelity:** Models real-world psychological concepts including **Attention Residue** (the cost of switching) and **Flow State Accumulation** (deep work efficiency).
- **OpenEnv Compliance:** Strictly follows the OpenEnv specification with typed Pydantic models for Observations, Actions, and Rewards.
- **AI-Driven Decision Making:** Uses **Meta-Llama-3-8B** via the Hugging Face Inference API for high-level reasoning.
- **Production Security:** Implements industry-standard **Environment Variable Secret Management** to handle API authentication securely.

##  System Architecture

### 1. Observation Space (The Human State)
- `attention`: (0-100) Represents the current "Flow State." Higher values increase work efficiency.
- `fatigue`: (0-100) Represents cognitive drain. High fatigue leads to massive efficiency penalties.
- `tasks`: A dynamic list of pending work with priorities and deadlines.
- `time`: Discrete steps tracking the progression of the workday.

### 2. Action Space
- `FOCUS`: Engage in deep work on the current task. Builds attention but adds moderate fatigue.
- `SWITCH`: Change focus to a new task. Resets attention to 0 (Context Switching Penalty).
- `BREAK`: Sacrifices time to drastically reduce fatigue.

### 3. Reward Logic
- **Dense Normalized Rewards:** Every step returns a reward between `0.0` and `1.0`, ensuring compatibility with standardized Reinforcement Learning evaluators.

##  Standardized Benchmarks

| Task ID | Difficulty | Target Score | Description |
| :--- | :---: | :---: | :--- |
| **ATTENTION_EASY** | 0.2 | 0.90 | Single task with a generous deadline. |
| **ATTENTION_MEDIUM** | 0.6 | 0.75 | Multiple tasks requiring strategic context switching. |
| **ATTENTION_HARD** | 0.9 | 0.55 | Extreme load with rapid deadlines and high fatigue. |

## Getting Started

### 1. Prerequisites
- Python 3.10+
- Hugging Face Access Token

### 2. Installation
```bash
pip install -r requirements.txt