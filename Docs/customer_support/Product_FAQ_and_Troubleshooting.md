# NovaTech Solutions — Product FAQ and Troubleshooting Guide

**Document Version:** 3.1  
**Last Updated:** March 5, 2026  
**Authors:** Support Team, Product Team  
**Classification:** Internal (Support Team Reference) — portions publishable to customer Help Center  
**Review Cycle:** Monthly updates; quarterly full review

---

## Section 1: Account and Billing

**Q1: How do I upgrade my subscription plan?**
To upgrade your subscription, navigate to **Settings → Subscription** in the admin console and click **Upgrade Plan**. You'll see available plans and pricing. Upgrades take effect immediately on a pro-rated basis; you'll be charged the difference for the remaining days in your billing cycle. Enterprise plan upgrades require contacting your Account Executive as they involve custom pricing and contract terms. Contact sarah.chen@novatech.com or support@novatech.com.

**Q2: How do I add more user licenses to my account?**
Admins can purchase additional user seats from **Settings → Users → Manage Licenses**. Click **Add Seats** and select the quantity. Each seat follows your current per-seat pricing (visible on your Order Form). New seats are available immediately and billed pro-rated on your next invoice. Enterprise customers should contact their Account Executive for volume pricing on large seat expansions (50+ seats).

**Q3: Where can I download my invoices?**
Invoices are available in **Settings → Billing → Invoice History**. You can download individual invoices as PDF or export the full invoice history as a CSV file. Invoices are emailed to the billing contact on file within 24 hours of generation. To update your billing contact, go to **Settings → Billing → Billing Contact**. For past invoices older than 24 months, submit a support ticket tagged `Billing`.

**Q4: Can I get a refund if I cancel my subscription?**
NovaTech's refund policy depends on your plan type and circumstances. Annual plans are non-refundable after the 14-day new customer window, but we offer prorated credits for SLA breaches and billing errors. If you believe you have a valid refund claim (billing error, SLA breach, duplicate charge), please submit a support ticket tagged `Refund Request` with your invoice number. Our team will review within 5 business days. See our full Refund Policy in your MSA or contact support@novatech.com.

**Q5: My payment failed. What happens to my account?**
If a payment fails, we send an email notification to the billing contact and retry the payment 3 times over 7 days (on days 1, 3, and 7). If all retries fail, access is suspended (data is retained for 90 days). To restore access, update your payment method in **Settings → Billing → Payment Methods** and pay the outstanding invoice. For Enterprise accounts on invoice payment terms, contact your Account Executive or ana.reyes@novatech.com to arrange payment.

**Q6: How do I change my billing cycle from monthly to annual?**
Annual billing is available at a 15% discount. To switch, go to **Settings → Billing → Subscription** and click **Switch to Annual**. The annual charge will be calculated from your next billing date. You'll receive a new invoice for the annual amount within 24 hours. If you've already paid the current month, a credit will be applied. Enterprise customers should contact their Account Executive to amend the contract.

**Q7: Can I get a copy of the invoice with our Purchase Order number?**
Yes. To add a PO number to future invoices, go to **Settings → Billing → Billing Settings** and enter your PO number. For reissuing a past invoice with a PO number, submit a support ticket with the invoice number and PO number. Our finance team reissues invoices within 2 business days.

---

## Section 2: Document Management

**Q8: What file types can I upload to NovaTech?**
NovaTech supports the following file types: PDF, DOCX, DOC, XLSX, XLS, PPTX, PPT, TXT, RTF, CSV, HTML, EPUB, images (PNG, JPG, TIFF — text is extracted via OCR), and ZIP archives (contents are extracted and indexed individually). Video and audio files are stored but not indexed for text search. If your file type is not supported, contact support for evaluation.

**Q9: What is the maximum file size I can upload?**
File size limits depend on your plan:
- Standard: 100 MB per file, 50 GB total storage
- Professional: 500 MB per file, 200 GB total storage
- Enterprise: 5 GB per file, 5 TB total storage (custom storage available)

If you need to upload a file larger than your plan's limit, contact support — we can often accommodate with a temporary limit increase for Enterprise customers. Note: there is a known intermittent issue with uploads between 50–200 MB (ENG-2751, fix targeted April 8, 2026). Workaround: compress the file or split into smaller sections.

**Q10: How long does document processing take after upload?**
Small documents (< 10 MB) are typically indexed within 30–60 seconds of upload. Large documents (> 100 MB) may take 2–10 minutes. Scanned PDFs requiring OCR take 3–15 minutes depending on page count. You'll receive an in-app notification and optional email when processing is complete. If a document shows "Processing" for more than 30 minutes, submit a support ticket with the document ID.

