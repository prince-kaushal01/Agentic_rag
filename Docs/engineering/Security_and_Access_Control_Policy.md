# NovaTech Solutions — Security and Access Control Policy

**Document Version:** 2.9  
**Last Updated:** January 15, 2026  
**Authors:** Anita Sharma (Security Champion, Staff Engineer), Priya Nair (VP Engineering), Legal & Compliance Team  
**Classification:** Internal — Confidential  
**Review Cycle:** Semi-annual (next: July 2026)  
**Compliance Mapping:** SOC 2 Type II, GDPR, ISO 27001 (in progress)

---

## 1. Purpose and Scope

This policy defines security and access control requirements for all NovaTech Solutions engineering staff, contractors, and systems. It covers access control to production systems, secrets management, application security standards, vulnerability management, penetration testing, and compliance obligations.

Violations of this policy may result in disciplinary action up to and including termination, and may expose NovaTech to legal or regulatory liability.

All engineering staff must review this policy annually. Acknowledgment is tracked in Workday.

---

## 2. Access Control Principles

### 2.1 Least Privilege

All access rights — to AWS, GitHub, databases, Kubernetes, and third-party tools — are granted on the basis of **least privilege**: each person or system receives only the access necessary to perform their defined function, and no more.

| Access Request Process |
|----------------------|
| Engineer submits access request via ServiceNow (IT ticketing) |
| Manager approves the request |
| IT/Security grants access, time-bound if non-permanent |
| Access is logged in the access registry (Google Sheet: "Engineering Access Registry") |

### 2.2 Quarterly Access Reviews

Access reviews are conducted **every quarter** (January, April, July, October):

1. IT/Security exports current access list for all systems
2. Each manager reviews their team's access and confirms or revokes
3. Revocations must be completed within **5 business days**
4. Results are documented for SOC 2 audit evidence
5. Any access not confirmed in review is automatically revoked

**Last completed:** January 10, 2026  
**Next scheduled:** April 7, 2026  
**Owner:** Anita Sharma + IT Manager (Kevin Walsh)

### 2.3 Access Tiers

| Tier | Description | Examples | Approval Required |
|------|-------------|---------|-----------------|
| Standard | Read access to non-production systems | Dev/staging AWS, GitHub repos | Manager |
| Elevated | Write access to non-production; read to production logs | Staging deploy, production Datadog | Manager + Security |
| Production | Write access to production systems | Production Kubernetes, RDS | Manager + VP Eng + Security |
| Break-Glass | Emergency production admin access | Production database direct access | VP Eng + CEO notification |

### 2.4 Joiner/Mover/Leaver Process

**Joiner (New Hire):**
- Access provisioned by IT on first day per role template
- No production access for first 30 days (probationary period)
- Security onboarding training must be completed within 7 days

**Mover (Role Change):**
- Previous role access revoked within 24 hours of role change
- New role access granted based on new role template
- Manager notifies IT via ServiceNow ticket

**Leaver (Offboarding):**
- All access revoked **same day** as last day of employment
- AWS IAM credentials, GitHub access, SSO accounts — all deactivated
- API keys issued to the employee must be rotated immediately
- Verified by IT checklist signed by manager

---

## 3. Production Access Procedures

### 3.1 Standard Production Access

Production systems are **read-only** for most engineers. Standard engineers have:
- Read access to production logs (Datadog, Kibana)
- Read access to production metrics
- No direct database access
- No kubectl exec in production

### 3.2 Elevated Production Access

On-call engineers and SREs have:
- `kubectl logs` and `kubectl describe` in production
- Read-only RDS access via bastion host (query console, no writes)
- AWS Console read access to production

### 3.3 Break-Glass Procedure

**Break-glass access** is for emergency situations where standard access is insufficient to resolve a P0 incident. It provides temporary admin-level access to production.

**Process:**
1. Engineer determines break-glass is required and notifies Incident Commander
2. IC approves via Slack in `#incidents` channel (creates an audit record)
3. Engineer retrieves break-glass credentials from AWS Secrets Manager:
   ```bash
   aws secretsmanager get-secret-value \
     --secret-id novatech/break-glass/prod-admin \
     --profile novatech-security
   ```
4. A CloudWatch alarm is triggered automatically, notifying VP Engineering and CTO
5. All actions taken with break-glass access are **automatically logged** to CloudTrail and the Audit Service
6. Break-glass access auto-expires after **4 hours**
7. Engineer must submit a break-glass usage report in Jira within 24 hours
8. Access is reviewed by Security team within 48 hours

**Break-glass usage in 2025:** 7 times (all P0 incidents; all documented and reviewed)

---

