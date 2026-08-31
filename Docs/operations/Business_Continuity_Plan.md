# NovaTech Solutions — Business Continuity Plan (BCP)
**Document Version:** 3.1
**Owner:** Tom Bradley, CISO & VP of Infrastructure
**Co-Owner:** Jennifer Walsh, VP of Operations
**Approved By:** David Huang, CEO
**Approval Date:** January 20, 2026
**Last BCP Test:** December 10–11, 2025 (Tabletop Exercise — Results: See Section 9)
**Next Scheduled Test:** June 2026 (Functional Drill — Data Center Failover)
**Classification:** Confidential — Internal Use Only

---

## 1. Purpose and Scope

This Business Continuity Plan defines NovaTech Solutions's approach to maintaining critical business operations in the event of a significant disruption. It establishes recovery objectives, assigns responsibility for business continuity response, and provides runbooks for the most likely disruption scenarios.

This BCP covers all NovaTech Solutions operations including:
- Customer-facing SaaS platform (novatech.io and api.novatech.io)
- Internal corporate systems (email, Slack, HRIS, ERP)
- San Francisco headquarters (535 Mission Street, Suite 1400)
- Remote employee operations (globally distributed workforce)

This BCP is reviewed annually and tested at least twice per year (one tabletop exercise, one functional drill).

---

## 2. Risk Scenarios

### Scenario 1: Data Center / Cloud Region Outage
**Description:** Primary AWS region (us-west-2, Oregon) becomes unavailable due to AWS infrastructure failure, natural disaster, or network connectivity loss.
**Likelihood (Annual):** Medium (3/5)
**Impact:** High (4/5)
**Risk Score:** 12/25
**Historical Precedent:** AWS us-east-1 partial outage, December 2021; AWS us-west-2 degradation, November 2023.

### Scenario 2: Key Person Dependency
**Description:** Critical technical or leadership personnel become unavailable for an extended period (illness, accident, sudden departure) without adequate knowledge transfer.
**Likelihood:** Medium (3/5)
**Impact:** Medium (3/5)
**Risk Score:** 9/25
**Most Critical Roles:** CTO (Marcus Webb), CISO (Tom Bradley), VP Engineering (Jennifer Yao)

### Scenario 3: Cyber Attack / Ransomware
**Description:** NovaTech systems are compromised by ransomware, data exfiltration attack, or destructive malware. Attacker achieves persistent access to production environment.
**Likelihood:** Medium-Low (2/5)
**Impact:** Very High (5/5)
**Risk Score:** 10/25
**Mitigation in Place:** Endpoint detection (CrowdStrike), SIEM (Splunk), phishing training (KnowBe4), SOC 2 Type II controls.

### Scenario 4: Pandemic / Mass Workforce Unavailability
**Description:** A significant portion of the NovaTech workforce becomes unable to work (illness, government-mandated closure, public health event).
**Likelihood:** Low (1/5)
**Impact:** High (4/5)
**Risk Score:** 4/25
**Note:** NovaTech is well-positioned for this scenario given fully remote-capable infrastructure established during COVID-19.

### Scenario 5: Major Customer Data Breach
**Description:** Customer data hosted on NovaTech's platform is accessed by an unauthorized party. Potential regulatory and reputational impact.
**Likelihood:** Low (2/5)
**Impact:** Very High (5/5)
**Risk Score:** 10/25
**Mitigation:** SOC 2 Type II, encryption at rest and in transit, zero-trust network access, quarterly penetration testing.

### Scenario 6: Critical Vendor Failure
**Description:** A critical third-party vendor (AWS, Pinecone, Anthropic, Stripe, Okta) experiences an outage or discontinues service.
**Likelihood:** Medium (3/5) for minor outage; Low (1/5) for discontinuation
**Impact:** Medium-High (4/5)
**Risk Score:** 8/25 (outage); 4/25 (discontinuation)

---

## 3. Recovery Objectives by System

### 3.1 Recovery Time Objectives (RTO)

RTO defines the maximum acceptable time from disruption onset to full restoration of the system.

| System | Tier | RTO | Owner |
|---|---|---|---|
| Authentication / SSO (Okta) | P0 | 1 hour | Tom Bradley |
| Core Product (Search + Knowledge Platform) | P0 | 4 hours | Marcus Webb |
| API Gateway and Webhooks | P0 | 4 hours | Marcus Webb |
| Customer-Facing Web Application | P0 | 4 hours | Marcus Webb |
| Corporate Email (Google Workspace) | P1 | 2 hours | Tom Bradley |
| Slack (Internal Communications) | P1 | 2 hours | Tom Bradley |
| CRM (Salesforce) | P1 | 8 hours | Sophia Lee |
| Analytics / Data Warehouse (Snowflake) | P2 | 24 hours | Jennifer Yao |
| Marketing Automation (HubSpot) | P2 | 24 hours | Rachel Torres |
| HRIS (Rippling) | P2 | 48 hours | Jennifer Walsh |
| Finance / ERP (QuickBooks + Ramp) | P2 | 48 hours | Carlos Ramirez |
| Internal IT (device management, MDM) | P3 | 72 hours | Tom Bradley |

