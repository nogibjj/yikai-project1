import React from 'react';
import PropTypes from 'prop-types';
import Checkbox from './source_checkbox'


class Application extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      sources: [],
      temp: 1,
      ischecked: true,
    };

    fetch("../api/numnews/", { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          temp: data.numnews,
          ischecked: (data.groupby === 1 ? true : false),
        });
      })
      .catch((error) => console.log(error));
    
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
          sources: data.sources,
        });
      })
      .catch((error) => console.log(error));
  }

  
  createCheckbox = items => (
    <Checkbox
      sourcename={items['sourcename']}
      active={items['active']}
      key={items['sourcename']}
      url={this.props.url}
    />
  )

  createCheckboxes = () => (
    this.state.sources.map(this.createCheckbox)
  )

  handlechange(event) {
    this.setState({ temp: event.target.value });
  }

  handlesubmit(event) {
    const { url } = this.props;
    const { temp } = this.state;
    fetch(url+temp+'/', {
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
      .catch((error) => console.log(error));
    event.preventDefault();
  }

  handleswitch(event) {
    const {url} = this.props;
    const {ischecked} = this.state;

    fetch(url+"groupby/"+(ischecked === true ? 0 : 1)+'/', {
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
      event.preventDefault();
  }

  test = () => {
   console.log("hello")
  }

  render() {
    const { temp } = this.state;
    const { ischecked } = this.state;
    return (
      <div className="sources">
        {this.createCheckboxes()}
        <form onSubmit={this.handlesubmit} className="numnews-form">
          <label for="tentacles">Number of news per source (1-100): </label>
          <input type="number" id="tentacles" name="tentacles" min="1" max="100" onChange={this.handlechange} value={temp} />
          <button type="submit"> Confirm </button>
        </form>
        <form onSubmit={this.handleswitch} className="switch-form">
          <input
            type="checkbox"
            value="Group by source"
            checked={ischecked}
            onChange={this.test}
          />
          Group by source
          <input
            type="checkbox"
            value="Group by company"
            checked={!ischecked}
            onChange={this.test}
          />
          Group by company
          <button type="submit"> Switch </button>
        </form>
      </div>

    );
  }

}

Application.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Application;
