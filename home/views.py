# home/views.py
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import MultiPartParser
from .models import Folder
from django.utils import timezone

def home(request):
    return render(request, 'home.html')

def download(request, uid):
    # Mark folder as downloaded and record download time
    folder = get_object_or_404(Folder, uid=uid)
    folder.downloaded = True
    folder.download_time = timezone.now()
    folder.save()
    
    return render(request, 'download.html', context={'uid': uid})

class HandleFileUpload(APIView):
    parser_classes = [MultiPartParser]
    
    def post(self, request):
        try:
            data = request.data
            serializer = FileListSerializer(data=data)
        
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 200,
                    'message': 'files uploaded successfully',
                    'data': serializer.data
                })
            
            return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': serializer.errors
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 500,
                'message': 'Internal server error'
            })