# NovaTech Solutions — Incident Response Playbook

**Document Version:** 4.1  
**Last Updated:** January 20, 2026  
**Authors:** Priya Nair (VP Engineering), Kevin Osei (SRE Lead), Rachel Torres (Engineering Manager)  
**Classification:** Internal — Engineering Confidential  
**Review Cycle:** Semi-annual (next review: July 2026)

---

## 1. Purpose and Scope

This playbook defines NovaTech Solutions' incident response procedures, roles, communication standards, and post-incident review processes. It applies to all engineering personnel who may be involved in responding to production incidents — including on-call engineers, Incident Commanders, engineering managers, and executive stakeholders.

Adherence to this playbook is required during all declared incidents (P0–P2). P3 and P4 incidents follow lightweight procedures outlined in Section 3.5.

---

## 2. Incident Severity Classification

### Severity Levels

| Severity | Name | Definition | Examples |
|----------|------|-----------|---------|
| **P0** | Critical — Service Down | Complete platform unavailability or data loss/corruption affecting all customers or a major customer segment | Full platform outage; database corruption; security breach; data loss |
| **P1** | High — Major Degradation | Core functionality severely degraded for a significant portion of customers; SLA breach in progress or imminent | Search service returning errors for 20%+ of requests; authentication failures for multiple tenants; significant performance regression (>5x normal latency) |
| **P2** | Medium — Partial Degradation | Non-critical feature impaired, or critical feature degraded for a small subset of customers; SLA breach possible | Single customer impacted by bug; non-critical integration down; elevated error rates on non-core endpoints |
| **P3** | Low — Minor Issue | Minor bug or cosmetic issue with no SLA impact; individual user complaint; documentation error | UI rendering bug; slow loading on a single page; typo in error message |
| **P4** | Informational | Potential future risk; non-production issue; proactive alert requiring investigation | Staging environment alert; elevated disk usage warning; non-customer-impacting dependency version issue |

### Severity Determination Guide

When paging is triggered (automatically by Datadog or manually), the on-call engineer must assess severity within **5 minutes** using the following questions:

1. Is the platform completely unavailable for any customers? → **P0**
2. Are core features (search, document upload, authentication) failing for >10% of users? → **P1**
3. Is there evidence of data loss or security breach? → **P0** (regardless of scope)
4. Is one major customer (Enterprise tier) experiencing a severe issue? → **P1** (escalate to P0 if customer escalates to executive level)
5. Is a non-critical feature unavailable for a subset of users? → **P2**

When in doubt, **escalate up** (declare higher severity). Downgrading is always easier than upgrading.

---

## 3. Response Time and Escalation Requirements

### 3.1 Response Time SLAs

| Severity | Acknowledgment | Initial Response to Customer | Resolution Target | Status Update Frequency |
|----------|---------------|------------------------------|------------------|------------------------|
| P0 | 5 minutes | 15 minutes | 4 hours | Every 15 minutes |
| P1 | 15 minutes | 30 minutes | 24 hours | Every 30 minutes |
| P2 | 1 hour | 4 hours | 72 hours | Every 4 hours |
| P3 | 4 hours | 24 hours | 7 days | Daily |
| P4 | 24 hours | Not required | 30 days | Weekly |

### 3.2 Escalation Paths

**P0 Escalation Chain:**
1. On-Call Engineer (acknowledges PagerDuty alert)
2. On-Call Engineering Manager (auto-paged after 5 min if not acknowledged)
3. VP Engineering — Priya Nair (auto-paged at P0 declaration; mobile: +1-628-555-0178)
4. CTO — Jonathan Mercer (notified by VP Engineering within 15 min of P0)
5. CEO — Michelle Watanabe (notified by CTO if outage exceeds 1 hour or affects major customer)

**P1 Escalation Chain:**
1. On-Call Engineer
2. On-Call Engineering Manager (notified, not auto-paged)
3. VP Engineering (notified within 30 minutes if P1 persists > 2 hours)

**P2 and below:**
1. On-Call Engineer manages independently
2. Engineering Manager notified if customer has escalated to VP level

---

