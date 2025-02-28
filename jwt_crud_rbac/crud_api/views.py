from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import User, Book
from .serializers import UserSerializer, BookSerializer, RegisterSerializer
from .permissions import IsAdmin, IsUser
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all users (Admin only).",
        responses={
            200: UserSerializer(many=True),
            403: "Forbidden - Admins only"
        }
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsAdmin])
    def admin_only(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Get all users with 'user' role.",
        responses={
            200: UserSerializer(many=True),
            403: "Forbidden - Only authenticated users can access"
        }
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsUser])
    def user_only(self, request):
        users = User.objects.filter(role='user')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Book.objects.none()
        return Book.objects.all() if user.role == 'admin' else Book.objects.filter(author=user)

    @swagger_auto_schema(
        operation_description="Get all books (admin only).",
        responses={
            200: BookSerializer(many=True),
            403: "Forbidden - Admins only"
        }
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsAdmin])
    def admin_books(self, request):
        books = self.get_queryset()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Get books for the authenticated user.",
        responses={
            200: BookSerializer(many=True),
            404: "No books found for this user"
        }
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsUser])
    def user_books(self, request):
        books = Book.objects.filter(author=request.user)
        if not books.exists():
            return Response({'message': 'No books found for this user'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


@swagger_auto_schema(
    method='post',
    operation_description="Register a new user.",
    request_body=RegisterSerializer,
    responses={
        201: openapi.Response(
            description="User registered successfully",
            examples={
                "application/json": {
                    "message": "User registered successfully!",
                    "user": {
                        "id": 1,
                        "username": "testuser",
                        "email": "test@example.com",
                        "role": "user"
                    }
                }
            },
        ),
        400: openapi.Response(
            description="Bad request",
            examples={
                "application/json": {"error": "Invalid data provided"}
            },
        ),
    }
)
@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'User registered successfully!',
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@swagger_auto_schema(
    method='post',
    operation_description="Logout a user by blacklisting the refresh token.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description="Refresh token"),
        },
        required=['refresh_token'],
    ),
    responses={
        205: openapi.Response(
            description="Logout successful",
            examples={
                "application/json": {"message": "Logout successful!"}
            },
        ),
        400: openapi.Response(
            description="Bad request",
            examples={
                "application/json": {"message": "No refresh token provided!"}
            },
        ),
    }
)
@api_view(['POST'])
def logout_user(request):
    refresh_token = request.data.get('refresh_token')
    
    if not refresh_token:
        return Response({'message': 'No refresh token provided!'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Logout successful!'}, status=status.HTTP_205_RESET_CONTENT)
    
    except Exception as e:
        return Response({'message': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    operation_description="Login a user and return access & refresh tokens.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description="Username"),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description="Password"),
        },
        required=['username', 'password'],
    ),
    responses={
        200: openapi.Response(
            description="Login successful",
            examples={
                "application/json": {
                    "message": "Login successful!",
                    "access_token": "your_jwt_access_token",
                    "refresh_token": "your_jwt_refresh_token"
                }
            },
        ),
        400: openapi.Response(description="Bad request"),
        401: openapi.Response(description="Invalid credentials"),
    }
)
@api_view(['POST'])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login successful!",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)