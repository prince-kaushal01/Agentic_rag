# NovaTech Solutions — Account Management Handbook
**Customer Success Organization | Version 2.0 | January 2026**
**Owner: Samuel Osei, Director of Customer Success**
**cs@novatechsolutions.com**

---

## Table of Contents
1. Customer Success Philosophy
2. QBR (Quarterly Business Review) Process
3. Customer Health Scoring Model
4. Expansion Playbook
5. Renewal Process
6. Executive Sponsor Program
7. Customer Onboarding Handoff (From Sales)
8. Escalation Procedures
9. Churn Risk Signals & Interventions
10. CS Metrics & KPIs

---

## 1. Customer Success Philosophy

At NovaTech Solutions, Customer Success is not a support function — it is a growth function. Our CSMs are accountable for three things:
1. **Adoption:** Customers achieve measurable value from the NovaTech platform
2. **Retention:** Customers renew their contracts; NRR target is 120%+
3. **Expansion:** Customers grow their investment in NovaTech through additional seats, modules, or multi-year commitments

Every CSM manages a named book of accounts. The size and makeup of each book depends on the CSM's level and the average ARR of their accounts:
- **Associate CSM:** $1M–$2M ARR book; typically 15–25 accounts (average ARR $75K–$100K)
- **CSM:** $2M–$3.5M ARR book; typically 12–18 accounts (average ARR $150K–$200K)
- **Senior CSM:** $3.5M–$6M ARR book; 8–12 strategic accounts (average ARR $400K–$600K)

All CSM activity is tracked in **Gainsight**, our Customer Success platform. Gainsight integrates with Salesforce, Zendesk, and the NovaTech platform itself to provide a 360-degree view of each customer.

---

## 2. QBR (Quarterly Business Review) Process

QBRs are the cornerstone of the NovaTech CSM motion for accounts above $75,000 ARR. They are held once per quarter (Q1 results in April; Q2 in July; Q3 in October; Q4/Year-End in January).

### 2.1 QBR Scheduling & Attendance
- QBRs should be scheduled at least **3 weeks in advance**
- Request attendance from: Champion, key day-to-day contacts, at least one VP or Director from the customer side
- NovaTech attendees: CSM (required), Customer's AE (for expansion discussions), and optionally the Director of CS (for strategic or at-risk accounts)
- Format: 60-minute video call (or in-person for Tier 1 accounts)
- For accounts <$75K ARR: QBRs are replaced with bi-annual Business Reviews (2x per year)

### 2.2 QBR Agenda Template

**Recommended 60-Minute Agenda:**

```
1. Welcome & Agenda Review (5 min)
   - Introductions if new faces
   - Confirm agenda and outcomes for the session

2. Your Business Update (10 min)
   - Customer shares: key business initiatives, org changes, strategic priorities for next quarter
   - CSM asks: "What's keeping you up at night this quarter?"

3. Platform Usage & Adoption Review (15 min)
   - Monthly active users (MAU) trend
   - Search volume and search success rate
   - Top 10 most-accessed content pieces
   - Departments with highest and lowest adoption
   - Action items from last QBR — did we deliver?

4. Value Delivered: Metrics Review (10 min)
   - Progress against agreed success metrics (e.g., ticket deflection rate, MTTR, onboarding time)
   - Customer-sourced data where available (customer to share their support metrics)
   - ROI calculation update

5. Product Updates & Roadmap Highlights (10 min)
   - New features released since last QBR
   - Roadmap items relevant to their use case (NDA if sharing unreleased roadmap)
   - Request feedback on priority features

6. Opportunities & Next Steps (10 min)
   - Are there untapped use cases (departments not yet using NovaTech)?
   - Expansion conversation if health is green
   - Open support tickets or unresolved issues
   - Agreement on 2–3 action items for next quarter (CSM and customer)
```

### 2.3 Pre-QBR Preparation (CSM Responsibilities)
- Pull Gainsight usage report 1 week before QBR
- Review support ticket history for the quarter
- Prepare a QBR deck using the standard template (in Notion: CS Resources > QBR Templates)
- Share deck with customer champion at least 48 hours before the meeting for preview
- Update Gainsight account record with QBR notes within 24 hours after meeting

