# NovaTech Solutions — Internal API Documentation

**Document Version:** 2.8  
**Last Updated:** March 1, 2026  
**Authors:** Elena Vasquez (API Platform Lead), Tom Okafor (Staff Engineer)  
**Classification:** Internal — Engineering  
**Applies To:** All NovaTech API endpoints (v1 and v2)

---

## 1. Overview

This document describes the NovaTech Solutions API platform standards, authentication mechanisms, rate limits, error handling, versioning policy, webhook system, and SDK availability. All internal and external APIs must comply with these standards.

The NovaTech API is RESTful, uses JSON for all request and response bodies (unless otherwise specified), and communicates exclusively over HTTPS (TLS 1.3 minimum). The base URL for production is:

- **v1 (deprecated — sunset July 1, 2026):** `https://api.novatech.io/v1`
- **v2 (current — stable):** `https://api.novatech.io/v2`
- **v3 (beta — available Q2 2026):** `https://api.novatech.io/v3`

Staging environment base URL: `https://api-staging.novatech.io`

---

## 2. Authentication

### 2.1 JWT Bearer Token Authentication

The primary authentication mechanism for all API requests is JWT Bearer tokens issued by the NovaTech Auth Service.

**Obtaining a Token:**

```http
POST /v2/auth/token
Content-Type: application/json

{
  "grant_type": "password",
  "username": "user@company.com",
  "password": "s3cur3_p4ss",
  "scope": "documents:read documents:write search:read"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4...",
  "scope": "documents:read documents:write search:read"
}
```

**Using the Token:**

```http
GET /v2/documents
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Token Properties:**
- Access token lifetime: **3600 seconds (1 hour)**
- Refresh token lifetime: **30 days** (sliding expiration on use)
- Algorithm: RS256 (RSA signature with SHA-256)
- Claims: `sub` (user ID), `tid` (tenant ID), `scope`, `iat`, `exp`, `jti`
- JWKS endpoint: `https://api.novatech.io/.well-known/jwks.json`

### 2.2 API Key Authentication

Machine-to-machine integrations may use API keys instead of user tokens. API keys are long-lived credentials scoped to a service account.

```http
GET /v2/documents
X-API-Key: ntk_live_a4f8b2c9d1e3f6a7b8c9d2e4f5a6b7c8
```

- API keys are prefixed: `ntk_live_` (production), `ntk_test_` (test environment)
- Keys are generated in the Admin Console under **Settings → API Keys**
- Keys can be scoped to specific permissions and IP address allowlists
- Key rotation recommended every 90 days; enforced for SOC 2 compliance accounts

### 2.3 OAuth 2.0 Authorization Code Flow

For third-party integrations that act on behalf of users:

**Step 1 — Authorization Request:**
```
GET https://api.novatech.io/v2/oauth/authorize
  ?client_id=your_client_id
  &redirect_uri=https://your-app.com/callback
  &response_type=code
  &scope=documents:read+search:read
  &state=random_state_string
```

**Step 2 — Token Exchange:**
```http
POST /v2/oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
&code=auth_code_from_step_1
&redirect_uri=https://your-app.com/callback
&client_id=your_client_id
&client_secret=your_client_secret
```

**Supported Grant Types:** `authorization_code`, `client_credentials`, `refresh_token`

### 2.4 SAML 2.0 SSO

Enterprise customers may authenticate via SAML 2.0. The NovaTech service provider metadata is available at:
`https://api.novatech.io/v2/auth/saml/metadata`

Supported Identity Providers: Okta, Azure AD, Google Workspace, OneLogin, PingFederate.

---

## 3. Rate Limiting

Rate limits are enforced at the API Gateway (Kong) level using a sliding window algorithm per tenant.

### 3.1 Rate Limit Tiers

| Subscription Tier | Requests/Minute | Requests/Hour | Requests/Day | Burst Allowance |
|------------------|----------------|--------------|-------------|----------------|
| Free | 60 | 1,000 | 10,000 | 2x for 10 seconds |
| Standard | 1,000 | 50,000 | 500,000 | 2x for 30 seconds |
| Professional | 2,500 | 100,000 | 2,000,000 | 2x for 60 seconds |
| Enterprise | 5,000 | 250,000 | 10,000,000 | 3x for 120 seconds |
| Enterprise+ (custom) | Negotiated | Negotiated | Negotiated | Custom |

### 3.2 Rate Limit Headers

All API responses include rate limit information:

```http
X-RateLimit-Limit: 5000
X-RateLimit-Remaining: 4873
X-RateLimit-Reset: 1743502800
X-RateLimit-Window: 60
Retry-After: 12
```

### 3.3 Rate Limit Exceeded Response

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Retry-After: 23

