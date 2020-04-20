from django.contrib import admin
from land.models import (Video, User)


class AdminVideo(admin.ModelAdmin):
    pass


class AdminUser(admin.ModelAdmin):
    pass


admin.site.register(Video, AdminVideo)
admin.site.register(User, AdminUser)
