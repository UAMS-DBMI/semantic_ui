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
          <div className="header_side">
            <Link to="/" className="header_link">
              Home
            </Link>
            <Link to="/" className="header_link">
              Access the Data
            </Link>
            <Link to="/" className="header_link">
              Submit Your Data
            </Link>
          </div>
          <Link to="/">
            <img src={logo} alt="ARIES" className="logo"/>
          </Link>
          <div className="header_side">
            <Link to="/" className="header_link">
              About Us
            </Link>
            <Link to="/" className="header_link">
              Research Activities
            </Link>
            <Link to="/" className="header_link">
              Help
            </Link>
          </div>
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
