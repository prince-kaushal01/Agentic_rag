# NovaTech Solutions — Sprint Planning Template and Norms

**Document Version:** 2.1  
**Last Updated:** January 8, 2026  
**Authors:** Rachel Torres (Engineering Manager, Product Team), Priya Nair (VP Engineering)  
**Classification:** Internal — Engineering  
**Applies To:** All engineering teams at NovaTech Solutions

---

## 1. Overview

NovaTech Solutions engineering teams operate on **2-week sprint cycles**. All teams are aligned to the same sprint calendar (synchronized start dates) to facilitate cross-team dependency management and unified sprint reviews.

The sprint cadence was standardized across all three teams (Platform, Product, Data) in Q3 2024. Prior to this, teams ran independent cadences, causing coordination overhead during cross-team projects.

**Current Sprint Cadence (Q2 2026):**
- Sprint Start: Monday, 10:00 AM PT
- Sprint End: Friday (end of sprint week 2)
- Planning: Sprint Start Monday, 10:00–12:00 AM PT
- Daily Standups: Monday–Friday, 9:30–9:45 AM PT (async Thursday; in-person sync Friday)
- Sprint Review: Second Friday, 3:00–4:00 PM PT
- Sprint Retrospective: Second Friday, 4:00–5:00 PM PT

---

## 2. Sprint Calendar Q2 2026

| Sprint | Start Date | End Date | Notes |
|--------|-----------|---------|-------|
| Sprint 42 | April 6, 2026 | April 17, 2026 | Q2 kickoff |
| Sprint 43 | April 20, 2026 | May 1, 2026 | |
| Sprint 44 | May 4, 2026 | May 15, 2026 | |
| Sprint 45 | May 18, 2026 | May 29, 2026 | Memorial Day May 25 — capacity impact |
| Sprint 46 | June 1, 2026 | June 12, 2026 | |
| Sprint 47 | June 15, 2026 | June 26, 2026 | Q2 close sprint |

---

## 3. Sprint Ceremonies

### 3.1 Sprint Planning (Monday, 10:00–12:00 PM PT — 2 hours)

**Purpose:** Align the team on the sprint goal, select stories from the backlog, and decompose work into tasks.

**Participants:** All team members, Engineering Manager, Product Manager (first 45 min), relevant stakeholders (first 15 min only)

**Agenda:**
| Time | Activity | Owner |
|------|----------|-------|
| 0:00–0:10 | Review sprint metrics from last sprint (velocity, carryover, bugs) | EM |
| 0:10–0:25 | Product Manager presents top priorities and context for this sprint | PM |
| 0:25–0:35 | Team reviews capacity (PTO, on-call rotation, interruption budget) | EM |
| 0:35–0:50 | Agree on Sprint Goal (1–2 sentences, outcome-focused) | Team |
| 0:50–1:45 | Pull stories from backlog into sprint; verify DoR; estimate if not yet estimated | Team |
| 1:45–2:00 | Confirm sprint commitment and identify dependencies/risks | Team |

**Outputs:**
- Sprint goal documented in Jira
- Sprint backlog populated and committed
- Risk/dependency log updated

### 3.2 Daily Standup (Daily, 9:30–9:45 AM PT — 15 minutes)

**Format:** Round-robin (max 2 minutes per person)

Each engineer answers:
1. **Yesterday:** What did I complete?
2. **Today:** What am I working on?
3. **Blockers:** Is anything blocking my progress?

**Rules:**
- Discussions are parked and taken offline — standup is for status, not problem-solving
- Async standup on Thursdays (post in team Slack by 10 AM PT using `/standup` bot)
- Absent engineers post async regardless of timezone

**Anti-patterns to avoid:**
- "Same as yesterday" — be specific
- Technical deep-dives — take them offline
- Status updates on tickets that aren't in the current sprint

### 3.3 Sprint Review (Second Friday, 3:00–4:00 PM PT — 1 hour)

**Purpose:** Demonstrate completed work to stakeholders; get feedback; celebrate wins.

**Participants:** Team, EM, PM, relevant stakeholders, Customer Success (optional for customer-facing features), Sales (optional)

**Agenda:**
| Time | Activity |
|------|----------|
| 0:00–0:05 | Sprint overview: goal, velocity, completion rate |
| 0:05–0:50 | Demos of completed stories (each engineer demos their own work) |
| 0:50–0:60 | Stakeholder feedback, questions, and discussion |

**Rules:**
- Only fully completed work (meets Definition of Done) is demoed
- Demo the actual product — no slides, no descriptions of what was built
- Stakeholder feedback is captured in Jira as new tickets or refinement notes

