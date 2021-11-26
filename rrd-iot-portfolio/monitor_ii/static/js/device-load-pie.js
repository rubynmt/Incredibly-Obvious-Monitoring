var pieChartCanvas2 = document.getElementById('device-load-pie')

var pieData = {labels: ['CPU Use', 'Idle'],
    datasets: [{
        data: [36, 64],
        borderWidth: 2,
        borderAlign: 'inner',
        borderWidth: 2,
        borderAlign: 'inner',
        backgroundColor: [
            'rgba( 102, 205, 170, 0.5)',
            'rgba( 100, 149, 237, 0.5)',
        ],
        borderColor: [
            'rgba( 70, 130, 109, 0.5)',
            'rgba( 97, 88, 152, 0.5)',
        ],
    }]
}

var pieOptions = {}
var myPieChart = new Chart(pieChartCanvas2, {
    type: 'pie',
    data: pieData,
    options: pieOptions,
})
