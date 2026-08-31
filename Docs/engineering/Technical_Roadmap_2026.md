# NovaTech Solutions — Engineering Technical Roadmap 2026

**Document Version:** 1.4  
**Last Updated:** February 20, 2026  
**Authors:** Priya Nair (VP Engineering), Marcus Webb (Principal Architect)  
**Classification:** Internal — Engineering + Leadership  
**Review Cycle:** Monthly roadmap reviews; quarterly major updates

---

## 1. Executive Summary

This document outlines the NovaTech Solutions engineering roadmap for calendar year 2026. The roadmap is organized around two thematic halves:

- **H1 2026 (Q1–Q2): Performance, Enterprise Scale, and Compliance**
  Focus on resolving known performance bottlenecks (ENG-2847: search performance for large tenants), achieving SOC 2 Type II re-certification, and delivering the Enterprise API v3 that will unlock new partnership opportunities.

- **H2 2026 (Q3–Q4): AI Leadership, HIPAA Readiness, and Platform Maturity**
  Expanding our AI-powered features (Agentic RAG, document intelligence), pursuing HIPAA compliance to unlock healthcare verticals, and maturing the platform's edge architecture and observability.

**Total Engineering Capacity 2026:** ~48 engineers × 46 working weeks = ~2,208 engineer-weeks

**Allocated to Roadmap Epics:** ~1,400 engineer-weeks (~63%)  
**Allocated to Tech Debt/Maintenance:** ~440 engineer-weeks (~20%)  
**Allocated to On-Call/Operational Work:** ~368 engineer-weeks (~17%)

---

## 2. H1 2026 Themes: Performance, Enterprise Scale, Compliance

### 2.1 Theme: Performance

Customer satisfaction is directly tied to platform performance. The #1 complaint in Q1 2026 CSAT surveys is search performance for large document sets. H1 is heavily focused on eliminating these bottlenecks.

**Key Metrics to Improve:**
- Search p99 latency from 8.3 seconds → < 1.5 seconds for tenants with > 5M documents
- Document upload processing time p99 from 42 seconds → < 15 seconds
- API gateway overhead from avg 45ms → < 20ms

### 2.2 Theme: Enterprise Scale

NovaTech's growth in the Enterprise segment (customers > $100K ARR) requires infrastructure and API capabilities that scale reliably. Enterprise API v3 and multi-tenant isolation improvements are priorities.

### 2.3 Theme: Compliance

SOC 2 Type II re-certification audit window opens February 2026. HIPAA readiness assessment (targeting healthcare vertical expansion) must be completed by end of Q3 2026.

---

## 3. Roadmap Epics — H1 2026

---

### Epic 1: Multi-Tenant Search Performance Overhaul

**Epic ID:** EPIC-2026-01  
**Owner:** Rajesh Kumar (Engineering Manager, Data Team)  
**Target Quarter:** Q1 2026 (primary), Q2 2026 (validation + rollout)  
**Priority:** P0 — Critical  
**Status:** In Progress (started February 2026)

**Problem Statement:**
Tenants with > 10 million indexed documents are experiencing search query latencies of 8–12 seconds at p99, versus our SLA target of < 2 seconds. This is affecting ACME Corp (11.2M documents), Pinnacle Systems (8.7M documents), and 3 other tenants. ACME Corp's VP of Technology escalated at the March 5, 2026 QBR, and the account is at risk.

**Engineering Approach:**
1. **Phase 1 (Q1 — In Progress):** Elasticsearch shard strategy optimization. Current sharding is uniform; large tenants need custom shard allocation with dedicated data nodes. Migrate top 5 tenants to dedicated Elasticsearch node pools.
2. **Phase 2 (Q1):** Query optimization. Implement query-time filter caching, increase field data cache, and optimize KNN vector search parameters for large indices.
3. **Phase 3 (Q2):** Index tiering. Move documents older than 24 months to a cold tier (Elasticsearch frozen indices) to reduce heap pressure on active search.
4. **Phase 4 (Q2):** Redis query result cache expansion. Increase cache TTL for common queries; implement predictive cache warming for power users.

