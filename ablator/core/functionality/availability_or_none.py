def _availability_or_none(availability):
    if availability:
        if availability.is_enabled:
            return availability
    return None
