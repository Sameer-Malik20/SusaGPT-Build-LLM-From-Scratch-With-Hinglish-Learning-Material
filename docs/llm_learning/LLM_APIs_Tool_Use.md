# 🔧 LLM APIs & Tool Use - From Function Calling to Agent Frameworks
> **Level:** Intermediate → Expert | **Language:** Hinglish | **Goal:** LLM APIs, function calling, aur agent-based systems master karna

---

## 📋 Table of Contents: LLM Tool Ecosystem

| Component | Purpose | Key Technologies |
|-----------|---------|------------------|
| **API Design** | LLM capabilities expose karna | REST APIs, GraphQL, gRPC |
| **Function Calling** | LLMs ko external tools se connect karna | OpenAI Functions, Gemini Tools |
| **Agent Frameworks** | Autonomous systems build karna | LangChain, LlamaIndex, AutoGPT |
| **Tool Orchestration** | Tool execution manage karna | LangGraph, CrewAI, Microsoft Autogen |
| **Evaluation** | Agent performance measure karna | AgentBench, WebArena |

---

## 1. 🚀 LLM API Fundamentals

### A. REST API Patterns

#### OpenAI-style API:
```python
import openai

response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}],
    temperature=0.7,
    max_tokens=100
)
```

#### Key Parameters:
- **temperature:** Creativity control (0-2) - Kitna creative output
- **max_tokens:** Output length limit - Maximum kitne tokens
- **top_p:** Nucleus sampling - Probability distribution se sampling
- **presence_penalty:** Avoid repetition - Repetition rokne ke liye
- **frequency_penalty:** Reduce common phrases - Common phrases kam karne ke liye

### B. Streaming Responses
```python
stream = openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### C. Error Handling & Rate Limiting
```python
import time
from openai import RateLimitError

def robust_completion(messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            return openai.chat.completions.create(
                model="gpt-4", 
                messages=messages
            )
        except RateLimitError:
            wait_time = 2 ** attempt  # Exponential backoff
            time.sleep(wait_time)
    raise Exception("Max retries exceeded")
```

---

## 2. 🛠️ Function Calling & Tool Use

### A. Function Calling Kya Hai?
LLMs available tools describe karte hain, aur system unhe execute karta hai.

#### OpenAI Functions Schema:
```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                },
                "required": ["location"]
            }
        }
    }
]
```

### B. Complete Function Calling Flow

```python
def execute_with_tools(user_query, available_tools):
    # Step 1: LLM decide karta hai tools chahiye ya nahi
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_query}],
        tools=available_tools,
        tool_choice="auto"
    )
    
    # Step 2: Tool calls extract karo
    tool_calls = response.choices[0].message.tool_calls
    if tool_calls:
        # Step 3: Tools execute karo
        tool_results = []
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            # Actual function execute karo
            result = globals()[function_name](**function_args)
            tool_results.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": str(result)
            })
        
        # Step 4: Results wapas LLM ko bhejo
        messages = [
            {"role": "user", "content": user_query},
            response.choices[0].message,
            *tool_results
        ]
        
        final_response = openai.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        return final_response.choices[0].message.content
    
    return response.choices[0].message.content
```

### C. Multi-turn Tool Conversations
```python
class ToolConversation:
    def __init__(self):
        self.messages = []
        self.available_tools = [...]  # Aapke tool definitions
    
    def chat(self, user_message):
        self.messages.append({"role": "user", "content": user_message})
        
        while True:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=self.messages,
                tools=self.available_tools
            )
            
            assistant_message = response.choices[0].message
            self.messages.append(assistant_message)
            
            if not assistant_message.tool_calls:
                return assistant_message.content
            
            # Tools execute karo aur conversation continue karo
            for tool_call in assistant_message.tool_calls:
                # ... tool execution logic ...
                tool_result = execute_tool(tool_call)
                self.messages.append(tool_result)
```

---

## 3. 🤖 Agent Frameworks

### A. LangChain Agents
```python
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI

# Tools define karo
tools = [
    Tool(
        name="Search",
        func=search_api,
        description="Search for information"
    ),
    Tool(
        name="Calculator",
        func=calculator,
        description="Perform calculations"
    )
]

# Agent initialize karo
agent = initialize_agent(
    tools, 
    OpenAI(temperature=0), 
    agent="zero-shot-react-description", 
    verbose=True
)

# Execute
result = agent.run("What's the population of India times the GDP per capita?")
```

### B. LlamaIndex Agents
```python
from llama_index.agent import OpenAIAgent
from llama_index.tools import FunctionTool

# Tools ko FunctionTool objects ke roop mein define karo
search_tool = FunctionTool.from_defaults(fn=search_function)
calc_tool = FunctionTool.from_defaults(fn=calculator_function)

# Agent create karo
agent = OpenAIAgent.from_tools(
    [search_tool, calc_tool],
    verbose=True
)

# Agent use karo
response = agent.chat("Research renewable energy trends and summarize")
```

### C. ReAct (Reasoning + Acting) Pattern
```python
# ReAct prompt template
react_prompt = """
You are a helpful assistant that can use tools.
You have access to the following tools:

{tools}

To use a tool, respond with:
Thought: I need to use a tool
Action: tool_name
Action Input: {{"param": "value"}}

When you have the final answer, respond with:
Thought: I have the final answer
Final Answer: [your answer]

Begin!

Question: {question}
"""
```

---

## 4. 🔄 Multi-Agent Systems

### A. LangGraph for Multi-Agent Workflows
```python
from langgraph.graph import Graph
from langgraph.prebuilt import create_react_agent

# Different specialized agents define karo
research_agent = create_react_agent(llm, research_tools)
writing_agent = create_react_agent(llm, writing_tools)
review_agent = create_react_agent(llm, review_tools)

