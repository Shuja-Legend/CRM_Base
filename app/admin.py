from django.contrib import admin
from .models import *

# Register your models here.

# Registering the UserProfile model with the admin site
# This allows the UserProfile model to be managed through the Django admin interface
class UserProfileAdmin(admin.ModelAdmin):
    # The list_display attribute specifies the fields to be displayed in the list view of the admin site
    # In this case, the 'id' and 'user' fields will be displayed
    list_display = ('id', 'user')

# Register the UserProfile model with the UserProfileAdmin options
admin.site.register(UserProfile, UserProfileAdmin)

# Registering the Lead model with the admin site
class LeadAdmin(admin.ModelAdmin):
    # The list_display attribute specifies the fields to be displayed in the list view of the admin site
    # In this case, the 'name', 'email', 'phone', and 'created_at' fields will be displayed
    list_display = ('name', 'email', 'phone', 'created_at')

# Register the Lead model with the LeadAdmin options
admin.site.register(Lead, LeadAdmin)
