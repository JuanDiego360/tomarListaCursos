// Variables globales
let listaActual = {
    grado: '',
    alumnos: []
};

// URL base del servidor
const API_URL = 'http://localhost:5000';

// Funciones para manejar modales
function abrirModal(modalId) {
    console.log('Abriendo modal:', modalId);
    const modal = document.getElementById(modalId);
    if (!modal) {
        console.error('No se encontró el modal:', modalId);
        return;
    }
    modal.style.display = 'block';
}

function cerrarModal(modalId) {
    console.log('Cerrando modal:', modalId);
    const modal = document.getElementById(modalId);
    if (!modal) {
        console.error('No se encontró el modal:', modalId);
        return;
    }
    modal.style.display = 'none';
}

// Configurar eventos cuando el documento esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('Iniciando configuración de la aplicación');

    // Configurar eventos de cierre para modales
    document.querySelectorAll('.close').forEach(closeBtn => {
        closeBtn.onclick = function() {
            this.closest('.modal').style.display = 'none';
        }
    });

    window.onclick = function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
        }
    }

    // Configurar eventos para los botones principales
    const btnCrearLista = document.getElementById('btnCrearLista');
    const btnCargarLista = document.getElementById('btnCargarLista');
    const btnEstadisticas = document.getElementById('btnEstadisticas');
    const btnCrearMateria = document.getElementById('btnCrearMateria');
    const btnCargarMateria = document.getElementById('btnCargarMateria');
    const btnEstadisticaMateria = document.getElementById('btnEstadisticaMateria');

    if (btnCrearLista) {
        console.log('Configurando botón Crear Lista');
        btnCrearLista.addEventListener('click', crearNuevaLista);
    }

    if (btnCargarLista) {
        console.log('Configurando botón Cargar Lista');
        btnCargarLista.addEventListener('click', cargarLista);
    }

    if (btnEstadisticas) {
        console.log('Configurando botón Estadísticas');
        btnEstadisticas.addEventListener('click', async () => {
            try {
                // Obtener las listas disponibles
                const response = await fetch(`${API_URL}/obtener-listas`);
                const listas = await response.json();

                if (!Array.isArray(listas) || listas.length === 0) {
                    alert('No hay listas registradas.');
                    return;
                }

                // Llenar el select con las listas disponibles
                const select = document.getElementById('selectListaEstadisticas');
                select.innerHTML = '<option value="">Seleccione un grado</option>';
                
                // Usar Set para tener grados únicos
                const gradosUnicos = new Set(listas.map(lista => lista.grado));
                
                gradosUnicos.forEach(grado => {
                    const option = document.createElement('option');
                    const lista = listas.find(l => l.grado === grado);
                    option.value = JSON.stringify(lista);
                    option.textContent = grado;
                    select.appendChild(option);
                });

                // Mostrar el modal
                abrirModal('modalSeleccionarListaEstadisticas');
            } catch (error) {
                alert('Error al cargar las listas: ' + error.message);
            }
        });
    }

    if (btnCrearMateria) {
        console.log('Configurando botón Crear Materia');
        btnCrearMateria.addEventListener('click', crearNuevaMateria);
    }

    if (btnCargarMateria) {
        console.log('Configurando botón Cargar Materia');
        btnCargarMateria.addEventListener('click', async () => {
            try {
                // Obtener las materias disponibles
                const response = await fetch(`${API_URL}/obtener-materias`);
                const materias = await response.json();

                if (!Array.isArray(materias) || materias.length === 0) {
                    alert('No hay materias registradas.');
                    return;
                }

                // Llenar el select con las materias disponibles
                const select = document.getElementById('selectMateria');
                select.innerHTML = '<option value="">Seleccione una materia</option>';
                
                materias.forEach(materia => {
                    const option = document.createElement('option');
                    option.value = JSON.stringify(materia);
                    option.textContent = `${materia.grado} - ${materia.materia}`;
                    select.appendChild(option);
                });

                // Mostrar el modal
                abrirModal('modalCargarMateria');
            } catch (error) {
                alert('Error al cargar las materias: ' + error.message);
            }
        });
    }

    if (btnEstadisticaMateria) {
        console.log('Configurando botón Estadística Materia');
        btnEstadisticaMateria.addEventListener('click', estadisticaMateria);
    }
});


// Funciones principales
function crearNuevaLista() {
    console.log('Iniciando creación de nueva lista');
    abrirModal('modalNuevaLista');
}