### 2.4 Post-QBR Requirements
- Send meeting recap email with agreed action items within 24 hours
- Update Gainsight health score based on QBR discussion
- Log any expansion indicators as Opportunities in Salesforce
- If account is in Yellow or Red health: update Risk record in Gainsight and notify CS Director

---

## 3. Customer Health Scoring Model

NovaTech uses a **Health Score** system in Gainsight to track account risk and prioritize CSM attention. Health scores update automatically based on platform data and are overridden manually based on CSM judgment.

### 3.1 Health Score Dimensions

| Dimension | Weight | Measured By |
|-----------|--------|-------------|
| Product Adoption | 30% | Monthly active users / total licensed users; search volume vs. baseline |
| Engagement | 20% | QBR held on time; champion responsiveness; NPS score (last 90 days) |
| Support Health | 15% | Open P1/P2 tickets >5 days; CSAT scores below 4.0/5.0 |
| Contract Health | 20% | Days to renewal; % of contract value at risk; multi-year status |
| Relationship Breadth | 15% | Number of departments using platform; champion seniority; exec sponsor presence |

### 3.2 Health Score Thresholds

| Score | Color | Meaning |
|-------|-------|---------|
| 80–100 | 🟢 Green | Healthy — on track for renewal and expansion |
| 60–79 | 🟡 Yellow | At Risk — attention required; intervention may be needed |
| 0–59 | 🔴 Red | High Risk — active save required; CS Director engaged |

### 3.3 Green Account Criteria
A Green account demonstrates:
- Monthly active users ≥70% of licensed seats
- QBR held within last 90 days
- No P1 open tickets
- CSAT score ≥4.2/5.0 (last 3 surveys)
- Renewal date >120 days away OR renewal conversation started
- Champion has responded to CSM within 7 days

### 3.4 Yellow Account Criteria
A Yellow account shows at least one of:
- MAU between 40–70% of licensed seats
- Last QBR held >90 days ago
- 1–2 open P2 tickets unresolved >5 days
- CSAT score 3.5–4.2
- Renewal date 60–120 days away without confirmed renewal conversation
- Champion has not responded in 7–14 days

### 3.5 Red Account Criteria
A Red account shows at least one of:
- MAU <40% of licensed seats
- Last QBR >150 days ago (or never held)
- P1 ticket open >48 hours or pattern of escalations
- CSAT score <3.5
- Renewal date <60 days without confirmed renewal commitment
- Champion departed (no replacement identified)
- Customer has formally expressed intent to churn or reduce scope

---

## 4. Expansion Playbook

### 4.1 Expansion Philosophy
Every CSM is responsible for identifying and surfacing expansion opportunities within their book. Expansion includes:
- **Seat Expansion:** Additional licensed users (departments not yet on platform)
- **Module Upsell:** Adding Compliance, Advanced Analytics, Support AI, or other modules
- **Tier Upgrade:** Moving from Starter to Professional, or Professional to Enterprise
- **Multi-Year Conversion:** Converting annual to 2- or 3-year commitment

Expansion conversations are led by the CSM, with the AE brought in to close commercial terms.

### 4.2 Upsell Triggers
Gainsight sends an automated alert to the CSM when any of the following signals are detected:

| Trigger | Signal | CSM Action |
|---------|--------|-----------|
| High adoption in one department | MAU >90%; search volume spiking | Identify adjacent departments; propose expansion |
| Knowledge gap alerts | >50 unanswered searches in 30 days | Propose content migration from adjacent system |
| New hire spike | Customer's LinkedIn headcount growth >10% in 90 days | Seat expansion conversation |
| Support ticket volume spike | Customer opening >30% more Zendesk tickets | Propose Support AI deflection module |
| Compliance event | News event; customer mentions audit; regulatory change | Propose Compliance Module |
| Annual review season | Annual review within 180 days | Multi-year conversion conversation |

### 4.3 Cross-Sell Motion
NovaTech's cross-sell motion focuses on getting the platform adopted in multiple departments within the same organization. The typical expansion journey:
- **Phase 1:** IT Department (internal knowledge base)
- **Phase 2:** Customer Support (Zendesk integration, Answer Suggestions)
- **Phase 3:** HR / People Ops (policy hub, onboarding documentation)
- **Phase 4:** Engineering (technical documentation, runbooks)
- **Phase 5:** Company-wide deployment