**Q11: Can I bulk upload documents?**
Yes. NovaTech supports bulk uploads via:
1. **Drag-and-drop in the UI:** Select up to 50 files at once
2. **API bulk endpoint:** `POST /v2/documents/bulk` — up to 50 documents per request (Enterprise)
3. **Integration sync:** Use the Google Drive, SharePoint, or Dropbox integrations to sync folders
4. **CSV import:** Upload a CSV file with document metadata and file URLs for batch ingestion

**Q12: How do I restore a deleted document?**
Deleted documents are retained in the recycle bin for 30 days before permanent deletion. To restore, go to **Documents → Recycle Bin**, find the document, and click **Restore**. If the document has been permanently deleted (>30 days), contact support — we may be able to restore from backup within the 35-day backup window. After 35 days, restoration is not possible.

**Q13: How do I set up document access controls?**
Document access is managed at three levels: (1) **Collection-level permissions:** assign user groups to collections with read/write/admin access in **Settings → Collections**; (2) **Document-level permissions:** override collection access for individual documents via the document's **Share** settings; (3) **Tenant-level policies:** admins can enforce "private by default" (all documents restricted until explicitly shared) in **Settings → Security → Document Policy**. Contact your CSM for guidance on access control design for large teams.

---

## Section 3: Search

**Q14: Why are my search results slow?**
Search performance depends on the size of your document index and query complexity. If you're experiencing consistently slow search (>3 seconds), please note:
- There is a **known performance issue (ENG-2847)** affecting tenants with >5M documents. Engineering is actively working on a fix (expected: April 15, 2026). If you're affected, please submit a ticket so we can track impact and prioritize.
- **Workaround for large collections:** Use specific filters (date range, document type, author) to narrow results before searching. This reduces the search scope significantly.
- If slowness is new or sudden, check status.novatech.io for any active incidents.

**Q15: How does NovaTech search work?**
NovaTech uses a hybrid search approach combining BM25 keyword matching (traditional full-text search) with vector similarity search (semantic/AI search). This means you can find documents using exact keywords AND conceptually related content. For example, searching "cost reduction" will also surface documents about "expense optimization" or "spending efficiency." You can toggle between "Keyword," "Semantic," and "Hybrid" modes in the search interface. Hybrid is recommended for most use cases.

**Q16: My search isn't finding a document I know exists. Why?**
If a document isn't appearing in search: (1) Check the document's status in **Documents → All Documents** — it may still be processing; (2) Verify you have read access to the document (access controls may be restricting it); (3) Try searching by the exact filename in the **Documents** view instead of the search bar; (4) If the document was recently uploaded (<30 minutes), wait for indexing to complete; (5) If none of these resolve it, submit a support ticket with the document ID and your search query.

**Q17: Can I search within a specific folder or collection only?**
Yes. In the search bar, click **Filter** and select **Collection** to limit search to one or more collections. Alternatively, navigate to the collection first, then use the search bar — it will automatically scope to that collection. API users can pass the `collection_id` parameter in the search request.

**Q18: How do I export search results?**
Click **Export** in the search results page to download results as CSV or JSON. The export includes document title, ID, URL, metadata, and the matched snippet. For large exports (>1,000 results), use `POST /v2/search/export` via API — the export runs asynchronously and delivers a download link via email and webhook when ready. Note: there is a current 5-request/minute rate limit on export endpoints.

---

## Section 4: Integrations

**Q19: How do I set up SSO (Single Sign-On)?**
NovaTech supports SAML 2.0 SSO with all major identity providers (Okta, Azure AD, Google Workspace, OneLogin, PingFederate). To configure: go to **Settings → Security → Single Sign-On**, download the NovaTech service provider metadata XML, and upload it to your identity provider. Enter your identity provider's metadata URL or XML in NovaTech. Test with a single user before enabling for all. Full setup guide: docs.novatech.io/sso. Enterprise customers can request a guided SSO setup call with our Solutions Engineering team.

**Q20: How do I connect NovaTech to Slack?**
Go to **Settings → Integrations → Slack** and click **Connect**. Authorize the NovaTech Slack app (requires Slack admin privileges). Configure which events trigger Slack notifications (document uploaded, search export ready, workflow completed, etc.) and which channel to post to. You can configure multiple channels for different event types. For enterprise-grade Slack usage (Slack Enterprise Grid), contact your CSM.

**Q21: What are the API rate limits?**
Rate limits depend on your subscription tier: Standard: 1,000 requests/minute; Professional: 2,500 requests/minute; Enterprise: 5,000 requests/minute. Rate limit status is returned in every API response header (`X-RateLimit-Remaining`). If you need higher limits, contact your Account Executive — Enterprise+ plans with custom limits are available. See full API documentation: docs.novatech.io/api.

**Q22: How do I rotate an API key?**
In **Settings → API Keys**, click the **...** menu next to the key and select **Rotate**. A new key is generated immediately; the old key remains valid for 24 hours to allow application updates. After 24 hours, the old key is revoked. We recommend rotating API keys every 90 days. For critical production keys, coordinate the rotation with your engineering team to avoid downtime.

