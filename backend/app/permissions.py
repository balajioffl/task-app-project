from rest_framework.permissions import BasePermission

class hasAccess(BasePermission):

    def has_permission(self, request, view):

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        
        if request.user.profile.role and request.user.profile.role.name == "Admin":
            return True
        
        return obj.created_by == request.user