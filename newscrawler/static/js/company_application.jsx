import React from 'react';
import PropTypes from 'prop-types';
import Checkbox from './company_checkbox'


class Application extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      companies: [],
      temp: '',
    };
    this.handlechange = this.handlechange.bind(this);
    this.handlesubmit = this.handlesubmit.bind(this);
  }

  componentDidMount() {
    const { url } = this.props;
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          companies: data.companies,
        });
      })
      .catch((error) => console.log(error));
  }

  createCheckbox = items => (
    <Checkbox
      companyname={items['companyname']}
      active={items['active']}
      key={items['companyname']}
      url={this.props.url}
    /> 
  )

  createCheckboxes = () => (
    this.state.companies.map(this.createCheckbox)
  )

  handlechange(event) {
    this.setState({ temp: event.target.value });
  }

  handlesubmit(event) {
    
    const { url } = this.props;
    const { temp } = this.state;
    fetch(url+temp+'/', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        const { companies } = this.state;
        const copycompanies = companies.slice();
        copycompanies.push(data);
        this.setState({ companies: copycompanies, temp: '' });
      })
      .catch((error) => console.log(error));
    event.preventDefault();
  }


  render() {
    const { temp } = this.state;

    return (
      <div className="portfolio">
        {this.createCheckboxes()}
        <form onSubmit={this.handlesubmit} className="comment-form">
          Add new company/keyword to follow: 
          <input type="text" onChange={this.handlechange} value={temp} />
          <button type="submit"> Confirm </button>
        </form>
      </div>
    );
  }

}

// Application.propTypes = {
//   url: PropTypes.string.isRequired,
// };

export default Application;
