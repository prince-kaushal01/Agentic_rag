# ACME Corp — Account Summary

**Document Type:** Strategic Account Profile  
**Last Updated:** March 19, 2026  
**Maintained By:** David Rodriguez (Customer Success Manager)  
**Account Executive:** Sarah Chen  
**Classification:** Internal — Customer Success + Sales + Engineering

---

## 1. Account Overview

| Field | Value |
|-------|-------|
| **Company Name** | ACME Corp |
| **Industry** | Manufacturing / Industrial Technology |
| **Headquarters** | Chicago, IL |
| **Employees** | ~3,200 |
| **Customer Since** | January 15, 2025 |
| **Account Tier** | Enterprise |
| **Contract Value** | $240,000 / year (USD) |
| **Contract Term** | January 15, 2025 – January 14, 2027 |
| **Payment Status** | Current — paid through June 2026 |
| **Licensed Users** | 500 |
| **Active Users** | 487 / 500 (97.4% seat utilization) |
| **Documents Indexed** | 11,247,842 (as of March 2026) |
| **Storage Used** | 4.7 TB |

---

## 2. Key Contacts

### 2.1 Customer Contacts

| Name | Title | Email | Phone | Role |
|------|-------|-------|-------|------|
| **James Harrington** | VP of Technology | james.harrington@acme-corp.com | +1-415-555-0142 | Primary Technical Contact / Executive Sponsor |
| **Lisa Park** | IT Manager | lisa.park@acme-corp.com | +1-415-555-0187 | Day-to-Day Technical Contact / Admin |
| **Robert Chen** | Director of Operations | robert.chen@acme-corp.com | +1-415-555-0203 | Business Sponsor (signed original contract) |
| **Diane Wu** | IT Systems Analyst | diane.wu@acme-corp.com | — | Platform Admin / Integration Lead |

**Primary decision-maker for renewal:** Robert Chen (Director of Operations), in consultation with James Harrington (VP Technology)

### 2.2 NovaTech Account Team

| Name | Role | Email | Phone |
|------|------|-------|-------|
| **Sarah Chen** | Account Executive | sarah.chen@novatech.com | +1-628-555-0234 |
| **David Rodriguez** | Customer Success Manager | david.rodriguez@novatech.com | +1-628-555-0247 |
| **Maria Fontaine** | Solutions Engineer (pre-sales/renewal) | maria.fontaine@novatech.com | — |

---

## 3. Account Health

| Metric | Current | Previous (Dec 2025) | Trend |
|--------|---------|---------------------|-------|
| **Health Score** | Yellow | Green | Degrading ↓ |
| **NPS Score** | 42 | 58 | Degrading ↓ |
| **CSAT (last ticket)** | 3.2 / 5.0 | 4.7 / 5.0 | Degrading ↓ |
| **Open Support Tickets** | 3 (1 High, 2 Medium) | 0 | Degraded ↓ |
| **Feature Adoption %** | 71% | 78% | Slight decline |
| **Last Login (admin)** | 2 days ago | — | Active |

**Health Score degraded from Green to Yellow in March 2026** due to the search performance issue (see Section 5). Account is **at risk for renewal** if performance is not resolved by Q3 2026.

---

## 4. Contract Details

| Field | Value |
|-------|-------|
| **Contract Start** | January 15, 2025 |
| **Contract End** | January 14, 2027 |
| **Days to Renewal** | 301 days (as of March 19, 2026) |
| **Annual Contract Value** | $240,000 USD |
| **Monthly Run Rate** | $20,000 USD |
| **Payment Terms** | Annual, net 30 — invoiced in advance |
| **Last Invoice** | January 15, 2026 — $240,000 — Paid January 22, 2026 |
| **Next Invoice** | January 15, 2027 |
| **Billing Contact** | Lisa Park (lisa.park@acme-corp.com) |

**Contract Inclusions:**
- 500 user licenses (full platform access)
- 5 TB document storage
- Enterprise SLA (99.95% uptime)
- 24/7 P0 support, business hours P1–P3
- Quarterly Business Reviews (QBRs)
- Dedicated Customer Success Manager
- SSO (SAML 2.0) enabled
- Dedicated Elasticsearch node pool (provisioned February 2026 for performance)
- API rate limit: 5,000 requests/minute

**Expansion Opportunity:**
ACME has expressed interest in adding 100 more user licenses (+$48,000/year potential) and the AI Q&A add-on ($24,000/year potential) — contingent on search performance resolution.

---

## 5. Open Support Tickets

### 5.1 High Priority — ACTIVE ESCALATION

