import { useLocation, useNavigate } from 'react-router-dom';

export default function OrderSuccess() {
  const location = useLocation();
  const navigate = useNavigate();
  const { orderItems, total } = location.state || { orderItems: [], total: "0.00" };

  return (
    <div style={{padding: '40px', maxWidth: '800px', margin: '0 auto', textAlign: 'center', animation: 'fadeIn 0.5s ease-out'}}>
      <div style={{fontSize: '5rem', marginBottom: '10px'}}>✅</div>
      <h1 className="text-gradient" style={{fontSize: '3rem', marginBottom: '10px'}}>Order Placed Successfully!</h1>
      <p style={{color: 'var(--text-muted)', fontSize: '1.2rem', marginBottom: '40px'}}>
        Your groceries have been ordered and will be delivered to you shortly.
      </p>

      {orderItems.length > 0 && (
        <div className="glass-panel" style={{padding: '40px', textAlign: 'left', marginBottom: '40px'}}>
          <h3 style={{marginBottom: '20px', borderBottom: '1px solid #333', paddingBottom: '15px', color: 'var(--secondary-color)'}}>Order Summary</h3>
          <ul style={{listStyle: 'none', padding: 0, marginBottom: '25px'}}>
            {orderItems.map((item, idx) => (
              <li key={idx} style={{display: 'flex', justifyContent: 'space-between', padding: '12px 0', borderBottom: '1px solid rgba(255,255,255,0.05)'}}>
                <span><span style={{color: 'var(--primary-color)', fontWeight: 'bold'}}>{item.quantity}x</span> {item.name}</span>
                <span>${(item.price * item.quantity).toFixed(2)}</span>
              </li>
            ))}
          </ul>
          <div style={{display: 'flex', justifyContent: 'space-between', color: 'var(--text-muted)', marginBottom: '10px'}}>
            <span>Subtotal</span>
            <span>${total}</span>
          </div>
          <div style={{display: 'flex', justifyContent: 'space-between', color: 'var(--text-muted)', marginBottom: '10px'}}>
            <span>Delivery Fee</span>
            <span>$4.99</span>
          </div>
          <div style={{display: 'flex', justifyContent: 'space-between', fontWeight: 'bold', fontSize: '1.4rem', marginTop: '20px', paddingTop: '20px', borderTop: '1px solid #333'}}>
            <span>Total Paid</span>
            <span className="text-gradient">${(parseFloat(total) + 4.99).toFixed(2)}</span>
          </div>
        </div>
      )}

      <div style={{display: 'flex', justifyContent: 'center', gap: '20px'}}>
        <button className="btn btn-secondary" onClick={() => navigate('/dashboard')} style={{padding: '12px 30px', fontSize: '1.1rem'}}>
          Back to Dashboard
        </button>
        <button className="btn btn-primary" onClick={() => navigate('/orders')} style={{padding: '12px 30px', fontSize: '1.1rem'}}>
          Track Order 📍
        </button>
      </div>
    </div>
  );
}
