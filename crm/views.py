from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Lead, Contact, Note, Reminder
from .serializers import LeadSerializer, ContactSerializer, NoteSerializer, ReminderSerializer

from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

# Create your views here.
from rest_framework.permissions import IsAuthenticated

# serilaizer
from .serializers import UserRegisterSerializer
from .serializers import UserLoginSerializer


class UserLoginAPIView(APIView):
    def post(self, request, *args, **kargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            response = {
                "username": {
                    "detail": "User Doesnot exist!"
                }
            }
            if User.objects.filter(username=request.data['username']).exists():
                user = User.objects.get(username=request.data['username'])
                token, created = Token.objects.get_or_create(user=user)
                response = {
                    'success': True,
                    'username': user.username,
                    'email': user.email,
                    'token': token.key
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterAPIView(APIView):
    def post(self, request, *args, **kargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'success': True,
                'user': serializer.data,
                'token': Token.objects.get(user=User.objects.get(username=serializer.data['username'])).key
            }
            return Response(response, status=status.HTTP_200_OK)
        raise ValidationError(
            serializer.errors, code=status.HTTP_406_NOT_ACCEPTABLE)


class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({"success": True, "detail": "Logged out!"}, status=status.HTTP_200_OK)

class LeadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            lead = get_object_or_404(Lead, pk=pk)
            serializer = LeadSerializer(lead)
        else:
            leads = Lead.objects.all()
            serializer = LeadSerializer(leads, many=True)
        return Response({
            'message': 'Lead(s) retrieved successfully',
            'data': serializer.data
        })

    def post(self, request):
        serializer = LeadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Lead created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Lead creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        lead = get_object_or_404(Lead, pk=pk)
        serializer = LeadSerializer(lead, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Lead updated successfully',
                'data': serializer.data
            })
        return Response({
            'message': 'Lead update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        lead = get_object_or_404(Lead, pk=pk)
        lead.delete()
        return Response({
            'message': 'Lead deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

class ContactAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            contact = get_object_or_404(Contact, pk=pk)
            serializer = ContactSerializer(contact)
        else:
            contacts = Contact.objects.all()
            serializer = ContactSerializer(contacts, many=True)
        return Response({
            'message': 'Contact(s) retrieved successfully',
            'data': serializer.data
        })

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Contact created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Contact creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        contact = get_object_or_404(Contact, pk=pk)
        serializer = ContactSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Contact updated successfully',
                'data': serializer.data
            })
        return Response({
            'message': 'Contact update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contact = get_object_or_404(Contact, pk=pk)
        contact.delete()
        return Response({
            'message': 'Contact deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

class NoteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            note = get_object_or_404(Note, pk=pk)
            serializer = NoteSerializer(note)
        else:
            notes = Note.objects.all().select_related('lead')
            serializer = NoteSerializer(notes, many=True)
        return Response({
            'message': 'Note(s) retrieved successfully',
            'data': serializer.data
        })

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Note created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Note creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        note = get_object_or_404(Note, pk=pk)
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Note updated successfully',
                'data': serializer.data
            })
        return Response({
            'message': 'Note update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        note = get_object_or_404(Note, pk=pk)
        note.delete()
        return Response({
            'message': 'Note deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

class ReminderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk=None):
        if pk:
            reminder = get_object_or_404(Reminder, pk=pk)
            serializer = ReminderSerializer(reminder)
        else:
            reminders = Reminder.objects.all().select_related('lead')
            serializer = ReminderSerializer(reminders, many=True)
        return Response({
            'message': 'Reminder(s) retrieved successfully',
            'data': serializer.data
        })

    def post(self, request):
        serializer = ReminderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Reminder created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Reminder creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        reminder = get_object_or_404(Reminder, pk=pk)
        serializer = ReminderSerializer(reminder, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Reminder updated successfully',
                'data': serializer.data
            })
        return Response({
            'message': 'Reminder update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reminder = get_object_or_404(Reminder, pk=pk)
        reminder.delete()
        return Response({
            'message': 'Reminder deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
