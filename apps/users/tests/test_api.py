import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.mark.django_db
class TestUserAPI:
    def setup_method(self):
        self.user_data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "testuser@example.com",
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_registration(self, client):
        url = reverse("register")
        response = client.post(
            url,
            {
                "username": "newuser",
                "password": "newpassword",
                "email": "newuser@example.com",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username="newuser").exists()

    def test_user_registration_duplicate(self, client):
        url = reverse("register")
        response = client.post(url, self.user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_obtain_token(self, client):
        url = reverse("token_obtain_pair")
        response = client.post(
            url,
            {"username": self.user.username, "password": self.user_data["password"]},
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_refresh_token(self, client):
        url = reverse("token_refresh")
        refresh = RefreshToken.for_user(self.user)
        response = client.post(url, {"refresh": str(refresh)})
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_verify_token(self, client):
        url = reverse("token_verify")
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        response = client.post(url, {"token": access_token})
        assert response.status_code == status.HTTP_200_OK

    def test_get_current_user(self, client):
        url = reverse("me")
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == self.user.username

    def test_list_users_admin(self, client):
        url = reverse("list")
        admin_user = User.objects.create_superuser(
            username="admin", password="adminpassword", email="admin@example.com"
        )
        refresh = RefreshToken.for_user(admin_user)
        access_token = str(refresh.access_token)
        client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)


@pytest.mark.django_db
class TestTaskAPI:
    def setup_method(self):
        self.user_data = {
            "username": "taskuser",
            "password": "taskpassword",
            "email": "taskuser@example.com",
        }
        self.user = User.objects.create_user(**self.user_data)
        self.task_data = {
            "title": "Sample Task",
            "description": "Task description",
            "due_date": "2024-12-31",
        }
        self.task = self.user.tasks.create(**self.task_data)

    def test_create_task(self, client):
        url = reverse("task-list-create")
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
        response = client.post(
            url,
            {
                "title": "New Task",
                "description": "New task description",
                "due_date": "2024-12-31",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.data

    def test_list_tasks(self, client):
        url = reverse("task-list-create")
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_update_task(self, client):
        url = reverse("task-detail", kwargs={"pk": self.task.id})
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
        response = client.put(
            url,
            {
                "title": "Updated Task",
                "description": "Updated description",
                "due_date": "2024-12-31",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Updated Task"

    def test_delete_task(self, client):
        url = reverse("task-detail", kwargs={"pk": self.task.id})
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not hasattr(self.user.tasks.filter(id=self.task.id))
