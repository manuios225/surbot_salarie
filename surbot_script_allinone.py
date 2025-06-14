import time
import json
import random
from datetime import datetime, timezone
import requests
import uuid
import os

# === CONFIGURATION ===
ADRESSE_WALLET = "0x4753ED479Af500aCa60aF66223AD88f5d2eB5ad1"
FICHIER_SIGNAUX = "signaux_surbot.json"
FICHIER_URLS = "urls_ocean.txt"
FICHIER_CIDS = "cid_log.txt"
INTERVALLE_MINUTES = 5  # Intervalle de génération des signaux (en minutes)
NFT_STORAGE_API_KEY = "f4ded406.726f8d71eed34936a5885a906bc54a42"  # Injectée en dur pour test
NFT_STORAGE_URL = "https://api.nft.storage/upload"

# === GÉNÉRATION DE SIGNAUX STRUCTURÉS POUR BOTS IA ===
def generer_signal():
    timestamp = datetime.now(timezone.utc).isoformat()
    signal = {
        "@context": "https://schema.org",
        "@type": "DataFeedItem",
        "identifier": str(uuid.uuid4()),
        "dateCreated": timestamp,
        "wallet": ADRESSE_WALLET,
        "signal": {
            "type": random.choice(["🔴 URGENCE", "🟠 RISQUE", "🟢 OPPORTUNITÉ"]),
            "domaine": random.choice(["crypto", "climat", "cybersécurité", "tendance", "santé", "marchés"]),
            "valeur": round(random.uniform(0.1, 1.0), 4)
        }
    }
    return signal

# === ENREGISTREMENT LOCAL DU SIGNAL POUR BACKUP ===
def enregistrer_local(signal):
    try:
        with open(FICHIER_SIGNAUX, "a") as f:
            f.write(json.dumps(signal) + "\n")
    except Exception as e:
        print(f"❌ Erreur d'enregistrement local : {e}")

# === ENVOI VERS NFT.STORAGE ===
def publier_nftstorage(signal):
    if not NFT_STORAGE_API_KEY:
        print("❌ Clé API NFT.Storage manquante. Ajoutez NFT_STORAGE_API_KEY aux variables d'environnement.")
        return
    try:
        headers = {"Authorization": f"Bearer {NFT_STORAGE_API_KEY}"}
        files = {'file': ("signal.json", json.dumps(signal))}
        response = requests.post(NFT_STORAGE_URL, headers=headers, files=files)
        if response.status_code == 200:
            cid = response.json().get("value", {}).get("cid")
            print(f"✅ Signal stocké sur NFT.Storage CID: {cid}")

            # Sauvegarde du CID localement
            with open(FICHIER_CIDS, "a") as cid_file:
                cid_file.write(f"{cid} | {signal['dateCreated']}\n")

            # Génération de l'URL IPFS pour Ocean
            url = f"https://{cid}.ipfs.nftstorage.link"
            with open(FICHIER_URLS, "a") as f_url:
                f_url.write(url + "\n")
        else:
            print(f"❌ Erreur NFT.Storage: {response.status_code} => {response.text}")
    except Exception as e:
        print(f"❌ Exception envoi NFT.Storage : {e}")

# === BOUCLE PRINCIPALE DU SURBOT ===
if __name__ == "__main__":
    print("🚀 Surbot salarié perpétuel PRO lancé...")
    while True:
        signal = generer_signal()
        enregistrer_local(signal)
        publier_nftstorage(signal)
        print(f"💾 Signal structuré : {signal['identifier']} envoyé à {signal['dateCreated']}")
        time.sleep(INTERVALLE_MINUTES * 60)
