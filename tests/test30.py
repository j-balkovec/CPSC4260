def log_message_simple_v1(message, level="INFO"):
    """Logs a simple message."""
    return f"[{level.upper()}]: {message}"

def audit_action_simple_v1(action, user):
    """Audits a simple user action."""
    return f"[AUDIT]: User {user} performed {action}" # Similar to log_message_simple_v1

def log_event_detailed_v2(event_type, details, timestamp=None, severity="MEDIUM", source="SYSTEM"):
    """Logs a detailed event with timestamp and severity."""
    import datetime
    ts = timestamp if timestamp else datetime.datetime.now().isoformat()
    return f"[{ts}] [{severity.upper()}] [{source.upper()}]: {event_type} - {details}"

def audit_operation_complex_v2(operation_name, performed_by, details_data=None, event_time=None, priority="NORMAL", component="APPLICATION"):
    """Audits a complex operation with detailed data and context.""" # Similar structure to log_event_detailed_v2
    import datetime
    et = event_time if event_time else datetime.datetime.now().isoformat()
    details_str = str(details_data) if details_data else "No details"
    return f"[{et}] [PRIORITY: {priority.upper()}] [{component.upper()}]: Operation {operation_name} by {performed_by} - Details: {details_str}"