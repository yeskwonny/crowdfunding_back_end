
from django.shortcuts import render
# APIView class-based view that helps handle API requests,
#such as GET, POST, PUT, DELETE. It provides a basic structure for API views.
from rest_framework.views import APIView
# Response: used to return API responses in JSON or other formats
from rest_framework.response import Response
# status status.HTTP_200_OK or status.HTTP_404_NOT_FOUND 
from rest_framework import status,permissions
from .permissions import IsOwnerOrAdminReadOnly,IsSupporterOrAdminReadOnly


from django.http import Http404
from .models import Project, Pledge
from .serializers import ProjectSerializer, PledgeSerializer,ProjectDetailSerializer,PledgeDetailSerializer

class ProjectList(APIView):
    #readonly for unauthentication user, allow to post for authenticated user
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
    #    bring all project data
        projects = Project.objects.all()
    #  make the data into json
        serializer = ProjectSerializer(projects, many=True)
    # send the response to client 
        return Response(serializer.data)
    
    def post(self,request):
        serializer=ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)   
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
                
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class ProjectDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrAdminReadOnly
]

    # what does this do? why do we need this?
    # return the error first when the object doesnt exist?
    def get_object(self,pk):
        try:
            project=Project.objects.get(pk=pk)
            self.check_object_permissions(self.request,project)
            return project
        except Project.DoesNotExist:
            raise Http404
        
    def get(self,request,pk):
        # find the project with the pk    
        project=self.get_object(pk) 
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)
    

    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(
            instance=project,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self,request,pk):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
      


class PledgeList(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAdminUser()] 
        return [permissions.IsAuthenticatedOrReadOnly()] 
    
    def get(self, request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(supporter=request.user)
            return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
    )

# pledgeDetail
class PledgeDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsSupporterOrAdminReadOnly
    ] 

    def get_object(self,pk):
        try:
            pledge=Pledge.objects.get(pk=pk)
            self.check_object_permissions(self.request,pledge)
            return pledge
        except Pledge.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        pledge = self.get_object(pk)
        serializer = PledgeDetailSerializer(
            instance=pledge,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )   
      
    def get(self,request,pk): 
        pledge=self.get_object(pk)
        serializer = PledgeSerializer(pledge)
        return Response(serializer.data)
    
    def delete(self,request,pk):
        pledge = self.get_object(pk)
        pledge.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        