# permissions input
from rest_framework import permissions




# permission clases
class AdminOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        
        
class SimpleOnlyOwnerPermission(permissions.BasePermission):
    message = None
    def has_object_permission(self, request, view, obj):
        # if obj.id == request.user.id:
        if obj == request.user and obj.is_activated == True:
            response = True
        elif obj == request.user and obj.is_activated == False:
            self.message = 'Цей особистий кабінет заблоковано'
            response = False
        elif obj == None:
            self.message = 'Такого особистого кабінету не зареєстровано'
            response = False
        elif obj != request.user:
            self.message = 'Тільки власник особистого кабінету має доступ до цієї сторінки'
            response = False
        return response