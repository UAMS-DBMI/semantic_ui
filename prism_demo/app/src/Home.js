import './Home.css';
import {
  Link
} from "react-router-dom";
import search from './search.svg';
import browse from './browse.svg';

function Home() {
  return (
    <div className="Home">
      <div className="textBlock">
        <h3>Semantic Search Demo</h3>
        <h4>Joseph Utecht</h4>
        <p>This is a demonstration of the semantic searching interface for cross-collection clinical feature cohort building.</p>
      </div>
      <div className="infoBlock">
        <h2>Explore Collection</h2>
        <Link to="/beam" className="sideButton">
          <img src={search} className="svgIcon" alt="search"/>
          <span>Explore Subject Cohort</span>
          <p>Use the BEAM tool to build a search cohort across TCIA collections.</p>
        </Link>
        <Link to="/" className="sideButton">
          <img src={browse} className="svgIcon" alt="search"/>
          <span>Browse Files</span>
          <p>Go directly to the NBIA download tool.</p>
        </Link>
      </div>
    </div>
  );
}

export default Home;
