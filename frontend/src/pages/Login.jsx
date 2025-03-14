import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";

function Login() {
    const [formData, setFormData] = useState({ username: "", password: ""});
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        try {
            const res = await api.post("/users/token", formData);
            localStorage.setItem(ACCESS_TOKEN, res.data.access);
            localStorage.setItem(REFRESH_TOKEN, res.data.access);
            navigate("/");
        } catch (error) {
            setError("Invalid credentials. Try again.");
        }
    };

    return (
        <div className="p-5">
            <h2>Login</h2>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <form onSubmit={handleSubmit}>
                <input type="text" name="username" placeholder="Username" onChange={handleChange} required/>
                <input type="text" name="password" placeholder="Password" onChange={handleChange} required/>
                <button type="submit">Login</button>
            </form>
        </div>
    );
}

export default Login;