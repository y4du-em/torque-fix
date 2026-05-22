# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Testing mandate

**Every code change must include tests. This is not optional.**

| What you add or change | Where to add tests |
|---|---|
| Utility function (`src/lib/`) | New `describe` block in `src/lib/__tests__/<file>.test.ts` |
| Zustand store action | Test case in `src/lib/__tests__/store.test.ts` |
| React hook (`src/hooks/`) | New file `src/hooks/__tests__/<hookName>.test.ts` |
| FastAPI route (`app/routers/`) | Test case in `apps/api/tests/test_routers.py` |
| Pydantic model (`app/models/`) | Test case in `apps/api/tests/test_models.py` |
| Prompt builder (`app/prompts/`) | Test case in `apps/api/tests/test_prompts.py` |
| Claude service function | Test case in `apps/api/tests/test_claude_service.py` |
| `vehicle-data` query function | Test case in `packages/vehicle-data/src/__tests__/index.test.ts` |
| Bug fix | Write a failing test that reproduces the bug first, then fix it |

Run the relevant test suite before considering any task done:
```bash
pnpm test:web          # after changing apps/web or packages/vehicle-data
pytest                 # after changing apps/api (run from inside apps/api with venv active)
pnpm test              # full suite from monorepo root
```

---

## Commands

### Monorepo root (pnpm + Turborepo)

```bash
pnpm dev              # start all apps concurrently
pnpm dev:web          # Next.js only (port 3000)
pnpm dev:api          # FastAPI only (port 8000)
pnpm build            # production build (web)
pnpm type-check       # tsc --noEmit across all packages
pnpm lint             # eslint across all packages
pnpm test             # all packages
pnpm test:web         # web + vehicle-data (Vitest)
pnpm test:vehicle-data
```

### FastAPI (`apps/api`)

```bash
# First-time setup
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # add ANTHROPIC_API_KEY

uvicorn app.main:app --reload --port 8000

ruff check . && ruff format .

pytest                                              # all tests
pytest tests/test_routers.py                        # single file
pytest tests/test_routers.py::test_health_endpoint  # single test
pytest -k "test_diagnose"                           # keyword filter
```

### Next.js (`apps/web`)

```bash
pnpm dev          # --turbopack
pnpm type-check
pnpm lint

pnpm test                                                        # vitest run (single pass)
pnpm test:watch                                                  # watch mode
pnpm vitest run src/lib/__tests__/store.test.ts                  # single file
pnpm vitest run --reporter=verbose -t "accumulates all chunks"   # single test by name
```

---

## Test patterns

### TypeScript / Vitest

**AAA structure** — every test:
```typescript
// Arrange
const { result } = renderHook(() => useMyHook());

// Act
await act(async () => { await result.current.doSomething(); });

// Assert
expect(result.current.value).toBe("expected");
```

**Hook tests** — always reset the store in `beforeEach`:
```typescript
beforeEach(() => {
  useTorqueFixStore.getState().resetAll();
  vi.clearAllMocks();
});
```

**Mocking `@/lib/api-client`** — declare at module level:
```typescript
vi.mock("@/lib/api-client", () => ({
  diagnoseVehicle: vi.fn(),
  streamChat: vi.fn(),
}));
```

**Async generators** (`streamChat`):
```typescript
// Success path — helper keeps tests readable
function makeStream(...chunks: string[]) {
  return (async function* () { for (const c of chunks) yield c; })();
}
(streamChat as Mock).mockReturnValue(makeStream("Hello", " world"));

// Error path
(streamChat as Mock).mockImplementation(async function* () {
  throw new Error("network error");
});
```

**Stable router mock** — use `vi.hoisted` when you need to assert on `router.push`:
```typescript
const mockRouterPush = vi.hoisted(() => vi.fn());
vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: mockRouterPush, replace: vi.fn(), ... }),
  usePathname: () => "/",
  useSearchParams: () => new URLSearchParams(),
}));
```

### Python / pytest

