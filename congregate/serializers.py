from django.db.models import Sum
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import CongregateUser, Group, Event, Activity, Vote


class VoteSerializer(ModelSerializer):
    activity = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = Vote
        fields = (
            'id',
            'voter',
            'activity',
            'vote',
        )


class ActivitySerializer(ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field='username', read_only=True)
    total_votes = SerializerMethodField('get_total_votes')

    def get_total_votes(self, obj):
        return obj.votes.aggregate(total_votes=Sum('vote'))['total_votes']

    class Meta:
        model = Activity
        fields = (
            'id',
            'title',
            'event',
            'creator',
            'description',
            'start_time',
            'end_time',
            'total_votes',
        )


class EventSerializer(ModelSerializer):
    group = serializers.SlugRelatedField(slug_field='title', read_only=True)
    activity_list = ActivitySerializer(many=True, source='activities', read_only=True)

    class Meta:
        model = Event
        fields = (
            'id',
            'title',
            'voting',
            'date',
            'activity_list',
            'group',
            'vote_closing_time',
            'decided',
        )


class DecidedEventSerializer(ModelSerializer):
    group = serializers.SlugRelatedField(slug_field='title', read_only=True)
    activity_list = SerializerMethodField('get_activity_list')

    def get_activity_list(self, obj):
        activities = obj.activities.all().order_by('-votes')
        serializer = ActivitySerializer(activities, many=True)
        return serializer.data

    class Meta:
        model = Event
        fields = (
            'id',
            'title',
            'voting',
            'date',
            'activity_list',
            'group',
            'vote_closing_time',
            'decided',
        )


class GroupSerializer(ModelSerializer):
    members = serializers.SlugRelatedField(slug_field='username', many=True, read_only=True)
    admin = serializers.SlugRelatedField(slug_field='username', read_only=True)
    event_list = EventSerializer(many=True, source='events', read_only=True)

    class Meta:
        model = Group
        fields = (
            'id',
            'title',
            'members',
            'admin',
            'event_list',
        )


class CongregateUserSerializer(ModelSerializer):
    group_list = GroupSerializer(many=True, source='user_groups', read_only=True)

    class Meta:
        model = CongregateUser
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'avatar',
            'group_list',
        )
