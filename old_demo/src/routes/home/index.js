import { h, Component } from 'preact';
import style from './style';
import FeatureSearch from '../../components/feature_search';
import FeatureRestriction from '../../components/feature_restriction';
import { Button } from '@material-ui/core';

export default class Home extends Component {
	state = {
		restrictions: [],
		search_started: false,
		results_in: false,
		search_button_disabled: true,
		results: []
	};

	addRestriction = (restriction) => {
		let newRest = this.state.restrictions.concat(restriction);
		this.setState({ restrictions: newRest,
										search_button_disabled: false });
	};

	removeRestriction = (restriction) => {
		var array = [...this.state.restrictions];
		let index = array.indexOf(restriction)
		if (index !== -1) {
			array.splice(index, 1);
			this.setState({ restrictions: array,
											search_button_disabled: array.length == 0 });
		}
	}

	startSearch = () => {
		console.log('searching....');
		this.setState({search_started: true,
									 results: [],
									 results_in: false,
									 search_button_disabled: true});
		let option_strings = this.state.restrictions.map( (rest) => (
			rest.type.toLowerCase().replace(" ", "_") + "=" + rest.label
		));
		let options = option_strings.join("&")
		window.fetch("http://localhost:8080/api?" + encodeURI(options))
					.then(response => response.json())
					.then(data => this.setState(
						{results: data,
						 results_in: true,
					   search_started: false,
					   search_button_disabled: false}
					)
				);
	}

	render() {
		return (
			<div class={style.home}>
				<h1>Search</h1>
				<p>Add restrictions on your cohort.</p>
				<FeatureSearch addRestriction={this.addRestriction} />
				{this.state.restrictions.map( (restriction) => (
					<FeatureRestriction
						removeRestriction={this.removeRestriction}
						value={restriction}/>
				))}
				<Button
					variant="contained"
					color="primary"
					onClick={this.startSearch}
					disabled={this.state.search_button_disabled || this.state.search_started}>
						Search
				</Button>
				{this.state.results_in &&
				<pre>{JSON.stringify(this.state.results, null, 2)}</pre>
				}
			</div>
		)
	}
}