**`conftest.py` must set the API key before any app import** (already done — don't change the import order):
```python
import os
os.environ.setdefault("ANTHROPIC_API_KEY", "sk-test-key-for-testing")
# app imports come after
```

**Mock at the service boundary** — patch the two module-level clients:
```python
with patch("app.services.claude_service._sync_client") as mock_sync, \
     patch("app.services.claude_service._async_client") as mock_async:
    ...
```

**Router tests** use `TestClient` (from `conftest.py` fixture), patch the service function:
```python
with patch("app.routers.diagnosis.diagnose_vehicle", return_value=sample_diagnosis):
    response = client.post("/api/v1/diagnose", json=payload)
assert response.status_code == 200
```

---

## Architecture

### Overview

```
packages/types        → shared TypeScript interfaces (VehicleContext, DiagnosisResponse, ChatMessage, …)
packages/vehicle-data → Indian vehicle database + symptomsByCategory + query utilities
packages/config       → tsconfig.base.json (strict, exactOptionalPropertyTypes)
apps/api              → FastAPI, calls Claude, 2 endpoints (/diagnose, /chat)
apps/web              → Next.js 15.3, all state in Zustand
```

### `apps/api` — request flow

1. Router (`app/routers/`) validates via Pydantic (`app/models/`)
2. Calls `app/services/claude_service.py`:
   - `_sync_client` (`anthropic.Anthropic`) — used for `diagnose_vehicle()` via `asyncio.to_thread`
   - `_async_client` (`anthropic.AsyncAnthropic`) — used for `stream_chat()` async generator
3. Prompts built in `app/prompts/`
4. `/diagnose` expects **raw JSON only** from Claude (no markdown fences) — `JSONDecodeError` → HTTP 502
5. `/chat` returns `StreamingResponse` in SSE format: `data: {chunk}\n\n`, terminated by `data: [DONE]\n\n`

`settings` in `app/config.py` is a module-level singleton — never instantiate `Settings()` elsewhere.

### `apps/web` — state and data flow

**Zustand store** (`src/lib/store.ts`, `useTorqueFixStore`) is the single source of truth. Key action: `updateLastAssistantMessage` iterates backwards to find the last assistant message and replaces its content — used for progressive streaming renders.

**Diagnosis flow:**
1. `useVehicleSelector` → local cascading state (type → make → model → year → fuelType); each setter clears all downstream fields; calls `setVehicleContext` when `isComplete`
2. `useDiagnosis` → reads store, calls `diagnoseVehicle()`, navigates to `/results` on success
3. `useChat` → calls `streamChat()` async generator, accumulates chunks via `updateLastAssistantMessage`

**Tailwind v4** — no `tailwind.config.ts`; brand colors are CSS variables in `src/app/globals.css` under `@theme inline` (e.g. `--color-brand-500: #f97316`).

**`exactOptionalPropertyTypes: true`** — never assign `undefined` to an optional prop. Use conditional spread:
```typescript
// Wrong
const obj = { foo: maybeUndefined };
// Right
const obj = { ...(value !== null && { foo: value }) };
```

**Component rules:**
- `"use client"` required on any file using hooks, Zustand, or browser APIs
- shadcn components are in `src/components/ui/` — import from `@/components/ui/<name>`
- `src/app/page.tsx` (landing) is a server component; keep it that way

### `packages/vehicle-data`

Pure query functions over `vehicleData: VehicleMake[]`. All data is Indian vehicles only. To add a make or model, append to `vehicleData` in `packages/vehicle-data/src/index.ts` and add coverage to `src/__tests__/index.test.ts`.

---

## Code quality rules

- **No `any` types** — if a type is unknown, use `unknown` and narrow it
- **No silently swallowed errors** — always surface errors to the caller or store
- **No hardcoded strings for vehicle makes/models** — all data lives in `packages/vehicle-data`
- **`workspace:*`** for all inter-package deps in `package.json` (not version numbers)
- **No mock of code you own** — mock only at external boundaries (API calls, Claude client)
- After adding a new shared type, add it to `packages/types/src/index.ts` and re-export it