**TKT-4821 — Search Performance Degradation**
- **Priority:** High
- **Status:** Open — Engineering Investigating
- **Subject:** Search results taking 8–12 seconds on large document sets
- **Reported By:** James Harrington (VP Technology)
- **Created:** March 10, 2026
- **Last Updated:** March 18, 2026
- **Assigned To:** David Rodriguez (CSM) + Rajesh Kumar (Engineering Lead, Data Team)
- **Engineering Ticket:** ENG-2847
- **Description:** ACME users are experiencing search response times of 8–12 seconds when querying their document collection (11.2M documents). This significantly exceeds the contractual SLA target of < 2 seconds at p99. The issue is most severe during peak business hours (9 AM – 12 PM CT).
- **Customer Impact:** ACME's entire legal and compliance team (87 users) relies on document search for contract review workflows. Productivity severely impacted.
- **Engineering Root Cause:** Identified as Elasticsearch shard allocation inefficiency for large-document tenants. ACME's index spans 47 shards across shared data nodes, causing cross-shard query overhead. Fix: dedicated node pool + query optimization (ENG-2847 in Sprint 41/42).
- **Expected Resolution:** April 15, 2026 (per Engineering roadmap)
- **Escalation Status:** VP-level escalation — James Harrington escalated to VP level on March 18, 2026 via email to Sarah Chen (Account Executive)
- **Last Communication to Customer:** March 18, 2026 — Sarah Chen sent escalation response email with engineering timeline commitment

### 5.2 Medium Priority

**TKT-4756 — Document Upload Failing for Files > 50MB**
- **Priority:** Medium
- **Status:** Open — Engineering Investigating
- **Subject:** Document upload failing for files > 50MB (intermittent)
- **Reported By:** Lisa Park (IT Manager)
- **Created:** March 1, 2026
- **Last Updated:** March 14, 2026
- **Assigned To:** Wei Zhang (Engineering, Product Team)
- **Engineering Ticket:** ENG-2751
- **Description:** Document uploads for files between 50MB and 200MB fail intermittently (~15% failure rate). ACME's engineering and legal teams regularly upload large CAD files, contracts, and multi-chapter technical manuals in this size range.
- **Workaround Available:** Files can be split into smaller segments. Lisa Park confirmed this workaround is "painful but usable."
- **Expected Resolution:** April 8, 2026 (Sprint 42 release)

**TKT-4892 — Bulk Export of Search Analytics**
- **Priority:** Medium
- **Status:** Open — Awaiting Product Roadmap Decision
- **Subject:** Need bulk export of search analytics data
- **Reported By:** James Harrington (VP Technology)
- **Created:** March 15, 2026
- **Last Updated:** March 16, 2026
- **Category:** Feature Request
- **Description:** ACME wants to export their search analytics data in bulk (CSV/JSON) to feed into their internal BI tool (Tableau). Currently, analytics are only available through the dashboard UI. This is a strategic request tied to their internal data governance initiative.
- **PM Decision Pending:** Feature request under review for Q2/Q3 roadmap

---

## 6. Account History and Timeline

### 6.1 Key Milestones

| Date | Event |
|------|-------|
| November 2024 | Initial sales engagement; Sarah Chen introduced ACME to NovaTech |
| December 2024 | Proof of Concept (30-day trial) — 50 users, limited document set |
| January 10, 2025 | Contract signed by Robert Chen (Director of Operations) |
| January 15, 2025 | Platform provisioned; onboarding began |
| February 3, 2025 | Kickoff call with Lisa Park and Diane Wu; SSO configuration completed |
| March 1, 2025 | First 200 users onboarded; 1.2M documents migrated |
| April 15, 2025 | Full 487-user rollout complete |
| June 2025 | QBR 1 — NPS 68, health Green. Strong satisfaction. Discussed AI features. |
| September 2025 | QBR 2 — NPS 62, health Green. Requested bulk analytics export feature. |
| October 2025 | ACME added 87 additional users (legal team expansion) |
| December 2025 | QBR 3 — NPS 58, health Green. First mention of occasional slowness in search. |
| January 2026 | Document count crossed 10M — performance issues begin manifesting |
| March 1, 2026 | Lisa Park reports upload failures (TKT-4756) |
| March 5, 2026 | QBR 4 — James Harrington expresses frustration about search performance. NPS dropped to 42. Health moved to Yellow. |
| March 10, 2026 | James Harrington formally reports search degradation (TKT-4821) |
| March 18, 2026 | James Harrington escalates to VP level via email; requests engineering timeline |
| March 19, 2026 | Sarah Chen + Priya Nair (VP Engineering) send joint response to James Harrington |

### 6.2 Recent Communications Log

