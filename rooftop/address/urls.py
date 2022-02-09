from rest_framework.routers import DefaultRouter
from .views import ProjectViewset, RoofInfoViewSet, UploadCSV

# Create a router and register our viewsets with it.
router = DefaultRouter()

router.register(r'address', ProjectViewset)
router.register(r'roof-info', RoofInfoViewSet)
router.register(r'upload-csv', UploadCSV)