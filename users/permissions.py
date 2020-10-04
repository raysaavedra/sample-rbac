from rest_framework.permissions import BasePermission


class SuperUserOrStaffOnly(BasePermission):
    
    def has_permission(self, request, view):
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        return False
