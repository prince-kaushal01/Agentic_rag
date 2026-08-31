# NovaTech Solutions — Security Incident Response Policy
**Document Version:** 2.2
**Owner:** Tom Bradley, CISO & VP of Infrastructure
**Co-Owner:** Amanda Hartley, General Counsel
**Approved By:** David Huang, CEO
**Approval Date:** January 20, 2026
**Last Tested:** December 11, 2025 (Tabletop Exercise — Ransomware Scenario)
**Review Cycle:** Annual (or after any declared security incident)
**Classification:** Confidential

---

## 1. Purpose and Scope

This Security Incident Response Policy (SIRP) establishes NovaTech Solutions's procedures for detecting, classifying, responding to, and recovering from security incidents. It covers all types of security events that may affect NovaTech employees, systems, customers, or data.

**This policy applies to:**
- All NovaTech employees, contractors, and temporary workers
- All NovaTech-owned or company-managed systems, networks, and devices
- All third-party vendors with access to NovaTech systems or customer data

**This policy does NOT replace the Engineering Incident Response runbook** (for production system outages not involving security). For platform availability incidents, see the Engineering On-Call Runbook (Confluence > Engineering > On-Call).

---

## 2. Incident Classification

### Severity Level 1 — Critical (P1)
**Definition:** Confirmed or suspected unauthorized access to customer data; active ransomware or destructive malware; complete compromise of a core production system; confirmed insider threat with data exfiltration.

**Examples:**
- Ransomware encrypting production database servers
- Unauthorized access to the NovaTech customer search index or customer data store
- Admin credentials compromised and used to access production systems
- Confirmed data exfiltration (any customer or employee PII)

**Response Time Target:** Incident Commander on call within 15 minutes; full response team assembled within 1 hour.

**Notification:** CEO notified immediately; Board Chair notified if incident duration >4 hours or data breach confirmed.

---

### Severity Level 2 — High (P2)
**Definition:** Suspected (not confirmed) unauthorized access; successful phishing attack resulting in account compromise; active malware detected and contained but not confirmed eradicated; internal policy violation with data exfiltration potential.

**Examples:**
- Employee falls for phishing attack; credentials used to access email or Slack
- Malware detected on an employee endpoint (CrowdStrike alert); device isolated
- Unauthorized access to internal systems (non-production); no customer data accessed
- Suspected but unconfirmed access to customer data

**Response Time Target:** Initial response within 1 hour; full team within 4 hours.

**Notification:** CISO + Legal notified immediately; CEO briefed within 2 hours.

---

### Severity Level 3 — Medium (P3)
**Definition:** Security policy violations without evidence of data exposure; failed unauthorized access attempts; phishing attempts that did not succeed; vulnerability discoveries requiring prompt remediation.

**Examples:**
- Employee reports suspected phishing email (not clicked)
- Failed brute-force login attempts on admin accounts (automated alerts)
- Discovery of an unpatched critical CVE in production software
- Unauthorized device found connected to office network

**Response Time Target:** Initial investigation within 4 hours; resolution plan within 24 hours.

---

### Severity Level 4 — Low (P4)
**Definition:** Minor policy violations, low-risk security observations, routine security hygiene findings.

**Examples:**
- Employee fails security awareness training quiz
- Expired SSL certificate (non-production)
- Lost badge or device (no sensitive data, properly encrypted)
- Minor misconfiguration with no access impact

**Response Time Target:** Acknowledged within 24 hours; resolved within 7 days.

---

## 3. Detection Sources

Security incidents at NovaTech may be detected through the following channels:

| Source | Owner | Alert Mechanism |
|---|---|---|
| SIEM (Splunk) | Tom Bradley's team | Automated alerts → PagerDuty |
| Endpoint Detection (CrowdStrike Falcon) | Tom Bradley | Automated alerts → PagerDuty + Slack #security-alerts |
| Email Security (Google Workspace Advanced Protection) | Tom Bradley | Alert email + console |
| Phishing simulation platform (KnowBe4) | Tom Bradley | Monthly reports; simulated failures |
| Employee reports | All employees | Via security@novatech.io or Slack #report-security |
| Vendor notifications | Tom Bradley / Vendor owner | Email/phone per vendor notification SLA |
| Bug bounty program (HackerOne) | Tom Bradley | HackerOne platform notifications |
| Penetration test findings | Tom Bradley | Quarterly pentest report (vendor: Cobalt) |
| Customer or partner reports | Janet Okonkwo (CS) → Tom Bradley | Email or Slack; CS team trained to escalate |

**Employee Reporting:** All employees are trained to report suspected incidents to **security@novatech.io** or Slack **#report-security** immediately. Employees who report incidents in good faith will not face retaliation, even if the reported event turns out to be non-malicious.

---

## 4. Incident Response Team

### Core Incident Response Team (CIRT)

| Role | Primary | Backup | Responsibility |
|---|---|---|---|
| Incident Commander | Tom Bradley (CISO) | Marcus Webb (CTO) | Overall coordination; escalation decisions |
| Technical Lead | Marcus Webb (CTO) | Jennifer Yao (VP Eng) | System investigation; containment; remediation |
| Legal Lead | Amanda Hartley (General Counsel) | External: Fenwick & West (415-555-0900) | Legal obligations; evidence preservation; regulatory notifications |
| Communications Lead | Rachel Torres (VP Marketing) | Jennifer Walsh (VP Ops) | Internal/external communications; customer notifications |
| Customer Success Lead | Janet Okonkwo (VP CS) | CS Manager on rotation | Named customer notification; customer liaison |
| Executive Sponsor | David Huang (CEO) | Carlos Ramirez (CFO) | Board notification; regulatory escalation; media response |
| Cyber Insurance Contact | Tom Bradley | Carlos Ramirez | AXA XL engagement; claim initiation |

