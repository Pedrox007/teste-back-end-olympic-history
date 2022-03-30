from rest_framework.routers import DefaultRouter

from django.urls import include, path

from core import views

router = DefaultRouter()

router.register("athlete", views.AthleteViewSet)
router.register("team", views.TeamViewSet)
router.register("modality", views.ModalityViewSet)
router.register("sport", views.SportViewSet)
router.register("game", views.GameViewSet)

urlpatterns = [path("", include(router.urls))]
