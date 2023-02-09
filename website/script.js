
// read from the csv
let result;
function preload()
{
    result = loadTable("assets/word_frequency.csv", "csv", "header");
}
function setup()
{    
    // loop through the csv and append to words and frequencies
    var words = [];
    var frequencies = [];
    for (var i = 0; i < result.getRowCount(); i++) {
        words.push(result.rows[i].arr[0]);
        frequencies.push(result.rows[i].arr[1]);
    }
    
    // debug
    console.log(words); 
    console.log(frequencies); 

    // get html elements
    const ctx_cloud = document.getElementById("cloud").getContext("2d");
    const ctx_dough = document.getElementById('dough');    
  var ctx_stacked = document.getElementById("stacked");
  
    // Doughnut Chart
    new Chart(ctx_dough, {
      type: 'doughnut',
      data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
          label: '# of Votes',
          data: [12, 19, 3, 5, 2, 3],
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  
  // Stacked Bar Chart
  var myChart = new Chart(ctx_stacked, {
      type: 'bar',
      data: {
          labels: ["<  1","1 - 2","3 - 4","5 - 9","10 - 14","15 - 19","20 - 24","25 - 29","> - 29"],
          datasets: [{
              label: 'Employee',
              backgroundColor: "#caf270",
              data: [12, 59, 5, 56, 58,12, 59, 87, 45],
          }, {
              label: 'Engineer',
              backgroundColor: "#45c490",
              data: [12, 59, 5, 56, 58,12, 59, 85, 23],
          }, {
              label: 'Government',
              backgroundColor: "#008d93",
              data: [12, 59, 5, 56, 58,12, 59, 65, 51],
          }, {
              label: 'Political parties',
              backgroundColor: "#2e5468",
              data: [12, 59, 5, 56, 58, 12, 59, 12, 74],
          }],
      },
  options: {
      tooltips: {
        displayColors: true,
        callbacks:{
          mode: 'x',
        },
      },
      scales: {
        xAxes: [{
          stacked: true,
          gridLines: {
            display: false,
          }
        }],
        yAxes: [{
          stacked: true,
          ticks: {
            beginAtZero: true,
          },
          type: 'linear',
        }]
      },
          responsive: true,
          maintainAspectRatio: false,
          legend: { position: 'bottom' },
      }
  });
  
  // Word Cloud
  new Chart(ctx_cloud, {
    type: "wordCloud",
    data: {
      labels: words,
      datasets: [
        {
            label: "",
            data: frequencies
        }
      ]
    },
    options: {
        title: {
          display: false,
          text: "Chart.js Word Cloud"
        },
        color: "black",
        family: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
        hoverColor: "red",
        lineHeight: 100,
        maxRotation: 0,
        minRotation: -90,
        padding: 1,
        rotate: 45,
        rotationSteps: 3,
        size: 30,
        string: "normal normal 90px 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
        style: "normal",
        weight: "bold",
        plugins: {
          legend: {
            display: false,
          },
        },     
    }
  });
}
  

  
