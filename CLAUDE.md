# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Testing mandate

**Every code change must include tests. No exceptions.**

| What you add or change | Where to add tests |
|---|---|
| Utility function (`src/lib/`) | `src/lib/__tests__/<file>.test.ts` |
| Zustand store action | `src/lib/__tests__/store.test.ts` |
| React hook (`src/hooks/`) | `src/hooks/__tests__/<hookName>.test.ts` |
| FastAPI route (`app/routers/`) | `apps/api/tests/test_routers.py` |
| Pydantic model (`app/models/`) | `apps/api/tests/test_models.py` |
| Prompt builder (`app/prompts/`) | `apps/api/tests/test_prompts.py` |
| Claude service function | `apps/api/tests/test_claude_service.py` |
| `vehicle-data` query function | `packages/vehicle-data/src/__tests__/index.test.ts` |
| Bug fix | Write a failing test reproducing the bug first, then fix |

Run the relevant suite before considering any task done:

```bash
pnpm test:web    # after changes to apps/web or packages/vehicle-data
pytest           # after changes to apps/api (venv must be active)
pnpm test        # full suite from monorepo root
```

---

## Commands

### Monorepo root

```bash
pnpm dev / dev:web / dev:api    # start apps (web=3000, api=8000)
pnpm build / type-check / lint  # production build, tsc, eslint
pnpm test / test:web / test:vehicle-data
```

### FastAPI (`apps/api`)

```bash
python3.12 -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"
cp .env.example .env   # add ANTHROPIC_API_KEY
uvicorn app.main:app --reload --port 8000
ruff check . && ruff format .
pytest                                              # all
pytest tests/test_routers.py::test_health_endpoint # single test
pytest -k "test_diagnose"                          # keyword filter
```

### Next.js (`apps/web`)

```bash
pnpm dev / build / type-check / lint
pnpm test                                                      # single pass
pnpm test:watch                                                # watch mode
pnpm vitest run src/lib/__tests__/store.test.ts                # single file
pnpm vitest run --reporter=verbose -t "accumulates all chunks" # by test name
```

---

## Test patterns

### TypeScript / Vitest

Every test follows **Arrange → Act → Assert** with a blank line between phases. Always reset the store in `beforeEach`:

```typescript
beforeEach(() => { useTorqueFixStore.getState().resetAll(); vi.clearAllMocks(); });
```

Mock `api-client` at module level. Use `vi.hoisted` for values referenced inside `vi.mock` factories (e.g. a router push spy):

```typescript
const mockRouterPush = vi.hoisted(() => vi.fn());
vi.mock("next/navigation", () => ({ useRouter: () => ({ push: mockRouterPush }) }));
vi.mock("@/lib/api-client", () => ({ diagnoseVehicle: vi.fn(), streamChat: vi.fn() }));
```

Async generator helper for `streamChat`:

```typescript
function makeStream(...chunks: string[]) {
  return (async function* () { for (const c of chunks) yield c; })();
}
// Error path:
(streamChat as Mock).mockImplementation(async function* () { throw new Error("fail"); });
```

### Python / pytest

`conftest.py` sets `ANTHROPIC_API_KEY` via `os.environ.setdefault` **before any app import** — do not change this order. Mock at the service boundary:

```python
with patch("app.services.claude_service._sync_client") as mock_sync, \
     patch("app.services.claude_service._async_client") as mock_async: ...

# Router tests: patch the service function, not the client
with patch("app.routers.diagnosis.diagnose_vehicle", return_value=sample_diagnosis): ...
```

---

## Architecture

```
packages/types        → shared TS interfaces (VehicleContext, DiagnosisResponse, ChatMessage, …)
packages/vehicle-data → Indian vehicle DB + symptomsByCategory + query utilities
packages/config       → tsconfig.base.json (strict, exactOptionalPropertyTypes)
apps/api              → FastAPI: 2 endpoints (/diagnose, /chat)
apps/web              → Next.js 15.3: all state in Zustand
```

**API request flow:** Router → Pydantic model validation → `claude_service.py` (two module-level clients: `_sync_client` for `/diagnose` via `asyncio.to_thread`, `_async_client` for `/chat` streaming) → prompt builders. `/diagnose` expects **raw JSON** from Claude; `JSONDecodeError` → 502. `/chat` uses SSE: `data: {chunk}\n\n`, terminated by `data: [DONE]\n\n`.

**Web data flow:** `useVehicleSelector` (cascading type→make→model→year→fuelType, each setter clears downstream) → `useDiagnosis` (calls `diagnoseVehicle`, navigates to `/results`) → `useChat` (streams via `updateLastAssistantMessage` which finds the last assistant message backwards and replaces its content).

**Key constraints:**
- `exactOptionalPropertyTypes: true` — never assign `undefined` to optional props; use `...(value && { prop: value })`
- `"use client"` required on any file using hooks, Zustand, or browser APIs
- `settings` in `app/config.py` is a module-level singleton — never re-instantiate `Settings()`
- Tailwind v4: no `tailwind.config.ts`; brand colors are `@theme inline` CSS vars in `globals.css`
- shadcn components live in `src/components/ui/` — import from `@/components/ui/<name>`

---

## Code quality rules

- No `any` types — use `unknown` and narrow
- No silently swallowed errors — always surface to caller or store
- `workspace:*` for all inter-package deps (not version numbers)
- Mock only at external boundaries (Claude clients, fetch) — never mock code you own
- New shared types go in `packages/types/src/index.ts`
- New vehicle makes/models go in `packages/vehicle-data/src/index.ts` with tests
