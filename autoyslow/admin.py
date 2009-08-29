from autoyslow.models import *
from django.contrib import admin
from django import forms

class PageInline(admin.TabularInline):
    model = Page
    extra = 1

class PageInlineModelForm(forms.ModelForm):
    class Meta:
        model = Page
    
    def clean_last_testrun(self):
        return self.cleaned_data['last_testrun']

class SiteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['base_url', 'last_testrun']}),
    ]
    inlines = [PageInline]
    list_display = ('base_url', 'last_testrun')
    list_per_page = 10
    search_fields = ['base_url']

admin.site.register(Site, SiteAdmin)
admin.site.register(Page)
admin.site.register(Test)