function registrarAlumnos() {
    console.log('Iniciando registro de alumnos');
    const nombreCurso = document.getElementById('nombreCurso');
    const numAlumnosInput = document.getElementById('numAlumnos');

    if (!nombreCurso || !numAlumnosInput) {
        console.error('No se encontraron los elementos del formulario');
        return;
    }

    const nombreCursoValue = nombreCurso.value.trim();
    const numAlumnos = parseInt(numAlumnosInput.value);

    console.log('Datos del formulario:', { nombreCursoValue, numAlumnos });

    if (!nombreCursoValue) {
        alert('Por favor ingrese el nombre del grado');
        return;
    }
    if (isNaN(numAlumnos) || numAlumnos <= 0) {
        alert('El número de alumnos debe ser mayor a 0');
        return;
    }

    listaActual.grado = nombreCursoValue;
    
    // Crear campos para ingresar nombres de alumnos
    const container = document.getElementById('alumnosContainer');
    if (!container) {
        console.error('No se encontró el contenedor de alumnos');
        return;
    }

    container.innerHTML = '';
    
    for (let i = 0; i < numAlumnos; i++) {
        const div = document.createElement('div');
        div.className = 'alumno-input';
        div.innerHTML = `
            <label for="alumno${i}">Alumno ${i + 1}:</label>
            <input type="text" id="alumno${i}" required>
        `;
        container.appendChild(div);
    }

    console.log('Campos de alumnos creados');
    cerrarModal('modalNuevaLista');
    abrirModal('modalAlumnos');
}

