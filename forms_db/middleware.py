from django.shortcuts import redirect
from django.urls import reverse

class QARedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Si el usuario está autenticado y es QA
        if (request.user.is_authenticated and 
            hasattr(request.user, 'employes') and 
            request.user.employes.QA):
            
            # URLs permitidas para QA
            allowed_urls = [
                reverse('weekly_failure_report'),
                reverse('logout'),
                reverse('login'),
                # Agrega otras URLs permitidas si es necesario
            ]
            
            # Si no está en una URL permitida, redirigir
            if request.path not in allowed_urls:
                return redirect('weekly_failure_report')
        
        return self.get_response(request)