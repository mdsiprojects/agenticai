_An [article](https://blog.context.ai/comparing-leading-multi-agent-frameworks/) from April 18, 2024, provides a detailed comparison of several leading multi-agent frameworks for large language models (LLMs). 🔍

The review covers five major frameworks:

🚀 **AutoGen**: Praised for its active community and customizable agents, but noted for its complexity and less structured nature.

🧠 **MetaGPT**: Excels in complex agent interactions with a rich library of predefined agents, though it heavily relies on asyncio and may lack generalizability.

👥 **CrewAI**: Designed for production use with a focus on agent delegation, but has limits on re-delegation and collects anonymized usage data.

📊 **LangGraph**: Uses a graph representation for agent connections, enhancing efficiency but has a complex setup and is limited in broad tasks.

💾 **AutoGPT**: Strong in memory and context management but depends on visual builders for application design.

The article emphasizes the importance of a robust evaluation framework to ensure effective functioning and continuous improvement of these multi-agent systems. ⚖️
_

Playground UI and SDK support:

- OpenAI's Agents SDK and Playground: https://openai.com/index/new-tools-for-building-agents/
- Autogen: https://devblogs.microsoft.com/autogen/autogen-reimagined-launching-autogen-0-4/



Others:
- n8n https://n8n.io/ai/ : workflows powered with AI Agents
- crewAI : https://www.crewai.com open source library and enterprise product for building multi agent systems

Samples:
- Google's Agent Starter Pack: https://github.com/GoogleCloudPlatform/agent-starter-pack
- Shilpa Jain's Timeseries Forecasting Agent: https://github.com/ShilJain/Azure_AI_Agent_Service_workshop/


Comparison between *AutoGen* and *CrewAI*:
- Flexibility vs. User-Friendliness: AutoGen provides more flexibility and control for advanced developers, while CrewAI offers a structured approach suitable for business users.
- Workflow Suitability: CrewAI is suited for structured, role-based research workflows, whereas AutoGen excels at adaptive, evolving prompts.
- Dynamic Feedback: AutoGen can self-correct code errors through iterative learning, while CrewAI lacks this dynamic feedback loop.
- Unique Features: CrewAI has a modular design and task delegation between agents, while AutoGen supports containerized code execution for safety.



additional resources:
- Large Language Model based Multi-Agents: A Survey of Progress and Challenges: https://arxiv.org/abs/2402.01680