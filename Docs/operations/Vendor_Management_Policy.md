# NovaTech Solutions — Vendor Management Policy
**Document Version:** 2.0
**Owner:** Jennifer Walsh, VP of Operations
**Co-Owner:** Tom Bradley, CISO
**Approved By:** David Huang, CEO | Carlos Ramirez, CFO
**Effective Date:** February 1, 2026
**Review Cycle:** Annual
**Classification:** Internal

---

## 1. Purpose and Scope

This Vendor Management Policy establishes NovaTech Solutions's standards for selecting, onboarding, managing, reviewing, and offboarding third-party vendors. Proper vendor management protects NovaTech, its customers, and its data by ensuring that all vendors who access NovaTech systems, handle customer data, or provide critical services meet defined security, reliability, and contractual standards.

**Scope:** This policy applies to all NovaTech Solutions employees, contractors, and departments that procure or manage third-party products, software, or services. It applies globally.

**Key Definitions:**
- **Vendor:** Any external organization that provides products, services, or technology to NovaTech Solutions under a commercial agreement.
- **Critical Vendor:** A vendor whose failure or unavailability would materially impair NovaTech's ability to deliver its product to customers.
- **Important Vendor:** A vendor whose failure would cause significant internal disruption but would not immediately impact customers.
- **Standard Vendor:** All other vendors.

---

## 2. Vendor Classification Tiers

### Tier 1 — Critical Vendor
**Criteria (any of the following):**
- Processes, stores, or has access to customer data
- Is essential to the uptime or availability of the NovaTech customer-facing platform
- Annual spend >$200,000
- No adequate substitution can be deployed within 72 hours

**Current Critical Vendors (as of Q1 2026):**

| Vendor | Category | Annual Spend | Data Access | Owner |
|---|---|---|---|---|
| Amazon Web Services (AWS) | Cloud Infrastructure | $1,840,000 | Yes (hosting) | Marcus Webb |
| Okta | Identity and Access Management | $94,000 | Yes (employee identity) | Tom Bradley |
| Pinecone | Vector Database | $312,000 | Yes (search index) | Marcus Webb |
| Anthropic | LLM API | $228,000 | Yes (inference only) | Marcus Webb |
| Stripe | Payment Processing | $84,000 | Yes (payment data) | Carlos Ramirez |
| Cloudflare | CDN and DDoS Protection | $96,000 | Yes (traffic) | Tom Bradley |
| PagerDuty | Incident Management | $24,000 | Yes (alert routing) | Tom Bradley |

**Requirements for Critical Vendors:**
- Annual security questionnaire (aligned to SIG Lite)
- Current SOC 2 Type II report (or equivalent: ISO 27001, FedRAMP) reviewed annually
- Signed Data Processing Agreement (DPA) if processing personal data
- Business Continuity Plan (BCP) documentation reviewed annually
- Vendor performance scorecard reviewed quarterly
- Executive sponsor assigned at NovaTech
- 30-day minimum contract termination notice (90-day preferred)
- Penetration test results reviewed annually (or upon request)

---

### Tier 2 — Important Vendor
**Criteria:**
- Internal systems access (non-customer data)
- Significant operational dependency
- Annual spend $25,000–$200,000

**Examples:** Salesforce (CRM), Google Workspace, Slack, GitHub, Snowflake, HubSpot, Rippling (HRIS), DocuSign, Zoom, Ramp (Expense)

**Requirements:**
- Security questionnaire (abbreviated — CAIQ lite or vendor-provided security overview)
- SOC 2 Type I or Type II reviewed (Type II preferred; Type I acceptable with compensating controls)
- Data processing agreement if handling personal data of employees
- Vendor performance reviewed annually
- 30-day contract notice period minimum

---

### Tier 3 — Standard Vendor
**Criteria:**
- No access to NovaTech systems, networks, or data
- Annual spend <$25,000
- Easily replaceable

**Examples:** Office supplies, catering, staffing agencies for non-technical roles, marketing agencies (non-data handling)

**Requirements:**
- Standard vendor agreement signed (NovaTech Standard Terms)
- Basic vendor information collected (insurance certificate if services performed on-site)
- Annual review not required unless spend crosses Tier 2 threshold

---

## 3. Vendor Due Diligence Requirements by Tier

### 3.1 Pre-Engagement Due Diligence

