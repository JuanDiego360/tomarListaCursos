import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
import pandas as pd
from tkinter import filedialog

class AsistenciaApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de control Estudiantil")
        self.root.geometry("800x600")
        
        # Configurar el estilo
        self.style = ttk.Style()
        self.style.configure('TButton', padding=10, font=('Arial', 12))
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True, fill='both')
        
        # Mensaje de bienvenida
        welcome_label = ttk.Label(
            main_frame,
            text="¡Bienvenido al Sistema de Control Estudiantil JD!",
            font=('Arial', 20, 'bold')
        )
        welcome_label.pack(pady=(30, 20))  # Menos padding arriba y abajo
        
        # Frame para los botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=(10, 30))  # Menos padding arriba
        
        # Botón Nueva Lista
        new_list_btn = ttk.Button(
            button_frame,
            text="Crear Nueva Lista",
            command=self.crear_nueva_lista
        )
        new_list_btn.pack(pady=10)
        
        # Botón Cargar Lista
        load_list_btn = ttk.Button(
            button_frame,
            text="Cargar Lista Existente",
            command=self.cargar_lista
        )
        load_list_btn.pack(pady=10)
        
        # Botón Estadística de la Lista
        stats_list_btn = ttk.Button(
            button_frame,
            text="Estadística de la Lista",
            command=self.mostrar_estadisticas
        )
        stats_list_btn.pack(pady=10)
        
        # Botón Crear Nueva Materia
        new_subject_btn = ttk.Button(
            button_frame,
            text="Crear Nueva Materia",
            command=self.crear_nueva_materia
        )
        new_subject_btn.pack(pady=10)
        
        # Botón Cargar Materia Existente
        load_subject_btn = ttk.Button(
            button_frame,
            text="Cargar Materia Existente",
            command=self.cargar_materia_existente
        )
        load_subject_btn.pack(pady=10)
        
        # Botón Estadística de la Materia
        stats_subject_btn = ttk.Button(
            button_frame,
            text="Estadística de la Materia",
            command=self.estadistica_materia,
            width=25  # Haciendo el botón más ancho
        )
        stats_subject_btn.pack(pady=10)
        
        # Marca de agua (nombre)
        watermark = ttk.Label(
            self.root,
            text="Juan Diego Florez Vera",
            font=('Arial', 8, 'italic')
        )
        watermark.pack(side='bottom', anchor='sw', padx=10, pady=5)
    
    def crear_nueva_lista(self):
        # Crear una nueva ventana
        nueva_lista_window = tk.Toplevel(self.root)
        nueva_lista_window.title("Crear Nueva Lista")
        nueva_lista_window.geometry("500x300")
        nueva_lista_window.transient(self.root)
        
        # Frame principal
        frame = ttk.Frame(nueva_lista_window, padding="30")
        frame.pack(expand=True, fill='both')
        
        # Entrada para el nombre del curso
        ttk.Label(frame, text="Nombre del curso o grado:", font=('Arial', 12)).pack()
        curso_entry = ttk.Entry(frame, width=40, font=('Arial', 11))
        curso_entry.pack(pady=15)
        
        # Entrada para el número de alumnos
        ttk.Label(frame, text="Número de alumnos:", font=('Arial', 12)).pack()
        num_alumnos_entry = ttk.Entry(frame, width=40, font=('Arial', 11))
        num_alumnos_entry.pack(pady=15)
        
        def registrar_alumnos():
            try:
                grado = curso_entry.get().strip()
                num_alumnos = int(num_alumnos_entry.get())
                
                if not grado:
                    messagebox.showerror("Error", "Por favor ingrese el nombre del grado")
                    return
                if num_alumnos <= 0:
                    messagebox.showerror("Error", "El número de alumnos debe ser mayor a 0")
                    return
                
                # Verificar si existe el archivo grados.txt
                if not os.path.exists('grados.txt'):
                    with open('grados.txt', 'w', encoding='utf-8') as file:
                        pass
                
                # Verificar si el grado ya existe
                with open('grados.txt', 'r', encoding='utf-8') as file:
                    grados = file.read().splitlines()
                
                if grado in grados:
                    messagebox.showerror("Error", "Este grado ya existe")
                    return
                
                # Agregar el nuevo grado a grados.txt
                with open('grados.txt', 'a', encoding='utf-8') as file:
                    file.write(grado + '\n')
                
                # Cerrar ventana actual
                nueva_lista_window.destroy()
                
                # Crear ventana para ingresar nombres
                nombres_window = tk.Toplevel(self.root)
                nombres_window.title(f"Registrar Alumnos - {grado}")
                nombres_window.geometry("500x600")
                nombres_window.transient(self.root)
                
                # Frame con scroll para los campos de entrada
                canvas = tk.Canvas(nombres_window)
                scrollbar = ttk.Scrollbar(nombres_window, orient="vertical", command=canvas.yview)
                scroll_frame = ttk.Frame(canvas)
                
                canvas.configure(yscrollcommand=scrollbar.set)
                
                # Lista para almacenar las entradas
                entries = []
                
                # Crear campos para cada alumno
                for i in range(num_alumnos):
                    frame_alumno = ttk.Frame(scroll_frame)
                    frame_alumno.pack(fill='x', pady=5)
                    ttk.Label(frame_alumno, text=f"Alumno {i+1}:").pack(side='left')
                    entry = ttk.Entry(frame_alumno, width=40)
                    entry.pack(side='left', padx=5)
                    entries.append(entry)
                
                def guardar_alumnos():
                    import csv
                    import os
                    from datetime import datetime
                    
                    # Crear directorio si no existe
                    if not os.path.exists('listas'):
                        os.makedirs('listas')
                    
                    # Generar nombre de archivo con formato: grado_YYYYMMDD_HHMMSS.csv
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"listas/{grado}_{timestamp}.csv"
                    
                    alumnos = [entry.get().strip() for entry in entries]
                    
                    # Verificar que todos los campos estén llenos
                    if any(not alumno for alumno in alumnos):
                        messagebox.showerror("Error", "Por favor complete todos los nombres")
                        return
                    
                    with open(filename, 'w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow(['alumnos'])  # Encabezado
                        for alumno in alumnos:
                            writer.writerow([alumno])
                    
                    messagebox.showinfo("Éxito", f"Lista guardada exitosamente en {filename}")
                    nombres_window.destroy()
                
                # Configurar el scroll
                scroll_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )
                
                canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
                
                # Empaquetar los widgets
                canvas.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")
                
                # Botón guardar
                ttk.Button(
                    nombres_window,
                    text="Guardar",
                    command=guardar_alumnos
                ).pack(pady=10)
                
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese un número válido de alumnos")
        
        # Botón para continuar
        continuar_btn = ttk.Button(
            frame,
            text="Continuar",
            command=registrar_alumnos,
            style='Custom.TButton'
        )
        self.style.configure('Custom.TButton', font=('Arial', 12), padding=(20, 10))
        continuar_btn.pack(pady=30)
    
    def cargar_lista(self):
        import os
        import csv
        from datetime import datetime
        
        # Verificar si existe el archivo de grados
        if not os.path.exists('grados.txt'):
            messagebox.showerror("Error", "No hay grados registrados aún")
            return
        
        # Leer grados disponibles
        with open('grados.txt', 'r', encoding='utf-8') as file:
            grados = file.read().splitlines()
        
        if not grados:
            messagebox.showerror("Error", "No hay grados registrados aún")
            return
        
        # Crear ventana para seleccionar grado
        seleccion_window = tk.Toplevel(self.root)
        seleccion_window.title("Seleccionar Grado")
        seleccion_window.geometry("500x250")
        seleccion_window.transient(self.root)
        
        # Frame principal
        frame = ttk.Frame(seleccion_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        # Label
        ttk.Label(frame, text="Seleccione un grado:", font=('Arial', 12)).pack(pady=10)
        
        # Combobox para seleccionar grado
        combo = ttk.Combobox(frame, values=grados, state='readonly', font=('Arial', 11), width=30)
        combo.pack(pady=20)
        
        def abrir_lista():
            grado_seleccionado = combo.get()
            if not grado_seleccionado:
                messagebox.showerror("Error", "Por favor seleccione un grado")
                return
            
            # Obtener todas las listas del grado seleccionado
            archivos_grado = [f for f in os.listdir('listas') if f.startswith(grado_seleccionado + '_') and f.endswith('.csv')]
            
            if not archivos_grado:
                messagebox.showerror("Error", f"No hay listas de estudiantes para el grado {grado_seleccionado}")
                return
            
            # Ordenar por fecha (más reciente primero)
            archivos_grado.sort(reverse=True)
            
            # Seleccionar el archivo más reciente
            archivo_seleccionado = os.path.join('listas', archivos_grado[0])
            seleccion_window.destroy()
            
            # Crear ventana para tomar asistencia
            asistencia_window = tk.Toplevel(self.root)
            asistencia_window.title("Tomar Asistencia")
            asistencia_window.geometry("600x700")
            asistencia_window.transient(self.root)
            
            # Frame principal
            main_frame = ttk.Frame(asistencia_window, padding="20")
            main_frame.pack(expand=True, fill='both')
            
            # Frame para la fecha
            fecha_frame = ttk.Frame(main_frame)
            fecha_frame.pack(fill='x', pady=(0, 20))
            
            ttk.Label(fecha_frame, text="Fecha (dd/mm/aaaa):", font=('Arial', 12)).pack(side='left')
            fecha_entry = ttk.Entry(fecha_frame, font=('Arial', 11), width=15)
            fecha_entry.pack(side='left', padx=10)
            
            # Frame con scroll para la lista de alumnos
            canvas = tk.Canvas(main_frame)
            scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            scroll_frame = ttk.Frame(canvas)
            
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Leer alumnos del archivo CSV
            with open(archivo_seleccionado, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers = next(reader)  # Leer encabezados
                alumnos = [row[0] for row in reader]  # Leer nombres de alumnos
            
            # Variables para los checkboxes
            vars_asistencia = {}
            
            # Crear checkboxes para cada alumno
            for alumno in alumnos:
                frame_alumno = ttk.Frame(scroll_frame)
                frame_alumno.pack(fill='x', pady=5)
                
                vars_asistencia[alumno] = tk.BooleanVar(value=True)
                
                ttk.Label(frame_alumno, text=alumno, font=('Arial', 11)).pack(side='left', padx=(0, 10))
                ttk.Checkbutton(frame_alumno, variable=vars_asistencia[alumno]).pack(side='right')
            
            def guardar_asistencia():
                fecha = fecha_entry.get().strip()
                
                # Validar formato de fecha
                try:
                    datetime.strptime(fecha, '%d/%m/%Y')
                except ValueError:
                    messagebox.showerror("Error", "Formato de fecha inválido. Use dd/mm/aaaa")
                    return
                
                # Verificar si la fecha ya existe
                with open(archivo_seleccionado, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    headers = next(reader)
                    if fecha in headers:
                        if not messagebox.askyesno("Confirmar", "Ya existe registro para esta fecha. ¿Desea sobrescribirlo?"):
                            return
                
                # Leer todo el contenido actual
                with open(archivo_seleccionado, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    contenido = list(reader)
                
                # Actualizar headers y contenido
                if fecha not in contenido[0]:
                    contenido[0].append(fecha)
                fecha_index = contenido[0].index(fecha)
                
                # Actualizar asistencia
                for i, row in enumerate(contenido[1:], 1):
                    alumno = row[0]
                    # Extender la fila si es necesario
                    while len(row) <= fecha_index:
                        row.append('')
                    row[fecha_index] = 'A' if vars_asistencia[alumno].get() else 'F'
                
                # Guardar cambios
                with open(archivo_seleccionado, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(contenido)
                
                messagebox.showinfo("Éxito", "Asistencia guardada correctamente")
                asistencia_window.destroy()
            
            # Configurar el scroll
            scroll_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
            
            # Empaquetar los widgets
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Botón guardar
            ttk.Button(
                main_frame,
                text="Guardar Asistencia",
                command=guardar_asistencia,
                style='Custom.TButton'
            ).pack(pady=20)
        
        # Estilo para el botón siguiente
        self.style.configure('Siguiente.TButton',
                            font=('Arial', 12, 'bold'),
                            padding=(30, 15))
        
        # Botón siguiente
        siguiente_btn = ttk.Button(
            frame,
            text="Siguiente",
            command=abrir_lista,
            style='Siguiente.TButton',
            width=15
        )
        siguiente_btn.pack(pady=30)
    
    def mostrar_estadisticas(self):
        import os
        import csv
        from datetime import datetime
        
        # Verificar si existe el archivo de grados
        if not os.path.exists('grados.txt'):
            messagebox.showerror("Error", "No hay grados registrados aún")
            return
        
        # Leer grados disponibles
        with open('grados.txt', 'r', encoding='utf-8') as file:
            grados = file.read().splitlines()
        
        if not grados:
            messagebox.showerror("Error", "No hay grados registrados aún")
            return
        
        # Crear ventana para seleccionar grado
        seleccion_window = tk.Toplevel(self.root)
        seleccion_window.title("Seleccionar Grado para Estadísticas")
        seleccion_window.geometry("500x250")
        seleccion_window.transient(self.root)
        
        # Frame principal
        frame = ttk.Frame(seleccion_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        # Label
        ttk.Label(frame, text="Seleccione un grado:", font=('Arial', 12)).pack(pady=10)
        
        # Combobox para seleccionar grado
        combo = ttk.Combobox(frame, values=grados, state='readonly', font=('Arial', 11), width=30)
        combo.pack(pady=20)
        
        def mostrar_detalles():
            # Obtener el grado seleccionado
            grado_seleccionado = combo.get()
            if not grado_seleccionado:
                messagebox.showerror("Error", "Por favor seleccione un grado")
                return
            
            # Verificar si existen archivos CSV para este grado
            archivos_grado = [f for f in os.listdir('listas') if f.startswith(grado_seleccionado + '_') and f.endswith('.csv')]
            
            if not archivos_grado:
                messagebox.showerror("Error", f"No hay listas de estudiantes para el grado {grado_seleccionado}")
                return
            
            seleccion_window.destroy()
            
            # Crear ventana para mostrar estadísticas
            stats_window = tk.Toplevel(self.root)
            stats_window.title(f"Estadísticas - {grado_seleccionado}")
            stats_window.geometry("800x600")
            stats_window.transient(self.root)
            
            # Frame principal
            main_frame = ttk.Frame(stats_window)
            main_frame.pack(expand=True, fill='both', padx=20, pady=20)
            
            # Ordenar por fecha (más reciente primero)
            archivos_grado.sort(reverse=True)
            
            # Seleccionar el archivo más reciente
            archivo_seleccionado = os.path.join('listas', archivos_grado[0])
            
            # Canvas y scrollbar
            canvas = tk.Canvas(main_frame, width=700)
            scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            scroll_frame = ttk.Frame(canvas, width=700)
            
            # Configurar el canvas
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Empaquetar scrollbar y canvas
            scrollbar.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)
            
            # Crear ventana en el canvas
            canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
            
            # Configurar eventos para ajustar el tamaño
            def _on_frame_configure(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
            
            def _on_canvas_configure(event):
                canvas.itemconfig(canvas_window, width=event.width)
            
            scroll_frame.bind('<Configure>', _on_frame_configure)
            canvas.bind('<Configure>', _on_canvas_configure)
            
            # Leer datos del CSV
            with open(archivo_seleccionado, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers = next(reader)
                datos = list(reader)
            
            # Procesar estadísticas por alumno
            for row in datos:
                alumno = row[0]
                faltas = []
                total_faltas = 0
                
                # Analizar cada fecha
                for i, valor in enumerate(row[1:], 1):
                    if valor == 'F':
                        fecha = headers[i]
                        faltas.append(fecha)
                        total_faltas += 1
                
                # Crear frame para cada alumno
                frame_alumno = ttk.Frame(scroll_frame)
                frame_alumno.pack(fill='x', pady=10)
                
                # Nombre del alumno
                ttk.Label(
                    frame_alumno,
                    text=f"Alumno: {alumno}",
                    font=('Arial', 12, 'bold')
                ).pack(anchor='w')
                
                if total_faltas == 0:
                    ttk.Label(
                        frame_alumno,
                        text="No registra faltas de asistencia",
                        font=('Arial', 11),
                        foreground='green'
                    ).pack(anchor='w', padx=20)
                else:
                    # Total de faltas
                    ttk.Label(
                        frame_alumno,
                        text=f"Total de faltas: {total_faltas}",
                        font=('Arial', 11)
                    ).pack(anchor='w', padx=20)
                    
                    # Detalle de faltas
                    ttk.Label(
                        frame_alumno,
                        text="Días de inasistencia:",
                        font=('Arial', 11)
                    ).pack(anchor='w', padx=20)
                    
                    for fecha in faltas:
                        ttk.Label(
                            frame_alumno,
                            text=f"- {fecha}",
                            font=('Arial', 11)
                        ).pack(anchor='w', padx=40)
                
                ttk.Separator(frame_alumno, orient='horizontal').pack(fill='x', pady=5)
            
            # Ajustar el tamaño del scroll_frame al canvas
            def _configure_scroll_frame(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
                canvas.itemconfig(canvas_window, width=event.width)
            
            canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
            scroll_frame.bind('<Configure>', _configure_scroll_frame)
            
            # Título de la ventana de estadísticas
            ttk.Label(
                scroll_frame,
                text=f"Estadísticas de Asistencia - {grado_seleccionado}",
                font=('Arial', 14, 'bold')
            ).pack(pady=(0, 20))
            
            # Verificar si hay datos para mostrar
            if not datos:
                ttk.Label(
                    scroll_frame,
                    text="No hay estudiantes registrados en esta lista",
                    font=('Arial', 12)
                ).pack(pady=20)
                return
        
        # Botón siguiente
        self.style.configure('Siguiente.TButton',
                            font=('Arial', 12, 'bold'),
                            padding=(30, 15))
        
        siguiente_btn = ttk.Button(
            frame,
            text="Siguiente",
            command=mostrar_detalles,
            style='Siguiente.TButton',
            width=15
        )
        siguiente_btn.pack(pady=30)
    
    def crear_nueva_materia(self):
        import os
        import csv
        
        # Verificar si existe el directorio y hay archivos
        if not os.path.exists('listas') or not any(f.endswith('.csv') for f in os.listdir('listas')):
            messagebox.showerror("Error", "No hay listas de grados disponibles")
            return
        
        # Crear ventana para seleccionar archivo
        seleccion_window = tk.Toplevel(self.root)
        seleccion_window.title("Seleccionar Grado")
        seleccion_window.geometry("500x250")
        seleccion_window.transient(self.root)
        
        # Frame principal
        frame = ttk.Frame(seleccion_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        # Label
        ttk.Label(frame, text="Seleccione un grado:", font=('Arial', 12)).pack(pady=10)
        
        # Obtener lista de archivos CSV
        archivos_csv = [f for f in os.listdir('listas') if f.endswith('.csv')]
        
        # Combobox para seleccionar archivo
        combo = ttk.Combobox(frame, values=archivos_csv, state='readonly', font=('Arial', 11), width=30)
        combo.pack(pady=20)
        
        def solicitar_nombre_materia():
            # Obtener el grado seleccionado
            grado_seleccionado = combo.get()
            if not grado_seleccionado:
                messagebox.showerror("Error", "Por favor seleccione un grado")
                return
                
            # Cerrar ventana de selección
            seleccion_window.destroy()
            
            # Crear ventana para nombre de materia
            materia_window = tk.Toplevel(self.root)
            materia_window.title("Nueva Materia")
            materia_window.geometry("400x200")
            materia_window.transient(self.root)
            
            # Frame principal
            materia_frame = ttk.Frame(materia_window, padding="20")
            materia_frame.pack(expand=True, fill='both')
            
            # Label y entrada para el nombre de la materia
            ttk.Label(materia_frame, text="Nombre de la materia:", font=('Arial', 12)).pack(pady=10)
            materia_entry = ttk.Entry(materia_frame, font=('Arial', 11), width=30)
            materia_entry.pack(pady=10)
            
            def crear_archivo_materia():
                nombre_materia = materia_entry.get().strip()
                if not nombre_materia:
                    messagebox.showerror("Error", "Por favor ingrese el nombre de la materia")
                    return
                
                # Crear nombre del nuevo archivo
                nombre_base = os.path.splitext(grado_seleccionado)[0]
                nuevo_archivo = f"listas/{nombre_base}-{nombre_materia}.csv"
                
                # Verificar si ya existe el archivo
                if os.path.exists(nuevo_archivo):
                    if not messagebox.askyesno("Confirmar", "Ya existe una lista para esta materia. ¿Desea sobrescribirla?"):
                        return
                
                try:
                    # Leer la lista de alumnos del grado
                    with open(os.path.join('listas', grado_seleccionado), 'r', encoding='utf-8') as file:
                        reader = csv.reader(file)
                        next(reader)  # Saltar el encabezado
                        alumnos = [row[0] for row in reader]  # Obtener solo los nombres
                    
                    # Crear el nuevo archivo de la materia
                    with open(nuevo_archivo, 'w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow(['alumnos'])  # Escribir encabezado
                        for alumno in alumnos:
                            writer.writerow([alumno])
                    
                    # Registrar la materia en materias_dictadas.txt
                    archivo_registro = 'materias_dictadas.txt'
                    nombre_archivo_csv = f"{nombre_base}-{nombre_materia}.csv"
                    
                    # Verificar si el archivo existe y obtener contenido actual
                    contenido_actual = []
                    if os.path.exists(archivo_registro):
                        with open(archivo_registro, 'r', encoding='utf-8') as file:
                            contenido_actual = file.readlines()
                    
                    # Eliminar líneas vacías y espacios en blanco
                    contenido_actual = [linea.strip() for linea in contenido_actual if linea.strip()]
                    
                    # Agregar nueva materia si no existe
                    if nombre_archivo_csv not in contenido_actual:
                        with open(archivo_registro, 'a', encoding='utf-8') as file:
                            if contenido_actual:  # Si hay contenido previo, agregar nueva línea
                                file.write('\n')
                            file.write(nombre_archivo_csv)
                    
                    messagebox.showinfo("Éxito", f"Lista de la materia {nombre_materia} creada exitosamente")
                    materia_window.destroy()
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Error al crear el archivo: {str(e)}")
            
            # Botón crear
            ttk.Button(
                materia_frame,
                text="Crear",
                command=crear_archivo_materia,
                style='Siguiente.TButton',
                width=15
            ).pack(pady=20)
        
        # Botón siguiente
        self.style.configure('Siguiente.TButton',
                            font=('Arial', 12, 'bold'),
                            padding=(30, 15))
        
        siguiente_btn = ttk.Button(
            frame,
            text="Siguiente",
            command=solicitar_nombre_materia,
            style='Siguiente.TButton',
            width=15
        )
        siguiente_btn.pack(pady=30)
    
    def cargar_materia_existente(self):
        import os
        import csv
        from datetime import datetime
        
        # Verificar si existe el archivo materias_dictadas.txt
        if not os.path.exists('materias_dictadas.txt'):
            messagebox.showerror("Error", "No hay materias registradas. Por favor, cree primero una Nueva materia con el botón 'Crear Nueva materia'")
            return
        
        # Leer las materias disponibles
        with open('materias_dictadas.txt', 'r', encoding='utf-8') as file:
            materias = [linea.strip() for linea in file.readlines() if linea.strip()]
        
        if not materias:
            messagebox.showerror("Error", "No hay materias registradas. Por favor, cree primero una Nueva materia")
            return
        
        # Crear ventana para seleccionar materia
        seleccion_window = tk.Toplevel(self.root)
        seleccion_window.title("Seleccionar Materia")
        seleccion_window.geometry("500x250")
        seleccion_window.transient(self.root)
        
        # Frame principal
        frame = ttk.Frame(seleccion_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        # Label
        ttk.Label(frame, text="Seleccione la materia que quiere cargar:", font=('Arial', 12)).pack(pady=10)
        
        # Combobox para seleccionar materia
        combo = ttk.Combobox(frame, values=materias, state='readonly', font=('Arial', 11), width=30)
        combo.pack(pady=20)
        
        def registrar_actividad():
            materia_seleccionada = combo.get()
            if not materia_seleccionada:
                messagebox.showerror("Error", "Por favor seleccione una materia")
                return
            
            archivo_seleccionado = os.path.join('listas', materia_seleccionada)
            if not os.path.exists(archivo_seleccionado):
                messagebox.showerror("Error", f"No se encuentra el archivo de la materia: {materia_seleccionada}")
                return
            
            seleccion_window.destroy()
            
            # Crear ventana para registrar actividad
            actividad_window = tk.Toplevel(self.root)
            actividad_window.title("Registrar Actividad")
            actividad_window.geometry("800x700")
            actividad_window.transient(self.root)
            
            # Frame principal
            main_frame = ttk.Frame(actividad_window, padding="20")
            main_frame.pack(expand=True, fill='both')
            
            # Frame para datos de la actividad
            datos_frame = ttk.Frame(main_frame)
            datos_frame.pack(fill='x', pady=(0, 20))
            
            # Fecha
            fecha_frame = ttk.Frame(datos_frame)
            fecha_frame.pack(fill='x', pady=5)
            ttk.Label(fecha_frame, text="Fecha (dd/mm/aaaa):", font=('Arial', 12)).pack(side='left')
            fecha_entry = ttk.Entry(fecha_frame, font=('Arial', 11), width=15)
            fecha_entry.pack(side='left', padx=10)
            
            # Nombre de la actividad
            actividad_frame = ttk.Frame(datos_frame)
            actividad_frame.pack(fill='x', pady=5)
            ttk.Label(actividad_frame, text="Nombre de la actividad:", font=('Arial', 12)).pack(side='left')
            actividad_entry = ttk.Entry(actividad_frame, font=('Arial', 11), width=30)
            actividad_entry.pack(side='left', padx=10)
            
            # Variable para controlar el estado del checkbox
            nota_porcentuada = tk.BooleanVar(value=False)
            porcentaje_entry = None
            
            def toggle_porcentaje():
                if nota_porcentuada.get():
                    porcentaje_entry.configure(state='normal')
                    porcentaje_entry.delete(0, tk.END)
                    porcentaje_entry.insert(0, '')
                else:
                    porcentaje_entry.configure(state='disabled')
                    porcentaje_entry.delete(0, tk.END)
                    porcentaje_entry.insert(0, '100')  # Valor automático cuando está desactivado
            
            # Frame para porcentaje
            porcentaje_frame = ttk.Frame(datos_frame)
            porcentaje_frame.pack(fill='x', pady=5)
            
            # Checkbox para nota porcentuada
            ttk.Checkbutton(
                porcentaje_frame,
                text="Nota porcentuada",
                variable=nota_porcentuada,
                command=toggle_porcentaje
            ).pack(side='left')
            
            # Entry para el porcentaje
            ttk.Label(porcentaje_frame, text="Porcentaje:", font=('Arial', 12)).pack(side='left', padx=(10, 0))
            porcentaje_entry = ttk.Entry(porcentaje_frame, font=('Arial', 11), width=10, state='disabled')
            porcentaje_entry.pack(side='left', padx=5)
            porcentaje_entry.insert(0, '100')
            
            # Variable para escala personalizada
            escala_personalizada = tk.BooleanVar(value=False)
            
            # Frame para escala
            escala_frame = ttk.Frame(datos_frame)
            escala_frame.pack(fill='x', pady=5)
            
            def toggle_escala():
                if escala_personalizada.get():
                    nota_min_entry.configure(state='normal')
                    nota_max_entry.configure(state='normal')
                    nota_min_entry.delete(0, tk.END)
                    nota_max_entry.delete(0, tk.END)
                else:
                    nota_min_entry.configure(state='disabled')
                    nota_max_entry.configure(state='disabled')
                    nota_min_entry.delete(0, tk.END)
                    nota_max_entry.delete(0, tk.END)
                    nota_min_entry.insert(0, '0')
                    nota_max_entry.insert(0, '5')
            
            # Checkbox para escala personalizada
            ttk.Checkbutton(
                escala_frame,
                text="Escala de calificación personalizada",
                variable=escala_personalizada,
                command=toggle_escala
            ).pack(side='left')
            
            # Frame para entradas de nota mínima y máxima
            notas_frame = ttk.Frame(escala_frame)
            notas_frame.pack(side='left', padx=10)
            
            # Entrada para nota mínima
            ttk.Label(notas_frame, text="Mín:", font=('Arial', 11)).pack(side='left')
            nota_min_entry = ttk.Entry(notas_frame, width=5, state='disabled')
            nota_min_entry.pack(side='left', padx=2)
            nota_min_entry.insert(0, '0')
            
            # Entrada para nota máxima
            ttk.Label(notas_frame, text="Máx:", font=('Arial', 11)).pack(side='left', padx=(5,0))
            nota_max_entry = ttk.Entry(notas_frame, width=5, state='disabled')
            nota_max_entry.pack(side='left', padx=2)
            nota_max_entry.insert(0, '5')
            
            # Frame con scroll para la lista de alumnos
            canvas = tk.Canvas(main_frame)
            scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            scroll_frame = ttk.Frame(canvas)
            
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Leer alumnos del archivo CSV
            with open(archivo_seleccionado, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers = next(reader)
                alumnos = [row[0] for row in reader]
            
            # Diccionario para almacenar las entradas de notas
            notas_entries = {}
            
            # Crear entradas para cada alumno
            for alumno in alumnos:
                frame_alumno = ttk.Frame(scroll_frame)
                frame_alumno.pack(fill='x', pady=5)
                
                ttk.Label(frame_alumno, text=alumno, font=('Arial', 11)).pack(side='left', padx=(0, 10))
                nota_entry = ttk.Entry(frame_alumno, width=10)
                nota_entry.pack(side='right')
                notas_entries[alumno] = nota_entry
            
            def guardar_actividad():
                # Validar fecha
                fecha = fecha_entry.get().strip()
                try:
                    datetime.strptime(fecha, '%d/%m/%Y')
                except ValueError:
                    messagebox.showerror("Error", "Formato de fecha inválido. Use dd/mm/aaaa")
                    return
                
                # Validar nombre de actividad
                nombre_actividad = actividad_entry.get().strip()
                if not nombre_actividad:
                    messagebox.showerror("Error", "Por favor ingrese el nombre de la actividad")
                    return
                
                # Obtener el porcentaje
                if not nota_porcentuada.get():
                    porcentaje = 100  # Si no está activada la opción, usar 100%
                else:
                    try:
                        porcentaje = float(porcentaje_entry.get())
                        if porcentaje <= 0 or porcentaje > 100:
                            raise ValueError
                    except ValueError:
                        messagebox.showerror("Error", "El porcentaje debe ser un número entre 0 y 100")
                        return
                
                # Obtener límites de notas
                if not escala_personalizada.get():
                    nota_min = 0
                    nota_max = 5
                else:
                    try:
                        nota_min = float(nota_min_entry.get())
                        nota_max = float(nota_max_entry.get())
                        if nota_min >= nota_max:
                            messagebox.showerror("Error", "La nota mínima debe ser menor que la nota máxima")
                            return
                    except ValueError:
                        messagebox.showerror("Error", "Los límites de notas deben ser números válidos")
                        return

                # Validar notas
                notas = {}
                for alumno, entry in notas_entries.items():
                    try:
                        nota = float(entry.get())
                        if nota < nota_min or nota > nota_max:
                            messagebox.showerror("Error", f"La nota de {alumno} debe estar entre {nota_min} y {nota_max}")
                            return
                        notas[alumno] = nota
                    except ValueError:
                        messagebox.showerror("Error", f"La nota de {alumno} debe ser un número válido")
                        return
                
                # Crear nombre de la columna
                nueva_columna = f"{porcentaje}%-{fecha}-{nombre_actividad}"
                
                # Leer contenido actual del CSV
                with open(archivo_seleccionado, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    contenido = list(reader)
                
                # Verificar si la columna ya existe
                if nueva_columna in contenido[0]:
                    if not messagebox.askyesno("Confirmar", "Ya existe un registro para esta actividad. ¿Desea sobrescribirlo?"):
                        return
                    columna_index = contenido[0].index(nueva_columna)
                else:
                    contenido[0].append(nueva_columna)
                    columna_index = len(contenido[0]) - 1
                
                # Actualizar notas
                for i, row in enumerate(contenido[1:], 1):
                    alumno = row[0]
                    # Extender la fila si es necesario
                    while len(row) <= columna_index:
                        row.append('')
                    row[columna_index] = str(notas[alumno])
                
                # Guardar cambios
                with open(archivo_seleccionado, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(contenido)
                
                messagebox.showinfo("Éxito", "Actividad registrada correctamente")
                actividad_window.destroy()
            
            # Configurar el scroll
            scroll_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Botón guardar
            ttk.Button(
                main_frame,
                text="Guardar Actividad",
                command=guardar_actividad,
                style='Custom.TButton'
            ).pack(pady=20)
        
        # Botón siguiente
        self.style.configure('Siguiente.TButton',
                            font=('Arial', 12, 'bold'),
                            padding=(30, 15))
        
        siguiente_btn = ttk.Button(
            frame,
            text="Siguiente",
            command=registrar_actividad,
            style='Siguiente.TButton',
            width=15
        )
        siguiente_btn.pack(pady=30)
    
    def estadistica_materia(self):
        # Verificar si existe el archivo de materias
        if not os.path.exists('materias_dictadas.txt'):
            messagebox.showerror("Error", "No hay materias registradas aún")
            return
        
        # Leer materias disponibles
        with open('materias_dictadas.txt', 'r', encoding='utf-8') as file:
            materias = file.read().splitlines()
        
        if not materias:
            messagebox.showerror("Error", "No hay materias registradas aún")
            return
        
        # Crear ventana de selección
        seleccion_window = tk.Toplevel(self.root)
        seleccion_window.title("Seleccionar Materia")
        seleccion_window.geometry("500x200")
        seleccion_window.transient(self.root)
        
        frame = ttk.Frame(seleccion_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="Seleccione la materia:", font=('Arial', 12)).pack(pady=10)
        
        combo = ttk.Combobox(frame, values=materias, state='readonly', font=('Arial', 11), width=30)
        combo.pack(pady=20)
        
        def mostrar_estadisticas():
            materia_seleccionada = combo.get()
            if not materia_seleccionada:
                messagebox.showerror("Error", "Por favor seleccione una materia")
                return
            
            archivo_csv = os.path.join('listas', materia_seleccionada)
            if not os.path.exists(archivo_csv):
                messagebox.showerror("Error", f"No se encuentra el archivo: {materia_seleccionada}")
                return
            
            seleccion_window.destroy()
            
            # Crear ventana de estadísticas
            stats_window = tk.Toplevel(self.root)
            stats_window.title(f"Estadísticas - {materia_seleccionada}")
            stats_window.geometry("1000x600")
            
            # Frame principal
            main_frame = ttk.Frame(stats_window, padding="20")
            main_frame.pack(expand=True, fill='both')
            
            # Leer datos con pandas
            df = pd.read_csv(archivo_csv)
            
            # Calcular nota final
            notas_finales = []
            for _, row in df.iterrows():
                nota_final = 0
                porcentajes_procesados = {}
                
                for col in df.columns[1:]:
                    if '%-' in col:
                        porcentaje = float(col.split('%-')[0])
                        if porcentaje not in porcentajes_procesados:
                            porcentajes_procesados[porcentaje] = {'suma': 0, 'count': 0}
                        
                        if not pd.isna(row[col]):
                            porcentajes_procesados[porcentaje]['suma'] += float(row[col])
                            porcentajes_procesados[porcentaje]['count'] += 1
                
                for porcentaje, datos in porcentajes_procesados.items():
                    if datos['count'] > 0:
                        promedio = datos['suma'] / datos['count']
                        nota_final += (promedio * porcentaje / 100)
                
                notas_finales.append(round(nota_final, 2))
            
            df['Nota Final'] = notas_finales
            
            # Crear tabla
            tree_frame = ttk.Frame(main_frame)
            tree_frame.pack(expand=True, fill='both')
            
            # Scrollbars
            y_scroll = ttk.Scrollbar(tree_frame)
            y_scroll.pack(side='right', fill='y')
            
            x_scroll = ttk.Scrollbar(tree_frame, orient='horizontal')
            x_scroll.pack(side='bottom', fill='x')
            
            # Treeview
            tree = ttk.Treeview(tree_frame, yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
            tree.pack(expand=True, fill='both')
            
            y_scroll.config(command=tree.yview)
            x_scroll.config(command=tree.xview)
            
            # Configurar columnas
            tree['columns'] = list(df.columns)
            tree['show'] = 'headings'
            
            for column in df.columns:
                tree.heading(column, text=column)
                tree.column(column, width=100)
            
            # Agregar datos
            for idx, row in df.iterrows():
                tree.insert('', 'end', values=list(row))
            
            def guardar_excel():
                try:
                    nombre_excel = os.path.splitext(materia_seleccionada)[0] + '.xlsx'
                    ruta_excel = filedialog.asksaveasfilename(
                        defaultextension='.xlsx',
                        initialfile=nombre_excel,
                        filetypes=[("Excel files", "*.xlsx")]
                    )
                    
                    if ruta_excel:
                        df.to_excel(ruta_excel, index=False)
                        messagebox.showinfo("\u00c9xito", "Archivo Excel guardado correctamente")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al guardar el archivo: {str(e)}")
            
            # Frame para botones y controles
            controls_frame = ttk.Frame(main_frame)
            controls_frame.pack(pady=10)
            
            # Botón para guardar en Excel
            ttk.Button(
                controls_frame,
                text="Guardar en Excel",
                command=guardar_excel
            ).pack(side='left', padx=5)
            
            # Campo para nota mínima
            ttk.Label(controls_frame, text="Nota mínima:").pack(side='left', padx=(15,5))
            nota_minima_entry = ttk.Entry(controls_frame, width=5)
            nota_minima_entry.pack(side='left')
            
            def colorear_filas():
                try:
                    nota_minima = float(nota_minima_entry.get())
                    
                    # Eliminar colores existentes
                    for item in tree.get_children():
                        tree.tag_configure(item, background='')
                    
                    # Configurar etiquetas de color
                    tree.tag_configure('rojo', background='#ffb3b3')
                    tree.tag_configure('verde', background='#b3ffb3')
                    
                    # Colorear filas
                    for item in tree.get_children():
                        valores = tree.item(item)['values']
                        nota_final = float(valores[-1])  # Última columna (Nota Final)
                        
                        if nota_final < nota_minima:
                            tree.item(item, tags=('rojo',))
                        else:
                            tree.item(item, tags=('verde',))
                            
                except ValueError:
                    messagebox.showerror("Error", "Por favor ingrese una nota mínima válida")
            
            # Botón para colorear
            ttk.Button(
                controls_frame,
                text="Colorear",
                command=colorear_filas
            ).pack(side='left', padx=5)
        
        ttk.Button(
            frame,
            text="Siguiente",
            command=mostrar_estadisticas
        ).pack(pady=10)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AsistenciaApp()
    app.run()
