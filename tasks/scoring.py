from datetime import date, datetime

def calculate_task_score(task_data):
    """
    Calculates a priority score.
    Higher score = Higher priority.
    """
    score = 0

    # Parse due_date if it's a string
    due_date = task_data.get('due_date')
    if isinstance(due_date, str):
        try:
            due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
        except ValueError:
            # Handle invalid date format, maybe default to today or ignore urgency
            due_date = date.today()
    elif due_date is None:
         due_date = date.today() # Default to today if missing

    # 1. Urgency Calculation
    today = date.today()
    days_until_due = (due_date - today).days

    if days_until_due < 0:
        score += 100  # OVERDUE! Huge priority boost
    elif days_until_due <= 3:
        score += 50   # Due very soon
    elif days_until_due <= 7:
        score += 20   # Due this week

    # 2. Importance Weighting
    importance = task_data.get('importance', 5)
    score += (importance * 5) # Multiply to give it weight

    # 3. Effort (Quick wins logic)
    estimated_hours = task_data.get('estimated_hours', 1)
    if estimated_hours < 2:
        score += 10 # Small bonus for quick tasks
    
    # 4. Dependency Handling (Basic)
    # If a task has dependencies, it might be blocked, so maybe lower priority?
    # Or if we want to prioritize tasks that block others, we need more context.
    # For this assignment, let's assume we want to clear dependencies first.
    # But wait, if Task A depends on Task B, Task B should be done first.
    # So Task B should have higher priority?
    # The input `task_data` only knows what IT depends on.
    # We can't easily know if it blocks others without the full list.
    # So we'll stick to the core factors for now.

    return score
