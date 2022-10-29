from rest_framework.decorators import api_view
from user_app.api.serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
# from user_app import models # need this for generate token but I don need it if I use jwt
from rest_framework import status
## jwt ##
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def logout_view(request):

  if request.method =='POST':
    #  request.user.auth_token.delete() this is for token, if I want to log out with JWT I have to delete from localsorage using React
     return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        
        data = {}
        
        if serializer.is_valid(): #I modifie this method from serializer
            account = serializer.save() #acont data comes from serializer return
            data['response'] = 'Registration SUccesfully'
            data['username'] = account.username
            data['email'] = account.email
            # token = Token.objects.get(user=account).key #acces to user's token
            # data['token'] = token
            refresh = RefreshToken.for_user(account) 
            
            
            data['token'] = {
                 'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            # return Response(serializer.data) 
            
        else: 
            data = serializer.errors
            # return Response({'error':'data no valida o usuario ya existe'})
        return Response(data, status=status.HTTP_201_CREATED)
   
