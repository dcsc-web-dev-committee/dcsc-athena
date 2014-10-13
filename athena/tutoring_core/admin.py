from django.contrib import admin

from tutoring_core import models

# Register your models here.
admin.site.register(models.Tutor)
admin.site.register(models.Course)
admin.site.register(models.WeeklyTimeSlot)

admin.site.register(models.ActiveTerm)