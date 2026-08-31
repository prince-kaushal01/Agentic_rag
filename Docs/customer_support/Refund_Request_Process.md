# NovaTech Solutions — Refund Request Process

**Document Version:** 1.8  
**Last Updated:** November 12, 2025  
**Authors:** Jennifer Osei (Head of Customer Support), Ana Reyes (Finance Manager)  
**Classification:** Internal — Customer Support + Finance  
**Review Cycle:** Annual

---

## 1. Overview

This Standard Operating Procedure (SOP) defines the process for handling customer refund requests. NovaTech's refund policy is governed by the customer's Master Service Agreement (MSA) and Order Form. This SOP operationalizes that policy for the support and finance teams.

**General Policy:**
- NovaTech does not offer refunds for digital subscriptions that have been accessed and used
- Exceptions are granted in specific circumstances defined in Section 3
- The process is designed to be fair to customers while protecting NovaTech's revenue integrity
- Decisions must be consistent — precedents set by approving non-standard refunds create risk

---

## 2. Intake Process

### 2.1 How Refund Requests Arrive

Refund requests arrive via:
- Support ticket (support@novatech.com or support portal) — most common
- Direct email to Account Executive
- Direct email to Customer Success Manager
- In rare cases, via letter or legal notice

**All refund requests must be converted into a support ticket** tagged with:
- Category: `Billing`
- Sub-category: `Refund Request`
- Label: `refund`

This ensures tracking, audit trail, and SLA accountability.

### 2.2 Initial Triage (Tier 1 — within 24 hours)

Upon receiving a refund request, the Tier 1 agent must:

1. **Acknowledge the request** within SLA timeframe (24 business hours for P3)
2. **Send the intake response** (Template: `REFUND-01-Intake`)
3. **Gather required information** from the customer (see Section 2.3)
4. **Tag the ticket** correctly in Zendesk: `billing > refund`
5. **Notify the CSM** (if the customer has an assigned CSM) within 1 hour of receiving the request
6. **Do NOT** make any commitment about refund eligibility or amount at this stage

### 2.3 Required Information from Customer

The following information must be collected before the refund review can begin:

| Required Item | Why Needed |
|--------------|-----------|
| Account name and email | Identity verification |
| Invoice number(s) being contested | Specific the amount in question |
| Reason for refund request | Eligibility determination |
| Period of service covered by refund | SLA calculation if applicable |
| Supporting documentation | Varies by reason type (see Section 3) |

**Intake Template (REFUND-01):**
```
Subject: Re: [Refund Request] — NovaTech Support Ticket #TKT-XXXX

Hi [Customer Name],

Thank you for reaching out about a refund for your NovaTech subscription. I've created a 
support ticket (TKT-XXXX) to track this request.

To begin our review, I'll need the following information:
1. The invoice number(s) you are requesting a refund for
2. A brief description of the reason for your refund request
3. [If SLA-related]: The dates and descriptions of the service issues you experienced
4. [If billing error]: The amount you believe was charged incorrectly and the correct amount

Please reply to this email with the above information and we will complete our review 
within 5 business days.

If you have any questions in the meantime, please don't hesitate to ask.

Best regards,
[Agent Name]
NovaTech Customer Support
```

---

## 3. Refund Eligibility Criteria

### 3.1 Eligible for Refund

| Scenario | Eligible Amount | Supporting Doc Required |
|----------|----------------|------------------------|
| **Billing error** (NovaTech charged wrong amount) | Full amount of overcharge | Invoice showing discrepancy |
| **Duplicate charge** (customer charged twice) | Full duplicate amount | Bank statement or two invoice numbers |
| **Service not provisioned** (customer paid but access never granted) | Pro-rated amount for days without access | Account provisioning logs |
| **SLA breach** (per SLA credit schedule, if customer requests cash vs. credit) | Per SLA credit schedule (10–50% of monthly fee) | Incident ticket numbers; dates |
| **Annual subscription cancellation within 14 days** (new customers only) | 100% refund, no usage charges | — |
| **Material misrepresentation** during sales (documented) | Negotiated (CSM + VP Sales involved) | Written documentation of misrepresentation |
| **Account compromised and charges fraudulent** | Fraudulent charges | Police report or bank fraud declaration |

### 3.2 Not Eligible for Refund

| Scenario | Reason |
|----------|--------|
| General dissatisfaction with product (product is accessible and working) | MSA Section 8.2: no refunds for accessed services |
| Failure to use the service (unused subscription) | Non-usage is not a NovaTech failure |
| Cancellation after 14-day new customer period | Outside policy window |
| Performance issues below SLA threshold | Performance credits (not refunds) per SLA policy |
| Change of business needs | Not a service defect |
| Mid-year plan downgrade | Credits applied per contract; no cash refund |

**Note:** Even for ineligible scenarios, the support team should explore alternatives (SLA credits, contract extension, feature unlock) rather than simply saying "no."

---

## 4. Internal Review Process

### 4.1 Review Workflow

```
Tier 1 gathers information → Eligibility check against policy (Section 3)
        │
        ▼
Tier 2 / Support Manager reviews (all requests)
        │
        ├── Amount ≤ $500: Support Manager approves/denies
        │
        ├── Amount $501 – $10,000: Finance Manager approval required
        │         (Ana Reyes — ana.reyes@novatech.com)
        │
        └── Amount > $10,000: VP Finance approval required
                  (Mark Henderson — mark.henderson@novatech.com)
                  + Notification to VP Customer Success and relevant AE
```

### 4.2 Review Checklist

