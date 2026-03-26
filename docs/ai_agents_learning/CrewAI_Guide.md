# 🤖 CrewAI Complete Guide
> **Level:** Intermediate | **Language:** Hinglish | **Goal:** Master CrewAI framework

---

## 🧭 Core Concepts (Concept-First)

- Agents: Autonomous workers
- Tasks: Specific jobs
- Crews: Team of agents
- Tools: Agent capabilities

---

## 1. 👤 Agents & Tasks

```python
from crewai import Agent, Task, Crew

# Create agent
researcher = Agent(
    role='Research Analyst',
    goal='Find information about AI trends',
    backstory='Expert researcher',
    verbose=True
)

# Create task
research_task = Task(
    description='Research latest AI trends for 2024',
    agent=researcher,
    expected_output='Detailed report on AI trends'
)
```

---

## 2. 👥 Crew

```python
# Create another agent
writer = Agent(
    role='Content Writer',
    goal='Write engaging content',
    backstory='Expert writer'
)

# Create writing task
write_task = Task(
    description='Write article based on research',
    agent=writer
)

# Create crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    verbose=True
)

# Execute
result = crew.kickoff()
```

---

## ✅ Checklist

- [ ] CrewAI agents create kar sakte ho
- [ ] Tasks define kar sakte ho
- [ ] Crew execute kar sakte ho