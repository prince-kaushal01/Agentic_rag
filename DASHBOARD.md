# Project Dashboard — Enterprise Agentic Knowledge Assistant

> Last updated: 2026-09-17 | Branch: `main` | Commit: `7d24836`

---

## Overall Progress

```
████████████████████████████████████████████████████████████  100%
```

**77 / 77 tasks complete** across 12 phases

---

## Phase Summary Table

| # | Phase | Status | Progress | Tasks Done | Tasks Total | Started | Completed |
|---|-------|--------|----------|-----------|-------------|---------|-----------|
| 1 | Foundation & Project Setup | ✅ Done | `████████████` 100% | 11 | 11 | 2026-08-30 | 2026-08-30 |
| 2 | Document Ingestion Pipeline | ✅ Done | `████████████` 100% | 8 | 8 | 2026-08-30 | 2026-08-30 |
| 3 | Basic RAG | ✅ Done | `████████████` 100% | 5 | 5 | 2026-09-04 | 2026-09-04 |
| 4 | Production Retrieval | ✅ Done | `████████████` 100% | 6 | 6 | 2026-09-07 | 2026-09-07 |
| 5 | Authentication & Authorization | ✅ Done | `████████████` 100% | 7 | 7 | 2026-09-11 | 2026-09-11 |
| 6 | Agent Runtime | ✅ Done | `████████████` 100% | 6 | 6 | 2026-09-01 | 2026-09-01 |
| 7 | Tool Registry & Enterprise Connectors | ✅ Done | `████████████` 100% | 6 | 6 | 2026-09-17 | 2026-09-17 |
| 8 | Human-in-the-Loop & Approvals | ✅ Done | `████████████` 100% | 5 | 5 | 2026-09-17 | 2026-09-17 |
| 9 | Memory & State Management | ✅ Done | `████████████` 100% | 5 | 5 | 2026-09-17 | 2026-09-17 |
| 10 | Security Hardening | ✅ Done | `████████████` 100% | 5 | 5 | 2026-09-17 | 2026-09-17 |
| 11 | Evaluation Suite | ✅ Done | `████████████` 100% | 5 | 5 | 2026-09-17 | 2026-09-17 |
| 12 | Observability, Cost & Deployment | ✅ Done | `████████████` 100% | 8 | 8 | 2026-09-17 | 2026-09-17 |

**Status legend:** ✅ Done · 🔄 In Progress · ⬜ Not Started · 🚧 Blocked

---

## Phase Details

---

### Phase 1 — Foundation & Project Setup ✅ 100%

> *Goal: repo structure, environment, dependencies, seed data, Docker, database schema.*

```
████████████  100%
```

| Task | Status | Notes |
|------|--------|-------|
| Initialize repository with full directory structure | ✅ | `1024cd9` — 2026-08-30 |
| Create README.md and DASHBOARD.md | ✅ | 2026-08-30 — professional project docs |
| `.env` + `.env.example` + secrets management | ✅ | 2026-08-30 — `.env` gitignored, leading-space bug fixed |
| `requirements.txt` — all 40+ packages defined | ✅ | 2026-08-30 — version conflicts resolved |
| Python virtual environment setup + all packages installed | ✅ | 2026-08-30 — Python 3.11.8, all imports verified |
| `.gitignore` — comprehensive (venv, secrets, ML artifacts, OS files) | ✅ | 2026-08-30 |
| 89 synthetic seed documents across 8 departments | ✅ | 2026-08-30 — HR, Sales, Finance, Legal, Engineering, Support, Marketing, Ops |
| Docker Compose — Postgres 16 + pgvector + Redis 7.2 | ✅ | 2026-08-30 — port 5433 (native PG conflict resolved), both containers healthy |
| SQLAlchemy models — 10 tables created in DB | ✅ | 2026-08-30 — Organization, User, Document, DocumentChunk, Conversation, Message, Task, ToolCall, Approval, AuditLog |
| `backend/database/connection.py` — async engine + session factory | ✅ | 2026-08-30 |
| `backend/database/init_db.py` — pgvector extension + table creation script | ✅ | 2026-08-30 — verified against live DB |

---

### Phase 2 — Document Ingestion Pipeline ✅ 100%

> *Goal: upload any supported file format; parse, chunk, embed, and index it into pgvector.*

```
████████████  100%
```

