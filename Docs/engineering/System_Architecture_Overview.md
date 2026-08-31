# NovaTech Solutions — System Architecture Overview

**Document Version:** 3.4  
**Last Updated:** February 14, 2026  
**Authors:** Priya Nair (VP Engineering), Marcus Webb (Principal Architect), Anita Sharma (Staff Engineer)  
**Classification:** Internal — Engineering Confidential  
**Review Cycle:** Quarterly

---

## 1. Executive Summary

NovaTech Solutions operates a cloud-native, microservices-based platform designed to serve enterprise customers at scale. The platform processes over 14 million API requests per day, indexes more than 2.8 billion documents across all customer tenants, and maintains a 99.95% uptime SLA for Enterprise-tier customers. This document provides a comprehensive overview of the system architecture, including service topology, data flows, infrastructure design, security layers, and disaster recovery posture.

The architecture is built on twelve (12) independently deployable microservices, orchestrated on Amazon Elastic Kubernetes Service (EKS), with a polyglot persistence strategy leveraging PostgreSQL, Redis, Elasticsearch, and object storage via Amazon S3.

---

## 2. Architectural Principles

The following principles guide all architectural decisions at NovaTech Solutions:

1. **Multi-Tenancy by Design:** Every service is tenant-aware. Tenant isolation is enforced at the data, compute, and network layers.
2. **Scalability First:** Services are designed to scale horizontally. Stateless services scale to zero during off-peak hours.
3. **Resilience over Efficiency:** Circuit breakers, bulkheads, and retry budgets are standard. No single point of failure is acceptable in the critical path.
4. **Security in Depth:** Authentication and authorization are enforced at every service boundary. Zero-trust networking is enforced via service mesh (Istio).
5. **Observability as a Feature:** Every service emits structured logs, distributed traces, and business metrics. SLOs are defined and tracked for all user-facing services.
6. **API-First Design:** All features are API-accessible. Internal service communication uses the same quality standards as external APIs.

---

## 3. High-Level Architecture Diagram

```
                          ┌─────────────────────────────────────────────────┐
                          │               Internet / Customers                │
                          └────────────────────┬────────────────────────────┘
                                               │
                          ┌────────────────────▼────────────────────────────┐
                          │         CloudFront CDN (Edge Layer)              │
                          │    Edge Locations: us-east-1, eu-west-1,         │
                          │    ap-southeast-1                                │
                          └────────────────────┬────────────────────────────┘
                                               │
                          ┌────────────────────▼────────────────────────────┐
                          │         AWS WAF + Shield Advanced                │
                          │    DDoS mitigation, rate limiting, geo-blocking  │
                          └────────────────────┬────────────────────────────┘
                                               │
                          ┌────────────────────▼────────────────────────────┐
                          │              API Gateway (Kong)                  │
                          │    Auth enforcement, rate limiting, routing,     │
                          │    request/response transformation, logging      │
                          └────┬───────────┬──────────┬────────┬────────────┘
                               │           │          │        │
              ┌────────────────▼─┐  ┌──────▼──┐  ┌───▼──┐  ┌─▼──────────┐
              │   Auth Service   │  │  Doc     │  │Search│  │Notification│
              │   (Port 8001)    │  │  Service │  │Svc   │  │Service     │
              └──────────────────┘  └──────────┘  └──────┘  └────────────┘
                                          │            │
                          ┌───────────────┼────────────┼──────────────────┐
                          │               │   Kafka     │                  │
                          │               │  Message    │                  │
                          │               │    Bus      │                  │
                          └───────────────┼─────────────┼─────────────────┘
                                          │             │
                          ┌───────────────▼─────────────▼─────────────────┐
                          │          Persistence Layer                      │
                          │   PostgreSQL | Redis | Elasticsearch | S3       │
                          └─────────────────────────────────────────────────┘
```

---

## 4. Microservices Inventory

NovaTech Solutions currently operates **12 production microservices**. Each service has a dedicated team, owns its data store, and communicates with other services exclusively through defined API contracts or Kafka topics.

