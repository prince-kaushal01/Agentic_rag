# NovaTech Solutions — Sales Process Standard Operating Procedures
**Version 2.1 | Effective January 1, 2026**
**Revenue Operations | revops@novatechsolutions.com**
**Owner: Preethi Ramachandran, Revenue Operations Manager**

---

## Table of Contents
1. Overview & Purpose
2. Lead Handoff: SDR to AE
3. CRM Hygiene Requirements (Salesforce)
4. Deal Review Process
5. Deal Desk & Approval Thresholds
6. Contract Routing to Legal
7. Order Form Execution
8. Revenue Recognition Handoff to Finance
9. Customer Handoff to Customer Success
10. Escalation Paths & Exception Handling
11. Quarterly Process Audit

---

## 1. Overview & Purpose

This SOP defines the end-to-end standard operating procedures for NovaTech's sales process, from lead handoff to post-close customer handoff. Adherence to these SOPs is **mandatory** for all Sales, Revenue Operations, Legal, Finance, and Customer Success team members involved in the sales cycle.

The purpose of this document is to:
- Ensure consistency, accountability, and predictability in deal execution
- Maintain Salesforce as the single source of truth for all sales activity and revenue data
- Enable accurate revenue forecasting and recognition
- Protect NovaTech's commercial and legal interests in every transaction
- Create a seamless customer experience from first contact through post-sale onboarding

Non-adherence to these SOPs is tracked via the quarterly CRM audit process (§11) and may result in coaching, rep scorecards being affected, or escalation to the Sales Manager and VP of Sales.

---

## 2. Lead Handoff: SDR to AE

### 2.1 SDR Responsibilities Before Handoff
Before an SDR passes a qualified lead to an AE, the following requirements must be met:

**SDR Qualification Checklist (all must be confirmed):**
- [ ] Confirmed contact is at a company matching the ICP (500+ employees, B2B, appropriate industry)
- [ ] Identified pain or interest that aligns with NovaTech's core value propositions
- [ ] Confirmed the contact has at least influence over (if not authority over) a purchasing decision
- [ ] Secured a committed, calendared meeting (not "reach out next week" — an actual meeting invite sent and accepted)
- [ ] Confirmed meeting is for at least 30 minutes in the calendar
- [ ] No active opportunity already exists for this account in Salesforce (check before outreach begins)

**SDR Disqualification Criteria (any one disqualifies):**
- Company has fewer than 150 employees
- Contact is completely outside any relevant buying committee
- Company is a direct competitor of NovaTech
- Company is already a current NovaTech customer (pass to CSM, not AE)

### 2.2 Handoff Meeting (Required for Enterprise Accounts)
For any meeting at a company with 1,000+ employees or likely deal value >$100K ARR:
- SDR must hold a **5-minute verbal briefing with the AE** before the scheduled meeting
- Briefing covers: company context, contact name/title/what they said, pain signals identified, any prior outreach attempts and responses
- AE confirms they've reviewed the SDR's research notes in Salesforce

For mid-market accounts (<1,000 employees, likely deal <$100K), briefing can be replaced by a documented summary in Salesforce for the AE to review asynchronously.

