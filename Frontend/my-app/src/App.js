import React, { Component } from "react";
import "./App.css";
import NavBar from "./components/Navbar";
import Company from "./components/Company";

class App extends Component {
  constructor() {
    super();
    this.state = {
      graphs: [],
      items: [],
      companies: []
    };
  }

  selectCompany = company => {
    var number = -1;
    var items = this.state.items;
    for (let i = 0; i < items.length; i++) {
      if (items[i] == company) {
        number = i;
      }
    }
    console.log(number);
    var joined = this.state.graphs.concat(this.state.companies[number]);
    this.setState({ graphs: joined });
  };

  componentWillMount() {
    fetch("http://127.0.0.1:5000/get_measurements")
      .then(res => res.json())
      .then(json => {
        var items = [];
        var companies = json["Companies"];
        console.log(companies);
        for (let i = 0; i < companies.length; i++) {
          var item = companies[i]["Name"] + " : " + companies[i]["Symbol"];
          items.push(item);
        }
        console.log(items);

        this.setState({
          companies: json["Companies"],
          items: items
        });
      });
  }

  render() {
    // this.getCompanies();
    console.log(this.state.items);

    var charts = [];
    for (let i = 0; i < this.state.graphs.length; i++) {
      charts.push(<Company company={this.state.graphs[i]} />);
    }
    return (
      <React.Fragment>
        <NavBar selectCompany={this.selectCompany} items={this.state.items} />
        <main>{charts}</main>
      </React.Fragment>
    );
  }
}

export default App;

// getCompanyData = company => {
//   fetch("http://127.0.0.1:5000/company_data/" + company)
//     .then(res => res.json())
//     .then(json => {
//       var labels = [];
//       var values = [];
//       for (let i = 0; i < json.length; i++) {
//         labels = labels.concat(json[i][0]);
//         values = values.concat(json[i][1]);
//       }

//       var chartDataElement = {
//         labels: labels,
//         datasets: [
//           {
//             label: "Stock Prices",
//             data: values,
//             pointRadius: 0,
//             borderColor: "blue",
//             backgroundColor: "rgba(0,0,0,0.1)"
//           }
//         ]
//       };

//       console.log("In get company");
//       console.log(chartDataElement);
//       console.log(this.state.chartData);
//       let chartData = this.state.chartData;
//       chartData.push( chartDataElement );
//       console.log("In company after append");
//       console.log(chartData);
//       this.setState({
//         chartData: chartData
//       });
//     });
// };

// chartData: [
//   {
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
//         label: "Stock Prices",
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
//   },
//   {
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
//         label: "Stock Prices",
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
//   }
// ],

// getChartData() {
//   this.setState({
//     chartData: {
//       labels: [
//         "Boston1",
//         "A place",
//         "another place",
//         "something",
//         "testing123"
//       ],
//       datasets: [
//         {
//           label: "Population",
//           data: [12345, 23234, 34243, 32323, 45454]
//         }
//       ]
//     }
//   });
// }

// componentWillMount() {
//   fetch("http://127.0.0.1:5000/company_data/AAL")
//     .then(res => res.json())
//     .then(json => {
//       this.setState({
//         items: json
//       });
//     });
//   // this.getChartData();
// }
