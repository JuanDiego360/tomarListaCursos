import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os

class AsistenciaApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Asistencia Estudiantil")
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
            text="¡Bienvenido al Sistema de Control de Asistencia!",
            font=('Arial', 20, 'bold')
        )
        welcome_label.pack(pady=50)
        
        # Frame para los botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=30)
        
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
                curso = curso_entry.get().strip()
                num_alumnos = int(num_alumnos_entry.get())
                
                if not curso:
                    messagebox.showerror("Error", "Por favor ingrese el nombre del curso")
                    return
                if num_alumnos <= 0:
                    messagebox.showerror("Error", "El número de alumnos debe ser mayor a 0")
                    return
                
                # Cerrar ventana actual
                nueva_lista_window.destroy()
                
                # Crear ventana para ingresar nombres
                nombres_window = tk.Toplevel(self.root)
                nombres_window.title(f"Registrar Alumnos - {curso}")
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
                    
                    # Crear directorio si no existe
                    if not os.path.exists('listas'):
                        os.makedirs('listas')
                    
                    filename = f"listas/{curso}.csv"
                    
                    # Verificar si el archivo ya existe
                    if os.path.exists(filename):
                        if not messagebox.askyesno("Confirmar", "Ya existe una lista con este nombre. ¿Desea sobrescribirla?"):
                            return
                    
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
        
        # Verificar si existe el directorio y hay archivos
        if not os.path.exists('listas') or not any(f.endswith('.csv') for f in os.listdir('listas')):
            messagebox.showerror("Error", "No hay listas de estudiantes disponibles")
            return
        
        # Crear ventana para seleccionar archivo
        seleccion_window = tk.Toplevel(self.root)
        seleccion_window.title("Seleccionar Lista")
        seleccion_window.geometry("500x250")
        seleccion_window.transient(self.root)
        
        # Frame principal
        frame = ttk.Frame(seleccion_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        # Label
        ttk.Label(frame, text="Seleccione una lista:", font=('Arial', 12)).pack(pady=10)
        
        # Obtener lista de archivos CSV
        archivos_csv = [f for f in os.listdir('listas') if f.endswith('.csv')]
        
        # Combobox para seleccionar archivo
        combo = ttk.Combobox(frame, values=archivos_csv, state='readonly', font=('Arial', 11), width=30)
        combo.pack(pady=20)
        
        def abrir_lista():
            if not combo.get():
                messagebox.showerror("Error", "Por favor seleccione una lista")
                return
            
            archivo_seleccionado = os.path.join('listas', combo.get())
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
        
        # Verificar si existe el directorio y hay archivos
        if not os.path.exists('listas') or not any(f.endswith('.csv') for f in os.listdir('listas')):
            messagebox.showerror("Error", "No hay listas de estudiantes disponibles")
            return
        
        # Crear ventana para seleccionar archivo
        seleccion_window = tk.Toplevel(self.root)
        seleccion_window.title("Seleccionar Lista para Estadísticas")
        seleccion_window.geometry("500x250")
        seleccion_window.transient(self.root)
        
        # Frame principal
        frame = ttk.Frame(seleccion_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        # Label
        ttk.Label(frame, text="Seleccione una lista:", font=('Arial', 12)).pack(pady=10)
        
        # Obtener lista de archivos CSV
        archivos_csv = [f for f in os.listdir('listas') if f.endswith('.csv')]
        
        # Combobox para seleccionar archivo
        combo = ttk.Combobox(frame, values=archivos_csv, state='readonly', font=('Arial', 11), width=30)
        combo.pack(pady=20)
        
        def mostrar_detalles():
            # Obtener el valor seleccionado antes de cualquier otra operación
            lista_seleccionada = combo.get()
            if not lista_seleccionada:
                messagebox.showerror("Error", "Por favor seleccione una lista")
                return
            
            archivo_seleccionado = os.path.join('listas', lista_seleccionada)
            seleccion_window.destroy()
            
            # Verificar si el archivo existe
            if not os.path.exists(archivo_seleccionado):
                messagebox.showerror("Error", f"No se encuentra el archivo: {lista_seleccionada}")
                return
            
            # Crear ventana para mostrar estadísticas
            stats_window = tk.Toplevel(self.root)
            stats_window.title(f"Estadísticas - {lista_seleccionada}")
            stats_window.geometry("800x600")
            stats_window.transient(self.root)
            
            # Frame principal
            main_frame = ttk.Frame(stats_window)
            main_frame.pack(expand=True, fill='both', padx=20, pady=20)
            
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
                text=f"Estadísticas de Asistencia - {lista_seleccionada}",
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
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AsistenciaApp()
    app.run()
