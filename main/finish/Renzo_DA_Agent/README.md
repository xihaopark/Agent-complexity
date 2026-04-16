# Renzo - LangGraph-Based Data Analysis Agent

A general-purpose data analysis agent system with a minimalist frontend, built on LangGraph state machine architecture.

## Overview

Renzo is a next-generation data analysis platform that combines:
- **State Machine Architecture**: LangGraph-based orchestration with intelligent routing
- **Dual-Agent Execution**: Inspired by LAMBDA (Programmer + Inspector loop)
- **Structured Planning**: Adapted from Agentic Data Scientist orchestration patterns
- **Docker Sandbox**: Safe code execution with automatic dependency management
- **Minimalist UI**: Clean, distraction-free interface for data analysis

## Features

- 🎨 **Minimalist Design**: Clean, distraction-free interface with a monochrome color scheme
- 📁 **File Upload**: Drag-and-drop support for CSV, Excel, and JSON files
- 💬 **Chat Interface**: Conversational interaction with the agent
- 📊 **Real-time Visualization**: Display execution results and data insights
- 💻 **Code Viewer**: Monaco editor for viewing generated code
- 📈 **Progress Tracking**: Visual progress indicator for multi-step analyses
- 📚 **Session History**: Save and restore previous analysis sessions

## Tech Stack

- **Frontend**: React 18 + TypeScript + Vite
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Communication**: WebSocket + REST API
- **Backend**: FastAPI
- **Deployment**: Docker + Docker Compose

## Quick Start

Renzo is now self-contained at the repository level: Docker startup does not require `../biomni` or `../workflow_pool`.

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.10+ (for local development)

### Using Docker (Recommended)

1. Initialize environment defaults (optional but recommended):

```bash
cd renzo
cp .env.example .env
```

2. Build and start the containers:

```bash
docker-compose up --build -d
```

3. Access the application (Docker-first defaults):
   - Frontend: http://localhost:13000
   - Backend API: http://localhost:18000
   - API Docs: http://localhost:18000/docs
   - Health: http://localhost:18000/api/health
   - Ready: http://localhost:18000/api/ready

4. Run smoke checks:

```bash
./scripts/smoke.sh
```

**Quick restart (no rebuild):** After changing `.env` or only `app/` code, run `./scripts/quick_restart.sh`. After changing `backend/` or `frontend/` code, run `./scripts/update.sh` (incremental build). See QUICKSTART.md for the full table.

**External / LAN access:** In `.env` set `BIND_IP=0.0.0.0` (default). Then open the app using the server’s IP instead of localhost, e.g. `http://<server-ip>:13000` (frontend) and `http://<server-ip>:18000` (API). To listen only on one NIC, set `BIND_IP=<that-ip>`.

### Local Development

Use local mode only when you explicitly need Vite hot-reload and direct Python process debugging.

```bash
cd renzo
./start_local.sh start
```

Default local URLs:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

Stop/status/logs:

```bash
./start_local.sh stop
./start_local.sh status
./start_local.sh logs
```

### Manual Local Startup (optional)

#### Backend (manual)

```bash
cd renzo/backend
python3 -m pip install -r requirements.txt
python3 -m uvicorn api_gateway:app --host 0.0.0.0 --port 8000
```

#### Frontend (manual)

```bash
cd renzo/frontend
npm install
npm run dev
```

## Usage

1. **Upload Data**: Drag and drop a CSV, Excel, or JSON file onto the upload area
2. **Start Analysis**: Type your analysis request in the chat interface
3. **View Results**: See real-time progress, generated code, and execution results
4. **Save Session**: Sessions are automatically saved and can be accessed from the sidebar

## API Endpoints

- `POST /api/upload` - Upload data files
- `POST /api/chat` - Send messages to the agent
- `GET /api/health` - Liveness
- `GET /api/ready` - Readiness with runtime dependency checks
- `GET /api/sessions` - List all sessions
- `GET /api/sessions/{id}` - Get session details
- `DELETE /api/sessions/{id}` - Delete a session
- `WS /ws/{session_id}` - WebSocket for real-time updates

## Project Structure

```
renzo/
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── stores/        # Zustand stores
│   │   ├── api/           # API client
│   │   └── App.tsx        # Main app component
│   ├── Dockerfile
│   └── nginx.conf
├── backend/               # FastAPI backend
│   ├── api_gateway.py    # Main API server
│   ├── requirements.txt
│   └── Dockerfile
├── app/                   # Renzo agent code
├── data/                  # Data storage
│   ├── uploads/          # Uploaded files
│   └── artifacts/        # Generated outputs
└── docker-compose.yml
```

## Design Philosophy

The interface follows a "minimalist" (性冷淡风) design philosophy:

- **Colors**: Monochrome palette with a single accent color
- **Typography**: Clean sans-serif fonts with clear hierarchy
- **Layout**: Generous whitespace and simple, intuitive navigation
- **Interactions**: Direct and immediate feedback

## Development

### Adding New Components

1. Create component in `frontend/src/components/`
2. Import and use in `App.tsx`
3. Update state management in `stores/agentStore.ts` if needed

### Extending the API

1. Add new endpoints in `backend/api_gateway.py`
2. Update API client in `frontend/src/api/client.ts`
3. Update types and store as needed

## License

MIT
