# Inicie o servidor:
# python xRay_server.py
# Envie uma solicitação via cURL:
# Submeta uma solicitação

# importar os pacotes necessários
import cv2
from keras.models import load_model
import numpy as np
from flask import json
import flask
from flask_cors import CORS


# inicialize nosso aplicativo Flask e o modelo Keras
app = flask.Flask(__name__)
CORS(app)
model = None

def load():
    global model
    # carregar o modelo Keras pré-treinado (aqui estamos usando um modelo
    # cronstruido e treinado para o problema dos pulmões)
    
    model = load_model("Model_xRay")

def prepare_image(image, target):

    img = cv2.resize(image, (64,64))
    img = img.astype(np.float32)/255.
    img = np.expand_dims(img, axis=0)
    img = np.expand_dims(img, -1)
    # retorna a imagem processada
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
            # Resize da imagem para 64x64 pixels  
            # (É a dimensão de rentrada exigida pela rede) 
            image = prepare_image(image, target =(64, 64)) 
      
        
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
    # retorna a resposta Json
    return response
  
# se esse for o principal thread de execução, primeiro carregue o modelo e
# depois inicie o servidor
if __name__ == "__main__":
	print(("* Loading Keras model and Flask starting server..."
		"please wait until server has fully started"))
	load()
	app.run(debug=True, use_reloader=False)
