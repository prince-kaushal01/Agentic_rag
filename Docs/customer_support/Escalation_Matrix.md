# NovaTech Solutions — Escalation Matrix

**Document Version:** 2.1  
**Last Updated:** February 1, 2026  
**Authors:** Jennifer Osei (Head of Customer Support), Priya Nair (VP Engineering), Sarah Chen (VP Sales)  
**Classification:** Internal — Customer Support + Engineering + Sales  
**Review Cycle:** Quarterly

---

## 1. Overview

This document defines escalation triggers, paths, contacts, and communication procedures for customer issues that exceed standard support resolution capacity. Escalation is not a failure — it is a deliberate, time-bound process to bring the right resources to the problem.

**Escalation Principles:**
1. Escalate early, not late. It's always better to involve more people sooner.
2. Escalate with context — never escalate a cold hand-off.
3. Escalation ownership stays with the original agent/CSM until the customer confirms resolution.
4. Every escalation requires a designated owner at each level.

---

## 2. Escalation Trigger Criteria

### 2.1 Automatic Escalation Triggers (No Judgment Required)

| Trigger | Immediate Action |
|---------|----------------|
| Customer mentions "cancel," "churn," "terminate," or "legal" | Notify CSM + Head of Support within 15 minutes |
| VP or C-Suite contact from customer reaches out directly | Treat as P1; notify CSM + AE within 15 minutes |
| Customer reports suspected data breach or data loss | Security protocol: notify Head of Support + Security team within 5 minutes |
| P0 incident declared (platform down) | Incident response process; see Incident Response Playbook |
| CSAT score of 1 or 2 on a resolved ticket | Head of Support + CSM notified within 24 hours |
| Customer submits 3+ tickets within 7 days | CSM receives automated health alert; escalation review |
| SLA breach confirmed (response or resolution overdue) | Tier 2 notified immediately; SLA breach report filed |
| Ticket open > 5 business days without resolution | Tier 2 supervisor notified |

### 2.2 Judgment-Based Escalation Triggers

The following situations require agent judgment. When in doubt, escalate:

- Customer is expressing strong frustration or emotional distress
- Issue has wide impact (multiple users or features affected) but not clearly P0/P1
- You don't understand the technical issue well enough to respond accurately
- You are being asked to make a commitment you don't have authority to make
- The customer has a complex billing dispute requiring contractual review
- Customer requests to speak with a manager or executive

---

## 3. Escalation Paths by Issue Type

### 3.1 Technical Escalation Path

```
Tier 1 Agent
     │ (unresolved in 30 min, or Tier 2 trigger criteria met)
     ▼
Tier 2 Senior Support Engineer (Grace Nwosu or Kofi Asante)
     │ (unresolved in 4 hours, or requires code fix / data access)
     ▼
Engineering Team Lead (relevant team: Platform / Product / Data)
     │ (bug confirmed; Jira ticket created ENG-XXXX)
     ▼
Engineering Manager (Rachel Torres / Rajesh Kumar / Aisha Okonkwo)
     │ (P0/P1 or customer at risk)
     ▼
VP Engineering (Priya Nair) 
     │ (executive involvement required or > 24h unresolved P1)
     ▼
CTO (Jonathan Mercer) — [P0 only, or at customer CEO/board request]
```

### 3.2 Customer Satisfaction / Retention Escalation Path

```
Support Agent notices at-risk signals
     │
     ▼
Customer Success Manager (assigned CSM)
     │ (customer dissatisfied; health score Yellow or Red)
     ▼
Head of Customer Support (Jennifer Osei)
     │ (account at risk of churn; customer VP-level engagement)
     ▼
Account Executive (Sarah Chen or assigned AE)
     │ (renewal at risk; discount or contractual concessions needed)
     ▼
VP of Customer Success (Michelle Park)
     │ (> $100K ARR account at high churn risk; executive negotiation required)
     ▼
CEO (Michelle Watanabe) — [Strategic accounts > $200K ARR, at imminent churn risk]
```

### 3.3 Billing and Contractual Escalation Path

