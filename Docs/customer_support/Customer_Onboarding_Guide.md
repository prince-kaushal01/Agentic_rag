# NovaTech Solutions — Customer Onboarding Guide

**Document Version:** 2.3  
**Last Updated:** January 20, 2026  
**Authors:** David Rodriguez (CSM Lead), Solutions Engineering Team  
**Classification:** Internal — Customer Success  
**Review Cycle:** Quarterly

---

## 1. Overview

NovaTech Solutions offers three onboarding tiers designed to match the complexity and size of each customer's deployment. Onboarding success is defined as: the customer has configured the platform, trained their users, and is seeing measurable value within the first 30 days.

**Onboarding Tiers:**

| Tier | Eligibility | Duration | White-Glove? | CSM Assigned? |
|------|------------|---------|-------------|--------------|
| **Self-Serve** | Free and Standard plans, < 50 users | 0–2 weeks | No | No |
| **Guided** | Professional plans, 50–200 users | 4 weeks | Partial | Shared pool CSM |
| **Enterprise White-Glove** | Enterprise plans, > 200 users, > $100K ARR | 8 weeks | Yes | Dedicated CSM |

---

## 2. Self-Serve Onboarding

Self-serve customers are directed through an in-app onboarding checklist:

1. **Account setup:** Verify email; set up 2FA; invite first team members
2. **Upload first documents:** Walk-through of drag-and-drop upload
3. **Run first search:** Guided search tutorial with sample query
4. **Explore integrations:** Prompted to connect one integration (Google Drive, Slack, etc.)
5. **Share with team:** Invite 3 colleagues

**Resources available to self-serve:**
- In-app product tour (triggered on first login)
- Video tutorial library: docs.novatech.io/videos (12 tutorials, each < 5 minutes)
- Help Center: help.novatech.io (300+ articles)
- Community forum: community.novatech.io
- Chatbot (Intercom AI): 24/7 for common questions

**Self-serve conversion goal:** 40% of self-serve customers convert to paid within 14 days.

---

## 3. Guided Onboarding (Professional)

Professional customers receive structured onboarding over 4 weeks with a shared-pool CSM:

| Week | Milestone | Activities |
|------|-----------|-----------|
| Week 1 | Account configured | Kickoff call; SSO setup; admin training |
| Week 2 | Data ingested | Bulk document upload; collection structure setup |
| Week 3 | Team onboarded | End-user training sessions (2 × 45 min group); first searches |
| Week 4 | Go-live | API integration (if applicable); success metrics review |

---

## 4. Enterprise White-Glove Onboarding (8-Week Program)

### 4.1 Timeline Overview

| Week | Phase | Key Activities | Owner |
|------|-------|--------------|-------|
| Week 0 | Pre-kickoff | Assign dedicated CSM; schedule all week 1 calls; send pre-read | CSM |
| Week 1 | Kickoff | Executive kickoff call; discovery session; technical setup kickoff | CSM + Solutions Engineer |
| Weeks 2–3 | Technical Setup | SSO; SCIM; API keys; webhook config; data migration | Solutions Engineer + Customer IT |
| Week 4 | Data Migration | Bulk document import; indexing; QA of search results | CSM + Customer IT |
| Week 5 | Admin Training | Admin console training; user management; reporting | CSM |
| Week 6 | End-User Training | Role-based training sessions; search best practices | CSM + Customer Champions |
| Week 7 | Pilot | Soft launch to pilot group (20–50 users); feedback collection | CSM |
| Week 8 | Go-Live | Full rollout; go-live confirmation; success metrics baseline | CSM + AE |

### 4.2 Kickoff Call Agenda (Week 1 — 90 Minutes)

**Participants:** Customer (IT Manager, Admin, Executive Sponsor); NovaTech (CSM, AE, Solutions Engineer)

