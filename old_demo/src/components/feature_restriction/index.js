import { h, Component } from 'preact';
import style from './style';
import Chip from '@material-ui/core/Chip';

export default class FeatureRestriction extends Component {
	constructor(props){
		super();
		this.removeRestriction = props.removeRestriction;
		this.state = {value: props.value, count:"..."};
		this.startSearch();
	}

	handleDelete = () => {
		this.removeRestriction(this.state.value);
	}

	startSearch() {
		this.setState({count:"...",
									 results_in: false});
		let option = this.state.value.type.toLowerCase().replace(" ", "_") + "=" + this.state.value.label
		window.fetch("http://localhost:8080/api?" + encodeURI(option))
					.then(response => response.json())
					.then(data => this.setState(
						{count: data.length,
						 results_in: true}
					)
				);
	}

	render({value, removeRestriction}, {}) {
		return (
			<div class={style.feature_restriction}>
				<p>
					Where <span class={"search_" + value.type.toLowerCase()}>({value.type})</span> is "{value.label}"
				</p>
				<Chip
					label={this.state.count}
					color="primary"
				/>
				<Chip
					label="Remove Restriction"
					onDelete={this.handleDelete}
					onClick={this.handleDelete}
					color="secondary"
					variant="outlined"
				/>
			</div>
		);
	}
}