async function guardarAlumnos() {
    const inputs = document.querySelectorAll('#alumnosContainer input');
    const alumnos = Array.from(inputs).map(input => input.value.trim());

    // Verificar que todos los campos estén llenos
    if (alumnos.some(alumno => !alumno)) {
        alert('Por favor complete todos los nombres');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/crear-lista`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                grado: listaActual.grado,
                alumnos: alumnos
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            alert(`Lista guardada exitosamente en ${data.archivo}`);
            cerrarModal('modalAlumnos');
        } else {
            throw new Error(data.error || 'Error al guardar la lista');
        }
    } catch (error) {
        alert('Error al guardar la lista: ' + error.message);
    }
}

async function cargarLista() {
    try {
        const response = await fetch(`${API_URL}/obtener-listas`);
        const listas = await response.json();

        if (!Array.isArray(listas) || listas.length === 0) {
            alert('No hay listas guardadas');
            return;
        }

        // Llenar el select con las listas disponibles
        const select = document.getElementById('selectLista');
        select.innerHTML = '<option value="">Seleccione un grado</option>';
        
        // Usar Set para tener grados únicos
        const gradosUnicos = new Set(listas.map(lista => lista.grado));
        
        gradosUnicos.forEach(grado => {
            const option = document.createElement('option');
            const lista = listas.find(l => l.grado === grado);
            option.value = JSON.stringify(lista);
            option.textContent = grado;
            select.appendChild(option);
        });

        // Mostrar el modal
        abrirModal('modalSeleccionarLista');
    } catch (error) {
        alert('Error al cargar las listas: ' + error.message);
    }
}

function mostrarModalAsistencia(lista) {
    // Establecer la fecha actual en el input
    const fechaInput = document.getElementById('fechaAsistencia');
    const hoy = new Date().toISOString().split('T')[0];
    fechaInput.value = hoy;

    // Crear checkboxes para cada alumno
    const container = document.getElementById('asistenciaContainer');
    container.innerHTML = '';

    lista.alumnos.forEach((alumno, index) => {
        const div = document.createElement('div');
        div.className = 'alumno-input';
        div.innerHTML = `
            <label>
                <input type="checkbox" id="asistencia${index}" checked>
                <span>${alumno}</span>
            </label>
        `;
        container.appendChild(div);
    });

    // Mostrar el modal
    abrirModal('modalAsistencia');
}

async function guardarAsistencia() {
    const fecha = document.getElementById('fechaAsistencia').value;

    if (!fecha) {
        alert('Por favor seleccione una fecha');
        return;
    }

    // Verificar si ya existe asistencia para esta fecha
    if (listaActual.fechasAsistencia && listaActual.fechasAsistencia.includes(fecha)) {
        const confirmar = confirm('Ya existe un registro de asistencia para esta fecha. ¿Desea sobrescribirlo?');
        if (!confirmar) return;
    }

    // Obtener el estado de los checkboxes
    const asistencias = [];
    listaActual.alumnos.forEach((_, index) => {
        const checkbox = document.getElementById(`asistencia${index}`);
        asistencias.push(checkbox.checked ? 'A' : 'F');
    });

    try {
        const response = await fetch(`${API_URL}/guardar-asistencia`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                archivo: listaActual.archivo,
                fecha: fecha,
                asistencias: asistencias
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            alert('Asistencia guardada exitosamente');
            cerrarModal('modalAsistencia');
        } else {
            throw new Error(data.error || 'Error al guardar la asistencia');
        }
    } catch (error) {
        alert('Error al guardar la asistencia: ' + error.message);
    }
}

async function mostrarEstadisticas() {
    try {
        const response = await fetch(`${API_URL}/obtener-listas`);
        const listas = await response.json();

        if (!Array.isArray(listas) || listas.length === 0) {
            alert('No hay listas guardadas para mostrar estadísticas');
            return;
        }

        const grado = prompt('Ingrese el nombre del grado a consultar:');
        if (!grado) return;

        const lista = listas.find(l => l.grado === grado);
        if (!lista) {
            alert('No se encontró la lista especificada');
            return;
        }

        // Preparar los datos para la página de estadísticas
        const alumnosSinFaltas = lista.estadisticas.filter(a => a.faltas === 0).length;
        const estadisticasData = {
            grado: lista.grado,
            totalAlumnos: lista.alumnos.length,
            totalClases: lista.fechasAsistencia.length,
            alumnosSinFaltas: alumnosSinFaltas,
            alumnosConFaltas: lista.alumnos.length - alumnosSinFaltas,
            alumnos: lista.estadisticas
        };

        // Abrir nueva ventana con las estadísticas
        const dataParam = encodeURIComponent(JSON.stringify(estadisticasData));
        window.open(`estadisticas.html?data=${dataParam}`, '_blank');
    } catch (error) {
        alert('Error al obtener estadísticas: ' + error.message);
    }
}

// Funciones para materias
async function crearNuevaMateria() {
    try {
        // Obtener las listas disponibles
        const response = await fetch(`${API_URL}/obtener-listas`);
        const listas = await response.json();

        if (!Array.isArray(listas) || listas.length === 0) {
            alert('No hay listas de grados disponibles. Primero debe crear una lista de estudiantes.');
            return;
        }

        // Llenar el select con las listas disponibles
        const select = document.getElementById('gradoMateria');
        select.innerHTML = '<option value="">Seleccione un grado</option>';
        
        listas.forEach(lista => {
            const option = document.createElement('option');
            option.value = lista.archivo;
            option.textContent = lista.grado;
            select.appendChild(option);
        });

        // Mostrar el modal
        abrirModal('modalMateria');
    } catch (error) {
        alert('Error al cargar las listas: ' + error.message);
    }
}

async function guardarMateria() {
    const gradoSelect = document.getElementById('gradoMateria');
    const nombreMateria = document.getElementById('nombreMateria').value.trim();
    const archivoBase = gradoSelect.value;
    const grado = gradoSelect.options[gradoSelect.selectedIndex].text;

    if (!archivoBase) {
        alert('Por favor seleccione un grado');
        return;
    }

    if (!nombreMateria) {
        alert('Por favor ingrese el nombre de la materia');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/crear-materia`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                grado: grado,
                materia: nombreMateria,
                archivoBase: archivoBase
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            alert(`Materia ${nombreMateria} creada exitosamente`);
            cerrarModal('modalMateria');
            // Limpiar el formulario
            document.getElementById('nombreMateria').value = '';
            gradoSelect.value = '';
        } else {
            if (response.status === 409) {
                if (confirm('Ya existe una lista para esta materia. ¿Desea sobrescribirla?')) {
                    // Aquí podríamos implementar la lógica para sobrescribir
                }
            } else {
                throw new Error(data.error || 'Error al crear la materia');
            }
        }
    } catch (error) {
        alert('Error al crear la materia: ' + error.message);
    }
}