```
Tier 1 Agent (intake; gather info)
     │
     ▼
Finance Manager (Ana Reyes) — amounts $501–$10,000
     │
     ▼
VP Finance (Mark Henderson) — amounts > $10,000
     │ + notification to VP Customer Success + relevant AE
     ▼
Legal Team — contract dispute, chargeback > $5K, threatened legal action
     │
     ▼
CEO + General Counsel — lawsuit filed or regulatory inquiry
```

### 3.4 Legal and Regulatory Escalation Path

```
Any report of potential legal issue, regulatory breach, GDPR complaint
     │ (within 24 hours)
     ▼
Legal Team (legal@novatech.com — monitored 24/7 for urgent items)
     │
     ▼
General Counsel (Margaret Liu — margaret.liu@novatech.com)
     │ (if data breach confirmed or GDPR Article 33 notification required)
     ▼
CEO + Board notification (within 72 hours for confirmed data breach)
```

---

## 4. Escalation Contact Directory

### 4.1 Internal Escalation Contacts

| Role | Name | Email | Phone | Available |
|------|------|-------|-------|---------|
| Head of Customer Support | Jennifer Osei | jennifer.osei@novatech.com | +1-628-555-0218 | Business hours + P0 on-call |
| CSM — Strategic Accounts | David Rodriguez | david.rodriguez@novatech.com | +1-628-555-0247 | Business hours |
| CSM — Mid-Market | Sasha Ivanova | sasha.ivanova@novatech.com | +1-628-555-0251 | Business hours |
| VP Customer Success | Michelle Park | michelle.park@novatech.com | +1-628-555-0209 | Business hours + urgent |
| Account Executive | Sarah Chen | sarah.chen@novatech.com | +1-628-555-0234 | Business hours |
| VP Engineering | Priya Nair | priya.nair@novatech.com | +1-628-555-0178 | P0/P1 on-call |
| SRE Lead | Kevin Osei | kevin.osei@novatech.com | +1-628-555-0192 | On-call rotation |
| Finance Manager | Ana Reyes | ana.reyes@novatech.com | +1-628-555-0261 | Business hours |
| Legal Team | — | legal@novatech.com | — | Business hours + urgent |
| General Counsel | Margaret Liu | margaret.liu@novatech.com | +1-628-555-0275 | Business hours + urgent |
| CEO | Michelle Watanabe | michelle.watanabe@novatech.com | +1-628-555-0200 | Executive level only |
| CTO | Jonathan Mercer | jonathan.mercer@novatech.com | +1-628-555-0201 | P0 incidents only |

### 4.2 Key Account Contacts (Customer Side)

| Account | Executive Contact | Email |
|---------|-----------------|-------|
| ACME Corp | James Harrington (VP Technology) | james.harrington@acme-corp.com |
| ACME Corp | Robert Chen (Director Operations) | robert.chen@acme-corp.com |
| GlobalTech Inc | Amanda Foster (IT Director) | amanda.foster@globaltech.com |
| Meridian Enterprises | Sandra Kim (VP Technology) | sandra.kim@meridian-ent.com |
| Pinnacle Systems | Kevin Walsh (CTO) | kevin.walsh@pinnacle-systems.com |
| SkyBridge Ltd | Oliver Nash (CEO) | oliver.nash@skybridge.co.uk |

---

## 5. Response Time SLAs at Each Escalation Level

| Escalation Level | Response Time | Update Frequency |
|----------------|--------------|----------------|
| Tier 2 (first escalation) | Within 2 hours | Every 4 hours |
| Engineering Lead | Within 4 hours | Every 4 hours |
| Engineering Manager | Within 2 hours of notification | Every 2 hours |
| VP Engineering | Within 1 hour | Every hour for P0/P1 |
| CSM | Within 2 hours | Daily during active escalation |
| VP Customer Success | Within 2 hours | Every 4 hours |
| Account Executive | Within 2 hours | Daily |
| Finance Manager | Within 1 business day | Per milestone |
| Legal | Within 4 hours (urgent) / 1 business day (standard) | Per milestone |

