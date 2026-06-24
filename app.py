"""
=====================================================================
 Exportador de Datos a iCalendar
 ConfiguroWeb · 2026 · Python real en el navegador (PyScript)
=====================================================================
"""
from pyscript import document, window
from js import localStorage
import json
import math

APP_CLAVE = "python_exportador_datos_icalendar_datos"
VERSION = "1.0.0"


# =====================================================================
#  Lógica de negocio
# =====================================================================
class Calculadora:
    """Modelo de cálculo de Exportador de Datos a iCalendar."""

    def __init__(self, titulo, fecha, hora, duracion):
        self.titulo = float(titulo)
        self.fecha = float(fecha)
        self.hora = float(hora)
        self.duracion = float(duracion)

    def calcular(self):
        """Ejecuta el cálculo principal y devuelve un dict de resultados."""

        ics = (
            "BEGIN:VCALENDAR\nVERSION:2.0\nBEGIN:VEVENT\n"
            f"SUMMARY:{self.titulo}\n"
            f"DTSTART:{self.fecha}T{self.hora}\n"
            f"DURATION:PT{int(self.duracion)}M\n"
            "END:VEVENT\nEND:VCALENDAR"
        )
        return {"ics": ics}


    def diagnostico(self, resultados):
        """Texto explicativo del resultado."""
        return "✅ Bloque iCalendar generado. Guárdalo como .ics"


# =====================================================================
#  Formateadores
# =====================================================================
def fmt_moneda(v):
    if v is None:
        return "—"
    if math.isinf(v):
        return "∞"
    return f"${v:,.0f}"

def fmt_num(v):
    if v is None:
        return "—"
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return f"{v:,}"

def fmt_pct(v):
    if v is None:
        return "—"
    return f"{v:.1f}%"


# =====================================================================
#  Persistencia localStorage
# =====================================================================
def cargar_guardado():
    try:
        raw = localStorage.getItem(APP_CLAVE)
        if raw:
            return json.loads(raw)
    except Exception:
        pass
    return None

def guardar_ls(datos):
    try:
        localStorage.setItem(APP_CLAVE, json.dumps(datos))
        return True
    except Exception:
        return False


# =====================================================================
#  UI helpers
# =====================================================================
def input_float(eid):
    el = document.querySelector(f"#{eid}")
    if not el or not el.value:
        return 0.0
    try:
        return float(el.value)
    except (ValueError, TypeError):
        return 0.0

def mostrar(html, clase=""):
    caja = document.querySelector("#resultado")
    caja.innerHTML = html
    caja.classList.remove("hidden", "is-error", "is-success")
    if clase:
        caja.classList.add(clase)


# =====================================================================
#  Handlers
# =====================================================================
def calcular_handler(event=None):
    """Lee inputs, instancia, calcula y muestra."""

    c = Calculadora(
        document.querySelector("#titulo").value or "",
        document.querySelector("#fecha").value or "",
        document.querySelector("#hora").value or "",
        input_float("duracion"),
    )
    r = c.calcular()
    html = f"""
      <div class="result-value">📅 Evento iCalendar</div>
      <pre style="white-space:pre-wrap;background:#fff;padding:1rem;border-radius:8px;border:1px solid var(--cweb-border);font-size:.85rem;">{r["ics"]}</pre>
      <p class="result-detail">{c.diagnostico(r)}</p>
    """
    mostrar(html, clase="is-success")



def guardar_datos(event=None):
    datos = {
            "titulo": input_float("titulo"),
            "fecha": input_float("fecha"),
            "hora": input_float("hora"),
            "duracion": input_float("duracion"),
        "version": VERSION,
    }
    ok = guardar_ls(datos)
    if ok:
        mostrar("💾 Datos guardados en este navegador.", clase="is-success")
    else:
        mostrar("❌ No se pudieron guardar los datos.", clase="is-error")


def cargar_al_inicio():
    datos = cargar_guardado()
    if not datos:
        return
    try:
        if "titulo" in datos:
            document.querySelector("#titulo").value = datos["titulo"]
        if "fecha" in datos:
            document.querySelector("#fecha").value = datos["fecha"]
        if "hora" in datos:
            document.querySelector("#hora").value = datos["hora"]
        if "duracion" in datos:
            document.querySelector("#duracion").value = datos["duracion"]
        aviso = document.querySelector("#resultado")
        aviso.innerHTML = "📂 Datos cargados. Pulsa <em>Calcular</em>."
        aviso.classList.remove("hidden")
    except Exception:
        pass


def inicializar():
    cargar_al_inicio()
    window.dispatchEvent(window.Event.new("py:ready"))

inicializar()
