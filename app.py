from flask import Flask, request, jsonify, render_template
from pulp import LpProblem, LpVariable, LpMinimize

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/optimizar', methods=['POST'])
def optimizar():
    # Extraer datos del formulario
    data = request.json
    print("Datos recibidos del formulario:", data)
    
    vuelos_cortos = int(data.get("vuelos_cortos", 0))
    vuelos_medios = int(data.get("vuelos_medios", 0))
    vuelos_largos = int(data.get("vuelos_largos", 0))
    duracion_corto = int(data.get("duracion_corto", 0))
    duracion_medio = int(data.get("duracion_medio", 0))
    duracion_largo = int(data.get("duracion_largo", 0))
    costo_piloto = int(data.get("costo_piloto", 0))
    costo_cabina = int(data.get("costo_cabina", 0))

    # Verificar que los datos sean correctos
    print("Vuelos cortos:", vuelos_cortos)
    print("Duración vuelos cortos:", duracion_corto)
    print("Costo piloto:", costo_piloto)
    print("Costo cabina:", costo_cabina)

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


    # Restricciones dinámicas basadas en los vuelos diarios
    problema += pilotos_corto >= 2 * vuelos_cortos
    problema += cabina_corto >= 3 * vuelos_cortos
    problema += pilotos_medio >= 3 * vuelos_medios
    problema += cabina_medio >= 4 * vuelos_medios
    problema += pilotos_largo >= 4 * vuelos_largos
    problema += cabina_largo >= 6 * vuelos_largos
    
    # Resolver el problema
    problema.solve()

    # Verificar variables de decisión
    print("Pilotos cortos asignados:", pilotos_corto.varValue)
    print("Cabina cortos asignados:", cabina_corto.varValue)
    print("Pilotos medios asignados:", pilotos_medio.varValue)
    print("Cabina medios asignados:", cabina_medio.varValue)
    print("Pilotos largos asignados:", pilotos_largo.varValue)
    print("Cabina largos asignados:", cabina_largo.varValue)

    # Resultado
    resultado = {
    "Pilotos para vuelos cortos": pilotos_corto.varValue or 0,
    "Personal de cabina para vuelos cortos": cabina_corto.varValue or 0,
    "Costo pilotos cortos": (vuelos_cortos or 0) * (pilotos_corto.varValue or 0) * (duracion_corto or 0) * (costo_piloto or 0),
    "Costo cabina cortos": (vuelos_cortos or 0) * (cabina_corto.varValue or 0) * (duracion_corto or 0) * (costo_cabina or 0),
    "Pilotos para vuelos medios": pilotos_medio.varValue or 0,
    "Personal de cabina para vuelos medios": cabina_medio.varValue or 0,
    "Costo pilotos medios": (vuelos_medios or 0) * (pilotos_medio.varValue or 0) * (duracion_medio or 0) * (costo_piloto or 0),
    "Costo cabina medios": (vuelos_medios or 0) * (cabina_medio.varValue or 0) * (duracion_medio or 0) * (costo_cabina or 0),
    "Pilotos para vuelos largos": pilotos_largo.varValue or 0,
    "Personal de cabina para vuelos largos": cabina_largo.varValue or 0,
    "Costo pilotos largos": (vuelos_largos or 0) * (pilotos_largo.varValue or 0) * (duracion_largo or 0) * (costo_piloto or 0),
    "Costo cabina largos": (vuelos_largos or 0) * (cabina_largo.varValue or 0) * (duracion_largo or 0) * (costo_cabina or 0),
    "Costo total diario": problema.objective.value() or 0,
    "duracion_corto": duracion_corto,
    "duracion_medio": duracion_medio,
    "duracion_largo": duracion_largo,
    "costo_piloto": costo_piloto,
    "costo_cabina": costo_cabina
}

    # Imprimir resultado final para depuración
    print("Resultado final:", resultado)

    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
