# Smart Task Analyzer

A mini-application that intelligently scores and prioritizes tasks based on multiple factors like urgency, importance, and effort.

## Setup Instructions

1.  **Prerequisites**: Python 3.8+ installed.
2.  **Navigate to project directory**:
    ```bash
    cd task-analyzer
    ```
3.  **Create and activate virtual environment**:
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```
4.  **Install dependencies**:
    ```bash
    pip install django django-cors-headers
    ```
5.  **Run migrations**:
    ```bash
    python manage.py migrate
    ```
6.  **Run the server**:
    ```bash
    python manage.py runserver
    ```
7.  **Open the application**:
    Open `frontend/index.html` in your browser.

## Algorithm Explanation

The core of the Smart Task Analyzer is a scoring function designed to surface the most critical tasks while also identifying "quick wins" to maintain momentum. The algorithm calculates a numerical score for each task, where a higher score indicates higher priority.

The scoring logic considers three primary factors:

1.  **Urgency (Time Sensitivity)**:
    -   The algorithm calculates the number of days between today and the due date.
    -   **Overdue Tasks**: These are critical. Any task with a past due date receives a massive **+100 point** boost. This ensures they immediately jump to the top of the list.
    -   **Imminent Deadlines**: Tasks due within the next 3 days receive a **+50 point** boost. This creates a "warning zone" for users.
    -   **Upcoming Week**: Tasks due within 7 days get a smaller **+20 point** boost to keep them on the radar.

2.  **Importance (User Weighting)**:
    -   Users assign an importance rating from 1 to 10.
    -   This rating is multiplied by **5**.
    -   *Rationale*: A maximum importance task (10) gets 50 points, which is equivalent to a task due in 3 days. This balances "Urgent" vs "Important" effectively—a highly important task due next week might outrank a low-importance task due tomorrow.

3.  **Effort (Quick Wins)**:
    -   Productivity often stalls when facing large tasks. To combat this, the algorithm rewards low-effort tasks.
    -   Any task estimated to take less than **2 hours** receives a **+10 point** bonus. This encourages users to clear small items quickly.

**Handling Edge Cases**:
-   **Missing Dates**: If a due date is missing or invalid, the system defaults to "today" to ensure the task isn't lost at the bottom.
-   **Dependencies**: While the data model supports dependencies, the current scoring algorithm focuses on individual task attributes for speed and simplicity (O(N) complexity).

## Design Decisions

-   **Django Backend**: Chosen for its robust ORM and rapid development capabilities. It allows for easy expansion into a full database-backed application with user authentication in the future.
-   **Vanilla Frontend**: To keep the project lightweight and meet the requirement of no build steps, I used plain HTML/CSS/JS. This ensures the app can be run by simply opening a file, reducing friction for the reviewer.
-   **Stateless Analysis**: The `/analyze/` endpoint is stateless. It accepts a list of tasks and returns them sorted. This makes the API extremely easy to test and integrates well with the "bulk paste" feature on the frontend.
-   **CORS Configuration**: Enabled CORS to allow the local HTML file to communicate with the local Django server without browser security blocking the requests.

## Time Breakdown

-   **Project Setup**: 15 mins
-   **Backend Logic**: 45 mins
-   **Frontend UI/Logic**: 45 mins
-   **Documentation & Polish**: 30 mins

## Bonus Challenges

I successfully implemented the following bonus challenge:

-   **Unit Tests**: I wrote comprehensive unit tests in `tasks/tests.py` to verify the scoring algorithm. These tests cover:
    -   Overdue task scoring.
    -   Urgent task scoring (within 3 days).
    -   Quick win bonuses.
    -   Importance weighting comparisons.

## Future Improvements

With more time, I would implement:

1.  **Dependency Graph**: A topological sort to ensure blocking tasks are always recommended before the tasks they block.
2.  **User Authentication**: To allow users to save their task lists permanently.
3.  **Date Intelligence**: Skipping weekends when calculating "days until due" to provide a more realistic urgency score for business contexts.
4.  **Eisenhower Matrix View**: A frontend visualization plotting tasks on an Urgent vs. Important grid.
