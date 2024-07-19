from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserRegistrationView, CustomTokenObtainPairView,PDFUploadView, PDFListView,PatientCreateView, PatientListView, LinkPatientView, DoctorPatientsListView

urlpatterns = [
    # urls for registration and token creation
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    #pdf upload
    path('api/pdf/upload/', PDFUploadView.as_view(), name='pdf-upload'),
    path('api/pdf/list/', PDFListView.as_view(), name='pdf-list'),
    
    # urls for patient creation and patient linking 
    path('api/patients/create/', PatientCreateView.as_view(), name='patient-create'),
    path('api/patients/list/', PatientListView.as_view(), name='patient-list'),
    path('api/patients/link/', LinkPatientView.as_view(), name='patient-link'),
    path('api/doctor/patients/', DoctorPatientsListView.as_view(), name='doctor-patients-list'),
]
