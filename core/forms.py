from django import forms
from .models import ContactMessage, EventRegistration, ProjectSubmission

class ContactForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput)
    class Meta:
        model = ContactMessage
        fields = ['name','email','subject','message','consent']
        widgets = {'message':forms.Textarea(attrs={'rows':5})}
        labels = {'name':'Nom','email':'Adresse courriel','subject':'Sujet','message':'Votre message','consent':'J’accepte que mes renseignements soient utilisés pour répondre à ma demande.'}
    def clean_website(self):
        value = self.cleaned_data['website']
        if value: raise forms.ValidationError('Soumission invalide.')
        return value

class EventRegistrationForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput)
    class Meta:
        model = EventRegistration
        fields = ['name','email','program','consent']
        labels = {'name':'Nom et prénom','email':'Adresse courriel','program':'Programme d’études (facultatif)','consent':'J’accepte que mes renseignements soient utilisés pour gérer mon inscription.'}
    def clean_website(self):
        if self.cleaned_data['website']: raise forms.ValidationError('Soumission invalide.')
        return self.cleaned_data['website']

class ProjectSubmissionForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput)
    class Meta:
        model = ProjectSubmission
        fields = ['title','description','domain','technologies','authors','email','consent']
        labels = {'title':'Titre du projet','description':'Description','domain':'Domaine','technologies':'Technologies utilisées','authors':'Auteurs (avec leur accord)','email':'Courriel de contact','consent':'J’autorise le comité à examiner cette proposition et à me recontacter.'}
        widgets = {'description':forms.Textarea(attrs={'rows':5})}
    def clean_website(self):
        if self.cleaned_data['website']: raise forms.ValidationError('Soumission invalide.')
        return self.cleaned_data['website']
