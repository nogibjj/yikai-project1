import React from 'react';
import ReactDOM from 'react-dom';
import Application from './company_application';

// This method is only called once
ReactDOM.render(
  // Insert the likes component into the DOM
  <Application url="/api/portfolio/"/>,
  document.getElementById('reactEntry'),
);
