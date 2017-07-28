from django.contrib import admin
# from .models import SocialAccount, Session, Feedback

from apps.messenger.models import MessengerSession, MessengerInfo , Question, Answer , Intent

@admin.register(MessengerSession)
class MessengerSession(admin.ModelAdmin):
	list_display = ['id', 'user', 'token','psid', 'page_id', 'expiration']

	class Meta:
		models = MessengerSession

@admin.register(MessengerInfo)
class MessengerInfo(admin.ModelAdmin):
	list_display = ['user', 'messenger_id','first_name', 'last_name', 'profile_pic', 'locale', 'timezone', 'gender']

	class Meta:
		models = MessengerInfo


@admin.register(Question)
class Question(admin.ModelAdmin):
	list_display = ['question']

	class Meta:
		models = Question


@admin.register(Answer)
class Answer(admin.ModelAdmin):
	list_display = ['answer']

	class Meta:
		models = Answer


@admin.register(Intent)
class Intent(admin.ModelAdmin):
	filter_horizontal = ['question','answer']
	
	class Meta:
		models = Intent