# Workflow graph create karo
workflow = Graph()
workflow.add_node("research", research_agent)
workflow.add_node("write", writing_agent)
workflow.add_node("review", review_agent)

# Edges define karo
workflow.add_edge("research", "write")
workflow.add_edge("write", "review")
workflow.add_edge("review", "__end__")

# Workflow execute karo
result = workflow.invoke({"question": "Write a report on AI ethics"})
```

### B. CrewAI: Role-based Agents
```python
from crewai import Agent, Task, Crew

# Roles ke saath agents define karo
researcher = Agent(
    role='Senior Research Analyst',
    goal='Find and analyze the latest AI trends',
    backstory='Expert in technology research'
)

writer = Agent(
    role='Technical Writer',
    goal='Write engaging technical content',
    backstory='Experienced technical writer'
)

# Tasks create karo
research_task = Task(
    description='Research AI trends in 2024',
    agent=researcher
)

write_task = Task(
    description='Write a blog post about AI trends',
    agent=writer
)

# Crew create aur run karo
crew = Crew(agents=[researcher, writer], tasks=[research_task, write_task])
result = crew.kickoff()
```

---

## 5. 📊 Tool & Agent Evaluation

### A. Tool Effectiveness Metrics
- **Tool selection accuracy:** Kya LLM sahi tool choose karta hai?
- **Parameter correctness:** Kya parameters correctly extract hote hain?
- **Execution success rate:** Kya tool execution successful hota hai?
- **Latency:** Query se final response tak ka time

### B. Agent Evaluation Frameworks

#### 1. AgentBench
```python
# Standardized tasks par evaluate karo
from agentbench import TaskSuite

suite = TaskSuite(["web_navigation", "coding", "reasoning"])
results = suite.evaluate(agent)
print(f"Overall score: {results['overall']}")
```

#### 2. Custom Evaluation
```python
def evaluate_agent(agent, test_cases):
    scores = []
    for case in test_cases:
        question, expected_tools = case
        response = agent(question)
        
        # Check karo kya correct tools use kiye gaye
        used_tools = extract_tools_from_response(response)
        score = len(set(used_tools) & set(expected_tools)) / len(expected_tools)
        scores.append(score)
    
    return sum(scores) / len(scores)
```

### C. Safety & Reliability
```python
class SafeAgent:
    def __init__(self, base_agent):
        self.agent = base_agent
        self.safety_checker = SafetyChecker()
    
    def run(self, query):
        # Safety check
        if not self.safety_checker.is_safe(query):
            return "I cannot help with that request."
        
        # Tool permission check
        allowed_tools = self.safety_checker.get_allowed_tools(query)
        
        # Restrictions ke saath run karo
        return self.agent.run(query, tools=allowed_tools)
```

---

## 6. 🚀 Production Deployment

### A. API Gateway Pattern
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    tools: list = []

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    agent = AgentManager.get_agent(request.tools)
    response = agent.chat(request.message)
    return {"response": response}
```

### B. Caching & Optimization
```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def cached_agent_response(query: str, tools_config: str) -> str:
    # Hash-based caching
    cache_key = hashlib.md5(f"{query}{tools_config}".encode()).hexdigest()
    return agent.chat(query)
```

### C. Monitoring & Observability
```python
import prometheus_client
from opentelemetry import trace

tracer = trace.get_tracer(__name__)
requests_counter = prometheus_client.Counter('agent_requests', 'Number of agent requests')

@app.post("/chat")
async def monitored_chat(request: ChatRequest):
    with tracer.start_as_current_span("agent_chat"):
        requests_counter.inc()
        # ... agent logic ...
```

---

## 7. 🧪 Practical Exercises

### Exercise 1: Personal Assistant Banayo
1. Calendar, email, aur web search ke liye tools create karo
2. Error handling ke saath function calling implement karo
3. Multi-turn interactions ke liye conversation memory add karo

### Exercise 2: Multi-Agent Research System
1. Researcher, analyst, aur writer agents create karo
2. Research pipeline ke liye LangGraph workflow implement karo
3. Quality control aur validation steps add karo

### Exercise 3: Tool Evaluation Framework
1. Tool selection accuracy ke liye test cases create karo
2. Automated evaluation metrics implement karo
3. Agent performance monitor karne ke liye dashboard banayo

---

## 📚 Resources

### Essential Libraries
- **LangChain:** Most popular agent framework
- **LlamaIndex:** Data-aware agents aur RAG
- **CrewAI:** Role-based multi-agent systems
- **AutoGPT:** Autonomous agent implementation
- **Microsoft Autogen:** Conversational multi-agent framework

### APIs & Platforms
- **OpenAI API:** Function calling, GPT-4 Turbo
- **Anthropic Claude:** Tool use, constitutional AI
- **Google Gemini:** Function calling, multimodal
- **Together AI:** Open-source model hosting

### Learning Resources
- **LangChain Documentation:** Comprehensive guides
- **OpenAI Cookbook:** Function calling examples
- **CrewAI Tutorials:** Multi-agent workflows
- **AgentBench:** Standardized evaluation

---

## 🏆 Checklist
- [ ] LLM services ke liye REST API implement kar sakte hain
- [ ] Function calling mechanics samajh mein aaye
- [ ] LangChain/LlamaIndex ke saath agents build kar sakte hain
- [ ] Multi-agent system design samajh mein aaya
- [ ] Agent performance evaluate kar sakte hain
- [ ] Agents ko production mein deploy kar sakte hain

> **Pro Tip:** Single-function agents se simple start karo. Jab zaroorat ho tab hi complexity add karo. Production systems ke liye hamesha proper error handling aur safety checks implement karo.