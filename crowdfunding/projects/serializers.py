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
    supporter = serializers.ReadOnlyField(source='supporter.id')
    class Meta:
        model=apps.get_model('projects.Pledge')
        fields = '__all__'


class PledgeDetailSerializer(PledgeSerializer):
    
    projects=ProjectSerializer(many=True, read_only=True)
    def update(self, instance, validated_data):
        instance.amount = validated_data.get('amount', instance.amount)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.anonymous = validated_data.get('anonymous', instance.anonymous)
        instance.project = validated_data.get('project', instance.project)
        instance.supporter = validated_data.get('supporter', instance.supporter)
        instance.save()
        return instance


# Add pledge in the prject model
class ProjectDetailSerializer(ProjectSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.movie_synopsis= validated_data.get('movie_synopsis', instance.movie_synopsis)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.genres=validated_data.get('genres',instance.genres)
        instance.image = validated_data.get('image', instance.image)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.goal_deadline = validated_data.get('goal_deadline', instance.goal_deadline)
        instance.date_created = validated_data.get('date_created', instance.date_created)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        return instance
