from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import PDF, Patient, DoctorPatient
import json

User = get_user_model()

class DoctorAccountTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'testdoctor@example.com',
            'name': 'Test Doctor',
            'specialty': 'Cardiology',
            'password': 'testpass123',
            'password2': 'testpass123'
        }

    def test_create_doctor_account(self):
        response = self.client.post('/api/register/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testdoctor@example.com')

    def test_login(self):
        User.objects.create_user(email='testdoctor@example.com',name= 'Test Doctor', password='testpass123')
        response = self.client.post('/api/token/', {'email': 'testdoctor@example.com', 'password': 'testpass123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

class PDFManagementTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testdoctor@example.com',name= 'Test Doctor', password='testpass123')
        self.client.force_authenticate(user=self.user)

    def test_upload_pdf(self):
        pdf_file = SimpleUploadedFile("file.pdf", b"file_content", content_type="application/pdf")
        response = self.client.post('/api/pdf/upload/', {'file': pdf_file, 'title': 'Test PDF'}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PDF.objects.count(), 1)

    def test_list_pdfs(self):
        PDF.objects.create(doctor=self.user, file='test.pdf', title='Test PDF')
        response = self.client.get('/api/pdf/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['pdfs']), 1)

class PatientManagementTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testdoctor@example.com',name= 'Test Doctor', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.patient_data = {
            'name': 'Test Patient',
            'email': 'testpatient@example.com',
            'date_of_birth': '1990-01-01'
        }

    def test_create_patient(self):
        response = self.client.post('/api/patients/create/', self.patient_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.count(), 1)

    def test_list_patients(self):
        patient = Patient.objects.create(**self.patient_data)
        DoctorPatient.objects.create(doctor=self.user, patient=patient)
        response = self.client.get('/api/patients/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['patients']), 1)

class DoctorPatientLinkingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testdoctor@example.com',name= 'Test Doctor', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.patient = Patient.objects.create(name='Test Patient', email='testpatient@example.com', date_of_birth='1990-01-01')

    def test_link_patient(self):
        response = self.client.post('/api/patients/link/', {'patient': self.patient.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DoctorPatient.objects.count(), 1)

    def test_list_linked_patients(self):
        DoctorPatient.objects.create(doctor=self.user, patient=self.patient)
        response = self.client.get('/api/doctor/patients/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['doctor_patients']), 1)

class AuthenticationRequiredTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_pdf_upload_requires_auth(self):
        response = self.client.post('/api/pdf/upload/', {'file': 'test.pdf', 'title': 'Test PDF'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patient_create_requires_auth(self):
        response = self.client.post('/api/patients/create/', {'name': 'Test Patient', 'email': 'test@example.com', 'date_of_birth': '1990-01-01'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patient_list_requires_auth(self):
        response = self.client.get('/api/patients/list/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patient_link_requires_auth(self):
        response = self.client.post('/api/patients/link/', {'patient': 1})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)