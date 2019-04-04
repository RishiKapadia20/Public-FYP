import React, { Component } from "react";
import ReactTable from "react-table";
import "react-table/react-table.css";

class Stats extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [{}]
    };
  }

  loadData = data => {
    console.log("in load data");
    console.log(data.datasets);
    console.log(typeof data);
    if (typeof data.datasets !== "undefined") {
      data = data.datasets[0].data;
      this.setState({
        data: data
      });
    }
  };

  componentWillReceiveProps(nextProps) {
    this.loadData(nextProps.predictData);
  }

  render() {
    console.log("in stats");
    console.log(this.props.predictData);
    const columns = [
      {
        Header: "Date",
        accessor: "x",
        width: 200
      },
      {
        Header: "Price",
        accessor: "y",
        width: 200
      }
    ];
    return (
      <div className="Stats">
        <p>Predictions</p>
        <ReactTable
          columns={columns}
          data={this.state.data}
          defaultPageSize={10}
          showPaginationBottom
        />
      </div>
    );
  }
}

export default Stats;
