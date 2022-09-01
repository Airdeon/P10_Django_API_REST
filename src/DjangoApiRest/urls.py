"""DjangoApiRest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from API.views import ProjectsViewSet, IssuesViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from Accounts.views import Signup, UserViewSet
from rest_framework_nested import routers

# API URL
router = routers.SimpleRouter()

# router.register("signup", ViewSetSignup, basename="signup")
router.register(r"projects", ProjectsViewSet, basename="projects")

users_router = routers.NestedSimpleRouter(router, r"projects", lookup="projects")
users_router.register(r"users", UserViewSet, basename="project-users")

issues_router = routers.NestedSimpleRouter(router, r"projects", lookup="projects")
issues_router.register(r"issues", IssuesViewSet, basename="project-issues")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(r"", include(router.urls)),
    path(r"", include(users_router.urls)),
    path(r"", include(issues_router.urls)),
    path("signup/", Signup.as_view(), name="signup"),
]
