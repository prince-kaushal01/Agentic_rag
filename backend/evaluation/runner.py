"""
Evaluation runner — executes test cases against the live RAG system and
computes Recall@K, Precision@K, MRR, Answer Correctness, and Tool Selection
Accuracy.

Usage (from repo root):
    python -m backend.evaluation.runner [--mode retrieval|agent|security|all]
                                        [--top-k 5]
                                        [--output results.json]
"""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import time
import uuid
from dataclasses import dataclass, asdict, field
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

from backend.evaluation.test_cases import (
    RETRIEVAL_TEST_CASES,
    AGENT_TEST_CASES,
    SECURITY_TEST_CASES,
    TestCase,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


# ── Result data classes ────────────────────────────────────────────────────────

@dataclass
class CaseResult:
    case_id: str
    case_type: str
    query: str
    passed: bool
    latency_ms: int
    keywords_found: list[str]
    keywords_missing: list[str]
    sources_found: list[str]
    recall_at_k: float       # fraction of expected_sources retrieved in top-K
    precision_at_k: float    # fraction of returned sources that are expected
    mrr: float               # reciprocal rank of first relevant source
    answer_snippet: str      # first 200 chars of answer
    tool_correct: Optional[bool] = None  # for agent cases
    injection_blocked: Optional[bool] = None  # for security cases
    error: Optional[str] = None


@dataclass
class EvalReport:
    total: int = 0
    passed: int = 0
    failed: int = 0
    avg_latency_ms: float = 0.0
    avg_recall_at_k: float = 0.0
    avg_precision_at_k: float = 0.0
    avg_mrr: float = 0.0
    answer_correctness: float = 0.0  # keyword-based proxy (0–1)
    tool_selection_accuracy: float = 0.0
    security_block_rate: float = 0.0
    results: list[CaseResult] = field(default_factory=list)


# ── Metrics helpers ────────────────────────────────────────────────────────────

def recall_at_k(retrieved_files: list[str], expected_files: list[str]) -> float:
    if not expected_files:
        return 1.0  # no expectation → trivially satisfied
    hits = sum(1 for ef in expected_files if any(ef.lower() in rf.lower() for rf in retrieved_files))
    return hits / len(expected_files)


def precision_at_k(retrieved_files: list[str], expected_files: list[str]) -> float:
    if not retrieved_files or not expected_files:
        return 1.0
    hits = sum(1 for rf in retrieved_files if any(ef.lower() in rf.lower() for ef in expected_files))
    return hits / len(retrieved_files)


def mrr_score(retrieved_files: list[str], expected_files: list[str]) -> float:
    """Mean Reciprocal Rank — here just RR since we have one query."""
    if not expected_files:
        return 1.0
    for rank, rf in enumerate(retrieved_files, start=1):
        if any(ef.lower() in rf.lower() for ef in expected_files):
            return 1.0 / rank
    return 0.0


def keyword_hit_rate(answer: str, expected_keywords: list[str]) -> tuple[list[str], list[str]]:
    answer_lower = answer.lower()
    found = [kw for kw in expected_keywords if kw.lower() in answer_lower]
    missing = [kw for kw in expected_keywords if kw.lower() not in answer_lower]
    return found, missing


# ── Retrieval runner ───────────────────────────────────────────────────────────

async def _run_retrieval_case(case: TestCase, top_k: int, tenant_id: uuid.UUID) -> CaseResult:
    """Run a single retrieval/answer test case directly against the RAG pipeline."""
    from backend.database.connection import AsyncSessionLocal
    from backend.retrieval.hybrid import hybrid_search
    from backend.retrieval.reranker import rerank
    from backend.retrieval.context_builder import build_context
    from backend.retrieval.llm import answer_with_context
    from backend.auth.permissions import get_permissions

    start = time.monotonic()
    error = None
    answer = ""
    retrieved_files: list[str] = []

    try:
        # Use manager-level permissions to ensure restricted docs are accessible
        perms = get_permissions("manager")

        async with AsyncSessionLocal() as session:
            candidates = await hybrid_search(
                session=session,
                query=case.query,
                tenant_id=tenant_id,
                top_k=top_k * 3,
                access_level=perms.max_access_level,
                departments=perms.allowed_departments,
                semantic_k=top_k * 3,
                keyword_k=top_k * 3,
            )

        reranked = await asyncio.to_thread(rerank, case.query, candidates, top_k)
        retrieved_files = [c.file_name for c in reranked]

        ctx = build_context(reranked)
        llm_resp = await asyncio.to_thread(answer_with_context, case.query, ctx, [])
        answer = llm_resp.answer

    except Exception as exc:
        error = str(exc)
        logger.warning("Case %s error: %s", case.id, exc)

    latency_ms = int((time.monotonic() - start) * 1000)
    found_kws, missing_kws = keyword_hit_rate(answer, case.expected_keywords)
    rak = recall_at_k(retrieved_files, case.expected_sources)
    pak = precision_at_k(retrieved_files, case.expected_sources)
    mrr = mrr_score(retrieved_files, case.expected_sources)

    passed = (
        error is None
        and (len(found_kws) / max(len(case.expected_keywords), 1)) >= 0.5
    )

    return CaseResult(
        case_id=case.id,
        case_type=case.case_type,
        query=case.query,
        passed=passed,
        latency_ms=latency_ms,
        keywords_found=found_kws,
        keywords_missing=missing_kws,
        sources_found=retrieved_files,
        recall_at_k=rak,
        precision_at_k=pak,
        mrr=mrr,
        answer_snippet=answer[:200],
        error=error,
    )


# ── Security runner ────────────────────────────────────────────────────────────

async def _run_security_case(case: TestCase) -> CaseResult:
    """Check that adversarial queries are blocked or neutralized."""
    from backend.security.prompt_injection import PromptInjectionDefense
    from backend.security.pii_detector import PIIDetector

    start = time.monotonic()
    injection_blocked = False

    is_safe, threats = PromptInjectionDefense.is_safe_query(case.query)
    if not is_safe:
        injection_blocked = True

    latency_ms = int((time.monotonic() - start) * 1000)

    return CaseResult(
        case_id=case.id,
        case_type="security",
        query=case.query,
        passed=injection_blocked if case.is_adversarial else is_safe,
        latency_ms=latency_ms,
        keywords_found=[],
        keywords_missing=[],
        sources_found=[],
        recall_at_k=1.0,
        precision_at_k=1.0,
        mrr=1.0,
        answer_snippet="[blocked]" if injection_blocked else "[not blocked]",
        injection_blocked=injection_blocked,
    )


# ── Agent runner ───────────────────────────────────────────────────────────────

async def _run_agent_case(case: TestCase, tenant_id: uuid.UUID) -> CaseResult:
    """Run an agent test case through the full LangGraph pipeline."""
    from backend.agents.state import initial_state
    from backend.agents.graph import build_graph

    start = time.monotonic()
    error = None
    answer = ""
    tool_correct: Optional[bool] = None
    tools_used: list[str] = []

    try:
        state = initial_state(
            task_id=str(uuid.uuid4()),
            user_id=str(uuid.uuid4()),
            tenant_id=str(tenant_id),
            role="account_manager",
            user_query=case.query,
            step_budget=8,
        )
        graph = build_graph()
        final = await graph.ainvoke(state)
        answer = final.get("final_answer") or ""
        tools_used = [
            s["tool_name"]
            for s in final.get("steps_completed", [])
            if s.get("tool_name")
        ]
        if case.expected_tool:
            tool_correct = case.expected_tool in tools_used

    except Exception as exc:
        error = str(exc)
        logger.warning("Agent case %s error: %s", case.id, exc)

    latency_ms = int((time.monotonic() - start) * 1000)
    found_kws, missing_kws = keyword_hit_rate(answer, case.expected_keywords)
    passed = (
        error is None
        and (tool_correct is not False)
        and (len(found_kws) / max(len(case.expected_keywords), 1)) >= 0.4
    )

    return CaseResult(
        case_id=case.id,
        case_type="agent",
        query=case.query,
        passed=passed,
        latency_ms=latency_ms,
        keywords_found=found_kws,
        keywords_missing=missing_kws,
        sources_found=tools_used,
        recall_at_k=1.0,
        precision_at_k=1.0,
        mrr=1.0,
        answer_snippet=answer[:200],
        tool_correct=tool_correct,
        error=error,
    )


# ── Main runner ────────────────────────────────────────────────────────────────

async def run_evaluation(
    mode: str = "all",
    top_k: int = 5,
    tenant_id: uuid.UUID | None = None,
) -> EvalReport:
    """
    Run evaluation suite and return an EvalReport.

    Args:
        mode: "retrieval" | "agent" | "security" | "all"
        top_k: Number of chunks to retrieve per query
        tenant_id: UUID of the tenant to run against (uses env DEFAULT_TENANT_ID or first org)
    """
    # Resolve tenant
    if tenant_id is None:
        tid_str = os.getenv("DEFAULT_TENANT_ID")
        if tid_str:
            tenant_id = uuid.UUID(tid_str)
        else:
            # Fall back: fetch first organization from DB
            from backend.database.connection import AsyncSessionLocal
            from backend.database.models.users import Organization
            from sqlalchemy import select
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(Organization).limit(1))
                org = result.scalar_one_or_none()
                if org is None:
                    raise RuntimeError("No organization found — run seed.py first")
                tenant_id = org.id

    report = EvalReport()
    tasks: list[asyncio.Task] = []

    if mode in ("retrieval", "all"):
        for case in RETRIEVAL_TEST_CASES:
            tasks.append(asyncio.create_task(
                _run_retrieval_case(case, top_k, tenant_id),
                name=case.id,
            ))

    if mode in ("security", "all"):
        for case in SECURITY_TEST_CASES:
            tasks.append(asyncio.create_task(
                _run_security_case(case),
                name=case.id,
            ))

    results = await asyncio.gather(*tasks, return_exceptions=True)

    for res in results:
        if isinstance(res, Exception):
            logger.error("Unhandled case error: %s", res)
            continue
        report.results.append(res)

    # Run agent cases sequentially (outside gather) to avoid DB contention
    if mode in ("agent", "all"):
        for case in AGENT_TEST_CASES:
            res = await _run_agent_case(case, tenant_id)
            report.results.append(res)

    # Compute aggregate metrics
    report.total = len(report.results)
    report.passed = sum(1 for r in report.results if r.passed)
    report.failed = report.total - report.passed
    report.avg_latency_ms = (
        sum(r.latency_ms for r in report.results) / report.total
        if report.total else 0.0
    )

    retrieval_results = [r for r in report.results if r.case_type in ("retrieval", "answer")]
    if retrieval_results:
        report.avg_recall_at_k = sum(r.recall_at_k for r in retrieval_results) / len(retrieval_results)
        report.avg_precision_at_k = sum(r.precision_at_k for r in retrieval_results) / len(retrieval_results)
        report.avg_mrr = sum(r.mrr for r in retrieval_results) / len(retrieval_results)
        all_kw_rates = []
        for r in retrieval_results:
            total_kw = len(r.keywords_found) + len(r.keywords_missing)
            if total_kw > 0:
                all_kw_rates.append(len(r.keywords_found) / total_kw)
        report.answer_correctness = sum(all_kw_rates) / len(all_kw_rates) if all_kw_rates else 0.0

    agent_results = [r for r in report.results if r.case_type == "agent" and r.tool_correct is not None]
    if agent_results:
        report.tool_selection_accuracy = sum(1 for r in agent_results if r.tool_correct) / len(agent_results)

    security_results = [r for r in report.results if r.case_type == "security" and r.injection_blocked is not None]
    if security_results:
        report.security_block_rate = sum(1 for r in security_results if r.injection_blocked) / len(security_results)

    return report


