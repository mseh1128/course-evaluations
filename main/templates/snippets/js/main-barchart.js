<script>
$(function () {
  $('.mycontainer').highcharts({
     chart: {
        type: 'bar'
     },
     title: {
        text: 'Historic World Population by Region'   
     },
     subtitle: {
        text: 'Source: wikipedia'
     },
     xAxis: {
        categories: ['Africa', 'America', 'Asia', 'Europe', 'Oceania', 'Test'],
        title: {
           text: null
        },
        min: 0,
        max: 4,
        scrollbar: {
          enabled: true
        },
     },
     yAxis: {
        min: 0,
        max: 100,
        title: {
           text: ''
        },
        labels: {
           overflow: 'justify'
        }
     },
     tooltip: {
        valueSuffix: ' millions'
     },
     plotOptions: {
        bar: {
           dataLabels: {
              enabled: true
           }
        },
        series: {
           color: 'red'
  }
     },
     credits: {
        enabled: false
     },
     series: [
        {
           name: 'Value',
           showInLegend: false,
           data: [{y: 80, color: '#FFD700'},{y: 76, color: 'silver'}, {y: 70, color: '#CD7F32 '}, 69, 30,43,74,63,73,58,47]
        }
     ]
     
    });
});


$(function () {
  $('.mycontainersss').highcharts({
     chart: {
        type: 'bar'
     },
     title: {
        text: 'Historic World Population by Region'   
     },
     subtitle: {
        text: 'Source: Wikipedia.org'  
     },
     xAxis: {
        categories: ['Africa', 'America', 'Asia', 'Europe', 'Oceania'],
        title: {
           text: null
        }
     },
     yAxis: {
        min: 0,
        title: {
           text: ''
        },
        labels: {
           overflow: 'justify'
        }
     },
     tooltip: {
        valueSuffix: ' millions'
     },
     plotOptions: {
        bar: {
           dataLabels: {
              enabled: true
           }
        },
        series: {
           color: 'red'
  }
     },
     credits: {
        enabled: false
     },
     series: [
        {
           name: 'Value',
           showInLegend: false,
           data: [{y: 80, color: '#FFD700'},{y: 76, color: 'silver'}, {y: 70, color: '#CD7F32 '}, 69, 30]
        }
     ]
     
    });
});
</script>