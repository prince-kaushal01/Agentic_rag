# NovaTech Solutions — Intellectual Property and Proprietary Rights Policy

**Document Owner:** Legal Department  
**Policy Number:** LEGAL-POL-004  
**Effective Date:** January 1, 2026  
**Last Reviewed:** December 5, 2025  
**Next Review Date:** December 5, 2026  
**Approved By:** David Park, General Counsel; Derek Simmons, CEO  
**Version:** 2.5  

---

## Purpose and Scope

This Intellectual Property and Proprietary Rights Policy ("Policy") governs the ownership, protection, and management of intellectual property ("IP") created by or in connection with NovaTech Solutions, Inc. It applies to all full-time employees, part-time employees, interns, contractors, and consultants who create work product in connection with their engagement with NovaTech.

NovaTech's intellectual property — including its software platform, source code, algorithms, proprietary methodologies, patents, trademarks, trade secrets, and confidential know-how — represents a core component of the Company's value and competitive advantage. This Policy establishes NovaTech's rules for IP ownership, open source usage, patent rights, trademark management, trade secret protection, and software escrow.

All employees and contractors must read, understand, and comply with this Policy. By executing an employment agreement or contractor agreement with NovaTech, each individual acknowledges that they have reviewed and agreed to abide by the terms of this Policy.

---

## Section 1: Employee IP Assignment

### 1.1 Scope of Assignment

All work product created by an employee within the scope of their employment at NovaTech — whether created during regular working hours or otherwise, whether using NovaTech's resources or the employee's own resources — belongs exclusively to NovaTech Solutions, Inc. This includes:

- Software code, scripts, programs, algorithms, and architectures
- Technical designs, specifications, and documentation
- Product features, ideas, and improvements
- Business plans, marketing strategies, and sales materials
- Patents, patent applications, and inventions related to NovaTech's business
- Trade secrets and confidential methodologies
- Written content, blog posts, presentations, and training materials created in an employment capacity
- Data models, database schemas, and data processing pipelines
- User interface designs, wireframes, and prototypes

### 1.2 Assignment Agreement

Every NovaTech employee is required to execute a Confidentiality and IP Assignment Agreement (the "IP Agreement") as a condition of employment. The IP Agreement provides for:
- Assignment of all inventions, discoveries, and work product to NovaTech
- Cooperation in executing patent applications and other IP filings
- Ongoing obligations that survive termination of employment

### 1.3 Prior Inventions

Employees must disclose all prior inventions that they wish to exclude from the scope of the IP Assignment Agreement before their start date. Undisclosed prior inventions that relate to NovaTech's business are presumed to be covered by the Assignment Agreement.

### 1.4 California Labor Code Compliance

In accordance with California Labor Code Section 2870, the IP assignment obligation does not apply to inventions that (a) were developed entirely on the employee's own time, (b) without using NovaTech's equipment, supplies, facilities, or trade secret information, (c) that do not relate to NovaTech's business or NovaTech's actual or demonstrably anticipated research or development, and (d) that do not result from any work performed by the employee for NovaTech.

Employees claiming an exclusion under California Labor Code Section 2870 must disclose such inventions to the General Counsel within 30 days of creation.

---

## Section 2: Contractor IP Provisions

### 2.1 Work for Hire

All contractors and consultants engaged by NovaTech are required to execute a Contractor Agreement that includes an IP assignment provision. All work product created by contractors in the course of their engagement with NovaTech shall be deemed "work made for hire" to the maximum extent permitted by law. To the extent that any work product does not qualify as work made for hire, the contractor hereby assigns all rights, title, and interest in such work product to NovaTech.

### 2.2 Pre-existing Tools and Third-Party IP

Contractors may use pre-existing tools, frameworks, or libraries in deliverables, provided that:
- The use of such pre-existing materials is disclosed in writing to NovaTech before use
- The contractor has the right to use such materials and to grant NovaTech the necessary rights
- Any pre-existing materials used are clearly identified in the deliverable documentation
- Use of GPL-licensed or similarly restricted open source in commercial deliverables requires Legal team review and approval (see Section 3)

### 2.3 Contractor Confidentiality

All contractors must execute a Non-Disclosure Agreement before beginning any work. Contractor NDAs include obligations that survive the end of the engagement for a minimum of three (3) years.

---

## Section 3: Open Source Policy

### 3.1 Overview

NovaTech uses open source software in its products and infrastructure. The use of open source must be managed carefully to avoid introducing license obligations that could compromise NovaTech's proprietary IP, require disclosure of source code, or create compliance violations.

### 3.2 Approved Open Source Licenses (for use in commercial products)

The following open source licenses are **approved** for use in NovaTech's commercial products without restriction:

