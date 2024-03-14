import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Landing from "./pages/Landing";
import VenturesContainer from './containers/VenturesContainer'
import Guide from './pages/Guide'
import Login from './pages/Login'
import "./index.css";
import { createRoot } from "react-dom/client";
import { PlayerProvider } from './context/player';
import { CombatProvider } from './context/combat';

const container = document.getElementById("root");
const root = createRoot(container);

root.render(
  <Router>
    <CombatProvider>
    <PlayerProvider>
    <Switch>
      <Route exact path="/" component={Landing} />
      <Route exact path="/ventures" component={VenturesContainer} />
      <Route exact path="/guide" component={Guide} />
      <Route exact path="/login" component={Login} />
    </Switch>
    </PlayerProvider>
    </CombatProvider>
  </Router>
);