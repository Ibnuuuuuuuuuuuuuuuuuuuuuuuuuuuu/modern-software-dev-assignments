import httpx
import os
import base64
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
AUTH_URL = "https://developer.spotify.com/documentation/web-api/tutorials/getting-started"

async def test():
    # Membuat string Base64 dari Client ID dan Secret
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_base64 = base64.b64encode(auth_str.encode()).decode()

    print(f"--- Memulai Script Test Standar ---")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                AUTH_URL,
                # Mencoba mengirim data sesuai standar OAuth2
                data={"grant_type": "client_credentials"},
                headers={
                    "Authorization": f"Basic {auth_base64}",
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                timeout=10.0
            )
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print("BERHASIL! Token didapat.")
            else:
                print(f"Gagal lagi. Server menjawab: {response.text[:200]}...")
        except Exception as e:
            print(f"Error Koneksi: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test())