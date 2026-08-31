# NovaTech Solutions — Compliance and Regulatory Checklist

**Document Owner:** Legal Department / Security Team  
**Document Number:** LEGAL-COMP-001  
**Effective Date:** January 1, 2026  
**Last Updated:** January 10, 2026  
**Next Review:** June 30, 2026  
**Approved By:** David Park, General Counsel; Marcus Webb, CTO; Dr. Nina Bhatt, DPO  
**Classification:** Internal — Leadership and Compliance Team Only  

---

## Executive Summary

This Compliance and Regulatory Checklist provides NovaTech Solutions' current status across all major regulatory frameworks, security certifications, and compliance obligations. The document serves as the primary reference for the executive team, Board of Directors, customer due diligence inquiries, and internal audit purposes.

**Overall Compliance Health: GOOD** (as of January 10, 2026)

| Framework | Status | Next Action | Due Date |
|---|---|---|---|
| SOC 2 Type II | Current | Renewal audit | September 2026 |
| GDPR | Compliant | Annual review | June 2026 |
| CCPA/CPRA | Compliant | Annual review | July 2026 |
| HIPAA | Partial (Not BAA-ready) | Roadmap Phase 2 | Q4 2026 |
| ISO 27001 | In Progress | Certification target | Q4 2026 |
| NIST CSF | Aligned (not certified) | Gap assessment refresh | March 2026 |
| Pen Testing | Current | Next test | October 2026 |
| WCAG 2.1 AA | Compliant | Audit refresh | Q2 2026 |
| Export Control | Compliant | Annual review | November 2026 |
| SOX (partial) | Investor reporting only | — | Ongoing |

---

## Section 1: SOC 2 Type II

### 1.1 Current Status

**Status: ACHIEVED AND CURRENT**

- **Current Certificate Period:** January 1, 2025 – December 31, 2025
- **Audit Firm:** Ernst & Young LLP (San Francisco office)
- **Audit Partner:** Rebecca Thornton, CPA, CISA
- **Trust Service Criteria Covered:** Security, Availability, Confidentiality
- **Opinion:** Unqualified (clean) opinion for the 2025 audit period
- **Report Classification:** Type II (operating effectiveness of controls tested over 12 months)

### 1.2 Key Findings from 2025 SOC 2 Report

- **0 Exceptions** identified in the audit period for Security criteria
- **1 Management Note** (not a deficiency): Auditors noted that NovaTech's access review process, while effective, is manual. Management is implementing automated access review in Q1 2026 (via Okta Workflows).
- **Management Response:** Automated access review target: March 31, 2026

### 1.3 Renewal Timeline (2026 Audit)

| Milestone | Target Date | Owner |
|---|---|---|
| Ernst & Young engagement confirmation | August 1, 2026 | Margaret Liu |
| Audit kickoff meeting | September 8, 2026 | Marcus Webb |
| Interim controls testing | September – October 2026 | Marcus Webb / Security Team |
| Year-end controls testing | January – February 2027 | Marcus Webb |
| Draft SOC 2 report issued | February 28, 2027 | EY |
| Final 2026 SOC 2 report | March 31, 2027 | EY |

### 1.4 Customer Access to SOC 2 Report

The SOC 2 Type II report is available to:
- Enterprise customers upon execution of an NDA (available via Vanta Trust Center at trust.novatech.io)
- Prospective enterprise customers during due diligence (Legal team approval required)

---

## Section 2: GDPR Compliance

### 2.1 Current Status

**Status: COMPLIANT**

NovaTech Solutions is subject to GDPR as a data processor for EU-based customers and as a data controller for its own employees and marketing data.

### 2.2 Key GDPR Compliance Elements

