//
//function buildChart(labels, values, chartTitle) {
//    var ctx = document.getElementById('myChart').getContext('2d');
//    var myChart = new Chart(ctx, {
//        type: 'bar',
//        data: {
//            labels: labels,
//            datasets: [{
//                label: chartTitle,
//                data: values,
//                backgroundColor: 'rgba(0, 202, 216, 0.79)',
//                hoverBackgroundColor: 'rgba(0, 202, 216, 0.79)',
//                hoverBorderWidth: 3,
//                hoverBorderColor: 'rgba(0, 232, 255, 1)'
//            }]
//        },
//        options: {
//            plugins: {
//                legend:{
//                    display: false
//                }
//            }
//        }
//    });
//    return myChart;
//}
//
////function builtMixedChart(labels, values_bar, values_line, chartTitle) {
//function buildMixedChartTest() {
//    var ctx = document.getElementById('myChart').getContext('2d');
//    var myChart = new Chart(ctx, {
//        data: {
//            datasets: [{
//                type: 'bar',
//                label: 'Bar Dataset',
//                data: [10, 20, 30, 40]
//            },
//            {
//                type: 'line',
//                label: 'Line Dataset',
//                data: [50, 50, 50, 50],
//            }],
//            labels: ['January', 'February', 'March', 'April']
//        },
////        options: {
////            plugins: {
////                legend:{
////                    display: false
////                }
////            }
////        }
//    });
//    return myChart
//}

function buildMixedChart(labels, values_temp, values_hum) {
    var canvas = document.getElementById('myChart').getContext('2d');
    myChart = new Chart(canvas, {
        data: {
            labels: labels,
            datasets: [{
                type: 'line',
                label: 'Humidity',
                yAxisID: 'Humidity',
                data: values_hum,
                tension: 0.4,
                borderColor: 'rgba(250, 128, 114, 0.79)',
                backgroundColor: 'rgba(250, 128, 114, 0.79)',
                hoverBorderWidth: 3,
                hoverBorderColor: 'rgba(250, 128, 114, 1)'
            },
            {
                type: 'bar',
                label: 'Temperature',
                yAxisID: 'Temperature',
                data: values_temp,
                tension: 0.4,
                backgroundColor: 'rgba(0, 202, 216, 0.79)',
                hoverBackgroundColor: 'rgba(0, 202, 216, 0.79)',
                hoverBorderWidth: 3,
                hoverBorderColor: 'rgba(0, 232, 255, 1)'
            }]
        },
        options: {
            scales: {
                Temperature: {
                    type: 'linear',
                    position: 'left',
                    gridLines: {
                        display: false,
                        color: "rgba(0, 0, 0, 0)",
                        drawBorder: false,
                    },
                },
                Humidity: {
                    type: 'linear',
                    position: 'right',
                    gridLines: {
                        display: false,
                        color: "rgba(0, 0, 0, 0)",
                        drawBorder: false,
                    },
                    ticks: {
                        max: 100,
                        min: 0,
                        beginAtZero: true
                    }
                }
            }
        }
    });
    return myChart;
}

/* Toggle between showing and hiding the navigation menu links when the user clicks on the hamburger menu / bar icon */
function myFunction() {
  var x = document.getElementById("myLinks");
  if (x.style.display === "block") {
    x.style.display = "none";
  } else {
    x.style.display = "block";
  }
}