| Task | Status | Notes |
|------|--------|-------|
| File parsers: PDF, DOCX, TXT, MD, CSV, XLSX | ✅ | `ingestion/parsers/` — 5 parsers + auto-detect registry |
| Text cleaning & structure extraction | ✅ | Per-format: sections (DOCX/MD), pages (PDF), rows (CSV/XLSX) |
| Semantic + structural chunker | ✅ | `ingestion/chunking/chunker.py` — sections → pages → full content fallback, overlapping windows |
| Metadata attachment per chunk (doc_id, section, page, tenant, ACL) | ✅ | All fields on `DocumentChunk` model, propagated from parser |
| Embedding generation (batch + async) | ✅ | `ingestion/embeddings/embedder.py` — `all-MiniLM-L6-v2`, 384-dim, cosine-normalized |
| pgvector indexing | ✅ | `ingestion/indexing/pgvector_index.py` — upsert + chunk insert, `Vector(384)` column |
| Ingestion pipeline orchestrator | ✅ | `ingestion/pipeline.py` — `run_pipeline()` ties all stages together |
| Seed script — all 89 documents ingested | ✅ | `ingestion/seed.py` — **89 docs / 1907 chunks** in pgvector, 0 failures |

**Ingestion stats:**
- Documents indexed: **89 / 89**
- Total chunks in pgvector: **1,907**
- Embedding model: `all-MiniLM-L6-v2` (384 dimensions)
- Departments covered: customer_support, engineering, finance, hr, legal, marketing, operations, sales

---

### Phase 3 — Basic RAG ✅ 100%

> *Goal: question → vector retrieval → LLM answer with source citations.*

```
████████████  100%
```

| Task | Status | Notes |
|------|--------|-------|
| Semantic retrieval (pgvector cosine similarity) | ✅ | `backend/retrieval/semantic.py` — tenant + ACL filters, conditional dept filter |
| Context builder (top-K chunks → prompt) | ✅ | `backend/retrieval/context_builder.py` — numbered blocks, 12k char limit |
| LLM call with citation extraction | ✅ | `backend/retrieval/llm.py` — Gemini 2.5 Flash, [N] citation regex |
| `/chat` endpoint (basic) | ✅ | `POST /chat` — retrieval → context → LLM → response with sources |
| Conversation history persistence | ✅ | Messages saved to DB; multi-turn history loaded per conversation_id |

**Live test results:**
- Query: "What is the remote work policy at NovaTech?" → correct answer with [2] citation
- Multi-turn: follow-up in same conversation_id → context-aware answer
- ACL verified: `Remote_Work_Policy.md` (restricted) only returned for `access_level=restricted`
- Cost: ~$0.000112 per query | Model: `gemini-2.5-flash`

---

### Phase 4 — Production Retrieval ✅ 100%

> *Goal: hybrid search, reranking, metadata/permission filters, query rewriting.*

```
████████████  100%
```

| Task | Status | Notes |
|------|--------|-------|
| BM25 / keyword retrieval | ✅ | `backend/retrieval/keyword.py` — rank-bm25, in-process index over permitted chunks |
| Hybrid fusion (RRF — Reciprocal Rank Fusion) | ✅ | `backend/retrieval/hybrid.py` — RRF k=60, merges semantic + BM25 ranked lists |
| Cross-encoder reranker | ✅ | `backend/retrieval/reranker.py` — `ms-marco-MiniLM-L-6-v2`, runs on top-20 candidates |
| Query analysis & rewriting | ✅ | `backend/retrieval/query_rewriter.py` — Gemini standalone query rewriter for multi-turn |
| Metadata + permission filtering pre-retrieval | ✅ | ACL + tenant + department filters applied at SQL level in all retrieval paths |
| Document versioning support | ✅ | `is_latest` + `version` columns on Document model; filter-ready |

**Live test results:**
- Query: "What are the salary bands for senior engineers?" → `$180k–$240k` with exact section citations
- Hybrid retrieval mode tested; cross-encoder verified to rerank correctly
- Cost: ~$0.000181 per query | ACL-aware

---

### Phase 5 — Authentication & Authorization ✅ 100%

> *Goal: JWT auth, RBAC roles, document-level ACL, multi-tenant data isolation.*

```
████████████  100%
```

