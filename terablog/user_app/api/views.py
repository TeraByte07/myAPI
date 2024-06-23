from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from user_app.api.serializers import RegistrationSerializer, AuthorRequestSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from user_app.models import CustomUser
from rest_framework import generics
from terablog.settings import AUTH_USER_MODEL

@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['POST','PUT'])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            
            data['response'] = "Registration successful!"
            data['username'] = account.username
            data['email'] = account.email
            
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
            
        return Response(data)
        
class AuthorApprovalView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_author_requested:
            user.is_author = True
            user.is_author_requested = False
            user.save()
            return Response({'status': 'Author approved'}, status=status.HTTP_200_OK)
        return Response({'status': 'No author request found'}, status=status.HTTP_400_BAD_REQUEST)

class AuthorRequestView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AuthorRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
