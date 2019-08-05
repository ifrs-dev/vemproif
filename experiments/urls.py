from django.contrib.auth.decorators import login_required
from django.urls import path

from experiments import views

urlpatterns = [
    path('trabalho/<int:pk>/', views.ExperimentDetailView.as_view(), name='experiment-detail'),
    path('trabalho/novo/', login_required(views.ExperimentCreateView.as_view()), name='experiment-create'),
]
