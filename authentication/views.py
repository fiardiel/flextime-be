from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response 
from authentication.serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from course_plan.models import CoursePlan
from main.models import ActivityPlan

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username = request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({"token": token.key, "user": serializer.data})

@api_view(['POST'])
def register(request):
    serializer =  UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username']) 
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)

        course_plan = CoursePlan.objects.create(user=user)
        activity_plan = ActivityPlan.objects.create(course_plan=course_plan, user=user) 
        course_plan.save(), activity_plan.save()

        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout(request):    
    return Response({})

@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response({"message": f"passed for {request.user.email}", "user_id": request.user.id})


# create a view for admins to look at the users and their roles
@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def get_users(request):
    if not request.user.is_staff or not request.user.is_superuser:
        return Response({"detail": "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)