CSMs should understand which departments are NOT yet using NovaTech and present a phased expansion plan annually.

---

## 5. Renewal Process

### 5.1 90-Day Renewal Runway
The renewal process begins **90 days before the contract end date**. Gainsight auto-creates a "Renewal" call-to-action for the CSM at the 90-day mark.

**90 Days Out:**
- CSM confirms champion is still in role and aware of renewal
- CSM schedules "Renewal Health Review" call with champion
- CSM runs a health score review and flags any risks
- If account is Yellow or Red: escalate to CS Director immediately

**60 Days Out:**
- Commercial terms discussion begins with the champion
- If expansion is likely: AE is engaged
- CSM sends formal renewal notice email with contract summary
- Multi-year conversion proposal (if applicable)

**30 Days Out:**
- Final pricing confirmed; DocuSign renewal order form sent
- If not signed: Executive Sponsor from NovaTech called into the process
- CS Director reviews all renewals >$100K ARR

**Renewal Day:**
- If not signed by renewal date: account goes into 30-day grace period (per MSA terms)
- Grace period: CSM escalates daily; CS Director personally calls customer VP

### 5.2 At-Risk Renewal Protocol
If a renewal is in question (customer has expressed hesitation, budget constraints, or dissatisfaction):
1. CSM immediately flags as Red in Gainsight
2. CS Director joins the next customer call
3. A "Save Plan" is documented in Gainsight (root cause, proposed remedy, owner, timeline)
4. If root cause is product dissatisfaction: Product team is looped in for a roadmap conversation
5. If root cause is price: Sales Manager approves a discount (per the Discount Approval Matrix)
6. Marcus Harrington (CEO) or Daniel Okafor (VP Sales) personally calls any at-risk account >$200K ARR

### 5.3 Renewal Rate Targets (2026)
- Gross Revenue Retention (GRR) target: ≥90%
- Net Revenue Retention (NRR) target: ≥120%
- On-time renewal rate target: ≥85% (renewed before expiration)

---

## 6. Executive Sponsor Program

### 6.1 Overview
NovaTech assigns an Executive Sponsor from our leadership team to every customer with >$150K ARR. The Executive Sponsor is a named NovaTech executive who has a relationship with a senior executive at the customer organization.

### 6.2 Sponsor Assignments

| Customer ARR Tier | NovaTech Executive Sponsor |
|------------------|--------------------------|
| $150K–$300K | Director of CS or Sales Manager |
| $300K–$600K | VP of Sales or VP of Customer Success |
| $600K+ | CEO or CTO |

### 6.3 Executive Sponsor Responsibilities
- Attend or lead the Annual QBR for the account
- Respond within 24 hours when a CS escalation reaches executive level
- Maintain a personal relationship with the customer's C-suite or VP-level contact
- Be available for a 30-minute check-in call quarterly with the customer's exec

### 6.4 Executive Sponsor Contact List (as of January 2026)

| Customer | Annual ARR | NovaTech Sponsor |
|----------|-----------|-----------------|
| ACME Corp | $680,000 | Marcus Harrington (CEO) |
| GlobalTech Inc | $520,000 | Priya Venkatesan (CTO) |
| Meridian Enterprises | $387,000 | Daniel Okafor (VP Sales) |
| SkyBridge Ltd | $395,000 | Samuel Osei (Dir. CS) |
| Pinnacle Systems | $145,000 | Megan Fitzgerald (Sales Manager) |

---

## 7. Customer Onboarding Handoff (From Sales)

The handoff from the AE to the CSM is a critical moment that sets the tone for the customer relationship. Poorly executed handoffs are one of the top 3 causes of early churn.

### 7.1 Handoff Requirements (AE Responsibility)
Before handoff, the AE must complete a **Customer Handoff Document** in Salesforce/Notion within 5 business days of contract signing:
- Contract summary (ARR, term, modules purchased, users licensed)
- MEDDIC summary: customer pain points, success metrics agreed upon, key stakeholders
- Champion and EB contact information
- Any commitments made during the sales process (feature requests, SLAs, implementation timeline)
- Competitive context (who did they evaluate? why did they choose NovaTech?)
- Any red flags or concerns to be aware of