## 4. On-Call Structure

### 4.1 On-Call Teams

NovaTech maintains three on-call rotations:

| Team | Responsibility | Rotation | PagerDuty Schedule |
|------|---------------|----------|-------------------|
| Platform | Auth, User Management, Billing, Admin, Infrastructure | Weekly | `PD-Platform-Primary` |
| Product | Document Service, Notification, Integration, Workflow | Weekly | `PD-Product-Primary` |
| Data | Search, Analytics, AI Service, Elasticsearch, Kafka | Weekly | `PD-Data-Primary` |

### 4.2 On-Call Expectations
- Primary on-call must acknowledge pages within **5 minutes** at all hours
- Secondary on-call must acknowledge within **10 minutes** if primary does not respond
- On-call engineers must be within cell/data coverage for the duration of their shift
- Maximum consecutive on-call weeks: 2 (prevents burnout)
- On-call compensation: $200/week standby + $75/incident response outside business hours
- On-call schedule published via `/c/Users/Dell/OneDrive/Desktop/Agentic_rag/docs/engineering/On_Call_Schedule_Q2_2026.csv`

### 4.3 On-Call Handoff
Each on-call shift ends Sunday at 5:00 PM PT. The outgoing on-call must:
1. Post a handoff summary in `#oncall-handoff` Slack channel
2. List any ongoing incidents, open P2+ issues, and context needed
3. Confirm the incoming engineer has acknowledged the handoff

---

## 5. Incident Response Process

### 5.1 Phase 1: Detection and Declaration (0–10 minutes)

