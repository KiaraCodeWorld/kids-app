from allauth.socialaccount.signals import social_account_updated, social_account_added
from django.dispatch import receiver


def _sync_google_avatar(sociallogin):
    extra = sociallogin.account.extra_data
    picture = extra.get('picture', '')
    if picture and hasattr(sociallogin.user, 'profile'):
        profile = sociallogin.user.profile
        if not profile.avatar:  # don't overwrite a custom upload
            profile.google_avatar_url = picture
        if not profile.display_name:
            profile.display_name = extra.get('name', '')
        profile.save()


@receiver(social_account_added)
def on_social_account_added(sender, request, sociallogin, **kwargs):
    _sync_google_avatar(sociallogin)


@receiver(social_account_updated)
def on_social_account_updated(sender, request, sociallogin, **kwargs):
    _sync_google_avatar(sociallogin)
