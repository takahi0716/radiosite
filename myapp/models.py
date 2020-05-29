from django.conf import settings
from django.db import models
from django.utils import timezone

# ログイン・サインアップ
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.validators import UnicodeUsernameValidator

class Program(models.Model):

    title = models.CharField(
        verbose_name='番組名',
        max_length=200
    )

    corner_title = models.CharField(
        verbose_name='コーナー名',
        max_length=200,
        blank=True,
        null=True,
    )

    address = models.EmailField(
        verbose_name='メールアドレス',
        blank=True,
        null=True,
    )

    url = models.URLField(
        verbose_name='公式Webページ',
        blank=True,
        null=True,
    )

    genrelist = models.ManyToManyField(
        'myapp.Genre',
        verbose_name='ジャンル',
        blank=True,
        related_name='genres',
    )

    created_date = models.DateTimeField(
        verbose_name='作成時間',
        blank=True,
        null=True,
        default=timezone.now,
    )

    published_date = models.DateTimeField(
        verbose_name='更新時間',
        blank=True,
        null=True,
        default=timezone.now,
    )
    
    okini_num = models.IntegerField(
      verbose_name='お気に入り',
      default=0
    )

    

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def station_names(self):
        return self.stations.all()

    def dj_names(self):
        return self.djs.all()

    def listener_name(self):
        return self.listener_names.all()

    def okini_program(self):
        return self.okini_program

# 各ラジオ局のオンエア時間
class Station(models.Model):

    program = models.ForeignKey(
      'myapp.Program',
      on_delete=models.CASCADE,
      related_name='stations',
    )

    station_choice = (
        (0, '指定なし'),
        (1, 'TBSラジオ'),
        (2, 'ニッポン放送'),
        (3, '文化放送'),
        (4, 'NHK'),
    )

    station_name = models.IntegerField(
        verbose_name='ラジオ局',
        choices=station_choice,
    )

    day_of_the_week = models.ManyToManyField(
        'myapp.Week',
        verbose_name='曜日',
        blank=True,
        related_name='day_of_the_weeks',
    )

    start_time = models.TimeField (
        verbose_name='開始時間',
        blank=True,
        null=True,
    )

    end_time = models.TimeField (
        verbose_name='終了時間',
        blank=True,
        null=True,
    )


# 曜日
class Week(models.Model):

    week_choice = (
        (1, '月'),
        (2, '火'),
        (3, '水'),
        (4, '木'),
        (5, '金'),
        (6, '土'),
        (7, '日'),
    )

    weeks = models.IntegerField(
        verbose_name='曜日',
        choices=week_choice,
        null=True,
        unique=True,
    )

    def __str__(self):
        return self.get_weeks_display()


# 出演者
class Dj(models.Model):

    program = models.ForeignKey(
      'myapp.Program',
      on_delete=models.CASCADE,
      related_name='djs',
    )

    dj_name = models.CharField(
        verbose_name='出演者',
        max_length=100
    )

    main_dj = models.BooleanField(
        verbose_name='メインパーソナリティ',
    )

    def __str__(self):
        return self.dj_name


# はがき職人
class Listener(models.Model):

    program = models.ForeignKey(
      'myapp.Program',
      on_delete=models.CASCADE,
      related_name='listeners',
    )

    listener_name = models.CharField(
        verbose_name='主なハガキ職人',
        max_length=100
    )

    def __str__(self):
        return self.listener_name

# ジャンル
class Genre(models.Model):

    genre_choice = (
        ('var', 'バラエティ'),
        ('mus', '音楽'),
        ('news', 'ニュース'),
        ('edu', '教育'),
        ('info', '情報'),
        ('hob', '趣味'),
    )

    genre_name = models.CharField(
        verbose_name='ジャンル',
        choices=genre_choice,
        null=True,
        unique=True,
        max_length=4,
    )

    def __str__(self):
        return self.get_genre_name_display()

# お気に入り
class Okini(models.Model):

    user = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE,
      related_name='okini_user',
      default='',
    )

    program = models.ForeignKey(
      Program,
      on_delete=models.CASCADE,
      related_name='okini_program',
      default='',
    )

    date_created = models.DateTimeField(
      auto_now_add=True
    )

    def __str__(self):
        return self.program

# コメント
class Comment(models.Model):

    program = models.ForeignKey(
      'myapp.Program', 
      on_delete=models.CASCADE, 
      related_name='comments'
    )

    author = models.CharField(
      max_length=200
    )
    text = models.TextField()
    created_date = models.DateTimeField(
      default=timezone.now
    )
    # 承認されたコメント
    approved_comment = models.BooleanField(
      default=False
    )

    like_user = models.ManyToManyField(
      settings.AUTH_USER_MODEL,
      blank=True,
      related_name="like_users"
    )

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    def like_comment(self):
        return self.like_comment

# 運営からのお知らせ
class Info(models.Model):

    title = models.CharField(
        verbose_name='題名',
        max_length=200
    )

    text = models.TextField(
        verbose_name='お知らせ内容',
        blank=True,
        null=True,
    )
    created_date = models.DateTimeField(
      default=timezone.now
    )

class UserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        # unique=True,
        help_text=_('この項目は必須です!半角アルファベット、半角数字、@/./+/-/_ で150文字以下にしてください。'),
        validators=[username_validator],
        # error_messages={
        #     'unique': _("A user with that username already exists."),
        # },
    )
    profile = models.TextField(
        verbose_name='紹介文',
        blank=True,
        null=True,
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    # USERNAME_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)