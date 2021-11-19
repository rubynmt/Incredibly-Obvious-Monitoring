var barChartCanvas1 = document.getElementById('pressure-bar')

var barData = {
    labels: ['Today'],
    datasets: [
        {label: 'Air Pressure',
	    data: [50],
	    borderWidth: 2,
	    borderColor: ['rgba(231, 156, 58, 0.5)',
        ],
        backgroundColor: ['rgba( 255, 202, 0, 0.5)'],
    }],
}

var barOptions = {}
var myBarChart = new Chart(barChartCanvas1, {
    type: 'bar',
    data: barData,
    options: barOptions,
})
