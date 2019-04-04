import React, { Component } from "react";
import { Bar, Line, Pie, Scatter } from "react-chartjs-2";

class Chart extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: {}
    };
  }

  componentWillReceiveProps(nextProps) {
    let chartData = nextProps.chartData.datasets;
    let predictData = nextProps.predictData.datasets;

    if (
      typeof chartData !== "undefined" &&
      typeof predictData !== "undefined"
    ) {
      this.mergeData(nextProps.chartData, nextProps.predictData);
    }
  }

  mergeData = (chartData, predictData) => {
    let chartDataValues = chartData.datasets[0];
    let predictDataValues = predictData.datasets[0];

    let datasets = [];
    datasets = datasets.concat(chartDataValues);
    datasets = datasets.concat(predictDataValues);

    let data = { datasets };

    this.setState({
      data: data
    });
  };

  render() {
    // var timeFormat = "YYYY-MM-DD";

    return (
      <div className="chart">
        {" "}
        <Scatter
          data={this.state.data}
          options={{
            responsive: true,
            title: {
              display: true,
              text: this.props.companyName,
              fontSize: 25
            },
            legend: {
              display: true,
              position: "right"
            },
            scales: {
              xAxes: [
                {
                  type: "time",
                  time: {
                    // format: timeFormat,
                    // unit: "year"
                  },
                  scaleLabel: {
                    display: true,
                    labelString: "Date"
                  }
                }
              ],
              yAxes: [
                {
                  scaleLabel: {
                    display: true,
                    labelString: "value"
                  }
                }
              ]
            }
          }}
        />
      </div>
    );
  }
}

export default Chart;

// return (
//   <div className="chart">
//     {" "}
//     <Scatter
//       data={{
//         datasets:[
//         {
//           label:"test 1",
//           data: [{x: 1, y: 2}, {x: 2, y: 4}, {x: 3, y: 8},{x: 4, y: 16}],
//           showLine: true,
//           fill: false,
//           borderColor: 'rgba(0, 200, 0, 1)'
//         },
//         {
//           label: 'Chart 2',
//           data: [{x: 10, y: 20}, {x: 30, y: 4}, {x: 40, y: 6}, {x: 60, y: 9}],
//           showLine: true,
//           fill: false,
//           borderColor: 'rgba(200, 0, 0, 1)'
//         }
//       ]

//     }}

//       options={{
//         responsive: true,
//         title: {
//           display: true,
//           text: this.props.title,
//           fontSize: 25
//         },
//         legend: {
//           display: true,
//           position: "right"
//         },
//         scales: {
//           xAxes: [
//             {
//               type: "time",
//               time: {
//                 format: timeFormat,
//                 unit: "year"
//               },
//               scaleLabel: {
//                 display: true,
//                 labelString: "Date"
//               }
//             }
//           ],
//           yAxes: [
//             {
//               scaleLabel: {
//                 display: true,
//                 labelString: "value"
//               }
//             }
//           ]
//         }
//       }}
//     />
//   </div>
// );
// }
// }

// export default Chart;

//   this.data = {
//     labels: [
//       "2019-01-15",
//       "2018-02-14",
//       "2017-03-13",
//       "2016-04-12",
//       "2015-05-11",
//       "2014-06-11",
//       "2013-07-11",
//       "2012-08-11",
//       "2011-09-11",
//       "2010-10-11",
//       "2009-11-11",
//       "2008-12-11"
//     ],
//     datasets: [
//       {
//         label: "Value",
//         data: [
//           31.88,
//           31.88,
//           31.88,
//           31.88,
//           31.88,
//           31.88,
//           31.88,
//           31.88,
//           31.88,
//           31.88,
//           31.88,
//           31.88
//         ]
//       }
//     ]
//   };
// }
