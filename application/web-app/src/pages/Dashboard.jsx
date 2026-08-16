import { Link } from 'react-router-dom';

export default function Dashboard() {
  return (
    <div style={{padding: '40px', maxWidth: '1200px', margin: '0 auto', animation: 'fadeIn 0.5s ease-out'}}>
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '40px'}}>
        <div>
          <h1 className="text-gradient" style={{fontSize: '3rem', marginBottom: '10px'}}>Welcome to your Dashboard</h1>
          <p style={{color: 'var(--text-muted)', fontSize: '1.2rem'}}>Your NutriMind Intelligence Platform is ready.</p>
        </div>
      </div>

      <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '30px', marginBottom: '50px'}}>
        <Link to="/meal-planner" style={{textDecoration: 'none', color: 'inherit'}}>
          <div className="glass-panel" style={{padding: '30px', height: '100%', transition: 'all 0.3s ease', cursor: 'pointer'}} 
               onMouseEnter={e => { e.currentTarget.style.transform = 'translateY(-10px)'; e.currentTarget.style.boxShadow = '0 20px 40px rgba(0,0,0,0.4)'; }}
               onMouseLeave={e => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = 'none'; }}>
            <div style={{fontSize: '3.5rem', marginBottom: '20px'}}>🥗</div>
            <h3 style={{marginBottom: '15px', fontSize: '1.5rem', color: 'var(--text-light)'}}>AI Meal Planner</h3>
            <p style={{color: 'var(--text-muted)', lineHeight: '1.6'}}>Generate BMR-optimized nutrition plans for you and your family.</p>
          </div>
        </Link>
        
        <Link to="/shopping" style={{textDecoration: 'none', color: 'inherit'}}>
          <div className="glass-panel" style={{padding: '30px', height: '100%', transition: 'all 0.3s ease', cursor: 'pointer'}}
               onMouseEnter={e => { e.currentTarget.style.transform = 'translateY(-10px)'; e.currentTarget.style.boxShadow = '0 20px 40px rgba(0,0,0,0.4)'; }}
               onMouseLeave={e => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = 'none'; }}>
            <div style={{fontSize: '3.5rem', marginBottom: '20px'}}>🛒</div>
            <h3 style={{marginBottom: '15px', fontSize: '1.5rem', color: 'var(--text-light)'}}>Shopping Mode</h3>
            <p style={{color: 'var(--text-muted)', lineHeight: '1.6'}}>Optimize your grocery list against your weekly budget and pantry inventory.</p>
          </div>
        </Link>

        <Link to="/products" style={{textDecoration: 'none', color: 'inherit'}}>
          <div className="glass-panel" style={{padding: '30px', height: '100%', transition: 'all 0.3s ease', cursor: 'pointer'}}
               onMouseEnter={e => { e.currentTarget.style.transform = 'translateY(-10px)'; e.currentTarget.style.boxShadow = '0 20px 40px rgba(0,0,0,0.4)'; }}
               onMouseLeave={e => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = 'none'; }}>
            <div style={{fontSize: '3.5rem', marginBottom: '20px'}}>📦</div>
            <h3 style={{marginBottom: '15px', fontSize: '1.5rem', color: 'var(--text-light)'}}>Browse Products</h3>
            <p style={{color: 'var(--text-muted)', lineHeight: '1.6'}}>Explore the catalog, discover recommendations, and add items to your cart.</p>
          </div>
        </Link>
      </div>

      <div className="glass-panel" style={{padding: '40px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'rgba(99, 102, 241, 0.1)', border: '1px solid var(--primary-color)', borderRadius: '16px', flexWrap: 'wrap', gap: '20px'}}>
        <div>
          <h3 style={{marginBottom: '10px', fontSize: '1.8rem', color: 'var(--text-light)'}}>Ready to checkout?</h3>
          <p style={{color: 'var(--text-muted)'}}>Review your Smart Cart items and proceed with Fast Delivery.</p>
        </div>
        <Link to="/cart">
          <button className="btn btn-primary" style={{padding: '15px 30px', fontSize: '1.1rem'}}>View Cart</button>
        </Link>
      </div>
    </div>
  );
}