## 4. Secret Management Policy

### 4.1 Mandatory Rules

1. **No secrets in source code.** Ever. Including:
   - Passwords, API keys, tokens, certificates, private keys
   - Hardcoded connection strings with credentials
   - Test secrets that "look like" non-sensitive data

2. **No secrets in environment variables** (in code or Docker images). Services must retrieve secrets from AWS Secrets Manager at startup.

3. **No secrets in Terraform state** visible in plaintext. Use `sensitive = true` and remote state encryption.

4. **No secrets in CI/CD logs.** Mask secret values in GitHub Actions using `add-mask`.

5. **No secrets shared via Slack, email, or any messaging platform.** Use AWS Secrets Manager sharing or Vault.

### 4.2 Secret Detection

- **Gitleaks** runs in CI on every PR and blocks merge if secrets are detected
- **GitHub Advanced Security** secret scanning is enabled on all repositories
- **Pre-commit hook** includes `detect-secrets` to prevent accidental commits
- Weekly automated scans of all GitHub repositories via `truffleHog`

**If a secret is accidentally committed:**
1. Immediately rotate the compromised secret in the target system
2. Remove from git history using `git filter-repo` (NOT `git rebase`)
3. Force-push to remove from all branches (requires Security team approval)
4. File a security incident report in Jira (tag: `security-incident`)
5. Notify Security team within 1 hour of discovery

### 4.3 Secret Rotation Requirements

| Secret Type | Max Age | Rotation Method |
|------------|---------|----------------|
| Database passwords | 90 days | AWS Secrets Manager Lambda rotator |
| API keys (internal service accounts) | 90 days | Manual (with documented rotation runbook) |
| JWT signing keys | 180 days | Coordinated rotation (Platform team) |
| OAuth client secrets | 90 days | Manual |
| Third-party vendor API keys | Per vendor recommendation, max 365 days | Manual |
| Break-glass credentials | 30 days | Automated |
| SSH keys (bastion hosts) | 365 days | Manual |

---

## 5. Application Security

### 5.1 Secure Development Lifecycle (SDL)

| Phase | Security Activity |
|-------|-----------------|
| Design | Threat modeling for new features (required for P0/P1 risk features) |
| Development | Secure coding standards (see Code Review Standards doc) |
| Code Review | Security review required for auth, crypto, and data handling changes |
| CI/CD | SAST scan (Snyk Code), dependency scan (Snyk OSS) |
| Pre-release | DAST scan (OWASP ZAP) for new API endpoints |
| Production | Runtime security monitoring (Datadog Cloud Security) |

### 5.2 SAST Pipeline (Snyk Code)

- **Tool:** Snyk Code (SAST) + Snyk Open Source (SCA)
- **Runs:** On every PR (diff scan) and weekly full-repository scan
- **Blocking:** HIGH and CRITICAL severity findings block PR merge
- **Triage:** MEDIUM severity findings require documented acceptance or fix plan within 30 days
- **Dashboard:** `https://app.snyk.io/org/novatech-solutions`

Snyk scan results for the last full scan (March 1, 2026):
- Critical: 0
- High: 2 (both with active fix PRs, ENG-2894 and ENG-2895)
- Medium: 8 (all documented with fix plans)
- Low: 47 (informational, monitored)

### 5.3 DAST Pipeline (OWASP ZAP)

- **Tool:** OWASP ZAP (automated scan) + Burp Suite (manual testing)
- **Runs:** Weekly against staging environment; ad-hoc for major releases
- **Scope:** All public API endpoints, authentication flows, file upload endpoints
- **OWASP Top 10 coverage:** All 10 categories actively monitored
- **Results:** Published to Security Jira board weekly

### 5.4 Dependency Security

- **Tool:** Dependabot (automated PRs) + Snyk (vulnerability database)
- **Schedule:** Dependabot checks daily; creates PRs automatically
- **Policy:**
  - CRITICAL CVE: Must be patched within **24 hours** of disclosure
  - HIGH CVE: Must be patched within **7 days**
  - MEDIUM CVE: Must be patched within **30 days**
  - LOW CVE: Addressed in regular dependency update cycles (monthly)
- **Unresolved HIGH+ CVEs must be accepted with written justification** approved by Security Champion

---

## 6. Penetration Testing

### 6.1 Penetration Test Schedule

