# NovaTech Solutions — Product Launch Playbook
**Version:** 2.3
**Owner:** Rachel Torres, VP of Marketing
**Co-Owners:** Lisa Park (VP Product), Sophia Lee (VP Sales)
**Last Updated:** January 30, 2026
**Applies To:** All product feature and capability launches at NovaTech Solutions

---

## 1. Purpose and Scope

This playbook governs how NovaTech Solutions plans, executes, and measures the success of product launches. Every launch—regardless of size—must follow the applicable tier process. Skipping steps or compressing timelines must be approved by the VP of Marketing and VP of Product.

This document applies to:
- New product capabilities and features
- Integration launches (new third-party connectors)
- Platform updates with customer-visible changes
- Deprecations of features or APIs

It does NOT apply to:
- Internal engineering releases (infrastructure, security patches, non-visible changes)
- Bug fixes (covered by the Incident & Release process in Engineering)

---

## 2. Launch Tier Definitions

### Tier 1 — Major Release
**Definition:** New product capability, new product SKU, significant architectural change, or capability that addresses a new market segment or materially changes competitive positioning.

**Examples:** Multi-Modal Search launch (Q2 2026), NovaTech API v2.0 (2025), Enterprise Analytics Dashboard (2024)

**Requirements:**
- Full PR and media outreach
- Coordinated announcement with press release on PR Newswire
- Analyst briefings (Gartner, Forrester) minimum 2 weeks before launch
- Customer Advisory Board preview minimum 4 weeks before launch
- Sales training and enablement complete before launch
- Legal review of all customer communications and product claims
- CEO involvement in launch communications (blog post or LinkedIn post)

**Timeline:** 8-week minimum (T-8 to T+2 launch window)
**Budget:** $40,000–$120,000 per launch (dedicated campaign budget)

### Tier 2 — Feature Launch
**Definition:** Meaningful new feature within an existing capability that provides notable new value to customers and is worth external promotion.

**Examples:** Slack Integration (2025), Advanced Permissions (2025), Search Analytics Dashboard (2024)

**Requirements:**
- Blog post announcement (primary channel)
- Email notification to all customers (Product Update email)
- In-app announcement banner
- Sales team briefed (Slack message + Notion update)
- Social media posts (LinkedIn, Twitter/X)
- Help documentation updated before launch date

**Timeline:** 4-week minimum (T-4 to T+1 launch window)
**Budget:** $5,000–$20,000

### Tier 3 — Minor Update / Enhancement
**Definition:** Small improvements, UI updates, performance improvements, or minor capability additions.

**Examples:** Search results UI refresh, API rate limit increases, new language support

**Requirements:**
- In-app notification (product changelog)
- Release notes posted to help.novatech.io
- Slack notification to #product-updates channel (internal)
- Customer support team briefed

**Timeline:** 1-week minimum
**Budget:** $0–$2,000

---

## 3. Launch Tier Classification Matrix

| Criteria | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| New customer-facing capability | Yes | Partial | No |
| Addresses new market segment | Yes | No | No |
| Changes pricing or packaging | Yes | Possible | No |
| Competitive differentiation | High | Medium | Low |
| Requires sales training | Yes | Brief | No |
| Requires legal review | Yes | Recommended | No |
| Press release warranted | Yes | No | No |
| Analyst pre-brief required | Yes | No | No |

*Classification decision: VP Product makes initial call; VP Marketing confirms.*

---

## 4. Launch Process — 8-Week Timeline (Tier 1)

### T-8 Weeks: Launch Kickoff
**Owner:** VP Product (Lisa Park)

- [ ] Launch tier confirmed by VP Product + VP Marketing
- [ ] Launch brief created and circulated (template: Notion > Product > Launch Briefs)
- [ ] Launch team identified and DRI (Directly Responsible Individual) assigned
- [ ] External launch date locked (requires Engineering confidence in release date)
- [ ] Analyst pre-brief dates scheduled (Gartner: contact Sarah Kim; Forrester: contact Ben Watkins)
- [ ] Customer Advisory Board preview session scheduled
- [ ] Budget approved by CFO (Carlos Ramirez) for Tier 1 budget >$50K

**Launch Team for Tier 1:**

| Role | DRI | Backup |
|---|---|---|
| Launch Lead (Marketing) | Rachel Torres | Marcus Chen |
| Product Lead | Lisa Park | Alex Rodriguez (Sr. PM) |
| Engineering Lead | Marcus Webb | TBD |
| Sales Enablement | Sophia Lee | Derek Kim (Sr. AE) |
| Customer Success | Janet Okonkwo | CS Manager on rotation |
| Legal | Amanda Hartley | External counsel |
| PR | Rachel Torres + Vantage PR | — |
| Support | Raj Patel (Support Lead) | — |

