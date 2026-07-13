const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const fileControls = document.getElementById('file-controls');
const dashboard = document.getElementById('dashboard');
const tableBody = document.getElementById('table-body');
const filterSelect = document.getElementById('filter-select');
const detailsContainer = document.getElementById('line-details');
const manualText = document.getElementById('manual-text');
const btnAnalyzeText = document.getElementById('btn-analyze-text');
const fileNameDisplay = document.getElementById('file-name-display');

const btnExportFile = document.getElementById('btn-exportar-file');
const btnExportText = document.getElementById('btn-exportar-text');

let allResults = [];
let chartInstance = null;

// Tab logic
function switchTab(tabId) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.input-section').forEach(sec => sec.classList.remove('active'));
    document.querySelectorAll('.input-section').forEach(sec => sec.style.display = 'none');
    
    document.getElementById(`btn-tab-${tabId}`).classList.add('active');
    document.getElementById(`sec-${tabId}`).classList.add('active');
    document.getElementById(`sec-${tabId}`).style.display = 'block';
}

function limpiarAnalisis() {
    allResults = [];
    dashboard.style.display = 'none';
    fileControls.style.display = 'none';
    dropZone.style.display = 'block';
    dropZone.innerHTML = '<p>Arrastra y suelta tu archivo <b>.txt</b> aquí o haz clic para subir</p>';
    manualText.value = '';
    
    if (chartInstance) {
        chartInstance.destroy();
        chartInstance = null;
    }
    
    tableBody.innerHTML = '';
    detailsContainer.innerHTML = '<p class="placeholder" style="color: #94a3b8; font-style: italic;">Selecciona una fila en la tabla para inspeccionar su estructura interna original y los fallos exactos.</p>';
    
    btnExportFile.disabled = true;
    btnExportText.disabled = true;
}

// File logic
dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    if (e.dataTransfer.files.length) {
        handleFile(e.dataTransfer.files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length) {
        handleFile(e.target.files[0]);
    }
});

function handleFile(file) {
    if (!file.name.endsWith('.txt')) {
        alert('Por favor selecciona un archivo .txt válido.');
        return;
    }
    
    dropZone.innerHTML = '<p>Analizando la estructura profunda del log...</p>';
    btnExportFile.disabled = true;
    
    const formData = new FormData();
    formData.append('file', file);
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) throw new Error(data.error);
        dropZone.style.display = 'none';
        fileControls.style.display = 'block';
        fileNameDisplay.textContent = `Archivo cargado: ${file.name}`;
        dashboard.style.display = 'block';
        processData(data);
    })
    .catch(err => {
        alert('Error: ' + err.message);
        limpiarAnalisis();
    });
}

// Text logic
function analyzeText() {
    const text = manualText.value.trim();
    if (!text) {
        alert("Por favor, ingresa al menos una línea de texto.");
        return;
    }
    
    btnAnalyzeText.textContent = 'Analizando...';
    btnAnalyzeText.disabled = true;
    btnExportText.disabled = true;
    
    fetch('/upload_text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) throw new Error(data.error);
        dashboard.style.display = 'block';
        processData(data);
    })
    .catch(err => {
        alert('Error: ' + err.message);
    })
    .finally(() => {
        btnAnalyzeText.textContent = 'Analizar texto';
        btnAnalyzeText.disabled = false;
    });
}

// Shared processing
function processData(data) {
    document.getElementById('c-total').textContent = data.total_lineas;
    document.getElementById('c-validos').textContent = data.eventos_validos;
    document.getElementById('c-info').textContent = data.total_info;
    document.getElementById('c-warn').textContent = data.total_warning;
    document.getElementById('c-err').textContent = data.total_error;
    document.getElementById('c-malf').textContent = data.malformados;
    
    allResults = data.resultados;
    
    // Reset filters
    filterSelect.value = "Todos";
    renderTable(allResults);
    
    detailsContainer.innerHTML = '<p class="placeholder" style="color: #94a3b8; font-style: italic;">Selecciona una fila en la tabla para inspeccionar su estructura interna original y los fallos exactos.</p>';
    
    renderChart(data.total_info, data.total_warning, data.total_error, data.malformados);
    
    btnExportFile.disabled = false;
    btnExportText.disabled = false;
}

function renderTable(data) {
    tableBody.innerHTML = '';
    data.forEach(r => {
        const tr = document.createElement('tr');
        const estado = r.es_valida ? 'Válido' : 'Inválido';
        
        let color = 'var(--text-primary)';
        if (r.severidad === 'INFO') color = 'var(--c-info)';
        if (r.severidad === 'WARNING') color = 'var(--c-warn)';
        if (r.severidad === 'ERROR') color = 'var(--c-err)';
        
        tr.innerHTML = `
            <td>${r.numero_linea}</td>
            <td>${estado}</td>
            <td style="color: ${color}; font-weight: 500;">${r.severidad}</td>
            <td>${r.fecha}</td>
            <td>${r.mensaje}</td>
        `;
        tr.addEventListener('click', () => showDetails(r));
        tableBody.appendChild(tr);
    });
}

