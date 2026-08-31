# NovaTech Solutions — Code Review and Development Standards

**Document Version:** 2.6  
**Last Updated:** February 3, 2026  
**Authors:** Marcus Webb (Principal Architect), Anita Sharma (Staff Engineer), Tom Okafor (Staff Engineer)  
**Classification:** Internal — Engineering  
**Applies To:** All engineering staff; all production repositories

---

## 1. Purpose

This document establishes NovaTech Solutions' engineering standards for code quality, pull request workflow, testing requirements, CI/CD gate policies, and technical debt management. These standards exist to ensure that code merged into production is safe, maintainable, and tested. Consistency across teams reduces cognitive overhead and enables engineers to contribute across services.

These are **mandatory standards**, not guidelines. Exceptions require explicit approval from a Staff Engineer or above and must be documented in the PR description.

---

## 2. Development Workflow

### 2.1 Branching Strategy

NovaTech uses a **trunk-based development** model with short-lived feature branches.

**Branch Naming Convention:**

```
{type}/{ticket-id}-{brief-description}

Examples:
  feature/ENG-2901-bulk-document-upload
  bugfix/ENG-2847-search-performance-large-tenants
  hotfix/ENG-2912-auth-token-expiry-edge-case
  chore/ENG-2880-upgrade-fastapi-0110
  docs/ENG-2895-update-api-runbook
```

**Branch Types:**

| Type | Description | Target Branch | Review Requirement |
|------|-------------|--------------|-------------------|
| `feature/` | New feature or enhancement | `main` | Standard (2 reviewers) |
| `bugfix/` | Non-urgent bug fix | `main` | Standard (2 reviewers) |
| `hotfix/` | Urgent production fix | `main` (+ backport if needed) | Expedited (1 senior reviewer) |
| `chore/` | Dependency updates, tooling, refactor | `main` | Standard (1 reviewer) |
| `docs/` | Documentation only | `main` | 1 reviewer (can be any engineer) |
| `spike/` | Research/prototype (never merges to main directly) | Feature branch | No formal review required |

**Rules:**
- Feature branches must be rebased on `main` before creating a PR
- No long-lived feature branches. If a feature takes > 2 weeks, use feature flags to merge incrementally
- Branch deletion is automatic after merge via GitHub settings
- **Directly pushing to `main` is prohibited.** Branch protection rules enforce this.

### 2.2 Commit Message Format

NovaTech follows **Conventional Commits** (v1.0.0 specification):

```
{type}({scope}): {subject}

[optional body]

[optional footer(s)]
```

**Types:**

| Type | When to Use |
|------|-------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting only (no logic change) |
| `refactor` | Code refactoring (no behavior change) |
| `perf` | Performance improvement |
| `test` | Adding or fixing tests |
| `chore` | Build, tooling, dependency updates |
| `revert` | Reverting a previous commit |
| `ci` | CI/CD configuration changes |

**Examples:**

```
feat(search): add hybrid BM25+vector search mode

Implements a new search mode that combines BM25 keyword scoring with
dense vector similarity for improved relevance on natural language queries.

Closes ENG-2834
```

```
fix(auth): correct token expiry calculation for DST transitions

The token expiry was calculated using local time rather than UTC, causing
1-hour discrepancy during daylight saving transitions.

Fixes ENG-2912
Tested-by: Rachel Torres
```

**Rules:**
- Subject line: max 72 characters, imperative mood ("add" not "added"), no period at end
- Breaking changes: add `BREAKING CHANGE:` footer
- Reference Jira ticket in footer: `Closes ENG-XXXX` or `Related to ENG-XXXX`
- Commit messages are enforced by `commitlint` in the pre-commit hook

---

## 3. Pull Request Standards

### 3.1 PR Size Limits

