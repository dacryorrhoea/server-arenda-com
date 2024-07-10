from rest_framework import routers
from .views import AdsView

router = routers.DefaultRouter()
router.register(r'ads', AdsView)

urlpatterns = router.urls