| Requirement | Tier 1 (Critical) | Tier 2 (Important) | Tier 3 (Standard) |
|---|---|---|---|
| Vendor information form | Required | Required | Required |
| Security questionnaire (SIG Lite) | Required | Abbreviated | Not required |
| SOC 2 / Compliance report review | Required (Type II) | Required (Type I+) | Not required |
| Data Processing Agreement | Required if data access | Required if data access | Not required |
| Business continuity documentation | Required | Optional | Not required |
| Reference check (2+ customers) | Required | Recommended | Not required |
| Financial stability check (D&B or equivalent) | Required | Recommended | Not required |
| Legal review of contract | Required | Required (template OK) | Standard PO acceptable |
| CFO approval | Required (>$200K) | Required (>$50K) | Not required |

### 3.2 Security Questionnaire Process

**Tier 1 — Full SIG Lite Questionnaire:**
1. Vendor receives NovaTech's SIG Lite questionnaire via Venminder platform (venminder.com — NovaTech's vendor risk management tool)
2. Vendor completes questionnaire within 15 business days
3. Tom Bradley's security team reviews responses and scores (1–5 per domain)
4. Any domain scoring ≤ 2 requires a remediation plan before engagement
5. Results stored in Venminder and linked to vendor record in Salesforce

**Tier 2 — Abbreviated Review:**
1. Vendor provides current SOC 2 report (or equivalent) + 1-page security overview
2. IT reviews for material gaps (data encryption, access controls, incident response)
3. If material gaps: escalate to Tom Bradley for Tier 1 process

---

## 4. Contractual Minimum Requirements

All vendor contracts (regardless of tier) must include:

**Required for ALL Vendors:**
- Clear description of services and deliverables
- Payment terms (NovaTech standard: Net 30)
- Intellectual property ownership (NovaTech owns all work product created for NovaTech)
- Confidentiality obligations (NDA or equivalent)
- Termination provisions (cause and convenience)

**Required for Tier 1 and 2 Vendors:**
- Data security requirements (encryption, access controls)
- Audit rights (NovaTech right to audit vendor security practices annually)
- Incident notification requirement: notify NovaTech within 24 hours of suspected breach
- SLA and remedy provisions (uptime SLA minimum for Tier 1: 99.9%; penalty: service credits)
- Insurance requirements (General liability ≥$1M; Cyber liability ≥$2M for Tier 1 data processors)
- Limitation of liability (mutual)

**Required for Tier 1 Vendors handling customer data:**
- Data Processing Agreement (GDPR Article 28 compliant)
- Sub-processor list and notification of changes (30-day advance notice)
- Data deletion/return upon contract termination (within 30 days)
- Data residency specification (US, EU, or as required)

---

## 5. Vendor Performance Scorecards

### 5.1 Quarterly Scorecard — Tier 1 (Critical) Vendors

Tier 1 vendors are reviewed quarterly using a standardized scorecard. Results are shared with the vendor's account manager and tracked in Venminder.

**Scorecard Categories:**

| Category | Weight | How Measured |
|---|---|---|
| Service Availability / Uptime | 30% | Actual uptime vs. SLA; incident count |
| Security Posture | 25% | Questionnaire delta; incident response; compliance cert status |
| Support Responsiveness | 20% | Average ticket response time; escalation rate |
| Contract Compliance | 15% | SLA penalties claimed; compliance certifications current |
| Innovation / Roadmap | 10% | New features relevant to NovaTech; roadmap alignment |

**Score Thresholds:**
- 85–100: Satisfactory
- 70–84: Acceptable — improvement plan requested
- 55–69: At Risk — executive escalation; 60-day remediation window
- <55: Unsatisfactory — begin vendor replacement process

### 5.2 Annual Review — Tier 2 Vendors
Annual review covers: renewal decision, spend review, security document refresh, and assessment of continued need.

---

## 6. Vendor Risk Register

Top vendor risks (reviewed quarterly by Operations and Security):

| Risk | Affected Vendor(s) | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| AWS regional outage | AWS | Medium | Critical | Multi-region failover (us-east-1 warm standby) |
| Pinecone price increase >40% | Pinecone | Low | High | Evaluate pgvector self-hosted as alternative |
| Anthropic API rate limits during peak | Anthropic | Medium | Medium | Request capacity reservation; implement queue |
| Okta breach / SSO outage | Okta | Low | Critical | Backup authentication (emergency access procedure) |
| Stripe PCI non-compliance | Stripe | Very Low | Critical | Annual PCI review; Stripe is PCI DSS Level 1 |
| HubSpot data portability | HubSpot | Low | Medium | Annual export of contact database |
| Key vendor exits market | Any | Very Low | Variable | Annual vendor financial stability check |

---

## 7. Single-Source Dependency Mitigation

NovaTech actively tracks single-source dependencies (critical functions performed by only one vendor with no practical alternative). As of Q1 2026:

