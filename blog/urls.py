
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static


from apps.home.views import HomeView
urlpatterns = [
   	url(r'^$', HomeView.as_view()),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



