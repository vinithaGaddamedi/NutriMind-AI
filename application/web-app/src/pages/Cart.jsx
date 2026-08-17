import { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import { useNavigate } from 'react-router-dom';

export default function Cart({ userId }) {
  const [cart, setCart] = useState([]);
  const navigate = useNavigate();

  const fetchCart = async () => {
    if (userId) {
      const res = await apiClient.get(`/cart/${userId}`);
      setCart(res.data);
    }
  };

  useEffect(() => {
    fetchCart();
  }, [userId]);

  const updateQuantity = async (productId, newQuantity) => {
    if (newQuantity <= 0) {
      await handleRemove(productId);
      return;
    }
    try {
      await apiClient.put(`/cart/${userId}/${productId}`, { quantity: newQuantity });
      await fetchCart(); // Refresh cart
    } catch (e) {
      console.error(e);
      alert("Failed to update quantity");
    }
  };

  const handleRemove = async (productId) => {
    try {
      await apiClient.delete(`/cart/${userId}/${productId}`);
      await fetchCart();
    } catch (e) {
      console.error(e);
      alert("Failed to remove item");
    }
  };

  const handleCheckout = async () => {
    try {
      await apiClient.post('/order/', { user_id: userId });
      const currentTotal = calculateTotal();
      const currentCart = [...cart];
      setCart([]);
      navigate('/order-success', { state: { orderItems: currentCart, total: currentTotal } });
    } catch (e) {
      alert("Error placing order: " + (e.response?.data?.detail || e.message));
    }
  };

  const calculateTotal = () => {
    return cart.reduce((total, item) => total + (item.price * item.quantity), 0).toFixed(2);
  };

  return (
    <div style={{padding: '40px', maxWidth: '900px', margin: '0 auto'}}>
      <h2 className="text-gradient" style={{marginBottom: '10px'}}>Your Smart Cart</h2>
      <p style={{marginBottom: '30px', color: 'var(--text-muted)'}}>Review your items before proceeding to Fast Delivery checkout.</p>
      
      {cart.length === 0 ? (
        <div className="glass-panel" style={{padding: '50px', textAlign: 'center'}}>
          <p style={{fontSize: '1.2rem', color: 'var(--text-muted)'}}>Your cart is currently empty.</p>
          <button className="btn btn-secondary" onClick={() => navigate('/products')} style={{marginTop: '20px'}}>Browse Products</button>
        </div>
      ) : (
        <div style={{display: 'flex', gap: '30px', flexWrap: 'wrap'}}>
          <div style={{flex: '2', minWidth: '400px'}}>
            <ul style={{listStyle: 'none', padding: 0}}>
              {cart.map(item => (
                <li key={item.id} className="glass-panel" style={{padding: '20px', marginBottom: '15px', display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                  <div style={{flex: '1'}}>
                    <h3 style={{marginBottom: '5px'}}>{item.name}</h3>
                    <div style={{color: 'var(--text-muted)', fontSize: '0.9rem'}}>${item.price.toFixed(2)} / each</div>
                  </div>
                  
                  <div style={{display: 'flex', alignItems: 'center', gap: '15px'}}>
                    <div style={{display: 'flex', alignItems: 'center', background: '#0f172a', borderRadius: '8px', overflow: 'hidden', border: '1px solid #333'}}>
                      <button onClick={() => updateQuantity(item.product_id, item.quantity - 1)} style={{padding: '8px 12px', background: 'transparent', border: 'none', color: 'white', cursor: 'pointer', fontSize: '1.2rem'}}>-</button>
                      <span style={{padding: '0 10px', minWidth: '30px', textAlign: 'center'}}>{item.quantity}</span>
                      <button onClick={() => updateQuantity(item.product_id, item.quantity + 1)} style={{padding: '8px 12px', background: 'transparent', border: 'none', color: 'white', cursor: 'pointer', fontSize: '1.2rem'}}>+</button>
                    </div>
                    
                    <div style={{fontWeight: 'bold', width: '70px', textAlign: 'right'}}>
                      ${(item.price * item.quantity).toFixed(2)}
                    </div>

                    <button onClick={() => handleRemove(item.product_id)} style={{background: 'rgba(239, 68, 68, 0.2)', color: '#ef4444', border: '1px solid rgba(239, 68, 68, 0.3)', padding: '8px 12px', borderRadius: '8px', cursor: 'pointer', transition: 'all 0.2s'}}>
                      Remove
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          </div>
          
          <div className="glass-panel" style={{flex: '1', minWidth: '300px', alignSelf: 'flex-start', padding: '30px'}}>
            <h3 style={{marginBottom: '20px', borderBottom: '1px solid #333', paddingBottom: '15px'}}>Order Summary</h3>
            <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '15px', color: 'var(--text-muted)'}}>
              <span>Subtotal</span>
              <span>${calculateTotal()}</span>
            </div>
            <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '15px', color: 'var(--text-muted)'}}>
              <span>Delivery Fee</span>
              <span>$4.99</span>
            </div>
            <div style={{display: 'flex', justifyContent: 'space-between', marginTop: '20px', paddingTop: '20px', borderTop: '1px solid #333', fontWeight: 'bold', fontSize: '1.2rem'}}>
              <span>Total</span>
              <span className="text-gradient">${(parseFloat(calculateTotal()) + 4.99).toFixed(2)}</span>
            </div>
            
            <button className="btn btn-primary" onClick={handleCheckout} style={{width: '100%', marginTop: '30px', padding: '15px', fontSize: '1.1rem'}}>
              Checkout
            </button>
          </div>
        </div>
      )}

      <div style={{marginTop: '40px', display: 'flex', justifyContent: 'space-between', borderTop: '1px solid #333', paddingTop: '20px'}}>
        <button className="btn btn-secondary" onClick={() => navigate('/shopping')}>
          ⬅ Back to Shopping Mode
        </button>
      </div>
    </div>
  );
}