### 3.4 Sprint Retrospective (Second Friday, 4:00–5:00 PM PT — 1 hour)

**Purpose:** Team-level continuous improvement. Honest reflection on process, not people.

**Participants:** Engineering team and EM only (no PM, no stakeholders — psychological safety)

**Format (rotating between three formats):**
1. **Start/Stop/Continue:** What should we start doing, stop doing, keep doing?
2. **4Ls:** What did we Like, Learn, Lacked, and Long for?
3. **DACI for action items:** After discussion, each action item gets: Driver, Approver, Contributor, Informed

**Rules:**
- Feedback is about the process, not individuals
- Every retro must produce ≥ 1 and ≤ 3 concrete action items with owners and deadlines
- Action items from the previous retro are reviewed at the start of each retro (were they completed?)
- Retro notes are kept private within the team (not distributed to leadership)

---

## 4. Story Point Scale

NovaTech uses the **Fibonacci sequence** for story points: 1, 2, 3, 5, 8, 13, 21, and ∞ (spike/unknown).

| Points | Complexity Level | Description |
|--------|----------------|-------------|
| 1 | Trivial | Clearly understood change; minimal risk; < 2 hours |
| 2 | Simple | Well-understood; minor unknowns; < 4 hours |
| 3 | Moderate | Some complexity; a few unknowns; ~1 day |
| 5 | Complex | Multiple components; meaningful unknowns; ~2 days |
| 8 | Large | Significant complexity; several unknowns; ~3–4 days |
| 13 | Very Large | Major effort; high uncertainty; consider breaking down; ~1 week |
| 21 | Epic-sized | Should be decomposed into smaller stories |
| ∞ | Unknown | Spike required before estimation is possible |

**Estimation Rules:**
- Points estimate **relative complexity**, not time. A 3-point story for a senior engineer takes the same relative effort as a 3-point story for a junior engineer — the point reflects the problem complexity, not the person.
- Never assign points to a story without discussing it as a team. Solo estimation is prohibited.
- If spread > 3 Fibonacci values, the team must discuss before re-estimating
- Stories > 13 points must be decomposed before entering a sprint

**Planning Poker:** Used for estimation. Tool: `PlanningPokerOnline.com` (team shortlink: `nt.tools/poker`)

---

## 5. Velocity Tracking

### 5.1 Current Velocity Statistics

| Team | 3-Sprint Average | 6-Sprint Average | Target | Trend |
|------|----------------|----------------|--------|-------|
| Platform Team | 44 points | 42 points | 40–48 points | Stable ↔ |
| Product Team | 38 points | 40 points | 38–46 points | Stable ↔ |
| Data Team | 46 points | 44 points | 42–50 points | Improving ↑ |
| **Combined Average** | **42 points** | **42 points** | **40–48 points** | — |

**Platform Team (7 engineers, Q1 2026 sprints):**
- Sprint 38: 48 points
- Sprint 39: 41 points (1 engineer on vacation)
- Sprint 40: 43 points

**Product Team (8 engineers, Q1 2026 sprints):**
- Sprint 38: 37 points
- Sprint 39: 40 points
- Sprint 40: 37 points

**Data Team (6 engineers, Q1 2026 sprints):**
- Sprint 38: 44 points
- Sprint 39: 47 points
- Sprint 40: 47 points

### 5.2 Velocity Guidelines

- **Don't inflate velocity.** Never carry unfinished work as "done." Partial credit is 0 points.
- **Protect velocity.** Use historical velocity + capacity calculation to plan, not optimism.
- **Velocity is a team metric**, not an individual performance metric. Do not compare individual output.
- Velocity fluctuations of ±20% are expected and normal.

---

## 6. Capacity Planning

### 6.1 Capacity Calculation

```
Sprint Capacity (points) = Available Team Days × Focus Factor × Points Per Day

Available Team Days = (Team size × Sprint days) - PTO days - Holiday days
Sprint days = 10 (2-week sprint)
Focus Factor = 0.70 (accounts for meetings, standups, reviews, on-call)
Points Per Day = team velocity / (team size × sprint days × focus factor)

Example (Platform Team, Sprint 42, April 6–17, 2026):
Team size: 7 engineers
PTO: 3 days (1 engineer out 3 days)
Holiday: 0
Available days: (7 × 10) - 3 = 67 days
Focus Factor: 0.70
Adjusted capacity: 67 × 0.70 = 46.9 ~ 47 points

Interruption budget (20%): 47 × 0.20 = 9.4 ~ 9 points reserved
Available for planned stories: 47 - 9 = 38 points
```

