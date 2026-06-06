
// =========================================================
// ENRUTADOR DINÁMICO (SPA) - FARMA SUR
// =========================================================

// 1. Diccionario de datos para la inyección de vistas
const vistas = {
    dashboard: `
        <div class="dashboard-grid" id="dashboard-view">
            <div class="card card-banner">
                <div class="banner-content">
                    <h2 class="banner-label">Productos procesados hoy</h2>
                    <div class="banner-value">824</div>
                    <div class="banner-indicators">
                        <div class="indicator-item"><i class='bx bx-star'></i> <span>Popularidad 93</span></div>
                        <div class="indicator-item"><i class='bx bx-trending-up'></i> <span>Eficiencia 4.7</span></div>
                    </div>
                    <button class="btn-action-main">VER ESTADÍSTICAS COMPLETAS &gt;</button>
                </div>
                <div class="banner-graphic">
                    <div class="graphic-placeholder"><i class='bx bx-cube'></i></div>
                </div>
            </div>
            <div class="card card-peach">
                <h2 class="peach-header">Índice de Rotación</h2>
                <div class="peach-body">
                    <div class="peach-value">87°</div>
                    <div class="gauge-simulation"></div>
                </div>
                <p class="peach-text">El índice ha incrementado debido a la reciente actualización. <strong>¡Sigue adelante</strong> y consigue más puntos!</p>
            </div>
            <div class="bottom-row">
                <div class="card">
                    <h3 class="section-title-sm">Rendimiento Financiero</h3>
                    <div class="bar-chart-container">
                        <div class="chart-bar-wrapper"><div class="bar-pill bar-dic"></div><span class="bar-title">Dic</span></div>
                        <div class="chart-bar-wrapper"><div class="bar-pill bar-ene"></div><span class="bar-title">Ene</span></div>
                        <div class="chart-bar-wrapper"><div class="bar-pill bar-feb"></div><span class="bar-title">Feb</span></div>
                        <div class="chart-bar-wrapper"><div class="bar-pill bar-mar"></div><span class="bar-title">Mar</span></div>
                        <div class="chart-bar-wrapper"><div class="bar-pill active-bar bar-abr"></div><span class="bar-title">Abr</span></div>
                        <div class="chart-bar-wrapper"><div class="bar-pill bar-may"></div><span class="bar-title">May</span></div>
                    </div>
                </div>
                <div class="card">
                    <h3 class="section-title-sm">Operadores Destacados</h3>
                    <div class="data-list">
                        <div class="list-entry"><div class="entry-details"><div class="entry-icon-box"><i class='bx bx-user'></i></div><div><p class="entry-name">Davi</p><p class="entry-sub">En línea</p></div></div><span class="entry-score">4.3</span></div>
                        <div class="list-entry"><div class="entry-details"><div class="entry-icon-box"><i class='bx bx-user'></i></div><div><p class="entry-name">Gaby</p><p class="entry-sub">En línea</p></div></div><span class="entry-score">4.7</span></div>
                        <div class="list-entry"><div class="entry-details"><div class="entry-icon-box"><i class='bx bx-user'></i></div><div><p class="entry-name">Cesar</p><p class="entry-sub">Hace 2 min</p></div></div><span class="entry-score">4.4</span></div>
                    </div>
                </div>
                <div class="card">
                    <h3 class="section-title-sm">Distribución por Región</h3>
                    <div class="map-wrapper">
                        <span class="map-location-label">Punto Fijo</span>


<div class="map-node node-1"></div>
                        <div class="map-node node-2"></div>
                    </div>
                </div>
            </div>
        </div>
    ,
    inventario: 
        <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
                <h2 style="font-size: 1.4rem; font-weight: 700; color: var(--text-main);">Control de Inventario</h2>
                <button class="btn-action-main" style="background-color: var(--accent-color); padding: 10px 18px;"><i class='bx bx-plus' style='vertical-align: middle; margin-right: 6px; font-size: 1rem;'></i>Registrar Lote</button>
            </div>
            <div class="card" style="padding: 20px; overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.85rem;">
                    <thead>
                        <tr style="color: var(--text-muted); border-bottom: 1px solid #f1f5f9;">
                            <th style="padding: 12px;">Medicamento</th>
                            <th style="padding: 12px;">Categoría</th>
                            <th style="padding: 12px;">Stock Actual</th>
                            <th style="padding: 12px;">Estado</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom: 1px solid #f1f5f9;">
                            <td style="padding: 14px; font-weight: 600;">Ibuprofeno 400mg</td>
                            <td style="padding: 14px; color: var(--text-muted);">Analgésico</td>
                            <td style="padding: 14px; font-weight: 700;">142 uds</td>
                            <td style="padding: 14px;"><span style="background: #e2fbe8; color: #1e7e34; padding: 4px 10px; border-radius: 10px; font-size: 0.75rem; font-weight: 600;">Estable</span></td>
                        </tr>
                        <tr style="border-bottom: 1px solid #f1f5f9;">
                            <td style="padding: 14px; font-weight: 600;">Amoxicilina 500mg</td>
                            <td style="padding: 14px; color: var(--text-muted);">Antibiótico</td>
                            <td style="padding: 14px; font-weight: 700; color: #dc2626;">18 uds</td>
                            <td style="padding: 14px;"><span style="background: #fee2e2; color: #dc2626; padding: 4px 10px; border-radius: 10px; font-size: 0.75rem; font-weight: 600;">Stock Crítico</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    ,
    reportes: 
        <div>
            <h2 style="font-size: 1.4rem; font-weight: 700; color: var(--text-main); margin-bottom: 24px;">Historial y Reportes</h2>
            <div class="bottom-row" style="grid-template-columns: 1fr 1fr;">
                <div class="card">
                    <h3 class="section-title-sm"><i class='bx bx-file' style='margin-right: 6px; color: var(--text-muted);'></i>Auditorías de Stock</h3>
                    <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 20px; line-height: 1.5;">Exporta hojas de balance automatizadas sobre las entradas y salidas críticas del almacén.</p>
                    <button class="btn-action-main" style="width: 100%;">Descargar Reporte Semanal (.xlsx)</button>
                </div>
                <div class="card">
                    <h3 class="section-title-sm"><i class='bx bx-time-five' style='margin-right: 6px; color: var(--text-muted);'></i>Actividad Reciente</h3>
                    <div class="data-list" style="gap: 12px; font-size: 0.8rem;">
                        <p style="border-left: 3px solid var(--accent-color); padding-left: 8px;"><strong>Gaby</strong> editó inventario de Amoxicilina (Hace 5 min)</p>


<p style="border-left: 3px solid var(--peach-accent); padding-left: 8px;"><strong>Davi</strong> validó un egreso de lote (Hace 42 min)</p>
                    </div>
                </div>
            </div>
        </div>
    ,
    configuracion: 
        <div>
            <h2 style="font-size: 1.4rem; font-weight: 700; color: var(--text-main); margin-bottom: 24px;">Ajustes del Sistema</h2>
            <div class="card" style="max-width: 550px;">
                <h3 class="section-title-sm">Parámetros Globales</h3>
                <div style="display: flex; flex-direction: column; gap: 16px;">
                    <label style="font-size: 0.8rem; font-weight: 600; color: var(--text-muted); display: flex; flex-direction: column; gap: 6px;">
                        Identificador de la Sucursal
                        <input type="text" value="Farma Sur - Punto Fijo" style="width: 100%; padding: 10px; border: 1px solid #e2e8f0; border-radius: 8px; color: var(--text-main); font-weight: 500;">
                    </label>
                    <label style="font-size: 0.8rem; font-weight: 600; color: var(--text-muted); display: flex; flex-direction: column; gap: 6px;">
                        Umbral de Alerta Temprana
                        <select style="width: 100%; padding: 10px; border: 1px solid #e2e8f0; border-radius: 8px; color: var(--text-main); font-weight: 500;">
                            <option>Notificar cuando queden menos de 20 unidades</option>
                            <option>Notificar cuando queden menos de 50 unidades</option>
                        </select>
                    </label>
                </div>
            </div>
        </div>
    `
};

