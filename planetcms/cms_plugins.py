from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from planetcms.models import PostsForFeed


class PostsForFeedPlugin(CMSPluginBase):

    model = PostsForFeed
    name = _("Posts for RSS Feed")
    render_template = "planetcms/postsforfeed.html"

    def render(self, context, instance, placeholder):
        context.update({
            'feed': instance.feed,
            'limit': instance.limit,
            'placeholder': placeholder,
        })
        return context


plugin_pool.register_plugin(PostsForFeedPlugin)
