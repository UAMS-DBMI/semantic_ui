import { h } from 'preact';
import { Link } from 'preact-router/match';
import style from './style.css';

const Header = () => (
	<header class={style.header}>
		<h1>PRISM Semantic Search</h1>
		<nav>
			<Link activeClassName={style.active} href="/">Search</Link>
			<Link activeClassName={style.active} href="/about">About</Link>
		</nav>
	</header>
);

export default Header;
