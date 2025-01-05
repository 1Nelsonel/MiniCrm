from rest_framework import serializers
from .models import Lead, Contact, Note, Reminder

from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.authtoken.models import Token


class UserLoginSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password"]


class UserRegisterSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name",
                "last_name", "email", "password", "password2"]
        extra_kwargs = {
            'password': {"write_only": True}
        }

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            detail = {
                "detail": "User Already exist!"
            }
            raise ValidationError(detail=detail)
        return username

    def validate(self, instance):
        if instance['password'] != instance['password2']:
            raise ValidationError({"message": "Both password must match"})

        if User.objects.filter(email=instance['email']).exists():
            raise ValidationError({"message": "Email already taken!"})

        return instance

    def create(self, validated_data):
        passowrd = validated_data.pop('password')
        passowrd2 = validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        user.set_password(passowrd)
        user.save()
        Token.objects.create(user=user)
        return user

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'

class ContactleadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ('id', 'name')

class ContactSerializer(serializers.ModelSerializer):
    lead = ContactleadSerializer(read_only=True)
    lead_id = serializers.PrimaryKeyRelatedField(
        queryset=Lead.objects.all(), write_only=True, source='lead'
    )

    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'phone', 'lead', 'lead_id']

class ConstactLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['id', 'name']

class NoteSerializer(serializers.ModelSerializer):
    lead = ConstactLeadSerializer(read_only=True)
    lead_id = serializers.PrimaryKeyRelatedField(
        queryset=Lead.objects.all(), write_only=True, source='lead'
    )
    class Meta:
        model = Note
        fields = ['id', 'content', 'created_at', 'lead', 'lead_id']

class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'