### 3.2 Recovery Point Objectives (RPO)

RPO defines the maximum acceptable data loss measured in time.

| System | RPO | Backup Frequency | Backup Location |
|---|---|---|---|
| Core Product Database (PostgreSQL on RDS) | 1 hour | Continuous replication | AWS us-east-1 (secondary region) |
| Customer Search Index (Pinecone) | 4 hours | Hourly snapshot | AWS S3 cross-region replication |
| Vector Embeddings Store | 4 hours | Hourly backup | AWS S3 (us-east-1) |
| Application Configuration (Terraform State) | 1 hour | Git + S3 versioning | Multiple locations |
| Salesforce CRM Data | 24 hours | Daily Salesforce backup | Salesforce + OwnBackup |
| Corporate Email (Google Workspace) | 24 hours | Google Vault (continuous) | Google (managed) |
| Financial Records (QuickBooks) | 24 hours | Daily automated backup | AWS S3 |

---

## 4. Backup Procedures

### 4.1 Database Backups (Production PostgreSQL)
- **Method:** AWS RDS automated backups + continuous transaction log shipping to us-east-1
- **Frequency:** Automated snapshots every 4 hours; transaction logs continuous (1-hour RPO achievable)
- **Retention:** 35 days for automated snapshots; 7 years for year-end snapshots (compliance)
- **Verification:** Weekly automated restoration test to isolated test environment (results logged in Confluence > Engineering > Backup Verification Log)
- **Owner:** Platform Engineering team; on-call rotation (PagerDuty)

### 4.2 Application Code and Configuration
- **Method:** GitHub (all code); Terraform state in S3 with versioning; Docker images in AWS ECR
- **Retention:** All code history retained indefinitely; Terraform state: 90-day version history
- **Owner:** Engineering Operations (Jennifer Yao)

### 4.3 Customer-Uploaded Documents (Knowledge Source Content)
- Customer documents are indexed but not stored by NovaTech (per privacy architecture); the index is the backup requirement.
- Search index backed up hourly to S3; see Vector Embeddings row above.

---

## 5. Failover Runbook — Scenario 1: AWS us-west-2 Outage

**Owner:** Marcus Webb (CTO) or designated on-call Engineering Lead
**Decision Authority:** CTO or CISO may invoke regional failover

**Step 1 — Detection (0–15 minutes)**
- PagerDuty alert triggers on health check failures across ≥3 production services
- On-call engineer assesses AWS Service Health Dashboard (status.aws.amazon.com)
- If AWS confirms regional issue OR if health checks fail for >10 minutes: escalate to Incident Commander (default: CTO)
- Incident Commander calls for war room in #incidents-sev1 Slack channel

**Step 2 — Decision to Failover (15–30 minutes)**
- Incident Commander assesses: Is outage localized (recoverable) or regional (requires failover)?
- If regional: Invoke failover. Inform VP Engineering, CISO, and CEO.
- Failover decision requires Incident Commander + one of: CTO, CISO, or CEO.

**Step 3 — Failover Execution (30–120 minutes)**
- Engineering team executes Terraform failover playbook (stored in GitHub: /infrastructure/runbooks/regional-failover.md)
- Route 53 DNS updated: novatech.io and api.novatech.io switched to us-east-1 load balancers (TTL: 60 seconds → expected propagation: 5 minutes)
- Database: Promote RDS read replica in us-east-1 to primary
- Search index: Redirect API calls to us-east-1 Pinecone environment (warm standby)
- Auth: Okta is globally distributed (no action required)
- Verify: Health check suite run against us-east-1 endpoints; all green before declaring service restored

**Step 4 — Customer Communication (30–60 minutes from decision to failover)**
- Status page (status.novatech.io) updated within 30 minutes of confirmed incident
- Customer Success notifies named accounts (Tier 1: ACME Corp, GlobalTech Inc, Meridian Enterprises, Pinnacle Systems, SkyBridge Ltd) via email + direct CSM call
- Mass customer email sent if outage exceeds 30 minutes
- Template: See Section 10, Customer Communication Templates

**Step 5 — Return to Primary Region**
- Planned maintenance window (off-hours, weekend preferred)
- Full data sync from us-east-1 back to us-west-2 before cutover
- Failback requires CTO + 2 Engineering leads sign-off
- Post-incident review within 5 business days

---

## 6. Communication Tree

### Incident Notification Order

**Level 1 — Immediate (within 15 minutes of confirmed P0 incident):**
- Tom Bradley, CISO (Primary: 415-555-0192; Backup: Signal)
- Marcus Webb, CTO (Primary: 415-555-0171; Backup: Signal)

**Level 2 — Within 30 minutes:**
- David Huang, CEO (Primary: 415-555-0100)
- Jennifer Yao, VP Engineering (Primary: 415-555-0204)
- Jennifer Walsh, VP Operations (Primary: 415-555-0218)

