Представления были написаны с помощью generics классов. *В Django REST Framework (DRF), **generics классы** — это предопределенные классы-представления (views), которые предоставляют базовую функциональность для обработки общих операций CRUD (Create, Retrieve, Update, Delete). Они упрощают создание API, предоставляя готовые реализации для этих операций, чтобы не писать много повторяющегося кода.* Находятся в файле views.py

Права доступа находятся в файле permissions.py.
```python permissions.py
from rest_framework import permissions

class IsOwnerReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
```

В основном используются данные разрешения:
- `IsAuthenticatedOrReadOnly`, что означает:
    - **Чтение**: Доступно всем пользователям.
    - **Запись**: Доступно только аутентифицированным пользователям.
- **`IsOwnerReadOnly`**: Пользователь может обновлять или удалять объект только в том случае, если он является владельцем поста.
# Пользователь. User.
views.py :
```python
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
```

| GET http://127.0.0.1:8000/users   | ![image](https://github.com/user-attachments/assets/9b567676-68a5-4c89-a25f-56345ec1d315) |
| --------------------------------- | ------------------------------------ |
| GET http://127.0.0.1:8000/users/1 | ![image](https://github.com/user-attachments/assets/6ed2ec0a-4723-4272-9aed-41a67230a9c4)|
# Пост. Post
views.py :
```python
class PostList(generics.ListAPIView):  
    queryset = Post.objects.all()  
    serializer_class = serializers.PostSerializer  
    permission_classes = permissions.IsAuthenticatedOrReadOnly  
    
    def perform_create(self, serializer):  
        serializer.save(owner=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerReadOnly]
```

| http://127.0.0.1:8000/posts   | ![image](https://github.com/user-attachments/assets/ca2617fe-65d4-4cd0-b6b6-b38c6d7d2ab0) |
| ----------------------------- | ------------------------------------ |
| http://127.0.0.1:8000/posts/6 | ![image](https://github.com/user-attachments/assets/093c9b03-0e39-47b6-bdbd-f518316783e0) |

# Комментарий. Comment 
views.py :
```python
class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerReadOnly]
```

| http://127.0.0.1:8000/comments/  | ![image](https://github.com/user-attachments/assets/0159fa80-ad95-407e-82fd-bcd6f844566f) |
| -------------------------------- | ------------------------------------ |
| http://127.0.0.1:8000/comments/5 | ![image](https://github.com/user-attachments/assets/e96457d4-1707-4b6c-bb51-d4ba6856900f) |
# Категория. Category.
views.py :
```python
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class =  serializers.CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner='self.request.user')

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerReadOnly]
```

| http://127.0.0.1:8000/categories/  | ![image](https://github.com/user-attachments/assets/df7c10cf-d5a0-4692-bd8f-29a120820cf1) |
| ---------------------------------- | ------------------------------------ |
| http://127.0.0.1:8000/categories/2 | ![image](https://github.com/user-attachments/assets/3cbeaf56-f1d9-49eb-a607-b62e67ee4fcd) |
# СХЕМА БАЗЫ ДАННЫХ
![image](https://github.com/user-attachments/assets/7e52e71a-cdaf-4167-9a01-8eeaf49806e4)
