from flask import Flask, render_template, request
import socket

app = Flask(__name__)

def scan_ports(target, start_port, end_port):
    open_ports = []

    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        return []

    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)   # fast timeout

        try:
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                open_ports.append(port)
        except:
            pass
        finally:
            sock.close()

    return open_ports

@app.route("/", methods=["GET", "POST"])
def home():
    open_ports = None
    scanned = False

    if request.method == "POST":
        scanned = True
        target = request.form["target"]
        start_port = int(request.form["start_port"])
        end_port = int(request.form["end_port"])

        # Safety limit
        if end_port - start_port > 50:
            open_ports = []
        else:
            open_ports = scan_ports(target, start_port, end_port)

    return render_template(
        "index.html",
        open_ports=open_ports,
        scanned=scanned
    )

if __name__ == "__main__":
    app.run(debug=True)
