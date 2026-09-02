#!/usr/bin/env python3
"""Genera los tres entregables PDF de AgroSmart Monitor."""

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Flowable,
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)

NAVY = HexColor("#17324D")
GREEN = HexColor("#2F855A")
MINT = HexColor("#E8F5EE")
BLUE = HexColor("#2B6CB0")
PALE_BLUE = HexColor("#EAF2FB")
AMBER = HexColor("#B7791F")
PALE_AMBER = HexColor("#FFF7E6")
RED = HexColor("#C53030")
PALE_RED = HexColor("#FFF0F0")
INK = HexColor("#243442")
MUTED = HexColor("#607283")
LINE = HexColor("#D9E2EA")
PAPER = HexColor("#F7FAFC")


BASE = getSampleStyleSheet()
STYLES = {
    "title": ParagraphStyle(
        "TitleCustom", parent=BASE["Title"], fontName="Helvetica-Bold",
        fontSize=29, leading=33, textColor=NAVY, alignment=TA_LEFT,
        spaceAfter=14,
    ),
    "subtitle": ParagraphStyle(
        "Subtitle", parent=BASE["Normal"], fontName="Helvetica",
        fontSize=13, leading=19, textColor=MUTED, spaceAfter=18,
    ),
    "h1": ParagraphStyle(
        "H1Custom", parent=BASE["Heading1"], fontName="Helvetica-Bold",
        fontSize=19, leading=23, textColor=NAVY, spaceBefore=6, spaceAfter=10,
    ),
    "h2": ParagraphStyle(
        "H2Custom", parent=BASE["Heading2"], fontName="Helvetica-Bold",
        fontSize=13.5, leading=17, textColor=GREEN, spaceBefore=10, spaceAfter=6,
    ),
    "h3": ParagraphStyle(
        "H3Custom", parent=BASE["Heading3"], fontName="Helvetica-Bold",
        fontSize=11, leading=14, textColor=BLUE, spaceBefore=7, spaceAfter=4,
    ),
    "body": ParagraphStyle(
        "BodyCustom", parent=BASE["BodyText"], fontName="Helvetica",
        fontSize=9.5, leading=14, textColor=INK, alignment=TA_LEFT,
        spaceAfter=6,
    ),
    "small": ParagraphStyle(
        "Small", parent=BASE["BodyText"], fontName="Helvetica",
        fontSize=7.8, leading=11, textColor=INK, spaceAfter=3,
    ),
    "caption": ParagraphStyle(
        "Caption", parent=BASE["BodyText"], fontName="Helvetica-Oblique",
        fontSize=7.5, leading=10, textColor=MUTED, spaceAfter=5,
    ),
    "cover_label": ParagraphStyle(
        "CoverLabel", parent=BASE["Normal"], fontName="Helvetica-Bold",
        fontSize=9, leading=12, textColor=GREEN, spaceAfter=12,
    ),
    "code": ParagraphStyle(
        "Code", parent=BASE["Code"], fontName="Courier",
        fontSize=7.2, leading=9.5, textColor=INK,
    ),
    "table_head": ParagraphStyle(
        "TableHead", parent=BASE["Normal"], fontName="Helvetica-Bold",
        fontSize=8, leading=10, textColor=colors.white,
    ),
    "table": ParagraphStyle(
        "TableBody", parent=BASE["Normal"], fontName="Helvetica",
        fontSize=7.7, leading=10.5, textColor=INK,
    ),
}


def P(text, style="body"):
    return Paragraph(text, STYLES[style])


def bullets(items, level=0):
    return ListFlowable(
        [ListItem(P(item), leftIndent=9) for item in items],
        bulletType="bullet", bulletColor=GREEN, leftIndent=18 + level * 10,
        bulletFontName="Helvetica-Bold", bulletFontSize=7, spaceAfter=7,
    )


def numbered(items):
    return ListFlowable(
        [ListItem(P(item), leftIndent=10) for item in items],
        bulletType="1", start="1", leftIndent=23, bulletFontName="Helvetica-Bold",
        bulletColor=GREEN, spaceAfter=7,
    )


def box(title, text, tone="green"):
    palette = {
        "green": (MINT, GREEN), "blue": (PALE_BLUE, BLUE),
        "amber": (PALE_AMBER, AMBER), "red": (PALE_RED, RED),
    }
    bg, accent = palette[tone]
    data = [[P(title, "h3")], [P(text)]]
    t = Table(data, colWidths=[16.4 * cm], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.8, accent),
        ("LINEBEFORE", (0, 0), (0, -1), 4, accent),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return KeepTogether([t, Spacer(1, 8)])


def table(rows, widths, header=True):
    cooked = []
    for r_i, row in enumerate(rows):
        style = "table_head" if header and r_i == 0 else "table"
        cooked.append([cell if isinstance(cell, Flowable) else P(str(cell), style) for cell in row])
    t = Table(cooked, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.45, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        commands += [("BACKGROUND", (0, 0), (-1, 0), NAVY)]
        start = 1
    else:
        start = 0
    for idx in range(start, len(rows)):
        if (idx - start) % 2:
            commands.append(("BACKGROUND", (0, idx), (-1, idx), PAPER))
    t.setStyle(TableStyle(commands))
    return t


def flow_diagram(items):
    cells = []
    widths = []
    for idx, item in enumerate(items):
        cells.append(P(item, "small"))
        widths.append(2.65 * cm)
        if idx < len(items) - 1:
            cells.append(P("-&gt;", "h3"))
            widths.append(0.55 * cm)
    t = Table([cells], colWidths=widths, hAlign="LEFT")
    commands = [("VALIGN", (0, 0), (-1, -1), "MIDDLE")]
    for idx in range(0, len(cells), 2):
        commands += [
            ("BACKGROUND", (idx, 0), (idx, 0), MINT),
            ("BOX", (idx, 0), (idx, 0), 0.7, GREEN),
            ("ALIGN", (idx, 0), (idx, 0), "CENTER"),
            ("LEFTPADDING", (idx, 0), (idx, 0), 6),
            ("RIGHTPADDING", (idx, 0), (idx, 0), 6),
            ("TOPPADDING", (idx, 0), (idx, 0), 8),
            ("BOTTOMPADDING", (idx, 0), (idx, 0), 8),
        ]
    t.setStyle(TableStyle(commands))
    return t


def cover(story, label, title, subtitle, meta):
    story += [Spacer(1, 2.4 * cm), P(label.upper(), "cover_label"), P(title, "title"),
              P(subtitle, "subtitle"), Spacer(1, 0.35 * cm)]
    story.append(Table([[""]], colWidths=[3.6 * cm], rowHeights=[0.12 * cm],
                       style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), GREEN)])))
    story += [Spacer(1, 1.2 * cm), box("AgroSmart Monitor", meta, "green"),
              Spacer(1, 4.3 * cm), P("Documento preparado el 2 de septiembre de 2026", "small"),
              P("Repositorio: github.com/AlexitoXD1/agrosmart-monitor", "small"), PageBreak()]


