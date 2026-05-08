import { Link } from 'react-router-dom';

export default function FeatureDelivery() {
  return (
    <div style={{padding: '40px', maxWidth: '1000px', margin: '0 auto', animation: 'fadeIn 0.5s ease-out'}}>
      <h1 className="text-gradient" style={{fontSize: '3.5rem', marginBottom: '20px'}}>Frictionless Fast Delivery</h1>
      <p style={{fontSize: '1.2rem', color: 'var(--text-muted)', marginBottom: '40px', lineHeight: '1.8'}}>
        Your time is valuable. Turn hours of meal planning, list writing, and store navigation into a single seamless checkout process delivered right to your door.
      </p>
      
      <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '30px', marginBottom: '50px'}}>
        <div className="glass-panel" style={{padding: '30px'}}>
          <div style={{fontSize: '2.5rem', marginBottom: '15px'}}>⚡</div>
          <h3 style={{marginBottom: '10px', fontSize: '1.5rem', color: 'var(--text-light)'}}>One-Click Fulfillment</h3>
          <p style={{color: 'var(--text-muted)', lineHeight: '1.6'}}>Once your Smart Cart is optimized, push the entire list to our logistics network with a single click. No manual re-entry required.</p>
        </div>
        <div className="glass-panel" style={{padding: '30px'}}>
          <div style={{fontSize: '2.5rem', marginBottom: '15px'}}>❄️</div>
          <h3 style={{marginBottom: '10px', fontSize: '1.5rem', color: 'var(--text-light)'}}>Cold-Chain Integrity</h3>
          <p style={{color: 'var(--text-muted)', lineHeight: '1.6'}}>Your groceries are picked and transported using our state-of-the-art cold-chain delivery system, ensuring produce and dairy arrive as fresh as if you picked them yourself.</p>
        </div>
      </div>

      <div style={{textAlign: 'center'}}>
        <Link to="/login">
          <button className="btn btn-primary" style={{padding: '15px 40px', fontSize: '1.1rem'}}>Try it out now</button>
        </Link>
      </div>
    </div>
  );
}
