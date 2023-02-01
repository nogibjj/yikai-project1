import React from 'react';
import ReactDOM from 'react-dom';
import Application from './source_application';

// This method is only called once
ReactDOM.render(
  // Insert the likes component into the DOM
  <Application url="/api/sources/"/>,
  document.getElementById('reactEntry'),
);
