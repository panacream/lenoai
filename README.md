# Leno AI: Modular Multi-Agent AI Platform

Welcome to **Leno AI** – a modular, open-source multi-agent AI framework for educational purposes designed for developers, engineers, and researchers to build, extend, and experiment with advanced AI agents. Featuring seamless integration with the [Google Agent Development Kit (ADK)](https://github.com/google-deepmind/agentkit), Leno AI enables robust orchestration, real-world tool use, and rapid prototyping of agent-based workflows.

---

## 🚀 Project Overview
- **Multi-Agent System:** Compose, orchestrate, and manage multiple specialized AI agents (e.g., Stock Agent, Coding Agent, Social Media Agent, etc.).
- **Extensible Architecture:** Easily add new sub-agents and custom tools.
- **Real-World Tooling:** Agents interact with APIs, databases, and external services (e.g., Alpaca for trading, OpenAI for coding, etc.).
- **Best Practices:** Built on Google ADK for session management, tool invocation, and agent communication.

---

## ✨ Features
- Modular sub-agent design (each with its own logic, tools, and instructions)
- Real-time and historical stock trading (via Alpaca API)
- Coding, scraping, social media, and more
- Easy integration with Google ADK WebUI and CLI
- Clear agent instructions and confirmation flows for safe operations
- Robust error handling and developer-friendly logging

---

## 🛠️ Tech Stack
- **Backend:** Python 3, FastAPI, Uvicorn
- **Agents:** Google ADK (LlmAgent, Runner, etc.)
- **Frontend:** React (Vite), Tailwind CSS (see `/frontend`)
- **Database:** MongoDB (optional, for persistent storage)
- **APIs:** Alpaca, OpenAI, yfinance, etc.

---

## 🏗️ Architecture

```
[ React Frontend ]  <->  [ FastAPI Python Backend ]  <->  [ Sub-Agents (Google ADK) & Tools ]
```

---

## 📦 Installation & Setup

1. **Clone the Repository**
   ```sh
   git clone https://github.com/yourusername/agent4.git
   cd agent4
   ```

2. **Create and Activate a Python Virtual Environment**
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Python Dependencies**
   ```sh
   pip install -r manager/requirements.txt
   ```

4. **Set Up Environment Variables**
   - Copy `.env.example` to `.env` and fill in your API keys (Alpaca, OpenAI, etc.).
   - Example variables:
     ```env
     ALPACA_API_KEY=your_key
     ALPACA_API_SECRET=your_secret
     ALPACA_BASE_URL=https://paper-api.alpaca.markets
     OPENAI_API_KEY=your_openai_key
     PORT=3001
     ```

5. **(Optional) Frontend Setup**
   ```sh
   cd frontend
   npm install
   npm run dev
   ```

---

## 🔑 Google Authentication Walkthrough (Google APIs)

To enable Google API features (Gmail, Sheets, Docs, Calendar, Drive, YouTube, etc.), you need to authenticate with Google and generate a local OAuth token file using `gmail_oauth_setup.py`.

### 1. **Set Up Google Cloud Credentials**
- Go to the [Google Cloud Console](https://console.cloud.google.com/apis/credentials).
- Create a new project (or select an existing one).
- Enable the APIs you want to use (e.g., Gmail API, Google Sheets API, Calendar API, etc.).
- Create OAuth 2.0 credentials:
  - Application type: Desktop app
  - Download the `credentials.json` file and place it in your project root (or as specified in your agent code).

### 2. **Specify Your Desired API Scopes**
- Open `gmail_oauth_setup.py`.
- Edit the `SCOPES` list to include the permissions you need. Example scopes:
  ```python
  SCOPES = [
      'https://www.googleapis.com/auth/gmail.send',           # Gmail send
      'https://www.googleapis.com/auth/gmail.readonly',       # Gmail read
      'https://www.googleapis.com/auth/spreadsheets',         # Google Sheets
      'https://www.googleapis.com/auth/documents',            # Google Docs
      'https://www.googleapis.com/auth/calendar',             # Google Calendar
      'https://www.googleapis.com/auth/drive',                # Google Drive
      'https://www.googleapis.com/auth/youtube',              # YouTube
  ]
  ```
- Add or remove scopes based on the APIs your agent/tools require. See the [Google API OAuth 2.0 Scopes](https://developers.google.com/identity/protocols/oauth2/scopes) for a full list.

### 3. **Run the OAuth Setup Script**
- In your terminal, run:
  ```sh
  python gmail_oauth_setup.py
  ```
- Follow the instructions in the browser to grant access to your Google account.
- Upon completion, a token file (e.g., `token.json`) will be generated in your project directory. This file stores your access and refresh tokens securely.

### 4. **Verify the Token File**
- Ensure the token file exists in your project root.
- Your agents can now access the chosen Google APIs using this token (no need to re-authenticate unless you delete or revoke the token).

**Note:**
- Never commit your OAuth token, `credentials.json`, or `gmail_oauth_setup.py` to public repositories.
- Add `gmail_oauth_setup.py` to your `.gitignore` file to ensure it is not pushed to the repo.
- For more details, see the [Google API Python Quickstart](https://developers.google.com/gmail/api/quickstart/python) and [Google API Scopes](https://developers.google.com/identity/protocols/oauth2/scopes).

---

## 🧑‍💻 Creating New Sub-Agents & Tools

**Sub-Agents:**
- Create a new folder under `manager/sub_agents/` (e.g., `my_agent/`).
- Add `agent.py`, `tools/`, `utils/`, and `docs/` as needed.
- Define your agent as a subclass or instance of `LlmAgent`.
- Write clear instructions in `docs/MY_AGENT_INSTRUCTIONS.md`.
- Register your tools in the agent’s `tools` list.

**Tools:**
- Place tool functions in `tools/` (e.g., `tools/my_tools.py`).
- Each tool should have a docstring, type annotations, and robust error handling.
- Follow Google ADK’s [tool registration best practices](https://google.github.io/adk-docs/tools/).

**Best Practices:**
- Keep tools atomic and stateless when possible.
- Use environment variables for credentials.
- Document all agent instructions and tool signatures.

---

## 🧪 Testing Agents with Google ADK (WebUI & CLI)

### 1. **Using the Google ADK WebUI**
- Launch the WebUI:
  ```sh
  adk web
  ```
- Select your agent (e.g., `stock_agent`) and interact via the browser.
- Test all tools and flows before frontend/UI integration.

### 2. **Using the Google ADK CLI**
- Run an agent session directly from the CLI:
  ```sh
  adk run <agent_name>
  ```
- Try various tool calls and session flows.

**Note:** See `google_adk.txt` in the repo for a local snapshot of the ADK documentation, or visit the [official Google ADK docs](https://github.com/google-deepmind/agentkit) for the latest updates.

---

## 🖥️ Demo on the Frontend UI
- After verifying agent logic via WebUI/CLI, start the backend server:
  ```sh
  python manager/server.py
  ```
- Start the frontend (see above), and interact with your agents through the web interface.
 ```sh
  npm run dev
 ```

---

## 🤝 Contributing
- Fork the repo and create a feature branch.
- Follow the existing agent and tool structure.
- Write clear docstrings and update agent instructions.
- Test your additions with the ADK WebUI/CLI before submitting a PR.
- Open issues or discussions for feature ideas and improvements!

---

## 📚 References
- [Google ADK Documentation](https://github.com/google-deepmind/agentkit)
- See `./manager/docs/google_adk.txt` in this repo for a local copy of the ADK docs
- [Alpaca API Docs](https://alpaca.markets/docs/)
- [OpenAI API Docs](https://platform.openai.com/docs/)
- [Google Gemini Docs](https://developers.google.com/gemini/)
- [Google Cloud Console](https://console.cloud.google.com/)

---

**Leno AI** is open-source and community-driven. We welcome your ideas, issues, and pull requests!
- Configure `.env` for secrets/API keys as needed.

---

## Configuration & Customization

### Actionable Task Detection (For the history tab of the frontend UI)
- **File:** `src/config/actionableTasksConfig.ts`
- **How:**
  - Edit the `ACTIONABLE_TASK_KEYWORDS` array to add/remove phrases.
  - Or, customize the `isActionableTask(agentContent)` function for advanced logic.

### Branding
- All agent-facing UI is branded as "Leno AI" (edit in `src/components/AgentChat.tsx`, `src/pages/Index.tsx`).

### Adding New Agents/Integrations
- Add new Python sub-agents in `manager/sub_agents/` and register them in `manager/agent.py`.

---

## Project Structure

```
agent4/
├── src/
│   ├── components/         # React components (UI)
│   ├── hooks/              # React hooks (chat, logs)
│   ├── config/             # Configurable logic (actionable tasks)
│   ├── lib/                # API utilities
│   ├── pages/              # Main app pages
├── manager/                # Python backend (FastAPI, agents)
│   ├── sub_agents/         # Specialized agent modules
├── requirements.txt        # Python backend dependencies
├── README.md
```

---

## Technologies Used
- **Frontend:** React, TypeScript, Vite, shadcn-ui, Tailwind CSS
- **Backend:** Python, FastAPI, Google APIs, Web3, Selenium, Playwright, gspread, PyGithub, etc. (see `requirements.txt`)

---

## Actionable Task Logging
- All significant actions performed by Leno AI are logged and viewable in the History tab.
- Logs include: task, agent, status, timestamp, and output/result.
- Export logs as CSV from the UI.

---

## License
MIT (or specify your own)

---

## Contributing
Pull requests and issues welcome! Please open an issue to discuss major changes.
