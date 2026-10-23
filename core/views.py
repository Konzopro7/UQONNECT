from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import ContactForm, EventRegistrationForm, ProjectSubmissionForm
from .models import Article, CommitteeMember, Event, EventCategory, EventRegistration, Project, ProjectSubmission

def home(request):
    now=timezone.now()
    return render(request,'core/home.html',{'events':Event.objects.filter(published=True,starts_at__gte=now)[:3],'articles':Article.objects.filter(published=True,published_at__lte=now)[:3]})
def about(request): return render(request,'core/about.html',{'members':CommitteeMember.objects.filter(active=True)})
def events(request):
    qs=Event.objects.filter(published=True); query=request.GET.get('q','').strip(); category=request.GET.get('categorie',''); tab=request.GET.get('vue','avenir')
    if query: qs=qs.filter(title__icontains=query)
    if category: qs=qs.filter(category__slug=category)
    qs=qs.filter(starts_at__lt=timezone.now()) if tab=='passes' else qs.filter(starts_at__gte=timezone.now())
    return render(request,'core/events.html',{'events':qs,'categories':EventCategory.objects.all(),'query':query,'category':category,'tab':tab})
def event_detail(request,slug):
    event=get_object_or_404(Event,slug=slug,published=True)
    form=EventRegistrationForm(request.POST or None)
    if request.method=='POST' and event.registration_type=='internal' and form.is_valid():
        with transaction.atomic():
            locked=Event.objects.select_for_update().get(pk=event.pk)
            registrations=EventRegistration.objects.filter(event=locked)
            if registrations.filter(email__iexact=form.cleaned_data['email']).exists():
                form.add_error('email','Cette adresse est déjà inscrite à cet événement.')
            elif locked.capacity and registrations.count() >= locked.capacity:
                form.add_error(None,'Les places pour cet événement sont comblées.')
            else:
                registration=form.save(commit=False); registration.event=locked; registration.save()
                messages.success(request,'Votre inscription est confirmée.'); return redirect('event_detail',slug=slug)
    return render(request,'core/event_detail.html',{'event':event,'form':form,'registration_count':event.registrations.count()})
def event_ics(request,slug):
    event=get_object_or_404(Event,slug=slug,published=True)
    start=event.starts_at.strftime('%Y%m%dT%H%M%S')
    end=(event.ends_at or event.starts_at).strftime('%Y%m%dT%H%M%S')
    def esc(value): return str(value).replace('\\','\\\\').replace(';','\\;').replace(',','\\,').replace('\n','\\n')
    body='BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//UQOnnect//FR-CA\r\nBEGIN:VEVENT\r\nUID:uqonnect-'+event.slug+'\r\nDTSTART:'+start+'\r\nDTEND:'+end+'\r\nSUMMARY:'+esc(event.title)+'\r\nDESCRIPTION:'+esc(event.summary or event.description)+'\r\nLOCATION:'+esc(event.location)+'\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n'
    response=HttpResponse(body,content_type='text/calendar; charset=utf-8'); response['Content-Disposition']='attachment; filename="'+event.slug+'.ics"'; return response
def articles(request):
    qs=Article.objects.filter(published=True,published_at__lte=timezone.now()); q=request.GET.get('q','').strip()
    if q: qs=qs.filter(title__icontains=q)
    return render(request,'core/articles.html',{'page_obj':Paginator(qs,9).get_page(request.GET.get('page')),'query':q})
def article_detail(request,slug):
    article=get_object_or_404(Article,slug=slug,published=True,published_at__lte=timezone.now())
    return render(request,'core/article_detail.html',{'article':article,'related':Article.objects.filter(published=True).exclude(pk=article.pk)[:3]})
def projects(request):
    form=ProjectSubmissionForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        form.save(); messages.success(request,'Merci! Votre proposition sera examinée par le comité.'); return redirect('projects')
    return render(request,'core/projects.html',{'projects':Project.objects.filter(approved=True),'form':form})
def contact(request):
    form=ContactForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        item=form.save()
        send_mail(f'UQOnnect — {item.subject}', f'{item.name} ({item.email})\n\n{item.message}', settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_EMAIL], fail_silently=True)
        messages.success(request,'Merci! Votre message a bien été envoyé.'); return redirect('contact')
    return render(request,'core/contact.html',{'form':form})
def sitemap(request):
    pages=['/','/a-propos/','/evenements/','/projets/','/actualites/','/contact/']
    return HttpResponse('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{request.build_absolute_uri(p)}</loc></url>' for p in pages)+'</urlset>',content_type='application/xml')
def robots(request): return HttpResponse('User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: '+request.build_absolute_uri('/sitemap.xml'),content_type='text/plain')
