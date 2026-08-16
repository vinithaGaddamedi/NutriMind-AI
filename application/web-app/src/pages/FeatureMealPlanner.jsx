import { Link } from 'react-router-dom';

export default function FeatureMealPlanner() {
  return (
    <div style={{padding: '40px', maxWidth: '1000px', margin: '0 auto', animation: 'fadeIn 0.5s ease-out'}}>
      <h1 className="text-gradient" style={{fontSize: '3.5rem', marginBottom: '20px'}}>Nutrition-Aware AI Meal Planning</h1>
      <p style={{fontSize: '1.2rem', color: 'var(--text-muted)', marginBottom: '40px', lineHeight: '1.8'}}>
        Take the guesswork out of eating healthy. Our AI planner uses your biological data (age, weight, height) and health goals to generate precisely calibrated weekly meal plans.
      </p>
      
      <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '30px', marginBottom: '50px'}}>
        <div className="glass-panel" style={{padding: '30px'}}>
          <div style={{fontSize: '2.5rem', marginBottom: '15px'}}>🔬</div>
          <h3 style={{marginBottom: '10px', fontSize: '1.5rem', color: 'var(--text-light)'}}>Deterministic BMR Calculations</h3>
          <p style={{color: 'var(--text-muted)', lineHeight: '1.6'}}>We utilize the Mifflin-St Jeor equation to establish your exact baseline metabolic rate, modifying calorie targets dynamically for weight loss, maintenance, or muscle gain.</p>
        </div>
        <div className="glass-panel" style={{padding: '30px'}}>
          <div style={{fontSize: '2.5rem', marginBottom: '15px'}}>👨‍👩‍👧‍👦</div>
          <h3 style={{marginBottom: '10px', fontSize: '1.5rem', color: 'var(--text-light)'}}>Family-Optimized Portions</h3>
          <p style={{color: 'var(--text-muted)', lineHeight: '1.6'}}>No more cooking different meals. The engine plans a single common recipe for the whole family, while adjusting individual portion sizes to meet everyone's unique caloric needs.</p>
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