**Activation:** The Incident Commander activates the full CIRT for P1 and P2 incidents. P3 incidents are managed by the Technical Lead (Tom Bradley's team) with CISO oversight.

---

## 5. Incident Response Procedure

### Phase 1 — Detection & Initial Triage (0–60 minutes)

**1.1 Receive and Log**
- All security alerts from automated systems and employee reports are logged in PagerDuty.
- The on-call security analyst (rotating weekly; see PagerDuty schedule) is responsible for initial triage.
- Initial log must capture: time of detection, source of detection, system(s) affected, preliminary classification (P1–P4).

**1.2 Initial Assessment**
- On-call analyst assesses the alert: Is this a true positive or false positive?
- False positives: documented in Splunk and closed. Pattern analyzed to reduce future false positives.
- True positives or uncertain: Escalate to CISO (Tom Bradley) immediately.

**1.3 Severity Classification**
- CISO confirms severity classification (P1–P4) based on the classification criteria in Section 2.
- P1/P2: Activate CIRT; initiate war room in #incidents-sec Slack channel (private channel).
- P3/P4: CISO manages with security team; log in Jira Security project.

---

### Phase 2 — Containment (1–4 hours for P1; 4–24 hours for P2)

**2.1 Short-term Containment**
Goal: Stop the bleeding. Prevent further spread or data access without destroying evidence.

Actions (as appropriate to the incident type):
- Isolate affected systems from the network (CrowdStrike network containment; AWS security group changes)
- Disable compromised user accounts (Okta: immediate suspension)
- Block malicious IPs at Cloudflare WAF and AWS security groups
- Revoke compromised API keys or certificates
- Preserve volatile evidence (memory snapshots, log captures) BEFORE reimaging

**2.2 Evidence Preservation**
- Do NOT wipe or reimage affected systems until forensic images are taken (AWS: create EBS snapshots; endpoints: CrowdStrike full disk collection).
- All system logs from affected time window must be preserved in Splunk (extended retention enabled immediately).
- Amanda Hartley (Legal) advises on evidence hold requirements.
- Forensic work is documented in the incident timeline (Confluence: Security > Incident Records > [Incident ID]).

**2.3 Long-term Containment**
- Remove malware; patch exploited vulnerabilities; close attacker persistence mechanisms.
- Rotate all credentials (passwords, API keys, certificates) that may have been exposed.
- Implement enhanced monitoring on recovered systems before restoration.

---

### Phase 3 — Investigation (During/After Containment)

**3.1 Root Cause Analysis**
- Technical Lead leads investigation with engineering team
- Key questions: How did the attacker gain access? What did they access or exfiltrate? Is there persistent access remaining?
- Investigation timeline documented in the incident record
- External forensics firm engaged for P1 incidents: Mandiant (primary contact: Sandra Webb, 415-555-1212)

**3.2 Impact Assessment**
- Identify all systems accessed by the attacker
- Determine whether customer data was accessed or exfiltrated
- Determine whether employee PII was accessed
- If data accessed: Legal (Amanda Hartley) leads regulatory notification analysis

---

### Phase 4 — Notification and Communication

#### 4.1 Internal Communication
- P1/P2 incidents: CEO and executive team notified within 2 hours
- P1 incidents lasting >4 hours: Board Chair (Linda Chen) notified by CEO
- All internal communications on P1/P2 incidents flow through the #incidents-sec private Slack channel; avoid email during active incidents (email may be compromised)

#### 4.2 Customer Notification Thresholds

| Situation | Notification Required | Timing |
|---|---|---|
| Customer data confirmed accessed by unauthorized party | Yes — mandatory | As soon as confirmed; target within 48 hours |
| Customer data potentially accessed (unconfirmed) | Discretionary — consult Legal | Legal determines within 24 hours of knowledge |
| NovaTech internal systems only; no customer data | No (unless contractually required) | N/A |
| Vendor breach that may have exposed customer data | Yes — mandatory (if customer data involved) | Per notification obligation analysis |

**Notification process:**
- Janet Okonkwo (VP CS) leads customer notification for named/enterprise accounts (ACME Corp, GlobalTech Inc, Meridian Enterprises, Pinnacle Systems, SkyBridge Ltd)
- Customer notification sent by the assigned CSM for each named account, not by an automated email blast, to ensure personal accountability
- Template: See Appendix A (Customer Breach Notification Template)

#### 4.3 Regulatory Reporting Obligations

| Regulation | Obligation | Deadline | Lead |
|---|---|---|---|
| GDPR (EU/UK) | Notify relevant Data Protection Authority (DPA) | Within 72 hours of becoming aware of a personal data breach | Amanda Hartley |
| CCPA/CPRA (California) | Notify affected CA residents | In the most expedient time possible; no specific timeframe | Amanda Hartley |
| State breach notification laws (all 50 states) | Notify affected individuals | Varies by state (30–90 days typical) | Amanda Hartley |
| Cyber insurance | Notify AXA XL of P1 incidents | Within 30 days of discovery; immediate notification recommended | Tom Bradley |

**GDPR 72-Hour Rule:** NovaTech's internal target is notification to the relevant DPA within **48 hours** of confirmed breach to allow buffer for preparation. Amanda Hartley manages all DPA communications. GDPR notification goes to the Irish Data Protection Commission (NovaTech's EU-designated lead supervisory authority).

#### 4.4 Media / Public Relations
- All media inquiries related to a security incident are routed to Rachel Torres (Communications Lead)
- No employee other than the CEO or General Counsel may speak to press about a security incident
- Holding statement template available from Vantage PR (PR agency); pre-approved by Legal

---

### Phase 5 — Recovery

- Affected systems restored from clean backups after forensic preservation
- Restored systems undergo enhanced security scanning before returning to production
- Monitoring increased on recovered systems for 30 days post-incident
- Customer-facing systems restored according to the priority order in the BCP

---

### Phase 6 — Post-Incident Review

