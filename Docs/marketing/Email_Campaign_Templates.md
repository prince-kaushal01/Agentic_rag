# NovaTech Solutions — Email Campaign Template Library
**Version:** 1.6
**Owner:** Rachel Torres, VP of Marketing
**Platform:** HubSpot Marketing Hub
**Last Updated:** February 14, 2026
**Usage:** All templates must be deployed via HubSpot. Do not send marketing emails outside of HubSpot without approval from Marketing Ops.

---

## Overview

This document contains the master copy for all recurring and campaign-specific email templates used by the NovaTech Solutions marketing team. Templates are designed for the HubSpot email editor and use personalization tokens noted in `{{double_curly_braces}}`.

**Global Email Signature (append to all templates):**
```
—
The NovaTech Solutions Team
www.novatech.io | help.novatech.io | Unsubscribe | Privacy Policy
NovaTech Solutions, Inc. | 535 Mission Street, Suite 1400 | San Francisco, CA 94105
```

---

## 1. Welcome Sequence (5 Emails — Triggered on New Trial Signup)

### Email W1 — Immediate (Send: T+0 minutes after signup)
**Subject Line Options:**
- A: "Welcome to NovaTech, {{first_name}}. Your 14-day trial starts now."
- B: "You're in, {{first_name}} — here's how to get started with NovaTech"

**Preview Text:** "It takes 14 minutes to connect your first knowledge source. Let's do it."

**Body:**
```
Hi {{first_name}},

Welcome to NovaTech Solutions. Your 14-day free trial is active.

Here's what to do first:

1. Connect your first knowledge source
   Takes 2 minutes. Connect Confluence, SharePoint, Google Drive, or Notion.
   → [Connect a source]

2. Ask your first question
   Type a real question your team asks every day. See how NovaTech answers it.
   → [Open NovaTech Search]

3. Invite a teammate
   Knowledge management is a team sport. Add up to 5 colleagues to your trial.
   → [Invite teammates]

If you have any questions, reply to this email or chat with us at novatech.io.

Your Customer Success Manager is {{csm_name}}. You'll hear from them within 1 business day.

Let's get started,
The NovaTech Team
```

---

### Email W2 — Day 1 (Send: T+24 hours)
**Subject Line Options:**
- A: "{{first_name}}, did you connect your first source?"
- B: "One question your team asked today — and how NovaTech would answer it"

**Preview Text:** "Most teams connect in under 10 minutes. Here's a quick video."

**Body:**
```
Hi {{first_name}},

Quick check-in: have you connected your first knowledge source yet?

If not, here's a 2-minute video showing exactly how:
→ [Watch: Connect Confluence to NovaTech in 2 minutes] (Loom embed)

If you have — great! Here's what to try next:

• Search for something your team asks frequently
• Use natural language: "What is our policy on expense reimbursement?"
• Notice the source citations — NovaTech tells you exactly where each answer came from

Questions? Here's what our customers asked on Day 1:
→ [Day 1 FAQ — help.novatech.io]

Talk soon,
{{csm_name}}
Customer Success, NovaTech Solutions
```

---

### Email W3 — Day 3 (Send: T+72 hours)
**Subject Line Options:**
- A: "What's working (and what's not) after 3 days — NovaTech tips"
- B: "3 things our best customers do in their first week"

**Preview Text:** "Teams that do these 3 things retain 94% after trial. Here's what they are."

**Body:**
```
Hi {{first_name}},

You're 3 days into your NovaTech trial. Here's what the most successful teams do
in their first week:

1. Connect at least 3 knowledge sources
   Teams with 3+ connected sources find answers 4× more often than teams with 1.
   Currently connected: {{connected_sources_count}} source(s)
   → [Connect more sources]

2. Ask 10+ questions
   The search model improves as it learns what your team searches for.
   Your team has asked {{query_count}} questions so far.
   → [Search now]

3. Invite their manager or a cross-functional colleague
   When multiple departments use NovaTech, knowledge sharing improves 67%.
   → [Invite a colleague]

Also: we have a live Q&A every Thursday at 12pm PT.
→ [Register for this week's session]

Best,
{{csm_name}}
```

---

