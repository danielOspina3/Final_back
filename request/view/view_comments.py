from ..models import Comments
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..serializer.comments_Serializer import CommentsSerializer
from rest_framework import status
import logging;

logger = logging.getLogger(__name__)

@api_view(['GET'])
def getComments(request):
    try:
        listComments = Comments.objects.all().order_by('id')
        serializer = CommentsSerializer(listComments, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error("Error al obtener los Comentarios: " + str(e))
        return Response({"error": "Error al obtener los comentarios"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def createComments(request):
    try:
        serializer = CommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error("Error al crear EPS: " + str(e))
        return Response({"error": "Error al crear EPS"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def updateComment(request, pk):
    try:
        comment = Comments.objects.get(id=pk)
        print(comment)
    except Comments.DoesNotExist:
        return Response({"error": "comment not found."}, status=status.HTTP_404_NOT_FOUND)

    # Copy request data to avoid modifying the original data directly
    request_data = request.data.copy()
    
    # Check if the password is being updated and hash it
    
    serializer = CommentsSerializer(instance=comment, data=request_data)
    print(request_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    