**Engineering Estimate:** 42 engineer-weeks total  
**Dependencies:** Elasticsearch 8.13 upgrade (Phase 2), additional EC2 capacity ($4,200/month cost increase during Phase 1)  
**Success Criteria:** p99 search latency < 1.5 seconds for all tenants including those with > 10M documents by April 15, 2026  
**Risk:** Elasticsearch version upgrade may require maintenance window; coordinate with SRE

---

### Epic 2: Agentic RAG Features (Q&A, Multi-Step Reasoning)

**Epic ID:** EPIC-2026-02  
**Owner:** Aisha Okonkwo (Engineering Manager, Data Team — AI)  
**Target Quarter:** Q1–Q2 2026  
**Priority:** P1 — High  
**Status:** Q1 design complete; development started Q1 2026

**Problem Statement:**
The AI Service launched in Q4 2025 with basic semantic search and document summarization. Customers (particularly GlobalTech Inc. and Meridian Enterprises) are requesting agentic AI features: multi-step reasoning over document collections, automated document comparison, and intelligent Q&A with source attribution.

**Engineering Approach:**
1. **Phase 1 (Q1):** Agentic Q&A API — `POST /v2/ai/qa` endpoint (launched March 2026). Accept a natural language question, retrieve relevant document chunks via RAG pipeline, synthesize an answer with citations.
2. **Phase 2 (Q1–Q2):** Multi-document reasoning — users can query across a tagged collection of documents. The agent retrieves from multiple documents and synthesizes a comparative answer.
3. **Phase 3 (Q2):** Streaming responses via Server-Sent Events (SSE). Reduces perceived latency from 8–10 seconds to near-instant first-token responses.
4. **Phase 4 (Q2):** Agentic workflows — scheduled AI processing jobs (e.g., "summarize all new documents added this week and email me").

**Engineering Estimate:** 56 engineer-weeks total  
**Dependencies:** OpenAI API contract upgrade (for higher rate limits), Anthropic API (for Claude 3.5 Sonnet integration), AI Service hardening (reliability improvements)  
**Success Criteria:** Q&A API GA in Q2 with < 8s p99 latency; 3+ Enterprise customers onboarded to beta by March 31, 2026  
**LLM Cost Estimate:** ~$0.08 per Q&A query at current volume; $12,000/month projected at full scale

---

### Epic 3: SOC 2 Type II Re-Certification (Audit Period Feb–Jul 2026)

**Epic ID:** EPIC-2026-03  
**Owner:** Anita Sharma (Security Champion, Staff Engineer)  
**Target Quarter:** Q1 (controls implementation) + Q2 (audit window closes)  
**Priority:** P0 — Business Critical  
**Status:** Audit period active. Controls evidence collection ongoing.

**Problem Statement:**
NovaTech's SOC 2 Type II certification (issued August 2025) covers the period February–July 2025. The 2026 certification must cover February–July 2026 to maintain continuous certification for enterprise sales.

**Engineering Tasks:**
1. Maintain all existing controls (access reviews, change management, incident response, encryption)
2. Close 3 open gaps identified in 2025 audit:
   - Insufficient rate limiting on password reset endpoint → Fix targeting Q2 (ENG-2765)
   - Missing audit log for bulk document delete operations → Fix targeting Q1 (ENG-2878)
   - Incomplete automated certificate rotation for internal services → Fix targeting Q1 (ENG-2879)
3. Expand monitoring: Vanta automated evidence collection coverage from 68% → 90%
4. Auditor (Schellman & Company) on-site review: scheduled June 8–12, 2026
5. Report delivery expected: August 15, 2026

**Engineering Estimate:** 18 engineer-weeks (distributed across platform and security)  
**Dependencies:** Schellman & Company engagement; Legal team (contract) confirmed  
**Success Criteria:** No new audit exceptions; certification delivered before September 1, 2026

---

### Epic 4: Enterprise API v3 (Beta Q2, GA Q3)

