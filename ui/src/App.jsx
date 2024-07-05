import { AuthProvider } from './AuthContext';
import Routes from './routes/Routes';

import './global.css'

function App() {
    return (
        <AuthProvider>
          <Routes/>
        </AuthProvider>
    );
}

export default App;
