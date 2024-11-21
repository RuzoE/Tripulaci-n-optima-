from flask import Flask, request, jsonify, render_template
from pulp import LpProblem, LpVariable, LpMinimize

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/optimizar', methods=['POST'])
def optimizar():
    data = request.json
    
    # Extraer datos del formulario
    vuelos_cortos = int(data["vuelos_cortos"])
    vuelos_medios = int(data["vuelos_medios"])
    vuelos_largos = int(data["vuelos_largos"])
    duracion_corto = int(data["duracion_corto"])
    duracion_medio = int(data["duracion_medio"])
    duracion_largo = int(data["duracion_largo"])
    costo_piloto = int(data["costo_piloto"])
    costo_cabina = int(data["costo_cabina"])
    
    # Definir el problema de optimización
    problema = LpProblem("Optimización_Tripulaciones", LpMinimize)
    
    # Variables de decisión
    pilotos_corto = LpVariable("Pilotos_Corto", lowBound=0, cat='Integer')
    cabina_corto = LpVariable("Cabina_Corto", lowBound=0, cat='Integer')
    pilotos_medio = LpVariable("Pilotos_Medio", lowBound=0, cat='Integer')
    cabina_medio = LpVariable("Cabina_Medio", lowBound=0, cat='Integer')
    pilotos_largo = LpVariable("Pilotos_Largo", lowBound=0, cat='Integer')
    cabina_largo = LpVariable("Cabina_Largo", lowBound=0, cat='Integer')
    
    # Función objetivo
    problema += (
        vuelos_cortos * (costo_piloto * pilotos_corto * duracion_corto + costo_cabina * cabina_corto * duracion_corto) +
        vuelos_medios * (costo_piloto * pilotos_medio * duracion_medio + costo_cabina * cabina_medio * duracion_medio) +
        vuelos_largos * (costo_piloto * pilotos_largo * duracion_largo + costo_cabina * cabina_largo * duracion_largo)
    )
    
    # Ajuste de restricciones para valores positivos
    if vuelos_cortos > 0:
        problema += pilotos_corto >= 2
        problema += cabina_corto >= 3
    if vuelos_medios > 0:
        problema += pilotos_medio >= 3
        problema += cabina_medio >= 4
    if vuelos_largos > 0:
        problema += pilotos_largo >= 4
        problema += cabina_largo >= 6
    
    # Resolver el problema
    problema.solve()

    # Resultado
    resultado = {
        "Pilotos para vuelos cortos": pilotos_corto.varValue if pilotos_corto.varValue is not None else 0,
        "Personal de cabina para vuelos cortos": cabina_corto.varValue if cabina_corto.varValue is not None else 0,
        "Pilotos para vuelos medios": pilotos_medio.varValue if pilotos_medio.varValue is not None else 0,
        "Personal de cabina para vuelos medios": cabina_medio.varValue if cabina_medio.varValue is not None else 0,
        "Pilotos para vuelos largos": pilotos_largo.varValue if pilotos_largo.varValue is not None else 0,
        "Personal de cabina para vuelos largos": cabina_largo.varValue if cabina_largo.varValue is not None else 0,
        "Costo total diario": problema.objective.value() if problema.objective.value() is not None else 0
    }

    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
