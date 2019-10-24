from django.contrib import admin
import general.models
import jsonfield
import django_json_widget.widgets
# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    formfield_overrides = {
        jsonfield.JSONField: {
            'widget': django_json_widget.widgets.JSONEditorWidget
        }
    }

class StoreAdmin(admin.ModelAdmin):
    formfield_overrides = {
        jsonfield.JSONField: {
            'widget': django_json_widget.widgets.JSONEditorWidget
        }
    }

admin.site.register(general.models.Vendor, VendorAdmin)
admin.site.register(general.models.Store, StoreAdmin)