| License | Common Examples | Key Conditions |
|---|---|---|
| MIT License | React, Express, Lodash | No copyleft; attribution required |
| Apache License 2.0 | Kubernetes, Kafka, TensorFlow | No copyleft; attribution required; patent grant included |
| BSD 2-Clause ("Simplified") | Flask, various | No copyleft; attribution required |
| BSD 3-Clause | Various | No copyleft; attribution required; no endorsement |
| ISC License | Node.js utilities | Functionally equivalent to MIT |
| Creative Commons (non-SA variants) | Documentation, content | For documentation/content use only; not for code |

### 3.3 Prohibited Open Source Licenses (in commercial products without Legal approval)

The following licenses are **prohibited** for use in NovaTech's commercially distributed products without prior written approval from the General Counsel:

| License | Risk | Notes |
|---|---|---|
| GNU General Public License v2 (GPL-2.0) | Strong copyleft — may require source disclosure | Requires written approval from Legal |
| GNU General Public License v3 (GPL-3.0) | Strong copyleft | Requires written approval from Legal |
| GNU Affero General Public License (AGPL-3.0) | Network copyleft — SaaS services may trigger disclosure | Prohibited in product; review required |
| GNU Lesser General Public License (LGPL) | Weak copyleft | May be permitted for dynamic linking only — requires Legal review |
| Server Side Public License (SSPL) | Copyleft triggered by cloud service use | Prohibited |
| Creative Commons ShareAlike (SA) | Copyleft for content | Prohibited for code; restricted for content |

### 3.4 Open Source Approval Process

Before incorporating any open source library or component into NovaTech's codebase, the developer must:

1. Check the license against the Approved and Prohibited lists above
2. For Approved licenses: proceed with use and document the component in the Open Source Inventory (maintained in Notion)
3. For Prohibited licenses: submit an approval request to Legal (legal@novatech.io) with the component name, version, license, proposed use case, and alternative analysis
4. For unclassified licenses: submit to Legal for classification before use

### 3.5 Open Source Attribution

NovaTech maintains an up-to-date open source attribution file (NOTICES.txt or THIRD_PARTY_LICENSES.md) included in all product distributions. The Engineering team uses FOSSA for automated license compliance scanning as part of the CI/CD pipeline.

### 3.6 Open Source Contributions

NovaTech employees who wish to contribute to external open source projects during work hours must obtain prior written approval from their manager and the General Counsel. Contributions that involve NovaTech's proprietary code or trade secrets are prohibited. Personal open source contributions on employees' own time, using their own resources, and unrelated to NovaTech's business are not subject to this Policy.

---

## Section 4: Patent Policy

### 4.1 Invention Disclosure

Employees who believe they have made a patentable invention in the course of their work at NovaTech must promptly submit an Invention Disclosure Form to the General Counsel (legal@novatech.io) within 30 days of conceiving the invention. The disclosure should describe: (a) the invention, including its technical basis and how it works; (b) the problem it solves; (c) how it differs from prior art; and (d) a list of all inventors who contributed to the conception.

### 4.2 Patent Committee Review

NovaTech's Patent Committee (chaired by the CTO and General Counsel, with the CPO and a senior engineer as additional members) reviews all invention disclosures quarterly and decides whether to:
- File a utility patent application (U.S. and/or international)
- File a provisional patent application to establish priority date
- Maintain as a trade secret (no patent filing)
- Abandon (no action)

### 4.3 Inventor Awards

NovaTech rewards employees who disclose inventions that result in patent filings and grants:

| Milestone | Award Amount |
|---|---|
| Invention Disclosure filed and accepted by Patent Committee | $500 |
| U.S. Patent Application filed | $2,500 |
| U.S. Patent Granted | $5,000 |
| International Patent Granted (per country) | $1,000 additional |
| Patent Licensed or Commercialized | $10,000 (one-time bonus) |

Awards are paid through payroll and are subject to applicable taxes.

### 4.4 Current Patent Portfolio

As of January 1, 2026, NovaTech has:
- 3 issued U.S. patents (workflow automation engine, AI recommendation model, data synchronization protocol)
- 5 pending U.S. patent applications
- 1 pending international (PCT) application
- 8 invention disclosures under review by Patent Committee

---

## Section 5: Trademark Guidelines

### 5.1 NovaTech Trademarks

The following are registered or pending trademarks of NovaTech Solutions, Inc.:

| Mark | Registration Status | Registration No. |
|---|---|---|
| NOVATECH SOLUTIONS® | Registered (USPTO) | 6,284,511 |
| NOVATECH® (word mark) | Registered (USPTO) | 6,284,512 |
| NovaTech logo (blue/white) | Registered (USPTO) | 6,312,847 |
| NovaTech logo (dark mode) | Application pending | App. No. 97/612,344 |