| PR Size | Lines Changed | Preference |
|---------|-------------|-----------|
| Ideal | < 200 lines | Strongly preferred; fastest reviews |
| Acceptable | 200–400 lines | Acceptable with clear description |
| Large | 400–800 lines | Requires justification in PR description |
| Exceptional | > 800 lines | Requires Staff Engineer pre-approval |

Large PRs that are primarily generated code (e.g., OpenAPI client generation, migrations) are exempt from the line limit but must be noted in the description.

**Why small PRs?**
- Reviews are more thorough and faster
- Bugs are easier to identify and bisect
- Rollback is simpler
- Each change is easier to understand in context

### 3.2 PR Description Requirements

Every PR must include a description following this template (available as a GitHub template):

```markdown
## Summary
[1-3 sentences describing what this PR does and why]

## Changes
- [Bullet list of specific changes]

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated (if API changes)
- [ ] Manual testing performed (describe what was tested)
- [ ] Feature flag required: [Yes/No — flag name if Yes]

## Rollback Plan
[How to roll this back if it causes issues in production]

## Screenshots / Logs
[Attach for UI changes or complex output changes]

## Related
- Jira: ENG-XXXX
- Related PRs: #XXX
- Docs updated: [Yes/No]
```

### 3.3 Review SLAs

| PR Type | Review SLA | Reviewers Required |
|---------|-----------|-------------------|
| Regular feature/bugfix | 24 business hours | 2 (1 must be from owning team) |
| Hotfix | 4 hours (any time) | 1 (must be Staff Engineer or EM) |
| Chore / dependency | 48 business hours | 1 |
| Docs only | 48 business hours | 1 |
| Security change | 24 business hours | 2 (1 must be security-trained) |
| Database migration | 24 business hours | 2 (1 must be DBA-designated) |

**Review SLA enforcement:**
- PRs open > 24 hours without review are auto-posted to `#eng-needs-review` Slack
- Reviewers who consistently miss SLAs are flagged by their EM quarterly

### 3.4 Required Reviewers by Change Type

| Change Type | Required Reviewer(s) |
|------------|---------------------|
| Authentication/authorization code | Platform Team senior engineer |
| Database schema changes | DBA-designated engineer (current: Tom Okafor) |
| API contract changes (new endpoints, field changes) | API Platform Lead (Elena Vasquez) |
| Infrastructure / Terraform changes | SRE team member (current: Kevin Osei or designee) |
| Billing/payment code | Finance engineering owner + EM sign-off |
| Security-sensitive code (crypto, secrets handling) | Security champion (current: Anita Sharma) |
| Performance-critical path changes | Staff Engineer review |

### 3.5 Review Conduct Standards

**As a reviewer:**
- Leave actionable, specific feedback. "This is wrong" → "This could cause a race condition under high concurrency. Consider using a database transaction here (line 47)."
- Distinguish between blocking issues (`[BLOCKING]`) and suggestions (`[NIT]` or `[SUGGESTION]`)
- Approve PRs promptly when standards are met — blocking by silence is not acceptable
- Do not request changes for purely stylistic reasons if the linter passes

**As a PR author:**
- Respond to all review comments before marking as resolved
- If you disagree with a comment, discuss it — don't silently resolve it
- Re-request review after addressing all comments

---

## 4. Code Style Standards

### 4.1 Python (Backend)

- **Formatter:** `ruff format` (replaces black + isort) — enforced in CI
- **Linter:** `ruff check` — all rules in `pyproject.toml`
- **Type checking:** `mypy` with strict mode enabled
- **Docstrings:** Google style for public functions/classes
- **Import ordering:** ruff manages; stdlib → third-party → local
- **String formatting:** f-strings preferred; `.format()` acceptable; `%` formatting prohibited

```python
# Correct — type annotations, Google docstring, f-string
async def get_document(document_id: str, tenant_id: str) -> Document:
    """Retrieve a document by ID within a tenant context.
    
    Args:
        document_id: The unique identifier of the document.
        tenant_id: The tenant context for authorization.
        
    Returns:
        The Document object.
        
    Raises:
        DocumentNotFoundError: If document does not exist.
        TenantMismatchError: If document belongs to a different tenant.
    """
    ...
```

