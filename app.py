from flask import Flask, render_template, request
import requests
import json
#hkh

app = Flask(__name__)

HTTP_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        url = request.form.get("url")
        raw_headers = request.form.get("headers", "")
        body = request.form.get("body", "")
        auth_type = request.form.get("auth_type")
        username = request.form.get("username")
        password = request.form.get("password")
        token = request.form.get("token")

        # Parse headers
        headers = {}
        for line in raw_headers.strip().splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                headers[key.strip()] = value.strip()

        # Handle Auth
        auth = None
        if auth_type == "basic" and username and password:
            auth = (username, password)
        elif auth_type == "bearer" and token:
            headers["Authorization"] = f"Bearer {token}"

        # Try JSON body
        try:
            json_body = json.loads(body) if body else None
        except:
            json_body = None

        # Test each method
        for method in HTTP_METHODS:
            try:
                if method in ["POST", "PUT", "PATCH"]:
                    res = requests.request(method, url, headers=headers, auth=auth,
                                           json=json_body if isinstance(json_body, dict) else None,
                                           data=body if not json_body else None)
                else:
                    res = requests.request(method, url, headers=headers, auth=auth)

                results.append({
                    "method": method,
                    "status_code": res.status_code,
                    "allowed": res.status_code < 400,
                    "response": res.text[:300]
                })
            except Exception as e:
                results.append({
                    "method": method,
                    "status_code": "ERROR",
                    "allowed": False,
                    "response": str(e)
                })

    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)