| Task | Status | Notes |
|------|--------|-------|
| JWT authentication + token refresh | ✅ | `tokens.py` — HS256, access (60min) + refresh (7d) |
| Role definitions: employee/engineer/account_manager/manager/hr/admin | ✅ | `permissions.py` — max_access_level + allowed_departments per role |
| RBAC middleware (FastAPI dependency) | ✅ | `dependencies.py` — `get_current_user`, `require_role(*roles)` factory |
| Document-level ACL (`access_level`, `department`, `tenant_id`) | ✅ | Permissions injected into retrieval — caller cannot override their own role |
| Permission filter injected into retrieval layer | ✅ | `/chat` reads `perms.max_access_level` + `perms.allowed_departments` from JWT |
| Audit log model + write path | ✅ | `audit.py` — `write_audit_log()`, records auth.login, chat.query per request |
| `/auth/register`, `/auth/login`, `/auth/refresh`, `/auth/me` | ✅ | All four endpoints live and tested |

**Permission matrix:**

| Role | Public Docs | Engineering | Financial | HR Records | CRM |
|------|:-----------:|:-----------:|:---------:|:----------:|:---:|
| Employee | ✅ | ❌ | ❌ | ❌ | ❌ |
| Engineer | ✅ | ✅ | ❌ | ❌ | ❌ |
| Account Mgr | ✅ | ❌ | ❌ | ❌ | ✅ |
| Manager | ✅ | ✅ | ✅ | ❌ | ✅ |
| HR | ✅ | ❌ | ❌ | ✅ | ❌ |
| Admin | ✅ | ✅ | ✅ | ✅ | ✅ |

---

### Phase 6 — Agent Runtime ✅ 100%

> *Goal: planner decomposes multi-step tasks; router selects retrieval vs. tool; executor runs steps with bounded budget.*

```
████████████  100%
```

| Task | Status | Notes |
|------|--------|-------|
| Task planner (LangGraph graph) | ✅ | Gemini decomposes query into 1-4 ordered steps |
| Retrieval vs. tool router | ✅ | Keyword-first + LLM fallback routing |
| Step executor with agent state | ✅ | `retrieve_node`, `tool_node`, `answer_node` |
| Max-step budget + early termination | ✅ | Budget guard on every conditional edge |
| `/tasks` API (create / get / list / trace) | ✅ | POST, GET, GET/{id}, GET/{id}/trace |
| Agent state schema | ✅ | `AgentState` TypedDict + `initial_state()` factory |

**Key files:**
```
backend/agents/planner.py
backend/agents/router.py
backend/agents/executor.py
backend/agents/graph.py
backend/agents/runner.py
backend/agents/state.py
```

---

### Phase 7 — Tool Registry & Enterprise Connectors ✅ 100%

> *Goal: typed tool definitions, simulated CRM + support + email tools, tool-level permission enforcement.*

```
████████████  100%
```

| Task | Status | Notes |
|------|--------|-------|
| Tool registry with schema, permission, risk level | ✅ | `backend/tools/registry.py` — 8 tools, risk levels 1–4, role enforcement |
| Knowledge tools: `search_knowledge`, `get_document` | ✅ | `backend/tools/knowledge.py` — hybrid search + reranking wrapper |
| CRM tools: `get_customer`, `get_customer_contract` | ✅ | `backend/tools/crm.py` — 20 synthetic NovaTech customers |
| Support tools: `get_tickets`, `create_ticket` | ✅ | `backend/tools/support.py` — simulated ticket store per customer |
| Email tools: `draft_email`, `send_email` (simulated) | ✅ | `backend/tools/email.py` — Gemini-drafted emails, simulated send |
| Retry + timeout policy per tool | ✅ | `execute_tool()` — 3 attempts, per-tool timeout (8–15s), fail-safe return |

**Tool risk levels:**

| Level | Label | Behaviour | Tools |
|-------|-------|-----------|-------|
| 1 | Read | Auto-execute | `search_knowledge`, `get_customer`, `get_tickets` |
| 2 | Draft | Auto-execute | `draft_email`, `get_document`, `get_customer_contract` |
| 3 | Write | Policy-based | `create_ticket` |
| 4 | External | Approval required | `send_email` |

**Key files:**
```
backend/tools/registry.py
backend/tools/knowledge.py
backend/tools/crm.py
backend/tools/support.py
backend/tools/email.py
```

