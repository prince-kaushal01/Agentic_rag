# NovaTech Solutions — Customer Support Playbook

**Document Version:** 2.4  
**Last Updated:** February 10, 2026  
**Authors:** Jennifer Osei (Head of Customer Support), David Rodriguez (CSM Lead)  
**Classification:** Internal — Customer Support  
**Review Cycle:** Quarterly

---

## 1. Overview and Philosophy

NovaTech Solutions Customer Support exists to ensure every customer — from a 10-seat startup to a 500-seat Enterprise account — gets fast, accurate, and empathetic help when they need it. We are not a ticket-processing factory; we are a trust-building team.

**Our Support Principles:**
1. **Respond fast, resolve faster.** Customers don't remember that we had a problem — they remember how quickly we fixed it.
2. **Communicate proactively.** If we know something is broken before the customer tells us, we tell them first.
3. **Own the outcome.** Support agents own the customer experience from ticket open to confirmed resolution. We do not "hand off and forget."
4. **Be honest about timelines.** Don't promise what engineering hasn't committed to.
5. **Escalate with context.** When escalating, provide full context so customers don't have to repeat themselves.

---

## 2. Team Structure

### 2.1 Support Tiers

| Tier | Name | Scope | Staffing |
|------|------|-------|---------|
| **Tier 1** | Customer Support Agents | First contact; FAQ resolution; ticket routing; basic troubleshooting | 8 agents |
| **Tier 2** | Senior Support Engineers | Complex technical issues; troubleshooting with tool access; product deep dives | 4 engineers |
| **Tier 3** | Engineering Escalations | Production bugs; performance issues; deep technical investigation | Engineering team (via internal escalation) |

### 2.2 Team Roster (Q1 2026)

**Head of Customer Support:** Jennifer Osei (jennifer.osei@novatech.com)

**Tier 1 Agents:**
- Maya Sullivan — EMEA customers, 9 AM – 5 PM GMT
- Carlos Mendez — US West, 8 AM – 4 PM PT
- Priya Chandrasekaran — US East, 9 AM – 5 PM ET
- Taichi Yamamoto — APAC customers, 9 AM – 5 PM JST
- Nicole Dubois — General queue, 10 AM – 6 PM PT
- Ahmad Hassan — General queue, 7 AM – 3 PM PT
- Lucy Thornton — Enterprise accounts Tier 1, 9 AM – 5 PM PT
- Daniel Park — Weekend/evening coverage, Thu–Mon 12 PM – 8 PM PT

**Tier 2 Senior Support Engineers:**
- Grace Nwosu — Technical lead; escalation owner
- James Petrov — Integrations and API specialist
- Kofi Asante — Infrastructure and performance specialist
- Yuki Tanaka — Search and AI features specialist

**Customer Success Managers (separate team, closely aligned):**
- David Rodriguez — ACME Corp, GlobalTech Inc, Meridian Enterprises
- Sasha Ivanova — Pinnacle Systems, SkyBridge Ltd, 8 other Mid-Market accounts
- Felipe Morales — SMB accounts (20+ accounts)

---

## 3. Support Hours

| Coverage | Hours | Supported Tiers |
|----------|-------|----------------|
| **P0 Coverage** | 24/7/365 | All tiers |
| **P1 Coverage** | 24/7/365 | Enterprise; P1 24h for Standard |
| **P2–P3 Business Hours** | Mon–Fri, 6 AM – 8 PM PT | All tiers |
| **Weekend Coverage** | Sat–Sun, 9 AM – 5 PM PT (P0/P1 only) | Enterprise and above |

**Holiday coverage:** Reduced staffing on US federal holidays. P0/P1 coverage maintained. P2/P3 response times extend by 1 business day.

---

## 4. Support Channels

| Channel | Available To | Use For | Response |
|---------|------------|---------|---------|
| **In-app chat** (Intercom) | All customers | Quick questions, P3/P4 | < 2 minutes during business hours |
| **Support email** (support@novatech.com) | All customers | Any issue; paper trail preferred | Per SLA tier |
| **Support portal** (support.novatech.io) | All customers | Ticket submission, knowledge base | Per SLA tier |
| **Phone** (Enterprise only) | Enterprise tier | P0/P1 urgent issues | < 5 minutes during business hours |
| **Zoom (scheduled)** | Professional + Enterprise | Complex troubleshooting sessions | Scheduled |
| **Dedicated Slack channel** | Enterprise (> $100K ARR) | Ongoing communication | Business hours, monitored |
| **Emergency pager** (internal) | Enterprise, escalated by CSM | P0 after-hours | 24/7 |

**Enterprise account dedicated channels:**
- ACME Corp: `#acme-corp-support` (shared Slack Connect channel)
- GlobalTech Inc: `#globaltech-support` (shared Slack Connect channel)
- Meridian Enterprises: Email + scheduled Zoom
- Pinnacle Systems: `#pinnacle-support` (shared Slack Connect channel)
- SkyBridge Ltd: Email (Slack Connect being evaluated)

---

## 5. Ticket Routing Rules

### 5.1 Priority Assignment

| Ticket Characteristics | Priority |
|-----------------------|---------|
| Platform completely down for the customer | P0 |
| Core feature (search, upload, auth) non-functional for all customer users | P1 |
| Core feature degraded for subset of users; workaround available | P2 |
| Non-critical feature broken; cosmetic issue | P3 |
| Feature request, documentation question | P3 or Feature Request |
| Billing inquiry | P3 (unless disputed amount > $10K → P2) |

### 5.2 Routing Matrix