async function cargarMateriaExistente() {
    try {
        // Obtener las materias disponibles
        const response = await fetch(`${API_URL}/obtener-materias`);
        const materias = await response.json();

        if (!Array.isArray(materias) || materias.length === 0) {
            alert('No hay materias registradas. Por favor, cree primero una Nueva materia.');
            return;
        }

        // Llenar el select con las materias disponibles
        const select = document.getElementById('selectMateria');
        select.innerHTML = '<option value="">Seleccione una materia</option>';
        
        materias.forEach(materia => {
            const option = document.createElement('option');
            option.value = materia.archivo;
            option.textContent = `${materia.grado} - ${materia.materia}`;
            option.dataset.alumnos = JSON.stringify(materia.alumnos);
            select.appendChild(option);
        });

        // Configurar eventos para los checkboxes
        document.getElementById('usarPorcentaje').addEventListener('change', function() {
            document.getElementById('porcentajeActividad').disabled = !this.checked;
        });

        document.getElementById('cambiarEscala').addEventListener('change', function() {
            document.getElementById('escalaActividad').disabled = !this.checked;
        });

        // Configurar evento para cuando se selecciona una materia
        select.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            if (selectedOption.value) {
                mostrarFormularioNotas(selectedOption.value);
            }
        });

        // Establecer la fecha actual
        const fechaInput = document.getElementById('fechaActividad');
        const hoy = new Date().toISOString().split('T')[0];
        fechaInput.value = hoy;

        // Mostrar el modal
        abrirModal('modalCargarMateria');
    } catch (error) {
        alert('Error al cargar las materias: ' + error.message);
    }
}

async function mostrarFormularioNotas(archivoMateria) {
    try {
        // Leer directamente el archivo de la materia
        const response = await fetch(`${API_URL}/obtener-materias`);
        const materias = await response.json();
        const materia = materias.find(m => m.archivo === archivoMateria);

        if (!materia) {
            throw new Error('No se encontró la materia');
        }

        // Crear campos para las notas
        const container = document.getElementById('notasContainer');
        container.innerHTML = '<h3>Notas de los estudiantes</h3>';

        // Leer el archivo CSV de la materia
        const csvResponse = await fetch(`${API_URL}/obtener-lista-materia?archivo=${archivoMateria}`);
        const csvData = await csvResponse.json();

        if (!csvResponse.ok) {
            throw new Error(csvData.error || 'Error al cargar la lista de alumnos');
        }

        csvData.alumnos.forEach((alumno, index) => {
            const div = document.createElement('div');
            div.className = 'alumno-input';
            div.innerHTML = `
                <label for="nota${index}">${alumno}:</label>
                <input type="number" id="nota${index}" class="nota-input" 
                       min="0" max="5" step="0.1" value="0">
            `;
            container.appendChild(div);
        });
    } catch (error) {
        alert('Error al cargar los alumnos: ' + error.message);
    }
}

async function cargarListaSeleccionada() {
    const select = document.getElementById('selectLista');
    const listaJson = select.value;
    
    if (!listaJson) {
        alert('Por favor seleccione un grado');
        return;
    }

    try {
        const lista = JSON.parse(listaJson);
        listaActual = lista;
        mostrarModalAsistencia(lista);
        cerrarModal('modalSeleccionarLista');
    } catch (error) {
        alert('Error al cargar la lista: ' + error.message);
    }
}

async function cargarMateriaSeleccionada() {
    const select = document.getElementById('selectMateria');
    const materiaJson = select.value;
    
    if (!materiaJson) {
        alert('Por favor seleccione una materia');
        return;
    }

    try {
        const materiaInfo = JSON.parse(materiaJson);
        mostrarFormularioNotas(materiaInfo.archivo);
        cerrarModal('modalCargarMateria');
    } catch (error) {
        alert('Error al cargar la materia: ' + error.message);
    }
}