### 4.1 Auth Service
- **Purpose:** Handles all authentication and authorization for the platform. Issues and validates JWT tokens, manages OAuth 2.0 flows, handles SAML 2.0 SSO integrations, and enforces RBAC policies.
- **Tech Stack:** Python 3.12 / FastAPI, PostgreSQL (user/session store), Redis (token blacklist cache)
- **Endpoints:** `/auth/login`, `/auth/logout`, `/auth/token/refresh`, `/auth/oauth/authorize`, `/auth/oauth/callback`, `/auth/saml/acs`
- **SLO:** 99.99% availability, p99 latency < 80ms
- **Team Owner:** Platform Team
- **Deployment:** 3 replicas minimum, HPA max 20 replicas

### 4.2 Document Service
- **Purpose:** Core service for document ingestion, storage, metadata management, versioning, and lifecycle management. Manages upload workflows, virus scanning, format conversion, and storage orchestration.
- **Tech Stack:** Python 3.12 / FastAPI, PostgreSQL (metadata), S3 (object storage), SQS (async processing queue)
- **Endpoints:** `/documents`, `/documents/{id}`, `/documents/{id}/versions`, `/documents/bulk`
- **SLO:** 99.95% availability, p99 latency < 500ms for upload initiation
- **Team Owner:** Product Team
- **Deployment:** 5 replicas minimum, HPA max 30 replicas

### 4.3 Search Service
- **Purpose:** Provides full-text and semantic search across indexed documents. Manages Elasticsearch index lifecycle, query routing, search ranking, and faceting. Supports hybrid search combining BM25 and vector similarity.
- **Tech Stack:** Python 3.12 / FastAPI, Elasticsearch 8.12, Redis (query result cache)
- **Endpoints:** `/search`, `/search/suggest`, `/search/filters`, `/search/export`
- **SLO:** 99.9% availability, p99 latency < 2000ms, p50 latency < 300ms
- **Team Owner:** Data Team
- **Deployment:** 4 replicas minimum, HPA max 25 replicas
- **Known Issue:** Performance degradation observed for tenants with > 10M documents (ENG-2847, under active investigation as of March 2026)

### 4.4 Notification Service
- **Purpose:** Manages delivery of email, in-app, and webhook notifications. Handles template rendering, delivery scheduling, retry logic, and delivery status tracking.
- **Tech Stack:** Python 3.12 / FastAPI, PostgreSQL (notification log), Redis (deduplication), SendGrid (email), Twilio (SMS)
- **Endpoints:** `/notifications`, `/notifications/preferences`, `/notifications/templates`
- **SLO:** 99.9% availability, email delivery p99 < 30 seconds
- **Team Owner:** Product Team

### 4.5 Analytics Service
- **Purpose:** Collects usage events, computes tenant-level metrics, generates reports, and powers the admin analytics dashboard. Stores time-series data for trend analysis.
- **Tech Stack:** Python 3.12 / FastAPI, PostgreSQL (aggregated metrics), ClickHouse (event store), Redis (real-time counters)
- **Endpoints:** `/analytics/usage`, `/analytics/reports`, `/analytics/export`, `/analytics/dashboard`
- **SLO:** 99.5% availability (non-critical path), data freshness < 5 minutes
- **Team Owner:** Data Team

### 4.6 User Management Service
- **Purpose:** Manages user profiles, roles, permissions, tenant memberships, and directory sync (SCIM 2.0). Handles user lifecycle from provisioning to deprovisioning.
- **Tech Stack:** Python 3.12 / FastAPI, PostgreSQL
- **Endpoints:** `/users`, `/users/{id}`, `/users/bulk`, `/roles`, `/permissions`, `/scim/v2`
- **SLO:** 99.95% availability, p99 latency < 150ms
- **Team Owner:** Platform Team

### 4.7 Billing Service
- **Purpose:** Manages subscription plans, usage metering, invoice generation, and payment processing. Integrates with Stripe for payment collection and Chargebee for subscription management.
- **Tech Stack:** Python 3.12 / FastAPI, PostgreSQL, Stripe API, Chargebee API
- **Endpoints:** `/billing/subscriptions`, `/billing/invoices`, `/billing/usage`, `/billing/payment-methods`
- **SLO:** 99.95% availability; financial transactions are idempotent and audited
- **Team Owner:** Platform Team

### 4.8 Integration Service
- **Purpose:** Manages third-party integrations (Salesforce, Slack, Google Drive, Microsoft 365, Zapier). Handles OAuth flows for external services, webhook ingestion from third parties, and data sync workflows.
- **Tech Stack:** Python 3.12 / FastAPI, PostgreSQL (integration configs), Redis (OAuth state), Kafka (event publishing)
- **Endpoints:** `/integrations`, `/integrations/{provider}`, `/integrations/webhooks`
- **SLO:** 99.5% availability
- **Team Owner:** Product Team