{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit of 5000 requests/minute exceeded.",
    "retry_after_seconds": 23,
    "limit": 5000,
    "window": "60s",
    "docs": "https://docs.novatech.io/api/rate-limiting"
  }
}
```

### 3.4 Per-Endpoint Limits

Certain high-cost endpoints have additional per-endpoint limits:

| Endpoint | Limit | Window |
|----------|-------|--------|
| `POST /documents/bulk` | 10 requests | per minute |
| `POST /search/export` | 5 requests | per minute |
| `POST /ai/qa` | 50 requests | per minute |
| `POST /ai/embeddings` | 100 requests | per minute |

---

## 4. Pagination

All list endpoints support cursor-based pagination (preferred for large datasets) and offset-based pagination (for compatibility).

### 4.1 Cursor-Based Pagination (Preferred)

```http
GET /v2/documents?limit=50&cursor=eyJpZCI6IjEyMzQ1NiIsImNyZWF0ZWRfYXQiOiIyMDI2LTAzLTAxVDAwOjAwOjAwWiJ9
```

**Response:**
```json
{
  "data": [...],
  "pagination": {
    "type": "cursor",
    "limit": 50,
    "has_next": true,
    "has_previous": true,
    "next_cursor": "eyJpZCI6IjEyMzQ1NyIsImNyZWF0ZWRfYXQiOiIyMDI2LTAzLTAyVDAwOjAwOjAwWiJ9",
    "previous_cursor": "eyJpZCI6IjEyMzQ1NSIsImNyZWF0ZWRfYXQiOiIyMDI2LTAyLTI4VDAwOjAwOjAwWiJ9",
    "total_count": 4821
  }
}
```

### 4.2 Offset-Based Pagination

```http
GET /v2/documents?limit=50&offset=100&sort=created_at&order=desc
```

**Response:**
```json
{
  "data": [...],
  "pagination": {
    "type": "offset",
    "limit": 50,
    "offset": 100,
    "total_count": 4821,
    "total_pages": 97,
    "current_page": 3
  }
}
```

**Pagination Limits:** Maximum `limit` is 200 per request. Requests exceeding this return a 400 error.

---

## 5. Error Reference

### 5.1 Error Response Format

All errors follow a consistent envelope format:

```json
{
  "error": {
    "code": "DOCUMENT_NOT_FOUND",
    "message": "The requested document with ID 'doc_abc123' was not found.",
    "status": 404,
    "request_id": "req_7f3a9b2c1d4e5f6a",
    "timestamp": "2026-03-10T14:32:17.421Z",
    "docs": "https://docs.novatech.io/errors/DOCUMENT_NOT_FOUND",
    "details": {}
  }
}
```

### 5.2 4xx Client Error Codes

| HTTP Status | Error Code | Description |
|------------|-----------|-------------|
| 400 | `INVALID_REQUEST` | Request body or parameters are malformed |
| 400 | `VALIDATION_ERROR` | One or more fields failed validation (details included) |
| 400 | `MISSING_REQUIRED_FIELD` | A required field is absent |
| 400 | `INVALID_PAGINATION` | Pagination parameters are invalid |
| 401 | `UNAUTHORIZED` | No authentication credentials provided |
| 401 | `TOKEN_EXPIRED` | JWT token has expired; refresh required |
| 401 | `TOKEN_INVALID` | JWT token signature is invalid |
| 401 | `API_KEY_INVALID` | Provided API key is invalid or revoked |
| 403 | `FORBIDDEN` | Authenticated but insufficient permissions |
| 403 | `TENANT_MISMATCH` | Resource belongs to a different tenant |
| 403 | `FEATURE_NOT_AVAILABLE` | Feature not included in subscription tier |
| 404 | `DOCUMENT_NOT_FOUND` | Document with specified ID does not exist |
| 404 | `USER_NOT_FOUND` | User with specified ID does not exist |
| 404 | `RESOURCE_NOT_FOUND` | Generic: requested resource not found |
| 409 | `CONFLICT` | Resource already exists or state conflict |
| 409 | `DUPLICATE_DOCUMENT` | Document with same hash already exists |
| 413 | `PAYLOAD_TOO_LARGE` | Request body exceeds maximum size |
| 413 | `FILE_TOO_LARGE` | Uploaded file exceeds plan limit (Standard: 100MB, Enterprise: 5GB) |
| 415 | `UNSUPPORTED_MEDIA_TYPE` | Content-Type is not supported |
| 422 | `UNPROCESSABLE_ENTITY` | Request understood but cannot be processed |
| 422 | `DOCUMENT_CORRUPT` | Uploaded file is corrupt or unreadable |
| 429 | `RATE_LIMIT_EXCEEDED` | Rate limit exceeded (see Section 3) |

### 5.3 5xx Server Error Codes

| HTTP Status | Error Code | Description |
|------------|-----------|-------------|
| 500 | `INTERNAL_ERROR` | Unexpected server error; engineering is automatically alerted |
| 502 | `BAD_GATEWAY` | Upstream service returned an invalid response |
| 503 | `SERVICE_UNAVAILABLE` | Service is temporarily unavailable; retry with backoff |
| 503 | `SEARCH_UNAVAILABLE` | Search service is degraded (see status page) |
| 504 | `GATEWAY_TIMEOUT` | Request timed out at gateway (default timeout: 30s) |
| 507 | `STORAGE_QUOTA_EXCEEDED` | Tenant has exceeded storage quota |

---

## 6. API Versioning Policy

### 6.1 Version Lifecycle

| Version | Status | GA Date | Sunset Date | Notes |
|---------|--------|---------|------------|-------|
| v1 | Deprecated | Q1 2023 | July 1, 2026 | No new features; security patches only |
| v2 | Current — Stable | Q3 2024 | TBD (min 24 months from v3 GA) | All new features |
| v3 | Beta | Q2 2026 target | — | Breaking changes from v2 documented below |

### 6.2 Deprecation Policy
- APIs are deprecated with **minimum 12 months notice** for Standard/Professional customers
- Enterprise customers receive **18 months notice** with direct communication from their Account Executive
- Deprecated endpoints continue to function until sunset date
- Sunset enforcement: deprecated endpoints return `X-API-Deprecated: true` header and a deprecation notice in the response body

### 6.3 v2 → v3 Breaking Changes (Preview)
The following breaking changes are planned for v3 (subject to change during beta):
- Pagination: cursor-only pagination (offset-based removed)
- Error format: `error.code` changed from SCREAMING_SNAKE_CASE to dot.notation (e.g., `document.not_found`)
- Bulk endpoints consolidated under `/batch` prefix
- Date fields standardized to ISO 8601 with timezone (currently inconsistent)
- `GET /documents` response field `created` renamed to `created_at`

---

## 7. Webhooks

### 7.1 Overview

NovaTech supports webhooks for real-time event notifications. Configure webhooks in the Admin Console under **Settings → Webhooks** or via the API.

```http
POST /v2/webhooks
Content-Type: application/json
Authorization: Bearer ...

