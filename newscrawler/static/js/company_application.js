"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _react = _interopRequireDefault(require("react"));

var _propTypes = _interopRequireDefault(require("prop-types"));

var _company_checkbox = _interopRequireDefault(require("./company_checkbox"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

class Application extends _react.default.Component {
  constructor(props) {
    super(props);

    _defineProperty(this, "createCheckbox", items => /*#__PURE__*/_react.default.createElement(_company_checkbox.default, {
      companyname: items['companyname'],
      active: items['active'],
      key: items['companyname'],
      url: this.props.url
    }));

    _defineProperty(this, "createCheckboxes", () => this.state.companies.map(this.createCheckbox));

    this.state = {
      companies: [],
      temp: ''
    };
    this.handlechange = this.handlechange.bind(this);
    this.handlesubmit = this.handlesubmit.bind(this);
  }

  componentDidMount() {
    const {
      url
    } = this.props;
    fetch(url, {
      credentials: 'same-origin'
    }).then(response => {
      if (!response.ok) throw Error(response.statusText);
      return response.json();
    }).then(data => {
      this.setState({
        companies: data.companies
      });
    }).catch(error => console.log(error));
  }

  handlechange(event) {
    this.setState({
      temp: event.target.value
    });
  }

  handlesubmit(event) {
    const {
      url
    } = this.props;
    const {
      temp
    } = this.state;
    fetch(url + temp + '/', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
      }
    }).then(response => {
      if (!response.ok) throw Error(response.statusText);
      return response.json();
    }).then(data => {
      const {
        companies
      } = this.state;
      const copycompanies = companies.slice();
      copycompanies.push(data);
      this.setState({
        companies: copycompanies,
        temp: ''
      });
    }).catch(error => console.log(error));
    event.preventDefault();
  }

  render() {
    const {
      temp
    } = this.state;
    return /*#__PURE__*/_react.default.createElement("div", {
      className: "portfolio"
    }, this.createCheckboxes(), /*#__PURE__*/_react.default.createElement("form", {
      onSubmit: this.handlesubmit,
      className: "comment-form"
    }, "Add new company/keyword to follow:", /*#__PURE__*/_react.default.createElement("input", {
      type: "text",
      onChange: this.handlechange,
      value: temp
    }), /*#__PURE__*/_react.default.createElement("button", {
      type: "submit"
    }, " Confirm ")));
  }

} // Application.propTypes = {
//   url: PropTypes.string.isRequired,
// };


var _default = Application;
exports.default = _default;