| Time | Topic | Owner |
|------|-------|-------|
| 0:00–0:10 | Introductions and roles | CSM |
| 0:10–0:20 | Customer goals and success definition | Executive Sponsor |
| 0:20–0:35 | NovaTech platform overview (tailored to customer use case) | Solutions Engineer |
| 0:35–0:50 | Technical setup requirements and timeline | Solutions Engineer + Customer IT |
| 0:50–1:05 | Data migration approach | CSM + Customer IT |
| 1:05–1:20 | Training plan and user communication approach | CSM |
| 1:20–1:30 | Success metrics definition; QBR cadence | CSM + AE |
| 1:30 | Next steps, owners, and calendar invites | CSM |

**Pre-kickoff materials to send (3 days before):**
- Onboarding checklist (shared Google Sheet)
- Technical requirements questionnaire
- NovaTech platform overview deck
- SSO configuration guide (docs.novatech.io/sso)
- SCIM configuration guide

### 4.3 Technical Setup Checklist

**Phase 1: Authentication (Week 2)**
- [ ] SSO identity provider determined (Okta / Azure AD / Google / OneLogin)
- [ ] NovaTech service provider metadata shared with customer IT
- [ ] Customer IdP metadata URL provided to NovaTech
- [ ] SAML attribute mapping completed (email, firstName, lastName, department)
- [ ] SSO tested with 5 pilot users
- [ ] MFA enforcement policy aligned with customer requirements

**Phase 2: User Provisioning (Week 2)**
- [ ] SCIM 2.0 configured in identity provider (if Enterprise with >100 users)
- [ ] SCIM provisioning tested (create, update, deactivate user)
- [ ] Group/role mapping configured (admin group → Admin role, etc.)
- [ ] User provisioning runbook documented for customer IT team

**Phase 3: API and Integrations (Week 3)**
- [ ] API key(s) generated for integration use (scoped to minimum permissions)
- [ ] Webhook endpoint URL provided and tested (POST /v2/webhooks)
- [ ] Webhook signature verification implemented by customer developer
- [ ] Desired integrations configured: Slack / Google Drive / SharePoint / other
- [ ] Webhook events subscribed (document.created, document.deleted, user.created)

**Phase 4: Data Migration (Week 4)**
- [ ] Source system inventory completed (document count, size, formats)
- [ ] Migration approach agreed: bulk API / integration sync / manual upload
- [ ] Document metadata mapping defined (source fields → NovaTech fields)
- [ ] Collection structure designed (folder/collection hierarchy approved)
- [ ] Test migration: 100 documents → verify indexing and search
- [ ] Full migration: execute and monitor progress
- [ ] QA: sample search queries return expected results

**Phase 5: Configuration (Week 5)**
- [ ] User roles and permissions configured
- [ ] Email notification preferences set (per team/role)
- [ ] Storage quota confirmed and allocated
- [ ] Data retention policy configured (default: 7 years)
- [ ] Audit logging requirements reviewed (SOC 2 / HIPAA customers)
- [ ] IP allowlist configured (if required for security)
- [ ] Custom domain configured (e.g., novatech.acme-corp.com)

---

## 5. Admin Training Curriculum

### 5.1 Admin Training Modules (Week 5 — 3 × 60-minute sessions)

**Session 1: User Management and Access Control (60 min)**
- User lifecycle: invite, onboard, manage, deactivate
- Roles and permissions: built-in and custom roles
- SCIM provisioning monitoring and troubleshooting
- SSO configuration updates
- Audit log review and export

**Session 2: Platform Configuration and Compliance (60 min)**
- Collection and folder structure management
- Storage monitoring and quota management
- Security settings: IP allowlist, session policies, 2FA enforcement
- Compliance features: audit log, data export, retention policies
- Integration management: viewing, testing, reconfiguring

**Session 3: Analytics and Reporting (60 min)**
- Usage dashboard: active users, document counts, search volume
- Analytics API for custom reporting
- Notification center configuration
- Webhook monitoring and troubleshooting
- Escalation: when and how to contact NovaTech support

---

## 6. End-User Training Plan

### 6.1 Training Approach

NovaTech recommends a **champion-led training model**:
1. NovaTech trains 2–5 internal champions (power users/team leads)
2. Champions train their teams using provided materials
3. NovaTech provides recorded sessions and written guides as leave-behind materials

