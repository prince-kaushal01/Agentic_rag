# NovaTech Solutions — Data Processing Agreement (DPA)

**Document Reference:** LEGAL-DPA-STANDARD-001  
**Version:** 2.3  
**Effective Date:** January 1, 2026  
**Last Updated:** December 15, 2025  
**Approved By:** David Park, General Counsel; Dr. Nina Bhatt, Data Protection Officer  
**Governing Standards:** GDPR (EU) 2016/679; UK GDPR; CCPA/CPRA  
**Classification:** Standard Customer DPA — Enterprise Tier  

---

## Introduction

This Data Processing Agreement ("DPA") forms part of and is incorporated into the Master Enterprise Subscription Agreement, Enterprise Software Subscription Agreement, or other applicable agreement (the "Principal Agreement") between NovaTech Solutions, Inc. ("NovaTech" or "Processor") and the customer identified in the Principal Agreement ("Customer" or "Controller").

This DPA applies to NovaTech's processing of Personal Data on behalf of Customer in connection with the provision of the NovaTech Platform and associated services. The terms of this DPA shall prevail over any inconsistent terms in the Principal Agreement to the extent they relate to the processing of Personal Data.

By executing the Principal Agreement, Customer agrees to the terms of this DPA.

---

## Section 1: Definitions

For purposes of this DPA, the following definitions apply:

**1.1 "GDPR"** means the General Data Protection Regulation (EU) 2016/679 of the European Parliament and of the Council, as amended or replaced from time to time, and "UK GDPR" means GDPR as it forms part of the law of England and Wales, Scotland, and Northern Ireland by virtue of Section 3 of the European Union (Withdrawal) Act 2018.

**1.2 "Controller"** means the entity that determines the purposes and means of the processing of Personal Data. For purposes of this DPA, Customer is the Controller.

**1.3 "Processor"** means the entity that processes Personal Data on behalf of the Controller. For purposes of this DPA, NovaTech is the Processor.

**1.4 "Sub-Processor"** means any third party engaged by NovaTech to process Personal Data on NovaTech's behalf in connection with the Principal Agreement.

**1.5 "Personal Data"** means any information relating to an identified or identifiable natural person ("Data Subject"), including but not limited to names, email addresses, IP addresses, and any other data that, alone or in combination, identifies an individual.

**1.6 "Processing"** means any operation or set of operations performed on Personal Data, whether or not by automated means, such as collection, recording, storage, use, disclosure, or deletion.

**1.7 "Data Subject"** means the identified or identifiable natural person to whom Personal Data relates. This includes Customer's employees, contractors, and customers whose Personal Data is processed in connection with the Services.

**1.8 "Standard Contractual Clauses" or "SCCs"** means the contractual clauses adopted by the European Commission pursuant to its Implementing Decision 2021/914/EU, for the transfer of personal data to third countries.

**1.9 "Security Incident"** means any accidental or unlawful destruction, loss, alteration, unauthorized disclosure of, or access to Personal Data transmitted, stored, or otherwise processed by NovaTech in connection with the Services.

**1.10 "Applicable Data Protection Law"** means all applicable privacy and data protection laws and regulations, including GDPR, UK GDPR, and CCPA/CPRA as applicable to each Party's respective activities.

---

## Section 2: Scope and Purpose of Processing

**2.1 Processing Instructions.** NovaTech shall process Personal Data only: (a) on behalf of Customer; (b) in accordance with Customer's documented instructions as set forth in this DPA and the Principal Agreement; and (c) for no other purpose unless required by applicable law, in which case NovaTech will notify Customer to the extent permitted by law.

**2.2 Nature of Processing.** NovaTech will process Personal Data to: provide and maintain the NovaTech Platform; provide customer support; send service-related communications; ensure security and integrity of the Platform; comply with legal obligations; and improve the Platform as permitted by this DPA.

**2.3 Categories of Data Subjects.** The following categories of Data Subjects may be included in Personal Data processed under this DPA:
- Customer's employees and contractors (Authorized Users)
- Customer's customers and end-users (to the extent Customer inputs such data into the Platform)
- Individuals whose data Customer uploads, imports, or processes through the Platform

