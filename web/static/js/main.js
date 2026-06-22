// Função para alternar as abas dos usuários
function mostrarRegistros(uid, elementoClicado) {
    document.getElementById('mensagem-inicial').classList.add('d-none');

    let containers = document.querySelectorAll('.container-registros');
    containers.forEach(div => div.classList.add('d-none'));

    let botoes = document.querySelectorAll('.user-card');
    botoes.forEach(btn => btn.classList.remove('active'));

    document.getElementById('dados-' + uid).classList.remove('d-none');
    elementoClicado.classList.add('active');
}

// Função para filtrar usuários na barra lateral
function filtrarUsuarios() {
    let input = document.getElementById('inputBusca');
    let filtro = input.value.toLowerCase();
    let botoes = document.getElementsByClassName('user-card');

    for (let i = 0; i < botoes.length; i++) {
        let nomeElemento = botoes[i].querySelector('.nome-usuario');
        if (nomeElemento) {
            let nome = nomeElemento.textContent || nomeElemento.innerText;
            if (nome.toLowerCase().indexOf(filtro) > -1) {
                botoes[i].style.display = ""; // Mostra
            } else {
                botoes[i].style.display = "none"; // Esconde
            }
        }
    }
}

// Função genérica para ordenar qualquer tabela html pelo ID e índice da coluna
function ordenarTabela(idTabela, n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById(idTabela);
    switching = true;
    // Direção padrão: ascendente
    dir = "asc";

    while (switching) {
        switching = false;
        rows = table.rows;

        // Loop passando por todas as linhas da tabela (exceto o cabeçalho)
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;

            // Pega os dois elementos que serão comparados
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];

            // Remove tags HTML para comparar apenas o texto (ex: tirar o span/badge)
            let valX = x.textContent.trim();
            let valY = y.textContent.trim();

            // Lógica para ordenar números/horas x strings comuns
            if (dir == "asc") {
                if (valX.toLowerCase() > valY.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            } else if (dir == "desc") {
                if (valX.toLowerCase() < valY.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount++;
        } else {
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}