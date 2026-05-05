document.addEventListener("DOMContentLoaded", () => {

    // Cridem a l'API que hem creat
    fetch("/api/stats_dashboard")
        .then(resposta => resposta.json())
        .then(dades => {

            // GRAFIC 1: HISTORIC DE PUNTUACIO
            const ctxHistoric = document.getElementById('graficHistoric').getContext('2d');
            new Chart(ctxHistoric, {
                type: 'line',
                data: {
                    labels: dades.historic.dates,
                    datasets: [{
                        label: 'Puntuació aconseguida',
                        data: dades.historic.puntuacions,
                        borderColor: '#00f2fe',
                        backgroundColor: 'rgba(0, 242, 254, 0.2)',
                        fill: true,
                        tension: 0.3
                    }]
                },
                options: {
                    scales: {
                        y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.1)' } },
                        x: { grid: { color: 'rgba(255,255,255,0.1)' } }
                    },
                    plugins: { legend: { labels: { color: 'white' } } }
                }
            });

            // GRÀFIC 2: ERRORS PER JOC (Gràfic de Barres)
            const ctxErrors = document.getElementById('graficErrors').getContext('2d');
            new Chart(ctxErrors, {
                type: 'bar',
                data: {
                    labels: dades.errors.noms_jocs,
                    datasets: [{
                        label: "Mitjana d'errors fallits",
                        data: dades.errors.mitjanes,
                        backgroundColor: 'rgba(255, 71, 87, 0.6)',
                        borderColor: 'rgba(255, 71, 87, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: { y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.1)' } } },
                    plugins: { legend: { labels: { color: 'white' } } }
                }
            });

        })
        .catch(err => console.error("Error al carregar el dashboard:", err));
});
