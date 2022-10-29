from rest_framework import permissions

#################### custom permissions #############################
class AdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        
        if request.method in permissions.SAFE_METHODS:
        # Check permissions for read-only request
            return True # if mehtod is Get allow only reading
        else:
            # Check permissions for write request
           return bool(request.user and request.user.is_staff) # mehtod is writing, chek if is admin or not

class ReviewUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
        # Check permissions for read-only request
            return True
        else:
            # Check permissions for write request

            return obj.review_user == request.user or request.user.is_staff