---

## 6. War Room Procedures (P0 / Executive Escalation)

### 6.1 When to Call a War Room

A War Room is declared when:
- A P0 incident has been ongoing for > 2 hours without resolution
- A major Enterprise customer is threatening to leave (churn risk > $100K ARR)
- A legal or security event requires multi-team coordination

### 6.2 War Room Structure

**Zoom Room:** Auto-created at `nt.tools/warroom` — always available, password: shared in #leadership Slack

| Role | Responsibility |
|------|---------------|
| **War Room Lead** | VP Engineering (technical) or VP Customer Success (business escalation) |
| **Technical Lead** | Engineering Manager or Staff Engineer for the affected service |
| **Customer Advocate** | CSM or Head of Customer Support |
| **Communications Lead** | Marketing or AE (for external communication) |
| **Scribe** | Support Agent — documents timeline and decisions in real time |

### 6.3 War Room Protocol

1. **First 10 minutes:** Everyone states their understanding of the problem
2. **Minutes 10–30:** Technical diagnosis; identify root cause or narrow to 2-3 hypotheses
3. **Minutes 30+:** Execute fix while Communications Lead prepares customer-facing message
4. **Every 30 minutes:** Check-in on status; update all parties

---

## 7. Escalation Notification Templates

### 7.1 Internal Escalation Notification (Slack)

```
@[name] — Escalation needed: [TKT-XXXX]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Customer: [Name] | Tier: [Enterprise/Pro/Standard]
Issue: [2-sentence description]
Priority: [P0/P1/P2] | Duration open: [X hours]
What we've tried: [bullet list]
What we need from you: [specific ask]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Customer contact: [name, email]
CSM: [name]
```

### 7.2 Executive Briefing Template (VP+ Level)

```
ESCALATION BRIEF — [Date Time]

Account: [Company Name] ([$X ARR] | [Tier] | [Renewal: date])
Issue: [2-3 sentence summary]
Customer Contact: [Name, Title]
Business Risk: [Low / Medium / High / Critical — explain why]
Current Status: [Investigating / Identified / Fix in progress]
ETA to Resolution: [date/time or Unknown]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Actions Taken:
• [action 1]
• [action 2]
Next Steps:
• [action 1 — owner — deadline]
• [action 2 — owner — deadline]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Escalation owner: [Name]
CSM: [Name]
AE: [Name]
```

---

## 8. De-Escalation Criteria

An escalation is considered resolved and can be de-escalated when:

| Criteria | Notes |
|----------|-------|
| Technical issue is resolved and verified by customer | Verified = customer confirms in ticket, not just our monitoring |
| Customer satisfaction has been restored (CSAT ≥ 4.0 on resolution survey) | Or CSM has spoken with customer and confirmed satisfaction |
| Renewal is no longer at immediate risk | AE has received positive signal from customer |
| SLA credit/refund has been processed and communicated | Not just approved internally |
| Root cause analysis communicated to customer (for P0/P1) | Within 5 business days of resolution |
| Follow-up action items are documented and scheduled | In Jira/Zendesk with owners and dates |

**De-escalation action:** Update the Zendesk ticket status; notify all escalation parties via Slack; close the escalation in the Escalation Tracker (Google Sheet: `CS > Escalations > Active`).

---

## 9. External Communication Approval

Before any written communication goes to a customer that:
- Acknowledges a legal obligation (SLA credit, refund commitment)
- Discusses a data breach or security incident
- Promises a feature or roadmap commitment
- Contains any admission of fault or liability

The communication must be reviewed and approved by:
- Legal team (legal@novatech.com) — for anything with legal implications
- VP Customer Success — for strategic accounts
- Head of Customer Support — for standard accounts

**Approval turnaround:** 4 hours for urgent escalations, 1 business day for standard.

---

*This escalation matrix is reviewed quarterly. For urgent escalation guidance during an active incident, contact Jennifer Osei (+1-628-555-0218) or the on-call engineering manager via PagerDuty.*
