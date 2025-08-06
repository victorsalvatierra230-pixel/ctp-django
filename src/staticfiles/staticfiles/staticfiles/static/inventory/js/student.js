document.addEventListener('DOMContentLoaded', function() {
  // Referencias a campos
  const courseSelect = document.getElementById('course_id');
  const matterSelect = document.getElementById('matter');
  const dniInput = document.getElementById('id_dni');
  const computerSelect = document.getElementById('computer');
  const btnGuardar = document.getElementById('btnGuardar');

  function validarCampos() {
    // chequeamos que todos los campos tengan valor válido
    const cursoValido = courseSelect && courseSelect.value.trim() !== '';
    const materiaValida = matterSelect && matterSelect.value.trim() !== '';
    const dniValido = dniInput && dniInput.value.trim() !== '';
    const computadoraValida = computerSelect && computerSelect.value.trim() !== '';

    if (cursoValido && materiaValida && dniValido && computadoraValida) {
      btnGuardar.removeAttribute('disabled');
    } else {
      btnGuardar.setAttribute('disabled', 'disabled');
    }
  }

  // Escuchar cambios en los campos
  if(courseSelect) courseSelect.addEventListener('change', validarCampos);
  if(matterSelect) matterSelect.addEventListener('change', validarCampos);
  if(dniInput) dniInput.addEventListener('input', validarCampos);
  if(computerSelect) computerSelect.addEventListener('change', validarCampos);

  // Validamos al cargar la página por si hay valores por defecto
  validarCampos();
});