### 4.9 Workflow Service
- **Purpose:** Powers automation workflows including document approval chains, scheduled processing tasks, and event-driven automations. Uses a DAG-based execution engine.
- **Tech Stack:** Python 3.12 / FastAPI, PostgreSQL (workflow definitions and state), Celery + Redis (task queue)
- **Endpoints:** `/workflows`, `/workflows/{id}/runs`, `/workflows/triggers`
- **SLO:** 99.5% availability
- **Team Owner:** Product Team

### 4.10 Audit Service
- **Purpose:** Immutable audit log for all user actions, admin operations, and system events. Provides compliance reporting for SOC 2, HIPAA, and GDPR requirements.
- **Tech Stack:** Python 3.12 / FastAPI, PostgreSQL (append-only log), S3 (long-term archival)
- **Endpoints:** `/audit/events`, `/audit/reports`, `/audit/export`
- **SLO:** 99.99% write availability (no audit event may be dropped), read 99.5%
- **Team Owner:** Platform Team

### 4.11 AI Service
- **Purpose:** Powers AI features including semantic search embeddings, document summarization, Q&A over documents, and agentic RAG workflows. Manages LLM prompt routing and response caching.
- **Tech Stack:** Python 3.12 / FastAPI, Elasticsearch (vector index), Redis (semantic cache), OpenAI API, Anthropic API
- **Endpoints:** `/ai/search`, `/ai/summarize`, `/ai/qa`, `/ai/embeddings`
- **SLO:** 99.0% availability, p99 latency < 10s (LLM-dependent)
- **Team Owner:** Data Team
- **Status:** Launched Q4 2025, actively expanding in 2026

### 4.12 Admin Service
- **Purpose:** Internal-facing service for NovaTech operations team. Provides tenant management, feature flag management, support tooling, and operational dashboards.
- **Tech Stack:** Python 3.12 / FastAPI, PostgreSQL, React (admin UI)
- **Endpoints:** `/admin/tenants`, `/admin/feature-flags`, `/admin/impersonate`, `/admin/metrics`
- **SLO:** 99.5% availability (internal traffic only)
- **Team Owner:** Platform Team

---

## 5. Technology Stack Summary

| Layer | Technology | Version | Notes |
|-------|-----------|---------|-------|
| Backend API | Python / FastAPI | 3.12 / 0.109 | All microservices |
| Frontend | React / TypeScript | 18.2 / 5.3 | Single SPA with module federation |
| API Gateway | Kong Gateway | 3.5 | Self-hosted on EKS |
| Container Orchestration | Kubernetes (EKS) | 1.29 | 3 node groups per cluster |
| Primary Database | PostgreSQL (RDS) | 15.4 | Per-service databases |
| Cache | Redis (ElastiCache) | 7.2 | Cluster mode enabled |
| Search Engine | Elasticsearch | 8.12 | 9-node cluster, 3 dedicated masters |
| Message Bus | Apache Kafka (MSK) | 3.6 | 6 brokers, 3 AZs |
| Object Storage | AWS S3 | — | Versioning + lifecycle policies |
| CDN | AWS CloudFront | — | 450+ edge locations |
| Service Mesh | Istio | 1.20 | mTLS between all services |
| Observability | Datadog | — | APM, logs, metrics, synthetics |
| Secret Management | AWS Secrets Manager | — | All credentials |
| Infrastructure as Code | Terraform | 1.7 | Terragrunt for DRY configs |
| CI/CD | GitHub Actions | — | Workflows in `.github/workflows/` |
| Feature Flags | LaunchDarkly | — | All feature gates |

---

## 6. Data Flow: Document Upload and Search

### 6.1 Document Upload Flow

```
Customer Browser/API Client
        │
        ▼
  CloudFront CDN ──► API Gateway (Kong)
        │
        ▼
  Auth Service (JWT validation)
        │
        ▼
  Document Service
        │
        ├──► S3 (multipart upload, max 5GB)
        │
        ├──► SQS Queue (async processing job)
        │
        ▼
  Document Processor (Worker)
        │
        ├──► ClamAV (virus scan)
        │
        ├──► Tika (content extraction)
        │
        ├──► AI Service (embedding generation)
        │
        └──► Kafka Topic: document.indexed
                    │
                    ▼
              Search Service (index update)
              Audit Service (event log)
              Analytics Service (usage event)
              Notification Service (confirm email)
```

