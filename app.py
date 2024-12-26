from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Lista de objetos y sus probabilidades
personajes = [
    {"nombre": "Silla", "probabilidad": 0.100, "imagen": "imgs/sillaComun.png"},
    {"nombre": "Llavero", "probabilidad": 0.10, "imagen": "imgs/llavero.png"},
    {"nombre": "Beca", "probabilidad": 0.1, "imagen": "imgs/beca.png"},
    {"nombre": "Programador Top", "probabilidad": 0.4, "imagen": "imgs/programador_top.png"},
]

# Lista para almacenar los objetos seleccionados
objetos_seleccionados = []

@app.route('/')
def index():
    return render_template('jugar.html')

@app.route('/jugar')
def jugar():
    return render_template('jugar.html')

@app.route('/alazar', methods=['POST'])
def alazar():
    # Extraer nombres y probabilidades en listas separadas
    nombres = [p["nombre"] for p in personajes]
    probabilidades = [p["probabilidad"] for p in personajes]

    # Seleccionar un personaje basado en la probabilidad
    resultado = random.choices(nombres, probabilidades)[0]

    # Agregar el objeto a la lista de objetos seleccionados
    objetos_seleccionados.append(resultado)

    # Obtener el objeto seleccionado
    objeto_seleccionado = next(p for p in personajes if p["nombre"] == resultado)

    return jsonify({
        'nombre': resultado,
        'imagen': objeto_seleccionado["imagen"]
    })

@app.route('/ver_objetos')
def ver_objetos():
    # Crear una lista de diccionarios con nombre e imagen de los objetos seleccionados
    objetos_con_imagen = []
    for objeto in objetos_seleccionados:
        objeto_info = next(p for p in personajes if p["nombre"] == objeto)
        objetos_con_imagen.append({
            'nombre': objeto_info["nombre"],
            'imagen': objeto_info["imagen"]
        })
    
    return render_template('ver_objetos.html', objetos=objetos_con_imagen)


@app.route('/descripcion')
def descripcion():
    return render_template('descripcion.html')

if __name__ == '__main__':
    app.run(debug=True)