{
  "url": "https://your-app.com/novatech-webhook",
  "events": ["document.created", "document.deleted", "search.export.completed"],
  "secret": "your_webhook_signing_secret",
  "active": true
}
```

### 7.2 Supported Webhook Events

| Event | Description | Payload |
|-------|-------------|---------|
| `document.created` | Document successfully uploaded and indexed | Document object |
| `document.updated` | Document metadata or content updated | Document object + changed fields |
| `document.deleted` | Document deleted | Document ID + metadata |
| `document.processing.failed` | Document processing failed (virus, format) | Document ID + error |
| `search.export.completed` | Bulk search export ready for download | Export object + download URL |
| `user.created` | New user added to tenant | User object |
| `user.deleted` | User removed from tenant | User ID |
| `user.role.changed` | User role updated | User ID + old/new roles |
| `workflow.completed` | Automation workflow run completed | Workflow run object |
| `workflow.failed` | Automation workflow run failed | Workflow run + error |
| `billing.invoice.created` | New invoice generated | Invoice object |
| `billing.payment.succeeded` | Payment successfully collected | Payment object |
| `billing.payment.failed` | Payment collection failed | Payment object + error |

### 7.3 Webhook Payload Schema

```json
{
  "id": "evt_8f3a2b9c1d4e5f6a7b8c",
  "type": "document.created",
  "tenant_id": "tnt_acme_corp",
  "timestamp": "2026-03-10T14:32:17.421Z",
  "api_version": "v2",
  "data": {
    "document": {
      "id": "doc_abc123xyz",
      "filename": "Q4_Report_2025.pdf",
      "size_bytes": 2048576,
      "created_at": "2026-03-10T14:32:15.000Z",
      "created_by": "usr_james_harrington"
    }
  }
}
```

### 7.4 Webhook Security

All webhook deliveries include a signature header for payload verification:

```
X-NovaTech-Signature: sha256=hmac_sha256(webhook_secret, request_body)
X-NovaTech-Event: document.created
X-NovaTech-Delivery: evt_8f3a2b9c1d4e5f6a7b8c
```

Verify signatures in your webhook handler before processing any event.

### 7.5 Retry Logic

Failed webhook deliveries (non-2xx response or timeout) are retried with exponential backoff:

| Attempt | Delay |
|---------|-------|
| 1st retry | 1 minute |
| 2nd retry | 5 minutes |
| 3rd retry | 30 minutes |
| 4th retry | 2 hours |
| 5th retry | 8 hours |
| Final (6th) | 24 hours |

After 6 failed attempts, the webhook endpoint is marked as `failed` and delivery stops. NovaTech sends an email alert to the admin email on file.

---

## 8. SDK Overview

### 8.1 Python SDK

**Package:** `novatech-sdk` — Available on PyPI  
**Version:** 2.4.1 (released February 20, 2026)  
**Python Support:** 3.10+

```bash
pip install novatech-sdk
```

```python
from novatech import NovaTechClient

