from django.urls import include, path
from rest_framework import routers

from count.views import ListOfPartiesViewSet, MembersViewSet, ExpensesViewSet, CountExpenses

router = routers.DefaultRouter()
router.register(r'party', ListOfPartiesViewSet)
router.register(r'members', MembersViewSet)
router.register(r'expenses', ExpensesViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/count_exp/<int:id>/', CountExpenses.as_view())
]

