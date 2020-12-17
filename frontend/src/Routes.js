import React from 'react';

import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";

import Webcam from "./Webcam";
import App from "./App"
import Solution from "./Solution"


export default function Rt() {
  return (
    <Router>
      <Switch>
          <Route path="/webcam">
            <Webcam/>
          </Route>

          <Route path={"/solution"} >
            <Solution/>
          </Route>

          <Route path={["/", "/upload"]} >
            <App/>
          </Route>
        </Switch>
    </Router>
  );
}