from django.contrib import admin
from land.models import Video


class AdminVideo(admin.ModelAdmin):
    pass


admin.site.register(Video, AdminVideo)
