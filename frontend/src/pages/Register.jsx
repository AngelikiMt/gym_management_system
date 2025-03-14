import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";

function Register() {
    const [formData, setFormData] = useState({ username: "", email: "", password: ""});
    const [error, serError] = useState("");
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        try {
            await api.post("/users/register", formtData);
            alert("Registration successful!");
            navigate("/users/login");
        } catch (error) {
            setError("Failed to register. Please try again.");
        }
    };

    return (
        <div className="p-5">
            <h2>Register</h2>
            {error && <p style={{ color: "red"  }}>{error}</p>}
            <form onSubmit={handleSubmit}>
                <input type="text" name="username" placeholder="Username" onChange={handleChange} required/>
                <input type="email" name="email" placeholder="Email" onChange={handleChange} required/>
                <input type="password" name="password" placeholder="Password" onChange={handleChange} required/>
                <button type="submit">Register</button>
            </form>
        </div>
    );
}

export default Register;