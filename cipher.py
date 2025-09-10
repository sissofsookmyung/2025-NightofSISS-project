from flask import Flask, url_for, request, jsonify
import caesar
import vigenere
import polybius
import railfence

app = Flask(__name__)


def template(id, input_text=None):
    return f'''<!doctype html>
    <html>
    <head>
        <title>Classical Crypto Playground</title>
        <meta charset="utf-8">
        <link rel="stylesheet" href="{url_for('static', filename='style.css')}">
        <script src="{url_for('static', filename='buttonEvent.js')}"></script>
    </head>
        <body data-current="{id}"> <!--id=index, ceasar, ... 등 색상 변경용(지금이 어떤 페이지인지 표시)-->
            <h1><a class="title" href="/">Classical Crypto Playground</a></h1>

            <div id="cipherBoxes">
            <a class="cipherBox" href="/caesar/" data-id="caesar">Caesar</a>
            <a class="cipherBox" href="/vigenere/" data-id="vigenere">Vigenere</a>
            <a class="cipherBox" href="/polybius/" data-id="polybius">Polybius</a>
            <a class="cipherBox" href="/railfence/" data-id="railfence">Rail Fence</a>
            </div>

            <div id="encORdecBoxes">
            <input class="encORdec" type="button" value="ENC"> <!--onclick=함수 나중에 추가(색상 변경+readonly해제 후 입력받는 문구 넣기+입력받기)-->
            <input class="encORdec" type="button" value="DEC">
            </div>


            <form action="{id}/" method="POST">
                <textarea id="inputBox" name="inputBox" placeholder="{input_text}" readonly></textarea><br>
                <textarea id="keyBox" name="keyBox" readonly></textarea><br>
                <div class="button-container">
                <input type="submit" value="Go" disabled>
                </div>
            </form>
            <br>
            <br>
            <textarea name="outputBox" readonly></textarea>
            <br><br><br>

        </body>
    </html>
    '''

@app.route('/')
def index():
    return template('index', 'Select a Cipher.')

@app.route('/caesar/', methods=["GET", "POST"])
def caesar_page():
    if request.method == "POST":
        data = request.get_json()
        msg = data.get("text", "")
        key = data.get("key", "")
        mode = data.get("mode", "")

        result = caesar.caesar(msg, key, mode)
        if not result:
            return jsonify({"result": "Error: invalid input"})
        return jsonify({"result": result})

    return template('caesar', 'Select either ENC or DEC.')

@app.route('/vigenere/', methods=["GET", "POST"])
def vigenere_route():
    if request.method == "POST":
        data = request.get_json()
        text = data.get("text", "")
        key = data.get("key", "")
        mode = data.get("mode", "")

        if mode == "ENC":
            result = vigenere.vigenere_encrypt(text, key)
        else:
            result = vigenere.vigenere_decrypt(text, key)

        return jsonify({"result": result})

    return template('vigenere', 'Select either ENC or DEC.')

@app.route('/polybius/', methods=["GET", "POST"])
def polybius_route():
    if request.method == "POST":
        data = request.get_json()
        text = data.get("text", "")
        mode = data.get("mode", "")

        if mode == "ENC":
            result = polybius.polybius_enc(text)
        elif mode == "DEC":
            result = polybius.polybius_dec(text)
        else:
            result = "Error: invalid mode"

        return jsonify({"result": result})

    return template('polybius', 'Select either ENC or DEC.')

@app.route('/railfence/', methods=["GET", "POST"])
def railfence_route():
    if request.method == "POST":
        data = request.get_json()
        text = data.get("text", "")
        key = data.get("key", "")
        mode = data.get("mode", "")

        try:
            key = int(key)
        except ValueError:
            return jsonify({"result": "Error: key must be a number"})

        if mode == "ENC":
            result = railfence.railfence_enc(text, key)
        elif mode == "DEC":
            result = railfence.railfence_dec(text, key)
        else:
            result = "Error: invalid mode"

        return jsonify({"result": result})

    return template('railfence', 'Select either ENC or DEC.')



if __name__ == "__main__":
    app.run(debug=True)