**Epic ID:** EPIC-2026-04  
**Owner:** Elena Vasquez (API Platform Lead)  
**Target Quarter:** Q2 2026 (Beta), Q3 2026 (GA)  
**Priority:** P1 — High  
**Status:** Design phase (RFC circulated February 2026)

**Problem Statement:**
API v2, launched Q3 2024, has several design inconsistencies that have accumulated as the platform grew. Enterprise customers are requesting improvements: better bulk operation support, improved pagination, standardized error formats, and new capabilities (native async operations, webhook pagination, streaming).

**Key v3 Changes:**
1. Cursor-only pagination (removes offset pagination)
2. Error codes in dot.notation (e.g., `document.not_found` vs `DOCUMENT_NOT_FOUND`)
3. Native async job API (`POST /v3/jobs`, `GET /v3/jobs/{id}`) for bulk and long-running operations
4. Streaming support (SSE) for AI endpoints and bulk exports
5. Webhooks v2: pagination, filtering, replay capability

**Engineering Estimate:** 64 engineer-weeks total  
**Dependencies:** v1 sunset (July 2026 — reduces maintenance burden), SDK v3 updates (Python, JS, Java)  
**Success Criteria:** v3 Beta available June 30, 2026; 2+ Enterprise customers using beta; GA by September 30, 2026  
**Migration Support:** Dedicated migration guide, SDK auto-migration tools, 18-month overlap period with v2

---

### Epic 5: Observability Upgrade (Datadog RUM + Enhanced SLOs)

**Epic ID:** EPIC-2026-05  
**Owner:** Kevin Osei (SRE Lead)  
**Target Quarter:** Q1 2026  
**Priority:** P1 — High  
**Status:** 60% complete (January start)

**Engineering Tasks:**
1. Datadog Real User Monitoring (RUM) for the React frontend — capture real user page load times, JavaScript errors, and user journey flows
2. Define and implement SLO burn rate alerts for all 12 services (replacing threshold-based alerts)
3. Implement distributed trace sampling strategy (reduce cost by 40% via head-based sampling)
4. Custom business metric dashboards: documents indexed per day, search queries per minute by tier, AI query volume

**Engineering Estimate:** 16 engineer-weeks  
**Success Criteria:** RUM deployed by February 28, 2026; all SLOs defined and alerted by March 31, 2026

---

## 4. Roadmap Epics — H2 2026

---

### Epic 6: HIPAA Readiness

**Epic ID:** EPIC-2026-06  
**Owner:** Priya Nair (VP Engineering, sponsoring) / Anita Sharma (lead)  
**Target Quarter:** Q3 2026  
**Priority:** P1 — High (blocks healthcare vertical sales)  
**Status:** Gap assessment in progress (Q1 2026)

**Problem Statement:**
NovaTech has received inbound interest from 4 healthcare organizations (hospitals, health systems) representing ~$1.2M potential ARR. Healthcare customers require HIPAA compliance (BAA in place, Technical Safeguards compliant). NovaTech is currently not HIPAA-compliant.

**Gap Analysis Findings (Preliminary):**
- Audit logs: Complete (Audit Service meets 45 CFR 164.312 requirements)
- Data encryption: Complete (AES-256 at rest, TLS 1.3 in transit)
- Access controls: Mostly complete; need unique user identification enforcement
- Data backup: Complete
- Data integrity: Need file integrity monitoring (FIM) for document storage
- Transmission security: Complete
- BAA framework: Legal drafting (Q2 2026 target)

**Engineering Tasks:**
1. PHI data isolation: Dedicated RDS instances and S3 buckets for HIPAA tenants
2. Unique user identification enforcement (disable shared accounts)
3. File integrity monitoring (FIM) for S3 document storage
4. HIPAA audit log report generation (monthly, automated)
5. Emergency access procedures documentation
6. Training: Security awareness training with HIPAA module (all engineers)

**Engineering Estimate:** 32 engineer-weeks  
**Dependencies:** Legal (BAA template), external HIPAA consultant ($25,000 budget approved), healthcare-focused sales hire (in progress)  
**Success Criteria:** External HIPAA readiness assessment passed by September 30, 2026; first BAA signed

