# NovaTech Solutions — Infrastructure Runbook

**Document Version:** 3.2  
**Last Updated:** February 28, 2026  
**Authors:** Kevin Osei (SRE Lead), Dmitri Volkov (Senior DevOps Engineer), Fatima Al-Hassan (Infrastructure Engineer)  
**Classification:** Internal — Engineering  
**Review Cycle:** Quarterly (next: May 2026)

---

## 1. Overview

This runbook provides operational procedures for managing NovaTech Solutions' cloud infrastructure. It covers AWS account structure, Kubernetes cluster management, database operations, caching, search infrastructure, certificate management, secrets management, and cost optimization.

All infrastructure is managed as code (Terraform + Terragrunt). Direct console modifications without corresponding Terraform changes are **strictly prohibited** except during active incident response, and must be reconciled within 24 hours.

Infrastructure repository: `github.com/novatech/infra` (internal)

---

## 2. AWS Account Structure

NovaTech uses a **multi-account AWS Organization** structure for environment isolation and cost tracking:

| Account | Account ID | Purpose | Access |
|---------|-----------|---------|--------|
| `novatech-root` | 123456789000 | AWS Organization root; billing consolidation | Finance + Engineering VPs only |
| `novatech-prod` | 123456789001 | Production workloads | SRE + on-call engineers (MFA required) |
| `novatech-staging` | 123456789002 | Pre-production testing | All engineers |
| `novatech-dev` | 123456789003 | Development/sandbox | All engineers |
| `novatech-security` | 123456789004 | Security tooling, GuardDuty aggregator, CloudTrail logs | Security team only |
| `novatech-shared` | 123456789005 | Shared services: ECR, artifact storage, DNS | SRE team |

### 2.1 Accessing Production

**Production access requires MFA and is logged.** To access production:

1. Assume the `NovaTechSRERole` role via AWS SSO:
   ```bash
   aws sso login --profile novatech-prod
   export AWS_PROFILE=novatech-prod
   ```

2. For elevated/admin access (break-glass), see the Security Policy document.

3. All AWS Console actions in production are logged to CloudTrail and forwarded to the `novatech-security` account. Logs are retained for 7 years.

### 2.2 Regions

- **Primary:** `us-east-1` (N. Virginia) — all production workloads
- **DR:** `us-west-2` (Oregon) — passive warm standby
- **Edge:** CloudFront global (450+ PoPs)

---

## 3. Kubernetes Cluster Management (EKS)

### 3.1 Cluster Inventory

| Cluster | Region | Account | EKS Version | Nodes | Purpose |
|---------|--------|---------|------------|-------|---------|
| `novatech-prod-us-east-1` | us-east-1 | prod | 1.29 | 45–120 | Production |
| `novatech-staging-us-east-1` | us-east-1 | staging | 1.29 | 12–30 | Staging |
| `novatech-dev-us-east-1` | us-east-1 | dev | 1.29 | 6–15 | Development |
| `novatech-dr-us-west-2` | us-west-2 | prod | 1.29 | 10–30 | DR warm standby |

### 3.2 Node Groups

Production cluster node groups:

| Node Group | Instance Type | Min | Max | On-Demand/Spot | Purpose |
|-----------|--------------|-----|-----|---------------|---------|
| `system` | m6i.large | 3 | 3 | On-Demand (100%) | Cluster system pods (coredns, etc.) |
| `platform-standard` | m6i.2xlarge | 6 | 30 | On-Demand (50%) / Spot (50%) | Platform services |
| `data-compute` | r6i.4xlarge | 4 | 20 | On-Demand (70%) / Spot (30%) | Memory-intensive data services |
| `enterprise-dedicated` | m6i.4xlarge | 2 | 10 | On-Demand (100%) | Enterprise customer dedicated pods |
| `batch-spot` | m6i.2xlarge | 0 | 40 | Spot (100%) | Async batch processing |

### 3.3 Namespaces

