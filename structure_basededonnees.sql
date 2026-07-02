
-- Table mentors
CREATE TABLE mentors(
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    telephone VARCHAR(20) UNIQUE,
    photo_profil VARCHAR(255),
    promo VARCHAR(10) NOT NULL,
    filiere VARCHAR(100) NOT NULL,
    bio TEXT,
    competences TEXT NOT NULL,
    disponibilites TEXT NOT NULL,
    format_mentorat VARCHAR(30) DEFAULT'les_deux',
    actif BOOLEAN DEFAULT TRUE,
    date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE mentors ADD CONSTRAINT check_format_mentorat
  CHECK (format_mentorat IN ('presentiel', 'en_ligne', 'les_deux'))