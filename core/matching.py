import re

def extraire_heure(dispo_str):
    """
    Extrait les heures de début et fin d'une disponibilité
    Exemple: "Lundi 14h-16h" → (14, 16)
             "Mercredi 10h30-12h30" → (10.5, 12.5)
    """
    # Pattern pour trouver les heures au format "14h" ou "14h30"
    match = re.search(r'(\d{1,2})(?:h|:)(\d{2})?\s*[-–]\s*(\d{1,2})(?:h|:)(\d{2})?', dispo_str)
    if match:
        h1 = int(match.group(1))
        m1 = int(match.group(2) or '0')
        h2 = int(match.group(3))
        m2 = int(match.group(4) or '0')
        
        # Convertir en minutes pour faciliter les calculs
        debut = h1 * 60 + m1
        fin = h2 * 60 + m2
        return (debut, fin)
    return None

def extraire_jour(dispo_str):
    """
    Extrait le jour d'une disponibilité
    Exemple: "Lundi 14h-16h" → "lundi"
    """
    jours = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
    for jour in jours:
        if jour in dispo_str.lower():
            return jour
    return None

def horaires_compatibles(dispo_mentor, heure_recherchee, tolerance=60):
    """
    Vérifie si deux horaires sont compatibles avec une tolérance en minutes
    Par défaut: tolérance de 60 minutes (±1 heure)
    """
    if not heure_recherchee:
        return True  # Pas d'horaire spécifié → compatible
    
    # Extraire le jour et l'heure de la disponibilité du mentor
    jour_mentor = extraire_jour(dispo_mentor)
    heure_mentor = extraire_heure(dispo_mentor)
    
    # Extraire le jour et l'heure de la recherche
    jour_recherche = extraire_jour(heure_recherchee)
    heure_recherche = extraire_heure(heure_recherchee)
    
    # Vérifier si les jours correspondent
    if jour_mentor and jour_recherche and jour_mentor != jour_recherche:
        return False
    
    # Vérifier si les heures se chevauchent
    if heure_mentor and heure_recherche:
        debut_m, fin_m = heure_mentor
        debut_r, fin_r = heure_recherche
        
        # Vérifier l'intersection avec tolérance
        if fin_m < debut_r - tolerance:
            return False
        if fin_r < debut_m - tolerance:
            return False
        
        return True
    
    return False

def calculer_score(mentor, competences_recherchees, heure_recherchee, filiere_recherchee):
    """
    Calcule le score de compatibilité d'un mentor
    Retourne: (score, competences_communes)
    """
    score = 0
    competences_communes = []
    
    # Nettoyer et préparer les compétences
    competences_mentor = mentor.get_competences_list()
    competences_rech = [c.strip().lower() for c in competences_recherchees.split(',') if c.strip()]
    
    # 1. Vérifier les compétences communes (OBLIGATOIRE)
    for comp in competences_rech:
        for comp_mentor in competences_mentor:
            if comp in comp_mentor or comp_mentor in comp:
                if comp not in competences_communes:
                    competences_communes.append(comp)
                break
    
    # Si aucune compétence commune, score = 0
    if not competences_communes:
        return 0, []
    
    # 30 points par compétence commune
    score += len(competences_communes) * 30
    
    # 2. Compatibilité horaire (bonus 25 points)
    if heure_recherchee:
        disponibilites_mentor = mentor.get_disponibilites_list()
        for dispo in disponibilites_mentor:
            if horaires_compatibles(dispo, heure_recherchee):
                score += 25
                break
    
    # 3. Même filière (bonus 15 points)
    if filiere_recherchee and mentor.filiere:
        if filiere_recherchee.lower() in mentor.filiere.lower():
            score += 15
    
    return score, competences_communes