async function guardarActividad() {
    const materiaSelect = document.getElementById('selectMateria');
    const fecha = document.getElementById('fechaActividad').value;
    const nombreActividad = document.getElementById('nombreActividad').value.trim();
    const usarPorcentaje = document.getElementById('usarPorcentaje').checked;
    const porcentaje = usarPorcentaje ? document.getElementById('porcentajeActividad').value : null;
    const cambiarEscala = document.getElementById('cambiarEscala').checked;
    const escala = cambiarEscala ? document.getElementById('escalaActividad').value : 5;

    if (!materiaSelect.value) {
        alert('Por favor seleccione una materia');
        return;
    }

    if (!fecha) {
        alert('Por favor seleccione una fecha');
        return;
    }

    if (!nombreActividad) {
        alert('Por favor ingrese el nombre de la actividad');
        return;
    }

    // Obtener todas las notas
    const notasInputs = document.querySelectorAll('.nota-input');
    const notas = Array.from(notasInputs).map(input => parseFloat(input.value));

    // Validar que todas las notas estén dentro del rango
    const maxNota = cambiarEscala ? escala : 5;
    if (notas.some(nota => isNaN(nota) || nota < 0 || nota > maxNota)) {
        alert(`Las notas deben estar entre 0 y ${maxNota}`);
        return;
    }

    try {
        const response = await fetch(`${API_URL}/guardar-actividad`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                archivo: materiaSelect.value,
                fecha: fecha,
                actividad: nombreActividad,
                notas: notas,
                porcentaje: porcentaje,
                escala: parseInt(escala)
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            alert('Actividad guardada exitosamente');
            cerrarModal('modalCargarMateria');
        } else {
            if (response.status === 409) {
                if (confirm('Ya existe una actividad con esta fecha. ¿Desea sobrescribirla?')) {
                    // Aquí podríamos implementar la lógica para sobrescribir
                }
            } else {
                throw new Error(data.error || 'Error al guardar la actividad');
            }
        }
    } catch (error) {
        alert('Error al guardar la actividad: ' + error.message);
    }
}

async function estadisticaMateria() {
    try {
        // Obtener las materias disponibles
        const response = await fetch(`${API_URL}/obtener-materias`);
        const materias = await response.json();

        if (!Array.isArray(materias) || materias.length === 0) {
            alert('No hay materias registradas.');
            return;
        }

        // Llenar el select con las materias disponibles
        const select = document.getElementById('selectMateriaEstadistica');
        select.innerHTML = '<option value="">Seleccione una materia</option>';
        
        materias.forEach(materia => {
            const option = document.createElement('option');
            option.value = JSON.stringify(materia);
            option.textContent = `${materia.grado} - ${materia.materia}`;
            select.appendChild(option);
        });

        // Mostrar el modal
        abrirModal('modalSeleccionarMateria');
    } catch (error) {
        alert('Error al cargar las materias: ' + error.message);
    }
}

async function mostrarEstadisticasLista() {
    const select = document.getElementById('selectListaEstadisticas');
    const listaJson = select.value;
    
    if (!listaJson) {
        alert('Por favor seleccione un grado');
        return;
    }

    try {
        const lista = JSON.parse(listaJson);

        // Obtener estadísticas de la lista
        const statsResponse = await fetch(`${API_URL}/obtener-estadisticas?archivo=${lista.archivo}`);
        const statsData = await statsResponse.json();

        if (!statsResponse.ok) {
            throw new Error(statsData.error || 'Error al obtener estadísticas');
        }

        // Preparar datos para la página de estadísticas
        const data = {
            grado: lista.grado,
            estudiantes: statsData.estudiantes,
            fechas: statsData.fechas
        };

        // Abrir nueva ventana con las estadísticas
        const dataParam = encodeURIComponent(JSON.stringify(data));
        window.open(`estadisticas.html?data=${dataParam}`, '_blank');

        // Cerrar el modal
        cerrarModal('modalSeleccionarListaEstadisticas');
    } catch (error) {
        alert('Error al obtener estadísticas: ' + error.message);
    }
}

async function mostrarEstadisticasMateria() {
    const select = document.getElementById('selectMateriaEstadistica');
    const materiaJson = select.value;
    
    if (!materiaJson) {
        alert('Por favor seleccione una materia');
        return;
    }

    try {
        const materiaInfo = JSON.parse(materiaJson);

        // Obtener estadísticas de la materia
        const statsResponse = await fetch(`${API_URL}/obtener-estadisticas-materia?archivo=${materiaInfo.archivo}`);
        const statsData = await statsResponse.json();

        if (!statsResponse.ok) {
            throw new Error(statsData.error || 'Error al obtener estadísticas');
        }

        // Preparar datos para la página de estadísticas
        const data = {
            grado: materiaInfo.grado,
            materia: materiaInfo.materia,
            estudiantes: statsData.estudiantes,
            actividades: statsData.actividades
        };

        // Abrir nueva ventana con las estadísticas
        const dataParam = encodeURIComponent(JSON.stringify(data));
        window.open(`estadisticas_materia.html?data=${dataParam}&archivo=${materiaInfo.archivo}`, '_blank');
        
        // Cerrar el modal
        cerrarModal('modalSeleccionarMateria');
    } catch (error) {
        alert('Error al obtener estadísticas: ' + error.message);
    }
}
