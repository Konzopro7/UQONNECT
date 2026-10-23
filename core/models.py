from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class EventCategory(models.Model):
    name = models.CharField('nom', max_length=80, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.name); super().save(*args, **kwargs)
    def __str__(self): return self.name

class Event(models.Model):
    REGISTRATION_CHOICES = [('none','Aucune inscription'),('external','Lien externe'),('internal','Formulaire interne')]
    title = models.CharField('titre', max_length=180)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(EventCategory, verbose_name='catégorie', on_delete=models.SET_NULL, null=True, blank=True)
    summary = models.CharField('résumé', max_length=240, blank=True)
    description = models.TextField('description')
    starts_at = models.DateTimeField('début')
    ends_at = models.DateTimeField('fin', null=True, blank=True)
    location = models.CharField('lieu', max_length=180)
    cover = models.ImageField('image de couverture', upload_to='events/', blank=True)
    speakers = models.CharField('intervenant·e·s', max_length=240, blank=True)
    published = models.BooleanField('publié', default=False)
    registration_type = models.CharField('inscription', max_length=12, choices=REGISTRATION_CHOICES, default='none')
    registration_url = models.URLField('lien d’inscription', blank=True)
    capacity = models.PositiveIntegerField('capacité', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['starts_at']; indexes = [models.Index(fields=['published','starts_at'])]
    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.title); super().save(*args, **kwargs)
    def __str__(self): return self.title
    @property
    def upcoming(self): return self.starts_at >= timezone.now()

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, verbose_name='événement', on_delete=models.CASCADE, related_name='registrations')
    name = models.CharField('nom et prénom', max_length=160)
    email = models.EmailField('courriel')
    program = models.CharField('programme d’études', max_length=140, blank=True)
    consent = models.BooleanField('consentement', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['created_at']
        constraints = [models.UniqueConstraint(fields=['event','email'], name='unique_registration_per_event_email')]
    def __str__(self): return f'{self.name} — {self.event}'

class Article(models.Model):
    title = models.CharField('titre', max_length=180)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.CharField('résumé', max_length=240)
    content = models.TextField('contenu')
    image = models.ImageField('image', upload_to='articles/', blank=True)
    author = models.CharField('auteur', max_length=120, blank=True)
    category = models.CharField('catégorie', max_length=80, blank=True)
    published = models.BooleanField('publié', default=False)
    published_at = models.DateTimeField('date de publication', default=timezone.now)
    class Meta: ordering = ['-published_at']
    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.title); super().save(*args, **kwargs)
    def __str__(self): return self.title

class CommitteeMember(models.Model):
    name = models.CharField('nom', max_length=120)
    role = models.CharField('fonction', max_length=120)
    bio = models.TextField('biographie', blank=True)
    photo = models.ImageField('photo', upload_to='team/', blank=True)
    link = models.URLField('lien professionnel', blank=True)
    order = models.PositiveIntegerField('ordre', default=0)
    active = models.BooleanField('actif·ve', default=True)
    class Meta: ordering = ['order','name']
    def __str__(self): return f'{self.name} — {self.role}'

class Project(models.Model):
    title = models.CharField('titre', max_length=160)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField('description')
    domain = models.CharField('domaine', max_length=100, blank=True)
    technologies = models.CharField('technologies', max_length=240, blank=True)
    authors = models.CharField('auteur·rice·s', max_length=240, blank=True)
    image = models.ImageField('image', upload_to='projects/', blank=True)
    github_url = models.URLField('GitHub', blank=True)
    demo_url = models.URLField('démo', blank=True)
    approved = models.BooleanField('approuvé', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.title); super().save(*args, **kwargs)
    def __str__(self): return self.title

class ProjectSubmission(models.Model):
    title = models.CharField('titre', max_length=160)
    description = models.TextField('description')
    domain = models.CharField('domaine', max_length=100, blank=True)
    technologies = models.CharField('technologies', max_length=240, blank=True)
    authors = models.CharField('auteur·rice·s', max_length=240, blank=True)
    email = models.EmailField('courriel de contact')
    consent = models.BooleanField('accord de publication', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField('traité', default=False)
    def __str__(self): return self.title

class ContactMessage(models.Model):
    name = models.CharField('nom', max_length=120)
    email = models.EmailField('courriel')
    subject = models.CharField('sujet', max_length=160)
    message = models.TextField('message')
    consent = models.BooleanField('consentement', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField('traité', default=False)
    class Meta: ordering = ['-created_at']
    def __str__(self): return f'{self.subject} — {self.name}'