### 7.2 Introduction Meeting
The AE schedules a **Sales-to-CS Handoff Introduction Call** within 5 business days of contract signing:
- AE introduces the CSM to the champion and day-to-day contacts
- AE explicitly passes the relationship ("Jordan will be your day-to-day point of contact going forward; she'll know your business better than I do")
- CSM outlines the onboarding plan and introduces the timeline
- AE attends but says very little — this is the CSM's meeting

### 7.3 Onboarding Timeline (Standard)
| Week | Activity |
|------|---------|
| Week 1 | Kickoff call; technical SSO setup; admin training (2 hours) |
| Week 2–3 | Content migration (customer provides content; NovaTech provides tools and templates) |
| Week 4 | Integration setup (Zendesk, Slack, Salesforce) |
| Week 5–6 | User training sessions (by department); launch communications support |
| Week 7–8 | Go-live; 30-day adoption check |
| Week 12 | First health score review; first QBR scheduled |

---

## 8. Escalation Procedures

### 8.1 Product/Technical Escalation
When a customer reports a P1 issue (platform down or severely impaired):
1. Customer contacts support via email or phone
2. Support team opens P1 ticket in Zendesk and pages on-call engineering (PagerDuty)
3. CSM is automatically notified via Gainsight
4. CSM proactively contacts customer within 1 hour to acknowledge and provide status
5. Engineering provides 30-minute status updates until resolved
6. CSM sends post-incident summary within 24 hours of resolution

### 8.2 Relationship Escalation
When a customer expresses frustration, distrust, or intent to cancel:
1. CSM notifies CS Director (Samuel Osei) within 4 hours
2. CS Director reviews the situation and determines appropriate response level
3. For accounts >$200K: VP of Sales or CEO is looped in
4. A Save Plan is documented in Gainsight
5. Resolution timeline: committed response within 24 hours; save plan execution within 7 days

---

## 9. Churn Risk Signals & Interventions

### 9.1 Early Warning Signals
Monitor these Gainsight signals weekly:

| Signal | Risk Level | Recommended Intervention |
|--------|-----------|--------------------------|
| MAU drops >20% month-over-month | High | Adoption intervention call within 3 business days |
| Champion departs | High | Identify replacement champion; executive outreach within 48 hours |
| CSAT score drops below 3.5 | High | CSM + CS Director call within 24 hours |
| No QBR in 120+ days | Medium | Proactively schedule QBR; offer exec sponsor involvement |
| Support ticket spike (>50% increase) | Medium | Technical health check; loop in engineering if needed |
| Customer mentions competitor | Medium | Prepare competitive talking points; escalate to Sales for support |
| Low search success rate (<70%) | Medium | Content audit; offer content consultation session |
| 60+ days to renewal with no conversation | Medium | Immediate renewal outreach |

### 9.2 Intervention Scripts

**For Low Adoption:**
"Hi [Name] — I was reviewing your platform data this week and noticed usage has been lower than I'd expect given how many users you have licensed. I'd love to schedule 30 minutes to understand what's getting in the way — whether it's awareness, content quality, or something in the workflow. I have some ideas that have worked well for other [industry] customers. Are you free [specific date/time]?"

**For Champion Departure:**
"Hi [New Contact] — I wanted to reach out because I heard that [Former Champion] has moved on. I'm [Name], your Customer Success Manager at NovaTech. I'd love to set up a call to introduce myself and make sure the transition is as smooth as possible for your team. Would [date/time] work?"

---

## 10. CS Metrics & KPIs (2026)

| Metric | 2026 Target | 2025 Actual |
|--------|------------|-------------|
| Net Revenue Retention (NRR) | 120% | 114% |
| Gross Revenue Retention (GRR) | 90% | 88% |
| Average Onboarding Time to Value | 45 days | 52 days |
| QBR Completion Rate | 85% on schedule | 71% |
| NPS Score | 42+ | 38 |
| CSAT (support) | 4.3/5.0+ | 4.1/5.0 |
| Expansion ARR (CS-sourced) | $5.5M | $3.8M |
| Churn Rate (logo) | <8% | 9.2% |
| CSM Capacity (ARR per CSM) | $3M | $2.6M |

---

*Document Owner: Samuel Osei, Director of Customer Success*
*Contributing Authors: Grace Nakamura, Drew Washington*
*Last Updated: January 10, 2026 | Next Review: July 2026*
