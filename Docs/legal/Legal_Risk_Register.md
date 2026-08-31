# NovaTech Solutions — Legal Risk Register

**Document Owner:** Legal Department  
**Document Number:** LEGAL-RISK-001  
**Version:** 2.1  
**Effective Date:** January 1, 2026  
**Last Updated:** January 15, 2026  
**Next Review:** June 30, 2026  
**Approved By:** David Park, General Counsel; Derek Simmons, CEO  
**Classification:** Confidential — Legal and Executive Leadership Only  

---

## Overview

This Legal Risk Register ("Register") identifies, assesses, and tracks material legal risks facing NovaTech Solutions, Inc. The Register is reviewed quarterly by the General Counsel and semi-annually with the CEO and Board Audit Committee. Risk assessments reflect current conditions as of the Last Updated date.

**Risk Scoring Methodology:**
- **Likelihood:** H = High (likely to occur within 12 months), M = Medium (possible within 24 months), L = Low (unlikely within 24 months)
- **Impact:** H = High (material financial/operational/reputational harm), M = Medium (moderate disruption or cost), L = Low (minor disruption)
- **Risk Score:** HH = Critical, HM or MH = High, MM or HL = Medium, Others = Low

---

## Risk 1: Open Source License Compliance Violation

| Field | Detail |
|---|---|
| **Risk ID** | LEGAL-RISK-001 |
| **Category** | Intellectual Property |
| **Risk Description** | NovaTech inadvertently incorporates open source software with GPL, AGPL, or SSPL license terms into its commercial product. This could require NovaTech to publicly disclose its proprietary source code under copyleft obligations, significantly impairing the Company's IP value and competitive position. The risk is heightened as the codebase grows (currently 380,000+ lines of code) and as engineers incorporate new libraries without proper license review. |
| **Likelihood** | M |
| **Impact** | H |
| **Risk Score** | High |
| **Current Controls** | FOSSA automated license scanning in CI/CD pipeline; Open Source Policy (LEGAL-POL-004); approved/prohibited license list maintained; quarterly Engineering briefings on open source hygiene |
| **Residual Risk** | FOSSA catches license issues pre-merge but does not cover indirect/transitive dependencies in all frameworks. |
| **Mitigation Actions** | 1. Expand FOSSA scanning to cover all transitive dependencies by Q2 2026. 2. Add mandatory open source review to Engineering sprint review checklist. 3. Annual open source audit by external IP counsel (Fenwick & West). |
| **Owner** | David Park / Marcus Webb |
| **Review Date** | April 2026 |

---

## Risk 2: Customer Data Breach — Liability Exposure