### 2.3 What Gets Created in Salesforce at Handoff
At the moment an SDR passes a lead to an AE, the following Salesforce records must exist:
- **Account** record (create if it doesn't exist)
- **Contact** record linked to the Account
- **Opportunity** record created by the SDR, with:
  - Account name, contact, and role
  - Stage set to "1 — Prospecting"
  - Close date set to 90 days from discovery meeting date (AE adjusts after discovery)
  - ARR estimate (SDR's rough guess based on company size — AE will refine)
  - Lead source (outbound, inbound, referral, event, etc.)
  - SDR name in "SDR" custom field
  - AE name in "Account Executive" field (AE takes ownership)
  - Notes from SDR conversations in "Initial Discovery Notes" field

### 2.4 SDR to AE Transition Communication
Within 24 hours of handoff, the SDR sends an email introduction:

> Subject: Introduction: [AE name], meet [Contact name] at [Company]
>
> Hi [Contact],
>
> I wanted to formally introduce you to [AE name], who is an account executive at NovaTech. [AE name] works with companies like yours that are focused on [pain area discussed]. He/She/They will be your primary contact going forward and has a ton of relevant experience in [industry].
>
> [AE name] — [Contact] and I had a great conversation about [brief pain summary]. I'll let you take it from here.
>
> [AE name], here's the context doc: [link to Salesforce opportunity]
>
> [SDR name]

The AE must respond to this thread within 4 business hours and take ownership of scheduling the discovery meeting.

---

## 3. CRM Hygiene Requirements (Salesforce)

Salesforce is NovaTech's system of record. Every interaction, stage change, and deal data point lives in Salesforce. **If it's not in Salesforce, it doesn't exist.**

### 3.1 Required Fields by Stage

| Stage | Required Fields |
|-------|----------------|
| 1 — Prospecting | Account, Contact, ARR estimate, Close Date, Lead Source, AE, SDR |
| 2 — Discovery | MEDDIC fields (M, E, D, D, I, C), Champion name, Next Step with date |
| 3 — Demo/Evaluation | Demo completed date, Evaluation criteria documented, Technical contact identified |
| 4 — Proposal | Proposal sent date, Proposal amount, Multi-year offered Y/N |
| 5 — Negotiation | Verbal agreement date, Legal review initiated Y/N, Discount % (if any), Discount approval chain |
| 6 — Closed Won | Signed order form attached, Close date (actual), ARR final, Contract term (months), Start date |
| 7 — Closed Lost | Lost date, Lost reason (dropdown), Lost to competitor (if applicable), Key lessons |

### 3.2 Weekly CRM Hygiene Standards
Every AE must maintain the following Salesforce hygiene standards, checked weekly by Revenue Operations:
- All opportunities have a **Next Step** (action + date) that is within 7 days of today
- All opportunities have been **touched** (activity logged) within the past 7 days
- All opportunities in Stage 3+ have a **Close Date** that is realistic and not past
- All closed lost opportunities have a **Lost Reason** selected within 48 hours of loss

CRM hygiene is reviewed every Monday morning by Revenue Operations. AEs receive a weekly hygiene score via automated Salesforce report. Hygiene scores are included in manager 1:1s and quarterly performance reviews.

### 3.3 Activity Logging Requirements
All customer-facing activities must be logged in Salesforce within **24 hours**:
- Discovery calls and demo calls: log as "Call" activity with summary notes
- Emails sent to prospects: automatically synced if using Outreach.io (strongly recommended); otherwise log manually
- In-person meetings: log as "Meeting" with attendees and summary
- Proposals sent: log as a "Task — Proposal Sent" with proposal value and date

---

## 4. Deal Review Process

### 4.1 Weekly Pipeline Review (All AEs)
The Sales Manager holds a **weekly pipeline review** every **Monday at 10:00 AM PT** (30–45 minutes). All AEs are required to attend.

**Pipeline Review Agenda:**
- Review all opportunities in Stage 3–5 (Demo, Proposal, Negotiation)
- Each AE provides a 2-minute verbal update on their top 3 deals: current status, next step, any risks
- Manager flags any deal with no activity in past 7 days for urgent follow-up
- Identify any deals that need executive support or cross-functional involvement
- Review forecast accuracy from prior week

**AE Preparation for Pipeline Review:**
- Salesforce must be fully updated by Sunday 11:59 PM
- Top 3 deals summarized in writing in the Slack #pipeline-review channel before the Monday call

### 4.2 Weekly Forecast Call (Manager + VP)
Every Tuesday at 1:00 PM PT, the Sales Manager holds a forecast call with the VP of Sales:
- Review committed deals (80%+ close probability, within current quarter)
- Review best-case deals (50–79%)
- Update quarterly revenue forecast in Salesforce (roll-up to VP view)
- Flag any forecast risk changes from the prior week

### 4.3 Monthly Deal Review (Stage 4–5 Deals, >$100K ARR)
Any deal in Proposal or Negotiation stage with ARR >$100K requires a formal **Deal Review** with the VP of Sales before the proposal is sent or a verbal commitment is made to the customer.

**Deal Review Meeting Format (30 minutes):**
1. AE presents: who is involved (champion, EB, technical), MEDDIC summary, competitive situation
2. VP asks: "What could kill this deal?" and "What do we need to do this week to advance?"
3. Commercial terms reviewed: proposed pricing, discount level, contract term
4. Confirm discount approval is in place before proposal goes out (see §5)
5. Executive involvement: does the CEO/CTO need to be engaged?

---

## 5. Deal Desk & Approval Thresholds

The Deal Desk is a Revenue Operations function that ensures all commercial terms are within approved boundaries before being offered to a customer.

### 5.1 Deal Desk Triggers
A Deal Desk review is required when any of the following apply:
- Deal ARR is ≥$150,000
- Discount exceeds the AE's self-approval threshold (>15% off list)
- Contract term is non-standard (e.g., month-to-month, 4+ years)
- Customer is requesting non-standard payment terms (e.g., quarterly payment instead of annual)
- Customer is requesting custom data residency requirements
- Custom SLA provisions requested
- Any deal with a government entity

### 5.2 Deal Desk Process
1. AE submits a **Deal Desk Request** in Salesforce (Deal Desk tab on the Opportunity record)
2. Revenue Operations reviews the request within **2 business days**
3. RevOps routes to appropriate approvers based on deal size and non-standard terms
4. RevOps confirms approval or counter-proposes alternative terms to AE within **3 business days total**
5. AE proceeds with customer negotiation only after written Deal Desk approval

### 5.3 Approval Matrix

| Deal Size / Issue | Approver |
|------------------|---------|
| Discount 16–25% | Sales Manager |
| Discount 26–35% | VP of Sales |
| Discount 36–45% | VP of Sales + CFO |
| Discount >45% | CEO + CFO |
| ARR $150K–$300K custom terms | VP of Sales + RevOps |
| ARR >$300K any non-standard | VP of Sales + CFO + Legal |
| Custom SLA (<99.5% uptime) | VP Engineering + Legal |
| Government entity | Legal + CFO |
| HIPAA Business Associate Agreement (BAA) | Legal + CISO |

### 5.4 Non-Negotiable Terms (Cannot Be Modified Without Board Approval)
- NovaTech's limitation of liability cap (standard: 12 months ARR)
- Indemnification provisions in the standard MSA
- Data processing agreement (DPA) GDPR terms
- NovaTech's intellectual property ownership provisions
- Any term that would classify NovaTech as a data fiduciary (rather than data processor)

---

## 6. Contract Routing to Legal

All customer-facing contracts must go through NovaTech's Legal team for review before execution. The two primary documents are:
- **Master Subscription Agreement (MSA):** Governs the overall relationship
- **Order Form:** Specifies the commercial terms of each purchase

### 6.1 Standard Contract Process

**Scenario A: Customer Signs NovaTech's Standard MSA (preferred)**
1. AE sends NovaTech Standard MSA + Order Form to customer via DocuSign
2. Customer signs; contract is fully executed
3. No Legal review required for standard form (pre-approved by Legal)
4. AE uploads signed documents to Salesforce Opportunity and marks Closed Won

**Scenario B: Customer Provides Their Own MSA / Redlines NovaTech's MSA**
1. Customer sends their paper (or redlines) to AE
2. AE sends to legal@novatechsolutions.com with subject: "CONTRACT REVIEW — [Company Name] — [ARR]"
3. Legal confirms receipt within 1 business day
4. Legal review timeline:
   - Standard redlines: 5 business days
   - Complex or non-standard: 10 business days (Legal notifies AE of timeline)
   - Urgent (customer deadline): AE requests expedited review; Legal accommodates within 3 business days if staffing allows
5. Legal provides marked-up redlines to AE with "approved to accept," "do not accept," and "propose alternative" annotations
6. AE negotiates with customer based on Legal's guidance; material changes require re-review

### 6.2 Legal Review Request Format
When emailing legal@novatechsolutions.com, include:
- Customer name and Salesforce Opportunity link
- Deal ARR and contract term
- Customer's primary concern or negotiation focus (if known)
- Deadline for execution (if any)
- Attach: customer's MSA or NovaTech MSA with their redlines

### 6.3 Contract Storage
All executed contracts (MSA + Order Form, fully countersigned) must be stored in:
- **Salesforce:** Attached to the Opportunity record (required)
- **Google Drive:** Legal folder (RevOps uploads within 24 hours of execution)
- **Ironclad (CLM):** Contract lifecycle management tool; RevOps uploads for metadata indexing and renewal alerting

---

## 7. Order Form Execution

The Order Form is the commercial document that specifies what the customer is purchasing, at what price, and for what term.

### 7.1 Order Form Generation
All Order Forms are generated in **Salesforce CPQ** (Configure, Price, Quote module). AEs must not create Order Forms manually (in Word or Google Docs) without RevOps approval.

**To generate an Order Form in Salesforce CPQ:**
1. Navigate to the Opportunity record
2. Click "New Quote" in the Quotes section
3. Select the appropriate price book (Standard 2026, or Nonprofit/Education/Partner if applicable)
4. Add products: select tier (Starter, Professional, Enterprise), user count, modules, term
5. Apply any approved discounts
6. Generate PDF and send via DocuSign integration (DocuSign is embedded in CPQ)

### 7.2 Order Form Required Fields
Every Order Form must include:
- Customer legal entity name (exact legal name, not trade name)
- Billing address
- Contract start date
- Contract end date
- Total ARR and total contract value (TCV)
- Payment terms (standard: net 30, annual invoice)
- List of all licensed products and modules
- User count
- Data residency (US, EU, or AUS)
- Signatures: Customer authorized signatory + NovaTech authorized signatory (VP Sales or CFO for deals >$200K)

### 7.3 Signature Authority
NovaTech employees authorized to countersign Order Forms and MSAs:
- Deals ≤$100K ARR: Sales Manager (M1)
- Deals $100K–$500K ARR: VP of Sales (Daniel Okafor)
- Deals >$500K ARR: CFO (Carlos Jimenez) or CEO (Marcus Harrington)

Do not send a DocuSign with the wrong NovaTech signer — this delays execution and creates legal complications.

### 7.4 DocuSign Routing Order
Standard DocuSign routing:
1. Customer authorized signatory signs first
2. NovaTech authorized signatory countersigns
3. Both parties receive fully executed copy automatically via DocuSign

AEs must NOT sign on behalf of NovaTech.

---

## 8. Revenue Recognition Handoff to Finance

When an Order Form is fully executed (countersigned by both parties), the following revenue recognition process is triggered:

### 8.1 AE Responsibilities at Close
Within **4 business hours** of receiving a fully executed Order Form:
1. Change Salesforce Opportunity Stage to "6 — Closed Won"
2. Enter the actual close date (date of last signature)
3. Attach the signed Order Form PDF to the Opportunity record
4. Update the Opportunity with final ARR, TCV, contract start date, contract end date
5. Notify the Finance team via the #deal-close Slack channel with the Opportunity name and link

### 8.2 Finance Processing
Finance receives a real-time notification via Salesforce when an Opportunity is marked Closed Won.

Finance team (Derek Santos, Sr. Financial Analyst; Carlos Jimenez, CFO) reviews the Opportunity and Order Form to:
- Confirm contract start date and billing period
- Create the invoice in NetSuite (within 3 business days of close)
- Set up the revenue recognition schedule in NetSuite (straight-line over the contract term, per ASC 606)
- Process the commission calculation for the AE (RevOps runs commissions by the 15th of the month following the close month)

### 8.3 Revenue Recognition Policy
NovaTech recognizes subscription revenue on a straight-line basis over the contract term (ASC 606 compliant). For a $120,000 ARR 1-year contract starting February 1, 2026:
- Revenue recognized per month: $10,000
- Total recognized in FY2026 (Feb–Dec): $110,000
- Deferred revenue at Jan 1, 2026: $0 (contract not yet started)

Multi-year contracts with upfront payment are recognized ratably over the full term.

### 8.4 Booking vs. Billing vs. Revenue
Finance tracks three distinct metrics for each deal:
- **Booking:** Date the Order Form is countersigned (AE's "close")
- **Billing:** Date the invoice is sent to the customer (typically within 3 business days of booking)
- **Revenue Recognition:** Begins on the contract start date, recognized ratably

AEs are measured on **bookings** for quota and commission purposes.

---

## 9. Customer Handoff to Customer Success

The handoff from Sales to Customer Success is one of the highest-impact moments in the customer lifecycle. Poor handoffs are a top-3 driver of early churn.

### 9.1 Handoff Timing
The Sales-to-CS handoff must occur within **5 business days** of the Order Form being fully executed.

### 9.2 AE Handoff Document (Required for All Deals)
The AE must complete a **Customer Handoff Document** in Notion (template: CS Resources > Handoff Template) and share with the assigned CSM before the introduction call.

**Required Handoff Document Sections:**
1. **Deal Summary:** ARR, contract term, products purchased, start date
2. **Customer Context:** Industry, company size, primary use case, number of users, technical environment (Zendesk, Salesforce, Okta, etc.)
3. **Stakeholder Map:** Champion name, EB name, technical contact, other key contacts (with email and LinkedIn)
4. **Pain Points & Success Metrics:** What pain did they buy to solve? What metrics did they commit to improving? What did we promise them by 90 days?
5. **Competitive Context:** Who did they evaluate? Why did they choose NovaTech? What concerns came up?
6. **Commitments Made During Sales:** Any non-standard promises, feature requests, SLA commitments, pricing side agreements
7. **Red Flags or Risks:** Anything the CSM should know going in (e.g., internal skeptic on the team, historical bad experience with previous vendor, complex data migration)

### 9.3 Introduction Call
The AE schedules and attends the **Sales-to-CS Introduction Call** within 5 business days of close:
- AE introduces the CSM to the champion and day-to-day contacts
- AE explicitly transfers the relationship to the CSM
- CSM presents the onboarding plan and 30-day schedule
- AE should say very little after the introduction; this is the CSM's meeting

After the introduction call, the AE should only be involved in the account for expansion and renewal commercial discussions — not for day-to-day customer management.

### 9.4 CSM Assignment
CSM assignment is handled by the Director of Customer Success (Samuel Osei) within 2 business days of deal close notification via the #deal-close Slack channel. Assignment is based on CSM capacity, industry expertise, and geographic proximity.

---

## 10. Escalation Paths & Exception Handling

### 10.1 Deal Execution Exceptions
If a customer requires terms outside this SOP (e.g., extreme urgency, unusual payment terms, unique legal requirements):
- AE escalates to Sales Manager immediately
- Sales Manager assesses whether exception is commercially warranted
- If yes: RevOps + Legal are involved in expedited review
- All exceptions must be documented in Salesforce under "Exception Notes" field

### 10.2 Stuck Deal Escalation
If a deal has been in Stage 4 or 5 for more than 30 days without a signed agreement:
- Sales Manager is automatically notified via Salesforce workflow
- Sales Manager schedules an immediate deal review with the AE
- VP of Sales is notified if the deal has been stuck for 45+ days
- Executive engagement from the CEO or CTO may be deployed for strategic accounts

### 10.3 Legal Dispute Escalation
If a customer raises concerns during contract negotiations that Legal determines represent unacceptable risk:
- Legal documents the concern and proposed resolution in the Ironclad CLM
- Legal communicates position to RevOps and AE within 1 business day
- If customer insists on unacceptable terms: VP of Sales and CFO decide whether to walk away from the deal

---

## 11. Quarterly Process Audit

Revenue Operations conducts a **quarterly sales process audit** to ensure compliance with this SOP.

### 11.1 Audit Scope
Each quarter, RevOps audits a random sample of 20% of all closed opportunities (won and lost) for:
- CRM field completion at each stage
- Activity logging within required timelines
- Presence of signed contracts in Salesforce
- Proper handoff document completion
- Commission calculation accuracy

### 11.2 Audit Scorecard
Each AE receives a quarterly audit score (0–100) based on adherence to SOP requirements. Scores are shared with:
- The individual AE
- Their Sales Manager
- The VP of Sales (aggregate team score)

Scores below 70 trigger a coaching conversation. Scores below 50 for two consecutive quarters are escalated to HR for performance management consideration.

### 11.3 Process Improvement
Audit findings that reveal systemic issues (e.g., a field that is consistently missed because it's confusing) are brought to the RevOps + Sales leadership monthly meeting for process refinement. This SOP is updated quarterly based on audit findings.

---

*SOP Owner: Preethi Ramachandran, Revenue Operations Manager*
*Reviewed by: Daniel Okafor, VP of Sales | Carlos Jimenez, CFO | Legal Team*
*Last Updated: January 10, 2026*
*Next Quarterly Review: April 2026*
*Salesforce Admin questions: salesforce-admin@novatechsolutions.com*
