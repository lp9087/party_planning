from django.urls import include, path
from rest_framework import routers

from count.views import ListOfPartiesViewSet, MembersViewSet, PurchaseAPIView, CountExpenses

router = routers.DefaultRouter()
router.register(r'party', ListOfPartiesViewSet)
router.register(r'members', MembersViewSet)
#router.register(r'purchase/<int:party_id>', PurchaseViewSet, basename='purchase')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/purchase/<int:party_id>/', PurchaseAPIView.as_view()),
    path('api/count_exp/<int:id>/', CountExpenses.as_view()),
]

