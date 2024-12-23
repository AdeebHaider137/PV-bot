from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook/dailyupdate', methods=['POST'])
def handle_dailyupdate():
    try:
        data = request.json
        print("Received Webhook Data:", data)
        return "OK", 200
    except Exception as e:
        print("Error:", str(e))
        return "Error processing webhook", 500

if __name__ == "__main__":
    app.run(port=8000)
