import math
import csv

def lambert93_to_wgs84(x, y):
    """
    Convertit des coordonnées Lambert-93 (EPSG:2154) en WGS84 (EPSG:4326).

    :param x: Coordonnée X en Lambert-93 (mètres).
    :param y: Coordonnée Y en Lambert-93 (mètres).
    :return: Un tuple (latitude, longitude) en degrés décimaux (WGS84).
    """
    # ------------------------------
    # Paramètres Lambert-93 (IGN)
    # ------------------------------
    # Éllipsoïde GRS80 (quasi identique à WGS84 d'un point de vue géodésique)
    e = 0.0818191910428158  # excentricité de l'ellipsoïde
    n = 0.7256077650532670  # coefficient n (facteur d'échelle)
    C = 11754255.426096     # constante C
    xs = 700000.0           # coordonnée X du faux point d'origine (en Lambert-93)
    ys = 12655612.049876    # coordonnée Y du faux point d'origine (en Lambert-93)
    lon_0 = 3.0             # méridien central (en degrés Est)

    # ------------------------------
    # 1) Distance R et angle gamma
    # ------------------------------
    R = math.sqrt((x - xs)**2 + (y - ys)**2)       # distance radiale depuis (xs, ys)
    gamma = math.atan((x - xs) / (ys - y))         # angle par rapport au méridien central

    # ------------------------------
    # 2) Conversion en latitude isométrique
    # ------------------------------
    lat_iso = -1.0 / n * math.log(abs(R / C))

    # ------------------------------
    # 3) Conversion latitude isométrique -> latitude géographique (itérations)
    # ------------------------------
    phi = 2 * math.atan(math.exp(lat_iso)) - math.pi / 2
    for _ in range(10):
        phi = 2 * math.atan(
            ((1 + e * math.sin(phi)) / (1 - e * math.sin(phi))) ** (e / 2)
            * math.exp(lat_iso)
        ) - math.pi / 2

    # ------------------------------
    # 4) Calcul de la longitude (lambda en radians)
    # ------------------------------
    lambda_radians = gamma / n + (lon_0 * math.pi / 180.0)

    # ------------------------------
    # 5) Conversion en degrés décimaux
    # ------------------------------
    latitude = phi * 180.0 / math.pi
    longitude = lambda_radians * 180.0 / math.pi

    return (latitude, longitude)


def main():
    """
    Lit un fichier CSV (séparateur : point-virgule) contenant 
    (au moins) deux colonnes correspondant à X et Y en Lambert-93,
    convertit ces coordonnées en WGS84, et enregistre le résultat
    dans un nouveau fichier CSV (suffixé par "_WGS84.csv").

    Étapes principales :
      1. Demande du chemin/nom du fichier CSV original.
      2. Ouverture et lecture via `csv.DictReader` (avec délimiteur ';').
      3. Filtrage des colonnes vides et détermination de la première et
         deuxième colonne comme étant X et Y.
      4. Conversion Lambert-93 -> WGS84.
      5. Écriture du résultat dans un nouveau CSV.
    """
    # Saisie utilisateur : le nom (ou le chemin) du fichier CSV d'entrée
    csv_file_in = input("Chemin (ou nom) du fichier CSV (Lambert-93) : ")

    # On génère le nom du fichier de sortie en rajoutant "_WGS84.csv"
    csv_file_out = csv_file_in + "_WGS84.csv"

    try:
        # Ouverture du fichier CSV d'entrée en lecture
        with open(csv_file_in, mode="r", newline="", encoding="utf-8") as f_in:
            # On utilise DictReader avec un séparateur de type point-virgule
            reader = csv.DictReader(f_in, delimiter=";")
            fieldnames = reader.fieldnames  # Liste des noms de colonnes

            # Filtrer les colonnes vides (celles qui n'ont pas de nom, 
            # ou juste des espaces) pour éviter d'avoir plein de colonnes inutiles
            filtered_fieldnames = [name for name in fieldnames if name and name.strip()]

            # On ajoute à la fin du fichier deux colonnes vides ("", "")
            # avant nos deux nouvelles colonnes : "latitude_wgs84" et "longitude_wgs84".
            # (Cette étape est optionnelle, selon ce que vous souhaitez faire
            # des colonnes vides.)
            output_fieldnames = filtered_fieldnames + ["", ""] + ["latitude_wgs84", "longitude_wgs84"]

            # On considère la première colonne (après filtrage) comme X, 
            # la deuxième comme Y (Lambert-93)
            x_col_name = fieldnames[0]
            y_col_name = fieldnames[1]

            # Ouverture du fichier CSV de sortie en écriture
            with open(csv_file_out, mode="w", newline="", encoding="utf-8") as f_out:
                # On définit le DictWriter avec les noms de colonnes de sortie 
                # (et toujours le séparateur ';')
                writer = csv.DictWriter(f_out, fieldnames=output_fieldnames, delimiter=";")
                writer.writeheader()  # Écrit la ligne d'en-tête

                # Parcours des lignes du CSV d'entrée
                for row in reader:
                    # On récupère les valeurs X et Y dans la 1ère et 2ème colonne
                    # en remplaçant la virgule décimale ',' par un point '.'
                    try:
                        x_str = row[x_col_name].replace(",", ".")
                        y_str = row[y_col_name].replace(",", ".")

                        x_val = float(x_str)
                        y_val = float(y_str)
                    except (ValueError, KeyError):
                        # Si la conversion échoue (valeur non numérique ou colonne inexistante),
                        # on ignore simplement cette ligne
                        continue

                    # Conversion Lambert93 -> WGS84
                    lat, lon = lambert93_to_wgs84(x_val, y_val)

                    # On ajoute ces infos dans la ligne
                    row["latitude_wgs84"] = lat
                    row["longitude_wgs84"] = lon

                    # On ne réécrit que les colonnes valides + lat/long
                    # En d'autres termes, on "filtre" le dictionnaire original
                    # pour ne conserver que ce qui nous intéresse.
                    filtered_row = {k: row[k] for k in filtered_fieldnames if k in row}
                    filtered_row["latitude_wgs84"] = lat
                    filtered_row["longitude_wgs84"] = lon

                    # Écriture de la ligne modifiée dans le CSV de sortie
                    writer.writerow(filtered_row)

        print(f"Conversion terminée avec succès ! Fichier créé : {csv_file_out}")

    except FileNotFoundError:
        print(f"Le fichier {csv_file_in} est introuvable.")
    except Exception as e:
        print(f"Erreur : {e}")


if __name__ == "__main__":
    main()
