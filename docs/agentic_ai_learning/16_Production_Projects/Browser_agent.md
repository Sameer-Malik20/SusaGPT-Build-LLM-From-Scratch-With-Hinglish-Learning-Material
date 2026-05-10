# 🌐 Project: Autonomous Browser Agent (Intermediate)
> **Level:** Intermediate | **Goal:** Build an agent that can navigate websites, click buttons, and extract data just like a human using Playwright or Selenium.

---

## 🏗️ 1. Architecture
We use a **Vision-Language Model (VLM)** or **DOM-Parser** approach.
- **Engine:** Playwright (Headless browser).
- **Brain:** LLM that receives the "HTML DOM" or "Screenshot".
- **Actions:** Click, Type, Scroll, Wait.
- **Feedback Loop:** Action -> Observe New State -> Decide Next Action.

---

## 📂 2. Folder Structure
```text
browser_agent/
├── src/
│   ├── browser_engine.py  # Playwright setup
│   ├── parser.py          # HTML to Markdown/Text
│   └── agent_logic.py     # Decision making loop
├── recordings/            # Screenshots of agent actions
├── main.py
└── config.yaml
```

---

## 💻 3. Full Code (Core Logic)
```python
# Hinglish Logic: Browser kholo, page ka text nikaalo, aur AI se pucho 'Kahan click karna hai?'
from playwright.sync_api import sync_playwright

def browse_and_extract(url, goal):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        
        # 1. Get simplified DOM
        dom_text = page.content()[:5000] # Simplified for example
        
        # 2. Ask LLM for next action
        # action = llm.invoke(f"Goal: {goal}, DOM: {dom_text}. What is the CSS selector to click?")
        
        # 3. Perform action
        # page.click(action_selector)
        
        return "Task Completed"
```

---

## 🔍 4. Observability
- **Screenshot Traces:** Save a screenshot after every action to see where the agent got stuck.
- **Action Logs:** Record every selector clicked and every text typed.

---

## 📊 5. Evaluation
- **Success Rate:** % of navigation tasks completed without errors.
- **Step Efficiency:** Does the agent take 3 steps or 20 steps to reach the goal?

---

## 🛡️ 6. Security
- **Sandboxing:** Run the browser in a restricted container to prevent "Local File Access" exploits.
- **Sensitive Data:** Block the agent from visiting URLs like `localhost` or `169.254.169.254` (Cloud Metadata).

---

## 🚀 7. Deployment
- **Docker:** Needs a "Heavy" image with Playwright dependencies installed.
- **Environment:** Use **Browserless.io** or self-hosted Chromium clusters.

---

## 📈 8. Scaling
- **Parallel Browsing:** Use a task queue (Celery) to run 10 browser agents at once.
- **Session Reuse:** Keeping the browser open across multiple steps to avoid "Cold start" page loads.

---

## 💰 9. Cost Optimization
- **Text-only Mode:** Disable images and CSS to save bandwidth and token usage during DOM parsing.
- **DOM Pruning:** Only send "Interactive" elements (buttons, inputs) to the LLM.

---

## ⚠️ 10. Failure Handling
- **Anti-Bot Detection:** Use `stealth` plugins to avoid being blocked by Cloudflare/Captchas.
- **Element Not Found:** If a selector is missing, tell the agent to "Scroll Down" and try again.

---
