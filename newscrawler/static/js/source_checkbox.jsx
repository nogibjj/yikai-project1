import React, { Component, PropTypes } from 'react';

class Checkbox extends Component {
  constructor(props) {
    super(props);

    this.state = {
      ischecked: (this.props.active === 1 ? true : false),
    };
    
  }

  toggleCheckboxChange = () => {
    const {url} = this.props;
    const {sourcename} = this.props;
    fetch(url+sourcename+'/', {
      method: 'PUT',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then(() => {
        this.setState(({ ischecked }) => (
          {
            ischecked: !ischecked,
          }
        ));
      });   
  }

 
  render() {
    const { sourcename } = this.props;
    const { ischecked } = this.state;
    
    return (
      <div>
        <div className="checkbox">
          <label>
            <input
              type="checkbox"
              value={sourcename}
              checked={ischecked}
              onChange={this.toggleCheckboxChange}
            />
            {sourcename}
          </label>
        </div> 
      </div>
    );
  }
}


export default Checkbox;
