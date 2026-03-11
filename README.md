# google-adk-v1

Google ADK Sample demos

## Copilot Notes:

The term **“pydantic”** in the context of the Agent Development Kit (ADK) documentation refers to the use of [Pydantic](https://docs.pydantic.dev/)—a Python library for data validation and settings management using Python type annotations. Here's how it's applied throughout the ADK modules:

---

### 🧠 What Is Pydantic Doing Here?

Pydantic is used to define and validate structured data models for agents, contexts, configurations, and events. In ADK, many classes inherit from `BaseModel`, which is the core class provided by Pydantic.

---

### 📦 Key Roles of Pydantic Models in ADK

#### 1. **Agent Definitions**

- Classes like `BaseAgent`, `LlmAgent`, `LoopAgent`, `ParallelAgent`, and `SequentialAgent` are all Pydantic models.
- These models define fields such as:
  - `name`: validated to be a unique Python identifier.
  - `description`: used for routing decisions.
  - `callbacks`: lists of functions to run before or after agent execution.

#### 2. **Invocation Context**

- `InvocationContext` is a Pydantic model that encapsulates the state of a single agent invocation.
- It includes fields like:
  - `agent`: the current agent.
  - `session`: session metadata.
  - `end_invocation`: flag to terminate the run.

#### 3. **Event Tracking**

- `Event` and `EventActions` are Pydantic models used to log interactions between agents and users.
- They store metadata like timestamps, authorship, and function calls.

#### 4. **Code Execution**

- Executors like `BaseCodeExecutor`, `BuiltInCodeExecutor`, and `ContainerCodeExecutor` use Pydantic to define configuration fields (e.g., retry attempts, delimiters).

#### 5. **Runtime Configuration**

- `RunConfig` is a Pydantic model that controls agent behavior during execution (e.g., max LLM calls, streaming mode, transcription settings).

---

### ✅ Benefits of Using Pydantic in ADK

- **Validation**: Ensures fields like agent names and callback formats are correct.
- **Serialization**: Easily convert models to JSON for logging or transmission.
- **Extensibility**: Developers can subclass and override methods like `from_config()` or `model_post_init()` for custom behavior.

---
