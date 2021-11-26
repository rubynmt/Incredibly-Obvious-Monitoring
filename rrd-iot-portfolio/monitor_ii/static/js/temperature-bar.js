var barChartCanvas1 = document.getElementById('temperature-bar')

var barData = {
    labels: ['Today'],
    datasets: [
        {label: 'Max Temperature (Celcius)',
	    data: [34],
	    borderWidth: 2,
	    borderColor: ['rgba(90, 125, 10 0.5)',
        ],
        backgroundColor: ['rgba(143, 206, 0, 0.5)'],
    }],
}

var barOptions = {}
var myBarChart = new Chart(barChartCanvas1, {
    type: 'bar',
    data: barData,
    options: barOptions,
})
