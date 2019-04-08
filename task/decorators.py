from rest_framework.response import Response
from rest_framework.views import status

def validate_create_data(fn):
    def decorated(*args, **kwargs):
        title = args[0].request.data.get("title", "")
        if not title :
            return Response(
                data={
                    "message": "'title' are required to add a task"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated

def validate_update_data(fn):
    def decorated(*args, **kwargs):
        title = args[0].request.data.get("title", "")
        completed = args[0].request.data.get("completed", None)
        if not title and completed is None:
            return Response(
                data={
                    "message": "'title' or 'completed' are required to add a task"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        elif not completed is None:
            if not completed in ['True', 'False']:
                return Response(
                data={
                    "message": "'completed' only accept 'True' or 'False'"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return fn(*args, **kwargs)
    return decorated