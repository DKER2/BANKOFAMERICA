from flask import Flask, request, json, jsonify
from flask_cors import CORS, cross_origin
from Components.ReportGenerator import reportGenerator
from Components.PricingEngine import PricingEngine
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

pricingEngine = PricingEngine()
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/reportGenerator')
# ‘/’ URL is bound with hello_world() function.
def reportGenerator():
    print("a")
    #reportGenerator()

@app.post('/priceEngine')
# ‘/’ URL is bound with hello_world() function.
def priceEngine():
    print(json.loads(request.data))
    data = pricingEngine.processRequest(json.loads(request.data))
    return jsonify(data)

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    cors = CORS(app, expose_headers='Authorization')
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.run(debug=True, host="0.0.0.0", use_reloader=False, port=8080)