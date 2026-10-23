import csv
from django.contrib import admin
from django.http import HttpResponse
from .models import Article, CommitteeMember, ContactMessage, Event, EventCategory, EventRegistration, Project, ProjectSubmission

admin.site.site_header='UQOnnect · Administration'
admin.site.site_title='UQOnnect'
admin.site.index_title='Gestion du site'
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display=('title','starts_at','location','published','registration_type'); list_filter=('published','category','registration_type'); search_fields=('title','description'); prepopulated_fields={'slug':('title',)}
@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display=('event','name','email','program','created_at'); list_filter=('event',); search_fields=('name','email')
    actions=['export_csv']
    @admin.action(description='Exporter les inscriptions sélectionnées en CSV')
    def export_csv(self, request, queryset):
        response=HttpResponse(content_type='text/csv; charset=utf-8'); response['Content-Disposition']='attachment; filename="inscriptions-uqonnect.csv"'; response.write('\ufeff')
        writer=csv.writer(response); writer.writerow(['Événement','Nom','Courriel','Programme','Date'])
        for item in queryset.select_related('event'): writer.writerow([item.event.title,item.name,item.email,item.program,item.created_at.isoformat()])
        return response
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display=('title','published_at','published','category'); list_filter=('published','category'); search_fields=('title','summary','content'); prepopulated_fields={'slug':('title',)}
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display=('title','domain','approved','created_at'); list_filter=('approved','domain'); search_fields=('title','description'); prepopulated_fields={'slug':('title',)}
admin.site.register(EventCategory)
admin.site.register(CommitteeMember)
admin.site.register(ContactMessage)
admin.site.register(ProjectSubmission)