### T-7 Weeks: Messaging and Positioning
**Owner:** VP Marketing (Rachel Torres)

- [ ] Draft product messaging framework (elevator pitch, headline, key benefits, differentiators)
- [ ] Get messaging sign-off from VP Product + CEO
- [ ] Identify 2–3 customer beta participants for quotes/case study
- [ ] Begin drafting press release (first draft to Legal by T-5)
- [ ] Begin drafting blog post announcement
- [ ] Briefing document created for analyst briefings

### T-6 Weeks: Customer Advisory Board Preview
**Owner:** VP Product (Lisa Park)

- [ ] Present feature to CAB in preview session (NDA required)
- [ ] Gather customer feedback; incorporate into messaging
- [ ] Secure at least 2 customer quotes for launch communications
- [ ] Identify customer reference willing to speak to press (optional for Tier 2)

### T-5 Weeks: Sales Enablement Development
**Owner:** VP Sales (Sophia Lee)

- [ ] Sales battlecard updated (new capability added, competitive response refreshed)
- [ ] Demo environment updated with new feature (Engineering hands off to SE team)
- [ ] Sales deck updated (new slides for feature/capability)
- [ ] Pricing/packaging changes communicated to Sales (if applicable)
- [ ] Legal review of press release (first draft) — target: 5 business day turnaround

### T-4 Weeks: Content Production
**Owner:** Director of Brand & Design (Priya Mehta) + Content team

- [ ] Blog post draft completed and in review
- [ ] Social media copy written (5–10 posts for launch week + follow-up)
- [ ] Product screenshots/GIFs captured for use in blog, social, and sales materials
- [ ] Explainer video script approved (if Tier 1 with video component)
- [ ] Help documentation drafted (Owner: Support Lead Raj Patel)
- [ ] Email templates drafted for customer announcement and prospect announcement

### T-3 Weeks: PR and Analyst Outreach
**Owner:** Rachel Torres + Vantage PR

- [ ] Analyst briefings held (Gartner, Forrester, IDC as applicable)
- [ ] Press release finalized and approved by Legal
- [ ] Media list developed by Vantage PR (target journalists + publications)
- [ ] Embargo agreement drafted for press (if major launch)
- [ ] Pre-brief invitations sent to top 5 target journalists under embargo
- [ ] G2 review request campaign prepared (send within 48h of launch to existing customers)

### T-2 Weeks: Final Approvals
**Owner:** Launch Lead (Rachel Torres)

- [ ] All launch materials reviewed and approved:
  - [ ] Blog post (VP Marketing sign-off)
  - [ ] Press release (Legal + CEO sign-off)
  - [ ] Customer email (CS Lead review)
  - [ ] Sales materials (VP Sales sign-off)
  - [ ] Help documentation (Support Lead review)
  - [ ] Website page updates (Engineering + Marketing review)
- [ ] Sales training session conducted (all AEs + SDRs; recorded for async)
- [ ] Support team briefed on new feature; FAQ document provided
- [ ] Launch day runbook finalized and distributed

### T-1 Week: Pre-Launch
**Owner:** Launch Lead (Rachel Torres)

