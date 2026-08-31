# NovaTech Solutions — SLA and Uptime Guidelines

**Document Version:** 2.2  
**Last Updated:** January 5, 2026  
**Authors:** Jennifer Osei (Head of Customer Support), Legal Team, Kevin Osei (SRE Lead)  
**Classification:** Internal — Customer Success + Engineering + Legal  
**Review Cycle:** Annual (or upon significant architecture change)

---

## 1. Overview

This document defines NovaTech Solutions' Service Level Agreement (SLA) commitments, uptime measurement methodology, planned maintenance policies, credit schedules, and current SLA performance. It supplements the customer Master Service Agreement (MSA) and Order Form.

---

## 2. Uptime Commitments by Plan Tier

| Plan Tier | Monthly Uptime Commitment | Max Downtime per Month | Max Downtime per Year |
|-----------|--------------------------|----------------------|----------------------|
| Free | 99.0% | 7 hours 18 minutes | 87.6 hours |
| Standard | 99.5% | 3 hours 39 minutes | 43.8 hours |
| Professional | 99.9% | 43 minutes 49 seconds | 8.7 hours |
| Enterprise | 99.95% | 21 minutes 54 seconds | 4.4 hours |
| Enterprise+ (custom) | 99.99% (negotiated) | 4 minutes 22 seconds | 52 minutes |

**Note:** Uptime is measured per calendar month. A 31-day month has 44,640 minutes; a 28-day month has 40,320 minutes.

**Example Calculations:**
```
Enterprise SLA (99.95%):
March 2026 (31 days = 44,640 minutes):
Allowed downtime = 44,640 × (1 - 0.9995) = 22.3 minutes

Professional SLA (99.9%):
March 2026 (31 days = 44,640 minutes):
Allowed downtime = 44,640 × (1 - 0.999) = 44.6 minutes
```

---

## 3. What Constitutes Downtime

### 3.1 Covered (Counts Against SLA)

| Condition | Measurement |
|-----------|------------|
| Platform returning HTTP 5xx error rate > 5% on core endpoints for > 5 consecutive minutes | Continuous monitoring |
| Core feature (authentication, document search, document upload) returning errors for > 10% of requests | API error rate monitors |
| Response times on core endpoints exceeding 30 seconds for > 5 consecutive minutes | Latency monitors |
| Database unavailability causing user-facing errors | Dependency health checks |

**Core Endpoints:**
- `POST /v2/auth/token` (Authentication)
- `GET /v2/documents` (Document listing)
- `POST /v2/documents` (Document upload)
- `GET /v2/search` (Document search)
- `GET /v2/users` (User management)

### 3.2 Not Covered (Does NOT Count Against SLA)

| Exclusion | Rationale |
|-----------|----------|
| Planned maintenance windows (see Section 5) | Customer notified in advance; can plan around |
| Issues caused by customer's own infrastructure, network, or misconfiguration | Outside NovaTech's control |
| Third-party service outages (e.g., AWS regional outage, SendGrid email delivery) | Force majeure / dependency |
| Issues caused by customer-initiated API misuse (e.g., sending malformed requests) | Customer-caused |
| Alpha or beta features explicitly labeled as not SLA-covered | Documented at time of access grant |
| Free plan | Not included in paid SLA |
| Issues during DR failover testing (scheduled and announced) | Planned operational activity |

---

## 4. Uptime Measurement Methodology

### 4.1 Monitoring Infrastructure

NovaTech measures uptime using:

1. **Datadog Synthetic Monitors:** Automated checks run every **5 minutes** from **3 geographic regions**:
   - `us-east-1` (Virginia) — primary
   - `eu-west-1` (Ireland) — EMEA customers
   - `ap-southeast-1` (Singapore) — APAC customers

2. **Check endpoints:**
   - Authentication endpoint (`POST /v2/auth/token`)
   - Search endpoint (`GET /v2/search?q=healthcheck`)
   - Document list endpoint (`GET /v2/documents?limit=1`)
   - Health endpoint (`GET /health`)

3. **Incident confirmed when:** 2 of 3 geographic monitors fail simultaneously for 2 consecutive check intervals (10 minutes)

4. **Incident resolved when:** All 3 geographic monitors pass for 2 consecutive check intervals

### 4.2 Status Page

Real-time status and historical uptime data are published at:
**`https://status.novatech.io`** (powered by StatusPage.io)

Customers can subscribe to status page notifications (email, SMS, webhook, RSS) at no charge.

**Historical uptime reports** (monthly, by component) are available at:
`https://status.novatech.io/history`

### 4.3 SLA Uptime Report

Monthly SLA uptime reports are automatically generated and:
- Emailed to billing contacts of Professional and Enterprise accounts on the 5th of each month
- Available on request via support ticket
- Maintained in internal BI dashboard (Metabase) for CSM reference

---

## 5. Planned Maintenance Windows

### 5.1 Standard Maintenance Window

| Day | Time | Duration | Notice Required |
|-----|------|---------|----------------|
| **Sunday** | 2:00 AM – 4:00 AM PT | Up to 2 hours | 14 calendar days minimum |

Maintenance during this window does **not** count against SLA uptime.

### 5.2 Emergency Maintenance

In rare cases where a security vulnerability or critical system issue requires immediate maintenance outside the standard window:
- Minimum 4-hour notice via email and StatusPage
- Emergency maintenance does **not** count against SLA (unless notification period is not met)
- Customer Success team proactively contacts Enterprise customers

