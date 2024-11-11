
from flask import Flask, request, jsonify
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import io

def image_to_model(img):
    return img


app = Flask(__name__)

chás = {
    "Alecrim": {
        "nome_cientifico": "Rosmarinus officinalis",
        "beneficios": [
            "Propriedades antioxidantes e anti-inflamatórias",
            "Melhora da digestão",
            "Alívio de dores de cabeça",
            "Redução do estresse e ansiedade",
            "Melhora da memória e concentração"
        ]
    },
    "Camomila": {
        "nome_cientifico": "Matricaria chamomilla",
        "beneficios": [
            "Propriedades calmantes",
            "Redução da ansiedade",
            "Melhora da qualidade do sono",
            "Alívio de cólicas menstruais",
            "Auxílio na digestão",
            "Alívio de irritações na pele e inflamações"
        ]
    },
    "Erva-doce": {
        "nome_cientifico": "Foeniculum vulgare",
        "beneficios": [
            "Alívio de problemas digestivos, como inchaço, gases e indigestão",
            "Redução da tosse",
            "Alívio de cólicas em bebês",
            "Propriedades antioxidantes que promovem a saúde geral"
        ]
    },
    "Hortelã": {
        "nome_cientifico": "Mentha spicata",
        "beneficios": [
            "Propriedades digestivas",
            "Alívio de náuseas, dores de estômago e indigestão",
            "Alívio de sintomas de resfriados",
            "Melhora da respiração",
            "Efeito refrescante e relaxante"
        ]
    },
    "Jambu": {
        "nome_cientifico": "Acmella oleracea",
        "beneficios": [
            "Propriedades anestésicas que aliviam dores de dente e inflamações bucais",
            "Estimula o sistema imunológico",
            "Melhora da circulação sanguínea",
            "Efeitos anti-inflamatórios"
        ]
    },
    "Malva": {
        "nome_cientifico": "Malva sylvestris",
        "beneficios": [
            "Alívio de irritações na garganta, tosse e inflamações das vias respiratórias",
            "Propriedades calmantes que ajudam no tratamento de problemas digestivos",
            "Efeitos emolientes que aliviam inflamações na pele"
        ]
    }
}

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    class_labels = ['Alecrim', 'Camomila', 'Erva-doce', 'Jambu', 'Malva', 'Hortelã']
    img_size = 224
    model = load_model("modelo_cnn.h5")
    
    img_bytes = io.BytesIO(file.read())
    img = image.load_img(img_bytes, target_size=(img_size, img_size))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.
    
    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction)
    predicted_class_name = class_labels[predicted_class]
    
    chá_info = chás.get(predicted_class_name)
    
    if chá_info:
        return jsonify({
            "classe": predicted_class_name,
            "nome_cientifico": chá_info["nome_cientifico"],
            "beneficios": chá_info["beneficios"]
        })
    else:
        return jsonify({"error": "Class not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
