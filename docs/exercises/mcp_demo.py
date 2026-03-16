"""
╔══════════════════════════════════════════════════════════╗
║      🔌  MCP — Model Context Protocol Interactive Demo   ║
║      Docs: docs/ai/MCP_Guide.md                          ║
╚══════════════════════════════════════════════════════════╝

Run: python mcp_demo.py
No extra dependencies required!
"""

import os
import json
import time

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# ─────────────────────────────────────────────────────────
# Simulated MCP Server (Notes)
# ─────────────────────────────────────────────────────────

class NotesMCPServer:
    """Simulated MCP Notes Server"""

    def __init__(self):
        self.name = "notes-mcp-server"
        self.version = "1.0"
        self.notes_db = {}
        self.next_id = 1
        self.call_log = []

        # Define tools (MCP standard schema)
        self.tools = [
            {
                "name": "create_note",
                "description": "Nayi note create karo",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Note ka title"},
                        "content": {"type": "string", "description": "Note ka content"},
                        "tags": {"type": "array", "description": "Tags list (optional)"}
                    },
                    "required": ["title", "content"]
                }
            },
            {
                "name": "search_notes",
                "description": "Notes me search karo",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search kya karna hai"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "list_all_notes",
                "description": "Saari notes ki list do",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "delete_note",
                "description": "Note delete karo",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "note_id": {"type": "string", "description": "Delete karne wali note ID"}
                    },
                    "required": ["note_id"]
                }
            },
            {
                "name": "get_note",
                "description": "Specific note padho",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "note_id": {"type": "string", "description": "Note ID"}
                    },
                    "required": ["note_id"]
                }
            }
        ]

        # Resources
        self.resources = [
            {
                "uri": "notes://all",
                "name": "All Notes",
                "description": "Saari notes ka collection",
                "mimeType": "application/json"
            }
        ]

        # Prompts
        self.prompts = [
            {
                "name": "summarize_notes",
                "description": "Notes ko summarize karo",
                "template": "In notes ko concise bullet points me summarize karo:\n{notes}"
            }
        ]

    # ── Tool Handlers ──────────────────────────────────────

    def create_note(self, title, content, tags=None):
        note_id = f"note_{self.next_id:03d}"
        self.next_id += 1
        self.notes_db[note_id] = {
            "id": note_id,
            "title": title,
            "content": content,
            "tags": tags or [],
        }
        self.call_log.append(f"CREATE: '{title}'")
        return {"success": True, "note_id": note_id,
                "message": f"Note '{title}' bana diya! (ID: {note_id})"}

    def search_notes(self, query):
        results = []
        for note in self.notes_db.values():
            q = query.lower()
            if (q in note["title"].lower() or
                    q in note["content"].lower() or
                    any(q in tag.lower() for tag in note["tags"])):
                results.append(note)
        self.call_log.append(f"SEARCH: '{query}' → {len(results)} results")
        return {"results": results, "count": len(results), "query": query}

    def list_all_notes(self):
        notes = list(self.notes_db.values())
        self.call_log.append(f"LIST: {len(notes)} notes")
        return {"notes": notes, "total": len(notes)}

    def delete_note(self, note_id):
        if note_id in self.notes_db:
            title = self.notes_db[note_id]["title"]
            del self.notes_db[note_id]
            self.call_log.append(f"DELETE: '{title}' ({note_id})")
            return {"success": True, "message": f"'{title}' delete ho gaya!"}
        else:
            return {"success": False, "error": f"Note '{note_id}' nahi mila!"}

    def get_note(self, note_id):
        if note_id in self.notes_db:
            return {"success": True, "note": self.notes_db[note_id]}
        return {"success": False, "error": f"'{note_id}' nahi mila!"}

    # ── Main Request Handler ───────────────────────────────

    def handle_request(self, method, params):
        """MCP JSON-RPC style request handle karo"""
        if method == "tools/list":
            return {"tools": self.tools}
        elif method == "resources/list":
            return {"resources": self.resources}
        elif method == "prompts/list":
            return {"prompts": self.prompts}
        elif method == "tools/call":
            tool_name = params.get("name")
            args = params.get("arguments", {})
            if tool_name == "create_note":
                result = self.create_note(**args)
            elif tool_name == "search_notes":
                result = self.search_notes(**args)
            elif tool_name == "list_all_notes":
                result = self.list_all_notes()
            elif tool_name == "delete_note":
                result = self.delete_note(**args)
            elif tool_name == "get_note":
                result = self.get_note(**args)
            else:
                result = {"error": f"Tool '{tool_name}' not found!"}
            return {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}]}
        return {"error": "Unknown method"}