client = NovaTechClient(
    api_key="ntk_live_a4f8b2c9d1e3f6a7b8c9",
    base_url="https://api.novatech.io"  # optional, defaults to production
)

# Upload a document
doc = client.documents.upload(
    file_path="/path/to/document.pdf",
    title="Q4 Annual Report",
    tags=["finance", "quarterly"]
)

# Search documents
results = client.search.query(
    q="revenue forecast Q4",
    filters={"date_range": {"gte": "2025-01-01"}},
    limit=20
)
```

### 8.2 JavaScript / TypeScript SDK

**Package:** `@novatech/sdk` — Available on npm  
**Version:** 2.3.8 (released March 5, 2026)  
**Node.js Support:** 18+, Browser-compatible (ESM)

```bash
npm install @novatech/sdk
```

```typescript
import { NovaTechClient } from '@novatech/sdk';

const client = new NovaTechClient({
  apiKey: 'ntk_live_a4f8b2c9d1e3f6a7b8c9',
});

// Search with TypeScript types
const results = await client.search.query({
  q: 'contract renewal 2026',
  limit: 50,
});
```

### 8.3 Java SDK

**Package:** `io.novatech:novatech-sdk` — Available on Maven Central  
**Version:** 2.2.0 (released January 15, 2026)  
**Java Support:** 11+

```xml
<dependency>
  <groupId>io.novatech</groupId>
  <artifactId>novatech-sdk</artifactId>
  <version>2.2.0</version>
</dependency>
```

---

## 9. API Changelog (2025–2026)

### v2 — March 2026
- **Added:** `POST /v2/ai/qa` — Q&A over documents using RAG pipeline
- **Added:** `GET /v2/documents/{id}/similar` — semantic similarity search for a given document
- **Fixed:** `GET /v2/search` — inconsistent `total_count` when using date range filters (ENG-2801)
- **Deprecated:** `GET /v2/documents/{id}/preview` — use `/v2/documents/{id}/render` instead

### v2 — January 2026
- **Added:** `POST /v2/documents/bulk` — bulk document upload (up to 50 documents per request)
- **Added:** `GET /v2/analytics/usage` — tenant-level usage metrics API
- **Changed:** Rate limit headers now include `X-RateLimit-Window`
- **Fixed:** Webhook retry logic now correctly handles 429 responses from endpoints

### v2 — November 2025
- **Added:** SCIM 2.0 endpoints for user provisioning (`/v2/scim/v2/Users`, `/v2/scim/v2/Groups`)
- **Added:** `GET /v2/audit/events` — compliance audit log API
- **Changed:** `POST /v2/auth/token` now returns `scope` field in response
- **Security:** Enforced minimum TLS 1.2 on all endpoints (TLS 1.0/1.1 removed)

### v2 — September 2025
- **Added:** `POST /v2/ai/summarize` — AI-powered document summarization
- **Added:** `GET /v2/search/suggest` — search autocomplete/suggestions
- **Changed:** Pagination cursors are now base64-encoded JSON (previously opaque strings)
- **Fixed:** `DELETE /v2/documents/bulk` now correctly returns 207 Multi-Status

### v1 — Deprecation Notice (September 2025)
- v1 officially deprecated as of September 1, 2025
- Sunset date: **July 1, 2026**
- All v1 customers notified via email and in-app banner
- Migration guide: `https://docs.novatech.io/migration/v1-to-v2`

---

## 10. Internal API Standards Checklist

All new APIs must meet the following standards before production release:

- [ ] RESTful resource naming (plural nouns, lowercase, hyphens not underscores)
- [ ] Consistent error format (Section 5)
- [ ] Pagination implemented for all list endpoints
- [ ] Rate limiting applied at API gateway
- [ ] Auth enforced (no unauthenticated endpoints except health check and JWKS)
- [ ] Input validation with descriptive VALIDATION_ERROR responses
- [ ] Idempotency-Key support for POST/PUT/DELETE operations
- [ ] Request ID (`X-Request-Id`) logged and returned in response
- [ ] OpenAPI 3.1 spec updated and published
- [ ] Postman collection updated
- [ ] SDK updated (Python, JS, Java)
- [ ] Changelog entry written
- [ ] Runbook updated if new operational considerations