### 6.2 Search Query Flow

```
Customer Search Request
        │
        ▼
  API Gateway ──► Auth + Rate Limit Check
        │
        ▼
  Search Service
        │
        ├──► Redis Cache Check (cache hit → return immediately)
        │
        ├──► Query Expansion (synonyms, stemming)
        │
        ├──► Elasticsearch Query (BM25 + KNN hybrid)
        │           │
        │           ├── Document metadata (title, tags, author)
        │           ├── Full-text content index
        │           └── Vector index (dense_vector field)
        │
        ├──► Results Re-ranking (ML model)
        │
        ├──► Tenant Permission Filter (document ACL enforcement)
        │
        ├──► Redis Cache Write (TTL 300s)
        │
        └──► Response to Client
```

---

## 7. Multi-Tenancy Design

NovaTech uses a **shared infrastructure, logically isolated** multi-tenancy model with the following enforcement mechanisms:

### 7.1 Data Isolation
- **PostgreSQL:** Each tenant has a dedicated schema within a shared RDS cluster. Row-level security (RLS) policies enforce tenant isolation at the database level as a secondary defense.
- **Elasticsearch:** Each tenant has dedicated index aliases. Index naming convention: `novatech-{tenant_id}-documents-{YYYY-MM}`. Cross-tenant queries are blocked at the application layer and validated by Elasticsearch index-level security.
- **S3:** Objects are stored under tenant-scoped prefixes: `s3://novatech-documents-prod/{tenant_id}/{document_id}`. IAM policies enforce no cross-tenant access.
- **Redis:** All keys are namespaced by tenant ID: `{tenant_id}:{cache_type}:{cache_key}`.

### 7.2 Compute Isolation
- Enterprise customers with > $100K ARR receive dedicated node pools in EKS with taints/tolerations.
- Standard and Professional tier customers share node pools with namespace-level resource quotas.
- CPU/memory limits are enforced at the Kubernetes namespace level.

### 7.3 Network Isolation
- Istio service mesh enforces mutual TLS (mTLS) between all services.
- Network policies block all inter-namespace traffic except explicitly allowed paths.
- Enterprise customers may opt for dedicated VPC peering for API access.

---

## 8. API Gateway Configuration

Kong Gateway serves as the primary API Gateway, handling:

- **JWT Authentication:** Validates tokens issued by the Auth Service. Public key fetched from JWKS endpoint.
- **Rate Limiting:** Standard tier: 1,000 req/min. Professional: 2,500 req/min. Enterprise: 5,000 req/min. Rate limits are per-tenant and enforced using Redis counters.
- **Request Routing:** Path-based routing to upstream microservices. Canary routing (weighted) for gradual rollouts.
- **Request/Response Transformation:** Header injection (tenant ID, request ID, trace ID), response compression (gzip/br).
- **Logging:** All requests logged to Datadog with full request metadata. PII fields are masked.
- **Health Checks:** Active upstream health checks every 5 seconds. Unhealthy upstreams removed from rotation automatically.

---

## 9. CDN and Edge Architecture

CloudFront is configured for:

- **Static Assets:** React application bundle, images, fonts. Cache TTL 365 days (content-addressed).
- **API Caching:** GET requests for public endpoints cached at edge for 60 seconds.
- **Geographic Restrictions:** Blocked regions per export compliance requirements.
- **Origin Shield:** Enabled in us-east-1 to reduce origin load during cache misses.
- **Edge Locations Active:** 450+ globally. Primary traffic served from us-east-1 (North America), eu-west-1 (Europe), ap-southeast-1 (APAC).

---

## 10. Security Architecture

### 10.1 Defense in Depth Layers

| Layer | Control | Technology |
|-------|---------|-----------|
| Edge | DDoS protection, WAF rules | AWS Shield Advanced, AWS WAF |
| DNS | DNSSEC, CAA records | Route 53 |
| Transport | TLS 1.3 minimum, HSTS | CloudFront, ALB |
| API Gateway | Auth enforcement, rate limiting | Kong |
| Service Mesh | mTLS between services | Istio |
| Application | RBAC, tenant isolation | Custom middleware |
| Data | Encryption at rest (AES-256) | RDS, S3, ElastiCache |
| Secrets | No secrets in code or env | AWS Secrets Manager |
| Audit | Immutable event log | Audit Service |

