const buscador = document.getElementById('buscador-servicios');
const sinResultados = document.getElementById('sin-resultados');

buscador.addEventListener('input', () => {
    const texto = buscador.value.toLowerCase();
    const filas = document.querySelectorAll('#tabla-servicios tr[data-nombre]');
    let visibles = 0;
    filas.forEach(fila => {
        const visible = fila.dataset.nombre.includes(texto);
        fila.style.display = visible ? '' : 'none';
        if (visible) visibles++;
    });
    sinResultados.style.display = visibles === 0 ? 'block' : 'none';
});

function abrirModalNuevo() {
    document.getElementById('modal-titulo').textContent = 'Nuevo servicio';
    document.getElementById('form-servicio').action = '/admin/servicios/nuevo';
    document.getElementById('campo-nombre').value = '';
    document.getElementById('campo-descripcion').value = '';
    document.getElementById('modal-servicio').style.display = 'flex';
}

function abrirModalEdicion(id, nombre, descripcion) {
    document.getElementById('modal-titulo').textContent = 'Editar servicio';
    document.getElementById('form-servicio').action = '/admin/servicios/' + id + '/editar';
    document.getElementById('campo-nombre').value = nombre;
    document.getElementById('campo-descripcion').value = descripcion;
    document.getElementById('modal-servicio').style.display = 'flex';
}

function cerrarModal() {
    document.getElementById('modal-servicio').style.display = 'none';
}
