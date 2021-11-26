function getData() {
    data = [];
    for (let i = 0; i < 25; i++) {
       int = Math.floor(Math.random() * 42)
        data.push(int)
        console.log(data)
    }
    return data;
}
var lineChartCanvas1 = document.getElementById('history-line-chart')

var lineData = {
    labels: ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th','10th','11th','12th','13th','14th','15th','16th',
        '17th','18th','19th','20th','21st','22nd','23rd','24th'],
    datasets: [
        {
            label: '',
            line: '',
            data: getData(),
            lineTension: 0.2,
            borderWidth: 2,
            fill: false,
            borderColor: ['rgba( 211, 085, 211, 0.5)',
            ],
        },
        ],
}

var lineOptions = {
    lineTension: 0.2,
    legend: {display: false},
    title: {
        display: true,
        text: 'Historical Temperature'},
    scales: {
        xAxes: [{
            scaleLabel: {
                display: true,
                labelString: 'This month',
            }
        }],
        yAxes: [{
            scaleLabel: {
                display: true,
                labelString: 'Temp',
            },
            ticks: {
                beginAtZero: false,
            },
        }],
    },
}

var mylineChart = new Chart(lineChartCanvas1, {
    type: 'line',
    data: lineData,
    options: lineOptions,
})
