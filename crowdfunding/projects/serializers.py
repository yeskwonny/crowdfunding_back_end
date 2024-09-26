from rest_framework import serializers
from django.apps import apps

class ProjectSerializer(serializers.ModelSerializer):
    # loggin user is owner of this project
    owner = serializers.ReadOnlyField(source='owner.id')
    class Meta:
        model = apps.get_model('projects.Project')
        fields = '__all__'


class PledgeSerializer(serializers.ModelSerializer):
     # loggin user is owner of this pledge
    owner = serializers.ReadOnlyField(source='owner.id')
    class Meta:
        model=apps.get_model('projects.Pledge')
        fields = '__all__'

# Add pledge in the prject model
class ProjectDetailSerializer(ProjectSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)