---

### Phase 8 — Human-in-the-Loop & Approvals ✅ 100%

> *Goal: agent pauses before Level 4 actions; user reviews, edits, approves or rejects; audit trail recorded.*

```
████████████  100%
```

| Task | Status | Notes |
|------|--------|-------|
| Approval request creation + persistence | ✅ | Runner creates `Approval` DB record when `approval_required=True`; task → `awaiting_approval` |
| `/approvals/{id}/approve` and `/reject` endpoints | ✅ | `backend/api/routes/approvals.py` — approve (with optional payload edit), reject |
| Agent pauses on risk-4 tool call | ✅ | `tool_node` detects `risk_level >= 4`, sets `approval_required=True`, graph exits early |
| Approval audit record (who, when, decision) | ✅ | `write_audit_log()` called on every approve/reject with reviewer + outcome |
| `GET /approvals` list + `GET /approvals/{id}` detail | ✅ | Manager/admin see all; others see own; filtered by status |

**Approval flow:**
```
Agent encounters send_email
  → tool_node sets approval_required=True
  → graph exits (END edge)
  → runner creates Approval record (status=pending)
  → task status = awaiting_approval
  → manager calls POST /approvals/{id}/approve
  → task status = running  ← agent can resume
```

**Key files:**
```
backend/api/routes/approvals.py
backend/agents/executor.py   (approval_required guard)
backend/agents/graph.py      (end edge for approval_required)
backend/agents/runner.py     (Approval record creation)
```

---

### Phase 9 — Memory & State Management ✅ 100%

> *Goal: three-layer memory (conversation, task, persistent); Redis for hot state.*

```
████████████  100%
```

| Task | Status | Notes |
|------|--------|-------|
| Conversation memory (scoped to session) | ✅ | `ConversationMemory` — Redis list, 24h TTL, max 50 messages |
| Task memory (scoped to current task) | ✅ | `TaskMemory` — Redis hash, 1h TTL, survives tool calls |
| Persistent memory (user preferences + facts) | ✅ | `PersistentMemory` — Redis hash/list, no expiry, GDPR clear support |
| Redis for conversation + task hot state | ✅ | `RedisStore` singleton, async, JSON-serialised; injected into chat.py + runner.py |
| Memory compression / summarization | ✅ | `ConversationMemory.summarize_if_needed()` — Gemini compresses when > 30 messages |

**Key files:**
```
backend/memory/redis_store.py
backend/memory/conversation.py
backend/memory/task_memory.py
backend/memory/persistent.py
```

---

### Phase 10 — Security Hardening ✅ 100%

> *Goal: prompt injection defense, PII detection, tenant isolation, rate limiting.*

```
████████████  100%
```

| Task | Status | Notes |
|------|--------|-------|
| Prompt injection defense | ✅ | `PromptInjectionDefense` — 15 patterns, sanitize + XML-wrap retrieved context |
| PII detection before storage and display | ✅ | `PIIDetector` — 11 types: email, SSN, CC, IBAN, IP, AWS keys, phone, passport, DOB, bank routing, generic API keys |
| Tenant isolation verification | ✅ | `TenantIsolationChecker` — verify doc/conversation/task ownership at API boundaries |
| Rate limiting (per-IP sliding window) | ✅ | `RateLimiter` — 60 req/min on `/chat` + `/tasks`; Redis-backed, in-process fallback |
| Security middleware in FastAPI app | ✅ | Injection scan on every POST (returns 400 on threat); rate limit (returns 429) |

**Threat detection coverage:**

| Attack Type | Detection Method | Response |
|-------------|-----------------|----------|
| Prompt injection (user query) | Regex pattern scan | HTTP 400 |
| Prompt injection (retrieved docs) | XML-wrap + sanitize | Neutralized |
| PII in stored text | 11-type regex scan | Redaction available |
| Cross-tenant data access | UUID ownership check | PermissionError |
| Request flooding | Sliding-window rate limit | HTTP 429 |

**Key files:**
```
backend/security/pii_detector.py
backend/security/prompt_injection.py
backend/security/tenant_isolation.py
backend/security/rate_limiter.py
```

---

### Phase 11 — Evaluation Suite ✅ 100%

> *Goal: 50 test cases covering retrieval quality, answer correctness, agent behaviour, and security.*

