from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from api.models import Todo
from api.serializers import TodoSerializer

# Create your views here.

class TodoView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        try:
            todos = Todo.objects.all().order_by('-id')
            serialized_todos = TodoSerializer(todos, many=True)
            return Response({
                "todos" : serialized_todos.data,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error" : "Something went wrong"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        title = request.data.get('title')
        text = request.data.get('text')
        try:
            todo = Todo.objects.create(title=title,
                text=text)
            serialized_todo = TodoSerializer(todo, many=False)
            return Response({
                "todo" : serialized_todo.data, 
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error" : "Something went wrong"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        id = request.GET.get('id')
        title = request.data.get('title')
        text = request.data.get('text')
        try:
            todo = Todo.objects.get(id=id)
            todo.title = title
            todo.text = text
            todo.save()
            serialized_todo = TodoSerializer(todo, many=False)
            return Response({
                "todo" : serialized_todo.data,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({
                "Error" : "ToDo doesn't exists with given Id."
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        id = request.GET.get('id')
        try:
            todo = Todo.objects.get(id=id)
            todo.delete()
            return Response({
                "Success" : "OK"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "Error" : "ToDo doesn't exists with given Id."
            }, status=status.HTTP_400_BAD_REQUEST)


class TodoExtraView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        id = request.GET.get('id')
        try:
            todo = Todo.objects.get(id=id)
            todo.completed = not todo.completed
            todo.save()
            serialized_todo = TodoSerializer(todo, many=False)
            return Response({
                "todo" : serialized_todo.data,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            # print(e)
            return Response({
                "Error" : "ToDo doesn't exists with given Id."
            }, status=status.HTTP_400_BAD_REQUEST)