| Requirement | Status | Notes |
|---|---|---|
| Data Protection Officer appointed | Complete | Dr. Nina Bhatt (DPO since January 2025) |
| Article 30 Records of Processing Activities (ROPA) | Complete | Updated quarterly |
| Data Processing Agreements with customers | Complete | Standard DPA available; executed with all EU customers |
| Sub-processor agreements | Complete | SCCs in place with all US sub-processors |
| Privacy Policy (GDPR-compliant) | Complete | Updated January 1, 2026 |
| Cookie consent management | Complete | OneTrust CMP deployed on novatech.io |
| Data Subject Rights procedures | Complete | 30-day response SLA; tracked in Notion |
| Breach notification procedure | Complete | 72-hour notification process documented |
| International transfer mechanisms (SCCs) | Complete | EU SCCs (2021) executed with all US processors |
| DPIA process | In place | DPIA conducted for all new high-risk processing activities |
| EU Representative (Article 27) | Complete | DataRep (Ireland) appointed January 2025 |

### 2.3 GDPR Action Items (2026)

- [ ] **Q1 2026:** Complete ROPA review and update for new product features (AI analytics module)
- [ ] **Q2 2026:** Annual GDPR training for all employees (target: April 2026)
- [ ] **Q2 2026:** Review and update SCCs for sub-processors with new 2021 SCC requirements (final deadline passed — confirm all updates complete by March 2026)
- [ ] **Q3 2026:** DPIA for new biometric/behavioral analytics feature in roadmap
- [ ] **Q4 2026:** Annual privacy audit by external counsel (Fenwick & West)

---

## Section 3: CCPA/CPRA Compliance

### 3.1 Current Status

**Status: COMPLIANT**

NovaTech is subject to the California Consumer Privacy Act (as amended by the California Privacy Rights Act) both as a business (for its marketing and HR data) and as a service provider (for customer data processed on behalf of California business customers).

### 3.2 CCPA/CPRA Compliance Elements

| Requirement | Status | Notes |
|---|---|---|
| Privacy Policy (CCPA-compliant) | Complete | Updated January 1, 2026; includes all required disclosures |
| "Do Not Sell My Personal Information" | Complete | NovaTech does not sell data; opt-out link present on website |
| Data Subject Rights (Know, Delete, Correct, Portability) | Complete | Request process via privacy@novatech.io; 45-day response |
| Service Provider Agreements | Complete | CCPA service provider clauses in customer DPAs |
| Employee Privacy Notice (CPRA) | Complete | Updated employment privacy notice effective January 2026 |
| Sensitive Personal Information handling | Complete | SPI not collected; controls in place to prevent inadvertent collection |
| Annual audit obligation | In Progress | Internal audit Q3 2026 |

---

## Section 4: HIPAA Readiness Assessment

### 4.1 Current Status

**Status: PARTIAL — NOT BAA-READY FOR PRODUCTION PHI**

NovaTech is not currently HIPAA-compliant for Business Associate Agreement (BAA) execution. Several prospective healthcare-sector customers have requested HIPAA compliance; achieving BAA readiness is a strategic objective for 2026.

### 4.2 HIPAA Readiness Gap Assessment (December 2025)

| HIPAA Requirement | Current Status | Gap | Priority |
|---|---|---|---|
| Encryption of PHI at rest and in transit | Complete | No gap | — |
| Access controls and minimum necessary | Partial | Need per-customer data isolation | High |
| Audit controls (PHI access logging) | Partial | Need granular PHI audit trail | High |
| Business Associate Agreements | Not started | Legal template needed | High |
| Security Risk Analysis | Not completed | Full HIPAA-specific risk analysis needed | High |
| Breach Notification (HIPAA rule) | Partial | 60-day HIPAA notification differs from our 72-hr GDPR process | Medium |
| Employee HIPAA Training | Not started | Training program design needed | Medium |
| Facility access controls | Partial | AWS covered; office controls need documentation | Low |
| BAA with sub-processors | Not started | AWS BAA available; need Zendesk, others | High |

### 4.3 HIPAA Roadmap

- **Q2 2026:** Engage HIPAA compliance consultant (target: Coalfire)
- **Q3 2026:** Complete HIPAA security risk analysis
- **Q3 2026:** Implement required technical controls; execute AWS BAA
- **Q4 2026:** Complete HIPAA employee training
- **Q4 2026:** Achieve BAA-ready status; execute first customer BAAs

