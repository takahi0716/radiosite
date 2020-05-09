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

    created_date = models.DateTimeField(
        verbose_name='作成時間',
        blank=True,
        null=True,
        # editable=False,
        default=timezone.now,
    )

    published_date = models.DateTimeField(
        verbose_name='更新時間',
        blank=True,
        null=True,
        # editable=False,
        default=timezone.now,
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
        # return self.stations.get_station_name_display()

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

    # def __str__(self):
    #     return self.station_name

    # dj = models.CharField(
    #     verbose_name='出演者',
    #     max_length=50
    # )

    # 曜日
    # week_choice = (
    #     (1, '月'),
    #     (2, '火'),
    #     (3, '水'),
    #     (4, '木'),
    #     (5, '金'),
    #     (6, '土'),
    #     (7, '日'),
    # )

    # week = models.MultipleChoiceField(
    #     verbose_name='曜日',
    #     choices=week_choice,
    #     blank=True,
    #     null=True,
    # )

    # start_time = models.TimeField (
    #     verbose_name='開始時間',
    #     blank=True,
    #     null=True,
    # )

    # end_time = models.TimeField (
    #     verbose_name='終了時間',
    #     blank=True,
    #     null=True,
    # )



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

