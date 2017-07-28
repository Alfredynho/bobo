# -*- encoding:utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

class MessengerSession(models.Model):

    info = models.ForeignKey(
        'MessengerInfo',
        verbose_name=_('Información del usuario'),
        related_name='messenger_session',
        db_index=True,
    )

    token = models.CharField(
        verbose_name=_('Token'),
        max_length=255,
        blank=True,
        null=True,
        db_index=True,
    )

    psid = models.CharField(
        verbose_name=_('PSID'),
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        db_index = True,
    )

    page_id = models.CharField(
        verbose_name=_('PAGE ID'),
        max_length=255,
        blank=True,
        null=True,
        db_index=True,
    )

    expiration = models.DateTimeField(
        verbose_name=_('Vencimiento'),
        blank=True,
        null=True,
    )

    @property
    def user(self):
        if self.info and self.info.user:
            return self.info.user
        return None

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name=_('Sesion de Messenger')
        verbose_name_plural=_('Sesiones de Messenger')



class MessengerInfo(models.Model):
    user = models.ForeignKey(
        'users.User',
        verbose_name=_("Usuario"),
        related_name='msg_info',
        blank=True,
        null=True,
    )

    messenger_id = models.CharField(
        verbose_name=_('Messenger ID'),
        max_length=255,
        blank=True,
        null=True
    )

    first_name = models.CharField(
        verbose_name=_('Nombre'),
        max_length=150,
        blank=True,
        null=True,        
    )

    last_name = models.CharField(
        verbose_name=_('Apellido'),
        max_length=150,
        blank=True,
        null=True,
    )

    profile_pic = models.CharField(
        verbose_name=_('Foto de Perfil'),
        max_length=500,
        blank=True,
        null=True,        
    )

    locale = models.CharField(
        verbose_name=_('Lugar'),
        max_length=150,
        blank=True,
        null=True,        
    )

    timezone = models.CharField(
        verbose_name=_('Zona Horaria'),
        max_length=150,
        blank=True,
        null=True,        
    )

    gender = models.CharField(
        verbose_name=_('Género'),
        max_length=150,
        blank=True,
        null=True,        
    )


    def __str__(self):
        return self.first_name
        
    class Meta:
        verbose_name=_('Usuario')
        verbose_name_plural=_('Usuarios')


class Question(models.Model):
    question = models.TextField(
        verbose_name=_('Pregunta'),
    )

    def __str__(self):
        return self.question

    class Meta:
        verbose_name=_('Pregunta')
        verbose_name_plural=_('Preguntas')


class Answer(models.Model):
    answer = models.TextField(
        verbose_name=_('Repuesta'),
    )

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name=_('Respuesta')
        verbose_name_plural=_('Respuestas')


class Intent(models.Model):
    question = models.ManyToManyField(
        'messenger.Question',
    )

    answer = models.ManyToManyField(
        'messenger.Answer',
    )

    def __str__(self):
        return "%s - %s" % (self.question, self.answer)