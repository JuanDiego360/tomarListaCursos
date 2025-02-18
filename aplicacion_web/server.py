from flask import Flask, request, jsonify
import os
import csv
from datetime import datetime
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # Esto permite las peticiones desde nuestro frontend

# Asegurarse de que existen los directorios y archivos necesarios
if not os.path.exists('listas'):
    os.makedirs('listas')

if not os.path.exists('materias_dictadas.txt'):
    with open('materias_dictadas.txt', 'w', encoding='utf-8') as f:
        pass

@app.route('/crear-lista', methods=['POST'])
def crear_lista():
    try:
        data = request.json
        grado = data['grado']
        alumnos = data['alumnos']
        
        # Generar nombre de archivo con timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"listas/{grado}_{timestamp}.csv"
        
        # Crear DataFrame con los alumnos
        df = pd.DataFrame({
            'alumnos': alumnos
        })
        
        # Guardar en archivo CSV
        df.to_csv(filename, index=False)
        
        return jsonify({"mensaje": "Lista guardada exitosamente", "archivo": filename}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/obtener-listas', methods=['GET'])
def obtener_listas():
    try:
        listas = []
        for filename in os.listdir('listas'):
            # Solo procesar archivos CSV que no contengan guión (no son archivos de materias)
            if filename.endswith('.csv') and '-' not in filename:
                file_path = os.path.join('listas', filename)
                grado = filename.split('_')[0]  # Obtener el nombre del grado del archivo
                
                # Leer el archivo CSV con pandas
                df = pd.read_csv(file_path)
                alumnos = df['alumnos'].tolist()
                
                # Obtener las fechas de asistencia (todas las columnas excepto 'alumnos')
                fechas_asistencia = [col for col in df.columns if col != 'alumnos']
                
                # Calcular estadísticas por alumno
                estadisticas_alumnos = []
                for i, alumno in enumerate(alumnos):
                    faltas = 0
                    fechas_falta = []
                    for fecha in fechas_asistencia:
                        if df.loc[i, fecha] == 'F':
                            faltas += 1
                            fechas_falta.append(fecha)
                    
                    estadisticas_alumnos.append({
                        "nombre": alumno,
                        "faltas": faltas,
                        "fechasFalta": fechas_falta
                    })
                
                listas.append({
                    "grado": grado,
                    "archivo": filename,
                    "alumnos": alumnos,
                    "fechasAsistencia": fechas_asistencia,
                    "estadisticas": estadisticas_alumnos,
                    "fechaCreacion": datetime.fromtimestamp(os.path.getctime(file_path)).isoformat()
                })
        
        return jsonify(listas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/guardar-asistencia', methods=['POST'])
def guardar_asistencia():
    try:
        data = request.json
        archivo = data['archivo']
        fecha = data['fecha']
        asistencias = data['asistencias']  # Lista de booleanos
        
        file_path = os.path.join('listas', archivo)
        
        # Leer el archivo CSV existente
        df = pd.read_csv(file_path)
        
        # Agregar nueva columna con la fecha y las asistencias
        df[fecha] = asistencias
        
        # Guardar el archivo actualizado
        df.to_csv(file_path, index=False)
        
        return jsonify({"mensaje": "Asistencia guardada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/crear-materia', methods=['POST'])
def crear_materia():
    try:
        data = request.json
        grado = data['grado']
        materia = data['materia']
        archivo_base = data['archivoBase']
        
        # Crear nombre del nuevo archivo
        nombre_base = os.path.splitext(archivo_base)[0]
        nuevo_archivo = f"{nombre_base}-{materia}.csv"
        ruta_archivo = os.path.join('listas', nuevo_archivo)
        
        # Verificar si ya existe el archivo
        if os.path.exists(ruta_archivo):
            return jsonify({"error": "Ya existe una lista para esta materia"}), 409
        
        # Leer la lista de alumnos del grado
        df_base = pd.read_csv(os.path.join('listas', archivo_base))
        alumnos = df_base['alumnos'].tolist()
        
        # Crear el nuevo archivo de la materia
        df_materia = pd.DataFrame({'alumnos': alumnos})
        df_materia.to_csv(ruta_archivo, index=False)
        
        # Registrar la materia en materias_dictadas.txt
        with open('materias_dictadas.txt', 'a', encoding='utf-8') as file:
            file.write(nuevo_archivo + '\n')
        
        return jsonify({
            "mensaje": "Materia creada exitosamente",
            "archivo": nuevo_archivo
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/obtener-materias', methods=['GET'])
def obtener_materias():
    try:
        if not os.path.exists('materias_dictadas.txt'):
            return jsonify([]), 200
            
        with open('materias_dictadas.txt', 'r', encoding='utf-8') as file:
            materias = [linea.strip() for linea in file.readlines() if linea.strip()]
        
        # Obtener información detallada de cada materia
        materias_info = []
        for archivo in materias:
            try:
                ruta_archivo = os.path.join('listas', archivo)
                if os.path.exists(ruta_archivo):
                    df = pd.read_csv(ruta_archivo)
                    # Obtener nombre de la materia del archivo
                    nombre_base = os.path.splitext(archivo)[0]
                    grado, materia = nombre_base.split('-', 1)
                    
                    # Obtener columnas de actividades (todas excepto 'alumnos')
                    actividades = [col for col in df.columns if col != 'alumnos']
                    
                    materias_info.append({
                        "archivo": archivo,
                        "grado": grado,
                        "materia": materia,
                        "actividades": actividades
                    })
            except Exception:
                continue
        
        return jsonify(materias_info), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/guardar-actividad', methods=['POST'])
def guardar_actividad():
    try:
        data = request.json
        archivo = data['archivo']
        fecha = data['fecha']
        actividad = data['actividad']
        notas = data['notas']
        porcentaje = data.get('porcentaje', None)
        escala = data.get('escala', 5)
        
        ruta_archivo = os.path.join('listas', archivo)
        
        if not os.path.exists(ruta_archivo):
            return jsonify({"error": "No se encontró el archivo de la materia"}), 404
        
        # Leer el archivo CSV existente
        df = pd.read_csv(ruta_archivo)
        
        # Crear nombre de columna para la actividad
        nombre_columna = f"{fecha}-{actividad}"
        if porcentaje:
            nombre_columna += f"-{porcentaje}%"
        if escala != 5:
            nombre_columna += f"-{escala}"
        
        # Verificar si ya existe la actividad
        if nombre_columna in df.columns:
            return jsonify({"error": "Ya existe una actividad con esta fecha"}), 409
        
        # Agregar nueva columna con las notas
        df[nombre_columna] = notas
        
        # Guardar el archivo actualizado
        df.to_csv(ruta_archivo, index=False)
        
        return jsonify({"mensaje": "Actividad guardada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/obtener-estadisticas-materia', methods=['GET'])
def obtener_estadisticas_materia():
    try:
        archivo = request.args.get('archivo')
        if not archivo:
            return jsonify({"error": "No se especificó el archivo"}), 400

        ruta_archivo = os.path.join('listas', archivo)
        if not os.path.exists(ruta_archivo):
            return jsonify({"error": "No se encontró el archivo"}), 404

        # Leer el archivo CSV
        df = pd.read_csv(ruta_archivo)
        
        # Obtener lista de actividades (todas las columnas excepto 'alumnos')
        actividades = [col for col in df.columns if col != 'alumnos']
        
        # Procesar cada actividad para obtener porcentajes y escalas
        actividades_info = []
        for actividad in actividades:
            try:
                fecha, nombre = actividad.split('-', 1)
                info = {
                    'nombre': nombre.strip(),
                    'fecha': fecha.strip(),
                    'porcentaje': None,
                    'escala': 5
                }
                
                # Buscar porcentaje y escala en el nombre si existen
                if '%' in nombre:
                    porcentaje = nombre.split('%')[0].split()[-1]
                    info['porcentaje'] = float(porcentaje)
                    nombre = nombre.replace(f"{porcentaje}%", "").strip()
                
                if '/' in nombre:
                    escala = nombre.split('/')[-1].split()[0]
                    info['escala'] = float(escala)
                    nombre = nombre.replace(f"/{escala}", "").strip()
                
                info['nombre'] = nombre  # Actualizar nombre sin porcentaje/escala
                actividades_info.append(info)
            except Exception as e:
                print(f"Error procesando actividad {actividad}: {str(e)}")
                continue
        
        # Calcular notas finales
        estudiantes = []
        for index, row in df.iterrows():
            notas = []
            nota_final = 0
            total_porcentaje = 0
            
            for actividad, info in zip(actividades, actividades_info):
                try:
                    nota = float(row[actividad])
                    if info['escala'] != 5:
                        nota = (nota * 5) / info['escala']
                
                    notas.append({
                        'actividad': info['nombre'],
                        'fecha': info['fecha'],
                        'nota': nota,
                        'porcentaje': info['porcentaje']
                    })
                except Exception as e:
                    print(f"Error procesando nota {actividad}: {str(e)}")
                    continue
                
                if info['porcentaje']:
                    nota_final += (nota * info['porcentaje']) / 100
                    total_porcentaje += info['porcentaje']
            
            # Si no hay porcentajes, calcular promedio simple
            if total_porcentaje == 0 and notas:
                nota_final = sum(n['nota'] for n in notas) / len(notas)
            
            estudiantes.append({
                'nombre': row['alumnos'],
                'notas': notas,
                'nota_final': round(nota_final, 2)
            })
        
        return jsonify({
            'estudiantes': estudiantes,
            'actividades': actividades_info
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/exportar-excel', methods=['GET'])
def exportar_excel():
    try:
        archivo = request.args.get('archivo')
        if not archivo:
            return jsonify({"error": "No se especificó el archivo"}), 400

        ruta_archivo = os.path.join('listas', archivo)
        if not os.path.exists(ruta_archivo):
            return jsonify({"error": "No se encontró el archivo"}), 404

        # Leer el archivo CSV
        df = pd.read_csv(ruta_archivo)
        
        # Crear un nuevo DataFrame para el Excel
        nombre_base = os.path.splitext(archivo)[0]
        excel_path = os.path.join('listas', f"{nombre_base}.xlsx")
        
        # Guardar como Excel
        df.to_excel(excel_path, index=False)
        
        return jsonify({
            "mensaje": "Excel exportado exitosamente",
            "archivo": f"{nombre_base}.xlsx"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/obtener-lista-materia', methods=['GET'])
def obtener_lista_materia():
    try:
        archivo = request.args.get('archivo')
        if not archivo:
            return jsonify({"error": "No se especificó el archivo"}), 400

        ruta_archivo = os.path.join('listas', archivo)
        if not os.path.exists(ruta_archivo):
            return jsonify({"error": "No se encontró el archivo"}), 404

        # Leer el archivo CSV
        df = pd.read_csv(ruta_archivo)
        
        return jsonify({
            "alumnos": df['alumnos'].tolist()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/obtener-estadisticas', methods=['GET'])
def obtener_estadisticas():
    try:
        archivo = request.args.get('archivo')
        if not archivo:
            return jsonify({"error": "No se especificó el archivo"}), 400

        ruta_archivo = os.path.join('listas', archivo)
        if not os.path.exists(ruta_archivo):
            return jsonify({"error": "No se encontró el archivo"}), 404

        # Leer el archivo CSV
        df = pd.read_csv(ruta_archivo)
        alumnos = df['alumnos'].tolist()
        fechas = [col for col in df.columns if col != 'alumnos']

        # Calcular estadísticas por alumno
        estudiantes = []
        for i, alumno in enumerate(alumnos):
            faltas = 0
            fechas_falta = []
            for fecha in fechas:
                if df.loc[i, fecha] == 'F':
                    faltas += 1
                    fechas_falta.append(fecha)

            estudiantes.append({
                "nombre": alumno,
                "faltas": faltas,
                "fechasFalta": fechas_falta,
                "porcentajeAsistencia": ((len(fechas) - faltas) / len(fechas) * 100) if fechas else 100
            })

        return jsonify({
            "estudiantes": estudiantes,
            "fechas": fechas
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