### Email W4 — Day 7 (Send: T+7 days)
**Subject Line Options:**
- A: "Halfway through your trial — are you getting value?"
- B: "{{first_name}}, your NovaTech trial is 50% done. Here's a quick check-in."

**Preview Text:** "Let's make sure you see the value before your trial ends."

**Body:**
```
Hi {{first_name}},

You're halfway through your NovaTech trial. Let's make sure it's working for you.

Your trial summary:
• Sources connected: {{connected_sources_count}}
• Questions asked: {{query_count}}
• Team members active: {{active_users}}

If those numbers look low, let's fix that. Book a 20-minute call with {{csm_name}}
and we'll get your team fully set up before the trial ends.
→ [Book a call]

If things are going well — great! Here's what to think about next:

• Do you want to bring more of your team on board?
• Are there integrations you haven't connected yet? (Slack, Jira, GitHub, Salesforce)
• Ready to see NovaTech pricing?
→ [View pricing]

We're here to help.
{{csm_name}}
```

---

### Email W5 — Day 12 (Send: T+12 days — 2 days before trial ends)
**Subject Line Options:**
- A: "Your NovaTech trial ends in 2 days — here's how to continue"
- B: "Don't lose your NovaTech setup, {{first_name}}"

**Preview Text:** "Your connected sources, search history, and team setup are waiting."

**Body:**
```
Hi {{first_name}},

Your NovaTech free trial ends in 2 days ({{trial_end_date}}).

After your trial ends, your workspace will be paused — but not deleted. Everything
you've set up (connected sources, search history, team members) is saved for 30 days.

Ready to continue? Choose the plan that fits your team:
→ [View Plans and Pricing]

Not ready yet? That's okay. Here are two options:

1. Talk to us — If you have questions about pricing, implementation, or enterprise
   features, book 20 minutes with your CSM.
   → [Book a call with {{csm_name}}]

2. Request an extension — If you need more time to evaluate, we can extend your
   trial by 7 days.
   → [Request a 7-day extension]

Thank you for trying NovaTech. We hope it's been valuable.
The NovaTech Team
```

---

## 2. Prospect Nurture Sequence (8 Emails — Triggered on MQL)

### Email N1 — Day 0 (MQL Welcome — SDR Follow-up Pair)
**Subject Line:** "{{first_name}}, here's what to expect from NovaTech"
**Preview Text:** "3 resources to help you evaluate NovaTech — no pressure."

**Body:**
```
Hi {{first_name}},

Thanks for your interest in NovaTech Solutions. I'm {{sender_name}} from the
NovaTech team.

To help you evaluate whether NovaTech is right for {{company}}, here are 3 resources:

1. [The Enterprise Knowledge Management Buyer's Guide 2026] — 12-page guide to
   evaluating enterprise knowledge platforms (including questions to ask vendors)

2. [The {{industry}} Knowledge Management Case Study] — How a company like yours
   solved knowledge fragmentation

3. [5-minute product demo video] — See NovaTech in action, no meeting required

If you'd like a live demo or have specific questions, you can book time directly:
→ [Book a 30-minute demo]

No pressure — these resources are yours to keep.
{{sender_name}}, NovaTech Solutions
```

---

### Emails N2–N8 — Abbreviated Summaries

**N2 (Day 3):** "The ROI of Enterprise Search" — Subject: "How GlobalTech saved 43% in onboarding time." Sends GlobalTech case study. CTA: Book demo.

**N3 (Day 7):** "Enterprise Search Comparison" — Subject: "NovaTech vs. DataBridge vs. your current stack." Links to comparison page. CTA: Read comparison.

**N4 (Day 14):** "Security and Compliance Deep Dive" — Subject: "{{first_name}}, how NovaTech handles your data." Links to security page + SOC 2 overview. CTA: Request security documentation.

**N5 (Day 21):** "Customer Panel Webinar Invitation" — Subject: "Live: 3 enterprise customers on their NovaTech ROI [date/time]." CTA: Register for webinar.

**N6 (Day 30):** "ROI Calculator" — Subject: "What would NovaTech save {{company}}? Calculate it." Links to ROI calculator tool. CTA: Calculate your ROI.

