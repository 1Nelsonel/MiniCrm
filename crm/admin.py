from django.contrib import admin

# Register your models here.

from .models import Lead, Contact, Note, Reminder

admin.site.register(Lead)
admin.site.register(Contact)
admin.site.register(Note)
admin.site.register(Reminder)
# Compare this snippet from MiniCrm/crm/admin.py:
# from django.contrib import admin