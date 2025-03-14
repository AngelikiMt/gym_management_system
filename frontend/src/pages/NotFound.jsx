import { Link } from "react-router-dom";

function NotFound() {
    return (
        <div className="p-5">
            <h2>404 - Page Not Found</h2>
            <p>The page you are looking for does not exist.</p>
            <Link to="/">Go back to HomePage</Link>
        </div>
    );
}

export default NotFound;