- **Configuration:** `pyproject.toml` is the single source of truth for all Python tooling config
- **Version:** Python 3.12 minimum (3.11 allowed for legacy services until Q3 2026)

### 4.2 JavaScript / TypeScript (Frontend)

- **Formatter:** Prettier (`.prettierrc` in each repo root)
- **Linter:** ESLint with `@novatech/eslint-config` (shared config package)
- **Type strictness:** TypeScript strict mode required (`"strict": true` in tsconfig)
- **React:** Functional components with hooks only. Class components are prohibited in new code.
- **State management:** React Query for server state; Zustand for local UI state
- **CSS:** Tailwind CSS utility-first; no inline styles; CSS modules for complex components
- **Imports:** Absolute imports via `@/` alias for `src/` directory

### 4.3 SQL (Database Queries)

- ORM (SQLAlchemy) preferred for application queries
- Raw SQL required for migrations (Alembic)
- All queries must be parameterized — **no string formatting of SQL** (SQL injection prevention)
- EXPLAIN ANALYZE required in PR description for any new query on tables > 1M rows
- Index justification required for any new index creation

---

## 5. Testing Requirements

### 5.1 Coverage Requirements

| Test Type | Minimum Threshold | Enforcement |
|-----------|-----------------|-------------|
| Unit tests | 80% line coverage | CI gate — PR blocks if below |
| Integration tests | All API endpoints must have at least 1 test | CI gate |
| End-to-end tests | Critical user journeys (defined per team) | CI gate for P0 journeys |
| Performance tests | Required for changes to search/analytics path | CI gate (p99 budget) |

Coverage is measured per-service. A service with 75% coverage cannot merge a PR that doesn't improve coverage.

### 5.2 Unit Test Standards

- Framework: `pytest` (Python), `Vitest` (JavaScript/TypeScript)
- Tests must be isolated — no real database, network calls, or file system in unit tests
- Use `pytest-asyncio` for async code; `pytest-mock` for mocking
- Test naming: `test_{function_name}_{scenario}_{expected_outcome}`
  - Good: `test_search_query_with_empty_string_returns_400`
  - Bad: `test_search_1`
- One assertion per test is ideal; max 3 assertions per test
- Fixtures defined in `conftest.py`; shared fixtures in `tests/fixtures/`

### 5.3 Integration Test Standards

- All API endpoints must have integration tests covering: happy path, auth failure, validation error, and (for list endpoints) pagination
- Integration tests run against a real in-memory database (PostgreSQL via Docker) and mock external services
- Framework: `pytest` + `httpx.AsyncClient`
- Integration tests live in `tests/integration/` directory
- Must complete in < 5 minutes total per service

### 5.4 What to Test vs. What Not to Test

**Test:**
- Business logic functions
- All API endpoints
- Database queries (using test DB)
- Error handling and edge cases
- Authorization checks (each role)

**Do not test (not worth the maintenance):**
- Framework internals (FastAPI routing, SQLAlchemy query building)
- Trivial getters/setters with no logic
- Third-party library behavior
- Type annotations (mypy handles this)

---

## 6. CI/CD Gates

All PRs must pass the following checks before merge. CI runs on every commit to a PR branch.

### 6.1 Required CI Gates

| Gate | Tool | Failure Action |
|------|------|---------------|
| Code formatting | ruff / Prettier | Blocks merge |
| Linting | ruff / ESLint | Blocks merge |
| Type checking | mypy / tsc | Blocks merge |
| Unit tests | pytest / Vitest | Blocks merge |
| Coverage check | pytest-cov | Blocks merge if coverage drops |
| Integration tests | pytest | Blocks merge |
| Secret scanning | Gitleaks | Blocks merge |
| Dependency vulnerability scan | Dependabot / Snyk | Blocks if CRITICAL severity |
| Docker image build | Docker | Blocks merge |