def _print_report(report: EvalReport) -> None:
    print("\n" + "=" * 70)
    print("  EVALUATION REPORT")
    print("=" * 70)
    print(f"  Total cases  : {report.total}")
    print(f"  Passed       : {report.passed}  ({100 * report.passed / max(report.total, 1):.1f}%)")
    print(f"  Failed       : {report.failed}")
    print(f"  Avg latency  : {report.avg_latency_ms:.0f} ms")
    print(f"  Recall@K     : {report.avg_recall_at_k:.3f}")
    print(f"  Precision@K  : {report.avg_precision_at_k:.3f}")
    print(f"  MRR          : {report.avg_mrr:.3f}")
    print(f"  Answer corr. : {report.answer_correctness:.3f}")
    print(f"  Tool acc.    : {report.tool_selection_accuracy:.3f}")
    print(f"  Sec. block%  : {report.security_block_rate:.3f}")
    print("=" * 70)

    failures = [r for r in report.results if not r.passed]
    if failures:
        print(f"\nFailed cases ({len(failures)}):")
        for r in failures[:10]:
            print(f"  [{r.case_id}] {r.query[:60]}...")
            if r.error:
                print(f"    error: {r.error}")
            elif r.keywords_missing:
                print(f"    missing keywords: {r.keywords_missing[:3]}")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run RAG evaluation suite")
    parser.add_argument("--mode", choices=["retrieval", "agent", "security", "all"], default="retrieval")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--output", type=str, default=None, help="Write JSON report to file")
    args = parser.parse_args()

    report = asyncio.run(run_evaluation(mode=args.mode, top_k=args.top_k))
    _print_report(report)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(
                {
                    "summary": {
                        k: v for k, v in asdict(report).items() if k != "results"
                    },
                    "results": [asdict(r) for r in report.results],
                },
                f,
                indent=2,
            )
        print(f"Report written to {args.output}")
