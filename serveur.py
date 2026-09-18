"""Serveur local du workspace Allemand.

Sert les fichiers (comme `python -m http.server`) et ajoute une route
`/config.json` qui expose l'adresse IP LAN du PC, afin que l'interface
puisse afficher le lien pour le téléphone.

Aucune dépendance : bibliothèque standard uniquement.
"""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import socket

PORT = 8080


def lan_ip():
    """IP locale utilisée vers le réseau (aucun paquet n'est émis)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/config.json":
            ip = lan_ip()
            body = json.dumps({
                "port": PORT,
                "ip": ip,
                "urlTelephone": f"http://{ip}:{PORT}/site/index.html",
            }).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return
        return super().do_GET()


if __name__ == "__main__":
    ip = lan_ip()
    print(f"Serveur du workspace Allemand - Ctrl+C pour arreter")
    print(f"PC       : http://localhost:{PORT}/site/")
    print(f"Telephone: http://{ip}:{PORT}/site/")
    print("Premier lancement : autoriser les reseaux prives si le pare-feu le demande.")
    ThreadingHTTPServer(("", PORT), Handler).serve_forever()
