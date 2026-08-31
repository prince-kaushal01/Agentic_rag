# NovaTech Solutions — Support Scripts and Response Templates

**Document Version:** 2.6  
**Last Updated:** March 1, 2026  
**Authors:** Jennifer Osei (Head of Customer Support), Grace Nwosu (Tier 2 Lead)  
**Classification:** Internal — Customer Support  
**Review Cycle:** Monthly (high-use templates reviewed monthly; others quarterly)

---

## Instructions for Use

These templates are **starting points**, not scripts to copy-paste verbatim. Personalize every response:
- Use the customer's name
- Reference the specific issue they reported
- Use the correct ticket number
- Insert real ETAs and resolution details when available

Templates are numbered for reference in the playbook. Format: `[CATEGORY]-[NUMBER]-[DESCRIPTOR]`

---

## 1. Initial Response Templates

### INIT-01: Initial Response — P0 (Platform Down)

**Subject:** [URGENT] NovaTech Incident — We're on it | Ticket #TKT-XXXX

```
Hi [Name],

I'm [Agent Name], and I'm handling your urgent report personally.

We have confirmed a service disruption and our engineering team is actively responding 
right now. This is our highest priority.

Current Status: Actively investigating
Started: [time] PT
Affected: [brief description]

I will update you every 15 minutes until this is resolved. You can also monitor 
real-time status at status.novatech.io.

If you need to reach me directly: [agent phone or Slack Connect channel]

[Agent Name]
NovaTech Customer Support — P0 Response Team
```

---

### INIT-02: Initial Response — P1 (Major Feature Degraded)

**Subject:** Re: [Customer Subject] | NovaTech Support Ticket #TKT-XXXX

```
Hi [Name],

Thank you for reaching out. I'm [Agent Name] from NovaTech Support, and I'm personally 
taking ownership of this issue.

I've confirmed this is a P1 priority and our technical team is engaged. Here's where 
we stand:

Issue: [brief, plain-language description of what we understand the problem to be]
Status: [Investigating / Identified / Fix in progress]
Expected Update: Within [1/2] hour(s)

In the meantime: [If workaround exists — "Here's a workaround that may help:..." 
If not — "There is no workaround at this time. I'm sorry for the impact to your team."]

I'll keep you updated every hour. Please don't hesitate to reply to this email or 
contact me directly at [contact info].

[Agent Name]
NovaTech Customer Support
Ticket: TKT-XXXX
```

---

### INIT-03: Initial Response — P2 (Partial/Minor Degradation)

**Subject:** Re: [Customer Subject] | NovaTech Support Ticket #TKT-XXXX

```
Hi [Name],

Thank you for contacting NovaTech Support. I'm [Agent Name] and I'll be handling your 
ticket (TKT-XXXX).

I've reviewed your report and want to confirm a few details to make sure we investigate 
this thoroughly:

[Choose the relevant questions:]
- When did you first notice this issue?
- Is it affecting all users or specific users?
- Can you share the exact error message (screenshot or copy-paste)?
- What browser and OS version are you using?
- Has anything changed recently in your setup or SSO configuration?

While I gather this information, I've checked our Known Issues list and [there is a 
known issue that may be related: [KI-XXX — brief description and workaround] / this 
does not appear to be a known issue, so I'll investigate further].

I'll follow up within [4/8] business hours with an update.

[Agent Name]
NovaTech Customer Support
```

---

### INIT-04: Initial Response — P3 (Low Priority / Minor Issue)

**Subject:** Re: [Customer Subject] | NovaTech Support Ticket #TKT-XXXX

```
Hi [Name],

Thank you for reaching out! I'm [Agent Name] from NovaTech Support.

I've received your ticket (TKT-XXXX) and will look into this for you. Based on your 
description, this appears to be a low-impact issue, but I want to make sure it's fully 
resolved.

[If KB article answers it:]
I believe this article addresses your question: [link]. Let me know if that solves it 
or if you have additional questions.

[If investigation needed:]
I'll investigate and get back to you within 1 business day with an update.

Thanks for bringing this to our attention!

[Agent Name]
NovaTech Customer Support
```

---

## 2. Investigation and Escalation Templates

### ESC-01: Escalating to Engineering

**Subject:** Re: [Customer Subject] | TKT-XXXX — Engineering Team Engaged

```
Hi [Name],

I wanted to update you on the progress of your ticket (TKT-XXXX).

Our Tier 2 technical team has completed their initial investigation and confirmed that 
this requires engineering involvement. I've escalated to our [Platform/Product/Data] 
engineering team, and they are actively working on it.

Engineering Ticket: ENG-XXXX (our internal tracking reference)
Status: [Investigating / Root cause identified / Fix in progress]
[If known:] Expected Resolution: [date] based on engineering's assessment

[If applicable:] Workaround: While we work on a permanent fix, here is a workaround 
that may reduce the impact on your team: [describe workaround clearly]

I will continue to own this ticket and provide updates every [4/24] hours. You will 
hear from me before [specific date/time] with the next update.

Thank you for your patience.

[Agent Name]
NovaTech Customer Support
```

---

