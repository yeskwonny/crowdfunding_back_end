
from django.shortcuts import render
# APIView class-based view that helps handle API requests,
#such as GET, POST, PUT, DELETE. It provides a basic structure for API views.
from rest_framework.views import APIView
# Response: used to return API responses in JSON or other formats
from rest_framework.response import Response
# status status.HTTP_200_OK or status.HTTP_404_NOT_FOUND 
from rest_framework import status,permissions
from .permissions import IsOwnerOrAdminReadOnly,IsSupporterOrAdminReadOnly
from django.db.models import Sum

from django.http import Http404
from .models import Project, Pledge
from .serializers import ProjectSerializer, PledgeSerializer,ProjectDetailSerializer,PledgeDetailSerializer

class ProjectList(APIView):
    #readonly for unauthentication user, allow to post for authenticated user
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
    # get parameter 
        order = request.GET.get("order")
        status = request.GET.get("status")
        genre = request.GET.get("genre") 
    
    # bring all project
        projects = Project.objects.all()
        if order is not None:
            projects = projects.order_by('-' + order)
        
        # only is_open
        if status is not None:
            projects = projects.filter(is_open=True)
        
        # filter by genre
        if genre is not None:
            projects = projects.filter(genres__icontains=genre)
        
        serializer = ProjectSerializer(projects, many=True)
        serialized_data = serializer.data  # serializer.data는 리스트 형태
        
        # add pledge_total 
        for project_data, project_obj in zip(serialized_data, projects):
            project_data["pledge_total"] = project_obj.pledge_total
        
       
        return Response(serialized_data)

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
       
        # print(pledge_total)
        return Response(serializer.data)
    


    def put(self, request, pk):
        project = self.get_object(pk)
        print(request.data)
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
        # getting data from request dict
        project_id=request.data["project"]
        pledge_owner=request.user.id
        pledge_amount = request.data.get("amount")
        
 
        # checking the project is not null
 
        try:
            # bring the project object with id
            checking_project = Project.objects.get(id=project_id)
            project_owner=checking_project.owner.id
           # check if the project.ownwer == pledge.owner
            if(pledge_owner==project_owner):
               return Response(
                {"error": "Sorry, You can not make a pledge for yourself."}, 
                status=status.HTTP_400_BAD_REQUEST
                )
            
        except Project.DoesNotExist:
            return Response(
            {"error": "Project not found."},
            status=status.HTTP_404_NOT_FOUND
        )
            
        # checking the project is open or not 
        if not checking_project.is_open:
            return Response(
            {"error": "This project is not open for pledges."},
            status=status.HTTP_400_BAD_REQUEST
        )
      
        # checking pledge with goal /pledge total
        total_pledge=checking_project.pledge_total
        project_goal=checking_project.goal
        remaining_goal = checking_project.goal - total_pledge

        if total_pledge >= project_goal:
            return Response(
            {"error": "This project has already reached its funding goal."},
            status=status.HTTP_400_BAD_REQUEST
        )

        if pledge_amount > remaining_goal:
            return Response(
                {"error": f"You can only pledge up to ${remaining_goal} to reach the project goal."},
                status=status.HTTP_400_BAD_REQUEST
            )

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
        