| Test Type | Frequency | Last Completed | Next Scheduled | Provider |
|-----------|----------|---------------|---------------|---------|
| External network penetration test | Annual | October 2025 | October 2026 | Rapid7 |
| Web application penetration test | Annual | October 2025 | October 2026 | Rapid7 |
| API penetration test | Annual | October 2025 | October 2026 | Rapid7 |
| Cloud configuration review | Annual | October 2025 | October 2026 | Rapid7 |
| Social engineering (phishing simulation) | Semi-annual | December 2025 | June 2026 | KnowBe4 |
| Internal network (red team) | Every 2 years | October 2024 | October 2026 | External red team |

### 6.2 October 2025 Penetration Test Summary

**Provider:** Rapid7  
**Scope:** External perimeter, web application (app.novatech.io), API (api.novatech.io), cloud configuration  
**Duration:** October 13–24, 2025  
**Report received:** November 3, 2025

**Findings Summary:**

| Severity | Count | Remediated | In Progress | Accepted |
|----------|-------|-----------|------------|---------|
| Critical | 0 | — | — | — |
| High | 1 | 1 | 0 | 0 |
| Medium | 4 | 3 | 1 | 0 |
| Low | 11 | 6 | 3 | 2 |
| Informational | 8 | — | — | — |

High severity finding: Exposed internal service endpoint via misconfigured nginx rule. Remediated November 5, 2025. Medium in-progress: Insufficient rate limiting on password reset endpoint (ENG-2765, targeting Q2 2026).

---

## 7. Vulnerability Severity SLAs

| Severity | CVSS Range | Response SLA | Resolution SLA | Escalation |
|----------|-----------|-------------|---------------|-----------|
| P0 (Critical) | 9.0–10.0 | 1 hour | 24 hours | Immediate — VP Eng + CTO |
| P1 (High) | 7.0–8.9 | 4 hours | 7 days | Engineering Manager |
| P2 (Medium) | 4.0–6.9 | 24 hours | 30 days | Security Champion |
| P3 (Low) | 0.1–3.9 | 1 week | 90 days | Addressed in sprint |
| Informational | 0.0 | — | 180 days | Team discretion |

**Vulnerability SLA tracking** is maintained in the Security Jira board (`SEC` project). Weekly report sent to Engineering VP and CTO.

---

## 8. SOC 2 Type II Control Mapping

NovaTech achieved **SOC 2 Type II certification in August 2025** (audit period: February 2025 – July 2025). The next audit period begins February 2026, with audit completion expected August 2026.

Key engineering controls mapped to SOC 2 Trust Service Criteria:

| Control | SOC 2 Criteria | Evidence |
|---------|---------------|---------|
| Quarterly access reviews | CC6.1, CC6.2 | Access review reports in GDrive |
| Production access logging | CC6.3 | CloudTrail logs in security account |
| Break-glass procedure | CC6.3 | Break-glass usage reports in Jira |
| Secret rotation | CC6.1 | Secrets Manager rotation logs |
| Vulnerability management | CC7.1 | Snyk reports + Jira SEC board |
| Penetration testing | CC7.1 | Rapid7 report + remediation tracking |
| Incident response | CC7.3, CC7.4 | Incident postmortems |
| Change management | CC8.1 | GitHub PR history + CI/CD logs |
| Data encryption (at rest and transit) | C1.1, C1.2 | AWS Config rules + encryption attestation |
| Employee security training | CC1.4 | Workday training completion records |
| Backup and recovery testing | A1.2, A1.3 | DR test reports (semi-annual) |

**SOC 2 compliance dashboard:** Available in Vanta (`https://vanta.novatech.internal`)

---

## 9. Data Security and Privacy

### 9.1 Data Classification

| Classification | Description | Examples | Controls |
|---------------|-------------|---------|---------|
| Public | Information intended for public consumption | Marketing materials | None required |
| Internal | Business information for employees only | Runbooks, internal docs | Authentication required |
| Confidential | Sensitive business or customer information | Customer data, contracts | Encryption + access control |
| Restricted | Highly sensitive; regulatory implications | PHI, financial PII, credentials | Encryption + strict access + audit log |

### 9.2 Customer Data Handling

- Customer documents are stored encrypted at rest (AES-256, tenant-specific KMS keys)
- Customer PII is never logged in application logs
- Customer data is logically isolated by tenant ID (see Architecture Overview)
- Data retention follows customer's contract terms (default: 7 years after account termination)
- Right to erasure (GDPR Article 17) requests are fulfilled within 30 days

### 9.3 Data Residency

- All production data stored in `us-east-1` (N. Virginia)
- EU data residency option available for Enterprise customers (stored in `eu-west-1` — provisioned separately)
- APAC data residency: Planned for Q4 2026

---

*This policy is maintained by the Security team and Engineering Leadership. Questions: #security-help on Slack or anita.sharma@novatech.com. Security incidents: #security-incidents (emergency: security@novatech.com).*