### ESC-02: Awaiting Customer Information

**Subject:** Re: [Customer Subject] | TKT-XXXX — Information Needed

```
Hi [Name],

Thank you for reaching out. To investigate this issue fully, I need a bit more 
information from your team:

1. [Specific question 1]
2. [Specific question 2]
3. [Specific question 3 — e.g., "Can you share a screenshot of the error message?"]

The more detail you can provide, the faster we can identify the root cause.

If I don't hear back within 3 business days, I'll follow up with you, but the ticket 
will be put on hold until we receive this information.

Thank you for your help — we'll get this resolved quickly once we have the details.

[Agent Name]
NovaTech Customer Support
Ticket: TKT-XXXX
```

---

## 3. Resolution Templates

### RES-01: Resolution Confirmation — Standard

**Subject:** Resolved: [Customer Subject] | TKT-XXXX

```
Hi [Name],

Great news — the issue you reported (TKT-XXXX) has been resolved.

What was the issue: [Plain-language description]
Root cause: [Plain-language, non-jargon explanation]
What we fixed: [Brief description of the fix]
Deployed: [Date/time]

To verify: [Tell them exactly how to confirm it's working — e.g., "Please try 
searching for [query] and confirm results appear within 2 seconds."]

If you experience any further issues with this, please reply directly to this email 
and I'll re-open the ticket immediately.

We're sorry for the disruption to your workflow. [If applicable: "We'll follow up 
shortly with information about an SLA credit for the downtime you experienced."]

You may receive a brief survey asking about your support experience. Your feedback 
genuinely helps us improve.

[Agent Name]
NovaTech Customer Support
```

---

### RES-02: Resolution Confirmation — Known Issue Fixed (Multiple Customers)

**Subject:** Fix Deployed: [Issue Name] | TKT-XXXX

```
Hi [Name],

I'm happy to let you know that the [brief issue description] that you reported has 
been resolved in today's release (v[X.X.X]).

The fix is live in production as of [date/time] PT. No action is required on your end.

To confirm the fix: [specific verification steps]

Thank you for your patience while we worked through this issue. Your report helped us 
identify and prioritize the fix.

[Agent Name]
NovaTech Customer Support
```

---

## 4. SLA and Credit Templates

### SLA-01: SLA Credit Notification

**Subject:** SLA Credit Applied — [Month Year] | NovaTech Account

```
Hi [Name],

Following the [service/feature] disruption on [date], we have calculated the SLA 
impact for your account and are proactively issuing a credit.

SLA Credit Details:
• Incident: [Brief description]
• Date/Duration: [Date], [X minutes/hours] of degraded service
• Your SLA commitment: [99.9% / 99.95%]
• Measured uptime during March 2026: [X.XX%]
• Credit Amount: $[Amount] ([X]% of your [monthly/annual] fee)
• Applied To: Your next invoice (due [date])

This credit has been applied automatically — no action is required from you.

We sincerely apologize for the impact to your team. We have completed a root cause 
analysis and implemented the following improvements to prevent recurrence: 
[brief list of preventative measures]

If you have any questions about this credit or would like to discuss the incident 
further, please don't hesitate to reply or contact your Customer Success Manager, 
[CSM Name], at [CSM email].

[Agent Name]
NovaTech Customer Support
```

---

## 5. Refund Templates

### REFUND-01: Refund Intake

*(See Refund Request Process document for full intake template)*

**Subject:** Refund Request Received — NovaTech Support Ticket #TKT-XXXX

```
Hi [Name],

Thank you for contacting us about a refund. I've created ticket TKT-XXXX to track 
your request.

To complete our review, I need:
1. The invoice number(s) you're requesting a refund for
2. The reason for your refund request  
3. [If SLA related:] The dates of service issues you experienced
4. [If billing error:] The amount you were charged vs. what you expected

Our team will review within 5 business days and get back to you with a decision.

[Agent Name]
NovaTech Customer Support
```

---

### REFUND-02: Refund Approved (Full)

**Subject:** Refund Approved — $[Amount] | Invoice #[Number]

```
Hi [Name],

Good news — we have approved a full refund of $[Amount] for Invoice #[Invoice Number].

Refund Details:
• Amount: $[Amount]
• Method: [Credit to original payment method / Account credit]
• Timeline: 5–10 business days to appear on your statement
• Reason: [Brief explanation]

If you have any questions, please reference ticket TKT-XXXX.

[Agent Name]
NovaTech Customer Support
```

---

### REFUND-03: Refund Denied

**Subject:** Refund Request Update | TKT-XXXX

```
Hi [Name],

Thank you for your patience while we reviewed your refund request for $[Amount].

After thorough review, we are unable to approve this refund because [clear, factual, 
respectful explanation — e.g., "the service was fully accessible and functioning 
during the period in question, and the charge matches your contracted rate"].

We understand this isn't the answer you were hoping for. To help in another way, 
we'd like to offer: [alternative — e.g., a free 30-day extension / account credit / 
priority support for your next issue].

If you believe we've made an error, please reply to this ticket and we'll review again.

[Agent Name]
NovaTech Customer Support
```

---

### REFUND-04: Partial Refund Approved