---

## Section 5: ISO 27001 Roadmap

### 5.1 Current Status

**Status: IN PROGRESS — TARGET Q4 2026**

NovaTech's security posture is substantially aligned with ISO 27001 requirements, as evidenced by the clean SOC 2 Type II opinion. Formal ISO 27001 certification is a strategic objective for 2026, driven by enterprise customer requests (particularly from EMEA region prospects).

### 5.2 ISO 27001 Implementation Timeline

| Phase | Activities | Target Date | Owner |
|---|---|---|---|
| Gap Assessment | Third-party ISO 27001 gap assessment vs. current ISMS | February 2026 | Marcus Webb |
| ISMS Documentation | Document policies, procedures, risk register | Q1-Q2 2026 | Security Team |
| Risk Assessment | Formal ISO 27001 risk assessment and treatment plan | Q2 2026 | Security Team |
| Control Implementation | Remediate gaps identified in gap assessment | Q2-Q3 2026 | Engineering/IT |
| Internal Audit | Internal ISMS audit | August 2026 | External auditor |
| Certification Audit (Stage 1) | Document review by BSI (certification body) | September 2026 | BSI Group |
| Certification Audit (Stage 2) | On-site/remote implementation testing | October 2026 | BSI Group |
| Certification | ISO 27001:2022 certificate issued | November 2026 | BSI Group |

---

## Section 6: NIST Cybersecurity Framework Alignment

### 6.1 Current Status

**Status: SUBSTANTIALLY ALIGNED**

NovaTech has aligned its security program to the NIST Cybersecurity Framework (CSF) Version 2.0. A formal gap assessment was conducted in Q3 2025.

### 6.2 NIST CSF Maturity by Function

| Function | Current Maturity Level | Target | Notes |
|---|---|---|---|
| Identify | Tier 3 (Repeatable) | Tier 4 | Asset inventory partially automated; CMDB in progress |
| Protect | Tier 3 (Repeatable) | Tier 4 | Strong controls; WAF, encryption, MFA all deployed |
| Detect | Tier 3 (Repeatable) | Tier 4 | Datadog SIEM; alert tuning ongoing |
| Respond | Tier 2 (Risk-Informed) | Tier 3 | IR plan exists; tabletop exercises needed |
| Recover | Tier 2 (Risk-Informed) | Tier 3 | BCP documented; full DR test pending |

**Planned Actions:**
- Tabletop incident response exercise: March 2026 (owner: Marcus Webb)
- Full DR test: June 2026 (owner: DevOps team)
- CMDB implementation: Q2 2026 (using ServiceNow Lite)

---

## Section 7: Annual Penetration Test Schedule

### 7.1 2025 Penetration Test Results

- **Testing Firm:** Bishop Fox (November 2025)
- **Scope:** External web application, API endpoints, AWS infrastructure, internal network segment
- **Findings Summary:**
  - Critical: 0
  - High: 1 (SSRF vulnerability in image upload endpoint — remediated November 28, 2025)
  - Medium: 4 (all remediated or risk-accepted by December 31, 2025)
  - Low/Informational: 12 (tracked in vulnerability backlog)
- **Retest:** Completed December 15, 2025; all High findings confirmed remediated

### 7.2 2026 Penetration Test Schedule

| Test | Target Date | Scope | Testing Firm |
|---|---|---|---|
| Annual External Pen Test | October 2026 | Full external attack surface | Bishop Fox (contract renewal) |
| API Security Test | April 2026 | All API endpoints (v1 and v2) | Internal security team |
| Mobile Application Test | Q2 2026 (post-mobile app launch) | iOS and Android apps | To be determined via RFP |
| Social Engineering Test | Q3 2026 | Phishing simulation (1 week) | KnowBe4 (automated simulation) |

---

## Section 8: Vulnerability Disclosure Policy

### 8.1 Policy Overview

