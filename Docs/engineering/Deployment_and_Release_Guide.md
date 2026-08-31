# NovaTech Solutions — Deployment and Release Guide

**Document Version:** 3.0  
**Last Updated:** March 1, 2026  
**Authors:** Kevin Osei (SRE Lead), Elena Vasquez (API Platform Lead), Dmitri Volkov (Senior DevOps Engineer)  
**Classification:** Internal — Engineering  
**Review Cycle:** Quarterly

---

## 1. Release Cadence

NovaTech Solutions follows a **weekly release train** model with the following schedule:

| Release Type | Schedule | Approver | Audience |
|-------------|----------|---------|---------|
| Standard Release | Every Wednesday at 2:00 PM PT | Release Manager (rotating) | All customers |
| Hotfix Release | As needed, any time | VP Engineering | All customers |
| Feature Flag Rollout | Any time (no deploy needed) | Engineering Manager | Configurable per flag |
| Database Migration | Separate from code release | DBA-designated engineer | Internal |

### 1.1 Release Calendar Q2 2026

| Date | Release | Version | Notes |
|------|---------|---------|-------|
| April 8, 2026 | Standard | v2.14.0 | Sprint 42 deliverables |
| April 15, 2026 | Standard | v2.14.1 | Bug fixes; search perf patch |
| April 22, 2026 | Standard | v2.15.0 | Sprint 43 deliverables |
| April 29, 2026 | Standard | v2.15.1 | Bug fixes |
| May 6, 2026 | Standard | v2.16.0 | Sprint 44 deliverables |
| May 13, 2026 | Standard | v2.16.1 | Bug fixes |
| May 20, 2026 | Standard | v2.17.0 | Sprint 45 deliverables |
| June 3, 2026 | Standard | v2.18.0 | Sprint 46 deliverables |
| June 10, 2026 | Standard | v2.18.1 | Bug fixes |
| June 17, 2026 | Standard | v2.19.0 | Sprint 47 deliverables |
| June 24, 2026 | Standard | v2.19.1 | Q2 close release |

---

## 2. Release Train Process

### 2.1 Timeline (Standard Wednesday Release)

| Day | Activity |
|-----|----------|
| **Monday** | Release candidate branched from `main` (automated). Release branch: `release/v2.X.Y` |
| **Monday PM** | All PRs intended for this release must be merged to `main` by 3:00 PM PT |
| **Tuesday AM** | Release candidate deployed to staging automatically |
| **Tuesday** | QA + smoke test suite runs in staging. Release manager reviews Datadog staging dashboard |
| **Tuesday PM** | Release notes drafted by Release Manager; reviewed by PM |
| **Wednesday AM** | Final go/no-go decision at 10:00 AM PT release standup (10 min) |
| **Wednesday 2:00 PM PT** | Production deployment begins (canary phase) |
| **Wednesday 2:15 PM** | Canary validation (5% traffic) — 15-minute window |
| **Wednesday 2:30 PM** | Full rollout to 100% traffic (if canary healthy) |
| **Wednesday 3:00 PM** | Release confirmed healthy; release notes published |

### 2.2 Release Manager Role

The Release Manager is a **rotating role** among senior engineers and engineering managers (new RM each week):

**Responsibilities:**
- Owns the go/no-go decision for each release
- Monitors the release in production for 1 hour post-deployment
- Triggers rollback if needed (without waiting for approval)
- Publishes release notes to `#eng-releases` Slack and internal changelog
- Coordinates with Customer Success for any customer-facing changes

**Current Release Manager Schedule:**
- April 8: Kevin Osei
- April 15: Rachel Torres
- April 22: Rajesh Kumar
- April 29: Elena Vasquez
- May 6: Anita Sharma
- May 13: Dmitri Volkov

---

## 3. Feature Flags (LaunchDarkly)

NovaTech uses LaunchDarkly for all feature gates. Features are shipped behind flags by default; flags are then used to roll out to increasing percentages of users.

### 3.1 Feature Flag Lifecycle

```
Code merged with flag disabled → Deploy to production → 
Internal testing (flag on for novatech.io accounts) → 
Beta rollout (1-5% of target customers) → 
Gradual rollout (10% → 25% → 50% → 100%) → 
Flag removed from code (next release cycle)
```

### 3.2 Standard Rollout Percentages

| Rollout Stage | Target | Duration | Success Criteria |
|--------------|--------|---------|----------------|
| Internal | NovaTech employees only | 1-3 days | No errors in Datadog |
| Alpha | 1% of target tier | 2-3 days | Error rate < 0.1%; p99 within budget |
| Beta | 5% of target tier | 1 week | CSAT no regression; error rate < 0.1% |
| Early Access | 25% of target tier | 1 week | Same as Beta |
| General Rollout | 50% → 100% | 2-3 days | Same as Beta |
| Full GA | 100% | — | Flag scheduled for removal |

### 3.3 Feature Flag Naming Convention

```
{team}-{feature-name}-{environment}

Examples:
  data-agentic-qa-api-prod
  platform-api-v3-beta-prod
  product-bulk-upload-prod
  data-search-vector-hybrid-prod
```