# ─────────────────────────────────────────────────────────
# DEMO 1: MCP Architecture Overview
# ─────────────────────────────────────────────────────────
def demo_architecture():
    clear()
    print("=" * 60)
    print("  🏛️   DEMO 1: MCP Architecture — How It Works")
    print("=" * 60)

    print("""
  MCP (Model Context Protocol) ka flow:

  👤 User
    ↓  request deta hai
  🖥️  Host App (Claude/IDE/Custom App)
    ↓  MCP Client banata hai
  🔌 MCP Client
    ↓  JSON-RPC protocol se baat karta hai
  ⚙️  MCP Server (ye demo!)
    ↓  Tools / Resources / Prompts expose karta hai
  📁 External Systems (DB, Files, APIs)
    ↓  actual data laata hai
  ← Result wapas host tak
""")

    print("  ─────────────────────────────────────────────────────")
    print("  Ek typical MCP request (JSON-RPC format):\n")

    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "create_note",
            "arguments": {
                "title": "Python Tips",
                "content": "List slicing is very powerful!",
                "tags": ["python", "tips"]
            }
        }
    }
    print("  REQUEST:")
    print("  " + json.dumps(request, indent=4).replace("\n", "\n  "))

    response = {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "content": [{"type": "text", "text": '{"success": true, "note_id": "note_001"}'}]
        }
    }
    print("\n  RESPONSE:")
    print("  " + json.dumps(response, indent=4).replace("\n", "\n  "))

    print("\n  ✅ Standard JSON-RPC = predictable, structured communication!")


# ─────────────────────────────────────────────────────────
# DEMO 2: Live MCP Server
# ─────────────────────────────────────────────────────────
def demo_live_server():
    clear()
    print("=" * 60)
    print("  🚀  DEMO 2: Live Notes MCP Server — Chal Raha Hai!")
    print("=" * 60)

    server = NotesMCPServer()

    print(f"\n  ✅ Server '{server.name}' v{server.version} started!")
    print(f"\n  Initialization — Capabilities negotiate kar rahe hain:")
    time.sleep(0.5)
    print(f"    Client → Server: 'initialize' request")
    time.sleep(0.3)
    capabilities = server.handle_request("tools/list", {})
    print(f"    Server → Client: {len(capabilities['tools'])} tools available")
    resources = server.handle_request("resources/list", {})
    print(f"    Server → Client: {len(resources['resources'])} resources available")
    prompts = server.handle_request("prompts/list", {})
    print(f"    Server → Client: {len(prompts['prompts'])} prompts available")
    print(f"\n  Session established! 🤝\n")
    time.sleep(0.5)

    # Pre-defined demo sequence
    demo_calls = [
        ("tools/call", {"name": "create_note", "arguments":
            {"title": "Python Basics", "content": "Variables, loops, functions are core.", "tags": ["python", "basics"]}}),
        ("tools/call", {"name": "create_note", "arguments":
            {"title": "ML Notes", "content": "Gradient descent minimizes loss function.", "tags": ["ml", "math"]}}),
        ("tools/call", {"name": "create_note", "arguments":
            {"title": "Python Advanced", "content": "Decorators, generators, context managers.", "tags": ["python", "advanced"]}}),
        ("tools/call", {"name": "search_notes", "arguments": {"query": "python"}}),
        ("tools/call", {"name": "list_all_notes", "arguments": {}}),
    ]

    print("  🔄 Demo calls executing:\n")
    for i, (method, params) in enumerate(demo_calls, 1):
        tool_name = params.get("name", "?")
        args = params.get("arguments", {})
        arg_preview = list(args.values())[0] if args else ""
        if isinstance(arg_preview, dict):
            arg_preview = arg_preview.get("title", "")

        print(f"  Call {i}: {method} → {tool_name}('{str(arg_preview)[:30]}')")
        result = server.handle_request(method, params)
        result_text = json.loads(result["content"][0]["text"]) if "content" in result else result
        print(f"  Result: {json.dumps(result_text, ensure_ascii=False)[:80]}")
        print()
        time.sleep(0.4)

    print(f"  📋 Server Call Log:")
    for log in server.call_log:
        print(f"    📝 {log}")


