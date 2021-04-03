from . import views
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'releases', views.ReleaseViewSet)

urlpatterns = [
    path("", views.index, name="index"),
    path("restapi/", include(router.urls)),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('add_release', views.add_release,name="add_release"),
    path('releases', views.releases_view,name="releases"),
    path('releases/<int:releaseid>', views.release_view, name="release"),
    path('edit_release/<int:releaseid>', views.edit_release, name="edit_release")
]