| Namespace | Purpose | Resource Quota |
|-----------|---------|---------------|
| `novatech-prod` | All production microservices | 96 CPU / 384Gi memory |
| `novatech-infra` | Infrastructure services (Redis, etc.) | 32 CPU / 128Gi memory |
| `monitoring` | Datadog, Prometheus | 16 CPU / 64Gi memory |
| `istio-system` | Service mesh control plane | 8 CPU / 32Gi memory |
| `kube-system` | Kubernetes system components | Unrestricted |

### 3.4 Cluster Access

```bash
# Update kubeconfig for production
aws eks update-kubeconfig \
  --name novatech-prod-us-east-1 \
  --region us-east-1 \
  --profile novatech-prod \
  --role-arn arn:aws:iam::123456789001:role/NovaTechEKSReadRole

# Check cluster health
kubectl get nodes -o wide
kubectl get pods -n novatech-prod
kubectl top nodes
```

### 3.5 Horizontal Pod Autoscaling

All production services have HPA configured:

```bash
# View current HPA status
kubectl get hpa -n novatech-prod

# Example output:
# NAME              REFERENCE              TARGETS          MINPODS  MAXPODS  REPLICAS
# auth-service      Deployment/auth-svc    28%/60%           3       20       5
# search-service    Deployment/search-svc  71%/60%           4       25       12
# document-service  Deployment/doc-svc     34%/60%           5       30       8
```

HPA metrics used:
- CPU utilization (target: 60%)
- Custom metric: `http_requests_per_second` (target: 200 rps per pod)
- Memory utilization for data services (target: 75%)

### 3.6 Cluster Upgrades

EKS version upgrades follow this process:
1. Upgrade dev cluster → monitor 2 weeks
2. Upgrade staging cluster → monitor 1 week
3. Upgrade production: one node group at a time (system → platform → data → enterprise)
4. Max surge: 1 node per node group
5. PodDisruptionBudgets ensure minimum 2 replicas remain during draining

Next planned upgrade: EKS 1.30 targeting May 2026.

---

## 4. Database Operations (RDS PostgreSQL)

### 4.1 Database Inventory

| Database | Instance | RDS Instance | Storage | Multi-AZ | Read Replica |
|----------|---------|-------------|---------|---------|-------------|
| `novatech-auth-prod` | db.r6g.large | PostgreSQL 15.4 | 100 GB | Yes | 1 replica |
| `novatech-documents-prod` | db.r6g.2xlarge | PostgreSQL 15.4 | 2 TB | Yes | 2 replicas |
| `novatech-search-prod` | db.r6g.large | PostgreSQL 15.4 | 200 GB | Yes | 1 replica |
| `novatech-analytics-prod` | db.r6g.4xlarge | PostgreSQL 15.4 | 5 TB | Yes | 2 replicas |
| `novatech-billing-prod` | db.r6g.large | PostgreSQL 15.4 | 100 GB | Yes | 1 replica |
| `novatech-platform-prod` | db.r6g.xlarge | PostgreSQL 15.4 | 500 GB | Yes | 1 replica |

### 4.2 Backup Schedule

| Backup Type | Frequency | Retention | Storage |
|------------|-----------|-----------|---------|
| Automated PITR | Continuous (WAL archiving) | 35 days | S3 (novatech-db-backups) |
| Automated snapshots | Daily at 3:00 AM UTC | 90 days | AWS Managed |
| Manual snapshots (pre-migration) | Before any migration | 30 days | AWS Managed |
| Cross-region copy | Daily | 30 days | us-west-2 |

### 4.3 Point-in-Time Recovery Procedure

**Use case:** Accidental data deletion, data corruption

