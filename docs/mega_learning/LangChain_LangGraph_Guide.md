# Filename: LangChain_LangGraph_Guide.md

# LangChain aur LangGraph: AI Frameworks (Complete Guide)

LLM applications banane ke liye LangChain aaj ke waqt mein standard ban gaya hai. Jab complex automation / agents ki zaroorat hoti hai tab hum LangGraph use karte hain.

## 1. LangChain: Connectivity ka Maalik
LangChain kya hai? Ye bas ek framework hai jo LLMs (OpenAI, Anthropic, Gemini) ko databases, code executors, aur knowledge bases se connect karta hai. Isme concepts hain:
- **Chains:** Multi-step sequences jo inputs lekar outputs deti hain.
- **Agents:** Jo khud decide karte hain kaunsa tool use karna hai.
- **Tools:** LLM ko function calling access dene ke liye (search, calculator, code run).

## 2. LLMChain — Simple AI Pipeline
Ab ke version mein `RunnableSequence` (LangChain Expression Language - LCEL) use hoti hai.

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Model initialize karna
llm = ChatOpenAI(model="gpt-3.5-turbo")
prompt = ChatPromptTemplate.from_template("Explain {topic} in Hinglish.")
parser = StrOutputParser()

# Simple Chain Pipeline
chain = prompt | llm | parser
# result = chain.invoke({"topic": "Quantum Computing"})
```

## 3. Memory — Yaad Rakhne wali AI
LLMs by default stateless hote hain. LangChain memory add karke context save rakhta hai.

```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm=llm, 
    memory=memory,
    verbose=True
)

# conversation.predict(input="Hi, mera naam Susa hai.")
# conversation.predict(input="Mera naam kya hai?") # AI will remember!
```

## 4. Tools — Custom Agentic Power
Tools model ko superpowers dete hain. Aap custom tools bana sakte hain.

```python
from langchain.tools import tool

@tool
def get_stock_price(symbol: str) -> str:
    """Useful to get the current price of a stock."""
    # Logic to fetch stock price
    return f"The price of {symbol} is $150."

# Now LLM can choose this tool if needed
```

## 5. ReAct Agent — Reasoning aur Acting
Agents khud decision lete hain steps automate karne ke liye.

```python
from langchain.agents import create_react_agent, AgentExecutor
# tools = [get_stock_price, DuckDuckGoSearchRun()]
# agent = create_react_agent(llm, tools, prompt)
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
# agent_executor.invoke({"input": "Apple ka stock price kya hai?"})
```

## 6. LangGraph Intro: State Machines
LangGraph LangChain ka advance form hai. Ye workflow ko nodes (tasks) aur edges (flow) mein divide karta hai. Isme "State" hamesha maintain rehti hai.

## 7. Multi-Step Research Agent: Practical workflow
LangGraph mein hum graph compile karte hain.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence

class AgentState(TypedDict):
    messages: Sequence[str]

# Graph Initialization
workflow = StateGraph(AgentState)

# Add nodes (logic blocks)
# workflow.add_node("agent", call_model)
# workflow.add_node("action", call_tool)

# Add edges (directions)
# workflow.add_edge("agent", "action")
# workflow.set_entry_point("agent")
# app = workflow.compile()
```

## 8. Mini Project: PDF Chatbot with Memory
Is project mein hum: 
1. `PyPDFLoader` se PDF read karenge.
2. `ChromaDB` mein store karenge.
3. `ConversationalRetrievalChain` se question-answer chat banayenge with memory.

```python
# pseudo-code overview
# loader = PyPDFLoader("document.pdf")
# pages = loader.load_and_split()
# vectorstore = Chroma.from_documents(pages, OpenAIEmbeddings())
# qa = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever(), memory=memory)
# query = "What is the summary of this report?"
# result = qa.invoke({"question": query})
```
