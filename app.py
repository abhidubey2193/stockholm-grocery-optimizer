"""Small localhost-only interface. No external price scraping."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from optimizer import Price, best_basket

HTML = """<!doctype html><html lang="en"><meta charset="utf-8">
<title>Stockholm Grocery Optimizer</title>
<h1>Grocery Basket Optimizer</h1>
<p>Enter items and illustrative or user-verified prices (SEK). No live retail data.</p>
<label>Items (comma-separated): <input id="items" value="milk,bread"></label>
<p><textarea id="prices" rows="9" cols="95">[{"store":"Willys Sundbyberg Esplanaden","item":"milk","sek":16.9},{"store":"ICA Maxi Solna","item":"milk","sek":15.9},{"store":"Willys Sundbyberg Esplanaden","item":"bread","sek":25},{"store":"ICA Maxi Solna","item":"bread","sek":29}]</textarea></p>
<label>Additional store penalty (SEK) <input id="penalty" type="number" value="15" min="0"></label>
<button onclick="optimize()">Optimize</button><pre id="result"></pre>
<script>
async function optimize(){
try{
const response=await fetch('/optimize',{method:'POST',headers:{'Content-Type':'application/json'},
body:JSON.stringify({items:document.getElementById('items').value.split(','),
prices:JSON.parse(document.getElementById('prices').value),penalty:Number(document.getElementById('penalty').value)})});
document.getElementById('result').textContent=JSON.stringify(await response.json(),null,2);
}catch(e){document.getElementById('result').textContent=String(e)}
}
</script></html>"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return
        data = HTML.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        if self.path != "/optimize":
            self.send_error(404)
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size <= 0 or size > 100000:
                raise ValueError("Invalid payload size")
            payload = json.loads(self.rfile.read(size))
            result = best_basket(payload["items"], [Price(**p) for p in payload["prices"]],
                                 float(payload.get("penalty", 15)))
            data = json.dumps(result).encode()
            status = 200
        except (ValueError, TypeError, KeyError) as e:
            data = json.dumps({"error": str(e)}).encode()
            status = 400
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

if __name__ == "__main__":
    print("Open http://127.0.0.1:8085")
    ThreadingHTTPServer(("127.0.0.1", 8085), Handler).serve_forever()
