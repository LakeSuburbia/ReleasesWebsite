from . import views
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'releases', views.ReleaseViewSet)
router.register(r'scores', views.ScoreViewSet)

urlpatterns = [
    path("", views.index, name="index"),
    path("restapi/", include(router.urls)),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('add_release', views.add_release,name="add_release"),
    path('releases/<int:releaseid>', views.release_view, name="release"),
    path('edit_release/<int:releaseid>', views.edit_release, name="edit_release"),
    path('delete_vote/<int:releaseid>', views.delete_vote, name="delete_vote"),
    path('profile/<username>', views.profile_view, name="profile"),
]
