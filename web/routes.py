import os
from flask import Blueprint, render_template, request, jsonify, current_app, Response
from application.analysis_service import analizar_archivo, analizar_texto, serializar_resumen

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if not file.filename.endswith('.txt'):
        return jsonify({'error': 'Only .txt files allowed'}), 400

    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    try:
        resumen = analizar_archivo(filepath)
        return jsonify(serializar_resumen(resumen))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception:
                pass

@bp.route('/upload_text', methods=['POST'])
def upload_text():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
        
    texto = data['text']
    try:
        # Directamente analizamos el texto en RAM sin archivos temporales
        resumen = analizar_texto(texto)
        return jsonify(serializar_resumen(resumen))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/agent_triage', methods=['POST'])
def agent_triage():
    data = request.json
    try:
        from agent.agent import LogScopeAgent
        agent = LogScopeAgent()
        # Utilizamos la skill de triaje a través del agente
        diagnostico = agent.router.route_request("triage", {"resumen": data})
        comentario = agent.adapter.generate(f"Resume este diagnóstico: {diagnostico}")
        return jsonify({
            "diagnostico_agente": diagnostico,
            "llm_comentario": comentario,
            "skills_usadas": ["Triaje y Resumen"]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/export', methods=['POST'])
def export_report():
    data = request.json
    resumen = data.get('resumen')
    formato = data.get('formato', 'json')
    if not resumen:
         return jsonify({'error': 'No hay datos para exportar'}), 400
         
    if formato == 'json':
        return jsonify(resumen)
    elif formato == 'txt':
        lines = [f"Total: {resumen['total_lineas']}, Validos: {resumen['eventos_validos']}"]
        for r in resumen.get('resultados', []):
            lines.append(f"Linea {r['numero_linea']} - Valida: {r['es_valida']} - Sev: {r['severidad']} - Fecha: {r['fecha']} - Msj: {r['mensaje']}")
        return Response("\n".join(lines), mimetype='text/plain')
    return jsonify({'error': 'Formato no soportado'}), 400
