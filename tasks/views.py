from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .scoring import calculate_task_score
from datetime import date, datetime

@method_decorator(csrf_exempt, name='dispatch')
class AnalyzeTasksView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if not isinstance(data, list):
                return JsonResponse({'error': 'Expected a list of tasks'}, status=400)
            
            analyzed_tasks = []
            for task in data:
                score = calculate_task_score(task)
                task['score'] = score
                analyzed_tasks.append(task)
            
            # Sort by score descending
            analyzed_tasks.sort(key=lambda x: x['score'], reverse=True)
            
            return JsonResponse(analyzed_tasks, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

class SuggestTasksView(View):
    def get(self, request):
        # In a real app, we might fetch from DB. 
        # Here, the prompt implies we might just return suggestions based on some logic?
        # "Return the top 3 tasks the user should work on today"
        # Since this is a GET request without body, where do the tasks come from?
        # The prompt says: "Accept a list of tasks and return them sorted..." for /analyze/
        # For /suggest/, it implies we might need to store them or it's just a mock?
        # "Return the top 3 tasks the user should work on today, with explanations"
        # If we are not persisting tasks in DB from the /analyze/ endpoint (it just returns sorted),
        # then /suggest/ might need to read from DB if we implemented saving.
        # The instructions say "Database: SQLite is fine", and we defined a Model.
        # So we should probably save tasks or assume they are in DB.
        # But the /analyze/ endpoint in the example just takes a list and returns it sorted.
        # Let's assume /suggest/ works on tasks stored in the DB.
        
        # Let's fetch all tasks from DB
        from .models import Task
        tasks = Task.objects.all()
        
        task_list = []
        for t in tasks:
            task_data = {
                'id': t.id,
                'title': t.title,
                'due_date': t.due_date.strftime('%Y-%m-%d'),
                'estimated_hours': t.estimated_hours,
                'importance': t.importance,
                'dependencies': t.dependencies
            }
            score = calculate_task_score(task_data)
            task_data['score'] = score
            task_list.append(task_data)
            
        task_list.sort(key=lambda x: x['score'], reverse=True)
        
        suggestions = task_list[:3]
        
        # Add explanations
        for task in suggestions:
            explanation = []
            if task['score'] >= 100:
                explanation.append("Urgent! Overdue.")
            elif task['score'] >= 50:
                explanation.append("Due very soon.")
            
            if task['importance'] >= 8:
                explanation.append("High importance.")
            
            if task['estimated_hours'] < 2:
                explanation.append("Quick win.")
                
            task['explanation'] = " ".join(explanation) if explanation else "General priority."

        return JsonResponse(suggestions, safe=False)
