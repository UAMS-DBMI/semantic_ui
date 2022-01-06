import './App.css';
import Beam from './beam/Beam';
import Home from './Home';
import logo from './PRISM-logo.png';
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
            </div>
            <Link to="/">
              <img src={logo} alt="PRISM" className="logo"/>
            </Link>
            <div className="header_side">
            </div>
          </div>
          <h1 className="header_title">Semantic Search Cohort Builder</h1>
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