```
████████████  100%
```

| Task | Status | Notes |
|------|--------|-------|
| Test case schema + dataset (50 cases) | ✅ | 40 retrieval (8 depts × 5), 5 agent, 5 security adversarial |
| Retrieval evaluation: Recall@K, Precision@K, MRR | ✅ | `runner.py` — computed per case, averaged in report |
| Answer evaluation: keyword-based correctness | ✅ | Hit rate of expected keywords in LLM answer |
| Agent evaluation: tool selection accuracy | ✅ | `expected_tool` matched against `steps_completed` |
| Evaluation runner + report generation | ✅ | `python -m backend.evaluation.runner --mode all --output results.json` |

**Run evaluation:**
```bash
python -m backend.evaluation.runner --mode retrieval --top-k 5
python -m backend.evaluation.runner --mode security
python -m backend.evaluation.runner --mode all --output results.json
```

**Target metrics:**

| Metric | Target |
|--------|--------|
| Recall@5 | > 0.85 |
| Precision@5 | > 0.75 |
| MRR | > 0.80 |
| Answer correctness | > 0.90 |
| Tool selection accuracy | > 0.90 |
| Security block rate | 1.00 |

**Key files:**
```
backend/evaluation/test_cases.py   — 50 TestCase definitions
backend/evaluation/runner.py       — async runner, metrics, CLI
```

---

### Phase 12 — Observability, Cost & Deployment ✅ 100%

> *Goal: full request traces, cost tracking, model routing, CI/CD pipeline.*

```
████████████  100%
```

| Task | Status | Notes |
|------|--------|-------|
| Request tracing (span-based) | ✅ | `Tracer` / `SpanContext` — Redis-backed spans + optional OTLP export (Jaeger / Langfuse / Grafana Tempo) |
| LLM trace forwarding | ✅ | OTLP HTTP export when `OTLP_ENDPOINT` is set; spans include model, tokens, latency |
| Cost tracking per conversation / task / user / tenant | ✅ | `CostTracker` — Redis aggregates with daily buckets; `GET /observability/costs` |
| Model routing (fast / standard / advanced) | ✅ | `ModelRouter` — routes by task type + context size; env-configurable model names |
| Retry + fallback logic | ✅ | Tool registry: 3 retries with backoff; middleware: fail-open on all non-critical errors |
| Docker Compose (Postgres + pgvector + Redis) | ✅ | `docker-compose.yml` — all services healthy, port mapping, health checks |
| GitHub Actions CI | ✅ | `.github/workflows/ci.yml` — lint (ruff), mypy, import smoke test, unit tests, route check |
| `X-Process-Time-Ms` response header | ✅ | Timing middleware on every request |

**Observability endpoints:**
```
GET /health                        → service status
GET /tools                         → registered tools + risk levels
GET /observability/costs?tenant_id=<uuid>  → today's spend
GET /observability/models          → configured model names by tier
```

**Model tiers:**

| Tier | Default Model | Used For |
|------|--------------|----------|
| Fast | `gemini-2.0-flash` | Classification, routing, summarization, query rewrite |
| Standard | `gemini-2.5-flash` | Retrieval + answer (default) |
| Advanced | `gemini-2.5-pro` | Long context (> 20k chars), complex reasoning |

**Key files:**
```
backend/observability/tracing.py
backend/observability/cost_tracker.py
backend/observability/model_router.py
.github/workflows/ci.yml
```

---

