document.getElementById("form-busca").addEventListener("submit", function(e) {
    e.preventDefault(); // impede o recarregamento da página
    const termo = document.getElementById("campo-busca").value;

    fetch(`/buscar-consultas/?q=${encodeURIComponent(termo)}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("tabela-consultas").innerHTML = data.html;
        });
});