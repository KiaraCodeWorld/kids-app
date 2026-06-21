from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    google_avatar_url = models.URLField(blank=True, default='')
    display_name = models.CharField(max_length=80, blank=True, default='')
    grade_level = models.IntegerField(default=4, choices=[(i, f'Grade {i}') for i in range(1, 9)])
    total_stars = models.IntegerField(default=0)
    total_correct = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        if self.google_avatar_url:
            return self.google_avatar_url
        return None

    def get_display_name(self):
        return self.display_name or self.user.first_name or self.user.email.split('@')[0]

    def accuracy(self):
        if self.total_questions == 0:
            return 0
        return round(self.total_correct / self.total_questions * 100)

    def __str__(self):
        return f"Profile({self.user.email})"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


class PlayerProfile(models.Model):
    """A child's Brain Quest progress. Works for both logged-in users and
    anonymous players (keyed by session). Persisted in the DB so streaks/XP
    survive session expiry."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='player')
    session_key = models.CharField(max_length=64, blank=True, default='', db_index=True)

    # Mascot
    mascot_name = models.CharField(max_length=40, blank=True, default='Foxy')
    mascot_species = models.CharField(max_length=20, blank=True, default='fox')

    grade_level = models.IntegerField(default=4)

    # Progression
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

    # Streaks
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_mission_date = models.DateField(null=True, blank=True)

    # Totals
    total_missions = models.IntegerField(default=0)
    total_correct = models.IntegerField(default=0)
    total_items = models.IntegerField(default=0)

    # Adaptive data & history
    subject_stats = models.JSONField(default=dict, blank=True)   # {subject: {correct, total}}
    seen_items = models.JSONField(default=dict, blank=True)      # {uid: 'YYYY-MM-DD'}
    badges = models.JSONField(default=list, blank=True)          # [badge_key, ...]

    # Accessibility & comfort settings
    reduce_motion = models.BooleanField(default=False)
    large_text = models.BooleanField(default=False)
    high_contrast = models.BooleanField(default=False)
    dyslexia_font = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        who = self.user.email if self.user else f"anon:{self.session_key[:8]}"
        return f"Player({who}, L{self.level}, {self.xp}xp)"

    def accuracy(self):
        if self.total_items == 0:
            return 0
        return round(self.total_correct / self.total_items * 100)

    def weak_subject(self, default='math'):
        """Subject with the lowest accuracy (min 2 attempts), else default."""
        best = None
        for subj, st in (self.subject_stats or {}).items():
            if subj not in ('math', 'vocabulary', 'words', 'spelling'):
                continue
            tot = st.get('total', 0)
            if tot < 2:
                continue
            acc = st.get('correct', 0) / tot
            if best is None or acc < best[1]:
                best = (subj, acc)
        return best[0] if best else default

    def strong_subject(self, default='vocabulary'):
        best = None
        for subj, st in (self.subject_stats or {}).items():
            if subj not in ('math', 'vocabulary', 'words', 'spelling'):
                continue
            tot = st.get('total', 0)
            if tot < 2:
                continue
            acc = st.get('correct', 0) / tot
            if best is None or acc > best[1]:
                best = (subj, acc)
        return best[0] if best else default

    def recent_seen_uids(self, days=14):
        """uids seen within the last N days (for no-repeat rule)."""
        from datetime import date, timedelta
        cutoff = date.today() - timedelta(days=days)
        out = []
        for uid, d in (self.seen_items or {}).items():
            try:
                if date.fromisoformat(d) >= cutoff:
                    out.append(uid)
            except (ValueError, TypeError):
                continue
        return out


class MissionRecord(models.Model):
    """One completed (or in-progress) Daily Mission."""
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, related_name='missions')
    mission_date = models.DateField()
    items_json = models.JSONField(default=list, blank=True)
    is_recovery = models.BooleanField(default=False)
    score = models.IntegerField(default=0)      # correct gradeable items
    total = models.IntegerField(default=0)      # gradeable items
    xp_earned = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-mission_date', '-created_at']

    def __str__(self):
        return f"Mission({self.player_id}, {self.mission_date}, {self.score}/{self.total})"


class SavedFlashcard(models.Model):
    CARD_TYPES = [('word', 'Word'), ('idiom', 'Idiom')]
    card_type = models.CharField(max_length=10, choices=CARD_TYPES, default='word')
    front_text = models.CharField(max_length=200)
    back_text = models.TextField()
    example = models.TextField(blank=True, default='')
    emoji = models.CharField(max_length=10, blank=True, default='')
    extra_json = models.JSONField(default=dict, blank=True)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-saved_at']
        unique_together = [('card_type', 'front_text')]

    def __str__(self):
        return f"{self.card_type}: {self.front_text}"


class SavedVocabularyWord(models.Model):
    """Store user's saved vocabulary words"""
    word = models.CharField(max_length=100, unique=True)
    definition = models.TextField()
    usage = models.TextField()
    level = models.CharField(max_length=20)
    saved_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.word} ({self.level})"
