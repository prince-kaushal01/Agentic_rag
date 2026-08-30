# Enterprise Agentic Knowledge Assistant

> Built a production-oriented enterprise AI assistant using agentic RAG, hybrid retrieval, permission-aware document access, typed tool calling, persistent task state, human-in-the-loop actions, evaluation, observability, and cost controls.

---

## What This Is

Most AI document tools answer one question from one place.

This system does something different.

It acts as an **AI employee** — it understands what a user is asking, finds the right information across multiple internal systems, reasons over it, and safely executes approved actions. It respects organizational permissions, maintains task state across steps, requires human approval before risky actions, and leaves a complete audit trail.

**Instead of:** *"Find this in the documents."*

**This does:** *"Investigate across enterprise systems and complete the task."*

---

## The Core Demo

An account manager types:

> *"Check ACME's contract, compare it with our current refund policy, look at their open support tickets, determine whether they qualify for a refund, and draft an email to the account team explaining the decision."*

The system:

```
Authenticate user
       ↓
Understand multi-step task
       ↓
Retrieve ACME contract          [permission check]
       ↓
Retrieve refund policy          [permission check]
       ↓
Query open support tickets      [CRM tool]
       ↓
Reason across all three sources
       ↓
Determine eligibility
       ↓
Draft email with citations
       ↓
Pause for human approval
       ↓
Execute on approval
       ↓
Write audit log
```

The UI shows the full structured execution trace.

---

## Architecture

```
                         ┌───────────────────┐
                         │       USER        │
                         │   Web / Chat UI   │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │    FastAPI API    │
                         │  Authentication   │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │   Agent Runtime   │
                         │  Planner / Router │
                         └─────────┬─────────┘
                                   │
                 ┌─────────────────┼──────────────────┐
                 │                 │                  │
                 ▼                 ▼                  ▼
            Retrieval         Tool Manager         Memory
               │                   │                  │
       ┌───────┴────────┐     ┌────┴─────┐             │
       ▼                ▼     ▼          ▼             ▼
  Vector Search       BM25   SQL      Enterprise    Redis /
                           Query        APIs        Postgres
       │
       ▼
   Reranker
       │
       ▼
  Context Builder
       │
       ▼
   LLM Gateway ──► Model Router ──► Response Validator
                                            │
                                   ┌────────┴────────┐
                                   ▼                 ▼
                                 Answer           Action
                                                    │
                                             Human Approval
                                                    │
                                             Tool Execution
                                                    │
                                              Audit Log
```

---

## Document Ingestion Pipeline

```
Upload → Validate → Parse → Clean → Extract Structure
   → Chunk → Attach Metadata → Embed → Index (pgvector + BM25)
```

Every chunk carries full provenance:

```json
{
  "document_id": "refund-policy-v4",
  "chunk_id": "refund-policy-v4-12",
  "page": 12,
  "section": "Enterprise Refunds",
  "department": "finance",
  "access_level": "internal",
  "tenant_id": "acme-corp",
  "version": 4
}
```

---

## Production RAG (Not Basic RAG)

```
Query
  ↓
Query Analysis + Rewriting
  ↓
Permission Filter
  ↓
┌────────────────────────┐
│  Semantic   │  BM25    │   ← Hybrid Retrieval
└──────┬──────┴────┬─────┘
       └─────┬─────┘
             ▼
        Candidate Set
             ▼
          Reranker
             ▼
       Top-K Documents
             ▼
       Context Builder
             ▼
            LLM
```

Features: semantic search · BM25/keyword · hybrid fusion · metadata filtering · permission-aware retrieval · cross-encoder reranking · query rewriting · source citations · document versioning

---

## Permission Model

```
Role                  Access
─────────────────────────────────────────────────
Public Employee       Public docs, company wiki
Engineer              + Engineering docs, runbooks
Account Manager       + Customer contracts, CRM
Manager               + Financial reports
HR                    + Employee records, salaries
Admin                 Everything
```

A user asking *"What salary does employee X receive?"* gets a denial — not because the AI chooses to refuse, but because the authorization layer prevents that data from ever reaching retrieval.

---

## Tool Registry

| Tool | Level | Approval | Permission |
|------|-------|----------|------------|
| `search_knowledge()` | 1 — Read | Auto | `knowledge.read` |
| `get_customer()` | 1 — Read | Auto | `crm.read` |
| `query_database()` | 1 — Read | Auto | `db.read` |
| `draft_email()` | 2 — Draft | Auto | `email.draft` |
| `create_ticket()` | 3 — Write | Policy | `tickets.write` |
| `send_email()` | 4 — External | **Required** | `email.send` |
| `delete_record()` | 4 — External | **Required** | `admin.delete` |

---

## Human-in-the-Loop

When an action crosses a risk boundary, the agent pauses:

```
┌─────────────────────────────────────────────┐
│  AI wants to send an email                  │
│                                             │
│  To:      Account Manager — jane@corp.com   │
│  Subject: ACME Refund Decision              │
│                                             │
│  [Generated email preview]                  │
│                                             │
│         Edit       Approve       Reject     │
└─────────────────────────────────────────────┘
```

Every decision is recorded in the audit log with user, timestamp, action, and outcome.

---

## Repository Structure

