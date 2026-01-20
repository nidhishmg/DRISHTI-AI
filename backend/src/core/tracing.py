import uuid
from contextvars import ContextVar
from typing import Optional

_trace_id_ctx: ContextVar[Optional[str]] = ContextVar("trace_id", default=None)

def generate_trace_id() -> str:
    """Generate a new UUID4 trace ID."""
    return str(uuid.uuid4())

def set_trace_id(trace_id: str):
    """Set the current trace ID in context."""
    _trace_id_ctx.set(trace_id)

def get_trace_id() -> str:
    """Get the current trace ID, or generate a new one if not set."""
    tid = _trace_id_ctx.get()
    if not tid:
        tid = generate_trace_id()
        _trace_id_ctx.set(tid)
    return tid

class TraceContext:
    """Context manager for setting a trace ID."""
    def __init__(self, trace_id: Optional[str] = None):
        self.trace_id = trace_id or generate_trace_id()
        self.token = None

    def __enter__(self):
        self.token = _trace_id_ctx.set(self.trace_id)
        return self.trace_id

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.token:
            _trace_id_ctx.reset(self.token)
