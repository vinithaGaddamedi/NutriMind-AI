import { Link } from 'react-router-dom';

export default function FeatureSmartCart() {
  return (
    <div style={{padding: '40px', maxWidth: '1000px', margin: '0 auto', animation: 'fadeIn 0.5s ease-out'}}>
      <h1 className="text-gradient" style={{fontSize: '3.5rem', marginBottom: '20px'}}>The Intelligent Smart Cart</h1>
      <p style={{fontSize: '1.2rem', color: 'var(--text-muted)', marginBottom: '40px', lineHeight: '1.8'}}>
        Automatically convert your week's meals into an optimized grocery list that respects your budget, leverages your pantry, and maps to your favorite store.
      </p>
      
      <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '30px', marginBottom: '50px'}}>
        <div className="glass-panel" style={{padding: '30px'}}>
          <div style={{fontSize: '2.5rem', marginBottom: '15px'}}>📉</div>
          <h3 style={{marginBottom: '10px', fontSize: '1.5rem', color: 'var(--text-light)'}}>Budget & Pantry Optimization</h3>
          <p style={{color: 'var(--text-muted)', lineHeight: '1.6'}}>Provide your current pantry inventory and a weekly budget constraint. The engine will intelligently remove duplicates and adjust quantities to keep your finances in check.</p>
        </div>
        <div className="glass-panel" style={{padding: '30px'}}>
          <div style={{fontSize: '2.5rem', marginBottom: '15px'}}>🏪</div>
          <h3 style={{marginBottom: '10px', fontSize: '1.5rem', color: 'var(--text-light)'}}>Real-time Price Simulation</h3>
          <p style={{color: 'var(--text-muted)', lineHeight: '1.6'}}>Why overpay? We dynamically simulate cart totals across Walmart, Costco, and Amazon Fresh to recommend the most cost-effective checkout destination.</p>
        </div>
        <div className="glass-panel" style={{padding: '30px'}}>
          <div style={{fontSize: '2.5rem', marginBottom: '15px'}}>🗺️</div>
          <h3 style={{marginBottom: '10px', fontSize: '1.5rem', color: 'var(--text-light)'}}>Store Aisle Routing</h3>
          <p style={{color: 'var(--text-muted)', lineHeight: '1.6'}}>Shopping in person? We reorder your generated grocery list based on actual retail layouts (e.g., Produce → Dairy → Pantry) to cut your store trip time in half.</p>
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
