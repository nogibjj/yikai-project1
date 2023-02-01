"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _react = _interopRequireWildcard(require("react"));

function _getRequireWildcardCache(nodeInterop) { if (typeof WeakMap !== "function") return null; var cacheBabelInterop = new WeakMap(); var cacheNodeInterop = new WeakMap(); return (_getRequireWildcardCache = function (nodeInterop) { return nodeInterop ? cacheNodeInterop : cacheBabelInterop; })(nodeInterop); }

function _interopRequireWildcard(obj, nodeInterop) { if (!nodeInterop && obj && obj.__esModule) { return obj; } if (obj === null || typeof obj !== "object" && typeof obj !== "function") { return { default: obj }; } var cache = _getRequireWildcardCache(nodeInterop); if (cache && cache.has(obj)) { return cache.get(obj); } var newObj = {}; var hasPropertyDescriptor = Object.defineProperty && Object.getOwnPropertyDescriptor; for (var key in obj) { if (key !== "default" && Object.prototype.hasOwnProperty.call(obj, key)) { var desc = hasPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : null; if (desc && (desc.get || desc.set)) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } newObj.default = obj; if (cache) { cache.set(obj, newObj); } return newObj; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

class Checkbox extends _react.Component {
  constructor(props) {
    super(props);

    _defineProperty(this, "toggleCheckboxChange", () => {
      const {
        url
      } = this.props;
      const {
        companyname
      } = this.props;
      fetch(url + companyname + '/', {
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
    });

    _defineProperty(this, "handledelete", () => {
      const {
        url
      } = this.props;
      const {
        companyname
      } = this.props;
      fetch(url + companyname + '/', {
        method: 'DELETE',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json'
        }
      }).then(response => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      }); // .then(() => {
      //   this.setState(({ exist }) => (
      //     {
      //       exist: false,
      //     }
      //   ));
      // });  

      this.setState(({
        exist
      }) => ({
        exist: false
      }));
    });

    this.state = {
      ischecked: this.props.active === 1 ? true : false,
      exist: true
    };
  }

  render() {
    const {
      companyname
    } = this.props;
    const {
      ischecked
    } = this.state;
    const {
      exist
    } = this.state;
    return /*#__PURE__*/_react.default.createElement("div", {
      class: "container outer"
    }, exist === true ? /*#__PURE__*/_react.default.createElement("div", {
      class: "row"
    }, /*#__PURE__*/_react.default.createElement("div", {
      class: "col-sm-5 checkbox"
    }, /*#__PURE__*/_react.default.createElement("label", null, /*#__PURE__*/_react.default.createElement("input", {
      type: "checkbox",
      value: companyname,
      checked: ischecked,
      onChange: this.toggleCheckboxChange
    }), companyname)), /*#__PURE__*/_react.default.createElement("div", {
      class: "col-sm-1 deletebox"
    }, /*#__PURE__*/_react.default.createElement("button", {
      onClick: this.handledelete
    }, " ", /*#__PURE__*/_react.default.createElement("img", {
      src: "../static/img/bin.png",
      width: "24"
    }), " "))) : null);
  }

}

var _default = Checkbox;
exports.default = _default;