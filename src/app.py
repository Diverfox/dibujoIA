import os
import cv2
import numpy as np
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
UPLOAD_FOLDER = "src/static/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    if "imagen" not in request.files:
        return redirect(request.url)
    
    archivo = request.files["imagen"]
    
    if archivo.filename == "":
        return redirect(request.url)
    
    if archivo:
        ruta_imagen = os.path.join(app.config["UPLOAD_FOLDER"], "imagen_original.png")
        archivo.save(ruta_imagen)

        # Procesar la imagen con OpenCV
        imagen = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)  # Convertir a escala de grises
        imagen = cv2.GaussianBlur(imagen, (5, 5), 0)  # Aplicar desenfoque
        _, imagen_bin = cv2.threshold(imagen, 128, 255, cv2.THRESH_BINARY)  # Umbralizar la imagen
        
        # Guardar la imagen procesada
        ruta_procesada = os.path.join(app.config["UPLOAD_FOLDER"], "imagen_procesada.png")
        cv2.imwrite(ruta_procesada, imagen_bin)

        return render_template("index.html", resultado="Imagen procesada correctamente")

if __name__ == '__main__':
    app.run(debug=True)