**Automated Detection Sources:**
- Datadog monitors (500+ active monitors across all services)
- Synthetic checks (Datadog Synthetics — 5-minute interval from 3 regions)
- Customer reports (via support ticket tagged "incident")
- Internal reports (Slack #prod-issues channel)

**Manual Declaration:**
Any engineer may declare an incident. To declare:
1. Post in `#incidents` Slack channel: `/incident declare P[0-3] [brief description]`
2. This auto-creates the incident Slack channel (e.g., `#inc-20260310-search-degradation`)
3. PagerDuty is notified and escalation begins

### 5.2 Phase 2: Mobilization (10–20 minutes)

Upon incident declaration, the first senior engineer on the call becomes the **Incident Commander (IC)**. The IC responsibilities are:

- Own the incident channel; pin the incident status message
- Assign roles: Communications Lead, Technical Lead
- Ensure the status page is updated (StatusPage.io — `status.novatech.io`)
- Coordinate investigation across service teams
- **Do not deep-dive technically** — delegate debugging to Technical Lead
- Drive toward resolution, not toward finding the root cause (RCA comes later)
- Make escalation decisions
- Approve all external communications

### 5.3 Phase 3: Investigation and Mitigation

**Investigation Toolkit:**
- **Datadog:** Primary observability. Dashboards: `NOV-01 Platform Overview`, `NOV-07 Service SLOs`, `NOV-12 Customer Impact`
- **Datadog APM:** Distributed traces for request-level debugging
- **Elasticsearch Kibana:** Log search and aggregation (`https://kibana.novatech.internal`)
- **AWS Console / CLI:** Infrastructure-level diagnostics (requires MFA, logged)
- **PagerDuty:** Incident timeline and communication
- **StatusPage:** Customer-facing status updates

**Common Investigation Steps by Component:**

*Search Service Degradation:*
```bash
# Check Elasticsearch cluster health
curl -s https://elasticsearch.novatech.internal/_cluster/health | jq

# Check index status for affected tenant
curl -s "https://elasticsearch.novatech.internal/novatech-{tenant_id}-documents-*/_stats"

# Check Search Service pod logs
kubectl logs -l app=search-service -n novatech-prod --tail=200 -f

# Check Redis cache hit rate
kubectl exec -it redis-cluster-0 -n novatech-infra -- redis-cli info stats | grep hit
```

*Authentication Failures:*
```bash
# Check Auth Service logs
kubectl logs -l app=auth-service -n novatech-prod --tail=200

# Check JWT signing key rotation status
aws secretsmanager describe-secret --secret-id novatech/auth/jwt-private-key

# Check JWKS endpoint response
curl https://api.novatech.io/.well-known/jwks.json
```

### 5.4 Phase 4: Resolution and Recovery

When the immediate issue is resolved:
1. Verify resolution with Datadog monitors returning to green
2. Run smoke test suite: `make smoke-test ENV=production`
3. Confirm affected customers are able to use the platform
4. Update status page to "Resolved"
5. Send resolution communication (see Section 6)
6. Post incident summary in `#incidents` Slack

### 5.5 Lightweight Process for P3/P4

P3 and P4 incidents do not require an Incident Commander. The on-call engineer:
1. Creates a Jira ticket (P3 label)
2. Posts in `#prod-issues` Slack
3. Resolves within SLA (P3: 7 days, P4: 30 days)
4. No status page update required unless customer-visible

---

## 6. Communication Templates

### 6.1 Incident Channel Opening Message (Slack)

```
🚨 INCIDENT DECLARED: P[severity] — [Brief Title]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IC: @[name]
Tech Lead: @[name]  
Comms Lead: @[name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Status: INVESTIGATING
Started: [timestamp PT]
Customer Impact: [TBD / description]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
StatusPage updated: [yes/no]
Next update: In 15 minutes
```

### 6.2 Customer Status Page — Investigating

```
[Service Name] Degradation — Investigating
We are aware of an issue affecting [feature/service] and our team is actively investigating. 
We will provide an update within 30 minutes. We apologize for the inconvenience.

Impact: [describe customer impact]
Started: [time] PT
Components affected: [list]
```

### 6.3 Customer Status Page — Identified

```
[Service Name] Degradation — Identified
We have identified the root cause of the issue affecting [feature/service] and are working 
on a fix. We expect resolution by [estimated time] PT.

Impact: [describe]
Next update: [time] PT
```

### 6.4 Customer Status Page — Resolved

```
[Service Name] Degradation — Resolved
The issue affecting [feature/service] has been resolved as of [time] PT. All systems are 
operating normally.

Duration: [X hours Y minutes]
Root cause: [brief non-technical summary]
We sincerely apologize for the disruption to your workflow. A full post-incident report 
will be published within 5 business days.
```

### 6.5 Executive Update Template (Slack DM to VP Eng + CTO)

```
⚠️ P[severity] Incident Update — [time]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary: [2-3 sentences: what's broken, who's impacted]
Customer Impact: [named accounts if applicable]
Time in Incident: [X hours Y minutes]
Current Status: [Investigating / Identified / Fixing]
ETA to Resolution: [time or Unknown]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Actions Taken: [bullet list]
Next Steps: [bullet list]
IC: [name] | Tech Lead: [name]
```

### 6.6 Enterprise Customer Direct Communication (P0/P1)

For Enterprise accounts directly impacted, the CSM or Account Executive sends:

```
Subject: [URGENT] NovaTech Service Issue — [Customer Name]

Hi [Contact Name],

I'm writing to personally inform you that we are currently experiencing a service issue 
that is affecting your NovaTech platform access.

Issue: [brief description]
Started: [time] PT
Current Status: Actively investigating / Fix in progress
Expected Resolution: [time or "We will update you within 1 hour"]

Our engineering team is fully engaged on this issue as our top priority. I will personally 
update you every [30/60] minutes until this is resolved.

You can monitor our real-time status at status.novatech.io.

I sincerely apologize for the disruption. Please don't hesitate to call me directly at 
[CSM phone number].

[Name]
Customer Success Manager, NovaTech Solutions
```

---

## 7. Post-Incident Review (Postmortem) Process

### 7.1 Postmortem Requirements

| Severity | Postmortem Required | Due Date | Distribution |
|----------|--------------------|---------:|-------------|
| P0 | Always | Within 5 business days | All of Engineering + Leadership |
| P1 | Always | Within 5 business days | Engineering team + managers |
| P2 | If SLA breached or customer escalation | Within 7 business days | Engineering team |
| P3 | Optional (at team's discretion) | Within 14 days | Team only |

### 7.2 Postmortem Document Structure

Each postmortem must include:

1. **Incident Summary:** Date, duration, severity, services affected, customer impact
2. **Timeline:** Minute-by-minute timeline from first alert to resolution
3. **Root Cause Analysis:** 5-why analysis; technical root cause; contributing factors
4. **Customer Impact:** Quantified (requests failed, tenants affected, SLA breach calculation)
5. **What Went Well:** Honest assessment of effective response actions
6. **What Went Wrong:** Honest assessment of gaps in detection, response, or tooling
7. **Action Items:** Specific, assigned, time-bound tasks to prevent recurrence
8. **SLA Breach Calculation:** If applicable (see Section 8)

### 7.3 Blameless Culture

NovaTech follows a **blameless postmortem culture** based on the principle that:

> *"Given the same information, tools, and pressures, any engineer would have made the same decisions. The system created the conditions for failure, not the individual."*

**In postmortems:**
- Individual names are used only to identify owners of action items, not to assign blame
- "Mistakes" are reframed as "decision points" — what information was available and what led to the decision?
- Language like "engineer X should have known" is prohibited
- All action items target systemic improvements: better monitoring, documentation, tooling, or process

**IC responsibility:** Shut down blame-oriented discussion in the postmortem meeting immediately.

---

## 8. SLA Breach Calculation

### 8.1 Monthly Uptime Calculation

```
Uptime % = ((Total minutes in month - Downtime minutes) / Total minutes in month) × 100

Example (March 2026, 31 days = 44,640 minutes):
Downtime: 45 minutes
Uptime % = ((44,640 - 45) / 44,640) × 100 = 99.899%

Standard SLA: 99.9% → BREACHED (barely)
Enterprise SLA: 99.95% → BREACHED
```

### 8.2 What Counts as Downtime

**Counts:**
- Platform returning >5% error rate for core features (auth, search, document upload) for >5 consecutive minutes
- Response times exceeding 30 seconds on any core endpoint
- Complete service unavailability

**Does NOT Count:**
- Planned maintenance windows (announced 2 weeks in advance, max 2 hours, Sunday 2–4am PT)
- Customer-caused issues (incorrect API usage, customer network issues)
- Issues with third-party services outside NovaTech's control
- Alpha/beta features explicitly labeled as not covered by SLA

### 8.3 SLA Credit Schedule

| Monthly Uptime | Credit (% of monthly fee) |
|---------------|--------------------------|
| 99.0% – 99.89% | 10% |
| 95.0% – 98.99% | 25% |
| < 95.0% | 50% |

Credit requests must be submitted within 30 days of the incident. Credits are applied to the next invoice.

---

## 9. Customer Notification Thresholds

| Condition | Action | Owner |
|-----------|--------|-------|
| Any P0 | Auto-update status page | IC (Comms Lead) |
| P0 > 15 min | Direct email to all Enterprise customers | CSM team |
| P0 affecting named account | Direct call/SMS to account contact | Account Executive + CSM |
| P1 > 30 min | Update status page | IC (Comms Lead) |
| P1 affecting Enterprise customer | Direct email to affected customer | CSM |
| P2 affecting named Enterprise account | Proactive ticket update | Support Engineer |
| Any P0/P1 resolved | Send resolution communication + offer postmortem | CSM + Engineering |

---

## 10. Tools and Access

| Tool | Purpose | Access |
|------|---------|--------|
| PagerDuty | Alerting and on-call management | All engineers via SSO |
| Datadog | Monitoring, APM, logging | All engineers via SSO |
| StatusPage.io | Customer-facing status page | IC and Comms Lead |
| AWS Console | Infrastructure investigation | Via break-glass (see Security policy) |
| Kibana | Log search and visualization | All engineers via SSO |
| GitHub | Code review, hotfix deployment | All engineers |
| Slack #incidents | Incident coordination | All engineering staff |
| Zoom | War room calls (P0/P1) | All engineering staff |

---

*This playbook is maintained by the SRE team. For questions, reach out in #sre-team on Slack. For emergency amendments, contact Kevin Osei directly.*
