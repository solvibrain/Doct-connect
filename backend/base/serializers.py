from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import PDF,Patient, DoctorPatient

User = get_user_model()
# Serializer for Creating User
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'name', 'specialty', 'password', 'password2')
        extra_kwargs = {
            'name': {'required': True},
            'specialty': {'required': True},
            'email' :{'required' :True}
        }
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
            specialty=validated_data['specialty']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# Token creation for user
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['name'] = user.name
        token['specialty'] = user.specialty
        return token



# Pdf Serializer
class PDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDF
        fields = ['id', 'file', 'upload_date', 'title']
        read_only_fields = ['upload_date']


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'name', 'email', 'date_of_birth']

class DoctorPatientSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    patient_email = serializers.EmailField(source='patient.email', read_only=True)

    class Meta:
        model = DoctorPatient
        fields = ['id', 'patient', 'patient_name', 'patient_email', 'date_assigned']
        read_only_fields = ['date_assigned']
