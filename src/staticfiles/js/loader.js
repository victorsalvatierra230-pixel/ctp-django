document.addEventListener("DOMContentLoaded", function () {
    // Mostrar el indicador de carga
    const loader = document.getElementById("loader");
    const tableContent = document.getElementById("table-content");
    loader.style.display = "block";
    tableContent.style.display ="none"

    // Simular una demora de 3 segundos (ajusta el tiempo según tus necesidades)
    setTimeout(function () {
        // Ocultar el indicador de carga
        loader.style.display = "none";

        // Mostrar la información
        
        tableContent.style.display = "block";
    }, 1000);
});