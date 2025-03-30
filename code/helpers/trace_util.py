from agents import trace


def get_trace_url(tr: trace) -> str:
    tracing_url = f"https://platform.openai.com/traces/trace?trace_id={tr.trace_id}"
    return tracing_url