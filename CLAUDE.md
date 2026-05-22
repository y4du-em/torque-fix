# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### From the monorepo root (pnpm + Turborepo)

```bash
pnpm dev            # start all apps concurrently
pnpm dev:web        # Next.js only (port 3000)
pnpm dev:api        # FastAPI only (port 8000) — alias for turbo filter
pnpm build          # production build (web)
pnpm type-check     # tsc --noEmit across all packages
pnpm lint           # eslint across all packages
```

### FastAPI (`apps/api`)

```bash
# First-time setup
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # then add ANTHROPIC_API_KEY

# Run
uvicorn app.main:app --reload --port 8000

# Lint + format
ruff check .
ruff format .

# Tests
pytest
pytest tests/test_foo.py::test_bar   # single test
```

### Next.js (`apps/web`)

```bash
pnpm dev        # uses --turbopack
pnpm build
pnpm type-check
pnpm lint
```

## Architecture

### Overview

Two apps share types and vehicle data via workspace packages:

```
packages/types        → shared TypeScript interfaces (VehicleContext, DiagnosisResponse, ChatMessage, …)
packages/vehicle-data → Indian vehicle database + symptomsByCategory + query utilities
packages/config       → tsconfig.base.json (strict, exactOptionalPropertyTypes), tailwind color tokens
apps/api              → FastAPI, calls Claude, exposes 2 endpoints
apps/web              → Next.js 15.3, consumes API, all state in Zustand
```

### `apps/api` — FastAPI

**Request flow:**

1. Router (`app/routers/`) receives and validates request via Pydantic models (`app/models/`)
2. Calls `app/services/claude_service.py` which holds two module-level clients:
   - `_sync_client` (`anthropic.Anthropic`) — used for `/diagnose` via `asyncio.to_thread`
   - `_async_client` (`anthropic.AsyncAnthropic`) — used for `/chat` streaming
3. Prompt builders in `app/prompts/` construct the system and user messages
4. `diagnose_vehicle()` parses the raw JSON string Claude returns and maps it to Pydantic models
5. `stream_chat()` is an async generator; the router wraps it in `StreamingResponse` (SSE format: `data: {chunk}\n\n`, terminated by `data: [DONE]\n\n`)

**Key constraint:** `POST /diagnose` instructs Claude via system prompt to return **raw JSON only** — no markdown fences. The parser calls `json.loads()` directly; a `JSONDecodeError` surfaces as HTTP 502.

**Settings** are loaded from `.env` by `pydantic-settings` (`app/config.py`). The module-level `settings` singleton is imported across the app — don't instantiate `Settings()` again elsewhere.

### `apps/web` — Next.js 15.3

**State management:** A single Zustand store (`src/lib/store.ts`, `useTorqueFixStore`) holds all app state: vehicle context, selected symptoms, diagnosis result, and chat messages. The `updateLastAssistantMessage` action is used for in-place streaming updates — it finds the last assistant message by index and replaces its content.

**Data flow for diagnosis:**
1. `useVehicleSelector` (local state hook) cascades type → make → model → year → fuel type; each setter resets all downstream fields. When `isComplete`, `VehicleSelector` calls `setVehicleContext` in the store.
2. `useDiagnosis` hook reads store state, calls `diagnoseVehicle()` from `src/lib/api-client.ts`, then navigates to `/results`.
3. `useChat` hook calls `streamChat()` (async generator parsing SSE), accumulating chunks into the last assistant message via `updateLastAssistantMessage`.

**Tailwind v4** — configured entirely through CSS variables in `src/app/globals.css` using `@theme inline`. There is no `tailwind.config.ts`. Brand orange tokens are `brand-500` (`#f97316`) and `brand-600` (`#ea580c`).

**TypeScript strictness:** The base tsconfig enables `exactOptionalPropertyTypes`. This means you cannot pass `prop: value | undefined` to an optional field typed as `prop?: value` — you must either omit the key or use conditional spreading: `...(value && { prop: value })`.

**shadcn/ui** components live in `src/components/ui/` (added via `pnpm dlx shadcn@latest add`). Import from `@/components/ui/<name>`, not from `shadcn` or `radix-ui` directly.

**Server vs client components:** `src/app/page.tsx` (landing) is a server component. Any component using hooks, the Zustand store, or browser APIs needs `"use client"` at the top.

### `packages/vehicle-data`

Exports `vehicleData` (array of `VehicleMake`), `symptomsByCategory` (keyed by `SymptomCategory`), and five pure query functions (`getMakesByType`, `getModelsByMake`, `getYearsByModel`, `getMakeById`, `getModelById`). The dataset covers Indian vehicles only (Honda, Yamaha, Royal Enfield, KTM, Bajaj, TVS, Maruti Suzuki, Hyundai, Tata, Toyota). Add new makes/models to the `vehicleData` array in `packages/vehicle-data/src/index.ts`.
