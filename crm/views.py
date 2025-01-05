from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Lead, Contact, Note, Reminder
from .serializers import LeadSerializer, ContactSerializer, NoteSerializer, ReminderSerializer
from rest_framework.exceptions import ValidationError
from knox.models import AuthToken
from .serializers import UserRegisterSerializer
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        try:
            print("POST: login ", request.data)
            serializer = AuthTokenSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data['user']
                login(request, user)
                
                # Get the token and expiry from Knox
                token_instance, token = AuthToken.objects.create(user)
                
                return Response({
                    'status': 'success',
                    'message': 'Successfully logged in',
                    'data': {
                        'token': token,
                        'user': {
                            'id': user.id,
                            'username': user.username,
                            'email': user.email
                        }
                    }
                }, status=status.HTTP_200_OK)
            
            return Response({
                'status': 'error',
                'message': 'Invalid credentials',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'An error occurred during login',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserRegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        print("POST: user registration ", request.data)
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = AuthToken.objects.create(user)[1]
            response = {
                "success": True,
                "user": serializer.data,
                "token": token,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        
        raise ValidationError(serializer.errors, code=status.HTTP_400_BAD_REQUEST)


class LeadAPIView(APIView, PermissionRequiredMixin):

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

class ContactAPIView(APIView, PermissionRequiredMixin):

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

class NoteAPIView(APIView, PermissionRequiredMixin):

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

class ReminderAPIView(APIView, PermissionRequiredMixin):
    
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
