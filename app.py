from flask import Flask, render_template, jsonify, request
import random
import json

app = Flask(__name__)

# Lista de objetos y sus probabilidades 
# Cambiar a un archivo .Json 

with open('cartas.json', 'r') as f:
    personajes = json.load(f)
    # Endpoint para eliminar un objeto seleccionado
    @app.route('/eliminar', methods=['POST'])
    def eliminar():
        nombre = request.json.get('nombre')
        if nombre in objetos_seleccionados:
            objetos_seleccionados.remove(nombre)
            return jsonify({'status': 'success', 'message': f'{nombre} eliminado.'})
        else:
            return jsonify({'status': 'error', 'message': f'{nombre} no encontrado.'})
    
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