| Field | Detail |
|---|---|
| **Risk ID** | LEGAL-RISK-002 |
| **Category** | Regulatory / Contractual |
| **Risk Description** | A security incident results in unauthorized access to or disclosure of Customer Data (including personal data of Customer's employees or end-users). This could trigger GDPR/CCPA breach notification obligations, customer contract breach claims, potential regulatory enforcement (EU DPA fines up to 4% of global annual turnover), class action litigation, and reputational damage. The enterprise customer base (including ACME Corp, GlobalTech Inc., Meridian Enterprises) increases concentration risk. |
| **Likelihood** | M |
| **Impact** | H |
| **Risk Score** | High |
| **Current Controls** | SOC 2 Type II certified; AES-256 encryption at rest and in transit; 24/7 security monitoring via Datadog; annual penetration testing (Bishop Fox); incident response plan; MFA enforced; cyber liability insurance ($10M policy); liability cap in contracts (12-month fees) |
| **Residual Risk** | Sophisticated nation-state or well-resourced attacker; supply chain attack via sub-processors; social engineering of employees. |
| **Mitigation Actions** | 1. Complete ISO 27001 certification by Q4 2026. 2. Implement phishing-resistant MFA (FIDO2) by Q3 2026. 3. Expand security monitoring to cover sub-processor integrations. 4. Review and increase cyber liability coverage at next renewal (August 2026). 5. Implement HIPAA-aligned data segregation as preparatory step. |
| **Owner** | Marcus Webb / David Park |
| **Review Date** | March 2026 |

---

## Risk 3: Employment Law Changes — California Wage and Hour

| Field | Detail |
|---|---|
| **Risk ID** | LEGAL-RISK-003 |
| **Category** | Employment Law |
| **Risk Description** | California wage and hour laws are among the most complex in the U.S. NovaTech faces risk of misclassification claims (employee vs. contractor), overtime calculation errors for certain technical roles, failure to comply with California's meal and rest break requirements, or PAGA (Private Attorneys General Act) claims. A class action PAGA suit could result in civil penalties of $100–$200 per employee per pay period for initial violations, which at 319 employees could be material. |
| **Likelihood** | M |
| **Impact** | M |
| **Risk Score** | Medium |
| **Current Controls** | Employment counsel (Fenwick & West) advises on classification; Workday payroll system includes CA compliance rules; HR conducts annual wage and hour audit; all contractors have written agreements with IC classification analysis |
| **Residual Risk** | AB5 and Dynamex standard continues to evolve; remote employee multi-state issues as we hire in additional states (NY, TX, WA, MA currently). |
| **Mitigation Actions** | 1. Annual employment law audit by external counsel — next due March 2026. 2. Review all contractor classifications against AB5/Dynamex before April 2026. 3. HR to obtain EPLI (Employment Practices Liability Insurance) coverage review — current policy: $5M. 4. Implement automated CA break and overtime compliance check in Workday. |
| **Owner** | Jennifer Walsh / David Park |
| **Review Date** | April 2026 |

---

## Risk 4: Patent Troll / Non-Practicing Entity (NPE) Claims

| Field | Detail |
|---|---|
| **Risk ID** | LEGAL-RISK-004 |
| **Category** | Intellectual Property |
| **Risk Description** | As NovaTech grows and its platform becomes more widely used, it may become a target for patent assertion by non-practicing entities (NPEs or "patent trolls"). Common areas of risk for SaaS companies include: software workflow automation patents, notification and messaging patents, data synchronization patents, and AI/ML inference patents. Defense of even frivolous patent claims can cost $500K–$3M in legal fees and consume significant management attention. |
| **Likelihood** | L |
| **Impact** | M |
| **Risk Score** | Low-Medium |
| **Current Controls** | Freedom-to-operate analysis conducted for core product features; 3 issued patents provide some defensive portfolio; membership in Open Invention Network (OIN) under evaluation; IP indemnification provisions in customer contracts protect against upstream claims |
| **Residual Risk** | NovaTech's patent portfolio (3 issued) is insufficient for meaningful cross-licensing leverage if asserted by a large NPE. |
| **Mitigation Actions** | 1. File 5 additional patent applications in 2026 (target areas: workflow automation, AI recommendations, data sync protocol). 2. Evaluate OIN membership (annual cost: free for companies under $100M revenue). 3. Maintain $1M litigation reserve for IP defense (Finance to set aside in Q2 2026). 4. Obtain IP litigation insurance rider on D&O policy. |
| **Owner** | David Park / Marcus Webb |
| **Review Date** | June 2026 |

---

## Risk 5: GDPR Regulatory Enforcement

| Field | Detail |
|---|---|
| **Risk ID** | LEGAL-RISK-005 |
| **Category** | Regulatory |
| **Risk Description** | A complaint from an EU data subject, a customer, or a whistleblower could trigger an investigation by a European Data Protection Authority (DPA) — most likely the Irish DPA (Data Protection Commission) given NovaTech's EU processing through AWS Ireland. Maximum GDPR fines are €20M or 4% of global annual turnover (whichever is higher). At NovaTech's current ARR ($18.2M), maximum fine exposure is approximately $728,000. More significant risk is reputational harm and required remediation costs. |
| **Likelihood** | L |
| **Impact** | M |
| **Risk Score** | Low-Medium |
| **Current Controls** | GDPR-compliant Privacy Policy; DPO appointed; Article 30 ROPA maintained; SCCs executed with all sub-processors; customer DPAs in place; OneTrust CMP for cookie consent; data subject rights procedures operational |
| **Residual Risk** | New AI analytics features (launched November 2024) may have GDPR implications for automated decision-making (Article 22) that have not been fully assessed. |
| **Mitigation Actions** | 1. Complete DPIA for AI analytics module by February 2026. 2. Confirm Article 22 compliance (or applicability) for AI recommendations feature. 3. DPO to present GDPR compliance status to Board Audit Committee at April 2026 meeting. 4. Enroll DPO in IAPP annual conference for regulatory monitoring. |
| **Owner** | Dr. Nina Bhatt / David Park |
| **Review Date** | March 2026 |

---

## Risk 6: Enterprise Contract Dispute — Customer Churn and Refund Disputes

| Field | Detail |
|---|---|
| **Risk ID** | LEGAL-RISK-006 |
| **Category** | Contractual |
| **Risk Description** | As NovaTech scales its enterprise customer base, the probability of material contract disputes increases. Disputes may arise from: SLA breach claims, refund disputes, early termination fee conflicts, or allegations that the product materially failed to meet contracted specifications. A single large enterprise contract dispute (e.g., a customer seeking to void a $240,000 annual contract and recover fees paid) could result in significant legal costs, credit/refund exposure, and diversion of executive attention. Key current risk: ACME Corp's annual contract ($240K) is up for Year 2 billing; any service disruption or SLA breach in Year 1 could trigger a refund claim. |
| **Likelihood** | M |
| **Impact** | M |
| **Risk Score** | Medium |
| **Current Controls** | Standard contract terms include arbitration clause limiting litigation risk; 12-month liability cap; clear SLA credit structure; refund policy requires VP Finance approval for amounts > $10K; Customer Success team conducts QBRs with all enterprise customers; NPS monitoring |
| **Residual Risk** | Contract language ("materially fails to perform") is subject to interpretation; motivated customer with strong counsel could pursue broad interpretation of refund rights. |
| **Mitigation Actions** | 1. Legal to review and tighten "material specification failure" definition in enterprise contract template (Q1 2026). 2. CS to implement systematic SLA compliance tracking and reporting for all enterprise customers. 3. Ensure all enterprise refund requests route through Finance AND Legal for review before approval of amounts > $25K. 4. Build $200K contingency reserve in 2026 budget for potential refund/dispute settlements. |
| **Owner** | David Park / Rachel Kim (CCO) |
| **Review Date** | March 2026 |

---

## Risk 7: Series B Fundraising — Securities Law Compliance

| Field | Detail |
|---|---|
| **Risk ID** | LEGAL-RISK-007 |
| **Category** | Regulatory / Corporate |
| **Risk Description** | NovaTech is actively pursuing a Series B fundraise (target close Q3 2026, target raise: $25M–$35M). Securities law requirements for private placements (Regulation D, Rule 506(b) or 506(c)) require careful compliance. Risks include: improper general solicitation, sales to non-accredited investors, material misrepresentations or omissions in investor materials, and failure to file timely Form D. Consequences include rescission rights for investors, SEC enforcement, and potential disqualification from future private placements. |
| **Likelihood** | L |
| **Impact** | H |
| **Risk Score** | Medium |
| **Current Controls** | Lakeview Capital Partners engaged as financial advisor; Fenwick & West serving as Company counsel for the raise; Board approval required for all investor communications; all investor materials reviewed by Legal before distribution |
| **Residual Risk** | Multiple term sheets in negotiation simultaneously; complex disclosure requirements across multiple jurisdictions (U.S. + potentially UK/EU investors). |
| **Mitigation Actions** | 1. Engage qualified securities counsel at Fenwick & West immediately (already engaged). 2. Ensure all investor materials include standard risk factors and forward-looking statement disclaimers. 3. File Form D within 15 days of first sale. 4. Maintain investor suitability records for all accredited investor verifications. |
| **Owner** | David Park / Derek Simmons |
| **Review Date** | August 2026 (post-close) |

---

## Risk 8: Employee Trade Secret Misappropriation (Incoming)

| Field | Detail |
|---|---|
| **Risk ID** | LEGAL-RISK-008 |
| **Category** | Intellectual Property / Employment |
| **Risk Description** | As NovaTech hires aggressively (18 new hires in Q1 2026 alone), there is risk that a new employee brings and/or uses trade secrets or confidential information from their prior employer. This could expose NovaTech to trade secret misappropriation claims, injunctions affecting the employee's work, and potentially NovaTech's products. Specific current concern: a newly hired senior backend engineer (joined January 2026) previously worked at a direct competitor (Nexflow Systems). |
| **Likelihood** | M |
| **Impact** | M |
| **Risk Score** | Medium |
| **Current Controls** | All employees sign IP assignment agreement and certify no conflict with prior employer obligations; onboarding process includes legal briefing on trade secret policy; HR reviews offer letters for key hires |
| **Residual Risk** | Former employer (Nexflow Systems) is aware of the hire and may monitor NovaTech product releases for evidence of misappropriation. |
| **Mitigation Actions** | 1. Conduct tailored legal briefing with the specific new engineer (January 2026 — David Park meeting scheduled). 2. Assign the engineer to a product area not directly overlapping with their prior work for initial 6 months. 3. Document the assignment decision in HR file. 4. Retain Fenwick & West on standby for any potential cease and desist from Nexflow. |
| **Owner** | David Park / Jennifer Walsh |
| **Review Date** | July 2026 |

---

## Risk 9: CCPA/CPRA Class Action Litigation

| Field | Detail |
|---|---|
| **Risk ID** | LEGAL-RISK-009 |
| **Category** | Regulatory |
| **Risk Description** | The California Privacy Rights Act (CPRA) includes a private right of action for consumers whose non-redacted personal information is subject to unauthorized access, theft, or disclosure. A data incident affecting California residents could trigger class action litigation under CPRA with statutory damages of $100–$750 per incident per consumer. NovaTech's customer base includes California-based companies whose employees' personal data may be processed on the Platform. |
| **Likelihood** | L |
| **Impact** | H |
| **Risk Score** | Medium |
| **Current Controls** | Strong data security program (see Risk 2); encryption at rest and in transit; contractual limitation of liability; cyber liability insurance ($10M); privacy-by-design approach in product development |
| **Residual Risk** | CPRA private right of action is relatively new; plaintiffs' bar is actively developing theories. Even a minor incident could attract litigation. |
| **Mitigation Actions** | 1. Ensure CCPA/CPRA compliance review completed annually (next: July 2026). 2. Review and confirm cyber liability policy covers CPRA litigation (review at August 2026 renewal). 3. Implement "privacy by default" product settings per CPRA requirements. |
| **Owner** | Dr. Nina Bhatt / David Park |
| **Review Date** | July 2026 |

---

## Risk 10: Vendor/Supplier Contract Dispute

| Field | Detail |
|---|---|
| **Risk ID** | LEGAL-RISK-010 |
| **Category** | Contractual |
| **Risk Description** | NovaTech's primary infrastructure (AWS EDP contract, $420K/year) and key SaaS tools (Salesforce, $105K/year; Snowflake, $188K/year) are governed by complex vendor agreements. Risk includes: disputed auto-renewal, unexpected price increases at renewal, vendor enforcement of usage restrictions, or vendor insolvency affecting service continuity. The Snowflake contract renewals in August 2026 poses immediate risk as the current negotiation is contentious (Snowflake proposing a 22% price increase vs. NovaTech's 10% counter). |
| **Likelihood** | M |
| **Impact** | M |
| **Risk Score** | Medium |
| **Current Controls** | Procurement Policy requires legal review of contracts > $100K; Finance tracks all renewal dates in vendor register; alternatives evaluated at each renewal; Snowflake alternative (Google BigQuery) benchmarked in Q4 2025 as negotiation leverage |
| **Residual Risk** | Deep data integration with Snowflake makes switching costly and time-consuming; Snowflake is aware of this leverage. |
| **Mitigation Actions** | 1. Begin Snowflake renewal negotiation no later than June 2026 (current contract expires August 15). 2. Present Google BigQuery migration estimate to CFO as BATNA (Best Alternative to Negotiated Agreement) by May 2026. 3. Engage NovaTech's AWS account team as potential ally (Snowflake on AWS Marketplace — AWS may help). |
| **Owner** | Margaret Liu / David Park |
| **Review Date** | May 2026 |