| Issue Type | Tier 1 Action | Route To |
|-----------|--------------|---------|
| FAQ / Knowledge base answer available | Respond and close | — |
| Basic account/billing question | Tier 1 handles | — |
| Technical issue (reproducible) | Log details; attempt fix | Tier 2 if not resolved in 30 min |
| Performance complaint | Log; check Known Issues doc | Tier 2 immediately |
| Bug not in Known Issues | Log; basic triage | Tier 2 for engineering assessment |
| Security concern | Alert Head of Support immediately | Security team (anita.sharma@novatech.com) |
| Potential data loss | Alert Head of Support immediately | Tier 3 + Engineering VP |
| Executive escalation | Notify CSM and Head of Support | CSM + Account Executive |
| Refund request | Follow Refund Process SOP | Tier 1 handles intake; escalates per policy |

### 5.3 Ticket Triage Steps (Tier 1)

1. Acknowledge within SLA timeframe (per Section 6)
2. Gather: customer name, plan tier, what they were doing, exact error message, steps to reproduce, browser/device, time of occurrence
3. Check Known Issues doc (`/docs/customer_support/Known_Issues_and_Bug_Log.csv`) — if known issue, provide workaround and link engineering ticket ETA
4. Check StatusPage (status.novatech.io) — if active incident, link and notify customer
5. Attempt to reproduce in test environment
6. If not resolvable in Tier 1 within 30 minutes → escalate to Tier 2 with all gathered context

---

## 6. SLA Matrix

| Priority | First Response | Resolution Target | Update Frequency |
|----------|--------------|------------------|----------------|
| **P0** | 1 hour | 4 hours | Every 15 minutes |
| **P1** | 4 hours | 24 hours | Every 1 hour |
| **P2** | 8 business hours | 72 business hours | Every 4 business hours |
| **P3** | 24 business hours | 7 business days | Every 2 business days |
| **Feature Request** | 48 business hours | N/A (roadmap decision) | Within 2 weeks |

**Enterprise SLA Override:** Enterprise customers receive P1 response time (4h first response) for any issue they report, regardless of agent-assigned priority, until triage confirms lower priority.

---

## 7. Escalation Triggers

Escalate immediately (do not wait for SLA breach) when:

| Trigger | Action |
|---------|--------|
| Customer mentions "cancellation," "churn," or "legal action" | Notify CSM and Head of Support within 15 minutes |
| Executive contact (VP or above) reaches out directly | Notify CSM and Account Executive; prioritize as P1 minimum |
| Customer mentions "data loss" or "data leak" | Escalate to Head of Support + Security team; do NOT respond until reviewed |
| Known issue has no ETA or ETA has passed | Notify Head of Support to get engineering update |
| Customer has submitted 3+ tickets in 7 days | Flag to CSM as health risk |
| CSAT score ≤ 2.0 | Immediate CSM outreach; Head of Support reviews ticket |
| SLA breach in progress (response or resolution overdue) | Notify Tier 2 supervisor immediately |

---

## 8. Communication Guidelines and Tone

### 8.1 Tone Principles

- **Warm but professional.** We are solving real problems that affect real people's work.
- **Plain language.** No jargon, no acronyms without explanation.
- **Accountable.** Say "we" not "the system" or "the engineering team." Own the issue.
- **Factual.** Only commit to timelines that engineering has confirmed.
- **Empathetic.** Acknowledge the customer's frustration before jumping to solutions.

### 8.2 Prohibited Phrases

| Avoid | Say Instead |
|-------|-----------|
| "That's not possible" | "That's not currently supported, but here's what we can do..." |
| "It works on my end" | "Let's investigate together — please share your screen / logs..." |
| "Engineering won't fix that" | "That's not on the current roadmap, but I'll log your feedback..." |
| "You need to contact your IT team" | "Let's work through this together — here's what I'd check first..." |
| "Per our Terms of Service..." | [If contract reference needed, let legal/CSM handle it] |
| Committing to features not on roadmap | "I'll share this feedback with our product team." |

---

## 9. CSAT and Follow-Up Process

### 9.1 CSAT Survey

A CSAT survey is automatically sent via email (Intercom) **24 hours after ticket resolution:**

```
Subject: How was your NovaTech support experience? (2 minutes)

Hi [Name],

We recently resolved your support ticket: "[Ticket Subject]"

How would you rate your support experience?
⭐ ⭐ ⭐ ⭐ ⭐  (1 = Poor, 5 = Excellent)

[Optional] What could we have done better?

Thank you for helping us improve!
```

### 9.2 CSAT Response Actions

| CSAT Score | Automated Action | Human Action |
|-----------|----------------|-------------|
| 5 | Thank-you email | Review for team recognition |
| 4 | None | None |
| 3 | None | Tier 2 supervisor reviews ticket |
| 2 | Flag to Head of Support | CSM reaches out within 24h |
| 1 | Page Head of Support | CSM + AE outreach same day; ticket review |

**Current CSAT (Q1 2026):** 4.2 / 5.0 average (benchmark: 4.0)

---

## 10. Template Library

Full response templates are in `/docs/customer_support/Support_Scripts_and_Response_Templates.md`. Key template categories:

- Initial response (P0, P1, P2, P3)
- Escalation to engineering
- Known issue notification
- Resolution confirmation
- CSAT follow-up
- Refund templates (approved, denied, partial)
- SLA credit notification
- Executive escalation response

---

*This playbook is maintained by the Head of Customer Support. For questions, contact Jennifer Osei (jennifer.osei@novatech.com) or post in #customer-support on Slack.*
