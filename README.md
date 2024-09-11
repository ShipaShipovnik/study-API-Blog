***Серилизаторы** преобразовывают данные в формат json.*
Серилизаторы находятся в файле serializers.py.

**Представления** были написаны с помощью generics классов. *В Django REST Framework (DRF), **generics классы** — это предопределенные классы-представления (views), которые предоставляют базовую функциональность для обработки общих операций CRUD (Create, Retrieve, Update, Delete). Они упрощают создание API, предоставляя готовые реализации для этих операций, чтобы не писать много повторяющегося кода.* Находятся в файле views.py

Права доступа находятся в файле permissions.py.
```python
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
serializers.py :
```python
  class UserSerializer(serializers.ModelSerializer):
      posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
      comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
      categories = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
  
      class Meta:
          model = User
          fields = ['id', 'username', 'posts', 'comments','categories']
```

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
serializers.py :
```python
class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'owner', 'comments', 'categories']
```
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
serializers.py :
```python
class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = ['id', 'body', 'owner', 'post']
```
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
serializers.py :
```python
class CategorySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'owner', 'posts']
```
# РАБОТА С POSTMAN и ЗАПРОСАМИ
## POST
Добавление категории http://127.0.0.1:8000/categories/
Тело:
```json
    {
        "name": "ИИ Рразработка"
    }
```
![image](https://github.com/user-attachments/assets/df41fa5a-49e6-4a17-b51b-df5702721ec5)

## GET
Все посты. http://127.0.0.1:8000/posts
![image](https://github.com/user-attachments/assets/f3661807-a133-417a-8ef9-bc461aed0858)

## PUT
Поменять заголовок поста http://127.0.0.1:8000/posts/3
![image](https://github.com/user-attachments/assets/d6953a2b-0a46-431f-a614-e9c24c7bbe98)

## DELETE
Удалить комментарий http://127.0.0.1:8000/comments/4
![image](https://github.com/user-attachments/assets/5b65e6db-482f-4e1e-beed-695e2a0724ac)

# СХЕМА БАЗЫ ДАННЫХ
![image](https://github.com/user-attachments/assets/7e52e71a-cdaf-4167-9a01-8eeaf49806e4)
