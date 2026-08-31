# NovaTech Solutions — Revenue Recognition Policy

**Document Owner:** Finance Department  
**Policy Number:** FIN-POL-011  
**Effective Date:** January 1, 2026  
**Last Reviewed:** November 30, 2025  
**Next Review Date:** November 30, 2026  
**Approved By:** Priya Nair, CFO (Interim); Margaret Liu, VP Finance  
**External Auditor Reviewed:** Deloitte & Touche LLP (FY2025 audit)  
**Accounting Standard:** ASC 606 — Revenue from Contracts with Customers  
**Version:** 2.1  

---

## Section 1: Purpose and Background

This Revenue Recognition Policy ("Policy") establishes the principles, procedures, and guidelines NovaTech Solutions follows to recognize revenue in accordance with Accounting Standards Codification (ASC) 606, *Revenue from Contracts with Customers* (and its companion standard IFRS 15 for any international reporting requirements).

NovaTech Solutions is a software-as-a-service (SaaS) company that generates revenue primarily from subscription-based software licenses, professional services, and implementation fees. The correct and consistent application of revenue recognition policies is critical for:

- Accurate financial reporting to investors, the Board of Directors, and external auditors
- Compliance with GAAP as required by investor agreements and lender covenants
- Preparation for potential public market transactions (IPO) or future M&A events
- Proper commission and bonus accrual calculations tied to revenue metrics

All employees involved in contract structuring, deal closing, invoicing, or financial reporting must understand and adhere to this Policy.

---

## Section 2: The Five-Step Revenue Recognition Model

NovaTech applies the following five-step process to each customer contract:

### Step 1: Identify the Contract with a Customer

A contract exists when:
- The agreement has been approved and both parties are committed
- Each party's rights can be identified
- Payment terms can be identified
- The contract has commercial substance
- It is probable NovaTech will collect the consideration

**Applicable contract forms at NovaTech:**
- Enterprise Subscription Agreement (fully executed, countersigned)
- Order Form referencing a Master Subscription Agreement
- Online click-through agreement (for self-service Starter/Professional tiers)
- Statement of Work (SOW) for professional services

**Portfolio practical expedient:** For Starter and Professional tier contracts with similar characteristics and duration, NovaTech applies the portfolio approach as a practical expedient, treating groups of similar contracts as a single contract when the effect would not materially differ from individual contract accounting.

### Step 2: Identify the Performance Obligations

NovaTech identifies performance obligations by assessing whether each promised good or service is distinct. A promised good or service is distinct if:
- The customer can benefit from it on its own or together with readily available resources, AND
- The promise is separately identifiable from other promises in the contract

**NovaTech's identified performance obligations:**

| Performance Obligation | Distinct? | Basis |
|---|---|---|
| SaaS subscription access | Yes | Customer can use the platform independently |
| Implementation services | Usually distinct | Delivered before or concurrent with subscription; can be provided by third parties |
| Data migration services | Usually distinct | One-time service; separable |
| Training (live sessions) | Distinct | Customer can use without training |
| Custom development | Usually distinct | Separate SOW; delivered as specified deliverable |
| Premium support tier | Distinct | Separately priced; available on a standalone basis |
| API access / add-on modules | Distinct | Can be accessed independently |

**Bundled arrangements:** In some enterprise contracts, implementation is bundled with the subscription at no additional stated price. In these cases, Finance determines whether implementation is a distinct obligation or whether the subscription and implementation together represent a single obligation to provide a fully configured platform.

### Step 3: Determine the Transaction Price

The transaction price is the amount NovaTech expects to be entitled to in exchange for transferring promised goods or services, excluding amounts collected on behalf of third parties (sales taxes).

**Fixed consideration:** Most NovaTech contracts include fixed subscription fees as stated in the Order Form. These are straightforward to determine.

**Variable consideration:** NovaTech's contracts may include variable elements:
- Usage-based overage charges (API calls, data storage, active users above contracted limit)
- Volume discounts (tiered pricing based on seats)
- Penalties or service credits (SLA credits under enterprise agreements)
- Refunds (per the Refund and Cancellation Policy)

Variable consideration is estimated using the **most likely amount** method for binary outcomes (e.g., will an overage fee apply or not?) and the **expected value** method for a range of possible outcomes. Variable consideration is included in the transaction price only to the extent it is probable that a significant revenue reversal will not occur.

**Significant financing component:** NovaTech evaluates whether contracts contain a significant financing component when payment timing significantly differs from the delivery of services. Annual subscriptions billed upfront are not considered to contain a significant financing component because the practical expedient for contracts of one year or less applies.

**Non-cash consideration:** Stock-based payments or barter arrangements (none currently outstanding) would be measured at fair value of the consideration received.

