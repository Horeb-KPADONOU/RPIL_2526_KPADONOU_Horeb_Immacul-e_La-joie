# 1. Imports standards de Python
# ============================================
import json

# ============================================
# 2. Imports de Django
# ============================================
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

# ============================================
# 3. Imports de ton application
# ============================================
from .models import Mentor
from .matching import calculer_score


# ============================================
# 4. Vues
# ============================================

def index(request):
    """Page principale"""
    return render(request, 'index.html')


@csrf_exempt
def rechercher_mentors(request):
    """API de recherche de mentors"""
    if request.method != 'POST':
        return JsonResponse({'erreur': 'Méthode non autorisée'}, status=405)
    
    try:
        data = json.loads(request.body)
        competences = data.get('competences', '')
        heure = data.get('heure', '')
        filiere = data.get('filiere', '')
        
        if not competences:
            return JsonResponse({'erreur': 'Veuillez saisir au moins une compétence'}, status=400)
        
        mentors = Mentor.objects.filter(actif=True)
        resultats = []
        
        for mentor in mentors:
            score, competences_communes = calculer_score(
                mentor, competences, heure, filiere
            )
            
            if score > 0:
                resultats.append({
                    'id': mentor.id,
                    'nom': f"{mentor.prenom} {mentor.nom}",
                    'filiere': mentor.filiere,
                    'competences_communes': competences_communes,
                    'disponibilites': mentor.get_disponibilites_list(),
                    'format_mentorat': mentor.get_format_mentorat_display(),
                    'score': score,
                    'competences_completes': mentor.get_competences_list(),
                    'telephone': mentor.telephone or None,
                    'bio': mentor.bio or '',
                    'photo_profil': mentor.photo_profil.url if mentor.photo_profil else None,
                })
        
        resultats.sort(key=lambda x: x['score'], reverse=True)
        
        return JsonResponse({
            'total': len(resultats),
            'resultats': resultats
        }, status=200)
    
    except json.JSONDecodeError:
        return JsonResponse({'erreur': 'JSON invalide'}, status=400)
    except Exception as e:
        return JsonResponse({'erreur': str(e)}, status=500)


def liste_mentors(request):
    """Retourne tous les mentors (pour test)"""
    mentors = Mentor.objects.filter(actif=True)
    data = [{
        'id': m.id,
        'nom': f"{m.prenom} {m.nom}",
        'competences': m.get_competences_list(),
        'disponibilites': m.get_disponibilites_list()
    } for m in mentors]
    return JsonResponse(data, safe=False)


def upload_photo_page(request, mentor_id):
    """Page d'upload de photo"""
    mentor = get_object_or_404(Mentor, id=mentor_id)
    return render(request, 'upload_photo.html', {'mentor': mentor})


@csrf_exempt
def upload_photo(request, mentor_id):
    """API d'upload de photo"""
    if request.method != 'POST':
        return JsonResponse({'erreur': 'Méthode non autorisée'}, status=405)
    
    try:
        mentor = get_object_or_404(Mentor, id=mentor_id)
        
        if 'photo' not in request.FILES:
            return JsonResponse({'erreur': 'Aucune photo envoyée'}, status=400)
        
        photo = request.FILES['photo']
        
        if not photo.content_type.startswith('image/'):
            return JsonResponse({'erreur': 'Le fichier doit être une image'}, status=400)
        
        if photo.size > 5 * 1024 * 1024:
            return JsonResponse({'erreur': 'La photo ne doit pas dépasser 5 Mo'}, status=400)
        
        mentor.photo_profil = photo
        mentor.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Photo uploadée avec succès',
            'photo_url': mentor.photo_profil.url
        }, status=200)
        
    except Exception as e:
        return JsonResponse({'erreur': str(e)}, status=400)
def index(request):
    """Page principale de recherche"""
    return render(request, 'index.html')   