from django.contrib import admin

# Register your models here.
from .models import Mentor

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ['id', 'prenom', 'nom', 'filiere', 'promo', 'actif', 'date_inscription']
    list_filter = ['actif', 'filiere', 'promo', 'format_mentorat']
    search_fields = ['nom', 'prenom', 'telephone', 'filiere', 'competences']
    list_editable = ['actif']
    ordering = ['-date_inscription']
    fieldsets = (
        ('Identité', {
            'fields': ('nom', 'prenom', 'telephone', 'photo_profil')
        }),
        ('Parcours', {
            'fields': ('promo', 'filiere', 'bio')
        }),
        ('Compétences et Disponibilités', {
            'fields': ('competences', 'disponibilites')
        }),
        ('Paramètres', {
            'fields': ('format_mentorat', 'actif')
        }),
    )