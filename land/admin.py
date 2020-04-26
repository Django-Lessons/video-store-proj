from django.contrib import admin
from land.models import (
    Video,
    User,
    StripeCustomer,
    StripeSubscription
)


class AdminVideo(admin.ModelAdmin):
    pass


class AdminUser(admin.ModelAdmin):
    pass


class AdminStripeCustomer(admin.ModelAdmin):
    pass


class AdminStripeSubscription(admin.ModelAdmin):
    pass


admin.site.register(Video, AdminVideo)
admin.site.register(User, AdminUser)
admin.site.register(StripeCustomer, AdminStripeCustomer)
admin.site.register(StripeSubscription, AdminStripeSubscription)
