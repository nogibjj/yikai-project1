import React, { Component, PropTypes } from 'react';

class Checkbox extends Component {
  constructor(props) {
    super(props);

    this.state = {
      ischecked: (this.props.active === 1 ? true : false),
      exist: true,
    };
    
  }

  toggleCheckboxChange = () => {
    const {url} = this.props;
    const {companyname} = this.props;
    fetch(url+companyname+'/', {
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

  handledelete = () => {
    const {url} = this.props;
    const {companyname} = this.props;
    fetch(url+companyname+'/', {
      method: 'DELETE',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      // .then(() => {
      //   this.setState(({ exist }) => (
      //     {
      //       exist: false,
      //     }
      //   ));
      // });  
      this.setState(({ exist }) => (
        {
          exist: false,
        }
      ))
    
  }
 
  render() {
    const { companyname } = this.props;
    const { ischecked } = this.state;
    const { exist } = this.state;
    
    return (
      <div class="container outer">
        
        { exist === true ? 
          <div class="row">
            <div class="col-sm-5 checkbox">
              <label>
                <input
                  type="checkbox"
                  value={companyname}
                  checked={ischecked}
                  onChange={this.toggleCheckboxChange}
                />
                {companyname}
              </label>
            </div> 
            <div class="col-sm-1 deletebox">
              <button onClick={this.handledelete}> <img src="../static/img/bin.png" width='24' /> </button>
            </div>
        </div>
            :
          null
        }
      </div>
    );
  }
}

export default Checkbox;
