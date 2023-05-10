from flask import Flask, request
import py_interface

app = Flask(__name__)

@app.route('/wtn', methods=['GET'])
def wtn():
    concept = request.args.get('concept')
    language = request.args.get('language')
    output = py_interface.main(concept, language)
    return output

if __name__ == '__main__':
    app.run()