---

## Risk 11: Director and Officer Liability — Board Decision-Making

| Field | Detail |
|---|---|
| **Risk ID** | LEGAL-RISK-011 |
| **Category** | Corporate Governance |
| **Risk Description** | As NovaTech approaches a potential Series B and eventual exit (IPO or acquisition), Board decision-making becomes subject to higher scrutiny. Risks include: breach of fiduciary duty claims by minority investors or employees regarding equity dilution, compensation decisions, or strategic transactions. D&O insurance provides first-line protection but may not cover all claims, particularly in situations involving fraud or intentional misconduct. |
| **Likelihood** | L |
| **Impact** | M |
| **Risk Score** | Low-Medium |
| **Current Controls** | D&O insurance ($10M aggregate coverage; carrier: Chubb); independent Board directors (3 of 7 seats); Audit Committee oversight; regular Board meetings with documented minutes; Fenwick & West advises Board on governance |
| **Residual Risk** | Series B fundraise and anticipated option pool expansion will involve Board decisions about dilution that could be scrutinized. |
| **Mitigation Actions** | 1. Review D&O coverage at next renewal and consider increasing to $15M for post-Series B period. 2. Ensure Board minutes are thorough and reflect deliberative process for all material decisions. 3. Consider adding a third independent director prior to Series B (governance request from potential lead investor). |
| **Owner** | David Park / Derek Simmons |
| **Review Date** | September 2026 |

