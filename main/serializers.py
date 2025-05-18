from .models import TeacherUsersStats, TeacherTopic
from rest_framework import serializers

__all__ = [
    'TeacherUsersStatsSerializer',
    'TeacherEditSerializer',
    'TopicsSerializer',
    'TopicedTeachersSerializer',
    'TeacherTopicSerializer'
]


class TeacherTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherTopic
        fields = ['topic_name']

class TeacherUsersStatsSerializer(serializers.ModelSerializer):
    juda_ham_qoniqaman = serializers.IntegerField(default=0)
    ortacha_qoniqaman = serializers.IntegerField(default=0)
    asosan_qoniqaman = serializers.IntegerField(default=0)
    qoniqmayman = serializers.IntegerField(default=0)
    umuman_qoniqaman = serializers.IntegerField(default=0)

    class Meta:
        model = TeacherUsersStats
        fields = ['juda_ham_qoniqaman', 'ortacha_qoniqaman', 'asosan_qoniqaman', 'qoniqmayman', 'umuman_qoniqaman', 'updated_at', 'topic_name']
    
class TopicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherTopic
        fields = ['topic_name']

class TopicedTeachersSerializer(serializers.ModelSerializer):
    topic = serializers.CharField(source='topic.topic_name')

    class Meta:
        model = TeacherUsersStats
        fields = ["id",'full_name','topic','telegram_id']

class TeacherEditSerializer(serializers.ModelSerializer):
    juda_ham_qoniqaman = serializers.IntegerField(default=0)
    ortacha_qoniqaman = serializers.IntegerField(default=0)
    asosan_qoniqaman = serializers.IntegerField(default=0)
    qoniqmayman = serializers.IntegerField(default=0)
    umuman_qoniqaman = serializers.IntegerField(default=0)
    topic_name = TeacherTopicSerializer(source='topic', read_only=True)
    
    class Meta:
        model = TeacherUsersStats
        fields = ['juda_ham_qoniqaman', 'ortacha_qoniqaman', 'asosan_qoniqaman', 'qoniqmayman', 'umuman_qoniqaman', 'updated_at', 'topic_name']
    def update(self, instance, validated_data):
        instance.juda_ham_qoniqaman = validated_data.get('juda_ham_qoniqaman', instance.juda_ham_qoniqaman)
        instance.ortacha_qoniqaman = validated_data.get('ortacha_qoniqaman', instance.ortacha_qoniqaman)
        instance.asosan_qoniqaman = validated_data.get('asosan_qoniqaman', instance.asosan_qoniqaman)
        instance.qoniqmayman = validated_data.get('qoniqmayman', instance.qoniqmayman)
        instance.umuman_qoniqaman = validated_data.get('umuman_qoniqaman', instance.umuman_qoniqaman)

        instance.save()
        return instance