**2.4 Types of Personal Data.** Personal Data processed under this DPA may include:
- **Identity data:** First name, last name, username, job title
- **Contact data:** Work email address, phone number
- **Authentication data:** Login credentials (hashed/encrypted), SSO tokens
- **Usage data:** Platform activity logs, feature usage patterns, IP addresses
- **Communication data:** Support ticket content, chat logs
- **Customer-uploaded data:** Any personal data Customer inputs into the Platform (NovaTech does not control or review the nature of such data)

**2.5 Duration of Processing.** NovaTech will process Personal Data for the duration of the Principal Agreement plus any applicable retention periods, as set forth in Section 9.

---

## Section 3: Controller's Obligations

**3.1 Compliance.** Customer, as Controller, is responsible for compliance with Applicable Data Protection Law with respect to Customer's use of the Services, including ensuring it has a valid legal basis for processing Personal Data and for providing any required notices to Data Subjects.

**3.2 Accuracy of Data.** Customer is responsible for the accuracy, quality, and legality of Personal Data submitted to the Platform.

**3.3 Restricted Data.** Customer agrees not to submit to the Platform any special categories of personal data (as defined in GDPR Article 9) including health data, biometric data, genetic data, racial or ethnic origin data, or similar sensitive categories, unless Customer has separately notified NovaTech and obtained NovaTech's written agreement to process such data.

**3.4 Instructions.** Customer's instructions for processing are as set forth in this DPA and the Principal Agreement. Customer may provide additional written instructions through the account settings portal or by written notice to privacy@novatech.io.

---

## Section 4: NovaTech's Obligations as Processor

**4.1 Processing in Accordance with Instructions.** NovaTech shall process Personal Data only in accordance with Customer's documented instructions, unless required to do otherwise by applicable law. If NovaTech believes that an instruction violates Applicable Data Protection Law, NovaTech will promptly notify Customer.

**4.2 Confidentiality.** NovaTech shall ensure that its personnel authorized to process Personal Data are subject to appropriate confidentiality obligations (contractual or statutory).

**4.3 Security.** NovaTech shall implement and maintain the technical and organizational security measures described in Section 5 of this DPA.

**4.4 Sub-Processors.** NovaTech shall comply with the sub-processor requirements set forth in Section 6 of this DPA.

**4.5 Data Subject Rights.** NovaTech shall assist Customer in responding to Data Subject rights requests as set forth in Section 7 of this DPA.

**4.6 Data Protection Impact Assessments.** NovaTech shall provide reasonable assistance to Customer in conducting data protection impact assessments (DPIAs) and prior consultations with supervisory authorities, where required by Applicable Data Protection Law.

---

## Section 5: Technical and Organizational Security Measures (TOMs)

NovaTech implements the following technical and organizational measures to protect Personal Data:

### 5.1 Organizational Measures

| Measure | Description |
|---|---|
| Information Security Policy | Comprehensive ISMS aligned with ISO 27001 framework |
| Security Training | Annual mandatory security awareness training for all employees |
| Background Checks | Background screening for all employees with access to customer data |
| Access Review | Quarterly review of access rights; principle of least privilege enforced |
| Incident Response | Documented incident response plan; tested annually |
| Vendor Risk Management | Security assessments for all sub-processors handling Personal Data |

### 5.2 Technical Measures

| Measure | Description |
|---|---|
| Encryption at Rest | AES-256 encryption for all stored data (AWS S3, RDS, Snowflake) |
| Encryption in Transit | TLS 1.2 minimum (TLS 1.3 preferred) for all data in transit |
| Access Controls | RBAC with principle of least privilege; MFA enforced for all admin access |
| Network Security | VPC isolation; Web Application Firewall (WAF); DDoS protection |
| Logging and Monitoring | Centralized security logging (Datadog SIEM); 24/7 anomaly alerts |
| Vulnerability Management | Monthly automated scans; quarterly manual penetration testing |
| Endpoint Security | MDM enforced on all corporate devices; EDR on all endpoints |
| Backup and Recovery | Automated daily backups; tested recovery procedures; 99.9% durability target |

### 5.3 Physical Measures

- All production infrastructure hosted in AWS data centers (SOC 2, ISO 27001, PCI DSS certified)
- NovaTech offices secured with card-access control systems
- Clean desk policy enforced for all finance and legal personnel
- Remote work security standards aligned with corporate security policy

