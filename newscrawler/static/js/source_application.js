"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _react = _interopRequireDefault(require("react"));

var _propTypes = _interopRequireDefault(require("prop-types"));

var _source_checkbox = _interopRequireDefault(require("./source_checkbox"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

class Application extends _react.default.Component {
  constructor(props) {
    super(props);

    _defineProperty(this, "createCheckbox", items => /*#__PURE__*/_react.default.createElement(_source_checkbox.default, {
      sourcename: items['sourcename'],
      active: items['active'],
      key: items['sourcename'],
      url: this.props.url
    }));

    _defineProperty(this, "createCheckboxes", () => this.state.sources.map(this.createCheckbox));

    _defineProperty(this, "test", () => {
      console.log("hello");
    });

    this.state = {
      sources: [],
      temp: 1,
      ischecked: true
    };
    fetch("../api/numnews/", {
      credentials: 'same-origin'
    }).then(response => {
      if (!response.ok) throw Error(response.statusText);
      return response.json();
    }).then(data => {
      this.setState({
        temp: data.numnews,
        ischecked: data.groupby === 1 ? true : false
      });
    }).catch(error => console.log(error));
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
        sources: data.sources
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
      method: 'PUT',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
      }
    }).then(response => {
      if (!response.ok) throw Error(response.statusText);
      return response.json();
    }).catch(error => console.log(error));
    event.preventDefault();
  }

  handleswitch(event) {
    const {
      url
    } = this.props;
    const {
      ischecked
    } = this.state;
    fetch(url + "groupby/" + (ischecked === true ? 0 : 1) + '/', {
      method: 'PUT',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
      }
    }).then(response => {
      if (!response.ok) throw Error(response.statusText);
      return response.json();
    }).then(() => {
      this.setState(({
        ischecked
      }) => ({
        ischecked: !ischecked
      }));
    });
    event.preventDefault();
  }

  render() {
    const {
      temp
    } = this.state;
    const {
      ischecked
    } = this.state;
    return /*#__PURE__*/_react.default.createElement("div", {
      className: "sources"
    }, this.createCheckboxes(), /*#__PURE__*/_react.default.createElement("form", {
      onSubmit: this.handlesubmit,
      className: "numnews-form"
    }, /*#__PURE__*/_react.default.createElement("label", {
      for: "tentacles"
    }, "Number of news per source (1-100): "), /*#__PURE__*/_react.default.createElement("input", {
      type: "number",
      id: "tentacles",
      name: "tentacles",
      min: "1",
      max: "100",
      onChange: this.handlechange,
      value: temp
    }), /*#__PURE__*/_react.default.createElement("button", {
      type: "submit"
    }, " Confirm ")), /*#__PURE__*/_react.default.createElement("form", {
      onSubmit: this.handleswitch,
      className: "switch-form"
    }, /*#__PURE__*/_react.default.createElement("input", {
      type: "checkbox",
      value: "Group by source",
      checked: ischecked,
      onChange: this.test
    }), "Group by source", /*#__PURE__*/_react.default.createElement("input", {
      type: "checkbox",
      value: "Group by company",
      checked: !ischecked,
      onChange: this.test
    }), "Group by company", /*#__PURE__*/_react.default.createElement("button", {
      type: "submit"
    }, " Switch ")));
  }

}

Application.propTypes = {
  url: _propTypes.default.string.isRequired
};
var _default = Application;
exports.default = _default;