**N7 (Day 45):** "Re-engagement Check-in" — Subject: "{{first_name}}, still evaluating knowledge management tools?" Soft check-in from CSM. CTA: Book a call.

**N8 (Day 60):** "Final Nurture" — Subject: "Heading out of {{first_name}}'s inbox — but leaving something useful." Links to free downloadable RFP template for knowledge management. CTA: Download RFP template.

---

## 3. Product Announcement Template

**Subject Line Options:**
- A: "New: [Feature Name] — now available in NovaTech"
- B: "[Feature Name] is here — here's what you can do with it"

**Preview Text:** "Live now for all [plan type] customers. Here's how to try it."

**Body:**
```
Hi {{first_name}},

We're excited to share that [FEATURE NAME] is now available in your NovaTech
account.

[FEATURE NAME] lets you [one-sentence description of the primary use case].

Here's what you can do with it:
• [Benefit 1 — specific, concrete]
• [Benefit 2 — specific, concrete]
• [Benefit 3 — specific, concrete]

→ [Try [FEATURE NAME] now]
→ [Read the documentation]
→ [Watch a 3-minute overview]

[FEATURE NAME] is available to all [Standard / Professional / Enterprise] plan
customers starting today.

If you have questions, your Customer Success Manager is here:
→ [Book time with {{csm_name}}]

The NovaTech Product Team
```

---

## 4. Event Invitation Template

**Subject Line Options:**
- A: "{{first_name}}, you're invited: [Event Name] on [Date]"
- B: "Save your spot — [Event Name] [Date]"

**Preview Text:** "[One-sentence value proposition for attending]"

**Body:**
```
Hi {{first_name}},

You're invited to [EVENT NAME].

[DATE] | [TIME] [TIMEZONE] | [FORMAT: Virtual / In-Person / Location]

What you'll learn:
• [Session/topic 1]
• [Session/topic 2]
• [Session/topic 3]

Featuring:
• [Speaker 1, Title, Company]
• [Speaker 2, Title, Company]
• [NovaTech speaker, if applicable]

Who should attend:
[Target persona description — 1 sentence]

Reserve your spot — [attendance cap or urgency indicator if applicable]:
→ [Register now]

Questions? Reply to this email or contact {{sender_name}}.
```

---

## 5. Webinar Follow-Up Template (Post-Attendance and Post-No-Show)

### Attended Version
**Subject Line:** "Thanks for joining — recording + resources inside"
**Body:**
```
Hi {{first_name}},

Thanks for attending [WEBINAR TITLE] on [DATE]. Here's everything from the session:

• [Recording link — expires in 30 days]
• [Slide deck download]
• [Key resource mentioned in session]

Top questions from the session:
Q: [Question 1 from audience]
A: [Answer — 2 sentences]

Q: [Question 2 from audience]
A: [Answer — 2 sentences]

Next steps if you're ready to explore NovaTech for {{company}}:
→ [Book a personalized demo]
→ [Start a free trial]

Talk soon,
{{sender_name}}
```

### No-Show Version
**Subject Line:** "You missed [WEBINAR TITLE] — catch the recording here"
**Body:**
```
Hi {{first_name}},

We missed you at [WEBINAR TITLE] on [DATE] — but don't worry.
The full recording is available here:
→ [Watch the recording] (45 minutes)

[Short summary — 2 sentences on what was covered]

Most popular resource from the session:
→ [Key resource link]

If you'd like a personalized walkthrough for {{company}}, I'm happy to help:
→ [Book 30 minutes with me]

{{sender_name}}, NovaTech Solutions
```

---

## 6. Customer Newsletter Template (NovaTech Insider — Monthly)

**Subject Line:** "NovaTech Insider — [Month Year]: [Top story headline]"
**Preview Text:** "[Secondary story teaser — 10 words max]"

**Sections:**
1. **From the Desk of David Huang** — 100-word CEO note on a relevant trend or company milestone
2. **Product Update** — 2–3 bullet points on recent releases with links to documentation
3. **Customer Spotlight** — 200-word customer success summary with logo and quote
4. **Upcoming Events** — Webinars, conferences, CAB meetings
5. **Did You Know?** — 1 practical NovaTech tip or lesser-known feature
6. **Resources** — 2–3 new content pieces (blog posts, case studies, guides)