### Step 4: Allocate the Transaction Price

For contracts with multiple performance obligations, the transaction price is allocated based on **Standalone Selling Prices (SSP)**.

**SSP Determination Methods:**

| Performance Obligation | SSP Method | Current SSP Range |
|---|---|---|
| SaaS subscription | Observable — based on standalone contract pricing by tier | Starter: $299–$999/mo; Professional: $2,500–$15,000/mo; Business: $8,000–$25,000/mo; Enterprise: $20,000–$75,000/mo |
| Implementation services | Adjusted market assessment / cost plus margin | $5,000–$50,000 per engagement |
| Training | Observable — list rate | $2,500/day (onsite); $1,500/day (virtual) |
| Premium support | Observable — separately listed in Order Form | 20% of annual subscription fee |
| Custom development | Cost plus margin | $250–$350/hour depending on complexity |

**Residual approach:** Used when the SSP of a performance obligation is highly variable or uncertain and is not observable in standalone transactions. Allocated as the transaction price less the sum of SSPs of all other performance obligations.

### Step 5: Recognize Revenue When (or As) Performance Obligations Are Satisfied

Revenue is recognized when control of the promised goods or services is transferred to the customer.

| Performance Obligation | Recognition Pattern | Rationale |
|---|---|---|
| SaaS subscription | Over time — ratably | Customer simultaneously receives and consumes the benefit; NovaTech performs continuously |
| Implementation services | Over time — % completion | Customer receives benefit as milestones are completed; effort consumed by NovaTech |
| Data migration | Point in time or over time | When migration is complete and customer has access to migrated data |
| Training services | Point in time (per session) | Benefit received when session is delivered |
| Custom development | Point in time or over time | Based on whether customer controls asset as it is created |
| Premium support | Over time — ratably | Continuous stand-ready obligation |

---

## Section 3: Subscription Revenue Recognition

### 3.1 Monthly Subscriptions

Monthly subscription revenue is recognized in the calendar month to which it relates. A customer billed on the 15th of the month is recognized from the 15th through the 14th of the following month on a daily straight-line basis.

**Journal Entry — Monthly Subscription Billed and Collected:**
```
DR  Accounts Receivable          $7,600
    CR  Deferred Revenue                  $7,600
(upon invoicing — billing triggers receivable and deferred revenue)

DR  Deferred Revenue             $7,600
    CR  Subscription Revenue             $7,600
(at month end — revenue recognized for the month of service)
```

### 3.2 Annual Subscriptions

Annual subscriptions are billed in advance (typically at contract execution or renewal). The full invoice amount is recorded as deferred revenue upon billing and recognized ratably over the 12-month subscription period.

**Example:** ACME Corp Enterprise contract — $240,000 annual, billed January 15, 2025.
- Monthly recognized: $240,000 / 12 = $20,000/month
- Recognition period: January 15, 2025 – January 14, 2026

**Journal Entries:**
```
Upon billing (January 15, 2025):
DR  Accounts Receivable       $240,000
    CR  Deferred Revenue              $240,000

Monthly recognition (each month):
DR  Deferred Revenue          $20,000
    CR  Subscription Revenue          $20,000
```

### 3.3 Mid-Period Contract Modifications

When a customer upgrades, downgrades, or modifies their contract mid-period, NovaTech evaluates whether the modification:
- Adds distinct goods/services at a standalone price (treated as a separate contract — no impact on existing recognition)
- Modifies existing performance obligations (prospective or cumulative catch-up treatment required)

Upgrades: Prospective recognition of the new blended rate from the modification date.
Downgrades: Any excess already-recognized revenue is assessed; credits issued per the Refund Policy.

---

## Section 4: Implementation and Setup Fees

### 4.1 Treatment as Distinct Performance Obligation

When implementation services are determined to be distinct (see Step 2), the fee allocated to implementation is recognized using the **output method** (based on milestones achieved) or the **input method** (based on hours incurred) over the implementation project timeline, typically 4–12 weeks.

### 4.2 Treatment When Not Distinct

