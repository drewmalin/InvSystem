$(function() {
    var date_list = [];
    var series = [];
    var name = 'Quantity Over Time'
    var xName = 'Time'
    var yName = 'Quantity'
    var URL = document.URL
    var id = URL.substring(URL.lastIndexOf('/')+1)

    $.getJSON('/api/quantity/'+id,
        function(data) {
            date_list = data.dates;
            series = data.data;
            generateChart(data);
        }
    );

    function generateChart(data) {
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'quantity_chart',
                type: 'column',
                marginRight: 50
            },
            title: {
                text: name,
                x: -20
            },
            xAxis: {
                type: 'datetime',
                labels: {
                    staggerLines: 2
                },
                title: {
                    text: xName
                },
                categories: date_list
            },
            yAxis: {
                title: {
                    text: yName
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                formatter: function() {
                    return '<b>'+name+'</b><br>'+this.x+': '+this.y;
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticlAlign: 'top',
                x: -10,
                y: 100,
                borderWidth: 0
            },
            series: series
        });
    }
});
