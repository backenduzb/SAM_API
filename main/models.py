from django.db import models


class TeacherTopic(models.Model):

    topic_name = models.CharField(max_length=255)

    def __str__(self):
        return self.topic_name
    class Meta:
        verbose_name = "Konfedra"
        verbose_name_plural = "Konfedralar"

class TeacherUsersStats(models.Model):
    full_name = models.CharField(max_length=100)

    juda_ham_qoniqaman = models.IntegerField(default=0)
    ortacha_qoniqaman = models.IntegerField(default=0)
    asosan_qoniqaman = models.IntegerField(default=0)
    qoniqmayman = models.IntegerField(default=0)
    umuman_qoniqaman = models.IntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey(TeacherTopic, on_delete=models.CASCADE, null=True, blank=True)
    telegram_id = models.CharField(max_length=20,default="0")

    def __str__(self):
        return f"{self.full_name}"
    class Meta:
        verbose_name = "O'qituvchining statistikasi"
        verbose_name_plural = "O'qituvchilarnining statistikasi"
        ordering = ['-updated_at']