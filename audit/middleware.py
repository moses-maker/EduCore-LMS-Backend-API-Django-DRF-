"""
Audit middleware for tracking user actions.
"""

import json
from django.utils.deprecation import MiddlewareMixin
from apps.audit.models import AuditLog, ActionType


class AuditMiddleware(MiddlewareMixin):
    """
    Middleware to automatically log certain actions.
    Logs CREATE, UPDATE, DELETE operations on models.
    """
    
    # Methods to log
    LOGGED_METHODS = ['POST', 'PUT', 'PATCH', 'DELETE']
    
    # Paths to exclude from logging
    EXCLUDED_PATHS = [
        '/admin/',
        '/api/schema/',
        '/api/docs/',
        '/static/',
        '/media/',
    ]
    
    def should_log(self, request):
        """Determine if request should be logged"""
        # Check if method should be logged
        if request.method not in self.LOGGED_METHODS:
            return False
        
        # Check if path is excluded
        for excluded in self.EXCLUDED_PATHS:
            if request.path.startswith(excluded):
                return False
        
        # Only log authenticated requests
        if not request.user.is_authenticated:
            return False
        
        return True
    
    def get_action_type(self, method):
        """Map HTTP method to action type"""
        mapping = {
            'POST': ActionType.CREATE,
            'PUT': ActionType.UPDATE,
            'PATCH': ActionType.UPDATE,
            'DELETE': ActionType.DELETE,
        }
        return mapping.get(method, ActionType.CREATE)
    
    def get_request_body(self, request):
        """Safely extract request body"""
        try:
            if hasattr(request, '_body'):
                body = request.body
                if body:
                    return json.loads(body)
        except Exception:
            pass
        return {}
    
    def process_response(self, request, response):
        """Log the request/response after processing"""
        if not self.should_log(request):
            return response
        
        try:
            action = self.get_action_type(request.method)
            success = 200 <= response.status_code < 400
            
            # Build description
            description = f"{request.method} {request.path}"
            
            # Get request data
            extra_data = {
                'status_code': response.status_code,
                'request_data': self.get_request_body(request),
            }
            
            # Create audit log
            AuditLog.log_action(
                user=request.user,
                action=action,
                description=description,
                request=request,
                success=success,
                error_message='' if success else f'Status code: {response.status_code}',
                extra_data=extra_data
            )
        except Exception as e:
            # Don't let audit logging break the application
            print(f"Audit logging error: {str(e)}")
        
        return response
