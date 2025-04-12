from .models import UserPreference

class ThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Set default theme
        request.theme = 'light'
        
        # Check if user is authenticated
        if request.user.is_authenticated:
            # Try to get user preference
            try:
                preference = UserPreference.objects.get(user=request.user)
                request.theme = preference.theme
            except UserPreference.DoesNotExist:
                # Create default preference for user
                UserPreference.objects.create(user=request.user, theme='light')
        
        response = self.get_response(request)
        return response