### 5.4 Certifications

NovaTech maintains the following certifications relevant to data security:
- **SOC 2 Type II:** Most recent report period: January 1, 2025 – December 31, 2025; available under NDA upon request
- **ISO 27001:** Roadmap target: Q4 2026 certification
- **Annual Penetration Test:** Most recent: October 2025 (conducted by Bishop Fox); critical findings remediated within 30 days; medium findings within 90 days

---

## Section 6: Sub-Processor Management

**6.1 General Authorization.** Customer provides general authorization for NovaTech to engage sub-processors as set forth in this Section 6, provided NovaTech complies with the requirements herein.

**6.2 Current Approved Sub-Processors.** NovaTech's current approved sub-processors who may process Personal Data are:

| Sub-Processor | Purpose | Data Location | Security Standard |
|---|---|---|---|
| Amazon Web Services (AWS) | Cloud infrastructure; data storage | USA (us-east-1, us-west-2); EU (eu-west-1 for EU data residency customers) | SOC 2, ISO 27001, PCI DSS |
| Google Cloud Platform | Backup storage; BigQuery analytics | USA | SOC 2, ISO 27001 |
| Stripe, Inc. | Payment processing | USA | PCI DSS Level 1, SOC 2 |
| Twilio/SendGrid | Transactional email delivery | USA | SOC 2 |
| Zendesk, Inc. | Customer support ticketing | USA | SOC 2 |
| Snowflake, Inc. | Data analytics and warehousing | USA (configurable) | SOC 2 |

A full, current list of sub-processors is maintained at novatech.io/legal/subprocessors.

**6.3 New Sub-Processors.** NovaTech will provide at least **30 days' prior written notice** before engaging a new sub-processor that will process Personal Data, via update to the sub-processor list page and, for Enterprise customers, via email notification to the account's Data Protection contact.

**6.4 Customer Objection.** Customer may object to a new sub-processor within 15 days of receiving notice by sending written notice to privacy@novatech.io with the reasons for objection. If Customer reasonably objects and NovaTech cannot provide an alternative that addresses Customer's objection, Customer may terminate the Principal Agreement without penalty, with a prorated refund for prepaid unused periods.

**6.5 Sub-Processor Contractual Requirements.** NovaTech shall ensure that each sub-processor is bound by contractual obligations providing at least the same level of data protection as this DPA, in accordance with GDPR Article 28(4).

---

## Section 7: Data Subject Rights Assistance

**7.1 NovaTech's Obligations.** NovaTech shall provide Customer with reasonable technical and organizational assistance to enable Customer to fulfill its obligations to respond to Data Subject rights requests under Applicable Data Protection Law, including requests for access, rectification, erasure, restriction, portability, and objection.

**7.2 Forwarding Requests.** If NovaTech receives a Data Subject rights request directly from a Data Subject relating to Customer's account, NovaTech shall promptly (within 5 business days) forward such request to Customer and shall not respond to the Data Subject directly (except to acknowledge receipt and direct the individual to the Controller).

**7.3 Deletion and Erasure.** Upon receipt of a verified erasure request (whether from Customer as Controller or as directed by a Data Subject), NovaTech shall delete or anonymize the relevant Personal Data within 30 days, subject to any applicable legal retention obligations.

**7.4 Data Portability.** NovaTech shall make available data export functionality within the Platform (CSV and JSON format) to assist Customer in fulfilling portability requests.

---

## Section 8: Security Incident Notification

**8.1 Notification Timeline.** If NovaTech becomes aware of a confirmed Security Incident affecting Customer's Personal Data, NovaTech shall notify Customer without undue delay and in any event within **seventy-two (72) hours** of becoming aware of the confirmed incident, to the extent such notification is required by Applicable Data Protection Law.

**8.2 Notification Content.** Incident notifications shall include (to the extent then known):
- Nature of the Security Incident (type of incident, categories of Personal Data affected)
- Estimated number of Data Subjects affected
- Likely consequences of the incident
- Measures taken or proposed to be taken by NovaTech to address the incident and mitigate its effects
- Contact information for NovaTech's security team and DPO

