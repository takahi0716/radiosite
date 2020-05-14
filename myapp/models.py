from django.conf import settings
from django.db import models
from django.utils import timezone

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
    approved_comment = models.BooleanField(
      default=False
    )

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

