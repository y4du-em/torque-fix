# TorqueFix

AI-powered auto mechanic helper. Select your vehicle, describe the symptoms, and get expert repair guidance — tools, parts, and step-by-step instructions — powered by Claude AI.

## Monorepo Structure

```
torquefix/
├── apps/
│   ├── web/          # Next.js 15.3 + React 19 frontend
│   └── api/          # FastAPI 0.115 + Python 3.12 backend
├── packages/
│   ├── types/        # Shared TypeScript types
│   ├── vehicle-data/ # Vehicle database + symptom categories
│   ├── config/       # Shared tsconfig and Tailwind base config
│   └── ui/           # Shared UI package (shadcn base)
├── turbo.json
└── pnpm-workspace.yaml
```

## Requirements

- Node.js 22 (see `.nvmrc`)
- pnpm 9
- Python 3.12 (see `.python-version`)

## Getting Started

### 1. Install dependencies

```bash
pnpm install
```

### 2. Set up the API

```bash
cd apps/api
python3.12 -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
# Edit .env and set ANTHROPIC_API_KEY
```

### 3. Run both apps

```bash
# From monorepo root — starts both web and API
pnpm dev

# Or individually:
pnpm dev:web   # Next.js on http://localhost:3000
pnpm dev:api   # FastAPI on http://localhost:8000
```

## Scripts

| Command | Description |
|---|---|
| `pnpm dev` | Start all apps in dev mode |
| `pnpm dev:web` | Start frontend only |
| `pnpm dev:api` | Start API only (alias for uvicorn) |
| `pnpm build` | Production build |
| `pnpm type-check` | TypeScript type checking |
| `pnpm lint` | ESLint across all packages |

## Features

- **Vehicle selector** — Cascading make/model/year/fuel selection for 10 Indian brands
- **Symptom picker** — 8 categories with 8+ symptoms each
- **AI diagnosis** — Claude-powered analysis with tools, parts, and repair steps
- **Streaming chat** — Follow-up questions answered in real time via SSE
- **Dark UI** — shadcn/ui components with brand orange accent

## Environment Variables

### API (`apps/api/.env`)

```
ANTHROPIC_API_KEY=your_key_here
MODEL_NAME=claude-sonnet-4-20250514
CORS_ORIGINS=["http://localhost:3000"]
ENVIRONMENT=development
```

### Web (`apps/web/.env.local`)

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```
