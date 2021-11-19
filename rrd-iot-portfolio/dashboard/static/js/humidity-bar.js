var barChartCanvas1 = document.getElementById('humidity-bar')

var barData = {
    labels: ['Today'],
    datasets: [
        {label: 'Max Humidity',
	    data: [78],
	    borderWidth: 2,
	    borderColor: ['rgba( 211, 085, 211, 0.5)',
        ],
        backgroundColor: ['rgba(118, 56, 120, 0.5)'],
    }],
}

var barOptions = {}
var myBarChart = new Chart(barChartCanvas1, {
    type: 'bar',
    data: barData,
    options: barOptions,
})
