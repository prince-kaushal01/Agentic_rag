"""
Task memory — per-task state that survives tool calls.
Stored in Redis with a 1-hour TTL.
"""
from __future__ import annotations

from backend.memory.redis_store import RedisStore


class TaskMemory:
    """
    Persists agent state snapshots and tool call results for a single task.
    Key: task_mem:{task_id}      → JSON dict (full state snapshot)
         task_tools:{task_id}    → Redis list of tool call records
    """

    TTL = 3600  # 1 hour

    @staticmethod
    def _state_key(task_id: str) -> str:
        return f"task_mem:{task_id}"

    @staticmethod
    def _tools_key(task_id: str) -> str:
        return f"task_tools:{task_id}"

    @staticmethod
    async def save_state(task_id: str, state: dict) -> None:
        """Persist a full task state snapshot (for crash recovery / inspection)."""
        # Store only serializable fields
        safe_state = {
            k: v for k, v in state.items()
            if isinstance(v, (str, int, float, bool, list, dict, type(None)))
        }
        await RedisStore.set(TaskMemory._state_key(task_id), safe_state, ttl_seconds=TaskMemory.TTL)

    @staticmethod
    async def load_state(task_id: str) -> dict | None:
        """Load the last saved state snapshot."""
        return await RedisStore.get(TaskMemory._state_key(task_id))

    @staticmethod
    async def record_tool_call(task_id: str, tool_name: str, result: dict) -> None:
        """Append a tool call result to the task's tool log."""
        entry = {
            "tool_name": tool_name,
            "result": result,
        }
        await RedisStore.append_to_list(
            TaskMemory._tools_key(task_id),
            entry,
            max_length=50,
            ttl_seconds=TaskMemory.TTL,
        )

    @staticmethod
    async def get_tool_results(task_id: str) -> list[dict]:
        """Retrieve all recorded tool calls for this task."""
        return await RedisStore.get_list(TaskMemory._tools_key(task_id))

    @staticmethod
    async def clear(task_id: str) -> None:
        """Delete all task memory (call after task completes to free Redis memory)."""
        await RedisStore.delete(TaskMemory._state_key(task_id))
        await RedisStore.delete(TaskMemory._tools_key(task_id))