**Level 3 — Within 1 hour (if customer-impacting):**
- Janet Okonkwo, VP Customer Success (Primary: 415-555-0237)
- Sophia Lee, VP Sales (Primary: 415-555-0249)
- Rachel Torres, VP Marketing (Primary: 415-555-0261) — for communications

**Level 4 — Board Notification (if incident duration >4 hours OR customer data breach):**
- Board Chair: Linda Chen (linda.chen@novatechboard.io)
- Board notification via CEO (David Huang)

---

## 7. Crisis Team Roster

| Role | Primary | Backup | Contact |
|---|---|---|---|
| Incident Commander | Tom Bradley (CISO) | Marcus Webb (CTO) | 415-555-0192 |
| Technical Lead | Marcus Webb (CTO) | Jennifer Yao (VP Eng) | 415-555-0171 |
| Communications Lead | Rachel Torres (VP Mktg) | Jennifer Walsh (VP Ops) | 415-555-0261 |
| Customer Lead | Janet Okonkwo (VP CS) | CS Manager on rotation | 415-555-0237 |
| Legal Lead | Amanda Hartley (General Counsel) | External: Fenwick & West | 415-555-0188 |
| Executive Sponsor | David Huang (CEO) | Carlos Ramirez (CFO) | 415-555-0100 |
| Finance Lead | Carlos Ramirez (CFO) | Controller: Maya Singh | 415-555-0155 |

---

## 8. Annual BCP Test Schedule

| Test | Format | Date | Owner | Status |
|---|---|---|---|---|
| Q1 Tabletop Exercise | Ransomware scenario | December 10–11, 2025 | Tom Bradley | Completed |
| Q3 Functional Drill | Regional failover | June 2026 | Marcus Webb | Planned |
| Data Backup Verification | Automated + manual review | Monthly | Platform Engineering | Ongoing |
| Communication Tree Drill | Call tree verification | March 2026 | Jennifer Walsh | Planned |
| BCP Document Review | Annual | January 2026 | Tom Bradley | Completed |

### December 2025 Tabletop Exercise — Results Summary
- **Scenario tested:** Ransomware attack affecting production environment
- **Duration:** 4 hours
- **Participants:** 12 (all crisis team members)
- **Key findings:**
  1. Communication tree worked as designed — all Level 1/2 contacts reached within 25 minutes.
  2. Identified gap: Legal (Amanda Hartley) was not included in the breach notification decision tree — **RESOLVED: Added to Level 3 in updated plan (this document).**
  3. Identified gap: Customer communication template for data breach was missing — **RESOLVED: Template added to Section 10.**
  4. Identified gap: No designated backup for CTO if unavailable — **RESOLVED: Jennifer Yao designated as backup Technical Lead.**
- **Overall assessment:** BCP is functional. Two improvements implemented for Version 3.1.

---

## 9. Insurance Coverage Summary

| Policy Type | Carrier | Policy Number | Coverage Amount | Renewal Date |
|---|---|---|---|---|
| Cyber Liability (First-Party) | AXA XL | CYB-2024-NT-8821 | $10M per occurrence | March 31, 2026 |
| Cyber Liability (Third-Party) | AXA XL | CYB-2024-NT-8821 | $10M per occurrence | March 31, 2026 |
| Business Interruption | Chubb | BI-NT-4421-2025 | $5M (90-day max) | June 1, 2026 |
| Directors & Officers (D&O) | Travelers | DO-NT-9921 | $5M | September 1, 2026 |
| E&O (Technology) | Travelers | EO-NT-2241 | $5M per claim | September 1, 2026 |
| General Liability | Hartford | GL-NT-3312 | $2M per occurrence | April 1, 2026 |

**Cyber Insurance Contact:** Sarah Blackwood, AXA XL (sarah.blackwood@axaxl.com; 212-555-0481)
**Insurance Broker:** Newfront Insurance (SF) — Account Manager: Derek Hartman (derek.hartman@newfront.com)

---

## 10. Vendor Continuity Assessment Criteria

All Critical and Important vendors must undergo an annual Business Continuity Assessment (BCA). Assessment criteria:

| Criterion | Weight | Assessment Method |
|---|---|---|
| Uptime SLA (≥99.9% for Critical) | 25% | Contract review + SLA report |
| Geographic redundancy | 20% | Vendor documentation |
| Recovery time objective ≤ NovaTech's RTO | 20% | Vendor BCP document |
| SOC 2 Type II or equivalent | 15% | Audit report review |
| Data backup frequency and retention | 10% | Security questionnaire |
| Notification SLA for incidents | 10% | Contract review |

**Critical Vendors (undergo annual BCA):** AWS, Okta, Pinecone, Anthropic, Stripe, Cloudflare, PagerDuty
**Important Vendors (undergo annual BCA — simplified):** Salesforce, Google Workspace, Slack, GitHub, Snowflake, HubSpot

---

*Document Owner: Tom Bradley, CISO & VP Infrastructure | tom.bradley@novatech.io*
*Approved By: David Huang, CEO*
*Version 3.1 — Effective January 20, 2026*
*Next Review: January 2027 (or sooner if material changes occur)*
