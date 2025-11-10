from rest_framework import permissions

class CustomReadOnly(permissions.BasePermission):
    # GET: 누구나, PUT/PATCH: 해당 유저

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: # SAFE_METHODS는 데이터에 영향을 미치지 않는 메소드, GET과 같은 메소드를 의미
            return True
        return obj.user == request.user # 요청의 유저와 객체의 유저 비교