---

## Summary Risk Matrix

| Risk ID | Risk Name | Likelihood | Impact | Score | Owner | Next Review |
|---|---|---|---|---|---|---|
| LEGAL-RISK-001 | Open Source License Compliance | M | H | High | David Park | Apr 2026 |
| LEGAL-RISK-002 | Customer Data Breach | M | H | High | Marcus Webb | Mar 2026 |
| LEGAL-RISK-003 | CA Employment Law / PAGA | M | M | Medium | Jennifer Walsh | Apr 2026 |
| LEGAL-RISK-004 | Patent Troll / NPE | L | M | Low-Med | David Park | Jun 2026 |
| LEGAL-RISK-005 | GDPR Enforcement | L | M | Low-Med | Dr. Nina Bhatt | Mar 2026 |
| LEGAL-RISK-006 | Enterprise Contract Dispute | M | M | Medium | David Park | Mar 2026 |
| LEGAL-RISK-007 | Series B Securities Law | L | H | Medium | David Park | Aug 2026 |
| LEGAL-RISK-008 | Trade Secret (Incoming Employee) | M | M | Medium | Jennifer Walsh | Jul 2026 |
| LEGAL-RISK-009 | CCPA Class Action | L | H | Medium | Dr. Nina Bhatt | Jul 2026 |
| LEGAL-RISK-010 | Vendor Contract Dispute | M | M | Medium | Margaret Liu | May 2026 |
| LEGAL-RISK-011 | D&O / Board Liability | L | M | Low-Med | David Park | Sep 2026 |

---

*This Risk Register is reviewed quarterly. Risks that escalate to High or Critical require immediate escalation to the CEO and Board Chair. Questions should be directed to David Park, General Counsel (d.park@novatech.io).*

*Classification: CONFIDENTIAL — Legal and Executive Leadership Only*
*© 2026 NovaTech Solutions, Inc. | 580 Market Street, Suite 1200 | San Francisco, CA 94104*
