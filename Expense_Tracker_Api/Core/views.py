from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .utility import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ObjectDoesNotExist

# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method='post',
    operation_description="Register a new user.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING)
        }
    ),
    responses={200: "User registered", 400: "User already exists or validation failed"}
)
@api_view(['POST'])
def register(request):
    request_data = request.data
    username = request_data.get('username', None)
    password = request_data.get('password', None)
    result = validate_password(password)
    if result is not True:
        return Response({'message': result, "status": status.HTTP_201_CREATED})
    else:
        result = User.objects.filter(username=username).exists()
        if result is False:
            user_data = {
                "username": username,
                "password": password
            }
            user_data = User.objects.create_user(**user_data)
            return Response({
                "message": "usercreated sucessfully",
                "is_admin": user_data.is_superuser,
                "status": status.HTTP_200_OK
            })
        else:
            return Response({
                "message": "Invalid username or Username already exists in the system",
                "status": status.HTTP_400_BAD_REQUEST,
                "data": result
            })


@swagger_auto_schema(
    method='post',
    operation_description="Login user and return JWT tokens.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING)
        }
    ),
    responses={200: "Login successful", 401: "Invalid credentials"}
)
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    return Response({"error": "Invalid credentials", "data": user}, status=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(
    method='post',
    operation_description="Create a new expense record.",
    request_body=ExpenseSerilizer,
    responses={201: ExpenseSerilizer, 400: "Creation failed"}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_expense(request):
    Expense_data = request.data
    ins = ExpenseSerilizer(data=Expense_data, context={'request': request})
    if ins.is_valid():
        ins.save()
        return Response({
            'mesage': 'Creation sucess',
            'data': ins.data,
            'status': status.HTTP_201_CREATED
        })
    return Response({
        'mesage': 'Creation Failed',
        'status': status.HTTP_400_BAD_REQUEST,
        'error': ins.errors
    })


@swagger_auto_schema(
    method='patch',
    operation_description="Update an existing expense by ID.",
    request_body=ExpenseSerilizer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="Expense ID", type=openapi.TYPE_INTEGER)
    ],
    responses={201: ExpenseSerilizer, 400: "Validation failed"}
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_expense(request, id):
    model_data = ExpenseIncome.objects.get(id=id)
    request_data = request.data
    instance = ExpenseSerilizer(model_data, data=request_data, partial=True)
    if instance.is_valid():
        instance.save()
        return Response({
            'Message': 'Updated Sucesfully',
            'status': status.HTTP_201_CREATED,
            'data': instance.data
        })
    return Response({
        'message': 'Update operation failed, please try again',
        'status': status.HTTP_400_BAD_REQUEST,
        'error': instance.errors
    })


@swagger_auto_schema(
    method='delete',
    operation_description="Delete an expense by ID.",
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="Expense ID", type=openapi.TYPE_INTEGER)
    ],
    responses={200: "Deleted successfully", 404: "Expense not found"}
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_expense(request, id):
    instance = ExpenseIncome.objects.get(id=id)
    instance.delete()
    return Response({
        'message': f'expense of id {id} deleted successfully',
        'status': status.HTTP_200_OK
    })


@swagger_auto_schema(
    method='get',
    operation_description="Get all expenses for the current user. Superuser sees all records.",
    responses={200: ExpenseSerilizer(many=True)}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_expenses(request):
    paginator = PageNumberPagination()
    currentuser = request.user
    if currentuser.is_superuser:
        instances = ExpenseIncome.objects.all()
    else:
        instances = ExpenseIncome.objects.filter(user=currentuser)

    paginator.page_size = 10
    paginator.max_page_size = 100
    queryset = paginator.paginate_queryset(instances, request)
    serializer = ExpenseSerilizer(queryset, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(
    method='get',
    operation_description="Get a specific expense by ID.",
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="Expense ID", type=openapi.TYPE_INTEGER)
    ],
    responses={200: ExpenseSerilizer, 404: "Not found"}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_expense_byID(request, id):
    try:
        instance = ExpenseIncome.objects.get(id=id)
        serializer = ExpenseSerilizer(instance)
        return Response(serializer.data)
    except ObjectDoesNotExist:
        return Response({
            'message': f'expense of id {id} not found',
            'status': status.HTTP_404_NOT_FOUND
        })
