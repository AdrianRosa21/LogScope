import os
import tempfile
from flask import Flask, render_template, request, jsonify
from analyzer import analizar_archivo

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

def _serializar_resumen(resumen):
    """Convierte el objeto ResumenAnalisis a un dict serializable en JSON"""
    resultados_list = []
    for r in resumen.resultados:
        resultados_list.append({
            'numero_linea': r.numero_linea,
            'es_valida': r.es_valida,
            'severidad': r.severidad if r.severidad else "-",
            'fecha': r.fecha.strftime("%Y-%m-%d") if r.fecha else "-",
            'tiene_fecha': r.tiene_fecha,
            'mensaje': r.mensaje if r.mensaje else "-",
            'motivo_error': r.motivo_error if r.motivo_error else "",
            'texto_original': r.texto_original
        })
        
    return {
        'total_lineas': resumen.total_lineas,
        'eventos_validos': resumen.eventos_validos,
        'total_info': resumen.total_info,
        'total_warning': resumen.total_warning,
        'total_error': resumen.total_error,
        'malformados': resumen.total_lineas - resumen.eventos_validos,
        'resultados': resultados_list
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if not file.filename.endswith('.txt'):
        return jsonify({'error': 'Only .txt files allowed'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    try:
        resumen = analizar_archivo(filepath)
        return jsonify(_serializar_resumen(resumen))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload_text', methods=['POST'])
def upload_text():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
        
    texto = data['text']
    
    # DECISIÓN CLAVE: Para no duplicar el código de validación del backend ni tocar analyzer.py,
    # escribimos el texto en un archivo temporal en RAM y usamos la misma función.
    fd, temp_path = tempfile.mkstemp(suffix=".txt")
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(texto)
            
        resumen = analizar_archivo(temp_path)
        return jsonify(_serializar_resumen(resumen))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass

if __name__ == '__main__':
    # Arranca el servidor local
    app.run(debug=True, port=5000)
