# permissions input
from rest_framework import permissions




# permission clases
class AdminOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        

class AdminOrBuildeOwnerPermission(permissions.BasePermission):
    message = None    
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_builder:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):

        if hasattr(obj, 'builder') :
            if obj.builder == request.user or request.user.is_superuser == True:
                return True
            
        elif hasattr(obj, 'house'): 
            if obj.house.builder == request.user or request.user.is_superuser == True:
                return True
        
        elif request.user.is_superuser:
            return True
        else:
            self.message = 'Недостатньо прав: тільки забудовник\
                            або адміністратор має доступ.'
            return False


        
class SimpleOnlyOwnerPermission(permissions.BasePermission):
    message = None
    def has_object_permission(self, request, view, obj):
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
    

class SimpleUserOnlyListAndRetreiveAdminAllPermission(permissions.BasePermission):
    message = None
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve', 'create'] and request.user.is_authenticated:
            response = True
        elif view.action in ['list', 'retrieve', 'create'] and not request.user.is_authenticated == False:
            self.message = 'Для отримання відомостей про номатріуса, потрібно увійти в систему'
            response = False
        elif view.action in ['update', 'partial_update', 'destroy'] and request.user.is_superuser == True:
            response = True
        elif view.action in ['update', 'partial_update', 'destroy'] and request.user.is_superuser == False:
            self.message = 'Для зміни відомостей про номатріуса, потрібно мати право адміністратора.'
            response = False
        else:
            self.message = 'Технічна проблема з доступ. Зв`яжіться з адміністрацією.'
            response = False
        return response