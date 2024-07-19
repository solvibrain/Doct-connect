from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer,PatientSerializer, DoctorPatientSerializer
from .models import PDF,Patient, DoctorPatient
from django.contrib.auth import get_user_model


User = get_user_model()

# Doctor Account Creation
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "message": "Doctor account created successfully",
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Token Creation
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer  

# PDF upload
class PDFUploadView(generics.CreateAPIView):
    queryset = PDF.objects.all()
    serializer_class = PDFSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "message": "PDF uploaded successfully",
                "pdf": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


# View for handling request to list out PDF's of Doctor
class PDFListView(generics.ListAPIView):
    serializer_class = PDFSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PDF.objects.filter(doctor=self.request.user)    
    

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "message": "PDFs retrieved successfully",
            "pdfs": serializer.data
        }, status=status.HTTP_200_OK)




class PatientCreateView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "message": "Patient profile created successfully",
                "patient": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientListView(generics.ListAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(doctors=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "message": "Patients retrieved successfully",
            "patients": serializer.data
        }, status=status.HTTP_200_OK)

class LinkPatientView(generics.CreateAPIView):
    queryset = DoctorPatient.objects.all()
    serializer_class = DoctorPatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "message": "Patient linked to doctor successfully",
                "doctor_patient": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorPatientsListView(generics.ListAPIView):
    serializer_class = DoctorPatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoctorPatient.objects.filter(doctor=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "message": "Doctor's patients retrieved successfully",
            "doctor_patients": serializer.data
        }, status=status.HTTP_200_OK)