**March 19, 2026 — Joint Executive Response**
From: Sarah Chen (AE) + Priya Nair (VP Engineering)  
To: James Harrington (VP Technology, ACME)  
Subject: Re: Search Performance — Engineering Timeline  
Summary: Priya personally committed to the April 15, 2026 resolution date for search performance. Offered a dedicated weekly status call with Rajesh Kumar (Engineering Lead). Acknowledged the SLA impact and committed to providing SLA credit calculation once the issue is resolved.

**March 18, 2026 — Customer Escalation Email**
From: James Harrington (VP Technology, ACME)  
To: Sarah Chen (AE)  
CC: robert.chen@acme-corp.com, lisa.park@acme-corp.com  
Subject: Escalation — Unacceptable Search Performance  
Summary: "We have now been experiencing unacceptable search performance for over a week. Our legal team is unable to use the platform effectively. We are paying $240K/year for an Enterprise service and expect Enterprise-grade performance. We need an engineering timeline and a commitment on resolution. If this is not resolved by end of Q2, we will need to reconsider our renewal."

**March 15, 2026 — Feature Request Email**
From: James Harrington  
To: david.rodriguez@novatech.com  
Summary: Requested bulk search analytics export to connect with their Tableau environment.

**March 10, 2026 — Initial Performance Report**
From: James Harrington  
To: Support (support@novatech.com)  
Summary: Formally reported 8-12 second search times; created TKT-4821.

**March 5, 2026 — QBR 4 Notes**
Attendees: James Harrington, Lisa Park, Robert Chen (ACME); Sarah Chen, David Rodriguez (NovaTech)  
Key Points:
- NPS dropped from 58 to 42
- James: "Search is the core reason we bought NovaTech. If it's slow, everything else is irrelevant."
- Robert Chen: Supportive but noted "James handles technology decisions on renewals"
- Action items: Engineering to provide root cause analysis within 5 days; David to set up weekly status calls

---

## 7. Technical Configuration

| Setting | Value |
|---------|-------|
| SSO Provider | Azure AD (SAML 2.0) |
| SCIM Provisioning | Enabled (Azure AD → NovaTech) |
| Elasticsearch Tier | Dedicated node pool (provisioned February 2026) |
| API Rate Limit | 5,000 req/min (Enterprise) |
| Webhook Endpoints | 3 configured (document.created, document.deleted, user.created) |
| Integration: Slack | Enabled (notifications to #novatech-alerts channel) |
| Integration: SharePoint | Pending configuration (Diane Wu working on this) |
| Data Retention | 7 years (ACME legal requirement) |
| 2FA Required | Yes (enforced by ACME IT policy) |
| Custom Domain | novatech.acme-corp.com (white-label) |

---

## 8. Risk Assessment

**Overall Risk Level: MEDIUM-HIGH**

| Risk Factor | Assessment | Mitigation |
|------------|-----------|-----------|
| Search performance unresolved | HIGH — direct threat to renewal | ENG-2847 top engineering priority; April 15 target |
| VP-level frustration | HIGH — decision-maker engaged and frustrated | Executive-level response sent; weekly status calls |
| NPS dropped 16 points | MEDIUM | Proactive CSAT recovery plan in place |
| Competitive evaluation | MEDIUM — likely exploring alternatives | Sarah Chen to schedule retention call with Robert Chen |
| Upload performance issue | LOW-MEDIUM — workaround available | ENG-2751 targeted for April 8 release |

**Recommended Immediate Actions (March 2026):**
1. Rajesh Kumar (Engineering) to join weekly status call with James Harrington starting March 25, 2026
2. David Rodriguez to offer SLA credit proactively (calculate % of monthly fee)
3. Sarah Chen to schedule executive retention call with Robert Chen before end of March
4. PM to fast-track the search analytics export feature for Q2 roadmap to show ACME they are heard
5. Engineering to provide written April 15 commitment letter for search performance

**Renewal Probability (as of March 19, 2026):** 65% (down from 95% in December 2025)

---

## 9. Product Usage Summary

| Feature | Adoption | Usage Trend |
|---------|---------|------------|
| Document Upload | 98% of users | Heavy — 150K+ documents/month |
| Document Search | 94% of users | Heavy — 12K+ queries/day |
| AI Summarization | 8% of users | Beta access (12 power users) |
| Workflows | 0% | Not yet configured |
| Analytics Dashboard | Admin only (5 users) | Weekly |
| API Integration | 2 integrations active | Slack, SharePoint (pending) |
| Webhooks | 3 active endpoints | Daily activity |

---

*Last updated by David Rodriguez on March 19, 2026. Next update: March 26, 2026 (post weekly status call with James Harrington).*