### 6.2 Performance Gate

For changes to the Search Service or Analytics Service:
- p99 latency regression tests must not exceed 10% increase from baseline
- Baseline is measured against the last 7 days of production p99 metrics
- Failure is advisory for P2 regressions; blocking for P0/P1 regressions

### 6.3 Deployment Gate (Staging)

After merge to `main`, automated deployment to staging occurs. Manual promotion to production requires:
1. Staging smoke tests pass (`make smoke-test ENV=staging`)
2. No blocking alerts in staging Datadog for 30 minutes
3. Release manager approval (for weekly releases) or on-call approval (for hotfixes)

---

## 7. Documentation Requirements

### 7.1 Code Documentation

| Code Element | Documentation Required |
|-------------|----------------------|
| Public API endpoint | OpenAPI docstring in route handler |
| Public Python function | Google-style docstring |
| Complex algorithm | Inline comments explaining the "why" |
| Database model | Field-level docstrings in model class |
| Environment variable | Entry in `.env.example` with description |

### 7.2 PR Documentation

- API changes: Update OpenAPI spec (`openapi.yaml`) in same PR
- New environment variables: Update `.env.example` and Terraform variable definitions
- New service dependencies: Update `System_Architecture_Overview.md`
- Changed database schema: Update data dictionary (in Confluence)
- Feature flag added: Document in LaunchDarkly description and update the feature flags registry

### 7.3 Runbook Updates

Any change that affects operational behavior requires updating the relevant runbook:
- New deployment configuration → `Infrastructure_Runbook.md`
- New alert / on-call procedure → `Incident_Response_Playbook.md`
- New API behavior → `API_Documentation.md`

---

## 8. Tech Debt Management

### 8.1 Tech Debt Definition

Tech debt is any code, infrastructure, or process that:
- Creates unnecessary complexity or risk for future changes
- Deviates from current standards (e.g., pre-ruff Python formatting)
- Is explicitly marked with a `TODO(ENG-XXXX)` comment referencing an open ticket

### 8.2 Tech Debt Process

1. **Identification:** Any engineer may create a `chore/` Jira ticket tagged `tech-debt`
2. **Classification:** EM classifies as High/Medium/Low priority
3. **Budgeting:** 20% of each sprint capacity is reserved for tech debt and chores (see Sprint Planning norms)
4. **Tracking:** Tech debt tickets are tracked in the `Tech Debt` Jira board (linked from each team's board)
5. **Aging:** Tech debt tickets older than 6 months must be re-evaluated: fix now, defer, or close as won't-fix

### 8.3 TODO Comment Policy

```python
# Acceptable — references a ticket
# TODO(ENG-2801): Remove this workaround after Elasticsearch upgrade to 8.13
result = _legacy_search_path(query)

# NOT acceptable — no ticket, no owner, no plan
# TODO: fix this later
result = _legacy_search_path(query)
```

All TODO comments must reference a Jira ticket. TODOs without a ticket reference are flagged by `ruff check` and will block the CI gate.

---

## 9. Security Coding Standards

1. **Never log PII** (emails, names, document content) in application logs. Use masked representations.
2. **Never hardcode secrets** — use environment variables sourced from AWS Secrets Manager
3. **Parameterize all database queries** — no string interpolation in SQL
4. **Validate and sanitize all user inputs** — use Pydantic models for all FastAPI request bodies
5. **Use HTTPS for all outbound requests** — never use HTTP for external calls
6. **Follow least privilege** — service accounts and IAM roles must request minimum required permissions
7. **Audit security-sensitive operations** — all admin actions, data exports, and access control changes must be logged to the Audit Service

Violations of items 1–4 are **blocking** and will fail the Snyk SAST scan.

---

*Standards are reviewed quarterly by the Engineering Leadership team. Submit feedback in #eng-standards on Slack or open a Jira ticket tagged `engineering-standards`.*
