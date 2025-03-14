import { useNavigate } from "react-router-dom";

function Home() {
    const navigate = useNavigate();

    return (
        <div className="p-5">
            <h2>Welcome to Gyme Management System</h2>
            <button onClick={() => navigate("/users/logout")}>Logout</button>
        </div>
    );
}

export default Home;