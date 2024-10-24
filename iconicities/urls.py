from django.urls import path, include
from rest_framework import routers
from .views import index, FormViewSet, StimulusViewSet

router = routers.DefaultRouter()
router.register(r'stimuli', StimulusViewSet)
router.register(r'forms', FormViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('api/', include(router.urls)),
]