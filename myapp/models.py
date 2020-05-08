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

    # kyoku_choice = (
    #     (1, 'TBSラジオ'),
    #     (2, 'ニッポン放送'),
    #     (3, '文化放送'),
    #     (4, 'NHK'),
    # )

    # kyoku = models.IntegerField(
    #     verbose_name='ラジオ局',
    #     choices=kyoku_choice,
    #     blank=True,
    #     null=True,
    # )

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


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title