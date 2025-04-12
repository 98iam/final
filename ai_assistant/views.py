from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json

from .services import ai_service

@login_required
def ai_sidebar(request):
    """Render the AI assistant sidebar"""
    return render(request, 'ai_assistant/sidebar.html')

@login_required
@require_POST
def query_ai(request):
    """Handle AI queries from the sidebar"""
    try:
        data = json.loads(request.body)
        query = data.get('query', '')

        if not query.strip():
            return JsonResponse({
                'success': False,
                'error': 'Query cannot be empty'
            })

        # Get response from AI service
        result = ai_service.query_ai(query, request.user)

        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