### 5.2 Brand Usage Guidelines for Employees

Internal use:
- Always use "NovaTech Solutions" on first reference in external documents; "NovaTech" is acceptable on subsequent references
- Do not alter the NovaTech logo (no recoloring, stretching, overlaying, or unauthorized combinations)
- Use the registered trademark symbol (®) on first use in marketing materials and customer-facing documents
- Brand guidelines are maintained by the Marketing team at brand.novatech.io

External partner and customer use:
- Customers and partners who wish to use NovaTech's trademarks must obtain written approval from the Legal and Marketing teams
- Approved usage must comply with NovaTech's Partner Brand Guidelines (available upon request)

### 5.3 Domain and Social Media

NovaTech has registered and controls: novatech.io and key social media handles (@novatech on LinkedIn, Twitter/X, YouTube, and major platforms). Employees must not register domain names or social media accounts using NovaTech's name or marks without prior approval from Marketing and Legal.

---

## Section 6: Trade Secret Protection

### 6.1 Definition

NovaTech's trade secrets include, without limitation: source code and algorithms; product roadmaps and unreleased feature plans; pricing strategies and models; customer lists and customer-specific data; technical specifications not disclosed publicly; business strategies; financial projections; and proprietary methodologies.

### 6.2 Protection Requirements

All employees who have access to trade secrets must:
- Access trade secret information only on NovaTech-approved systems (no personal devices or unauthorized cloud services)
- Never share trade secret information outside NovaTech except under a signed NDA
- Immediately report any suspected unauthorized access or disclosure to legal@novatech.io
- Follow the clean desk and clean screen policies

### 6.3 Trade Secret Classification

NovaTech classifies information in four categories:

| Classification | Description | Access Control |
|---|---|---|
| Public | Publicly available information | No restriction |
| Internal | General internal information | Employees only |
| Confidential | Sensitive business information; trade secrets | Need-to-know basis; NDA required for external sharing |
| Restricted | Highest sensitivity (source code, financial data, legal matters) | Explicit written authorization required |

### 6.4 Departing Employee Procedures

Upon an employee's departure from NovaTech:
- All Company devices, access credentials, and materials must be returned on the last working day
- The employee must certify that they have not retained copies of NovaTech's trade secrets or confidential information
- The General Counsel may send a reminder letter to former employees regarding trade secret obligations
- For senior technical or commercial employees, NovaTech may send a notice to the departing employee's new employer informing them of existing confidentiality obligations

---

## Section 7: Software Escrow

### 7.1 Escrow Requirement

NovaTech offers software escrow arrangements to enterprise customers who require a continuity plan in the event NovaTech ceases to operate, undergoes a material acquisition, or is otherwise unable to provide the Platform.

### 7.2 Escrow Agent

NovaTech uses **Iron Mountain Intellectual Property Management** as its preferred escrow agent. The current master escrow agreement with Iron Mountain is dated June 1, 2024.

### 7.3 Escrow Triggers

Source code held in escrow is released to the beneficiary customer only upon the occurrence of defined "Release Conditions," including:
- NovaTech filing for bankruptcy protection (Chapter 7 or 11)
- NovaTech ceasing to provide the Platform for more than 90 consecutive days
- A Court order requiring release
- NovaTech's material breach of the Principal Agreement that is not cured within 60 days

### 7.4 Customer Eligibility

Software escrow arrangements are available to Enterprise customers with Annual Contract Values of $250,000 or greater. Customers may request escrow inclusion as a negotiated term in their Enterprise Subscription Agreement. Escrow fees (currently $4,500/year per customer escrow account) are billed separately from subscription fees.

### 7.5 Current Escrow Beneficiaries

As of January 1, 2026, the following enterprise customers have active software escrow arrangements:
- Meridian Enterprises (escrow account established July 2024)
- Pinnacle Systems (escrow account established January 2025)

---

## Appendix A: Key Legal Contacts

| Role | Name | Email |
|---|---|---|
| General Counsel | David Park | d.park@novatech.io |
| IP Counsel (External) | Michael Torres, Fenwick & West LLP | mtorres@fenwick.com |
| Patent Prosecution (External) | Susan Kwan, Kwan IP Group | skwan@kwanip.com |
| DPO / Privacy | Dr. Nina Bhatt | privacy@novatech.io |
| Brand / Trademark Inquiries | Legal Team | legal@novatech.io |

---

*This Policy is effective January 1, 2026 and supersedes all prior IP policies. Questions should be directed to David Park, General Counsel (d.park@novatech.io). All NovaTech employees must acknowledge receipt of this Policy annually during the compliance review process.*

*© 2026 NovaTech Solutions, Inc. All rights reserved. | 580 Market Street, Suite 1200 | San Francisco, CA 94104*