When implementation is bundled with and not distinct from the subscription (e.g., configuration-only services that don't transfer a distinct benefit), the combined transaction price (subscription + implementation) is recognized ratably over the expected customer relationship period.

**Expected customer life assumption:** Currently estimated at 36 months based on historical customer retention data (as of December 31, 2025). This assumption is reviewed annually.

**Journal Entry — Bundled Implementation Fee:**
```
Upon billing $15,000 implementation fee:
DR  Accounts Receivable        $15,000
    CR  Deferred Revenue (Implementation)   $15,000

Monthly recognition ($15,000 / 36 months = $416.67/month):
DR  Deferred Revenue           $416.67
    CR  Professional Services Revenue      $416.67
```

---

## Section 5: Professional Services Revenue

### 5.1 Percentage of Completion Method

Professional services (custom development, consulting engagements, data migration projects) are recognized over time using the percentage of completion method based on hours incurred as a proportion of total estimated hours.

**Formula:** Revenue Recognized = (Hours Incurred to Date / Total Estimated Hours) × Total Contract Value

**Example:** SOW for $50,000 custom integration. Estimated 200 hours total. 80 hours incurred through period end.
- % complete: 80/200 = 40%
- Revenue recognized: 40% × $50,000 = $20,000

### 5.2 Project Cost Overruns

If estimated total hours increase due to project complexity, NovaTech reassesses the percentage complete and recognizes revenue on the updated estimate. Cost overruns that render a project loss-generating require immediate recognition of the full expected loss (loss contract accounting under ASC 606-10-25-7).

### 5.3 Time and Materials Billing

For time-and-materials engagements billed at agreed hourly rates, NovaTech applies the right-to-invoice practical expedient, recognizing revenue in the amount it has the right to invoice (i.e., hours worked × rate), as this directly corresponds to the value of services delivered.

---

## Section 6: Variable Consideration — Usage-Based Revenue

### 6.1 Overage Fees

Customers who exceed contracted user or usage limits are billed overage fees per the pricing schedule. These overages are variable consideration and are estimated and constrained as follows:

- API call overages: Estimated based on trailing 3-month average usage + 10% growth assumption
- User overages: Constrained to $0 estimate until confirmed by actual usage data (binary outcome)
- Storage overages: Estimated based on current usage trajectory

### 6.2 Revenue Constraint

Variable consideration is included in the transaction price only to the extent it is probable a significant revenue reversal will not occur. NovaTech applies a conservative constraint and only recognizes overage revenue once the overage is confirmed (for usage) or once it is highly probable (for user-based overages with a track record).

---

## Section 7: Contract Assets and Liabilities

### 7.1 Contract Liabilities (Deferred Revenue)

Deferred revenue represents billings in advance of revenue recognition. This is NovaTech's primary contract liability and is presented as a current liability on the balance sheet (as it is expected to be recognized within 12 months for subscription revenue).

**Deferred Revenue Rollforward (FY2025):**

| | Amount |
|---|---|
| Balance, January 1, 2025 | $2,420,000 |
| Billings during 2025 | $19,850,000 |
| Revenue recognized during 2025 | $(18,430,000) |
| **Balance, December 31, 2025** | **$3,840,000** |

### 7.2 Contract Assets (Unbilled Receivables)

Contract assets arise when NovaTech has satisfied a performance obligation before billing the customer. This occurs in professional services engagements billed monthly in arrears. Contract assets are presented net of allowances.

**Balance, December 31, 2025:** $185,000

---

## Section 8: Practical Expedients Applied

NovaTech has elected the following practical expedients under ASC 606:

| Expedient | Election | Rationale |
|---|---|---|
| Portfolio approach | Elected for Starter and Professional tier contracts | Similar characteristics; immaterial difference from individual accounting |
| Significant financing component | Not assessed for contracts ≤ 1 year | Practical expedient elected |
| Incremental costs of obtaining contracts | Capitalized and amortized when > $5,000; expensed when ≤ $5,000 | Proportionality |
| Right to invoice | Elected for T&M professional services | Directly corresponds to value provided |
| Disclosure — remaining performance obligations | Not disclosed for contracts ≤ 1 year | Practical expedient elected |

---

## Section 9: Costs to Obtain and Fulfill Contracts

### 9.1 Sales Commissions

Sales commissions paid to NovaTech's sales team upon contract execution are incremental costs of obtaining contracts and are capitalized as a contract cost asset (ASC 340-40) when the expected amortization period exceeds one year.

- **Amortization period:** Consistent with the expected customer life (36 months) for new customer commissions
- **Renewal commissions:** Amortized over the renewal period (typically 12 months)
- **Expense elections:** Commissions on contracts with an amortization period of 12 months or less are expensed as incurred

**FY2025 Commission Asset Balance:** $842,000 (net of $380,000 amortization recognized in FY2025)

---

*This Policy is maintained by the Finance team and reviewed annually. Changes to accounting standards or significant changes to NovaTech's business model may require updates to this Policy between scheduled reviews. All questions should be directed to the Controller, James Tran (j.tran@novatech.io) or VP Finance, Margaret Liu (margaret.liu@novatech.io).*

*© 2026 NovaTech Solutions, Inc. | 580 Market Street, Suite 1200 | San Francisco, CA 94104*
