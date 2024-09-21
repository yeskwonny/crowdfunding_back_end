
from django.shortcuts import render
# APIView class-based view that helps handle API requests,
#such as GET, POST, PUT, DELETE. It provides a basic structure for API views.
from rest_framework.views import APIView
# Response: used to return API responses in JSON or other formats
from rest_framework.response import Response
# status status.HTTP_200_OK or status.HTTP_404_NOT_FOUND 
from rest_framework import status
from django.http import Http404
from .models import Project, Pledge
from .serializers import ProjectSerializer, PledgeSerializer,ProjectDetailSerializer

class ProjectList(APIView):

    def get(self, request):
    #    bring all project data
        projects = Project.objects.all()
    #  make the data into json
        serializer = ProjectSerializer(projects, many=True)
    # send the response to client 
        return Response(serializer.data)
    
    # TODO: how can i print request and others?? 
    # TODO: if Response make the data into JSON, what does serializer do? into python dictionary?
    # TODO: where i can see the Response(status)? When i have ui i can show the error? 
    # TODO:what is difference Response/ HTTP404 When it gives error

    def post(self,request):
        serializer=ProjectSerializer(data=request.data)
        # print("Request Data:", request.data, flush=True)
        if serializer.is_valid():
            # save in the db
            serializer.save()    
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
                
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class ProjectDetail(APIView):
    # if there is data =pk, return project 
    def get_object(self,pk):
        try:
            project=Project.objects.get(pk=pk)
            return project
        except Project.DoesNotExist:
            raise Http404
    
    def get(self,request,pk):
        # find the project with the pk 
        
        project=self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)
    

class PledgeList(APIView):

    def get(self, request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
    )