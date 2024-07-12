from rest_framework.views import APIView
from rest_framework.response import Response    
from rest_framework.exceptions import AuthenticationFailed
from users.serializers import UserSerializer
from users.models import User
import jwt, datetime
from main.models import ActivityPlan
from course_plan.models import CoursePlan

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        course_plan = CoursePlan.objects.create(user=user)
        activity_plan = ActivityPlan.objects.create(user=user, course_plan=course_plan)
        activity_plan.save()
        
        return Response(serializer.data)
    
    
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user =  User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.now(datetime.UTC)
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')    

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'jwt': token}

        return response

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated")
        
        try: 
            payload = jwt.decode(token, 'secret', algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        user = User.objects.filter(id=payload['id']).first()

        serializer = UserSerializer(user)

        return Response(serializer.data)
    
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Logout Success'
        }
        return response