**Mandatory for P1 and P2 incidents:**
- Post-incident review meeting held within 5 business days of incident closure
- Attendees: Full CIRT + affected team leads
- Post-incident report produced within 10 business days (Confluence template: Security > Post-Incident Reports)
- Post-incident report covers: timeline, root cause, impact, remediation actions, lessons learned, preventive measures
- Action items tracked in Jira; assigned owners; 30-day completion target

**Lessons Learned Database:** All post-incident reports are stored and cross-referenced. Recurring patterns trigger policy updates.

---

## 6. Cyber Insurance Claim Process

NovaTech's cyber insurance policy is with AXA XL (Policy: CYB-2024-NT-8821; $10M coverage).

**Steps to initiate a claim (P1 incidents):**
1. Tom Bradley notifies AXA XL cyber hotline within 24 hours of confirmed incident: 1-800-555-4200
2. AXA XL assigns a claims adjuster and may dispatch their approved forensics panel (we may also use Mandiant with AXA approval)
3. Carlos Ramirez coordinates financial documentation of losses (business interruption, remediation costs)
4. Amanda Hartley reviews all insurance communications for legal implications
5. NovaTech must preserve all evidence and documentation per AXA XL requirements — do not destroy or overwrite any potentially relevant evidence before notifying insurer

**Broker:** Newfront Insurance — Derek Hartman (derek.hartman@newfront.com; 415-555-0712)

---

## 7. Specific Incident Type Procedures

### 7.1 Phishing / Account Compromise
1. Employee reports suspicious email → security@novatech.io
2. Security team analyzes email headers and links in isolated sandbox
3. If credential capture confirmed: immediately suspend affected Okta account; force password reset for all accounts; check for MFA bypass
4. Review audit logs in Google Workspace, Slack, Salesforce for unauthorized access
5. Check for mail forwarding rules, OAuth app grants, or other persistence mechanisms
6. If credentials used: escalate to P2; initiate full investigation

### 7.2 Malware / Ransomware
1. CrowdStrike auto-contains infected endpoint (network isolation)
2. Security team reviews CrowdStrike console for lateral movement or additional compromised systems
3. Do NOT pay any ransom without CEO + Board + Legal approval; NovaTech's policy is to not pay ransoms as a general position, subject to legal advice in specific circumstances
4. Assess whether production systems are affected; if yes: escalate to P1, activate BCP
5. Restore from clean backups (see BCP, Section 5)

### 7.3 Unauthorized Physical Access
1. Cassandra Baines (Facilities) notified; reviews Brivo access logs
2. Building security management notified
3. If sensitive area accessed (server room, executive area): Incident Commander notified; physical evidence preserved
4. Review whether any equipment was accessed, modified, or removed

### 7.4 Vendor Data Breach (NovaTech data held by vendor)
1. Vendor notifies NovaTech per contractual notification obligation
2. Tom Bradley leads assessment: Was NovaTech or customer data exposed?
3. If NovaTech customer data exposed: treat as P1; follow customer notification process
4. If employee PII exposed: treat as P2; notify employees per applicable law
5. Review vendor contract for breach indemnification rights; engage Legal

---

## 8. Security Training and Awareness

- **Annual security training:** All employees complete mandatory security awareness training (KnowBe4) within 30 days of hire and annually thereafter. Completion tracked in Rippling.
- **Phishing simulations:** Monthly simulated phishing campaigns via KnowBe4. Employees who click receive additional remediation training within 24 hours.
- **Incident response training:** CIRT members participate in at least one tabletop exercise per year.
- **Security@novatech.io awareness:** All new hires trained on this channel during IT onboarding.

---

*Owner: Tom Bradley, CISO | tom.bradley@novatech.io*
*Co-Owner: Amanda Hartley, General Counsel | amanda.hartley@novatech.io*
*Approved: David Huang, CEO*
*Version 2.2 — January 20, 2026*
*Next review: January 2027 or following any P1 incident*