NovaTech maintains a responsible vulnerability disclosure program. Security researchers who discover vulnerabilities in the NovaTech Platform or website may report them to security@novatech.io.

**Key Policy Terms:**
- NovaTech will acknowledge receipt within 2 business days
- Critical vulnerabilities will be assessed within 24 hours; medium/low within 7 days
- NovaTech does not pursue legal action against good-faith researchers
- Coordinated public disclosure is supported; standard embargo period is 90 days
- Bug bounty: NovaTech participates in HackerOne private program (invitation-only as of January 2026; public launch planned Q2 2026)

---

## Section 9: Export Control Compliance (EAR)

### 9.1 Current Status

**Status: COMPLIANT**

NovaTech's software platform constitutes "EAR99" technology (no export license required for most destinations) under the Export Administration Regulations (EAR) administered by the U.S. Department of Commerce Bureau of Industry and Security (BIS).

### 9.2 EAR Compliance Procedures

- **Denied Party Screening:** All new customers and vendors are screened against U.S. Denied Parties List (DPL), Entity List, Specially Designated Nationals (SDN) list using Dow Jones Risk Center. Screening performed at contract execution and annually thereafter.
- **Country Restrictions:** NovaTech does not sell or provide services to customers in embargoed countries (Cuba, Iran, North Korea, Syria, Crimea Region) or to prohibited end-users.
- **Encryption:** NovaTech's platform uses encryption technology; applicable EAR encryption reporting requirements have been satisfied (annual self-classification report filed).
- **Training:** Annual export control training for Sales, Legal, and Finance teams.

---

## Section 10: WCAG 2.1 AA Accessibility

### 10.1 Current Status

**Status: SUBSTANTIALLY COMPLIANT**

The NovaTech Platform has been assessed against WCAG 2.1 Level AA criteria.

### 10.2 Accessibility Assessment Summary (October 2025, conducted by Deque Systems)

- **Criteria Tested:** All Level A (30 criteria) and Level AA (20 criteria)
- **Conformance:** 46 of 50 criteria fully met; 4 criteria partially met
- **Known Issues:** Color contrast in 2 legacy UI components (fix in Q1 2026 sprint); keyboard navigation in modal dialogs (fix in Q2 2026)
- **VPAT (Voluntary Product Accessibility Template):** Available upon request from customers

### 10.3 Accessibility Roadmap

- [ ] Q1 2026: Fix color contrast issues in legacy UI (Engineering sprint 24)
- [ ] Q2 2026: Fix keyboard navigation in modals
- [ ] Q2 2026: Reassessment by Deque Systems; update VPAT
- [ ] Q3 2026: ARIA label audit and remediation

---

## Section 11: 2026 Compliance Calendar

| Month | Compliance Activity | Owner |
|---|---|---|
| January | Q4 2025 GDPR ROPA update | Dr. Nina Bhatt |
| February | ISO 27001 gap assessment | Marcus Webb |
| March | Tabletop incident response exercise | Marcus Webb |
| April | Annual GDPR/CCPA employee training | HR + Legal |
| April | API security pen test | Security team |
| May | HIPAA gap analysis complete; consultant engaged | David Park |
| June | DR test; NIST CSF gap refresh | DevOps + Security |
| June | Annual GDPR review | Dr. Nina Bhatt |
| July | CCPA annual audit (internal) | Legal + Finance |
| August | SOC 2 2026 audit kickoff | Marcus Webb |
| September | ISO 27001 Stage 1 audit | BSI Group |
| October | Annual external penetration test | Bishop Fox |
| October | ISO 27001 Stage 2 audit | BSI Group |
| November | Export control annual training | Sales + Legal |
| November | ISO 27001 certification (target) | BSI Group |
| December | Year-end compliance review; 2027 planning | David Park |

---

*This document is reviewed semi-annually and updated to reflect current compliance status. Questions should be directed to David Park, General Counsel (d.park@novatech.io) or Dr. Nina Bhatt, DPO (privacy@novatech.io).*

*© 2026 NovaTech Solutions, Inc. | Confidential — Internal Use Only*
