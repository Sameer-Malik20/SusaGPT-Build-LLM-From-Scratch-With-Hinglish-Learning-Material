# 🕶️ Vibe Coding & AI Tool Safety (Codex, Cursor, Antigravity)
> **Level:** Beginner → Expert | **Goal:** Mastering AI-assisted coding without compromising Security or Architecture

---

## 📋 Is Guide Se Kya Seekhoge

| Topic | Importance |
|-------|------------|
| 1. Vibe Coding kya hai? | AI-driven development logic |
| 2. Security Risks (Secret Leakage) | Protecting API Keys in prompt history |
| 3. Hallucinated Vulnerabilities | AI-generated bug prevention |
| 4. Architecture Erosion | Keeping system design clean |
| 5. MCP (Model Context Protocol) | AI ko system context dena |
| 6. Best Practices for Vibe Coders | Productivity + Safety balance |

---

## 1. 🏗️ What is Vibe Coding?

Vibe Coding ka matlab hai **AI se high-level instructions dalkar poora code generate karwana** (Cursor, Antigravity, Github Copilot). 
Ye fast hai, lekin agar aapne code "Read" nahi kiya, toh production mein bade bugs aa sakte hain. 

---

## 🚨 2. Security Risks in AI Coding

Jab aap Cursor ya Antigravity use karte hain, toh AI ko aapka **पूरा Codebase** dikhta hai.

### A. Secret Leakage (The Biggest Risk)
Agar aapki `.env` file open hai ya code mein console.log mein keys hain, toh AI unhe apne training query mein bhej sakta hai.
- **Solution:** Always use `.gitignore` for `.env` files. Model ko "Context" dete waqt sensitive files exclude karein.

### B. Insecure Code Generation
AI hamesha "Working" code deta hai, "Secure" code nahi. 
- **Example:** Model `SELECT *` dalkar SQL Injection wala code generate kar sakta hai kyu ki wo simpler hai.

---

## 🏗️ 3. Architecture & System Design Erosion

AI hamesha "Current file" par focus karta hai. Wo poore system ka **Memory/Consistency** bhool sakta hai.
- **Problem:** AI naye services dalkar architecture ko "Spaghetti Code" bana deta hai.
- **Solution:** AI se code mangne se pehle use **System Design Spec** (Markdown file) hamesha context mein do.

---

## 🛠️ 4. MCP (Model Context Protocol): Strengthening AI

**MCP** ek naya standard hai (Anthropic/Cursor support) jo AI ko allow karta hai:
1. **Context Fetching:** Databases aur system logs ko AI se directly connect karna.
2. **Design Validation:** AI tool se puchna: "Kya ye naya component hamari `SusaGPT_Architecture.md` ke rules follow kar raha hai?"
3. **Security Audit:** "Find XSS vulnerabilities in this generated JS code."

---

## 🧪 5. Free Tools to Scan AI Generated Code

AI ne code likh diya? Ab in free tools se check karo:

1. **Snyk (Free Tier):** Code vulnerabilities aur library issues scan karne ke liye.
2. **Gitleaks:** Scan commit history for leaked API keys.
3. **SonarQube (Community):** Quality gate check karne ke liye.
4. **Semgrep:** Fast static analysis (Finds logic bugs).

---

## 📝 6. Vibe Coding Checklist (Final Advice)

- [ ] **Don't Copy-Paste Blindly:** AI ka code Line-by-Line read karo.
- [ ] **Sanity Check:** Kya AI ne koi deprecated library use kari hai?
- [ ] **Prompt Engineering:** AI ko bolo: "Generate this code keeping **Secure Coding Practices** in mind."
- [ ] **Log Everything:** AI ne kya change kiya, use Git history mein small commits mein track karo.

---

## 🧪 Exercises — Vibe Coding Challenge!

### Challenge 1: The AI Bug! ⭐⭐
**Scenario:** AI ne ek login function banaya jo `==` se password compare karta hai `Hash checking` ki jagah. 
Question: Aap ise production mein kyu nahi dalenge?
<details><summary>Answer</summary>
**Time-attack vulnerability** aur **Security basic breach**. Password plain text mein storage aur comparison unsafe hai. AI ne simplest code diya, secure nahi.
</details>

---

## 🔗 Resources
- [MCP Official Documentation](https://modelcontextprotocol.io/)
- [Vibe Coding Principles (Blog)](https://github.com/features/copilot)
- [Antigravity Security Guidelines](https://antigravity.google/docs/security)
