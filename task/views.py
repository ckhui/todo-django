from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status

from django_filters import rest_framework as filters

# Create your views here.
from django.http import HttpResponse

from .decorators import validate_update_data, validate_create_data
from .models import Task
from .serializers import TasksSerializer

from django_eventstream import send_event

class MyFilterSet(filters.FilterSet):
    class Meta:
        model = Task
        fields = {'completed': ['isnull'], }

def index(request):

    tasks = Task.objects.all().order_by('-date_created')
    context = {
        'new_title': "What needs to be done?",
        'tasks' : tasks
    }

    return render(request, 'task/todo.html', context)


class ListTodoView(generics.ListAPIView):
    """
    GET task/
    POST task/
    """
    queryset = Task.objects.all() #.order_by('-date_created')
    serializer_class = TasksSerializer

    @validate_create_data
    def post(self, request, *args, **kwargs):
        task = Task.objects.create(
            title=request.data["title"],
        )

        send_event('todo', 'new', task.to_data())
        return Response(
            data=TasksSerializer(task).data,
            status=status.HTTP_201_CREATED
        )

class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET task/:id/
    PUT task/:id/
    DELETE task/:id/
    """
    queryset = Task.objects.all()
    serializer_class = TasksSerializer
    filter_class = MyFilterSet

    def get(self, request, *args, **kwargs):
        try:
            task = self.queryset.get(pk=kwargs["id"])
            return Response(TasksSerializer(task).data)
        except Task.DoesNotExist:
            return Response(
                data={
                    "message": "Task with id: {} does not exist".format(kwargs["id"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_update_data
    def put(self, request, *args, **kwargs):
        try:
            task = self.queryset.get(pk=kwargs["id"])
            serializer = TasksSerializer()
            updated_task = serializer.update(task, request.data)

            send_event('todo', 'edit', updated_task.to_data())
            return Response(TasksSerializer(updated_task).data)
        except Task.DoesNotExist:
            return Response(
                data={
                    "message": "Task with id: {} does not exist".format(kwargs["id"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            task = self.queryset.get(pk=kwargs["id"])
            task.delete()

            send_event('todo', 'delete', task.to_data())
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response(
                data={
                    "message": "Task with id: {} does not exist".format(kwargs["id"])
                },
                status=status.HTTP_404_NOT_FOUND
            )