### 3.4 Rollback via Feature Flag

Feature flags provide an instant rollback mechanism for feature-level issues without requiring a code deployment:

```bash
# Disable a feature flag immediately via LaunchDarkly CLI
ld feature disable data-agentic-qa-api-prod

# Or via API
curl -X PATCH \
  https://app.launchdarkly.com/api/v2/flags/novatech/data-agentic-qa-api-prod \
  -H "Authorization: $LAUNCHDARKLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '[{"op": "replace", "path": "/environments/production/on", "value": false}]'
```

Flag changes take effect within **30 seconds** (LaunchDarkly streaming SDK).

---

## 4. Deployment Pipeline

### 4.1 Pipeline Overview

```
Developer pushes to PR branch
           │
           ▼
    CI Pipeline (GitHub Actions)
    ├── Lint + Format check
    ├── Unit tests
    ├── Integration tests
    ├── Security scan (Snyk + Gitleaks)
    ├── Docker image build
    └── PR status check (must be green for merge)
           │
           ▼
    Merge to main
           │
           ▼
    CD Pipeline (GitHub Actions - deploy.yml)
    ├── Docker image build + tag (SHA)
    ├── Push to ECR (novatech-shared account)
    └── Deploy to staging (auto)
           │
           ▼
    Staging Smoke Tests (automated - 10 min suite)
    ├── Authentication flow
    ├── Document upload + retrieval
    ├── Search query
    └── Webhook delivery
           │
           ▼
    [Wednesday 2:00 PM] Manual trigger: Production Deploy
           │
           ▼
    Canary Deploy (5% traffic - 15 min)
    ├── Datadog monitors active
    ├── Error rate < 0.5% threshold
    └── p99 latency < 1.1x baseline threshold
           │
     ┌─────┴─────┐
   Pass         Fail
     │             │
     ▼             ▼
  Full        Auto-Rollback
  Rollout     (< 2 min)
  (100%)
```

### 4.2 GitHub Actions Workflows

| Workflow | File | Trigger | Duration |
|---------|------|---------|---------|
| CI | `.github/workflows/ci.yml` | PR push, PR open | ~8 minutes |
| CD Staging | `.github/workflows/deploy-staging.yml` | Merge to main | ~12 minutes |
| CD Production (Canary) | `.github/workflows/deploy-prod-canary.yml` | Manual trigger | ~5 minutes |
| CD Production (Full) | `.github/workflows/deploy-prod-full.yml` | Manual (after canary) | ~10 minutes |
| Hotfix Deploy | `.github/workflows/hotfix-deploy.yml` | Tag push (`hotfix/*`) | ~8 minutes |

### 4.3 Kubernetes Rolling Update Configuration

```yaml
# Standard deployment rollout strategy (per service)
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 2           # Spin up 2 new pods before removing old ones
    maxUnavailable: 0     # Zero downtime — never remove until replacement is ready

# Pod disruption budget (ensures minimum replicas during node drain)
minAvailable: 2           # Always keep at least 2 pods running

# Readiness probe (pod not in rotation until this passes)
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5
  failureThreshold: 3
```

---

## 5. Rollback Procedure

### 5.1 Automated Rollback (Canary Phase)

During the 15-minute canary window, the pipeline automatically rolls back if:
- Error rate on new version > 0.5% (vs < 0.1% baseline)
- p99 latency > 1.5x baseline
- Any critical Datadog monitor fires (P0 severity)

Automated rollback completes in **< 2 minutes**.

### 5.2 Manual Rollback (Post-Full-Rollout)

If an issue is discovered after full rollout:

```bash
# Step 1: Identify the previous stable image SHA
kubectl rollout history deployment/search-service -n novatech-prod

# Step 2: Roll back to previous revision
kubectl rollout undo deployment/search-service -n novatech-prod

# Or roll back to specific revision
kubectl rollout undo deployment/search-service -n novatech-prod --to-revision=47

# Step 3: Monitor the rollback
kubectl rollout status deployment/search-service -n novatech-prod

# Step 4: Verify health
kubectl get pods -l app=search-service -n novatech-prod
```

**Target rollback time: < 5 minutes** from decision to completion.

### 5.3 Rollback Decision Tree

```
Issue detected post-release
        │
        ▼
Is the issue affecting >5% of users?
    ├── Yes → Declare P1 incident; initiate rollback
    └── No  → Can it be fixed with a feature flag?
                  ├── Yes → Disable feature flag immediately; create hotfix
                  └── No  → Assess impact; escalate to Release Manager
```

---

## 6. Database Migration Safety

### 6.1 Migration Principles

All database migrations must be **backwards-compatible**. This means:
- The old version of code must work with the new schema
- The new version of code must work with the old schema (during rolling deploy)
- Migrations are applied **before** code deployment
- Rollback migrations must be written alongside forward migrations

### 6.2 Migration Safety Checklist

Before applying any migration to production:

- [ ] Migration reviewed by DBA-designated engineer (Tom Okafor)
- [ ] Migration tested on staging with production-sized data (EXPLAIN ANALYZE run)
- [ ] Migration is zero-downtime (no `ACCESS EXCLUSIVE LOCK` for > 1 second)
- [ ] Rollback migration written and tested in staging
- [ ] Manual RDS snapshot taken (within 30 min of applying migration)
- [ ] Migration applied to staging and monitored for 24 hours
- [ ] On-call engineer standing by during production migration
- [ ] Migration scheduled during low-traffic window if > 1 minute estimated runtime

### 6.3 Online Schema Change Procedures

For large table migrations (> 10 million rows), use online schema change tools:

```bash
# For adding a NOT NULL column with a default (cannot do directly in PostgreSQL)
# Use pg_repack or run in multiple steps:

# Step 1: Add column as nullable
ALTER TABLE documents ADD COLUMN new_field VARCHAR(255);

# Step 2: Backfill in batches (do this in application code, not migration)
# Step 3: Add NOT NULL constraint after backfill complete
ALTER TABLE documents ALTER COLUMN new_field SET NOT NULL;

# For index creation on large tables (non-blocking):
CREATE INDEX CONCURRENTLY idx_documents_tenant_status 
ON documents(tenant_id, status);
```

---

## 7. Zero-Downtime Deployment Requirements

NovaTech's Enterprise SLA (99.95% uptime) requires zero-downtime deployments. The following requirements apply:

| Requirement | How Enforced |
|------------|-------------|
| No pod removed until replacement healthy | `maxUnavailable: 0` in rollout strategy |
| API gateway continues routing to healthy pods | Kong upstream health checks (5-second interval) |
| Database connections drained gracefully | `terminationGracePeriodSeconds: 60` on pods |
| In-flight requests completed | `preStop` hook: sleep 10 seconds before SIGTERM |
| No breaking database schema changes | Backwards-compat policy + DBA review |
| Session/cache continuity | Stateless services; Redis-backed sessions survive pod restart |

---

## 8. Release Notes Format

Release notes are published to:
1. Internal: `#eng-releases` Slack channel + Confluence Changelog page
2. Customer-facing: In-app changelog (app.novatech.io/changelog) + email for breaking changes

### 8.1 Standard Release Note Template

```markdown
## NovaTech Release v2.X.Y — [Date]

### New Features
- **[Feature Name]:** Brief description. [Link to docs]

### Improvements
- **[Component]:** Brief description of improvement.

### Bug Fixes
- Fixed [brief description] (affected [customer names or "some customers"])

### Security
- [If applicable: description of security fix]

### Deprecations
- **Deprecation Notice:** [Feature/endpoint] is deprecated as of this release. 
  Sunset date: [date]. Migration guide: [link]

### Breaking Changes
- **[API/Feature Change]:** [Description of breaking change and migration path]
```

---

## 9. Customer Communication for Breaking Changes

### 9.1 Communication Requirements

| Change Type | Notice Period | Communication Channel |
|------------|-------------|----------------------|
| Breaking API change | 90 days minimum | Email (all affected) + in-app banner + docs |
| Endpoint deprecation | 12 months minimum | Email + in-app banner |
| Feature removal | 60 days minimum | Email + in-app banner |
| Behavior change (non-breaking) | 2 weeks | Release notes + in-app changelog |

### 9.2 Breaking Change Communication Process

1. **Draft communication** reviewed by: Engineering Lead, Product Manager, Legal (for any liability implications)
2. **Customer Success** team is briefed 1 week before customer communication goes out
3. **Account Executives** briefed for Enterprise accounts — must be able to answer questions
4. **Communication sent** to technical contacts at all affected customer accounts
5. **Migration guide** published in docs before communication is sent (customers can act immediately)
6. **Office hours** scheduled: weekly 30-min Zoom for customers to ask migration questions

---

## 10. Hotfix Process

### 10.1 When to Hotfix

A hotfix bypasses the release train and deploys directly to production. Hotfixes are appropriate for:
- P0/P1 production incidents requiring immediate code fix
- Security vulnerabilities (CVSS 7.0+)
- Data integrity issues

**Hotfixes require VP Engineering approval** (or SRE Lead if VP unavailable).

### 10.2 Hotfix Procedure

```bash
# Step 1: Create hotfix branch from main (or from the current release tag)
git checkout -b hotfix/ENG-2912-auth-token-dst-fix v2.13.2

# Step 2: Apply the minimal fix; get expedited review (1 senior reviewer, 4-hour SLA)
# Step 3: Merge to hotfix branch and trigger hotfix pipeline
git tag hotfix/eng-2912-20260314
git push origin hotfix/eng-2912-20260314

# Hotfix pipeline deploys directly (no staging wait):
# Build → Integration tests → Staging (5-min smoke test) → Production Canary → Full
# Total time: ~15-20 minutes

# Step 4: Merge hotfix back to main
git checkout main
git merge hotfix/ENG-2912-auth-token-dst-fix

# Step 5: Release Manager publishes hotfix release notes
```

---

*This guide is maintained by the SRE team and Release Management rotation. For deployment issues, ping `#deployments` on Slack or contact the current Release Manager.*
