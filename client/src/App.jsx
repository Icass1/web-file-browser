import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Register from './components/Register';
import Login from './components/Login';
import Welcome from './components/Welcome';
import MainContainer from './components/MainContainer';


function App() {


    const api_regex = /^\/api\/.*/
    // if using "/api/" in the pathname, don't use React Router
    if (api_regex.test(window.location.pathname)) {
        return <div /> // must return at least an empty div
    } else {

        return (
            <Router>
                <Routes>
                    <Route path="/" element={<Welcome />} />
                    <Route path="/files/*" element={<MainContainer />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/login" element={<Login />} />
                </Routes>
            </Router>
        );
    }
}

export default App;
