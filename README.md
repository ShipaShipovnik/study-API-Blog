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

| GET http://127.0.0.1:8000/users   | ![[Pasted image 20240908225659.png]] |
| --------------------------------- | ------------------------------------ |
| GET http://127.0.0.1:8000/users/1 | ![[Pasted image 20240908225853.png]] |
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

| http://127.0.0.1:8000/posts   | ![[Pasted image 20240908230014.png]] |
| ----------------------------- | ------------------------------------ |
| http://127.0.0.1:8000/posts/6 | ![[Pasted image 20240908230038.png]] |

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

| http://127.0.0.1:8000/comments/  | ![[Pasted image 20240908230244.png]] |
| -------------------------------- | ------------------------------------ |
| http://127.0.0.1:8000/comments/5 | ![[Pasted image 20240908230303.png]] |
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

| http://127.0.0.1:8000/categories/  | ![[Pasted image 20240908230409.png]] |
| ---------------------------------- | ------------------------------------ |
| http://127.0.0.1:8000/categories/2 | ![[Pasted image 20240908230356.png]] |
# СХЕМА БАЗЫ ДАННЫХ
![[Pasted image 20240908230625.png]]