### 10.2 Encryption Standards
- **In Transit:** TLS 1.3 enforced. TLS 1.0/1.1 disabled. TLS 1.2 allowed for legacy SDK compatibility (deprecated Q2 2026).
- **At Rest:** RDS encrypted with AWS KMS (AES-256). S3 server-side encryption (SSE-S3). ElastiCache encryption at rest enabled.
- **Application Level:** Customer PII fields encrypted with tenant-specific keys using AWS KMS envelope encryption.

---

## 11. Disaster Recovery Architecture

### 11.1 Recovery Objectives
- **RTO (Recovery Time Objective):** 4 hours for full platform recovery
- **RPO (Recovery Point Objective):** 15 minutes maximum data loss

### 11.2 Multi-AZ Active-Active Design
All production infrastructure spans **three Availability Zones** (us-east-1a, us-east-1b, us-east-1c):
- EKS node groups distributed across all 3 AZs
- RDS Multi-AZ with synchronous replication
- ElastiCache Redis cluster with cross-AZ replica shards
- Kafka brokers distributed across 3 AZs (replication factor 3, min ISR 2)
- ALB distributes traffic across all healthy AZs

### 11.3 Cross-Region DR
A **passive warm standby** environment is maintained in **us-west-2**:
- RDS read replica with automated promotion procedure
- S3 cross-region replication (CRR) for document storage (RPO ~1 minute)
- Elasticsearch cross-cluster replication (CCR) with ~5-minute lag
- Route 53 health checks with automatic failover (DNS TTL 60 seconds)
- Estimated activation time: 30-45 minutes for full failover

### 11.4 Backup Schedule
| Component | Backup Frequency | Retention | Recovery Method |
|-----------|-----------------|-----------|----------------|
| RDS PostgreSQL | Continuous (PITR) | 35 days | Point-in-time restore |
| RDS Snapshots | Daily automated | 90 days | Snapshot restore |
| S3 Documents | Versioning + CRR | Indefinite | Version restore |
| Elasticsearch | Snapshots to S3 | 30 days | Snapshot restore |
| Redis | RDB snapshots | 7 days | Snapshot restore |

### 11.5 DR Testing
- Full DR failover drill conducted **twice annually** (last: November 2025, next: May 2026)
- Tabletop exercises conducted quarterly with Engineering and Operations leadership
- RTO/RPO validation documented in DR Test Report

---

## 12. Infrastructure Cost Allocation (January 2026)

| Service | Monthly Cost | YoY Change |
|---------|-------------|-----------|
| EKS Compute (EC2) | $41,200 | +18% |
| RDS PostgreSQL | $12,800 | +22% |
| ElastiCache Redis | $6,400 | +15% |
| Elasticsearch (OpenSearch) | $18,600 | +31% |
| Kafka (MSK) | $5,200 | +8% |
| S3 Storage + Transfer | $9,700 | +44% |
| CloudFront | $3,100 | +12% |
| AWS WAF + Shield | $2,400 | +0% |
| Misc (Route53, Secrets, etc.) | $1,800 | +5% |
| **Total** | **$101,200** | **+22%** |

Cost optimization initiatives active: Savings Plans (40% coverage), Spot instances for batch workloads, S3 Intelligent-Tiering for documents older than 90 days.

---

## 13. Appendix: Service Dependency Map

```
Auth Service ←── All Services (JWT validation)
Document Service → S3, SQS, Audit, Kafka
Search Service → Elasticsearch, Redis, Auth
Notification Service → PostgreSQL, Redis, SendGrid
Analytics Service → ClickHouse, PostgreSQL, Redis
User Management Service → PostgreSQL, Auth, Audit
Billing Service → PostgreSQL, Stripe, Chargebee, Audit
Integration Service → PostgreSQL, Redis, Kafka, Auth
Workflow Service → PostgreSQL, Redis, Celery, Kafka
Audit Service → PostgreSQL, S3
AI Service → Elasticsearch, Redis, OpenAI, Anthropic
Admin Service → PostgreSQL, Auth, LaunchDarkly
```

---

*Document maintained by the NovaTech Solutions Architecture Team. For questions or corrections, contact #eng-architecture on Slack or open an issue in the architecture-docs GitHub repository.*