| Dependency | Current Vendor | Risk Level | Mitigation Status |
|---|---|---|---|
| Cloud hosting | AWS only | HIGH | Evaluating Azure as secondary for DR (2027 roadmap) |
| Vector search | Pinecone only | MEDIUM | pgvector proof-of-concept planned Q3 2026 |
| LLM inference | Anthropic only | MEDIUM | Evaluating OpenAI + Cohere as alternatives; target Q3 2026 |
| Identity / SSO | Okta only | HIGH | Emergency access procedure documented; backup MFA implemented |
| Payment processing | Stripe only | MEDIUM | Evaluated Braintree in 2024; Stripe too embedded to replace in near-term |

---

## 8. Vendor Onboarding Procedure

**Target timeline: 5 business days for Tier 2 and 3; up to 21 business days for Tier 1**

**Step 1 — Request (Day 1)**
- Requestor submits New Vendor Request form (Notion > Operations > Vendor Requests)
- Requestor specifies: vendor name, service description, estimated annual spend, data access level, business justification
- Form automatically routes to Department Head for approval, then Procurement (Cassandra Baines)

**Step 2 — Classification (Day 2)**
- Procurement classifies vendor as Tier 1, 2, or 3
- If Tier 1: Engages Tom Bradley (Security) and Amanda Hartley (Legal)

**Step 3 — Due Diligence (Days 3–15)**
- Security questionnaire sent to vendor
- Legal review of draft contract
- References checked (Tier 1 only)

**Step 4 — Approval (Day 15–18)**
- Tier 1 (>$200K): CFO + CEO approval required
- Tier 1 (<$200K): VP of Operations + CISO approval
- Tier 2 (>$50K): CFO approval
- Tier 2 (<$50K): VP of Operations approval
- Tier 3: Department Head approval

**Step 5 — Contract Execution (Day 18–21)**
- Contract executed via DocuSign
- Vendor record created in Venminder and Salesforce (Vendors object)
- Vendor added to Preferred Vendor List if applicable

**Step 6 — System Access Provisioned (After Contract)**
- IT provisions access per approved scope
- Access logged in IT asset management system (Asset Panda)

---

## 9. Vendor Offboarding / Transition

When a vendor relationship is terminated:

**30 days before termination:**
- Identify replacement vendor or internal solution
- Begin data migration (if applicable)
- Notify vendor of termination in writing (per contract terms)

**At termination date:**
- All NovaTech data returned or deleted per contract (vendor provides written confirmation)
- All access credentials revoked (IT checklist: Notion > IT > Vendor Offboarding)
- All NovaTech-issued equipment returned
- Final invoice reviewed and approved; open disputes escalated to Legal

**Post-termination:**
- Vendor removed from Preferred Vendor List
- Venminder record updated to "Terminated"
- Deletion certificate filed (for data-handling vendors)

---

## 10. Vendor Spend Thresholds Requiring Procurement Involvement

| Spend Level | Approval Required |
|---|---|
| <$5,000 (one-time) | Department Head approval; P-card acceptable |
| $5,000–$25,000 | Department Head + Procurement (Cassandra Baines) |
| $25,001–$100,000 | VP of Operations + Procurement |
| $100,001–$500,000 | CFO + Procurement |
| >$500,000 | CEO + CFO + Board notification |
| Any Tier 1 vendor | Always requires Procurement and Security involvement |

---

## 11. Preferred Vendor List

The Preferred Vendor List includes vendors who have completed full due diligence and are approved for use across NovaTech departments. Employees should use preferred vendors when available; using non-preferred vendors requires New Vendor Request.

**Selected Preferred Vendors by Category:**

| Category | Preferred Vendor(s) | Tier |
|---|---|---|
| Cloud Infrastructure | Amazon Web Services | 1 |
| Identity & Access | Okta | 1 |
| Vector Database | Pinecone | 1 |
| LLM / AI | Anthropic | 1 |
| CRM | Salesforce | 2 |
| HR Information System | Rippling | 2 |
| Contract Management | DocuSign | 2 |
| Email / Productivity | Google Workspace | 2 |
| Communication | Slack | 2 |
| Finance / Expense | Ramp | 2 |
| Payroll | Rippling Payroll | 2 |
| Legal Services | Fenwick & West (primary) | 2 |
| Insurance Broker | Newfront Insurance | 2 |
| Marketing Automation | HubSpot | 2 |
| PR Agency | Vantage PR | 2 |
| SEO Agency | Clearwater Digital | 3 |
| Office Supplies | Amazon Business | 3 |
| Travel | Navan (TripActions) | 3 |
| Background Checks | Checkr | 3 |

---

*Policy Owner: Jennifer Walsh, VP of Operations | jennifer.walsh@novatech.io*
*Security Co-Owner: Tom Bradley, CISO*
*Approved: February 1, 2026*
*Next Review: February 2027*
