import './App.css';
import { Fragment } from 'react';
import { Route, Routes } from 'react-router-dom';
import MarketEvent from './Pages/MarketEvent';

function App() {
  return (
    // Routing for the later use when the application becomes bigger
    <Fragment>
      <Routes>
        <Route path='/' element={<MarketEvent />} />        
      </Routes>
    </Fragment>
  );
}

export default App;
