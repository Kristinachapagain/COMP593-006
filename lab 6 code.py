import os
import hashlib
import requests
import subprocess

def get_expected_sha256():
    # Get SHA256 value 
    hash_URL = f"{URL}.sha256"
    URL_response = requests.get(hash_URL)
    if URL_response.status_code == 200:
        expected_HASH = URL_response.content.split()[0].decode("utf-8")
    else:
        print("Failed to get SHA 256 hash")
        exit()
    return expected_HASH

def download_installer():
    # Download VLC installer
    URL_response = requests.get(URL, stream=True)
    if URL_response.status_code == 200:
        return URL_response
    else:
        print("Downloading VLC installer Failed")
        exit()

def installer_ok(installer_data, expected_sha256):
    FILE_hash = hashlib.sha256(installer_data.content).hexdigest()
    if FILE_hash == expected_sha256:
        print("Successfully Verified Installer")
        return True
    else:
        print("Failed Verification of Installer")
        exit()

def save_installer(installer_data):
    with open(filename, "wb") as f:
        for chunk in installer_data.iter_content(4096):
            f.write(chunk)
    print("Downloaded VLC installer Successfully")
    filepath = f"./{filename}"
    return filepath

def run_installer(installer_path):
    subprocess.run([installer_path, "/S"], check=True)
    print("Successfully installed VLC")

def delete_installer(installer_path):
    # Remove(Delete) VLC Installer from system
    os.remove(installer_path)
    print("Successfully deleted VLC installer")

def main():
    
    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()
    
    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):
        
        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)
        
        # Silently run the VLC installer
        run_installer(installer_path)
        
        # Delete the VLC installer from disk
        delete_installer(installer_path)

if __name__ == "__main__":

    # Version of VLC Media Player
    version = "3.0.18"

    # Define Operating System 
    if os.name == "nt":
        URL = f"https://get.videolan.org/vlc/{version}/win64/vlc-{version}-win64.exe"
        filename = f"vlc-{version}-win64.exe"
    elif os.name == "posix":
        URL = f"https://get.videolan.org/vlc/{version}/macosx/vlc-{version}-arm64.dmg"
        filename = f"vlc-{version}-arm64.dmg"
    else:
        print("Operating system not supported")
        exit()

    main()