```bash
# 1. Identify the restore point (timestamp)
RESTORE_TIME="2026-03-10T08:30:00Z"
SOURCE_INSTANCE="novatech-documents-prod"
RESTORE_INSTANCE="novatech-documents-prod-restored-20260310"

# 2. Initiate PITR restore (do NOT restore to production directly)
aws rds restore-db-instance-to-point-in-time \
  --source-db-instance-identifier $SOURCE_INSTANCE \
  --target-db-instance-identifier $RESTORE_INSTANCE \
  --restore-time $RESTORE_TIME \
  --db-instance-class db.r6g.2xlarge \
  --no-multi-az \
  --tags Key=purpose,Value=pitr-recovery Key=incident,Value=INC-XXXX

# 3. Wait for restore to complete (~20-40 minutes for large databases)
aws rds wait db-instance-available --db-instance-identifier $RESTORE_INSTANCE

# 4. Validate data in restored instance before any promotion
# 5. If promoting, coordinate with incident commander and notify customers
```

### 4.4 Read Replica Failover

**Use case:** Primary RDS instance failure or planned maintenance

```bash
# Check replication lag on read replicas
aws rds describe-db-instances \
  --db-instance-identifier novatech-documents-prod-replica-1 \
  --query 'DBInstances[0].StatusInfos'

# Promote read replica to standalone (breaks replication)
aws rds promote-read-replica \
  --db-instance-identifier novatech-documents-prod-replica-1 \
  --backup-retention-period 7

# Update application database URL (via AWS Secrets Manager)
# The application reads the endpoint at startup; pods need rolling restart
kubectl rollout restart deployment/document-service -n novatech-prod
```

**RTO for replica failover:** ~5-10 minutes (RDS Multi-AZ auto-failover is ~60-90 seconds; application reconnection adds time)

### 4.5 Database Migration Safety Checklist

Before running any migration in production:

- [ ] Migration tested in dev environment
- [ ] Migration tested in staging environment against production-sized dataset
- [ ] Rollback migration written and tested
- [ ] Migration is backwards-compatible (old code can run against new schema, and vice versa)
- [ ] No long-running lock acquisitions (table locks > 1 second are prohibited)
- [ ] Manual snapshot taken within 30 minutes of migration run
- [ ] Migration run scheduled during low-traffic window (or using online migration tools: `pg_repack`)
- [ ] On-call engineer standing by during migration
- [ ] Rollback procedure documented and practiced

---

## 5. Redis Cluster Management (ElastiCache)

### 5.1 Redis Cluster Inventory

| Cluster | Purpose | Instance Type | Shards | Replicas/Shard |
|---------|---------|--------------|--------|---------------|
| `novatech-cache-prod` | General application cache | cache.r6g.large | 6 | 2 |
| `novatech-session-prod` | Auth sessions, token blacklist | cache.r6g.large | 3 | 2 |
| `novatech-search-cache-prod` | Search result cache | cache.r6g.2xlarge | 6 | 2 |

### 5.2 Common Redis Operations

```bash
# Connect to Redis cluster (via bastion host)
redis-cli -h novatech-cache-prod.xxxxxx.use1.cache.amazonaws.com \
  -p 6379 --tls

# Check cluster info
redis-cli cluster info

# Monitor real-time operations
redis-cli monitor  # WARNING: performance impact — use briefly only

# Check memory usage
redis-cli info memory | grep used_memory_human

# Check hit/miss ratio
redis-cli info stats | grep -E "(keyspace_hits|keyspace_misses)"

# Flush a tenant's cache (during incident — use cautiously)
redis-cli --scan --pattern "{tenant_id}:*" | xargs redis-cli del
```

### 5.3 Redis Eviction Policy

- Policy: `volatile-lru` (evict keys with TTL set, using LRU)
- Max memory: 80% of available (leaves headroom for replication)
- If eviction rate spikes, check for missing TTLs on cached keys

---

## 6. Elasticsearch Index Management

### 6.1 Cluster Configuration

- Nodes: 9 data nodes (r6g.4xlarge) + 3 dedicated master nodes (m6g.large)
- Version: 8.12.1
- Cluster: `novatech-search-prod` (Amazon OpenSearch Service compatible)
- Shards per index: 5 (primary) + 1 (replica) = 10 shards per index
- Index lifecycle: Monthly rotation (one index per tenant per month)

