const Utilidades = {
    formatearMoneda: (valor) => {
        return new Intl.NumberFormat('es-VE', { 
            style: 'currency', 
            currency: 'VES' 
        }).format(valor);
    },

    formatearFecha: (fecha) => {
        return dayjs(fecha).format('DD/MM/YYYY');
    },

    mostrarAlerta: (mensaje, tipo = 'info') => {
        // En el futuro puedes conectar esto con una librería de alertas bonitas (como SweetAlert2)
        console.log(`[${tipo.toUpperCase()}]: ${mensaje}`);
        alert(mensaje);
    },

    normalizarTexto: (texto) => {
        return texto.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
    }
};