```
enterprise-agentic-assistant/
│
├── backend/
│   ├── api/                    # FastAPI routes, schemas, middleware
│   ├── agents/
│   │   ├── planner.py          # Task decomposition
│   │   ├── router.py           # Retrieval vs tool routing
│   │   └── executor.py         # Step execution + state management
│   │
│   ├── retrieval/
│   │   ├── semantic.py         # pgvector search
│   │   ├── keyword.py          # BM25 / full-text search
│   │   ├── hybrid.py           # RRF fusion
│   │   └── reranker.py         # Cross-encoder reranking
│   │
│   ├── tools/
│   │   ├── registry.py         # Tool definitions + permission mapping
│   │   ├── knowledge.py        # Document search tools
│   │   ├── crm.py              # Customer system tools
│   │   ├── support.py          # Ticket system tools
│   │   └── email.py            # Email draft + send tools
│   │
│   ├── memory/                 # Conversation, task, persistent memory
│   ├── auth/                   # JWT, OAuth, RBAC
│   ├── security/               # PII detection, prompt injection defense
│   ├── evaluation/             # Test harness, metrics
│   ├── observability/          # Tracing, cost tracking, metrics
│   └── database/               # SQLAlchemy models, migrations
│
├── ingestion/
│   ├── parsers/                # PDF, DOCX, CSV, HTML, Markdown
│   ├── chunking/               # Semantic + structural chunking
│   ├── embeddings/             # Embedding generation
│   └── indexing/               # pgvector + BM25 indexing
│
├── frontend/                   # React / Next.js chat UI
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── security/               # Permission bypass, injection tests
│   └── evaluation/             # RAG + agent eval suite (50-100 cases)
│
├── docs/
│   ├── architecture.md
│   ├── security.md
│   ├── evaluation.md
│   └── system-design.md
│
├── infrastructure/             # Docker, CI/CD
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python · FastAPI · Pydantic · SQLAlchemy |
| Database | PostgreSQL · pgvector |
| Cache / State | Redis |
| LLM | Claude API (Anthropic) |
| Embeddings | Embedding model via API |
| Reranker | Cross-encoder model |
| Agent Orchestration | LangGraph |
| Frontend | React / Next.js |
| Observability | OpenTelemetry · Langfuse |
| Infrastructure | Docker · Docker Compose · GitHub Actions |

---

## API Surface

```
POST   /auth/login
POST   /auth/refresh

POST   /documents/upload
GET    /documents/{id}
DELETE /documents/{id}

POST   /chat
GET    /conversations/{id}
GET    /conversations/{id}/messages

POST   /tasks
GET    /tasks/{id}
GET    /tasks/{id}/trace

POST   /approvals/{id}/approve
POST   /approvals/{id}/reject

GET    /traces/{id}
GET    /evaluations
GET    /metrics/cost
GET    /metrics/latency
```

---

## Evaluation Suite

~100 test cases covering:

**Retrieval**
- Recall@K, Precision@K, MRR
- Context relevance
- Permission boundary enforcement

**Answers**
- Correctness, groundedness
- Citation accuracy
- Hallucination rate

**Agent**
- Task success rate
- Tool selection accuracy
- Unnecessary tool call rate
- Average steps to completion

**Security**
- Unauthorized retrieval attempts
- Prompt injection resistance
- Permission bypass attempts

---

## Observability

Every request produces a structured execution trace:

```
REQUEST
 ├── AUTH         [2ms]
 ├── ROUTER       [8ms]
 ├── RETRIEVAL
 │    ├── BM25         [12ms] — 23 candidates
 │    ├── Vector Search [18ms] — 20 candidates
 │    └── Reranker      [45ms] — top 5 selected
 ├── LLM [gpt-4o]     [1.2s]  — 840 tokens
 ├── TOOL: get_customer [34ms]
 ├── LLM [gpt-4o]     [0.9s]  — 620 tokens
 └── RESPONSE          [total: 2.3s | cost: $0.0041]
```

---

## Security Controls

| Control | Implementation |
|---------|---------------|
| Authentication | JWT + OAuth2 |
| Authorization | RBAC + document-level ACL |
| Data isolation | Tenant ID on every entity |
| Prompt injection | Retrieved docs treated as untrusted data |
| PII detection | Scan before storage and display |
| Audit logging | Every action: who · what · when · outcome |
| Secrets | Environment variables only — never in prompts |

---

## Cost & Model Routing

| Operation | Model |
|-----------|-------|
| Intent classification | Small / fast model |
| Query rewriting | Small / fast model |
| Embedding generation | Embedding model |
| Complex reasoning | Large model |
| Fallback | Secondary provider |

Cost tracked per conversation, per task, per token class.

---

## Development Phases

| Phase | Scope |
|-------|-------|
| 1 | Document ingestion + basic RAG |
| 2 | Hybrid retrieval + reranking + citations |
| 3 | Agent runtime + tool registry |
| 4 | Auth + RBAC + document ACL + multi-tenancy |
| 5 | CRM, support, email tools + human approval |
| 6 | Evaluation + observability + cost tracking + deployment |

See [DASHBOARD.md](DASHBOARD.md) for live progress tracking.

---

## Engineering Philosophy

> LLM ≠ System.

The LLM is one component. A production AI system requires:

```
Models + Data + Retrieval + Tools + State + Permissions
+ Evaluation + Observability + Security + Failure Handling + Human Oversight
```

This project prioritizes **system design and reliability** over AI feature count.

---

## Skills Demonstrated

`LLMs` `Prompt Engineering` `Structured Generation` `Model Routing` `RAG` `Embeddings` `Vector Search` `BM25` `Hybrid Retrieval` `Reranking` `Metadata Filtering` `Citations` `Agentic AI` `Planning` `Tool Calling` `Agent State` `Memory` `Human-in-the-Loop` `FastAPI` `Async Python` `PostgreSQL` `pgvector` `Redis` `RBAC` `ACL` `JWT` `OAuth` `Multi-Tenancy` `Audit Logging` `PII Detection` `Prompt Injection Defense` `Evaluation` `Observability` `OpenTelemetry` `Cost Monitoring` `Docker` `CI/CD`

---

*Project by Prince Kaushal*