### 6.2 Role-Based Training Sessions (Week 6)

| Session | Audience | Duration | Topics |
|---------|---------|---------|--------|
| Power User Training | Champions; department leads | 90 min | All features; advanced search; integrations; shortcuts |
| General User Training | All end users | 45 min | Document upload; search; sharing; notifications |
| Search Specialist | Research; legal; compliance teams | 60 min | Advanced search; filters; semantic search; export |

### 6.3 Training Materials Provided

- **Quick Start Guide** (2-page PDF — branded with customer logo on request)
- **Search Tips Cheat Sheet** (laminate card format)
- **Video library access** (docs.novatech.io/videos)
- **Recorded training session** (MP4 delivered within 5 business days)
- **Admin Reference Card** (admin-specific quick reference)

---

## 7. Go-Live Criteria

Before proceeding to full go-live (Week 8), all of the following must be confirmed:

| Criterion | Verified By |
|-----------|------------|
| SSO functioning for all users (tested with 10+ users) | Customer IT + CSM |
| SCIM provisioning working (if configured) | Customer IT |
| All documents migrated and searchable | Customer admin spot-check |
| At least 3 successful test searches with relevant results | Customer team |
| Admin users trained (completed Session 1–3) | CSM attendance check |
| At least 1 end-user training session completed | CSM |
| Webhook endpoints tested (if configured) | Customer IT |
| Support contacts established (who to call; how to submit tickets) | CSM verbal confirmation |
| Success metrics baseline established | CSM + Customer |
| Emergency contact list shared (CSM phone; support email; status page URL) | CSM |

---

## 8. 30-Day Post Go-Live Check-In

**Meeting Format:** 30-minute Zoom with CSM + Customer Admin/Champion  
**Scheduled:** 30 days after Go-Live date

**Agenda:**

| Item | Discussion Points |
|------|-----------------|
| Usage check-in | Active user count; search volume; documents added since go-live |
| Wins | What's working well; early value stories |
| Blockers | Any features not being used; adoption challenges |
| Support tickets review | Outstanding issues; resolution satisfaction |
| Feature roadmap preview | Upcoming features relevant to customer |
| Next QBR schedule | Confirm 90-day QBR date |

**Output:** 30-day check-in summary emailed to customer admin and executive sponsor within 24 hours.

---

## 9. Common Onboarding Blockers and Solutions

| Blocker | Symptoms | Solution |
|---------|----------|---------|
| SSO configuration delay | IdP admin not available; firewall blocking SAML exchange | Escalate within customer to IT leadership; offer temporary username/password as bridge; provide IP ranges to whitelist |
| Data migration delay | Source system export is slow; format conversion needed | Offer interim access with manual uploads; use integration sync if source is in supported system (Google Drive; SharePoint) |
| Low user adoption | Few users logging in after training | Identify internal champion; manager-level communication to team; remind about key use cases |
| Search quality concerns | Users say results are irrelevant | Review collection structure and metadata; add tags; train users on query formulation; check if documents are processed |
| IT security review blocking | Customer InfoSec team requires documentation | Provide SOC 2 report; penetration test executive summary; DPA; architecture overview; ISMS documentation |
| Lack of executive engagement | Executive sponsor not attending QBRs | CSM escalates to AE; request AE-led executive briefing call |

---

## 10. Success Metrics to Establish at Go-Live

Agree on 3–5 measurable success metrics at the kickoff call. Examples by use case:

| Use Case | Suggested Metrics |
|---------|-----------------|
| Legal document management | Documents uploaded per month; search queries per user per week; time to find a specific contract (before vs. after) |
| Compliance/regulatory | Audit log queries per month; GDPR request completion time; document retention compliance rate |
| Enterprise knowledge management | Active users / total licensed users (>70% target); search volume per week; user satisfaction score (internal survey) |
| Sales enablement | Documents accessed by sales team; proposal creation time; search success rate (user self-reported) |

---

*This guide is maintained by the Customer Success team. For onboarding questions, contact David Rodriguez (david.rodriguez@novatech.com) or the shared CSM mailbox csm@novatech.com.*
