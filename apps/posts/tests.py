from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.posts.models.post import Post

User = get_user_model()


class PostModelTestCase(TestCase):
    """Тесты для модели Post"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )

    def test_post_creation(self):
        """Проверка создания поста"""
        post = Post.objects.create(
            author=self.user,
            title="Test Post",
            body="Test content"
        )
        self.assertEqual(str(post), post.title)
        self.assertIsNotNone(post.created_at)
        self.assertIsNotNone(post.updated_at)

    def test_post_title_max_length(self):
        """Проверка максимального длины заголовка"""
        post = Post(
            author=self.user,
            title="a" * 255,
            body="Test content"
        )
        post.full_clean()
        post.save()
        self.assertEqual(len(post.title), 255)

    def test_post_relationship(self):
        """Проверка связи Post с User"""
        post = Post.objects.create(
            author=self.user,
            title="Test Post",
            body="Test content"
        )
        self.assertEqual(self.user.posts.count(), 1)
        self.assertEqual(self.user.posts.first(), post)


class PostAPITestCase(APITestCase):
    """Тесты для API Post (CRUD операции)"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(user=self.user)
        
        self.post_data = {
            "title": "Test Post",
            "body": "Test content"
        }

    def test_list_posts_unauthenticated(self):
        """Проверка получения списка постов без авторизации"""
        Post.objects.create(
            author=self.user,
            title="Post 1",
            body="Content 1"
        )
        Post.objects.create(
            author=self.user,
            title="Post 2",
            body="Content 2"
        )
        
        response = self.client.get("/api/posts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_post(self):
        """Проверка создания поста (Create)"""
        response = self.authorized_client.post("/api/posts/", self.post_data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().title, "Test Post")
        self.assertEqual(Post.objects.first().author, self.user)

    def test_create_post_unauthenticated(self):
        """Проверка создания поста без авторизации"""
        response = self.client.post("/api/posts/", self.post_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_post(self):
        """Проверка получения поста по ID (Read)"""
        post = Post.objects.create(
            author=self.user,
            title="Test Post",
            body="Test content"
        )
        
        response = self.client.get(f"/api/posts/{post.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Post")

    def test_update_post(self):
        """Проверка обновления поста (Update)"""
        post = Post.objects.create(
            author=self.user,
            title="Old Title",
            body="Old content"
        )
        
        update_data = {
            "title": "Updated Title",
            "body": "Updated content"
        }
        
        response = self.authorized_client.put(f"/api/posts/{post.id}/", update_data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, "Updated Title")
        self.assertEqual(post.body, "Updated content")

    def test_partial_update_post(self):
        """Проверка частичного обновления поста (Partial Update)"""
        post = Post.objects.create(
            author=self.user,
            title="Old Title",
            body="Old content"
        )
        
        update_data = {"title": "New Title"}
        
        response = self.authorized_client.patch(f"/api/posts/{post.id}/", update_data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, "New Title")
        self.assertEqual(post.body, "Old content")

    def test_delete_post(self):
        """Проверка удаления поста (Delete)"""
        post = Post.objects.create(
            author=self.user,
            title="Test Post",
            body="Test content"
        )
        
        response = self.authorized_client.delete(f"/api/posts/{post.id}/")
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_delete_post_unauthenticated(self):
        """Проверка удаления поста без авторизации"""
        post = Post.objects.create(
            author=self.user,
            title="Test Post",
            body="Test content"
        )
        
        response = self.client.delete(f"/api/posts/{post.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_posts_filter_by_author(self):
        """Проверка фильтрации постов по автору"""
        user2 = User.objects.create_user(
            username="user2",
            email="user2@example.com",
            password="testpass123"
        )
        
        Post.objects.create(author=self.user, title="User1 Post", body="Content")
        Post.objects.create(author=user2, title="User2 Post", body="Content")
        
        response = self.client.get("/api/posts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_post_with_invalid_data(self):
        """Проверка создания поста с невалидными данными"""
        invalid_data = {"title": "", "body": ""}
        
        response = self.authorized_client.post("/api/posts/", invalid_data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)
