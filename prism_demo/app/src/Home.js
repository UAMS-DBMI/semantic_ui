import './Home.css';
import {
  Link
} from "react-router-dom";
import search from './search.svg';
import browse from './browse.svg';
import demo from './demo.png';

function Home() {
  return (
    <div className="Home">
      <div className="textBlock">
        <h3>Semantic Search Demo</h3>
        <h4>Joseph Utecht</h4>
        <p>This is a demonstration of the semantic searching interface for cross-collection clinical feature cohort building.</p>
        <p>This interface will allow you to build a cohort of subjects across multiple collections based on clinical features that were reported to the TCIA.</p>
        <p>To use the tool, click "Explore Subject Cohort" on the right.</p>
        <img className="demo-image" src={demo} alt="Instuctions for the demo"/>
        <p>This demo is under active development, please report any bugs encounted to lead developer <a href="mailto:jrutecht@uams.edu">Joseph Utecht</a></p>
      </div>
      <div className="infoBlock">
        <h2>Explore Collection</h2>
        <Link to="/beam" className="sideButton">
          <img src={search} className="svgIcon" alt="search"/>
          <span>Explore Subject Cohort</span>
          <p>Use the BEAM tool to build a search cohort across TCIA collections.</p>
        </Link>
        <a href="https://nbia.cancerimagingarchive.net/nbia-search/" className="sideButton">
          <img src={browse} className="svgIcon" alt="search"/>
          <span>Browse Files</span>
          <p>Go directly to the NBIA download tool.</p>
        </a>
      </div>
    </div>
  );
}

export default Home;
