import './App.css';
import Beam from './beam/Beam';
import Home from './Home';
import logo from './TCIA-logo.png';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="header">
          <div className="header_top">
            <div className="header_side">
              <a href="https://www.cancerimagingarchive.net/primary-data/" className="header_link">
                Submit Your Data
              </a>
              <a href="https://www.cancerimagingarchive.net/access-data/" className="header_link">
                Access the Data
              </a>
              <a href="https://www.cancerimagingarchive.net/support/" className="header_link">
                Help
              </a>
            </div>
            <Link to="/">
              <img src={logo} alt="ARIES" className="logo"/>
            </Link>
            <div className="header_side">
              <a href="https://www.cancerimagingarchive.net/about-the-cancer-imaging-archive-tcia/" className="header_link">
                About Us
              </a>
              <a href="https://www.cancerimagingarchive.net/publications/" className="header_link">
                Research Activities 
              </a>
              <a href="https://www.cancerimagingarchive.net/news/" className="header_link">
                News 
              </a>
            </div>
          </div>
          <h1 className="header_title">Semantic Search</h1>
        </nav>
        <div className="main_container">
          <Switch>
            <Route path='/beam'>
              <Beam />
            </Route>
            <Route path='/'>
              <Home />
            </Route>
          </Switch>
        </div>
      </div>
    </Router>
  );
}

export default App;
