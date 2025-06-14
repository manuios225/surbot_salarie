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
INTERVALLE_MINUTES = 5  # Intervalle de génération des signaux (en minutes)
NFT_STORAGE_API_KEY = os.getenv("NFT_STORAGE_API_KEY")  # à définir dans Render
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
        print(f"❌ Erreur d'enregistrement local : {e}", flush=True)

# === ENVOI VERS NFT.STORAGE ===
def publier_nftstorage(signal):
    if not NFT_STORAGE_API_KEY:
        print("❌ Clé API NFT.Storage manquante. Ajoutez NFT_STORAGE_API_KEY aux variables d'environnement.", flush=True)
        return
    try:
        headers = {"Authorization": f"Bearer {NFT_STORAGE_API_KEY}"}
        files = {'file': ("signal.json", json.dumps(signal))}
        response = requests.post(NFT_STORAGE_URL, headers=headers, files=files)
        if response.status_code == 200:
            cid = response.json().get("value", {}).get("cid")
            print(f"✅ Signal stocké sur NFT.Storage CID: {cid}", flush=True)
            # Sauvegarde du CID localement
            with open("cid_log.txt", "a") as cid_file:
                cid_file.write(f"{cid} | {signal['dateCreated']}\n")
            # Sauvegarde en URL directe pour Ocean Market (IPFS Gateway)
            with open("urls_ocean.txt", "a") as url_file:
                url_file.write(f"https://{cid}.ipfs.nftstorage.link\n")
        else:
            print(f"❌ Erreur NFT.Storage: {response.status_code} => {response.text}", flush=True)
    except Exception as e:
        print(f"❌ Exception envoi NFT.Storage : {e}", flush=True)

# === BOUCLE PRINCIPALE DU SURBOT ===
if __name__ == "__main__":
    print("🚀 Surbot salarié perpétuel PRO lancé...", flush=True)
    while True:
        try:
            signal = generer_signal()
            enregistrer_local(signal)
            publier_nftstorage(signal)
            print(f"💾 Signal structuré : {signal['identifier']} envoyé à {signal['dateCreated']}", flush=True)
        except Exception as e:
            print(f"❌ Erreur dans la boucle principale : {e}", flush=True)
        time.sleep(INTERVALLE_MINUTES * 60)
