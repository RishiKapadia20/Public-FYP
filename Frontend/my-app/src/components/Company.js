import React, { Component } from "react";
import Chart from "./Chart";
import Stats from "./Stats";

class Company extends Component {
  constructor(props) {
    super(props);
    this.state = {
      chartData: {},
      predictData: {}
    };
  }

  getCompanyData = (company, state) => {
    fetch("http://127.0.0.1:5000/company_data/" + company + "/" + state)
      .then(res => res.json())
      .then(json => {
        var values = [];
        for (let i = 0; i < json.length; i++) {
          values = values.concat({ x: json[i][0], y: json[i][1] });
        }

        var chartData = {
          datasets: [
            {
              label: "Historical Prices",
              data: values,
              showLine: true,
              pointRadius: 0,
              borderColor: "blue",
              backgroundColor: "rgba(0,0,0,0.1)"
            }
          ]
        };
        this.setState({
          chartData: chartData
        });
      });
  };

  getPredictionData = company => {
    fetch("http://127.0.0.1:5000/get_predict_price/" + company)
      .then(res => res.json())
      .then(json => {
        var values = [];
        for (let i = 0; i < json.length; i++) {
          values = values.concat({ x: json[i][0], y: json[i][1] });
        }

        var predictData = {
          datasets: [
            {
              label: "Prediction Price",
              data: values,
              showLine: true,
              pointRadius: 0,
              borderColor: "red",
              backgroundColor: "rgba(0,0,0,0.1)"
            }
          ]
        };

        this.setState({
          predictData: predictData
        });
      });
  };

  componentDidMount() {
    console.log("mounting");
    this.getCompanyData(this.props.company["Symbol"], "1Month");
    this.getPredictionData(this.props.company["Symbol"]);
  }

  componentDidUpdate() {
    fetch("http://127.0.0.1:5000/refreshdb/" + this.props.company["Symbol"]);
    console.log("refreshing");
  }

  render() {
    return (
      <div>
        <Chart
          companyName={this.props.company["Name"]}
          companySymbol={this.props.company["Symbol"]}
          chartData={this.state.chartData}
          predictData={this.state.predictData}
        />

        <button
          onClick={() =>
            this.getCompanyData(this.props.company["Symbol"], "1Week")
          }
          className="btn btn-danger btn-dm m-2"
        >
          {" "}
          1Week
        </button>

        <button
          onClick={() =>
            this.getCompanyData(this.props.company["Symbol"], "2Week")
          }
          className="btn btn-danger btn-dm m-2"
        >
          {" "}
          2Week
        </button>

        <button
          onClick={() =>
            this.getCompanyData(this.props.company["Symbol"], "1Month")
          }
          className="btn btn-danger btn-dm m-2"
        >
          {" "}
          1Month
        </button>

        <button
          onClick={() =>
            this.getCompanyData(this.props.company["Symbol"], "1Year")
          }
          className="btn btn-danger btn-dm m-2"
        >
          {" "}
          1Year
        </button>

        <button
          onClick={() =>
            this.getCompanyData(this.props.company["Symbol"], "full")
          }
          className="btn btn-danger btn-dm m-2"
        >
          {" "}
          Full
        </button>
        <Stats predictData={this.state.predictData} />
      </div>
    );
  }
}

export default Company;
