import { useAuth } from '../AuthContext';
import { Link } from 'react-router-dom';
import Wrapper from '../components/Wrapper';

const Home = () => {
    const { isAuth } = useAuth();
    return (
        <Wrapper>
            <h1>Home</h1>
            <p>Welcome home, you&apos;ve arrived.</p>
            {isAuth ? (
                <div>
                    <p>You&apos;re logged in, why not add a link?</p>
                    <Link to="/links/add">Add a Link</Link>
                </div>
            ) : (
                <div>
                    <p>User not authenticated.</p>
                    <Link to="/login">Click here to login</Link>
                </div>
            )}
        </Wrapper>
    );
};

export default Home;
