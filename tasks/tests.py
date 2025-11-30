from django.test import TestCase
from datetime import date, timedelta
from .scoring import calculate_task_score

class ScoringAlgorithmTests(TestCase):
    def test_overdue_task_score(self):
        """Overdue tasks should have a very high score (base 100+)"""
        yesterday = date.today() - timedelta(days=1)
        task = {
            'title': 'Overdue Task',
            'due_date': yesterday.strftime('%Y-%m-%d'),
            'importance': 5,
            'estimated_hours': 3
        }
        score = calculate_task_score(task)
        # 100 (overdue) + 25 (importance * 5) = 125
        self.assertGreaterEqual(score, 125)

    def test_urgent_task_score(self):
        """Tasks due within 3 days should have a high score"""
        tomorrow = date.today() + timedelta(days=1)
        task = {
            'title': 'Urgent Task',
            'due_date': tomorrow.strftime('%Y-%m-%d'),
            'importance': 5,
            'estimated_hours': 3
        }
        score = calculate_task_score(task)
        # 50 (due soon) + 25 (importance) = 75
        self.assertEqual(score, 75)

    def test_quick_win_score(self):
        """Quick tasks (< 2 hours) should get a bonus"""
        next_week = date.today() + timedelta(days=10)
        task = {
            'title': 'Quick Task',
            'due_date': next_week.strftime('%Y-%m-%d'),
            'importance': 5,
            'estimated_hours': 1
        }
        score = calculate_task_score(task)
        # 0 (urgency) + 25 (importance) + 10 (quick win) = 35
        self.assertEqual(score, 35)

    def test_high_importance_score(self):
        """High importance tasks should have higher scores"""
        next_week = date.today() + timedelta(days=10)
        task_high = {
            'title': 'Important Task',
            'due_date': next_week.strftime('%Y-%m-%d'),
            'importance': 10,
            'estimated_hours': 5
        }
        task_low = {
            'title': 'Unimportant Task',
            'due_date': next_week.strftime('%Y-%m-%d'),
            'importance': 1,
            'estimated_hours': 5
        }
        score_high = calculate_task_score(task_high)
        score_low = calculate_task_score(task_low)
        
        # High: 50 (importance)
        # Low: 5 (importance)
        self.assertGreater(score_high, score_low)