## API Route Reference

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/auth/register` | — | Register user, get JWT pair |
| POST | `/auth/login` | — | Login, get JWT pair |
| POST | `/auth/refresh` | Bearer | Refresh access token |
| GET | `/auth/me` | Bearer | Current user + permissions |
| POST | `/chat` | Bearer | RAG chat (hybrid retrieval + LLM) |
| POST | `/tasks` | Bearer | Run agentic task |
| GET | `/tasks` | Bearer | List my tasks |
| GET | `/tasks/{id}` | Bearer | Get task result |
| GET | `/tasks/{id}/trace` | Bearer | Get step-by-step trace |
| GET | `/approvals` | Bearer | List pending approvals |
| GET | `/approvals/{id}` | Bearer | Get approval detail |
| POST | `/approvals/{id}/approve` | Bearer | Approve (manager+) |
| POST | `/approvals/{id}/reject` | Bearer | Reject (manager+) |
| GET | `/health` | — | Service health check |
| GET | `/tools` | — | Registered tool registry |
| GET | `/observability/costs` | — | Today's cost by tenant |
| GET | `/observability/models` | — | Configured model tiers |

---

## Commit History

| Date | Commit | Phase | What Changed | Tasks Complete | Total % |
|------|--------|-------|-------------|----------------|---------|
| 2026-08-30 | `1024cd9` | 1 | Initial commit — repo created | 1/77 | 1% |
| 2026-08-30 | — | 1 | README.md + DASHBOARD.md | 3/77 | 4% |
| 2026-08-30 | — | 1 | `.env`, `.gitignore`, `requirements.txt` | 6/77 | 8% |
| 2026-08-30 | — | 1 | Python venv, 89 seed docs, Docker, DB schema | 11/77 | 14% |
| 2026-08-30 | — | 2 | 5 parsers, chunker, embedder, pgvector indexer | 19/77 | 25% |
| 2026-08-30 | — | 2 | Seed script — 89 docs / 1907 chunks | 21/77 | 27% |
| 2026-09-04 | — | 3 | Semantic retrieval, context builder, Gemini LLM | 26/77 | 34% |
| 2026-09-07 | `fd7e469` | 4 | BM25, hybrid RRF, cross-encoder, query rewriter | 32/77 | 42% |
| 2026-09-11 | `55826a7` | 5 | JWT auth, RBAC, ACL, audit logs | 39/77 | 51% |
| 2026-09-01 | `499362c` | 6 | LangGraph agent, planner, router, executor, `/tasks` | 45/77 | 58% |
| 2026-09-17 | `7d24836` | 7–12 | Tools, approvals, memory, security, eval, observability | 77/77 | **100%** |

---

## Velocity Chart

```
Progress over commits

100% │                                                                    *
     │
 58% │                                                               *
     │
 51% │                                                          *
     │
 42% │                                                     *
     │
 34% │                                                *
     │
 27% │                                          * *
     │
 14% │                                    *
     │
  8% │                         *
     │
  4% │              *
     │
  1% │       *
     │
  0% └────────────────────────────────────────────────────────────────
      init  README  reqs  seed  docker  db  parsers  seed  RAG  hybrid  auth  agent  phases7-12
```

---

## Key Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-08-30 | PostgreSQL + pgvector for vector storage | Keeps infra simple; avoids Pinecone/Weaviate dependency |
| 2026-08-30 | LangGraph for agent orchestration | Explicit state graph; easier to debug than implicit chains |
| 2026-08-30 | Modular monolith (not microservices) | Appropriate for 2-week build; clean module boundaries still present |
| 2026-08-30 | Simulated CRM/email (not live integrations) | Demonstrates multi-system orchestration without credential complexity |
| 2026-08-30 | UUID primary keys on all models | Tenant-safe, no sequential ID leakage across tenants |
| 2026-08-30 | `tenant_id` on every table | Multi-tenancy enforced at DB level, not just app level |
| 2026-08-30 | `all-MiniLM-L6-v2` at 384 dims | Local model, no API cost; swap to `text-embedding-3-small` for production |
| 2026-08-30 | Section → page → full-content chunk fallback | Preserves document structure; handles docs without clear sections |
| 2026-09-17 | Risk level 4 tools require human approval | `send_email` is irreversible; requires manager sign-off before dispatch |
| 2026-09-17 | Three-layer memory (conversation / task / persistent) | Different TTLs and scopes for different use cases; Redis for speed |
| 2026-09-17 | In-process rate limiter with Redis fallback | No external dependency needed; Redis used when available for multi-worker accuracy |
| 2026-09-17 | Custom span tracer instead of full OpenTelemetry SDK | Avoids 10+ transitive dependencies; OTLP export still supported via HTTP |
| 2026-09-17 | Model routing by task type + context size | Classification/routing doesn't need the most expensive model; saves ~60% cost on planner/router calls |
| 2026-09-17 | Security middleware fails open | Middleware errors must never block legitimate requests; threats are logged, not silently dropped |

---

## Open Blockers

| # | Blocker | Phase Affected | Status |
|---|---------|---------------|--------|
| — | None | — | — |

---

*Enterprise Agentic Knowledge Assistant — Prince Kaushal*
