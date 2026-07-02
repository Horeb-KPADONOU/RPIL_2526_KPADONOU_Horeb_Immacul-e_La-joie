from django.db import models

# Create your models here.

class Mentor(models.Model):
    """
    Modèle représentant un mentor
    Correspond exactement à la table SQL 'mentors'
    """
    
    # Choix pour le format de mentorat
    FORMAT_CHOICES = [
        ('presentiel', 'Présentiel'),
        ('en_ligne', 'En ligne'),
        ('les_deux', 'Les deux'),
    ]
    
    # Champs
    nom = models.CharField(
        max_length=50,
        verbose_name="Nom"
    )
    
    prenom = models.CharField(
        max_length=100,
        verbose_name="Prénom"
    )
    
    telephone = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Téléphone"
    )
    
    photo_profil = models.ImageField(
        upload_to='photos_profil/',
        blank =True,
        null=True,
        verbose_name="Photo de profil",
    )
    
    promo = models.CharField(
        max_length=10,
        verbose_name="Promotion"
    )
    
    filiere = models.CharField(
        max_length=100,
        verbose_name="Filière"
    )
    
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name="Biographie"
    )
    
    competences = models.TextField(
        verbose_name="Compétences (séparées par des virgules (ex: python, bd, algo))"
    )
    
    disponibilites = models.TextField(
        verbose_name="Disponibilités (ex: Lundi 14h-16h)"
    )
    
    format_mentorat = models.CharField(
        max_length=30,
        choices=FORMAT_CHOICES,
        default='les_deux',
        verbose_name="Format de mentorat"
    )
    
    actif = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )
    
    date_inscription = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'inscription"
    )
    
    class Meta:
        db_table = 'ifri_mentorLink_rattrapage' 
        verbose_name = "Mentor"
        verbose_name_plural = "Mentors"
        ordering = ['nom', 'prenom']
    
    def _str_(self):
        """Affichage dans l'admin"""
        return f"{self.prenom} {self.nom} - {self.filiere}"
    
    def get_competences_list(self):
        """Retourne la liste des compétences"""
        if not self.competences:
            return []
        return [c.strip().lower() for c in self.competences.split(',') if c.strip()]
    
    def get_disponibilites_list(self):
        """Retourne la liste des disponibilités"""
        if not self.disponibilites:
            return []
        return [d.strip() for d in self.disponibilites.split(',') if d.strip()]
    
    def get_format_mentorat_display(self):
        """Retourne le format affichable"""
        return dict(self.FORMAT_CHOICES).get(self.format_mentorat, self.format_mentorat)