### 6.2 Index Naming Convention

```
novatech-{tenant_id}-documents-{YYYY-MM}

Examples:
  novatech-acme-corp-documents-2026-03
  novatech-globaltech-documents-2026-03
  novatech-globaltech-documents-2026-02  (previous month)
```

Aliases point to the current month's index:
```
novatech-acme-corp-documents → novatech-acme-corp-documents-2026-03 (write alias)
novatech-acme-corp-documents-search → [all months] (search alias)
```

### 6.3 Common Elasticsearch Operations

```bash
# Check cluster health
curl -s https://elasticsearch.novatech.internal/_cluster/health | jq

# Check all indices for a tenant
curl -s "https://elasticsearch.novatech.internal/_cat/indices/novatech-acme*?v&h=index,status,docs.count,store.size"

# Check shard allocation
curl -s "https://elasticsearch.novatech.internal/_cat/shards?v&s=state&h=index,shard,prirep,state,node"

# Force segment merge (reduces search overhead — run during off-peak)
curl -X POST "https://elasticsearch.novatech.internal/novatech-acme-corp-documents-2026-01/_forcemerge?max_num_segments=1"

# Take a manual snapshot
curl -X PUT "https://elasticsearch.novatech.internal/_snapshot/novatech-es-backups/snapshot-manual-20260310"
```

### 6.4 Index Performance Tuning

Known performance issues and mitigations:

- **Large tenant index slow queries (ENG-2847):** Tenants with > 10M documents experience p99 > 8s on certain queries. Current mitigation: dedicated node pool routing for top 5 tenants. Permanent fix targeting April 15, 2026.
- **Shard allocation:** Monitor with `_cat/shards` for unassigned shards. Unassigned shards degrade search performance.
- **JVM heap:** Elasticsearch JVM heap at 50% of node memory. Alert fires at 80% heap utilization.

---

## 7. Certificate Management

### 7.1 Certificate Inventory

| Domain | Certificate Provider | Expiry | Auto-Renew |
|--------|---------------------|--------|-----------|
| `*.novatech.io` | AWS Certificate Manager | N/A | Yes (ACM managed) |
| `api.novatech.io` | AWS Certificate Manager | N/A | Yes |
| `*.novatech.internal` | Internal CA (Vault) | 90 days | Yes (cert-manager) |
| `status.novatech.io` | Let's Encrypt (via StatusPage) | 90 days | Yes |

### 7.2 Certificate Rotation Procedure

**External certificates (ACM):** Fully automated. ACM renews 60 days before expiry. No action required.

**Internal certificates (Istio mTLS via cert-manager):**
```bash
# Check certificate status in cluster
kubectl get certificates -A
kubectl describe certificate novatech-internal-tls -n istio-system

# Force certificate renewal (if cert-manager automation fails)
kubectl delete certificaterequest -n istio-system -l cert-manager.io/certificate-name=novatech-internal-tls
```

Alert: Datadog monitor `Certificate Expiry Warning` fires 30 days before expiry.

---

## 8. Secrets Management

All secrets are stored in **AWS Secrets Manager**. No secrets may be stored in:
- Source code
- Environment variables (except references to Secrets Manager ARNs)
- Docker images
- Kubernetes ConfigMaps
- Terraform state files (use `sensitive = true` for values)

### 8.1 Secret Naming Convention

```
novatech/{environment}/{service}/{secret-name}

Examples:
  novatech/prod/auth/jwt-private-key
  novatech/prod/documents/s3-encryption-key
  novatech/prod/billing/stripe-api-key
  novatech/prod/shared/datadog-api-key
```

### 8.2 Common Secret Operations

```bash
# Retrieve a secret
aws secretsmanager get-secret-value \
  --secret-id novatech/prod/auth/jwt-private-key \
  --profile novatech-prod | jq -r .SecretString

# Rotate a secret (auto-rotation)
aws secretsmanager rotate-secret \
  --secret-id novatech/prod/billing/stripe-api-key

# Create a new secret
aws secretsmanager create-secret \
  --name novatech/prod/integrations/new-service-api-key \
  --secret-string '{"api_key": "xxx"}' \
  --tags Key=team,Value=product Key=environment,Value=prod
```