- [ ] Feature-flagged in production; customer-facing feature NOT yet enabled
- [ ] All marketing assets staged and ready (website, email, social scheduled)
- [ ] Press release filed to PR Newswire (scheduled for launch time)
- [ ] Journalist pre-briefs completed (embargoed until launch time)
- [ ] Launch day communications confirmed (Slack #launch-day channel created)
- [ ] Executive communications drafted (CEO LinkedIn post scheduled)
- [ ] Rollback plan confirmed with Engineering

### T-0: Launch Day
**Owner:** Rachel Torres (Marketing) + Lisa Park (Product)

**Launch Day Timeline (all times Pacific):**

| Time | Action | Owner |
|---|---|---|
| 6:00 AM | Feature enabled in production (rolling deploy) | Engineering |
| 7:00 AM | Press release live on PR Newswire | Vantage PR |
| 7:00 AM | Blog post published | Marcus Chen |
| 7:00 AM | Website page updates live | Engineering |
| 7:15 AM | Social posts published (LinkedIn, Twitter/X) | Priya Mehta |
| 7:30 AM | Customer announcement email sent (All Customers segment) | Rachel Torres |
| 8:00 AM | Internal announcement: #announcements Slack | CEO |
| 8:00 AM | CEO LinkedIn post published | David Huang |
| 8:30 AM | Monitor for press coverage and social mentions | Priya Mehta |
| 9:00 AM | Sales team briefed via Zoom (30-min launch briefing) | Sophia Lee |
| 12:00 PM | Mid-day social post (engagement post) | Priya Mehta |
| 4:00 PM | End-of-day debrief — Launch team 30-min check-in | Rachel Torres |
| 5:00 PM | Launch metrics snapshot shared to Slack #launch-day | Marcus Chen |

### T+1 Week: Post-Launch
**Owner:** Marcus Chen

- [ ] Week 1 metrics report (email opens, blog traffic, MQL impact, press coverage)
- [ ] Monitor and respond to customer feedback in support tickets and social
- [ ] G2 review request email sent to existing customers
- [ ] Follow-up social posts (customer testimonial, use case spotlight)

### T+2 Weeks: Launch Retrospective
**Owner:** Rachel Torres

- [ ] Launch retrospective conducted with full launch team (60-minute session)
- [ ] Retrospective document completed (Notion > Product > Launch Retros)
- [ ] Success/failure metrics reviewed against targets
- [ ] Lessons learned captured and incorporated into next version of this Playbook

---

## 5. Press Release Template

```
FOR IMMEDIATE RELEASE

[DATE]

NovaTech Solutions Launches [FEATURE NAME], Enabling [PRIMARY BENEFIT]

[City, State] — NovaTech Solutions, the leading AI-powered knowledge management 
and enterprise search platform, today announced [FEATURE NAME], a new capability 
that [one-sentence description of what it does and for whom].

[QUOTE: CEO David Huang] — 2–3 sentence quote about strategic importance.

[BODY PARAGRAPH 1: Problem being solved — 2–3 sentences]

[BODY PARAGRAPH 2: How the feature works — non-technical, benefit-led — 3–4 sentences]

[QUOTE: Customer (name, title, company)] — 2–3 sentences on impact.

[BODY PARAGRAPH 3: Availability and pricing — 2 sentences]

[BODY PARAGRAPH 4: Supporting resources — links to blog post, demo, documentation]

About NovaTech Solutions
NovaTech Solutions is the AI-powered knowledge management and enterprise search 
platform for the modern enterprise. Founded in 2018 and headquartered in San 
Francisco, NovaTech serves 87 enterprise customers including ACME Corp, GlobalTech 
Inc, Meridian Enterprises, Pinnacle Systems, and SkyBridge Ltd. For more 
information, visit www.novatech.io.

Media Contact:
[Name], [Title]
press@novatech.io | [Phone]
```

---

## 6. Sales Enablement Requirements (Tier 1)

All of the following must be delivered to Sales at least 7 days before launch date:

| Deliverable | Owner | Format |
|---|---|---|
| Updated sales battlecard | Marcus Chen | 1-page PDF + Notion page |
| Updated master sales deck (new slides) | Priya Mehta | Google Slides |
| Customer FAQ (anticipated objections) | Lisa Park | Notion |
| Demo script (new capability section) | SE Team (James Kim) | Notion + Loom video |
| Competitive positioning (vs. DataBridge, FlowLogic) | Marcus Chen | 1-page PDF |
| Pricing/packaging sheet (if changed) | Sophia Lee + Finance | PDF |

---

## 7. Customer Communication Plan

### Existing Customers
- **Channel:** Email (HubSpot) + In-app notification
- **Sender:** Janet Okonkwo, VP of Customer Success (or CSM for named accounts)
- **Timing:** Launch day (email), T-1 week (in-app preview for beta participants)
- **Tone:** Informative, benefit-focused, action-oriented (CTA: "Try it now" or "Read more")
- **Segmentation:** All paying customers; separate email for customers on plans where feature is not included

### Prospects in Active Evaluation
- **Channel:** SDR/AE outreach (personalized email or call)
- **Timing:** Within 48 hours of launch
- **Talking point:** "You may have seen we launched [feature] — this directly addresses the [specific pain] you mentioned. I'd love to show you how it works."

---

## 8. Post-Launch Metrics

### Tier 1 Launch Success Metrics (measured at 30 and 90 days)

| Metric | Baseline | 30-Day Target | 90-Day Target |
|---|---|---|---|
| Feature adoption (% of customers using new feature) | 0% | 25% | 60% |
| Press coverage (articles/mentions) | 0 | 8 | 15 |
| MQLs influenced by launch content | 0 | 50 | 150 |
| Pipeline influenced | $0 | $500K | $1.5M |
| Customer CSAT (NPS survey post-launch) | Baseline | No regression | +3 pts |
| G2 reviews mentioning new feature | 0 | 5 | 15 |

---

*Document Owner: Rachel Torres, VP of Marketing*
*Approved By: David Huang (CEO), Lisa Park (VP Product), Sophia Lee (VP Sales)*
*Next Review: July 2026*
