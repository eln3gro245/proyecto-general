document.addEventListener("DOMContentLoaded", () => {
    
    const inputDesde = document.getElementById('fecha-desde');
    const inputHasta = document.getElementById('fecha-hasta');
    const selectMovimiento = document.getElementById('filtro-movimiento');
    const filas = document.querySelectorAll('.data-table tbody tr');

    function filtrar() {
        filas.forEach(fila => {
            
            const fechaTexto = fila.cells[0].innerText; 
            const tipoTexto = fila.cells[2].innerText.toLowerCase();
            
            const desde = inputDesde.value ? new Date(inputDesde.value) : null;
            const hasta = inputHasta.value ? new Date(inputHasta.value) : null;
            const fechaFila = new Date(fechaTexto);

            const cumpleFecha = (!desde || fechaFila >= desde) && (!hasta || fechaFila <= hasta);
            const cumpleTipo = (selectMovimiento.value === 'todos' || tipoTexto.includes(selectMovimiento.value));

            fila.style.display = (cumpleFecha && cumpleTipo) ? '' : 'none';
        });
    }

    if(inputDesde) inputDesde.addEventListener('change', filtrar);
    if(inputHasta) inputHasta.addEventListener('change', filtrar);
    if(selectMovimiento) selectMovimiento.addEventListener('change', filtrar);

    const btnExportar = document.querySelector('.btn-secondary-action');
    if(btnExportar) {
        btnExportar.addEventListener('click', () => {
            const tabla = document.querySelector('.data-table');
            const wb = XLSX.utils.table_to_book(tabla, {sheet: "Reportes"});
            XLSX.writeFile(wb, "Reporte_FarmaNorte.xlsx");
        });
    }

    const btnImprimir = document.querySelector('.btn-primary-action');
    if(btnImprimir) {
        btnImprimir.addEventListener('click', () => {
            
            const elementosAOcultar = [
                document.querySelector('.sidebar'),
                document.querySelector('.main-header'),
                document.querySelector('.inventory-controls-bar'),
                document.querySelector('.header-actions')
            ];

            elementosAOcultar.forEach(el => { if(el) el.style.display = 'none'; });

            window.print();

            setTimeout(() => {
                elementosAOcultar.forEach(el => { if(el) el.style.display = ''; });
            }, 1000);
        });
    }
});