Before making a recommendation, the reviewer must check:

- [ ] Is the customer's account in good standing (no fraud flags)?
- [ ] Verify payment history (Stripe) — was the charge correctly processed?
- [ ] Verify the invoice amount against the Order Form
- [ ] Check MSA for any special refund terms negotiated for this customer
- [ ] Review incident logs if SLA-related — calculate actual downtime
- [ ] Check if customer previously received any credits for the same period
- [ ] Assess the account relationship risk (is this a strategic account?)
- [ ] Review any prior refund history for this customer

### 4.3 Review Timeline

| Request Type | Target Decision |
|-------------|----------------|
| Standard refund (clear eligibility) | 5 business days |
| Expedited refund (P0 account issue, executive request) | 2 business days |
| Complex refund (SLA dispute, requires investigation) | 10 business days |
| Legal-escalated refund | Per legal team guidance (no standard SLA) |

---

## 5. Communication Templates

### 5.1 Refund Approved (Full)

```
Subject: Refund Approved — $[Amount] — Invoice #[Invoice Number]

Hi [Customer Name],

Good news! We have reviewed your refund request for Invoice #[Invoice Number] and have 
approved a full refund of $[Amount].

Refund Method: [Credit to original payment method / Account credit]
Processing Time: 5-10 business days for credit to appear on your statement.

Reason for Approval: [Brief explanation — e.g., "We confirmed a duplicate charge" / 
"This represents the SLA credit for the March service disruption"]

We sincerely apologize for any inconvenience. If you have any questions about your 
refund, please reference ticket TKT-XXXX or reply to this email.

Thank you for your patience and for being a NovaTech customer.

[Agent Name]
NovaTech Customer Support
```

### 5.2 Refund Approved (Partial)

```
Subject: Partial Refund Approved — $[Amount] — Invoice #[Invoice Number]

Hi [Customer Name],

After reviewing your refund request, we have approved a partial refund of $[Amount] 
(of the $[Original Amount] requested).

Refund Method: [Credit to original payment method / Account credit]
Processing Time: 5-10 business days.

Calculation: [Explain how the amount was calculated — e.g., "This reflects 18 minutes 
of confirmed downtime in March, representing a 10% SLA credit on your monthly fee of $20,000."]

For the remaining portion of your request ($[Remaining Amount]), we were unable to approve 
a refund because [brief, factual explanation].

We understand this may not be the outcome you were hoping for. If you have questions 
or would like to discuss further, your Customer Success Manager [Name] is happy to 
speak with you.

[Agent Name]
NovaTech Customer Support
```

### 5.3 Refund Denied

```
Subject: Refund Request Update — Invoice #[Invoice Number]

Hi [Customer Name],

Thank you for your patience while we reviewed your refund request for $[Amount].

After a thorough review, we are unable to approve a refund in this instance because 
[clear, factual, non-technical explanation].

While we cannot process a refund, we would like to offer [alternative if applicable — 
e.g., "a 30-day subscription extension" / "an account credit of $X toward your next renewal"].

If you believe we have made an error in this determination, or if you would like to 
discuss further, please don't hesitate to reply to this ticket or request a call with 
your Customer Success Manager, [Name].

We value your business and are committed to finding a resolution that works for both parties.

[Agent Name]
NovaTech Customer Support
```

---

## 6. Refund Execution

### 6.1 Credit Card Refund (via Stripe)

Once a refund is approved:

1. Log into Stripe Dashboard: `https://dashboard.stripe.com` (Finance team access only)
2. Navigate to the payment: Payments → search by customer name or invoice ID
3. Click **Refund** and enter the approved amount
4. Select reason: `Duplicate` / `Fraudulent` / `Requested by Customer` as appropriate
5. Copy the Stripe refund ID (e.g., `re_1OqXXXXXXXXXXXX`)
6. Update the Zendesk ticket with the Stripe refund ID and confirmation
7. Send the `REFUND-APPROVED` template to the customer

### 6.2 Account Credit (Alternative to Cash Refund)

For customers preferring account credit (or when cash refund is not contractually required):
1. Log into Chargebee: `https://app.chargebee.com`
2. Find the customer subscription
3. Add a **promotional credit** with description: "SLA Credit — [Month/Incident]" or "Refund Credit — [Reason]"
4. Set expiry: 12 months from today
5. Document in Zendesk ticket

### 6.3 Audit Log Requirements

All refund decisions (approved and denied) must be logged in:
1. The Zendesk ticket (full decision rationale)
2. The Refund Log Google Sheet (`Finance > Refunds > 2026 Refund Log`) — maintained by Finance
3. Stripe (automatic for processed refunds)

Refund log columns: date, customer, ticket_id, amount_requested, amount_approved, reason, approver, stripe_refund_id, notes

---

## 7. Escalation and Exceptions

### 7.1 Customer Disputes the Decision

If a customer disputes a refund denial:
1. Escalate to Head of Customer Support
2. CSM and AE are notified
3. If customer threatens legal action: Legal team notified within 24 hours
4. No further commitment made without Legal review

### 7.2 Chargeback Risk

If a customer files a credit card chargeback:
1. Finance team is automatically notified by Stripe
2. Finance team works with Support to gather evidence (contract, usage logs, MSA)
3. Stripe dispute response must be submitted within **7 calendar days**
4. Legal team involved if chargeback > $5,000

---

*This SOP is maintained by the Head of Customer Support and Finance Manager. For questions, contact jennifer.osei@novatech.com or ana.reyes@novatech.com.*
