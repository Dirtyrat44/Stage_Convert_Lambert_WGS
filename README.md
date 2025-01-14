# Lambert-93 to WGS84 CSV Converter

Ce script Python permet de convertir des coordonnées au format **Lambert-93** (EPSG:2154) en **WGS84** (EPSG:4326).  
Il lit un fichier CSV (avec séparateur `;`), récupère deux colonnes (X et Y) en Lambert-93, effectue la conversion, puis enregistre le résultat dans un nouveau fichier suffixé par `_WGS84.csv`.

---

## Fonctionnalités

- **Lecture** d'un fichier CSV (point-virgule, virgule décimale).
- **Filtrage** des colonnes vides pour ignorer d’éventuelles colonnes inutiles.
- **Conversion** Lambert-93 vers WGS84 (latitude/longitude en degrés décimaux).
- **Écriture** d’un nouveau fichier CSV avec deux nouvelles colonnes : `latitude_wgs84` et `longitude_wgs84`.

---

## Structure du script

### `lambert93_to_wgs84(x, y)`
- Reçoit des coordonnées en Lambert-93 (X, Y en mètres).
- Calcule la latitude et la longitude en WGS84 (degrés décimaux).
- Retourne un tuple `(latitude, longitude)`.

### `main()`
1. **Demande** le chemin ou le nom du fichier CSV d’entrée.  
2. **Lit** le CSV (séparateur `;`), détecte les champs (colonne 1 = X, colonne 2 = Y).  
3. **Convertit** chaque ligne en WGS84.  
4. **Génère** un nouveau fichier CSV suffixé de `_WGS84.csv`.  
5. Gère les éventuelles erreurs (fichier manquant, données invalides, etc.).

---

## Pré-requis

- **Python 3.x**  
- Aucune bibliothèque externe nécessaire (uniquement `math` et `csv` de la bibliothèque standard).

---

## Format du fichier CSV attendu

- **Séparateur** : `;` (point-virgule)  
- **Au moins deux colonnes** : la première pour X, la seconde pour Y, en Lambert-93.  
- **Virgule décimale** possible (ex : `433204,06`) : le script la convertit en point décimal.

### Exemple de fichier CSV :

```csv
X;Y
433204,06;5621352,34
433205,48;5621360,87
...
```

# Utilisation

1. **Exécutez le script avec Python :**

    ```bash
    python script.py
    ```

2. **Entrez le chemin ou le nom du fichier CSV à convertir lorsqu’il est demandé.**

3. **Une fois la conversion terminée, le fichier de sortie sera généré avec le suffixe `_WGS84.csv`.**

# Résultat

Le fichier CSV généré contiendra les colonnes d’origine ainsi que deux nouvelles colonnes :

- `latitude_wgs84`
- `longitude_wgs84`

**Exemple de sortie :**

| X         | Y          | latitude_wgs84 | longitude_wgs84 |
|-----------|------------|----------------|-----------------|
| 433204.06 | 5621352.34 | 50.634722      | 3.068611        |
| 433205.48 | 5621360.87 | 50.635000      | 3.069000        |
| ...       | ...        | ...            | ...             |


# Conclusion

Ce script simplifie la conversion des coordonnées dans vos fichiers CSV vers le système de référence WGS84. En ajoutant automatiquement les colonnes de latitude et de longitude, il facilite l'intégration des données géospatiales dans vos projets. Grâce à son utilisation intuitive, vous pouvez rapidement transformer vos données sans effort supplémentaire.

