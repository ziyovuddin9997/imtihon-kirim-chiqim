from rest_framework.permissions import BasePermission
from accounts.models import SELLER, MANAGER, ORDINARY_USER


class IsSellerOrManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticeted and request.user.role in [SELLER, MANAGER]
    
    
class IsOwnerOrManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticeted and request.user.role in [SELLER, MANAGER]
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticeted and (request.user == obj.user or request.user.role == MANAGER)
    
    
class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticeted and request.user.role == MANAGER
    
class IsOrdinaryUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticeted and request.user.role == ORDINARY_USER