// 2. Control de navegación y transiciones UX
document.addEventListener("DOMContentLoaded", () => {
    const contenedor = document.getElementById("view-container");
    const botonesMenu = document.querySelectorAll(".nav-item");
    let estaTransicionando = false;

    botonesMenu.forEach(boton => {
        boton.addEventListener("click", () => {
            const vistaDestino = boton.getAttribute("data-view");
            
            // Bloqueo de seguridad: Evita recargar la pestaña activa o spamear clics durante la animación
            if (boton.classList.contains("active") || estaTransicionando) return;
            if (!vistas[vistaDestino]) return;

            estaTransicionando = true;

            // Intercambiar clase activa en los botones del menú
            botonesMenu.forEach(b => b.classList.remove("active"));
            boton.classList.add("active");

            // Paso A: Desvanecer la vista actual (Fade Out)
            contenedor.classList.add("view-hidden");

            // Paso B: Esperar 200ms (duración de la transición CSS) para cambiar el HTML en memoria
            setTimeout(() => {
                contenedor.innerHTML = vistas[vistaDestino];
                
                // Forzar reflow para asegurar que el navegador registre el nuevo árbol DOM antes del Fade In
                contenedor.offsetHeight; 

                // Paso C: Mostrar la nueva vista con desvanecimiento hacia arriba (Fade In)
                contenedor.classList.remove("view-hidden");
                estaTransicionando = false;
            }, 200); 
        });
    });
});
