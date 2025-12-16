"""
Audit log models for EduCore LMS.
Tracks all important system actions for security and compliance.
"""

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from apps.users.models import User


class ActionType(models.TextChoices):
    """Action type choices for audit logging"""
    CREATE = 'CREATE', 'Create'
    READ = 'READ', 'Read'
    UPDATE = 'UPDATE', 'Update'
    DELETE = 'DELETE', 'Delete'
    LOGIN = 'LOGIN', 'Login'
    LOGOUT = 'LOGOUT', 'Logout'
    ACCESS_DENIED = 'ACCESS_DENIED', 'Access Denied'
    GRADE_SUBMITTED = 'GRADE_SUBMITTED', 'Grade Submitted'
    ENROLLMENT = 'ENROLLMENT', 'Enrollment'
    SUBMISSION = 'SUBMISSION', 'Submission'


class AuditLog(models.Model):
    """
    Audit log model for tracking system actions.
    Uses generic foreign keys to reference any model.
    """
    
    # User who performed the action
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs',
        help_text='User who performed the action'
    )
    
    # Action details
    action = models.CharField(
        max_length=20,
        choices=ActionType.choices,
        db_index=True
    )
    description = models.TextField(help_text='Description of the action')
    
    # Generic foreign key to reference any model
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Request metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    request_method = models.CharField(max_length=10, blank=True)
    request_path = models.CharField(max_length=500, blank=True)
    
    # Additional context
    extra_data = models.JSONField(
        default=dict,
        blank=True,
        help_text='Additional context data'
    )
    
    # Success/Failure
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    
    # Timestamp
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        db_table = 'audit_logs'
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'action', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        user_str = self.user.email if self.user else 'Anonymous'
        return f"{user_str} - {self.action} - {self.timestamp}"
    
    @classmethod
    def log_action(cls, user, action, description, content_object=None, 
                   request=None, success=True, error_message='', extra_data=None):
        """
        Helper method to create audit log entries.
        
        Args:
            user: User who performed the action
            action: ActionType choice
            description: Human-readable description
            content_object: Optional related object
            request: Optional Django request object
            success: Whether the action succeeded
            error_message: Optional error message if failed
            extra_data: Optional dict of additional data
        """
        log_data = {
            'user': user,
            'action': action,
            'description': description,
            'success': success,
            'error_message': error_message,
            'extra_data': extra_data or {},
        }
        
        if content_object:
            log_data['content_object'] = content_object
        
        if request:
            # Extract request metadata
            log_data.update({
                'ip_address': cls.get_client_ip(request),
                'user_agent': request.META.get('HTTP_USER_AGENT', '')[:500],
                'request_method': request.method,
                'request_path': request.path[:500],
            })
        
        return cls.objects.create(**log_data)
    
    @staticmethod
    def get_client_ip(request):
        """Extract client IP from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