**Subject:** Partial Refund Approved — $[Amount] | TKT-XXXX

```
Hi [Name],

After reviewing your request, we've approved a partial refund of $[Amount] 
(of the $[Requested Amount] requested).

How we calculated this: [clear explanation — e.g., "This reflects the 18 minutes of 
confirmed downtime per our monitoring, representing a 10% SLA credit on your $20,000 
monthly fee."]

For the remaining $[Difference]: [brief explanation of why the full amount was not 
approved].

Refund Method: [method] | Timeline: 5–10 business days

Your CSM [Name] is available to discuss if you have questions.

[Agent Name]
NovaTech Customer Support
```

---

## 6. Status Page and Incident Communication Templates

### INC-01: Service Degradation — Public StatusPage Post

```
[Service Name] Performance Degradation
We are investigating reports of [description — e.g., "slow search response times"] 
affecting some customers. Our engineering team is actively investigating.

Impact: [e.g., "Search query response times elevated to 5–12 seconds for some users"]
Started: [time] PT
Status: Investigating

We will provide an update within 30 minutes.
```

---

### INC-02: Service Degradation — Update

```
[Service Name] Performance Degradation — Update
We have identified the root cause: [brief technical description without jargon]. 
Our team is actively implementing a fix.

Expected resolution: [time] PT
Next update: In 30 minutes
```

---

### INC-03: Service Restored

```
[Service Name] — Resolved
The [issue description] has been resolved as of [time] PT.

Duration: [X hours Y minutes]
Root cause: [brief plain-language explanation]

All systems are operating normally. We apologize for the disruption.
A full post-incident summary will be published at status.novatech.io within 5 business days.
```

---

## 7. Proactive Communication Templates

### PROACT-01: Planned Maintenance Notification (14 Days)

**Subject:** Upcoming Planned Maintenance — [Date] | NovaTech

```
Hi [Name],

We want to give you advance notice of scheduled maintenance on the NovaTech platform:

Maintenance Window: [Day, Date] from [Time] to [Time] PT
Duration: Up to [X] hours (typically shorter)
Impact: [Brief description — e.g., "The platform will be unavailable during this window"]
Purpose: [Brief explanation — e.g., "Database upgrade to improve performance and security"]

This maintenance falls within our standard Sunday 2–4 AM PT window and does not count 
against your SLA uptime commitment.

If you have any questions or if this timing is particularly problematic, please reply 
to this email. We will do our best to accommodate.

[Agent Name / CSM Name]
NovaTech Customer Success
```

---

### PROACT-02: Renewal Reminder (90 Days)

**Subject:** Your NovaTech Subscription Renews on [Date]

```
Hi [Name],

I wanted to reach out personally to let you know that your NovaTech subscription 
renews on [Date] — about 90 days from now.

Your current plan: [Plan] | [X] users | $[Amount]/year

This is a great time to:
• Review your usage and make sure your seat count is right for your team
• Discuss any features or upgrades you've been considering
• Ask about our latest innovations (AI Q&A is now in beta!)

I'd love to schedule a quick call to discuss your experience and make sure NovaTech 
is set up to serve your team well going into [Year]. 

Would [date/time] work for a 30-minute chat?

[CSM Name]
Customer Success Manager, NovaTech Solutions
```

---

### PROACT-03: Executive Escalation Response

**Subject:** Personal Response to Your Concerns | NovaTech — [Company Name]

```
Dear [Executive Name],

I'm [Name, Title] at NovaTech Solutions. I'm writing personally in response to 
your escalation regarding [issue].

I want to start by sincerely apologizing. [Specific acknowledgment of the impact — 
e.g., "I understand that the search performance issue has materially impacted your 
legal team's productivity, and that is unacceptable for a platform you depend on 
every day."]

Here is exactly what we are doing about it:
• [Action 1 with owner and date]
• [Action 2 with owner and date]  
• [Resolution timeline: "Our engineering team is committed to resolving this by [date]"]

I am personally committed to ensuring this is resolved to your satisfaction. I would 
like to schedule a call with you and [Engineering Lead name] this week to walk through 
the technical plan in detail.

Would [Date] at [Time] PT work for you? Alternatively, please suggest a time that 
works better.

Sincerely,
[Name]
[Title], NovaTech Solutions
[Direct phone]
```

---

### CSAT-01: CSAT Follow-Up (After Survey Received)

**Subject:** Thank you for your feedback | NovaTech Support

```
Hi [Name],

Thank you for taking the time to rate your recent support experience. 

[If score 4-5:] We're delighted to hear we were able to help! Your feedback means a 
lot to our team.

[If score 1-3:] I'm sorry to hear we didn't meet your expectations on ticket TKT-XXXX. 
Your feedback is important to us, and I'd like to understand what we could have done 
better. Would you have 10 minutes for a quick call this week?

Thank you again for helping us improve.

[Agent Name]
NovaTech Customer Support
```

---

*Templates maintained by Jennifer Osei. To suggest a new template or revise an existing one, post in #support-templates on Slack or email jennifer.osei@novatech.com. All template changes require Head of Support approval before use.*