---

## 7. Re-Engagement Campaign (3 Emails — Triggered: 60 Days No Activity)

### RE1 — Day 0
**Subject:** "{{first_name}}, it's been a while — still managing knowledge the hard way?"
**Body:** Soft check-in; 1 paragraph on what's new since last login; CTA: Log in to NovaTech.

### RE2 — Day 7
**Subject:** "What's new in NovaTech since you last logged in"
**Body:** 3-bullet product update summary; customer quote; CTA: See what's new.

### RE3 — Day 14 (Final)
**Subject:** "Checking in one last time, {{first_name}}"
**Body:** Final outreach from CSM; offer a re-onboarding call; if no response, move to suppressed list and notify CSM.

---

## 8. Upsell Campaign Template (Triggered by Usage Threshold)

**Trigger:** Customer on Team plan with >40 active users (approaching 50-user cap) OR connecting >4 integrations

**Subject Line Options:**
- A: "{{company}} is growing — your NovaTech plan should too"
- B: "You're close to your {{plan_name}} plan limits — here's what to do"

**Body:**
```
Hi {{first_name}},

Great news — {{company}}'s team is growing on NovaTech.

Your current {{plan_name}} plan supports up to [LIMIT]. You're currently at [USAGE].

If your team keeps growing at this rate, here's what an upgrade to [NEXT TIER]
would get you:
• [Feature/benefit 1 of next tier]
• [Feature/benefit 2 of next tier]
• [Expanded limits]

Upgrading is instant — no migration required.
→ [View Enterprise plan details]
→ [Talk to your CSM: {{csm_name}}]

The NovaTech Team
```

---

## 9. Renewal Reminder Series

### T-90 Days Before Renewal
**Subject:** "{{first_name}}, your NovaTech renewal is 90 days away — let's plan ahead"
**Preview Text:** "Review your usage, explore new features, and lock in your rate."
**Body:** Usage summary for the year; highlights of new features added; CSM contact for renewal discussion; CTA: Book renewal review call.

### T-60 Days Before Renewal
**Subject:** "60 days to renewal — your NovaTech ROI summary inside"
**Preview Text:** "Here's the impact NovaTech has had on {{company}} this year."
**Body:** Personalized usage stats (queries, users, sources, time saved estimate); renewal pricing information; CTA: Confirm renewal or discuss expansion.

### T-30 Days Before Renewal
**Subject:** "Your NovaTech renewal is next month — action required"
**Preview Text:** "Renew by [date] to lock in current pricing."
**Body:** Direct renewal CTA; urgency on pricing (price increase effective at renewal for expansions); contact CSM for PO/procurement assistance.

### T-7 Days Before Renewal
**Subject:** "Final reminder: NovaTech renewal in 7 days"
**Preview Text:** "Avoid service interruption — renew by [date]."
**Body:** Renewal link; direct CSM phone number; escalation contact (VP of CS) if procurement delays are anticipated.

---

## 10. Churned Customer Win-Back Template (Send: 30–60 Days After Churn)

**Subject Line Options:**
- A: "{{first_name}}, a lot has changed at NovaTech since you left"
- B: "We've missed {{company}} — and we've been busy"

**Preview Text:** "Three things that are different now."

**Body:**
```
Hi {{first_name}},

It's been [X weeks/months] since {{company}} was with NovaTech. We respect your
decision, and we've spent that time listening.

Here's what we've shipped since you left:
• [New feature 1 — specific, relevant to their prior pain point if known]
• [New feature 2]
• [New integration or improvement]

We also heard your feedback on [specific objection at churn if known from CSM notes].
We've addressed that by [specific response].

If you'd be open to a 20-minute call to see what's changed, I'd love to show you.
No pressure to buy — just a chance to reconnect.
→ [Book 20 minutes]

If now isn't the right time, no hard feelings. I'll check back in [90 days].

{{csm_name}} or {{ae_name}}
NovaTech Solutions
```

---

*Document Owner: Rachel Torres, VP of Marketing | rachel.torres@novatech.io*
*HubSpot Admin: Marcus Chen | All templates live in HubSpot > Marketing > Email > Templates*
*Last Full Review: February 14, 2026 | Next Review: August 2026*
