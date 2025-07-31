"""
Módulo para obtener y mostrar datos de ClickUp
Maneja la conexión con la API de ClickUp y la visualización de tareas
"""

import requests
import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

class ClickUpManager:
    """Manejador para la API de ClickUp"""
    
    def __init__(self):
        # Cargar variables de entorno
        load_dotenv()
        self.api_token = os.getenv("CLICKUP_API_TOKEN")
        self.headers = {"Authorization": self.api_token}
        self.space_ids = ["90131499377", "90131519206", "90131497226", "90131499734"]
        
    def obtener_nombre_espacio(self, space_id):
        """Obtiene el nombre de un espacio por su ID"""
        try:
            url_space = f"https://api.clickup.com/api/v2/space/{space_id}"
            res = requests.get(url_space, headers=self.headers)
            res.raise_for_status()
            return res.json().get("name", f"Espacio {space_id}")
        except Exception as e:
            st.warning(f"No se pudo obtener el nombre del espacio {space_id}: {e}")
            return f"Espacio {space_id}"
    
    def obtener_listas_espacio(self, space_id):
        """Obtiene las listas de un espacio"""
        try:
            url_lists = f"https://api.clickup.com/api/v2/space/{space_id}/list"
            response_lists = requests.get(url_lists, headers=self.headers)
            response_lists.raise_for_status()
            return response_lists.json()["lists"]
        except Exception as e:
            st.error(f"Error obteniendo listas del espacio {space_id}: {e}")
            return []
    
    def obtener_tareas_lista(self, list_id):
        """Obtiene todas las tareas de una lista"""
        all_tasks = []
        page = 0
        
        try:
            while True:
                url_tasks = f"https://api.clickup.com/api/v2/list/{list_id}/task?page={page}&include_closed=true"
                response_tasks = requests.get(url_tasks, headers=self.headers)
                response_tasks.raise_for_status()
                tasks = response_tasks.json().get("tasks", [])
                
                if not tasks:
                    break
                    
                all_tasks.extend(tasks)
                page += 1
                
        except Exception as e:
            st.error(f"Error obteniendo tareas de la lista {list_id}: {e}")
            
        return all_tasks
    
    def procesar_tarea(self, task, list_name, folder_name, space_name):
        """Procesa una tarea individual y extrae sus datos"""
        task_id = task.get("id", "")
        name = task.get("name", "")
        content = task.get("text_content", "")
        
        # Status
        status_data = task.get("status", {})
        status = status_data.get("label") or status_data.get("name") or status_data.get("status") or ""
        
        # Fechas
        created_ts = task.get("date_created")
        due_ts = task.get("due_date")
        start_ts = task.get("start_date")
        closed_ts = task.get("date_closed")
        
        created = pd.to_datetime(int(created_ts) / 1000, unit='s') if created_ts else None
        due = pd.to_datetime(int(due_ts) / 1000, unit='s') if due_ts else None
        start = pd.to_datetime(int(start_ts) / 1000, unit='s') if start_ts else None
        closed = pd.to_datetime(int(closed_ts) / 1000, unit='s') if closed_ts else None
        
        # Otros datos
        parent_id = task.get("parent", "")
        attachments = [a["url"] for a in task.get("attachments", [])]
        assignees = [a["username"] for a in task.get("assignees", [])]
        tags = [t["name"] for t in task.get("tags", [])]
        
        priority_data = task.get("priority")
        priority = priority_data.get("priority") if isinstance(priority_data, dict) else ""
        
        time_estimate = task.get("time_estimate", "")
        time_spent = task.get("time_spent", "")
        
        return {
            "ID": task_id,
            "Nombre": name,
            "Contenido": content,
            "Estado": status,
            "Fecha Creación": created,
            "Fecha Vencimiento": due,
            "Fecha Inicio": start,
            "Fecha Cierre": closed,
            "ID Padre": parent_id,
            "Adjuntos": ", ".join(attachments),
            "Asignados": ", ".join(assignees),
            "Etiquetas": ", ".join(tags),
            "Prioridad": priority,
            "Lista": list_name,
            "Carpeta": folder_name,
            "Espacio": space_name,
            "Tiempo Estimado": time_estimate,
            "Tiempo Usado": time_spent
        }
    
    def obtener_todas_las_tareas(self):
        """Obtiene todas las tareas de todos los espacios configurados"""
        if not self.api_token:
            st.error("❌ No se encontró el token de API de ClickUp. Verificá el archivo .env")
            return pd.DataFrame()
        
        tareas_data = []
        
        # Mostrar progreso
        progress_container = st.container()
        
        with progress_container:
            st.info("🔄 Obteniendo datos de ClickUp...")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total_spaces = len(self.space_ids)
            
            for idx, space_id in enumerate(self.space_ids):
                progress = (idx + 1) / total_spaces
                progress_bar.progress(progress)
                
                # Obtener nombre del espacio
                space_name = self.obtener_nombre_espacio(space_id)
                status_text.text(f"🗂️ Procesando espacio: {space_name}")
                
                # Obtener listas del espacio
                lists = self.obtener_listas_espacio(space_id)
                
                for lst in lists:
                    list_id = lst["id"]
                    list_name = lst["name"]
                    folder_name = lst.get("folder", {}).get("name", "")
                    
                    status_text.text(f"📋 Procesando lista: {list_name}")
                    
                    # Obtener tareas de la lista
                    tasks = self.obtener_tareas_lista(list_id)
                    
                    # Procesar cada tarea
                    for task in tasks:
                        tarea_procesada = self.procesar_tarea(task, list_name, folder_name, space_name)
                        tareas_data.append(tarea_procesada)
            
            progress_bar.progress(1.0)
            status_text.text("✅ Datos obtenidos correctamente")
        
        # Limpiar el contenedor de progreso después de un momento
        import time
        time.sleep(1)
        progress_container.empty()
        
        return pd.DataFrame(tareas_data)


# Instancia global del manejador de ClickUp
clickup_manager = ClickUpManager()
