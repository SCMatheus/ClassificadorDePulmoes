# USAGE
# Start the server:
# 	python run_keras_server.py
# Submit a request via cURL:
# 	curl -X POST -F image=@dog.jpg 'http://localhost:5000/predict'
# Submita a request via Python:
#	python simple_request.py

# import the necessary packages
import cv2
from keras.models import load_model
import numpy as np
from flask import json
import flask
from flask_cors import CORS

# initialize our Flask application and the Keras model
app = flask.Flask(__name__)
CORS(app)
model = None

def load():
    global model
	# load the pre-trained Keras model (here we are using a model
	# pre-trained on ImageNet and provided by Keras, but you can
	# substitute in your own networks just as easily)
    
    model = load_model("Model_xRay")

def prepare_image(image, target):

    img = cv2.resize(image, (64,64))
    img = img.astype(np.float32)/255.
    img = np.expand_dims(img, axis=0)
    img = np.expand_dims(img, -1)
    # return the processed image
    return img


# Now, we can predict the results. 
@app.route("/predict", methods =["POST"]) 
def predict(): 
    data = {} # dictionary to store result 
    data["success"] = False
  
    # Check if image was properly sent to our endpoint 
    if flask.request.method == "POST": 
        if flask.request.files.get("image"): 
            filestr  = flask.request.files["image"].read() 
            npimg = np.fromstring(filestr, np.uint8)
            image = cv2.imdecode(npimg, cv2.IMREAD_GRAYSCALE)
            # Resize it to 224x224 pixels  
            # (required input dimensions for ResNet) 
            image = prepare_image(image, target =(64, 64)) 
  
            # Predict ! global preds, results     
        
            preds = model.predict(image) 
            
            porcentagem = round(preds[0][0]*100,2)
            
            resultadoFinal = (preds > 0.5)
            
            data["predictions"] = [] 
            
            if resultadoFinal[0][0] == True:
                data["predictions"] = "Chance de "+str(porcentagem)+"% de estar com Pneumonia"
            else:
                data["predictions"] = "Chance de "+str(100-porcentagem)+"% de estar Normal"

  
  
            data["success"] = True
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    # return JSON response 
    return response
  

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
	print(("* Loading Keras model and Flask starting server..."
		"please wait until server has fully started"))
	load()
	app.run(debug=True, use_reloader=False)
