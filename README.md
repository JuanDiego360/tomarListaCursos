# Sistema de Control de Asistencia Estudiantil

Este es un sistema de gestión de asistencia para estudiantes desarrollado en Python utilizando la biblioteca Tkinter para la interfaz gráfica. Permite llevar un registro detallado de la asistencia de estudiantes de bachillerato, con funcionalidades para crear nuevas listas, registrar asistencias y ver estadísticas.

## Características

### 1. Gestión de Grados
- Registro centralizado de grados en `grados.txt`
- Creación y validación automática de nuevos grados
- Organización de listas por grado con formato: `grado_YYYYMMDD_HHMMSS.csv`
- Manejo independiente de grados y materias

### 2. Crear Nueva Lista
- Permite crear una nueva lista de estudiantes para un grado específico
- Validación para evitar duplicación de grados
- Especificación del número de estudiantes
- Registro de nombres y apellidos de los estudiantes
- Almacenamiento automático en formato CSV con timestamp

### 3. Cargar Lista Existente
- Selección de grado y carga automática de la lista más reciente
- Registro de asistencia por fecha (formato dd/mm/aaaa)
- Marcación de asistencia mediante casillas de verificación
- Actualización automática del archivo CSV con los registros de asistencia

### 4. Estadísticas de la Lista
- Visualización de estadísticas por grado
- Muestra del total de inasistencias
- Detalle de fechas de ausencia
- Identificación de estudiantes sin faltas

### 5. Gestión de Materias
- Creación de materias asociadas a grados
- Registro de actividades y notas por materia
- Soporte para notas porcentuadas
- Escala de calificación personalizable (0-5 por defecto)

### 6. Estadísticas de Materias
- Visualización en formato tabla
- Cálculo automático de nota final según porcentajes
- Opción para colorear filas según nota mínima
- Exportación a Excel con un solo clic

## Estructura del Proyecto
```
tomador_de_lista/
│
├── interfazgrafica.py    # Archivo principal con la interfaz gráfica
├── listas/               # Directorio donde se almacenan los archivos CSV
│   ├── *.csv            # Archivos CSV de las listas de estudiantes
│   └── *.xlsx           # Archivos Excel exportados de las materias
├── grados.txt           # Registro centralizado de grados
├── materias_dictadas.txt # Registro de materias por grado
└── README.md            # Este archivo
```

## Requisitos
- Python 3.x
- Tkinter (incluido en la instalación estándar de Python)
- pandas (para manejo de datos y exportación a Excel)
- openpyxl (para soporte de archivos Excel)

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/JuanDiego360/tomarListaCursos.git
```

2. Navega al directorio del proyecto:
```bash
cd tomador_de_lista
```

3. Ejecuta el programa:
```bash
python3 interfazgrafica.py
```

## Uso

### Crear una Nueva Lista
1. Haz clic en "Crear Nueva Lista"
2. Ingresa el nombre del curso o grado
3. Especifica el número de estudiantes
4. Ingresa los nombres de los estudiantes
5. Guarda la lista

### Registrar Asistencia
1. Haz clic en "Cargar Lista Existente"
2. Selecciona la lista deseada
3. Ingresa la fecha en formato dd/mm/aaaa
4. Marca las casillas de los estudiantes presentes
5. Guarda el registro

### Ver Estadísticas de Lista
1. Haz clic en "Estadística de la Lista"
2. Selecciona el grado a consultar
3. Visualiza las estadísticas de asistencia por estudiante

### Gestionar Materias
1. Crea una nueva materia usando "Crear Nueva Materia"
2. Selecciona el grado para la materia
3. Registra actividades y notas con "Cargar Materia Existente"
4. Configura porcentajes y escalas de calificación según necesites

### Ver Estadísticas de Materias
1. Haz clic en "Estadística de la Materia"
2. Selecciona la materia a consultar
3. Visualiza la tabla de notas y nota final
4. Usa la opción de colorear para identificar estudiantes bajo la nota mínima
5. Exporta a Excel si lo necesitas

## Formato de Archivos
Los datos se almacenan en archivos CSV con la siguiente estructura:
- Primera columna: Nombres de los estudiantes
- Columnas siguientes: Fechas de asistencia
- Valores de asistencia: 'A' (Asistió), 'F' (Faltó)

## Contribución
Si deseas contribuir al proyecto:
1. Haz un Fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Realiza tus cambios y haz commit (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Autor
Juan Diego Florez Vera