def page_canvas(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setStrokeColor(LINE)
    canvas.line(2 * cm, h - 1.25 * cm, w - 2 * cm, h - 1.25 * cm)
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.setFillColor(NAVY)
    canvas.drawString(2 * cm, h - 0.9 * cm, "AGROSMART MONITOR")
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(w - 2 * cm, h - 0.9 * cm, doc.title[:62])
    canvas.line(2 * cm, 1.25 * cm, w - 2 * cm, 1.25 * cm)
    canvas.drawString(2 * cm, 0.82 * cm, "Herramientas de Desarrollo Profesional - TIC")
    canvas.drawRightString(w - 2 * cm, 0.82 * cm, f"Pagina {doc.page}")
    canvas.restoreState()


def build_pdf(path, title, story):
    doc = SimpleDocTemplate(
        str(path), pagesize=A4, rightMargin=2 * cm, leftMargin=2 * cm,
        topMargin=1.65 * cm, bottomMargin=1.6 * cm,
        title=title, author="Equipo AgroSmart Monitor",
        subject="AgroSmart Monitor - DevOps y CI/CD",
    )
    doc.build(story, onFirstPage=page_canvas, onLaterPages=page_canvas)


def report_story():
    s = []
    cover(
        s, "Tarea Academica 1", "Implementacion DevOps y evidencias de CI/CD",
        "Informe de cumplimiento basado en el repositorio y en ejecuciones reales de GitHub Actions.",
        "Aplicacion Java 17 con Maven, pruebas JUnit 5, pipeline automatizado, despliegue simulado y publicacion de artefactos.",
    )
    s += [P("1. Resumen ejecutivo", "h1"),
          P("AgroSmart Monitor simula lecturas de temperatura y humedad de una camara de frio agricola. La aplicacion clasifica cada lectura como NORMAL, WARNING o ALERT y genera un reporte de texto cuando detecta una alerta. El repositorio integra el cambio de codigo con pruebas, empaquetado, despliegue simulado y publicacion del JAR mediante GitHub Actions."),
          box("Resultado verificable", "La ejecucion #2, asociada al commit 00f4204, fallo en pruebas y bloqueo las etapas posteriores. La correccion del commit 9d77ab7 activo la ejecucion #3, que termino correctamente y publico un artefacto JAR de 6.34 KB.", "blue"),
          P("2. Objetivos y alcance", "h1"),
          bullets([
              "Implementar un pipeline CI/CD sobre la rama <b>main</b>.",
              "Proteger la regla de negocio con pruebas automatizadas antes del build.",
              "Relacionar cambio, commit, ejecucion, job, paso, log e impacto.",
              "Entregar un artefacto recuperable solo cuando la validacion termina correctamente.",
          ]),
          box("Limite del alcance", "El despliegue es deliberadamente simulado: copia el JAR a <b>staging/</b>. No hay infraestructura de produccion, sensores fisicos ni recomendacion sanitaria real.", "amber"),
          PageBreak(),
          P("3. Solucion implementada", "h1"),
          P("3.1 Arquitectura funcional", "h2"),
          flow_diagram(["SensorSimulator", "TemperatureReading", "Classifier", "Estado", "Reporte ALERT"]),
          Spacer(1, 10),
          table([
              ["Componente", "Responsabilidad", "Evidencia"],
              ["SensorSimulator", "Genera temperatura de 2 a 12 C y humedad de 45 a 90 %.", "Prueba determinista con semilla 42."],
              ["TemperatureClassifier", "Aplica NORMAL <= 8; WARNING <= 10; ALERT > 10.", "Tres pruebas de limites y casos representativos."],
              ["AlertReportGenerator", "Crea reports/alerta_yyyyMMdd_HHmmss.txt ante ALERT.", "Invocacion condicionada en Main."],
              ["Main", "Ejecuta cinco lecturas, imprime estados y reporta alertas.", "Punto de entrada declarado en el manifiesto JAR."],
          ], [3.4*cm, 8.1*cm, 4.9*cm]),
          P("3.2 Estructura del repositorio", "h2"),
          Preformatted("""agrosmart-monitor/
|-- .github/workflows/ci.yml
|-- pom.xml
|-- README.md
|-- src/main/java/com/agrosmart/
|   |-- Main.java
|   |-- SensorSimulator.java
|   |-- TemperatureReading.java
|   |-- TemperatureClassifier.java
|   |-- SensorStatus.java
|   `-- AlertReportGenerator.java
`-- src/test/java/com/agrosmart/
    |-- TemperatureClassifierTest.java
    `-- SensorSimulatorTest.java""", STYLES["code"]),
          PageBreak(),
          P("4. Pipeline CI/CD", "h1"),
          P("El workflow <b>CI Pipeline - AgroSmart Monitor</b> se activa con push o pull request sobre main y ejecuta un unico job llamado <b>build-test-deploy</b> en Ubuntu."),
          flow_diagram(["Checkout", "Java 17", "mvn test", "mvn package", "staging + artifact"]),
          Spacer(1, 10),
          table([
              ["Paso", "Comando o accion", "Criterio de exito"],
              ["Descargar codigo", "actions/checkout@v4", "Commit disponible en el runner."],
              ["Preparar Java", "actions/setup-java@v4, Temurin 17, cache Maven", "JDK y dependencias preparados."],
              ["Pruebas", "mvn -B test", "Todas las pruebas pasan; si falla, el job termina."],
              ["Build", "mvn -B package -DskipTests", "target/agrosmart-monitor.jar existe."],
              ["Deploy simulado", "Copiar target/*.jar a staging/", "El JAR aparece en staging."],
              ["Publicacion", "actions/upload-artifact@v4", "Artefacto agrosmart-monitor-jar disponible."],
          ], [3.5*cm, 7.2*cm, 5.7*cm]),
          P("4.1 Practicas DevOps demostradas", "h2"),
          bullets([
              "Control de versiones mediante commits y repositorio GitHub compartido.",
              "Integracion continua con ejecucion automatica en cada cambio relevante.",
              "Pruebas como puerta de calidad antes de empaquetar y desplegar.",
              "Retroalimentacion rapida por estado, anotaciones y logs del job.",
              "Entrega automatizada del JAR como artefacto vinculado a la ejecucion.",
          ]),
          PageBreak(),
          P("5. Evidencia de la ejecucion fallida", "h1"),
          box("GitHub Actions #2 - Failure", "URL: https://github.com/AlexitoXD1/agrosmart-monitor/actions/runs/33288383964<br/>Commit: 00f4204 (modificacion)<br/>Fecha: 29 de agosto de 2026, 21:36 GMT-5<br/>Duracion: 15 s<br/>Job: build-test-deploy, 11 s<br/>Anotaciones: 1 error y 2 advertencias<br/>Artefactos: ninguno", "red"),
          Image(str(ROOT / "docs/evidencias/github_actions_run_2_fallo.png"), width=16.4*cm, height=13.67*cm),
          P("Captura 1. Resumen publico de GitHub Actions: estado Failure, commit 00f4204, job fallido, exit code 1 y ausencia de artefactos.", "caption"),
          PageBreak(),
          P("5.1 Cambio que provoco el fallo", "h2"),
          Preformatted("assertEquals(SensorStatus.NORMAL,\n    TemperatureClassifier.classify(10.1));", STYLES["code"]),
          P("La prueba esperaba NORMAL para 10.1 C, aunque la regla del sistema devuelve ALERT por ser una temperatura superior a 10 C. GitHub Actions registro <b>Process completed with exit code 1</b>. El problema fue una expectativa inconsistente en la prueba, no una falla del runner."),
          P("5.2 Impacto", "h2"),
          bullets([
              "Maven marco la etapa de pruebas como fallida.",
              "Compilar y empaquetar fue omitido.",
              "El despliegue simulado no se ejecuto.",
              "No se publico ningun artefacto.",
              "Los pasos Post y Complete job solo limpiaron el runner; no convierten la ejecucion en exitosa.",
          ]),
          box("Interpretacion", "La puerta de calidad funciono: una discrepancia en la regla de negocio impidio producir y entregar una salida no validada.", "amber"),
          PageBreak(),
          P("6. Correccion y evidencia exitosa", "h1"),
          P("La correccion restablecio ALERT como valor esperado para 10.1 C:"),
          Preformatted("assertEquals(SensorStatus.ALERT,\n    TemperatureClassifier.classify(10.1));", STYLES["code"]),
          box("GitHub Actions #3 - Success", "URL: https://github.com/AlexitoXD1/agrosmart-monitor/actions/runs/33288476013<br/>Commit: 9d77ab7 (modificacion 2)<br/>Fecha: 29 de agosto de 2026, 21:38 GMT-5<br/>Duracion total: 17 s<br/>Job: build-test-deploy, 14 s<br/>Estado: Success<br/>Artefacto: agrosmart-monitor-jar, 6.34 KB<br/>Digest: sha256:42e5f8c82ab1cabebc6cff58dffb6e5be795ea1d1a1a82af2b5fd86e5da60ecf", "green"),
          Image(str(ROOT / "docs/evidencias/github_actions_run_3_exito.png"), width=16.4*cm, height=13.67*cm),
          P("Captura 2. Resumen publico de GitHub Actions: estado Success, commit 9d77ab7, artefacto publicado y tamaño de 6.34 KB.", "caption"),
          PageBreak(),
          P("6.1 Secuencia de recuperacion", "h2"),
          numbered([
              "Corregir la expectativa para alinearla con la regla ALERT > 10 C.",
              "Registrar el cambio en Git y enviarlo a main.",
              "Esperar el nuevo workflow disparado por el push.",
              "Confirmar pruebas, build, deploy simulado y publicacion del artefacto.",
          ]),
          P("7. Comparacion de trazabilidad", "h1"),
          table([
              ["Aspecto", "Ejecucion #2", "Ejecucion #3"],
              ["Commit", "00f4204", "9d77ab7"],
              ["Cambio", "Esperaba NORMAL para 10.1 C", "Restituyo ALERT para 10.1 C"],
              ["Estado", "Failure", "Success"],
              ["Duracion", "15 s", "17 s"],
              ["Pruebas", "Paso fallido; exit code 1", "Validacion completada"],
              ["Build y deploy", "Omitidos", "Ejecutados"],
              ["Artefacto", "No publicado", "JAR de 6.34 KB"],
              ["Efecto DevOps", "Bloqueo una entrega inconsistente", "Permitio entregar una salida validada"],
          ], [3.3*cm, 6.55*cm, 6.55*cm]),
          P("8. Checklist de entrega", "h1"),
          table([
              ["Requisito", "Estado", "Ubicacion / evidencia"],
              ["URL del repositorio", "Cumplido", "github.com/AlexitoXD1/agrosmart-monitor"],
              ["Workflow en .github/workflows", "Cumplido", ".github/workflows/ci.yml"],
              ["Historial de commits", "Cumplido", "810db2c ... 9d77ab7; incluye fallo y correccion"],
              ["Ejecucion fallida explicada", "Cumplido", "Actions run 33288383964 / commit 00f4204"],
              ["Ejecucion exitosa posterior", "Cumplido", "Actions run 33288476013 / commit 9d77ab7"],
              ["README de ejecucion y pipeline", "Cumplido", "README.md"],
          ], [5.4*cm, 2.5*cm, 8.5*cm]),
          PageBreak(),
          P("9. Conclusiones", "h1"),
          bullets([
              "El pipeline conecta repositorio, pruebas, construccion y entrega automatizada.",
              "Una prueba fallida detuvo correctamente las etapas posteriores.",
              "La pareja de ejecuciones #2 y #3 demuestra el ciclo detectar, diagnosticar, corregir, validar y entregar.",
              "La trazabilidad queda vinculada a commits, URLs de ejecucion y al digest del artefacto.",
          ]),
          P("Fuentes de evidencia", "h2"),
          P("Repositorio: <link href='https://github.com/AlexitoXD1/agrosmart-monitor' color='#2B6CB0'>https://github.com/AlexitoXD1/agrosmart-monitor</link><br/>Ejecuciones: <link href='https://github.com/AlexitoXD1/agrosmart-monitor/actions' color='#2B6CB0'>https://github.com/AlexitoXD1/agrosmart-monitor/actions</link><br/>Documento de referencia: TA1_Modelo_AgroSmart_Monitor_DevOps_Pipeline_CRMBQB.pdf."),
    ]
    return s


def careers_story():
    s = []
    cover(
        s, "Parte 1", "Rutas laborales y certificaciones TIC",
        "Dos rutas profesionales vinculadas con AgroSmart Monitor y tres certificaciones vigentes de nivel inicial.",
        "Investigacion orientada a construir un perfil de DevOps Engineer o Cloud Architect desde una base de Java, GitHub Actions y servicios cloud.",
    )
    s += [P("1. Proposito", "h1"),
          P("El objetivo es traducir las competencias practicadas en AgroSmart Monitor - versionamiento, automatizacion, pruebas y entrega - en rutas laborales concretas. Las certificaciones no sustituyen experiencia: ayudan a ordenar el aprendizaje y a demostrar fundamentos verificables."),
          box("Criterio de seleccion", "Se priorizaron credenciales introductorias, sin prerrequisitos obligatorios de experiencia, emitidas por AWS, Microsoft y GitHub. La informacion fue contrastada con fuentes oficiales consultadas el 2 de septiembre de 2026.", "blue"),
          P("2. Ruta profesional: DevOps Engineer", "h1"),
          P("Un DevOps Engineer diseña y mantiene el camino que lleva un cambio desde el repositorio hasta un entorno confiable. Integra desarrollo y operaciones, reduce tareas manuales y construye mecanismos de observabilidad, seguridad y recuperacion."),
          P("Responsabilidades habituales", "h2"),
          bullets([
              "Crear y mantener pipelines CI/CD, estrategias de ramas y controles de calidad.",
              "Automatizar compilacion, pruebas, empaquetado, despliegue y rollback.",
              "Gestionar contenedores, infraestructura como codigo, secretos y configuracion.",
              "Observar disponibilidad, rendimiento y errores; participar en respuesta a incidentes.",
              "Facilitar colaboracion entre equipos de desarrollo, QA, seguridad y operaciones.",
          ]),
          P("Requisitos de entrada recomendados", "h2"),
          table([
              ["Area", "Base necesaria", "Practica sugerida"],
              ["Sistemas", "Linux, procesos, archivos, permisos y redes TCP/IP.", "Administrar una VM y diagnosticar puertos/logs."],
              ["Programacion", "Scripting en Bash o Python; lectura de Java u otro lenguaje.", "Automatizar build y validaciones."],
              ["Versionamiento", "Git, ramas, pull requests y revision de codigo.", "Flujo feature branch -> PR -> main."],
              ["CI/CD", "Jobs, dependencias, artefactos, variables y secretos.", "Extender GitHub Actions con ambientes."],
              ["Plataforma", "Docker, registro de imagenes y fundamentos de Kubernetes.", "Contenerizar AgroSmart Monitor."],
              ["Cloud/IaC", "IAM, redes, compute, storage y Terraform.", "Desplegar un entorno reproducible."],
          ], [3.0*cm, 7.0*cm, 6.4*cm]),
          PageBreak(),
          P("3. Ruta profesional: Cloud Architect", "h1"),
          P("Un Cloud Architect convierte necesidades de negocio en una arquitectura cloud segura, resiliente, escalable y costo-eficiente. Su trabajo abarca decisiones de plataforma, integracion, gobernanza, continuidad y comunicacion con partes tecnicas y no tecnicas."),
          P("Responsabilidades habituales", "h2"),
          bullets([
              "Definir arquitecturas de aplicaciones, datos, redes, identidad y seguridad.",
              "Seleccionar servicios administrados y patrones de integracion adecuados.",
              "Diseñar para alta disponibilidad, recuperacion ante desastres y crecimiento.",
              "Aplicar gobernanza, etiquetado, presupuestos y optimizacion de costos.",
              "Documentar decisiones, riesgos y compromisos mediante diagramas y ADR.",
          ]),
          P("Requisitos de entrada recomendados", "h2"),
          table([
              ["Area", "Base necesaria", "Evidencia de dominio"],
              ["Cloud", "IaaS, PaaS, SaaS; regiones, zonas y responsabilidad compartida.", "Explicar una arquitectura de tres capas."],
              ["Redes", "CIDR, subredes, DNS, balanceo, VPN y controles de trafico.", "Diseñar red publica/privada."],
              ["Seguridad", "IAM, minimo privilegio, cifrado, claves, auditoria y cumplimiento.", "Matriz de acceso y amenazas."],
              ["Datos", "Relacional/no relacional, object storage, cache y respaldo.", "Elegir servicio por carga y RPO/RTO."],
              ["Confiabilidad", "Escalado, redundancia, health checks y observabilidad.", "Prueba de fallos y plan de recuperacion."],
              ["Comunicacion", "Requisitos, costos, riesgos y decisiones trazables.", "Diagrama, ADR y presentacion ejecutiva."],
          ], [3.0*cm, 7.4*cm, 6.0*cm]),
          PageBreak(),
          P("4. Comparacion de rutas", "h1"),
          table([
              ["Dimension", "DevOps Engineer", "Cloud Architect"],
              ["Foco", "Flujo de entrega, automatizacion y operacion.", "Diseño integral, gobernanza y decisiones."],
              ["Trabajo diario", "Pipelines, IaC, observabilidad, incidentes.", "Requisitos, diagramas, patrones, revisiones."],
              ["Profundidad", "Herramientas y operacion hands-on.", "Amplitud tecnica y trade-offs de negocio."],
              ["Entrada tipica", "Developer, sysadmin, SRE junior o QA automation.", "Cloud engineer, senior developer o infra engineer."],
              ["Portafolio ideal", "Pipeline con tests, contenedor, IaC y monitoreo.", "Arquitectura desplegable con costos, seguridad y DR."],
              ["Certificaciones iniciales", "GitHub Foundations + una cloud fundamentals.", "AWS CCP + Azure Fundamentals; luego nivel associate."],
          ], [3.5*cm, 6.45*cm, 6.45*cm]),
          box("Punto de encuentro", "Ambas rutas necesitan Git, seguridad, cloud, automatizacion y comunicacion. DevOps profundiza en el flujo operativo; arquitectura cloud profundiza en decisiones de diseño y gobernanza.", "green"),
          PageBreak(),
          P("5. Certificacion 1: AWS Certified Cloud Practitioner", "h1"),
          P("Codigo de examen: <b>CLF-C02</b>. Valida conocimiento general de AWS sin estar ligado a un rol concreto."),
          table([
              ["Requisito / dato", "Detalle"],
              ["Prerequisito formal", "AWS no exige otra certificacion ni experiencia obligatoria."],
              ["Experiencia recomendada", "Hasta seis meses de exposicion al diseño, implementacion u operacion en AWS para el candidato objetivo."],
              ["Conocimientos", "Conceptos cloud, seguridad y cumplimiento, servicios centrales, costos, facturacion y soporte."],
              ["Formato", "Opcion multiple y respuesta multiple; 50 preguntas puntuadas y 15 no puntuadas."],
              ["Aprobacion", "Puntaje escalado minimo de 700 sobre 1000."],
              ["Preparacion practica", "Cuenta AWS con presupuesto/alertas, IAM basico, EC2, S3, VPC y calculadora de precios."],
          ], [4.4*cm, 12.0*cm]),
          P("Dominios", "h2"),
          bullets(["Conceptos cloud: 24 %.", "Seguridad y cumplimiento: 30 %.", "Tecnologia y servicios cloud: 34 %.", "Facturacion, precios y soporte: 12 %." ]),
          P("Fuente oficial", "h2"),
          P("<link href='https://docs.aws.amazon.com/aws-certification/latest/cloud-practitioner-02/cloud-practitioner-02.html' color='#2B6CB0'>Guia oficial AWS Certified Cloud Practitioner CLF-C02</link>"),
          P("6. Certificacion 2: Microsoft Certified Azure Fundamentals", "h1"),
          P("Examen: <b>AZ-900</b>. Es una credencial de nivel principiante para demostrar fundamentos de nube y de Azure."),
          table([
              ["Requisito / dato", "Detalle"],
              ["Prerequisito formal", "No exige otra certificacion; se presenta como punto de entrada comun a Azure."],
              ["Experiencia recomendada", "Familiaridad con un area de TI, como infraestructura, bases de datos o desarrollo de software."],
              ["Conocimientos", "Conceptos cloud; arquitectura y servicios de Azure; administracion y gobernanza."],
              ["Evaluacion", "45 minutos; examen supervisado; puede incluir componentes interactivos."],
              ["Idiomas", "Incluye español, ingles y otros idiomas listados en Microsoft Learn."],
              ["Preparacion practica", "Microsoft Learn, practica oficial y laboratorio con recursos gratuitos/control de costos."],
          ], [4.4*cm, 12.0*cm]),
          P("Fuente oficial", "h2"),
          P("<link href='https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/' color='#2B6CB0'>Microsoft Certified: Azure Fundamentals</link>"),
          PageBreak(),
          P("7. Certificacion 3: GitHub Foundations", "h1"),
          P("Valida fundamentos para colaborar, contribuir y trabajar con GitHub. Es directamente aplicable al repositorio y al flujo de AgroSmart Monitor."),
          table([
              ["Requisito / dato", "Detalle"],
              ["Prerequisito formal", "GitHub no indica certificacion previa obligatoria."],
              ["Conocimientos", "Colaboracion, productos de GitHub, fundamentos de Git y trabajo con repositorios."],
              ["Registro", "Se realiza desde la pagina de certificaciones y se agenda con Pearson VUE."],
              ["Modalidad", "Centro de evaluacion o examen supervisado en linea; el equipo pasa una comprobacion previa."],
              ["Identificacion", "Documento gubernamental vigente con nombre, fotografia y firma; los nombres deben coincidir con el registro."],
              ["Preparacion practica", "Commits, branches, PR, issues, permisos, Markdown, GitHub flow y conceptos de Actions."],
          ], [4.4*cm, 12.0*cm]),
          P("Fuentes oficiales", "h2"),
          P("<link href='https://docs.github.com/en/get-started/showcase-your-expertise-with-github-certifications/about-github-certifications' color='#2B6CB0'>Acerca de GitHub Certifications</link><br/><link href='https://docs.github.com/es/get-started/showcase-your-expertise-with-github-certifications/registering-for-a-github-certifications-exam' color='#2B6CB0'>Registro y requisitos de identificacion</link>"),
          P("8. Plan recomendado de 6 meses", "h1"),
          table([
              ["Periodo", "Objetivo", "Resultado demostrable"],
              ["Mes 1", "Linux, redes, Git y GitHub.", "Repositorio con ramas, PR y documentacion."],
              ["Mes 2", "Cloud fundamentals y seguridad basica.", "Laboratorio con IAM, compute, storage y presupuesto."],
              ["Mes 3", "CI/CD y pruebas.", "Pipeline como AgroSmart Monitor con artefactos."],
              ["Mes 4", "Docker e infraestructura como codigo.", "Imagen versionada y entorno reproducible."],
              ["Mes 5", "Observabilidad, confiabilidad y costos.", "Metricas, logs, alertas y estimacion de costo."],
              ["Mes 6", "Preparacion de examen y portafolio.", "Practicas, simulacro y README con arquitectura."],
          ], [2.6*cm, 6.5*cm, 7.3*cm]),
          box("Secuencia sugerida", "GitHub Foundations -> AZ-900 o AWS CLF-C02 -> proyecto practico -> certificacion associate alineada con la ruta elegida.", "blue"),
          P("Nota de actualidad", "h2"),
          P("Los proveedores pueden cambiar temarios, precios, politicas y versiones de examen. Antes de pagar o agendar, se debe volver a consultar la pagina oficial correspondiente."),
    ]
    return s


def manual_story():
    s = []
    cover(
        s, "Manual integral", "Manual de usuario y de desarrollador",
        "Guia completa para instalar, ejecutar, interpretar, probar, modificar y mantener AgroSmart Monitor.",
        "Version documentada: 0.1.0. Aplicacion de consola Java 17, Maven, JUnit 5 y GitHub Actions.",
    )
    s += [P("Indice funcional", "h1"),
          table([
              ["Parte", "Contenido"],
              ["I. Usuario", "Proposito, requisitos, instalacion, ejecucion, salidas, reportes y solucion de problemas."],
              ["II. Desarrollador", "Arquitectura, clases, reglas, build, pruebas, pipeline, trazabilidad y extensiones."],
              ["III. Operacion", "Diagnostico, seguridad, mantenimiento, cambios seguros y checklist de entrega."],
          ], [3.3*cm, 13.1*cm]),
          P("1. Que es AgroSmart Monitor", "h1"),
          P("Es una aplicacion didactica de consola que simula el monitoreo de una camara de frio agricola. No necesita sensor fisico. Cada ejecucion crea cinco lecturas aleatorias con temperatura y humedad, clasifica la temperatura y genera un archivo cuando el estado es ALERT."),
          table([
              ["Rango / condicion", "Estado", "Accion"],
              ["Temperatura <= 8.0 C", "NORMAL", "Mostrar lectura; no crear reporte."],
              ["8.0 C < temperatura <= 10.0 C", "WARNING", "Mostrar advertencia; no crear reporte."],
              ["Temperatura > 10.0 C", "ALERT", "Mostrar alerta y crear reporte en reports/."],
          ], [6.0*cm, 3.0*cm, 7.4*cm]),
          box("Importante", "Los umbrales son didacticos y no constituyen una recomendacion sanitaria ni un sistema de control de produccion.", "amber"),
          PageBreak(),
          P("PARTE I - MANUAL DE USUARIO", "h1"),
          P("2. Requisitos", "h2"),
          bullets([
              "Java Development Kit 17 o posterior.",
              "Apache Maven 3.8 o posterior.",
              "Terminal con acceso a la carpeta del proyecto.",
              "Git solo si se desea clonar o actualizar el repositorio.",
          ]),
          Preformatted("java -version\nmvn -version\ngit --version", STYLES["code"]),
          P("2.1 Obtener el proyecto", "h2"),
          Preformatted("git clone https://github.com/AlexitoXD1/agrosmart-monitor.git\ncd agrosmart-monitor", STYLES["code"]),
          P("Si ya se tiene esta carpeta, no es necesario clonar: basta con abrir una terminal en la raiz, donde estan <b>pom.xml</b> y <b>README.md</b>."),
          P("3. Primera ejecucion", "h1"),
          numbered([
              "Ejecutar <b>mvn test</b> para validar la instalacion y la logica.",
              "Ejecutar <b>mvn package</b> para compilar y producir el JAR.",
              "Ejecutar <b>java -jar target/agrosmart-monitor.jar</b>.",
          ]),
          Preformatted("mvn test\nmvn package\njava -jar target/agrosmart-monitor.jar", STYLES["code"]),
          box("Resultado esperado", "La terminal muestra cinco lecturas. Al finalizar aparece <b>=== Fin de la simulacion ===</b>. Si alguna lectura supera 10 C, tambien se indica la ruta de un reporte nuevo.", "green"),
          PageBreak(),
          P("4. Como interpretar la salida", "h1"),
          Preformatted("""=== AgroSmart Monitor - monitoreo de camara de frio (simulado) ===
Lectura 1/5 -> [2026-09-02 10:30:12] Temp: 6.4 C | Humedad: 61.2% | Estado: NORMAL
Lectura 2/5 -> [2026-09-02 10:30:12] Temp: 11.3 C | Humedad: 58.9% | Estado: ALERT
  -> Reporte de alerta generado: reports/alerta_20260902_103012.txt
=== Fin de la simulacion ===""", STYLES["code"]),
          table([
              ["Campo", "Significado"],
              ["Lectura 1/5", "Posicion actual y total del ciclo."],
              ["Fecha y hora", "Momento local en que se creo el objeto TemperatureReading."],
              ["Temp", "Valor simulado en grados Celsius, mostrado con un decimal."],
              ["Humedad", "Valor simulado en porcentaje, mostrado con un decimal."],
              ["Estado", "Resultado de aplicar los umbrales de TemperatureClassifier."],
              ["Ruta de reporte", "Archivo creado unicamente para ALERT."],
          ], [4.0*cm, 12.4*cm]),
          P("5. Reportes de alerta", "h1"),
          P("Los archivos se guardan en <b>reports/</b> con el formato <b>alerta_yyyyMMdd_HHmmss.txt</b>. El directorio se crea automaticamente."),
          Preformatted("""ALERTA AUTOMATICA - AgroSmart Monitor
Estado: ALERT
Lectura: [2026-09-02 10:30:12] Temp: 11.3 C | Humedad: 58.9%""", STYLES["code"]),
          box("Colision posible", "El nombre solo tiene precision de segundos. Si se generan dos alertas dentro del mismo segundo, el segundo reporte puede sobrescribir al primero. Para un uso real conviene añadir milisegundos o un identificador unico.", "amber"),
          PageBreak(),
          P("6. Problemas frecuentes del usuario", "h1"),
          table([
              ["Sintoma", "Causa probable", "Solucion"],
              ["mvn: command not found", "Maven no esta instalado o no esta en PATH.", "Instalar Maven y reabrir la terminal; comprobar mvn -version."],
              ["UnsupportedClassVersionError", "El JAR fue compilado con una version de Java mas nueva.", "Usar Java 17+ y confirmar java -version."],
              ["Unable to access jarfile", "No se ejecuto package o se esta en otra carpeta.", "Ejecutar mvn package desde la raiz."],
              ["No aparece reports/", "No hubo temperatura > 10 C en esa ejecucion.", "Repetir la simulacion; la generacion es aleatoria."],
              ["Pruebas fallan", "Cambio incompatible o dependencia/cache dañada.", "Leer el primer fallo; luego probar mvn -U clean test."],
              ["Caracteres raros", "Terminal sin UTF-8.", "Configurar la terminal en UTF-8."],
          ], [4.0*cm, 5.5*cm, 6.9*cm]),
          P("7. Uso responsable", "h1"),
          bullets([
              "No usar las lecturas simuladas para decisiones sobre alimentos o seguridad.",
              "No almacenar secretos, tokens ni contraseñas dentro del repositorio.",
              "No asumir que staging/ es un despliegue real; es una demostracion local del pipeline.",
              "Conservar reportes solo durante el tiempo necesario; pueden crecer con ejecuciones repetidas.",
          ]),
          PageBreak(),
          P("PARTE II - MANUAL DE DESARROLLADOR", "h1"),
          P("8. Arquitectura y flujo de datos", "h2"),
          flow_diagram(["Random", "Reading", "Classify", "Console", "Report if ALERT"]),
          Spacer(1, 10),
          P("El diseño separa generacion de datos, representacion, clasificacion y efectos de salida. La dependencia principal va desde <b>Main</b> hacia los componentes; <b>TemperatureClassifier</b> permanece como utilidad sin estado."),
          table([
              ["Clase", "Contrato", "Dependencias"],
              ["Main", "Orquesta cinco lecturas y espera 300 ms entre ellas.", "SensorSimulator, classifier, report generator."],
              ["TemperatureReading", "Dato inmutable de timestamp, temperatura y humedad.", "LocalDateTime, DateTimeFormatter."],
              ["SensorSimulator", "Entrega una lectura por llamada; permite semilla en tests.", "java.util.Random."],
              ["TemperatureClassifier", "Funcion pura double -> SensorStatus.", "Sin dependencias externas."],
              ["SensorStatus", "Enum NORMAL, WARNING, ALERT.", "Ninguna."],
              ["AlertReportGenerator", "Crea directorio y escribe el reporte de ALERT.", "java.nio.file, LocalDateTime."],
          ], [3.4*cm, 8.0*cm, 5.0*cm]),
          PageBreak(),
          P("9. Detalle de las clases", "h1"),
          P("9.1 TemperatureReading", "h2"),
          P("El constructor recibe temperatura y humedad y captura <b>LocalDateTime.now()</b>. Los campos son finales. <b>toString()</b> produce la representacion usada tanto en consola como en el reporte."),
          P("9.2 SensorSimulator", "h2"),
          P("El constructor sin argumentos usa una semilla no determinista. El constructor <b>SensorSimulator(long seed)</b> existe para pruebas repetibles. <b>nextReading()</b> usa intervalos continuos y redondea a dos decimales."),
          P("9.3 TemperatureClassifier", "h2"),
          Preformatted("""if (temperature <= 8.0) return NORMAL;
if (temperature <= 10.0) return WARNING;
return ALERT;""", STYLES["code"]),
          P("El orden de comparacion incluye exactamente 8.0 en NORMAL y 10.0 en WARNING. Cualquier cambio de umbral debe actualizar pruebas y documentacion en el mismo commit."),
          P("9.4 AlertReportGenerator", "h2"),
          P("Crea <b>reports/</b> con <b>Files.createDirectories</b> y escribe con <b>Files.writeString</b>. Propaga IOException; Main tambien la declara. El estado se recibe como argumento, aunque Main solo llama al metodo para ALERT."),
          P("9.5 Main", "h2"),
          P("La constante <b>READINGS_TO_SIMULATE</b> controla el tamaño del ciclo. El retraso de 300 ms mejora la lectura de la consola, pero hace que el metodo declare InterruptedException."),
          PageBreak(),
          P("10. Compilacion y empaquetado", "h1"),
          table([
              ["Comando", "Uso", "Salida"],
              ["mvn clean", "Elimina resultados previos.", "Borra target/."],
              ["mvn test", "Compila y ejecuta JUnit 5.", "Reportes en target/surefire-reports/."],
              ["mvn package", "Prueba y empaqueta.", "target/agrosmart-monitor.jar."],
              ["mvn package -DskipTests", "Empaqueta sin volver a ejecutar tests.", "Usado en CI despues de mvn test."],
              ["java -jar target/agrosmart-monitor.jar", "Ejecuta el manifiesto Main-Class.", "Lecturas y posibles reports/."],
          ], [5.2*cm, 6.4*cm, 4.8*cm]),
          P("10.1 Configuracion de pom.xml", "h2"),
          bullets([
              "groupId: com.agrosmart; artifactId: agrosmart-monitor; version: 0.1.0.",
              "Compilacion source/target Java 17 y codificacion UTF-8.",
              "JUnit Jupiter 5.10.2 con alcance test.",
              "Surefire 3.2.5 para pruebas; maven-jar-plugin 3.4.1 para el manifiesto ejecutable.",
          ]),
          P("11. Estrategia de pruebas", "h1"),
          table([
              ["Suite", "Cobertura actual", "Riesgo protegido"],
              ["TemperatureClassifierTest", "NORMAL 6/8; WARNING 9/10; ALERT 10.1/15.", "Errores en limites de la regla de negocio."],
              ["SensorSimulatorTest", "20 lecturas con semilla 42 dentro de rangos.", "Valores fuera de temperatura/humedad permitidas."],
          ], [4.4*cm, 7.0*cm, 5.0*cm]),
          box("Pruebas adicionales recomendadas", "Agregar casos NaN/infinito, formato de TemperatureReading, contenido y colisiones de reportes, permisos de escritura e integracion de Main con reloj y filesystem inyectables.", "blue"),
          PageBreak(),
          P("12. Pipeline GitHub Actions", "h1"),
          Preformatted("""push/main o pull_request/main
  -> checkout@v4
  -> setup-java@v4 (Temurin 17 + cache Maven)
  -> mvn -B test
  -> mvn -B package -DskipTests
  -> copiar target/*.jar a staging/
  -> upload-artifact@v4""", STYLES["code"]),
          P("La ejecucion secuencial aplica fail-fast por defecto: si <b>mvn test</b> devuelve un codigo distinto de cero, los pasos normales posteriores se omiten. Los pasos internos Post pueden ejecutarse para limpiar recursos."),
          P("12.1 Como leer un fallo", "h2"),
          numbered([
              "Abrir Actions y seleccionar la ejecucion asociada al commit.",
              "Abrir el job build-test-deploy y localizar el primer paso rojo.",
              "Leer la primera causa, no solo el ultimo BUILD FAILURE.",
              "Relacionar clase, metodo, linea, valor esperado y valor real.",
              "Corregir localmente, ejecutar mvn test y subir un commit descriptivo.",
          ]),
          P("12.2 Evidencia real del proyecto", "h2"),
          table([
              ["Run", "Commit", "Estado", "Resultado"],
              ["#2", "00f4204", "Failure", "Exit code 1; no hubo artefacto."],
              ["#3", "9d77ab7", "Success", "JAR publicado, 6.34 KB, digest SHA-256 visible."],
          ], [2.0*cm, 3.0*cm, 3.0*cm, 8.4*cm]),
          PageBreak(),
          P("13. Guia para cambios seguros", "h1"),
          P("Cambiar un umbral", "h2"),
          numbered([
              "Acordar la nueva regla y documentar el motivo.",
              "Modificar TemperatureClassifier.",
              "Actualizar casos de borde y nombres de pruebas.",
              "Actualizar README y manuales si cambia el comportamiento externo.",
              "Ejecutar mvn test y revisar el diff antes del commit.",
          ]),
          P("Cambiar cantidad o rango simulado", "h2"),
          P("Editar READINGS_TO_SIMULATE en Main o las formulas de SensorSimulator. Conservar pruebas de limites y ajustar el texto que describe los rangos. Para una solucion mantenible, mover estos valores a argumentos de linea de comandos o variables de entorno con validacion."),
          P("Conectar un sensor real", "h2"),
          bullets([
              "Definir una interfaz ReadingSource con nextReading().",
              "Hacer que SensorSimulator la implemente.",
              "Crear un adaptador MQTT/HTTP separado con timeouts y reintentos.",
              "Inyectar la fuente en el orquestador y mantener tests con una fuente falsa.",
              "Validar datos, timestamps, unidades y comportamiento ante desconexion.",
          ]),
          P("14. Seguridad y operacion", "h1"),
          bullets([
              "Fijar permisos minimos del GITHUB_TOKEN y no imprimir secretos en logs.",
              "Revisar actualizaciones de actions/checkout, setup-java y upload-artifact.",
              "Agregar escaneo de dependencias y, si se usan contenedores, de imagenes.",
              "Conservar el digest del artefacto para trazabilidad e integridad.",
              "Separar ambientes y exigir aprobacion para un despliegue real a produccion.",
              "Definir retencion de reportes y artefactos para controlar datos y costos.",
          ]),
          PageBreak(),
          P("PARTE III - REFERENCIA RAPIDA", "h1"),
          P("15. Checklist antes de entregar", "h2"),
          bullets([
              "git status no contiene cambios accidentales ni archivos generados.",
              "mvn test termina con cero fallos y cero errores.",
              "mvn package crea target/agrosmart-monitor.jar.",
              "La aplicacion inicia con java -jar y finaliza el ciclo.",
              "README coincide con umbrales, rangos y comandos actuales.",
              "El workflow existe bajo .github/workflows/ y su YAML es valido.",
              "La ejecucion de Actions esta vinculada al commit correcto.",
              "El artefacto aparece solo despues de una ejecucion exitosa.",
          ]),
          P("16. Comandos esenciales", "h2"),
          Preformatted("""# Estado e historial
git status --short
git log --oneline --graph -10

# Validacion local
mvn clean test
mvn package
java -jar target/agrosmart-monitor.jar

# Publicacion normal
git add <archivos>
git commit -m "Describir el cambio y su objetivo"
git push origin main""", STYLES["code"]),
          P("17. Enlaces", "h2"),
          P("Repositorio: <link href='https://github.com/AlexitoXD1/agrosmart-monitor' color='#2B6CB0'>github.com/AlexitoXD1/agrosmart-monitor</link><br/>Pipeline: <link href='https://github.com/AlexitoXD1/agrosmart-monitor/actions' color='#2B6CB0'>github.com/AlexitoXD1/agrosmart-monitor/actions</link><br/>Workflow: <b>.github/workflows/ci.yml</b><br/>Configuracion Maven: <b>pom.xml</b><br/>Ayuda inicial: <b>README.md</b>."),
          box("Definicion de terminado", "Un cambio esta listo cuando la regla y sus pruebas coinciden, el build es reproducible, la documentacion refleja el comportamiento y el pipeline publica un artefacto trazable sin eludir la puerta de calidad.", "green"),
    ]
    return s


def main():
    outputs = [
        (OUT / "01_informe_cumplimiento_TA1_AgroSmart_Monitor.pdf", "Informe de cumplimiento TA1", report_story()),
        (OUT / "02_investigacion_rutas_laborales_y_certificaciones_TIC.pdf", "Rutas laborales y certificaciones TIC", careers_story()),
        (OUT / "03_manual_usuario_y_desarrollador_AgroSmart_Monitor.pdf", "Manual de usuario y desarrollador", manual_story()),
    ]
    for path, title, story in outputs:
        build_pdf(path, title, story)
        print(path)


if __name__ == "__main__":
    main()
