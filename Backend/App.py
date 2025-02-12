from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import tempfile
import os
import pandas as pd
import math
import re

app = Flask(__name__)
CORS(app)

# Correspondances entre les noms des tests et des données
correspondance_tests = {
    "Test TX_BR : 2402MHz  1-DH5 PRBS": "TX_BDR  2402 1DH5",
    "Test TX_BR : 2480MHz  1-DH5 PRBS": "TX_BDR  2480 1DH5",
    "Test TX_EDR : 2402MHz  3-DH5 PRBS": "TX_EDR  2402 3DH5",
    "Test TX_BLE :  2402MHz  LE 1M PRBS": "TX_LE  2402 1LE",
    "Test TX_BLE :  2480MHz  LE 1M PRBS": "TX_LE  2480 1LE",
    "Test RX_BR :  2480MHz  1-DH5 PRBS": "RX_BDR  2480 1DH5",
    "Test RX_EDR :2402 3-DH5 PRBS": "RX_EDR  2402 3DH5",
    "Test RX_BLE : 2442MHZ  LE 1M PRBS": "RX_LE  2442 1LE"
}

correspondance_donnees = {
    "Power": "POWER_AVERAGE_DBM",
    "Frequency drift": "FREQ_DRIFT",
    "Max drift rate": "MAX_FREQ_DRIFT_RATE",
    "Frequency deviation df2 ": "DELTA_F2_MAX",
    "Frequency stability w0+wi": "EDR_EXTREME_OMEGA_I0",
    "BER at RX Power -89dBm": "BER",
    "BER at RX Power -87dBm": "BER",
    "PER at RX Power -93dBm": "PER"
}

# Fonction pour comparer deux valeurs avec gestion de NaN et des chaînes
def comparer_valeurs(val1, val2):
    try:
        val1 = float(val1) if isinstance(val1, (int, float, str)) and val1 != "" else math.nan
    except ValueError:
        val1 = math.nan
    try:
        val2 = float(val2) if isinstance(val2, (int, float, str)) and val2 != "" else math.nan
    except ValueError:
        val2 = math.nan

    # Remplacer NaN par 999 pour comparaison
    val1 = 999 if math.isnan(val1) else val1
    val2 = 999 if math.isnan(val2) else val2
    return val1 == val2

# Fonction pour comparer les données entre Excel et Log
def comparer_donnees(excel_tests, log_tests):
    resultat_comparaison = []
    tests_non_trouves = {"Excel": [], "Log": []}  # Stocker les tests non trouvés

    # Comparer chaque test Excel avec le test Log correspondant
    for test_excel, test_log in correspondance_tests.items():
        # Trouver les tests correspondants dans Excel et Log
        donnees_excel = next((t for t in excel_tests if t["Test"].strip() == test_excel.strip()), None)
        donnees_log = next((t for t in log_tests if t["Test"].strip() == test_log.strip()), None)

        if donnees_excel and donnees_log:
            comparaison_test = {
                "Test Excel": test_excel,
                "Test Log": test_log,
                "Données": []
            }

            for nom_excel, nom_log in correspondance_donnees.items():
                # Rechercher les indices des données correspondantes
                index_excel = (
                    donnees_excel["Données"]["Nom"].index(nom_excel)
                    if nom_excel in donnees_excel["Données"]["Nom"]
                    else None
                )
                index_log = next(
                    (i for i, d in enumerate(donnees_log["Données"]) if d["Nom"] == nom_log),
                    None,
                )

                if index_excel is not None and index_log is not None:
                    # Extraire les valeurs Min et Max
                    min_excel = donnees_excel["Données"]["Min"][index_excel]
                    max_excel = donnees_excel["Données"]["Max"][index_excel]
                    min_log = donnees_log["Données"][index_log]["Min"]
                    max_log = donnees_log["Données"][index_log]["Max"]

                    # Comparer les valeurs Min et Max
                    comparaison_test["Données"].append({
                        "Nom Excel": nom_excel,
                        "Nom Log": nom_log,
                        "Min Excel": min_excel,
                        "Min Log": min_log,
                        "Min Identique": comparer_valeurs(min_excel, min_log),
                        "Max Excel": max_excel,
                        "Max Log": max_log,
                        "Max Identique": comparer_valeurs(max_excel, max_log)
                    })

            resultat_comparaison.append(comparaison_test)
        else:
            # Stocker les tests non trouvés
            if not donnees_excel:
                tests_non_trouves["Excel"].append(test_excel)
            if not donnees_log:
                tests_non_trouves["Log"].append(test_log)

    return resultat_comparaison, tests_non_trouves

