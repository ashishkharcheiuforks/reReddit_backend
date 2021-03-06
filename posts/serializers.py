from rest_framework import serializers
from django.utils.timezone import now
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils.translation import gettext as _

from .models import Post
from redditors.models import User
from subs.models import Sub
from votes.models import PostVote

class PostSerializer(serializers.ModelSerializer):
    
    poster = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    
    subreddit = serializers.PrimaryKeyRelatedField(
        queryset=Sub.objects.all(),
    )
    
    subreddit_title = serializers.SerializerMethodField()
    poster_username = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()
    vote_state = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ('pk', 'created', 'updated', 'title', 'body',
                  'upvotes', 'subreddit', 'poster', 'subreddit_title',
                  'poster_username', 'vote_state')
                
    def validate(self, data):
        """
        Ensure that the user is a member of the subreddit
        being posted to
        """
        poster = data.get("poster")
        subreddit = data.get("subreddit")
        
        # Only relevant when doing a creation, not an update
        if poster and subreddit:
            # make sure they aren't trying to create a post to a pseudo subreddit
            if subreddit.title.lower() in Sub.pseudo_subreddits.keys():
                message = _(
                    ("You can't create a post to the "
                    "'{}' subreddit.".format(subreddit.title))
                )
                raise serializers.ValidationError(message)
            if not subreddit in poster.subs.all():
                message = _("You must be a member of the subreddit to post here.")
                raise serializers.ValidationError(message)
    
        return data
    
    def get_subreddit_title(self, obj):
        return obj.subreddit.title
    
    def get_poster_username(self, obj):
        return obj.poster.username

    def get_created(self, obj):
        return naturaltime(obj.created)

    def get_updated(self, obj):
        return naturaltime(obj.updated)

    def get_vote_state(self, obj):
        """
        If a user is authenticated, look up whether they have voted on this post
        before.
        """
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            try:
                vote = obj.votes.all().get(user_id=request.user.pk)
                return vote.vote_type
            except PostVote.DoesNotExist:
                pass
        return 0
        