### 6.2 Interruption Budget

**20% of each sprint capacity is reserved for unplanned work:**
- Production bug fixes
- Customer escalations
- On-call incident follow-up
- Urgent dependency requests from other teams

If the interruption budget is exhausted mid-sprint, the team notifies the EM, who will negotiate with PM to defer low-priority sprint work.

If interruption budget is consistently < 50% utilized, the team should increase planned capacity accordingly.

---

## 7. Definition of Done (DoD)

A story is **Done** when ALL of the following criteria are met:

**Code Quality:**
- [ ] Code reviewed and approved (meeting PR standards)
- [ ] All CI checks passing (linting, tests, security scan)
- [ ] Unit test coverage maintained or improved (≥ 80% line coverage)
- [ ] Integration tests updated or added for API changes

**Functionality:**
- [ ] Acceptance criteria from the story are verified
- [ ] Feature tested in staging environment
- [ ] Feature flag configured (if applicable) and tested in disabled state
- [ ] No known P0 or P1 bugs introduced

**Documentation:**
- [ ] API docs updated (if API changes)
- [ ] Runbook updated (if operational behavior changes)
- [ ] PR description includes rollback plan

**Deployment:**
- [ ] Code merged to `main`
- [ ] Successfully deployed to staging
- [ ] Smoke tests passing in staging
- [ ] Ready for production release (pending release train schedule)

**Stories that do not meet DoD are not counted toward sprint velocity and carry over to the next sprint.**

---

## 8. Definition of Ready (DoR)

A story is **Ready** for sprint planning when:

- [ ] User story has a clear description: "As a [user], I want [capability] so that [outcome]"
- [ ] Acceptance criteria are specific and testable (at least 3 criteria)
- [ ] Story has been estimated (points assigned)
- [ ] Dependencies are identified and unblocked (or blocking tickets linked)
- [ ] Design/wireframes available (for UI stories)
- [ ] Technical approach agreed at high level (for complex stories > 5 points)
- [ ] Story is ≤ 13 points (larger stories decomposed)

**Backlog grooming SLA:** The top 2 sprints of backlog (2 × team velocity) must always be refined and meet DoR. PM owns refinement scheduling; EM owns technical readiness.

---

## 9. Sprint Goal Format

The sprint goal is a single outcome-focused statement that answers: **"What is the most important thing this team accomplishes this sprint?"**

**Good sprint goal format:**
> "Enable [customer segment] to [do something] by [completing key deliverables]."

**Examples of good sprint goals:**
- "Resolve the search performance bottleneck for large tenants by delivering Elasticsearch shard rebalancing and query cache optimization."
- "Launch the Agentic Q&A API in beta with 3 design partner customers onboarded and providing feedback."
- "Complete SOC 2 audit evidence collection for access controls and complete the missing audit log controls."

**Examples of bad sprint goals:**
- "Work on ENG-2847, ENG-2801, ENG-2834, ENG-2892" ← list of tickets, not an outcome
- "Make progress on the roadmap" ← too vague
- "Complete all stories in sprint" ← this is always the implicit goal; not a useful sprint goal

---

## 10. Bug Triage SLA

Bugs reported during a sprint are assessed and assigned a priority within the following timeframes:

| Bug Priority | Assessment SLA | Action |
|-------------|---------------|--------|
| P0 (production outage) | Immediate | Declared as incident; all hands |
| P1 (major feature broken) | 4 hours | Added to current sprint immediately; interruption budget |
| P2 (moderate impact) | 24 hours | Added to next sprint or current sprint if capacity allows |
| P3 (minor impact) | 48 hours | Added to backlog; prioritized in next grooming session |

Bug reports from customers automatically generate support tickets (TKT- prefix). If a bug is linked to a customer ticket, the priority is elevated by one level.

---

## 11. Meeting Norms

| Norm | Applies To |
|------|-----------|
| Start and end on time | All sprint ceremonies |
| No laptops unless presenting | Planning, Review, Retro |
| Decisions documented in Jira or Confluence by EM | Planning, Review |
| Camera on during remote ceremonies | All ceremonies |
| Async-first for questions that can wait | Between ceremonies |
| Pre-read materials shared 24h before planning | Planning |

---

*This document is maintained by Engineering Managers. Feedback welcome in #eng-process on Slack. Last major revision: January 8, 2026 (added interruption budget calculation; updated velocity stats for Q4 2025).*
