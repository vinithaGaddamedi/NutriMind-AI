import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Login({ setUserId }) {
  const [username, setUsername] = useState('');
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    if (username) {
      // Generate a deterministic user ID based on username so parallel tests don't share carts
      const mockId = username.length * 100 + username.charCodeAt(0);
      setUserId(mockId); 
      navigate('/dashboard');
    }
  };

  return (
    <div className="login-container" style={{display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '80vh'}}>
      <form onSubmit={handleLogin} className="glass-panel" style={{padding: '40px', width: '350px'}}>
        <h2 style={{marginBottom: '20px', textAlign: 'center'}}>Sign In</h2>
        <div style={{marginBottom: '20px'}}>
          <label htmlFor="username" style={{display: 'block', marginBottom: '8px', color: 'var(--text-muted)', textAlign: 'left'}}>Username</label>
          <input 
            id="username"
            type="text" 
            placeholder="Enter your username" 
            value={username} 
            onChange={(e) => setUsername(e.target.value)} 
            style={{width: '100%', padding: '12px', borderRadius: '8px', border: '1px solid #333', background: '#1e293b', color: 'white'}}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary" style={{width: '100%'}}>Login</button>
      </form>
    </div>
  );
}
