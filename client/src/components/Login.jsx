import React, { useState } from 'react';
import axios from 'axios';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        axios.post('/auth/login', {
            username,
            password
        }).then(response => {
            if (response.status == 201) {
                window.location.pathname = "/files"     
            }
        }).catch(error => {
            console.error(error.response.data.message)
        })
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="text" autoComplete='username' value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" />
            <input type="password" autoComplete='current-password' value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
            <button type="submit">Login</button>
        </form>
    );
}

export default Login;
