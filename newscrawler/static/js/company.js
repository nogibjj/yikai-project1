"use strict";

var _react = _interopRequireDefault(require("react"));

var _reactDom = _interopRequireDefault(require("react-dom"));

var _company_application = _interopRequireDefault(require("./company_application"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

// This method is only called once
_reactDom.default.render(
/*#__PURE__*/
// Insert the likes component into the DOM
_react.default.createElement(_company_application.default, {
  url: "/api/portfolio/"
}), document.getElementById('reactEntry'));