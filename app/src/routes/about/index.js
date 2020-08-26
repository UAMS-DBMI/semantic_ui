import { h, Component } from 'preact';
import style from './style';

export default class About extends Component {
	render() {
		return (
			<div class={style.about}>
				<p>This will explain how this whole thing works.</p>
			</div>
		);
	}
}