**8.3 Cooperation.** NovaTech shall cooperate with Customer and take commercially reasonable steps to investigate and mitigate the Security Incident. Customer is responsible for notifying relevant regulatory authorities and affected Data Subjects where required.

**8.4 Notification Channel.** Security incident notifications shall be sent to: (a) the email address on file for Customer's account administrator; and (b) the security contact designated in Customer's account settings. Enterprise customers may designate a dedicated security contact at privacy@novatech.io.

---

## Section 9: Data Retention and Deletion

**9.1 Retention During Agreement.** NovaTech will retain Customer's Personal Data for the duration of the Principal Agreement.

**9.2 Post-Termination.** Following termination or expiration of the Principal Agreement, NovaTech will: (a) make Customer Data available for download via the Platform for **60 days** following termination; and (b) permanently delete Customer's Personal Data from its production systems within 90 days of the termination date (unless longer retention is required by applicable law).

**9.3 Deletion Certificate.** Upon written request, NovaTech will provide Customer with a written certification of deletion within 30 days of completion of the deletion process.

**9.4 Backup Retention.** Automated backups are retained for 30 days. Personal Data in backup archives will be overwritten within the standard backup rotation cycle (30 days), after which no Personal Data from the terminated account will be recoverable.

---

## Section 10: Audit Rights

**10.1 Documentation.** NovaTech shall maintain appropriate records of its data processing activities as required by GDPR Article 30, and shall make such records available to Customer upon reasonable written request.

**10.2 Audits.** No more than once per calendar year, Customer may audit NovaTech's compliance with this DPA upon 60 days' prior written notice. Audits shall be conducted during NovaTech's regular business hours and shall not unreasonably interfere with NovaTech's operations. Customer shall bear the cost of any such audit unless the audit reveals a material breach of this DPA.

**10.3 Audit Reports.** In lieu of a direct audit, NovaTech may provide Customer with its most recent SOC 2 Type II audit report, penetration test executive summary, or other relevant third-party audit reports under NDA, which Customer may reasonably rely upon.

---

## Section 11: International Data Transfers

**11.1 Transfer Mechanisms.** For transfers of Personal Data from the EEA or UK to the United States (or other countries without an EU/UK adequacy decision), the Parties agree to rely on one or more of the following transfer mechanisms:

**(a) Standard Contractual Clauses (SCCs):** The Parties agree to execute the EU SCCs adopted by Commission Implementing Decision 2021/914 (Module 2 — Controller to Processor) as applicable. The SCCs are incorporated into this DPA by reference and shall apply to transfers of EEA Personal Data from Customer (as controller) to NovaTech (as processor).

**(b) UK International Data Transfer Addendum (IDTA):** For transfers from the United Kingdom, the Parties agree to the UK IDTA issued by the UK ICO, which supplements the SCCs for UK transfers.

**11.2 Annex Completion.** The Annexes to the SCCs (describing the transfer details, data subjects, and security measures) are deemed completed by reference to Section 2 (Scope) and Section 5 (Security Measures) of this DPA.

**11.3 Sub-Processor Transfers.** For onward transfers from NovaTech to sub-processors located outside the EEA/UK, NovaTech shall ensure appropriate transfer mechanisms are in place with each sub-processor (SCCs Module 3, or equivalent).

---

## Section 12: Governing Law

This DPA shall be governed by the laws of the State of California, except to the extent required otherwise by Applicable Data Protection Law (e.g., GDPR provisions shall be interpreted under EU law as appropriate).

---

## Appendix A: DPO Contact Information

**NovaTech Data Protection Officer:**  
Dr. Nina Bhatt  
privacy@novatech.io  
NovaTech Solutions, Inc., 580 Market Street, Suite 1200, San Francisco, CA 94104  
Phone: +1 (415) 555-0133  

**EU Representative (Article 27 GDPR):**  
NovaTech EU Representative  
c/o DataRep  
The Cube, Monahan Road, Cork, T12 H1XY, Ireland  
eu-rep@novatech.io  

---

*This DPA supersedes any prior data processing agreements between the Parties. For questions about this DPA, contact privacy@novatech.io.*

*© 2026 NovaTech Solutions, Inc. | Version 2.3 | GDPR/CCPA Compliant*
