$(function() {
    var date_list = [];
    var series = [];
    var name = 'Quantity Over Time'
    var xName = 'Time'
    var yName = 'Quantity'

    $.getJSON('/api/quantity/1',
        function(data) {
            alert('#hidden_vendor_id');
            date_list = data.dates;
            series = data.data;
            generateChart(data);
        }
    );

    function generateChart(data) {
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'quantity_chart',
                type: 'line',
                marginRight: 130,
                marginBottom: 25
            },
            title: {
                text: name,
                x: -20
            },
            xAxis: {
                type: 'datetime',
                labels: {
                    overflow: 'justify'
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
