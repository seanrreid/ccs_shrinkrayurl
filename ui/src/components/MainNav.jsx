import { Link } from 'react-router-dom';
import { useAuth } from '../AuthContext';

import Wrapper from './Wrapper';

import styles from './nav.module.css';

export default function MainNav() {
    const { isAuth } = useAuth();
    return (
        <Wrapper>
            <nav className={styles.nav}>
                <ul>
                    {isAuth && (
                        <li>
                            <Link to="/">Home</Link>
                        </li>
                    )}
                    {isAuth && (
                        <>
                            <li>
                                <Link to="/links">View Links</Link>
                            </li>
                            <li>
                                <Link to="/links/add">Add A Link</Link>
                            </li>
                        </>
                    )}
                    <li>
                        {isAuth ? (
                            <Link to="/logout">Logout</Link>
                        ) : (
                            <Link to="/login">Login</Link>
                        )}
                    </li>
                </ul>
            </nav>
        </Wrapper>
    );
}
