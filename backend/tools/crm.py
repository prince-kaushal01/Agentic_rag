"""
Simulated CRM tools — synthetic NovaTech customer data.
No real CRM API required; demonstrates multi-system orchestration.
"""
from __future__ import annotations

import re
from datetime import date

# ── Synthetic CRM data ────────────────────────────────────────────────────────

_CUSTOMERS: dict[str, dict] = {
    "CUST-001": {
        "id": "CUST-001",
        "name": "Acme Corp",
        "industry": "Manufacturing",
        "tier": "Enterprise",
        "arr_usd": 480_000,
        "status": "active",
        "health_score": 72,
        "primary_contact": {"name": "Sarah Chen", "email": "s.chen@acmecorp.com", "title": "VP Engineering"},
        "account_manager": "Jordan Rivers",
        "region": "North America",
        "employees": 2400,
        "renewal_date": "2025-06-30",
        "notes": "Expanding usage to 3 additional business units in Q3.",
    },
    "CUST-002": {
        "id": "CUST-002",
        "name": "TechFlow Inc",
        "industry": "SaaS",
        "tier": "Growth",
        "arr_usd": 120_000,
        "status": "active",
        "health_score": 91,
        "primary_contact": {"name": "Marcus Webb", "email": "m.webb@techflow.io", "title": "CTO"},
        "account_manager": "Priya Sharma",
        "region": "North America",
        "employees": 340,
        "renewal_date": "2025-09-15",
        "notes": "Champion-driven adoption; strong NPS. Potential for upsell to Enterprise.",
    },
    "CUST-003": {
        "id": "CUST-003",
        "name": "Meridian Financial",
        "industry": "Financial Services",
        "tier": "Enterprise",
        "arr_usd": 720_000,
        "status": "at_risk",
        "health_score": 44,
        "primary_contact": {"name": "Diana Okafor", "email": "d.okafor@meridianfin.com", "title": "Head of IT"},
        "account_manager": "Jordan Rivers",
        "region": "EMEA",
        "employees": 8700,
        "renewal_date": "2025-03-31",
        "notes": "Compliance team raised concerns about data residency. Escalation required.",
    },
    "CUST-004": {
        "id": "CUST-004",
        "name": "BlueSky Logistics",
        "industry": "Logistics",
        "tier": "Startup",
        "arr_usd": 36_000,
        "status": "active",
        "health_score": 83,
        "primary_contact": {"name": "Tom Keller", "email": "tkeller@blueskylogi.com", "title": "CEO"},
        "account_manager": "Priya Sharma",
        "region": "North America",
        "employees": 95,
        "renewal_date": "2025-12-01",
        "notes": "Fast-growing startup. Consider inviting to beta program.",
    },
    "CUST-005": {
        "id": "CUST-005",
        "name": "Quantum Health Systems",
        "industry": "Healthcare",
        "tier": "Enterprise",
        "arr_usd": 540_000,
        "status": "active",
        "health_score": 68,
        "primary_contact": {"name": "Anya Petrov", "email": "a.petrov@quantumhealth.com", "title": "CISO"},
        "account_manager": "Jordan Rivers",
        "region": "North America",
        "employees": 5100,
        "renewal_date": "2025-08-31",
        "notes": "HIPAA compliance is top priority. Legal review in progress for BAA addendum.",
    },
}

_CONTRACTS: dict[str, dict] = {
    "CUST-001": {
        "contract_id": "CTR-2024-001",
        "customer_id": "CUST-001",
        "value_usd": 480_000,
        "start_date": "2024-07-01",
        "end_date": "2025-06-30",
        "billing_cycle": "annual",
        "payment_terms": "Net 30",
        "auto_renew": True,
        "seats": 500,
        "modules": ["core_rag", "agent_runtime", "analytics"],
        "sla_tier": "platinum",
        "signed_date": "2024-06-15",
    },
    "CUST-002": {
        "contract_id": "CTR-2024-002",
        "customer_id": "CUST-002",
        "value_usd": 120_000,
        "start_date": "2024-10-01",
        "end_date": "2025-09-30",
        "billing_cycle": "annual",
        "payment_terms": "Net 30",
        "auto_renew": False,
        "seats": 100,
        "modules": ["core_rag", "agent_runtime"],
        "sla_tier": "gold",
        "signed_date": "2024-09-20",
    },
    "CUST-003": {
        "contract_id": "CTR-2024-003",
        "customer_id": "CUST-003",
        "value_usd": 720_000,
        "start_date": "2024-04-01",
        "end_date": "2025-03-31",
        "billing_cycle": "annual",
        "payment_terms": "Net 60",
        "auto_renew": True,
        "seats": 1000,
        "modules": ["core_rag", "agent_runtime", "analytics", "compliance_pack"],
        "sla_tier": "platinum",
        "signed_date": "2024-03-10",
    },
    "CUST-004": {
        "contract_id": "CTR-2024-004",
        "customer_id": "CUST-004",
        "value_usd": 36_000,
        "start_date": "2025-01-01",
        "end_date": "2025-12-31",
        "billing_cycle": "annual",
        "payment_terms": "Net 30",
        "auto_renew": True,
        "seats": 25,
        "modules": ["core_rag"],
        "sla_tier": "silver",
        "signed_date": "2024-12-20",
    },
    "CUST-005": {
        "contract_id": "CTR-2024-005",
        "customer_id": "CUST-005",
        "value_usd": 540_000,
        "start_date": "2024-09-01",
        "end_date": "2025-08-31",
        "billing_cycle": "annual",
        "payment_terms": "Net 30",
        "auto_renew": True,
        "seats": 750,
        "modules": ["core_rag", "agent_runtime", "analytics", "hipaa_pack"],
        "sla_tier": "platinum",
        "signed_date": "2024-08-25",
    },
}


def _find_customer(customer_id: str | None = None, name: str | None = None) -> dict | None:
    """Look up a customer by ID or fuzzy name match."""
    if customer_id:
        return _CUSTOMERS.get(customer_id.upper())
    if name:
        name_lower = name.lower()
        for c in _CUSTOMERS.values():
            if name_lower in c["name"].lower():
                return c
    return None


# ── Tool handlers ──────────────────────────────────────────────────────────────

async def get_customer(
    customer_id: str | None = None,
    name: str | None = None,
    tenant_id: str = "",
    **kwargs,
) -> dict:
    """Look up a NovaTech customer by ID or name."""
    customer = _find_customer(customer_id, name)
    if customer is None:
        return {
            "found": False,
            "query": customer_id or name,
            "message": "No customer found matching the given ID or name.",
            "available_customers": [c["name"] for c in _CUSTOMERS.values()],
        }
    return {"found": True, "customer": customer}


async def get_customer_contract(
    customer_id: str,
    tenant_id: str = "",
    **kwargs,
) -> dict:
    """Retrieve contract details for a customer."""
    customer = _find_customer(customer_id)
    if customer is None:
        # Try by name
        customer = _find_customer(name=customer_id)

    if customer is None:
        return {"found": False, "message": f"Customer '{customer_id}' not found."}

    cid = customer["id"]
    contract = _CONTRACTS.get(cid)
    if contract is None:
        return {"found": False, "message": f"No contract on file for {customer['name']}."}

    # Flag if expiring within 90 days
    try:
        end = date.fromisoformat(contract["end_date"])
        days_remaining = (end - date.today()).days
        contract = {**contract, "days_until_renewal": days_remaining}
        if days_remaining < 90:
            contract["renewal_alert"] = f"Contract expires in {days_remaining} days — renewal action required."
    except Exception:
        pass

    return {"found": True, "customer": customer["name"], "contract": contract}
