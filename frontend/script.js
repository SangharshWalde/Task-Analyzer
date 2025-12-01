document.addEventListener('DOMContentLoaded', () => {
    const taskInput = document.getElementById('taskInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const loadSampleBtn = document.getElementById('loadSampleBtn');
    const clearBtn = document.getElementById('clearBtn');
    const resultsContainer = document.getElementById('resultsContainer');
    const sortStrategy = document.getElementById('sortStrategy');

    const sampleTasks = [
        {
            "title": "Fix critical login bug",
            "due_date": new Date(Date.now() - 86400000).toISOString().split('T')[0], // Yesterday
            "estimated_hours": 4,
            "importance": 10,
            "dependencies": []
        },
        {
            "title": "Update documentation",
            "due_date": new Date(Date.now() + 86400000 * 5).toISOString().split('T')[0], // 5 days later
            "estimated_hours": 1,
            "importance": 4,
            "dependencies": []
        },
        {
            "title": "Refactor database schema",
            "due_date": new Date(Date.now() + 86400000 * 2).toISOString().split('T')[0], // 2 days later
            "estimated_hours": 8,
            "importance": 9,
            "dependencies": []
        },
        {
            "title": "Email team updates",
            "due_date": new Date(Date.now()).toISOString().split('T')[0], // Today
            "estimated_hours": 0.5,
            "importance": 6,
            "dependencies": []
        }
    ];

    loadSampleBtn.addEventListener('click', () => {
        taskInput.value = JSON.stringify(sampleTasks, null, 4);
    });

    clearBtn.addEventListener('click', () => {
        taskInput.value = '';
        resultsContainer.innerHTML = '<div class="placeholder-text">Run analysis to see results</div>';
    });

    analyzeBtn.addEventListener('click', analyzeTasks);

    async function analyzeTasks() {
        const inputData = taskInput.value.trim();
        if (!inputData) {
            alert('Please enter some tasks first.');
            return;
        }

        let tasks;
        try {
            tasks = JSON.parse(inputData);
        } catch (e) {
            alert('Invalid JSON format. Please check your input.');
            return;
        }

        resultsContainer.innerHTML = '<div class="placeholder-text">Analyzing...</div>';

        try {
            const response = await fetch('http://127.0.0.1:8000/api/tasks/analyze/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(tasks)
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            let analyzedTasks = await response.json();

            // Client-side sorting override if needed
            const strategy = sortStrategy.value;
            if (strategy === 'fastest') {
                analyzedTasks.sort((a, b) => a.estimated_hours - b.estimated_hours);
            } else if (strategy === 'impact') {
                analyzedTasks.sort((a, b) => b.importance - a.importance);
            } else if (strategy === 'deadline') {
                analyzedTasks.sort((a, b) => new Date(a.due_date) - new Date(b.due_date));
            }
            // 'smart' uses the server-side score which is already sorted

            displayResults(analyzedTasks);
        } catch (error) {
            console.error('Error:', error);
            resultsContainer.innerHTML = `<div class="placeholder-text" style="color: var(--high-priority)">Error: ${error.message}. Make sure backend is running.</div>`;
        }
    }

    function displayResults(tasks) {
        resultsContainer.innerHTML = '';

        if (tasks.length === 0) {
            resultsContainer.innerHTML = '<div class="placeholder-text">No tasks found.</div>';
            return;
        }

        tasks.forEach(task => {
            const card = document.createElement('div');
            card.className = `task-card ${getPriorityClass(task.score)}`;

            // Generate explanation if not provided by backend (backend logic is in Python, but we can infer or just show score)
            // The prompt says "Show a brief explanation of why each task received its score".
            // Since our backend returns the score but maybe not the explanation string for /analyze/,
            // we can generate a simple one here or rely on what we have.
            // Let's generate a simple one based on score components if backend doesn't send 'explanation'.

            const explanation = task.explanation || generateExplanation(task);

            card.innerHTML = `
                <div class="task-header">
                    <h3 class="task-title">${task.title}</h3>
                    <span class="task-score">Score: ${task.score}</span>
                </div>
                <div class="task-details">
                    <span>📅 Due: ${task.due_date}</span>
                    <span>⏱️ Effort: ${task.estimated_hours}h</span>
                    <span>⭐ Importance: ${task.importance}/10</span>
                </div>
                <div class="explanation">
                    💡 ${explanation}
                </div>
            `;
            resultsContainer.appendChild(card);
        });
    }

    function getPriorityClass(score) {
        if (score >= 100) return 'priority-high';
        if (score >= 50) return 'priority-medium';
        return 'priority-low';
    }

    function generateExplanation(task) {
        let reasons = [];
        const today = new Date().toISOString().split('T')[0];

        if (task.due_date < today) reasons.push("Overdue!");
        else if (task.due_date === today) reasons.push("Due today!");

        if (task.importance >= 8) reasons.push("High importance.");
        if (task.estimated_hours < 2) reasons.push("Quick win.");

        if (reasons.length === 0) return "Standard priority.";
        return reasons.join(" ");
    }
});