@app.route('/api/compare', methods=['POST'])
def compare_files():
    try:
        excel_file = request.files['excel']
        log_file = request.files['log']

        # Sauvegarde temporaire des fichiers
        with tempfile.TemporaryDirectory() as tmp_dir:
            excel_path = os.path.join(tmp_dir, secure_filename(excel_file.filename))
            log_path = os.path.join(tmp_dir, secure_filename(log_file.filename))
            
            excel_file.save(excel_path)
            log_file.save(log_path)

            # Lecture et traitement du fichier Excel
            print("Début du traitement du fichier Excel...")
            try:
                df = pd.read_excel(excel_path, sheet_name='BWC', header=None)
                print(f"Fichier Excel '{excel_path}' chargé avec succès.")

                # Convertir le DataFrame en liste de listes
                matrice = df.values.tolist()

                tableau_tests = []
                enregistrement = None

                def a_trop_de_nan_fin(ligne, seuil=7):
                    nan_count = 0
                    for val in reversed(ligne):
                        if isinstance(val, float) and math.isnan(val):
                            nan_count += 1
                        else:
                            break
                    return nan_count >= seuil

                for ligne in matrice:
                    if isinstance(ligne[0], str) and ligne[0].startswith("Test"):
                        if enregistrement:
                            tableau_tests.append(enregistrement)
                        enregistrement = {
                            "Test": ligne[0],
                            "Données": {"Nom": [], "Min": [], "Max": []}
                        }
                    elif enregistrement and not a_trop_de_nan_fin(ligne):
                        if len(ligne) > 4:
                            enregistrement["Données"]["Nom"].append(ligne[0])
                            enregistrement["Données"]["Min"].append(ligne[3])
                            enregistrement["Données"]["Max"].append(ligne[4])

                if enregistrement:
                    tableau_tests.append(enregistrement)

                print("Analyse du fichier Excel terminée.")

            except Exception as e:
                print(f"Erreur lors de la lecture du fichier Excel : {e}")

            # Lecture et traitement du fichier log
            print("\nDébut du traitement du fichier log...")
            try:
                with open(log_path, "r") as file:
                    tableau_enregistrements = []
                    enregistrement = None

                    regex_test = re.compile(r"^\d+\.(TX|RX).*")
                    regex_clean_test = re.compile(r"^\d+\.\s*|\s*_{2,}$")
                    regex_key_value = re.compile(r"^([\w\d_\- ]+)\s*:\s*(.*)$")
                    regex_values_with_range = re.compile(r"^(.*)\s*\((\s*[\d\.\-]*)\s*,\s*([\d\.\-]*)\s*\)$")

                    for ligne in file:
                        ligne = ligne.strip()
                        if regex_test.match(ligne):
                            if enregistrement:
                                tableau_enregistrements.append(enregistrement)
                            ligne_nettoyee = regex_clean_test.sub("", ligne)
                            enregistrement = {"Test": ligne_nettoyee.strip(), "Données": []}
                        elif enregistrement and regex_key_value.match(ligne):
                            key, value = regex_key_value.match(ligne).groups()
                            match = regex_values_with_range.match(value)
                            if match:
                                valeur, min_val, max_val = match.groups()
                                min_val = float(min_val) if min_val else math.nan
                                max_val = float(max_val) if max_val else math.nan
                                enregistrement["Données"].append({
                                    "Nom": key.strip(),
                                    "Valeur": valeur.strip(),
                                    "Min": min_val,
                                    "Max": max_val
                                })

                    if enregistrement:
                        tableau_enregistrements.append(enregistrement)

                print("Analyse du fichier log terminée.")

            except Exception as e:
                print(f"Erreur lors du traitement du fichier log : {e}")

            # Comparaison des données
            print("\nDébut de la comparaison des données...")
            resultats, tests_non_trouves = comparer_donnees(tableau_tests, tableau_enregistrements)

            # Afficher les résultats
            if resultats:
                for resultat in resultats:
                    print(f"Test Excel : {resultat['Test Excel']} <=> Test Log : {resultat['Test Log']}")
                    for donnee in resultat["Données"]:
                        print(f"  Nom Excel : {donnee['Nom Excel']} <=> Nom Log : {donnee['Nom Log']}")
                        print(f"    Min Excel : {donnee['Min Excel']} <=> Min Log : {donnee['Min Log']} | Identique : {donnee['Min Identique']}")
                        print(f"    Max Excel : {donnee['Max Excel']} <=> Max Log : {donnee['Max Log']} | Identique : {donnee['Max Identique']}")
                    print("\n")
            else:
                print("Aucun test correspondant trouvé entre Excel et le fichier Log.")


            return jsonify({
                "results": resultats,
            })

    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

if __name__ == '__main__':
    app.run(debug=True)