### 5.3 Maintenance Notification Process

1. **14 days before:** Email notification to all billing contacts + in-app banner
2. **48 hours before:** Reminder email notification
3. **1 hour before:** StatusPage scheduled maintenance begins (visible on status.novatech.io)
4. **Start of maintenance:** StatusPage status set to "Under Maintenance"
5. **End of maintenance:** StatusPage updated to "Operational"; recovery email sent

**2026 Planned Maintenance Schedule:**

| Date | Window | Duration | Systems |
|------|--------|---------|---------|
| January 19, 2026 | 2:00–3:30 AM PT | 90 min | Elasticsearch 8.12 upgrade |
| February 16, 2026 | 2:00–2:45 AM PT | 45 min | Database certificate rotation |
| March 15, 2026 | 2:00–4:00 AM PT | 2 hours | RDS PostgreSQL 15.4 minor upgrade; Kafka 3.6 upgrade |
| April 19, 2026 | 2:00–3:00 AM PT | 60 min | Security patch deployment |
| May 17, 2026 | 2:00–3:30 AM PT | 90 min | Infrastructure: EKS 1.30 upgrade |
| June 21, 2026 | 2:00–2:30 AM PT | 30 min | TLS certificate rotation |

---

## 6. SLA Credit Schedule

### 6.1 Credit Amounts

| Monthly Uptime Achieved | Credit (% of Monthly Fee) |
|------------------------|--------------------------|
| 99.9% – 99.94% (Enterprise only breach) | 10% |
| 99.0% – 99.89% (Professional breach) | 10% |
| 95.0% – 98.99% | 25% |
| 90.0% – 94.99% | 40% |
| Below 90.0% | 50% |

**Maximum credit per month:** 50% of monthly fee. Credits are non-refundable and must be applied within 12 months.

### 6.2 Credit Request Process

1. **Submit via:** Support ticket tagged `SLA Credit Request` at support.novatech.io
2. **Deadline:** Within **30 calendar days** of the incident month end
3. **Required information:** Incident date(s), approximate downtime duration, affected services, ticket number(s)
4. **Processing time:** 10 business days
5. **Review by:** Finance team + Head of Customer Support
6. **Application:** Credits applied to the next invoice; or to account balance

### 6.3 Proactive Credit Policy (Enterprise)

For Enterprise accounts ($100K+ ARR), NovaTech proactively calculates and issues SLA credits without requiring a customer request, if a confirmed SLA breach is documented in our monitoring systems. The credit is calculated and communicated to the CSM within 5 business days of the incident month close.

---

## 7. Current Month SLA Scorecard (March 2026)

*As of March 19, 2026 (month not yet complete)*

| Component | Uptime % | Status | Notes |
|-----------|---------|--------|-------|
| Authentication Service | 100.00% | Green | No incidents |
| Document Service | 99.98% | Green | 9-minute degradation March 3 (ENG-2867 related) |
| **Search Service** | **99.61%** | **Yellow** | Performance degradation ongoing — large tenant impact |
| Notification Service | 99.97% | Green | 13-minute delay March 8 (DST timezone bug) |
| Analytics Service | 100.00% | Green | No incidents |
| AI Service | 99.89% | Green | Within SLA (lower tier SLA for AI) |
| **Overall Platform** | **99.71%** | **Yellow** | Driven by search degradation |

**March SLA Status (as of March 19):**
- Standard (99.5% target): **MET** (99.71%)
- Professional (99.9% target): **At Risk** (99.71% — 86 minutes downtime; 44 minutes allowed)
- Enterprise (99.95% target): **BREACHED** (99.71% — 86 minutes downtime; 22 minutes allowed)

**Note on Search Degradation:**
The search performance issue (ENG-2847) is classified as performance degradation (not complete unavailability) for most customers. For ACME Corp and Pinnacle Systems, the 8–12 second response times exceed our "response time > 30 seconds" threshold intermittently but not consistently. SLA credit assessment is in progress and will be communicated to affected Enterprise customers by April 5, 2026.

---

## 8. Historical SLA Performance

| Month | Standard (target 99.5%) | Professional (target 99.9%) | Enterprise (target 99.95%) |
|-------|----------------------|--------------------------|--------------------------|
| January 2026 | 99.98% ✓ | 99.98% ✓ | 99.98% ✓ |
| February 2026 | 99.94% ✓ | 99.94% ✓ | 99.94% ✓ |
| December 2025 | 99.99% ✓ | 99.99% ✓ | 99.99% ✓ |
| November 2025 | 99.97% ✓ | 99.97% ✓ | 99.97% ✓ |
| October 2025 | 99.95% ✓ | 99.95% ✓ | 99.95% ✓ |
| September 2025 | 99.89% ✓ | 99.89% ✗ BREACH | 99.89% ✗ BREACH |
| August 2025 | 99.96% ✓ | 99.96% ✓ | 99.96% ✓ |

**September 2025 Breach:** RDS failover event caused 64 minutes of degradation. SLA credits were issued to all affected Professional and Enterprise accounts (10% of September fees). Total credits issued: $34,200.

---

*This document is maintained by the Head of Customer Support and SRE Lead. For questions, contact Jennifer Osei or reference the customer MSA for contractual terms.*
