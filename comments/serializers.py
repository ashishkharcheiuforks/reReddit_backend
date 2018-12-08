from rest_framework import serializers
from collections import defaultdict

from .models import Comment
from redditors.models import User
from posts.models import Post

class CommentSerializer(serializers.ModelSerializer):
    
    post = serializers.SlugRelatedField(
        slug_field='title',
        read_only=True
    )
    poster = serializers.SlugRelatedField(
        slug_field='username',
        queryset = User.objects.all()
    )
    parent = serializers.PrimaryKeyRelatedField(
        read_only=True,
        allow_null=True
    )
    parent_fn = serializers.CharField(
        write_only=True
    )
    
    class Meta:
        model = Comment
        fields = (
            'post', 'poster', 'parent', 'body', 'upvotes', 'parent_fn', 'pk',
        )
        
    # def validate(self, data):
    #     """
    #     The parent and the child (self) need to be made on the same post
    #     """
    #     parent = data['parent']
    #     if parent and not data['post'] == data['parent'].post:
    #         raise serializers.ValidationError("The parent comment must be " +
    #             "made on the same post."
    #         )
    #     return data
    
    def validate_parent_fn(self, value):
        """
        the parent_id must begin with 'tx_' where x is either
        1 or 2 to indicate that the comment was made on another
        comment or a post, respectively. Follows the idea from
        the reddit api.
        """
        # TODO get a regex
        if not (value.startswith("t") and value[2] == "_"):
            raise serializers.ValidationError("parent_fn must be a 'full name' "
                "and begin with either t1_ or t2_")
        return value
    
    def create(self, validated_data):
        
        parent_fn = validated_data.pop('parent_fn')
        parent_pk = parent_fn[3:]
        print("\nout: {}, [1]: {}\n".format(parent_fn, parent_fn[1]))
        
        if int(parent_fn[1]) == 1:
            validated_data['parent'] = Comment.objects.get(pk=parent_pk)
        elif int(parent_fn[1]) == 2:
            validated_data['post'] = Post.objects.get(pk=parent_pk)
        
        return super().create(validated_data)
    
class CommentTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields= ('poster', 'post', 'body', 'upvotes', 'parent', 'pk', 'children',)
    
    def get_children(self, obj):
        children = self.context['children'].get(obj.pk, [])
        serializer = self.__class__(
            children,
            context=self.context,
            many=True,
        )
        return serializer.data
        
        
