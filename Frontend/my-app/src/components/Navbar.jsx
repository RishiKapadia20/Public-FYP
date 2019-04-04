import React, { Component } from "react";
import AutoCompleteText from "./AutoCompleteText";

class NavBar extends Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <a className="navbar-brand" href="#">
          Navbar
        </a>
        <button
          className="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon" />
        </button>
        <AutoCompleteText
          selectCompany={this.props.selectCompany}
          // getCompanyData={this.props.getCompanyData}
          items={this.props.items}
        />
      </nav>
    );
  }
}

export default NavBar;