### 8.3 Secret Rotation Schedule

| Secret Type | Rotation Frequency | Auto-Rotation |
|------------|-------------------|--------------|
| Database passwords | 90 days | Yes (Lambda rotator) |
| JWT signing keys | 180 days | Semi-manual (coordinate with Platform team) |
| API keys (third-party) | 90 days | Manual (external service rotation required) |
| Internal service credentials | 180 days | Yes |

---

## 9. Cost Optimization

### 9.1 Resource Tagging Policy

All AWS resources must have the following tags:

| Tag Key | Required | Values | Example |
|---------|---------|--------|---------|
| `Environment` | Yes | prod, staging, dev | `prod` |
| `Team` | Yes | platform, product, data, sre | `data` |
| `Service` | Yes | Service name | `search-service` |
| `CostCenter` | Yes | Engineering, Infrastructure | `Infrastructure` |
| `ManagedBy` | Yes | terraform, manual | `terraform` |

Untagged resources are flagged weekly by AWS Config rules and reported to the relevant team.

### 9.2 Monthly Infrastructure Cost Breakdown (January 2026)

| Component | Monthly Cost | % of Total | Cost Driver |
|-----------|-------------|-----------|------------|
| EKS EC2 (On-Demand) | $24,720 | 24.4% | Growing workload |
| EKS EC2 (Spot) | $16,480 | 16.3% | Batch processing |
| RDS PostgreSQL | $12,800 | 12.7% | Analytics DB growing |
| Elasticsearch | $18,600 | 18.4% | Shard count growth |
| ElastiCache Redis | $6,400 | 6.3% | Cluster expansion |
| Kafka (MSK) | $5,200 | 5.1% | Stable |
| S3 + Transfer | $9,700 | 9.6% | Document growth (+44% YoY) |
| CloudFront | $3,100 | 3.1% | Traffic growth |
| Other | $4,200 | 4.1% | Misc AWS services |
| **Total** | **$101,200** | **100%** | +22% YoY |

### 9.3 Active Cost Optimization Initiatives

| Initiative | Owner | Savings Target | Status |
|-----------|-------|---------------|--------|
| Compute Savings Plans (1-year) | Kevin Osei | $8,000/month | Active since Jan 2026 |
| Spot instance migration (batch workloads) | Dmitri Volkov | $3,500/month | Complete |
| S3 Intelligent-Tiering for old documents | Fatima Al-Hassan | $1,200/month | In progress |
| Elasticsearch shard reduction (optimize sharding) | Data Team | $2,800/month | Planned Q2 2026 |
| Reserved ElastiCache nodes (1-year) | Kevin Osei | $1,800/month | In approval |

### 9.4 Budget Alerts

| Alert Level | Monthly Spend | Action |
|------------|-------------|--------|
| Warning | > $110,000 | Email SRE Lead + Engineering VP |
| Critical | > $125,000 | Page SRE Lead + VP Engineering |
| Emergency | > $150,000 | Page CTO |

---

## 10. Runbook Quick Reference

| Situation | Runbook Section |
|-----------|----------------|
| EKS pod crash-looping | Section 3.4 + check logs |
| RDS failover | Section 4.4 |
| Data recovery needed | Section 4.3 |
| Redis cache full | Section 5.3 |
| Elasticsearch cluster red | Section 6.3 |
| Certificate expiring | Section 7.2 |
| Secret rotation needed | Section 8.2 |
| Cost alert triggered | Section 9.4 |
| Production access needed | Section 2.1 |

---

*This runbook is maintained by the SRE team. For urgent questions during incidents, contact Kevin Osei (Slack: @kevin.osei, phone: +1-628-555-0192) or the current on-call SRE via PagerDuty.*