---

### Epic 7: Edge Caching and Global Performance

**Epic ID:** EPIC-2026-07  
**Owner:** Marcus Webb (Principal Architect)  
**Target Quarter:** Q3 2026  
**Priority:** P2 — Medium  
**Status:** Design phase planned for Q2

**Problem Statement:**
International customers (primarily EU and APAC) experience 40–80ms additional latency due to all API traffic routing to us-east-1. CloudFront currently caches only static assets. Enterprise customers in EU are requesting < 100ms API latency guarantees.

**Approach:**
1. CloudFront API caching for GET endpoints with appropriate cache-control headers
2. Lambda@Edge for request authentication at the edge (validate JWTs without round-trip to us-east-1)
3. EU regional stack (eu-west-1) for EU-resident customers: Document Service + Search Service regional deployment
4. APAC feasibility study (Singapore region)

**Engineering Estimate:** 38 engineer-weeks  
**Dependencies:** Data residency legal analysis (Q2), additional infrastructure budget ($18,000/month for EU region)

---

### Epic 8: Agentic Workflows (H2 Expansion)

**Epic ID:** EPIC-2026-08  
**Owner:** Aisha Okonkwo (Engineering Manager, AI)  
**Target Quarter:** Q3–Q4 2026  
**Priority:** P1 — High  
**Status:** Planned (builds on EPIC-2026-02 Phase 4)

**Description:**
Expand the Workflow Service to support AI-driven automation: intelligent document routing, auto-tagging, automated compliance checking, and scheduled AI summaries. Integration with Slack, Teams, and email for AI-generated digests.

**Engineering Estimate:** 48 engineer-weeks  
**Success Criteria:** Agentic Workflow feature in GA by December 31, 2026; 5+ Enterprise customers using workflows

---

## 5. Roadmap Summary Table

| Epic | Theme | Target | Owner | Eng-Weeks | Priority | Status |
|------|-------|--------|-------|-----------|---------|--------|
| EPIC-01: Search Performance | Performance | Q1–Q2 | Rajesh Kumar | 42 | P0 | In Progress |
| EPIC-02: Agentic RAG | AI Features | Q1–Q2 | Aisha Okonkwo | 56 | P1 | In Progress |
| EPIC-03: SOC 2 Re-cert | Compliance | Q1–Q2 | Anita Sharma | 18 | P0 | Active |
| EPIC-04: Enterprise API v3 | Enterprise Scale | Q2–Q3 | Elena Vasquez | 64 | P1 | Design |
| EPIC-05: Observability | Platform Health | Q1 | Kevin Osei | 16 | P1 | 60% Done |
| EPIC-06: HIPAA Readiness | Compliance | Q3 | Anita Sharma | 32 | P1 | Assessment |
| EPIC-07: Edge Caching | Performance | Q3 | Marcus Webb | 38 | P2 | Planned |
| EPIC-08: Agentic Workflows | AI Features | Q3–Q4 | Aisha Okonkwo | 48 | P1 | Planned |

**Total roadmap capacity commitment: 314 engineer-weeks (H1: 192, H2: 122)**

---

## 6. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Search performance fix delayed | Medium | High (ACME Corp at risk) | Dedicated Data Team sprint; weekly progress reviews |
| SOC 2 audit exception | Low | High (sales blocker) | Vanta monitoring; close all gaps by April |
| Engineering hiring shortfall | Medium | Medium (roadmap slip) | 6 open headcount positions; recruiting intensified |
| LLM API costs exceed budget | Medium | Medium (AI features) | Cost caps + caching; Anthropic contract negotiation |
| HIPAA compliance timeline | Medium | Medium (Q4 sales pipeline) | External consultant engaged; healthcare BD paused until Q4 |

---

*Roadmap is reviewed monthly in Engineering All-Hands and monthly leadership sync. Last reviewed: February 20, 2026. Next review: March 20, 2026. Contact Priya Nair with questions.*
