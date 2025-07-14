from rest_framework import serializers
from education.models import ContentNode

class ContentNodeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = ContentNode
        fields = [
            'id', 'title_en', 'title_sw', 'content_en', 'content_sw',
            'node_type', 'parent', 'children'
        ]

    def get_children(self, obj):
        children = obj.children.order_by('created_at')
        return ContentNodeSerializer(children, many=True).data
