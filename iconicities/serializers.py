from rest_framework import serializers
from .models import Stimulus, Form, Reply

class StimulusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stimulus
        fields = ['term', 'file_name']

class FormSerializer(serializers.ModelSerializer):
    guid = serializers.CharField(validators=[])

    class Meta:
        model = Form
        abstract = True
        fields = [
            'guid', 
            'test_mode',
            'browser',
            'operating_system',
            'is_mobile',
            'sex', 
            'birthdate', 
            'education',
            'preferred_language',
            'lsu_fluency'
        ]

class ReplySerializer(serializers.ModelSerializer):
    stimulus = serializers.SlugRelatedField(slug_field='file_name', queryset=Stimulus.objects.all())

    class Meta:
        model = Reply
        fields = ['stimulus', 'iconicity', 'rt', 'te']

class FormAndRepliesSerializer(FormSerializer):
    replies = ReplySerializer(many=True)

    class Meta(FormSerializer.Meta):
        fields = FormSerializer.Meta.fields + ['replies']
    
    def create(self, validated_data):
        replies_data = validated_data.pop('replies')
        form, created = Form.objects.update_or_create(**validated_data)
        for reply_data in replies_data:
            Reply.objects.update_or_create(form=form, **reply_data)
        return form
