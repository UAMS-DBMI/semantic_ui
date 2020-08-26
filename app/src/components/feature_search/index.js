import { h, Component } from 'preact';
import style from './style';
import { Button } from '@material-ui/core';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import { SELECT_OPTIONS } from './select_options';

export default class FeatureSearch extends Component {
	constructor(props){
		super();
		this.addRestriction = props.addRestriction;
		this.state = { value: null };
	}

	setValue = (n) => {
		if(!this.mounted) return;
		this.setState({value: n});
	};

	sendRestriction = () => {
		if(!this.mounted) return;
		this.addRestriction(this.state.value);
		this.setState({value:null});
	};

	componentWillMount(){
		this.mounted = true;
	}

	componentWillUnmount(){
		console.log("unmounting");
		this.mounted = false;
	}

	render({}, {}) {
		return (
			<div class={style.feature_search}>
				<Autocomplete
					id="combo-box-demo"
					options={SELECT_OPTIONS}
					value={this.state.value}
					onChange={(event, newValue) => {
						this.setValue(newValue);
					}}
					getOptionLabel={(option) => option.label}
					renderOption={(option) => (
						<>
							{option.label} <span class={"search_" + option.type.toLowerCase()}>({option.type})</span>
						</>
					)}
					style={{ width: 500 }}
					renderInput={(params) => <TextField {...params} label="Cohort restriction" variant="outlined" />}
				/>
				<Button
					variant="contained"
					color="primary"
					onClick={this.sendRestriction}
					disabled={this.state.value == null}>
						Add Restriction
				</Button>
			</div>
		);
	}
}
