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
FICHIER_CID = "cid_log.txt"
FICHIER_URL = "urls_ocean.txt"
INTERVALLE_MINUTES = 5
NFT_STORAGE_API_KEY = os.getenv("NFT_STORAGE_API_KEY")
NFT_STORAGE_URL = "https://api.nft.storage/upload"

def generer_signal():
    timestamp = datetime.now(timezone.utc).isoformat()
    return {
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

def enregistrer_local(signal):
    try:
        with open(FICHIER_SIGNAUX, "a") as f:
            f.write(json.dumps(signal) + "\n")
    except Exception as e:
        print(f"❌ Erreur d'enregistrement local : {e}")

def publier_nftstorage(signal):
    if not NFT_STORAGE_API_KEY:
        print("❌ Clé API NFT.Storage manquante.")
        return
    try:
        headers = {"Authorization": f"Bearer {NFT_STORAGE_API_KEY}"}
        files = {'file': ("signal.json", json.dumps(signal))}
        response = requests.post(NFT_STORAGE_URL, headers=headers, files=files)
        if response.status_code == 200:
            cid = response.json()["value"]["cid"]
            url = f"https://ipfs.io/ipfs/{cid}"
            print(f"✅ CID: {cid}")
            with open(FICHIER_CID, "a") as f:
                f.write(f"{cid} | {signal['dateCreated']}\n")
            with open(FICHIER_URL, "a") as f:
                f.write(f"{url}\n")
        else:
            print(f"❌ Erreur NFT.Storage: {response.status_code} => {response.text}")
    except Exception as e:
        print(f"❌ Exception envoi NFT.Storage : {e}")

if __name__ == "__main__":
    print("🚀 Surbot PRO en route...")
    while True:
        signal = generer_signal()
        enregistrer_local(signal)
        publier_nftstorage(signal)
        print(f"💾 Signal envoyé : {signal['identifier']} à {signal['dateCreated']}")
        time.sleep(INTERVALLE_MINUTES * 60)