---

## Section 5: Performance and Technical

**Q23: The platform is loading slowly. What should I check?**
First check status.novatech.io for any active incidents. If no active incident: (1) Try clearing browser cache and hard-refreshing (Ctrl+Shift+R on Chrome); (2) Test from a different browser or network; (3) Disable browser extensions temporarily; (4) If on mobile, try the web browser instead of the mobile app; (5) Check your network — NovaTech API calls require stable broadband (>10 Mbps). If the issue persists, submit a ticket with your browser/OS version and the specific pages that are slow.

**Q24: Document preview isn't loading. What's wrong?**
Document preview issues are usually caused by: (1) Unsupported file type for preview (try downloading instead); (2) Large file still being processed — check document status; (3) Browser missing the required viewer (try Chrome or Firefox); (4) Corporate firewall blocking the preview CDN URL (whitelist `cdn.novatech.io` and `preview.novatech.io`). If the document was recently uploaded and shows "Processing," wait 5 minutes and refresh.

**Q25: I'm getting "Session Expired" errors frequently.**
Session tokens expire after 1 hour of inactivity (auto-refreshed if you're actively using the platform). If you're seeing unexpected session expiries: (1) Check if your browser is blocking cookies (required for session management); (2) If using SSO, your IdP session timeout may be shorter than NovaTech's — coordinate with your IT team to align session timeouts; (3) Adblockers can sometimes interfere with session management — disable and test.

---

## Section 6: Security

**Q26: How is my data encrypted?**
All data is encrypted in transit using TLS 1.3 (minimum TLS 1.2 for legacy clients). Data at rest is encrypted using AES-256. Document content is stored in Amazon S3 with server-side encryption. Database records are encrypted at rest on RDS. Tenant-specific sensitive fields use envelope encryption with tenant-specific KMS keys — NovaTech cannot access your data without using your tenant's encryption key.

**Q27: Where is my data stored?**
All data is stored in Amazon Web Services (AWS) data centers in the United States (us-east-1, N. Virginia). Enterprise customers may request EU data residency (stored in eu-west-1, Ireland) for an additional fee. APAC data residency is planned for Q4 2026. Data is never transferred outside the primary region without customer consent except for disaster recovery (cross-region backups in us-west-2, Oregon).

**Q28: Is NovaTech GDPR compliant?**
Yes. NovaTech is GDPR compliant and acts as a Data Processor for customer data. We offer a Data Processing Agreement (DPA) available at docs.novatech.io/dpa. Key GDPR capabilities: right to access (data export), right to erasure (data deletion within 30 days), data breach notification (within 72 hours of confirmed breach), privacy by design (data minimization), and standard contractual clauses for data transfers. Contact legal@novatech.com for DPA signing.

**Q29: How do I manage user roles and permissions?**
NovaTech supports four built-in roles: **Owner** (full access, billing), **Admin** (user management, settings, no billing), **Editor** (upload, organize, search, share), **Viewer** (read-only search and view). Custom roles with granular permissions are available for Enterprise customers. Manage roles in **Settings → Users → Roles**. Role changes take effect immediately.

**Q30: How do I access the audit log?**
The audit log is available for Professional and Enterprise accounts in **Settings → Security → Audit Log**. It records all user actions, admin operations, and system events with timestamps, user attribution, and IP address. You can filter by user, action type, or date range and export to CSV. Via API: `GET /v2/audit/events`. Audit logs are retained for 1 year in the UI; 7 years in long-term storage (available on request).

---

## Section 7: Admin and User Management

**Q31: How do I add or remove users?**
Admins can manage users in **Settings → Users → User Management**. To add a user: click **Invite User**, enter their email, select a role, and click **Send Invite**. They'll receive an onboarding email. To remove a user: find them in the user list, click **...**, and select **Deactivate**. Deactivated users lose access immediately; their documents and data are retained.

**Q32: Can I provision users automatically via SCIM?**
Yes, NovaTech supports SCIM 2.0 for automated user provisioning and deprovisioning. SCIM is available for Enterprise accounts and integrates with Okta, Azure AD, OneLogin, and other SCIM-compatible identity providers. Setup guide: docs.novatech.io/scim. SCIM provisioning handles user creation, attribute sync, group assignment, and automatic deprovisioning when users are removed from your identity provider.

**Q33: How do I configure email domains to restrict sign-ups?**
In **Settings → Security → Allowed Domains**, add your company's email domains (e.g., acme-corp.com). Only users with emails from allowed domains can accept invites or sign up (if self-serve signup is enabled). This prevents unauthorized users from joining your tenant.

---

*This FAQ is maintained by the Support team. For questions not covered here, submit a ticket at support.novatech.io or email support@novatech.com. For urgent issues, use in-app chat during business hours.*
