# Sistema de Control de Asistencia Estudiantil

Este es un sistema de gestión de asistencia para estudiantes desarrollado en Python utilizando la biblioteca Tkinter para la interfaz gráfica. Permite llevar un registro detallado de la asistencia de estudiantes de bachillerato, con funcionalidades para crear nuevas listas, registrar asistencias y ver estadísticas.

## Características

### 1. Crear Nueva Lista
- Permite crear una nueva lista de estudiantes para un curso o grado específico
- Ingreso del nombre del curso/grado
- Especificación del número de estudiantes
- Registro de nombres y apellidos de los estudiantes
- Almacenamiento automático en formato CSV

### 2. Cargar Lista Existente
- Selección de listas previamente creadas
- Registro de asistencia por fecha (formato dd/mm/aaaa)
- Marcación de asistencia mediante casillas de verificación
- Actualización automática del archivo CSV con los registros de asistencia

### 3. Estadísticas de la Lista
- Visualización de estadísticas por estudiante
- Muestra del total de inasistencias
- Detalle de fechas de ausencia
- Identificación de estudiantes sin faltas

## Estructura del Proyecto
```
tomador_de_lista/
│
├── interfazgrafica.py    # Archivo principal con la interfaz gráfica
├── listas/               # Directorio donde se almacenan los archivos CSV
│   └── *.csv            # Archivos CSV de las listas de estudiantes
└── README.md            # Este archivo
```

## Requisitos
- Python 3.x
- Tkinter (incluido en la instalación estándar de Python)

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

### Ver Estadísticas
1. Haz clic en "Estadística de la Lista"
2. Selecciona la lista a consultar
3. Visualiza las estadísticas de asistencia por estudiante

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