# ─────────────────────────────────────────────────────────
# DEMO 3: Interactive MCP Client
# ─────────────────────────────────────────────────────────
def demo_interactive_client():
    clear()
    print("=" * 60)
    print("  🎮  DEMO 3: MCP Client — Tum Ho Client, Server Se Baat Karo!")
    print("=" * 60)

    server = NotesMCPServer()
    print(f"\n  ✅ Server connected! Tools available hai.\n")

    # Pre-populate with some notes
    server.create_note("Sample Note 1", "Ye ek demo note hai", ["demo"])
    server.create_note("Python Tips", "f-strings bahut useful hain", ["python"])

    while True:
        print(f"\n{'─'*50}")
        print(f"  Notes in DB: {len(server.notes_db)}")
        print(f"\n  Available Tools:")
        for i, tool in enumerate(server.tools, 1):
            print(f"    {i}. {tool['name']} — {tool['description']}")
        print(f"    0. Exit")

        try:
            choice = input(f"\n  Tool choose karo (0-{len(server.tools)}): ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if choice == "0":
            break

        try:
            tool_idx = int(choice) - 1
        except ValueError:
            continue

        if tool_idx < 0 or tool_idx >= len(server.tools):
            print("  ❌ Invalid tool!")
            continue

        tool = server.tools[tool_idx]
        print(f"\n  🔧 Tool: {tool['name']}")
        print(f"  Schema: {json.dumps(tool['inputSchema']['properties'], ensure_ascii=False)}")

        # Collect parameters
        params = {}
        for param_name, param_info in tool['inputSchema']['properties'].items():
            required = param_name in tool['inputSchema'].get('required', [])
            req_marker = " (required)" if required else " (optional, Enter=skip)"
            val = input(f"  {param_name}{req_marker}: ").strip()
            if val:
                if param_info.get("type") == "array":
                    params[param_name] = [t.strip() for t in val.split(",")]
                else:
                    params[param_name] = val
            elif required:
                print(f"  ❌ '{param_name}' required hai!")
                params = None
                break

        if params is None:
            continue

        # Make the call
        print(f"\n  📤 Sending request to server...")
        result = server.handle_request("tools/call", {"name": tool["name"], "arguments": params})

        if "content" in result:
            result_data = json.loads(result["content"][0]["text"])
            print(f"\n  📥 Server Response:")
            print(f"  {json.dumps(result_data, ensure_ascii=False, indent=4)}")
        else:
            print(f"  Error: {result}")


# ─────────────────────────────────────────────────────────
# EXERCISE + TEST
# ─────────────────────────────────────────────────────────
def exercise():
    clear()
    print("=" * 60)
    print("  ✏️   EXERCISE: MCP Concepts Test")
    print("=" * 60)

    questions = [
        {
            "q": "Q1: MCP me 'Tool' aur 'Resource' ka fark?",
            "options": ["A) Koi fark nahi",
                        "B) Tool action karta hai (side effects), Resource sirf data deta hai",
                        "C) Resource action karta hai, Tool data deta hai",
                        "D) Tool free hai, Resource paid"],
            "answer": "B",
            "exp": "Tools = actions with side effects (file create, email send). Resources = read-only data!"
        },
        {
            "q": "Q2: MCP kis protocol par based hai?",
            "options": ["A) REST API", "B) GraphQL", "C) JSON-RPC", "D) gRPC"],
            "answer": "C",
            "exp": "MCP JSON-RPC style communication use karta hai — structured requests aur responses."
        },
        {
            "q": "Q3: MCP 'initialization' phase me kya hota hai?",
            "options": ["A) Model train hota hai",
                        "B) Client aur server capabilities negotiate karte hain",
                        "C) User login karta hai",
                        "D) Data delete hota hai"],
            "answer": "B",
            "exp": "Initialization me client aur server agree karte hain: kaunsa version, kya-kya tools/resources supported."
        },
        {
            "q": "Q4: 'stdio' transport kab use karte hain MCP me?",
            "options": ["A) Remote network calls ke liye",
                        "B) Streaming data ke liye",
                        "C) Local process integration ke liye (same machine)",
                        "D) Authentication ke liye"],
            "answer": "C",
            "exp": "stdio = local process communication (stdin/stdout). Fast, no network overhead!"
        },
    ]

    score = 0
    for q in questions:
        print(f"\n{'─'*55}")
        print(f"\n  {q['q']}")
        for opt in q["options"]:
            print(f"    {opt}")
        ans = input(f"\n  Answer (A/B/C/D): ").strip().upper()
        if ans == q["answer"]:
            print(f"  ✅ SAHI! 🎉")
            score += 1
        else:
            print(f"  ❌ Galat! Sahi: {q['answer']}")
        print(f"  💡 {q['exp']}")

    total = len(questions)
    print(f"\n{'='*55}")
    print(f"  📊 Score: {score}/{total}  {'⭐'*score}{'☆'*(total-score)}")
    if score == total:
        print("  🏆 PERFECT! MCP crystal clear hai!")
    else:
        print("  📖 MCP_Guide.md + demos phir se dekho!")


# ─────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────
def main():
    while True:
        clear()
        print("=" * 60)
        print("  🔌  MCP — Model Context Protocol Demo")
        print("  📄  Ref: docs/ai/MCP_Guide.md")
        print("=" * 60)
        print()
        print("    1. 🏛️   MCP Architecture Overview (JSON-RPC dekho)")
        print("    2. 🚀   Live Notes MCP Server (auto demo)")
        print("    3. 🎮   Interactive MCP Client (tum control karo!)")
        print("    4. ✏️   MCP MCQ Test (score dekho!)")
        print()
        print("    0. 🔙  Back / Exit")
        print()

        choice = input("  Choice (0-4): ").strip()

        if choice == "1":
            demo_architecture()
            input("\n↩️  Enter dabao...")
        elif choice == "2":
            demo_live_server()
            input("\n↩️  Enter dabao...")
        elif choice == "3":
            demo_interactive_client()
            input("\n↩️  Enter dabao...")
        elif choice == "4":
            exercise()
            input("\n↩️  Enter dabao...")
        elif choice == "0":
            break
        else:
            print("❌ Invalid!")
            input("Enter dabao...")


if __name__ == "__main__":
    main()