filterSelect.addEventListener('change', (e) => {
    const val = e.target.value;
    if (val === 'Todos') renderTable(allResults);
    else if (val === 'Válidos') renderTable(allResults.filter(r => r.es_valida));
    else if (val === 'Malformados') renderTable(allResults.filter(r => !r.es_valida));
    else renderTable(allResults.filter(r => r.severidad === val));
});

function showDetails(r) {
    const estado = r.es_valida ? 'Válido' : 'Inválido';
    detailsContainer.innerHTML = `
        <span class="detail-label">Línea</span>
        <div class="detail-value">${r.numero_linea}</div>
        
        <span class="detail-label">Estado</span>
        <div class="detail-value">${estado}</div>
        
        <span class="detail-label">Severidad</span>
        <div class="detail-value">${r.severidad}</div>
        
        <span class="detail-label">Fecha Extraída</span>
        <div class="detail-value">${r.fecha}</div>
        
        <span class="detail-label">Mensaje Procesado</span>
        <div class="detail-value">${r.mensaje}</div>
        
        <span class="detail-label">Motivo (Fallo Estructural)</span>
        <div class="detail-value" style="color: var(--c-err);">${r.motivo_error || 'Ninguno. Estructura y calendario válidos.'}</div>
        
        <span class="detail-label">Texto Original (Crudo)</span>
        <div class="detail-value">${r.texto_original}</div>
    `;
}

function renderChart(info, warn, err, malf) {
    const ctx = document.getElementById('severityChart').getContext('2d');
    if (chartInstance) chartInstance.destroy();
    
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = 'Inter';
    
    chartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['INFO', 'WARNING', 'ERROR', 'Malformados'],
            datasets: [{
                data: [info, warn, err, malf],
                backgroundColor: ['#0ea5e9', '#f59e0b', '#ef4444', '#334155'],
                borderWidth: 0,
                cutout: '75%',
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { 
                    position: 'bottom',
                    labels: { padding: 20, usePointStyle: true, pointStyle: 'circle' }
                }
            },
            animation: { animateScale: true, animateRotate: true }
        }
    });
}

// Agent Logic
function requestAgentDiagnosis() {
    if (allResults.length === 0) {
        alert("No hay resultados para analizar.");
        return;
    }
    
    const btn = document.getElementById('btn-agent-diagnose');
    btn.disabled = true;
    btn.textContent = 'Pensando...';
    
    const payload = {
        total_lineas: parseInt(document.getElementById('c-total').textContent),
        eventos_validos: parseInt(document.getElementById('c-validos').textContent),
        total_error: parseInt(document.getElementById('c-err').textContent),
        total_warning: parseInt(document.getElementById('c-warn').textContent),
        malformados: parseInt(document.getElementById('c-malf').textContent),
        resultados: []
    };
    
    fetch('/agent_triage', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) throw new Error(data.error);
        
        document.getElementById('agent-results').style.display = 'block';
        
        const diag = data.diagnostico_agente;
        
        const priorityEl = document.getElementById('agent-priority');
        priorityEl.textContent = diag.prioridad;
        if (diag.prioridad === 'CRITICA') priorityEl.style.color = '#ef4444';
        else if (diag.prioridad === 'ALTA') priorityEl.style.color = '#f97316';
        else if (diag.prioridad === 'MEDIA') priorityEl.style.color = '#f59e0b';
        else priorityEl.style.color = '#10b981';
        
        document.getElementById('agent-comment').textContent = `"${data.llm_comentario}"`;
        document.getElementById('agent-skills').textContent = data.skills_usadas.join(', ');
        
        const populateList = (id, items) => {
            const ul = document.getElementById(id);
            ul.innerHTML = '';
            items.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                ul.appendChild(li);
            });
        };
        
        populateList('agent-facts', diag.hechos);
        populateList('agent-inferences', diag.inferencias);
        populateList('agent-recommendations', diag.recomendaciones);
    })
    .catch(err => {
        alert('Error del agente: ' + err.message);
    })
    .finally(() => {
        btn.disabled = false;
        btn.textContent = 'Generar Diagnóstico de Incidentes';
    });
}

function exportarDatos(formato) {
    if (allResults.length === 0) return;
    const payload = {
        total_lineas: parseInt(document.getElementById('c-total').textContent),
        eventos_validos: parseInt(document.getElementById('c-validos').textContent),
        resultados: allResults
    };
    
    fetch('/export', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resumen: payload, formato: formato })
    })
    .then(res => res.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `reporte.${formato}`;
        document.body.appendChild(a);
        a.click();
        a.remove();
    })
    .catch(err => alert('Error exportando: ' + err.message));
}

document.getElementById('btn-exportar-file').addEventListener('click', () => exportarDatos('json'));
document.getElementById('btn-exportar-text').addEventListener('click', () => exportarDatos('txt'));
