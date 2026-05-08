import { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import { useNavigate } from 'react-router-dom';

export default function Orders({ userId }) {
  const [orders, setOrders] = useState([]);
  const [productsMap, setProductsMap] = useState({});
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      if (!userId) return;
      try {
        const [ordersRes, productsRes] = await Promise.all([
          apiClient.get(`/order/${userId}`),
          apiClient.get('/products')
        ]);
        
        const pMap = {};
        productsRes.data.forEach(p => {
          pMap[p.id] = p.name;
        });
        setProductsMap(pMap);
        
        // Reverse so newest is first
        setOrders(ordersRes.data.reverse());
      } catch (e) {
        console.error("Error fetching orders", e);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [userId]);

  if (loading) {
    return <div style={{padding: '40px', textAlign: 'center'}}>Loading orders...</div>;
  }

  const currentOrders = orders.filter(o => o.status !== 'delivered' && o.status !== 'cancelled');
  const pastOrders = orders.filter(o => o.status === 'delivered' || o.status === 'cancelled');

  const renderOrderCard = (order) => (
    <div key={order.id} className="glass-panel" style={{padding: '25px', marginBottom: '20px', borderLeft: order.status === 'placed' ? '4px solid var(--primary-color)' : '4px solid #475569'}}>
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '15px'}}>
        <div>
          <h3 style={{margin: 0, fontSize: '1.2rem'}}>Order #{order.id.toString().padStart(4, '0')}</h3>
          <span style={{color: 'var(--text-muted)', fontSize: '0.9rem'}}>Total: ${order.total_amount.toFixed(2)}</span>
        </div>
        <div style={{
          padding: '5px 15px', 
          borderRadius: '20px', 
          fontSize: '0.85rem', 
          fontWeight: 'bold', 
          textTransform: 'uppercase',
          background: order.status === 'placed' ? 'rgba(99, 102, 241, 0.2)' : 'rgba(255,255,255,0.1)',
          color: order.status === 'placed' ? 'var(--primary-color)' : 'white'
        }}>
          {order.status}
        </div>
      </div>
      <ul style={{listStyle: 'none', padding: 0, margin: 0}}>
        {order.items.map((item, idx) => (
          <li key={idx} style={{display: 'flex', justifyContent: 'space-between', padding: '8px 0', fontSize: '0.95rem'}}>
            <span><span style={{color: 'var(--text-muted)'}}>{item.quantity}x</span> {productsMap[item.product_id] || "Product Item"}</span>
            <span>${(item.price * item.quantity).toFixed(2)}</span>
          </li>
        ))}
      </ul>
      {order.status === 'placed' && (
        <div style={{marginTop: '20px', display: 'flex', gap: '10px'}}>
           <button className="btn btn-secondary" style={{flex: 1, padding: '10px'}} onClick={() => alert("Tracking Status: Your order is currently being picked by an in-store shopper!")}>
             Track Order 📍
           </button>
        </div>
      )}
    </div>
  );

  return (
    <div style={{padding: '40px', maxWidth: '1000px', margin: '0 auto', animation: 'fadeIn 0.5s ease-out'}}>
      <h1 className="text-gradient" style={{fontSize: '3.5rem', marginBottom: '40px'}}>Your Orders</h1>
      
      <div style={{display: 'flex', gap: '40px', flexWrap: 'wrap'}}>
        
        {/* Current Orders */}
        <div style={{flex: 1, minWidth: '350px'}}>
          <h2 style={{fontSize: '1.5rem', marginBottom: '20px', color: 'white', display: 'flex', alignItems: 'center', gap: '10px'}}>
            🚚 Current Orders
          </h2>
          {currentOrders.length === 0 ? (
            <p style={{color: 'var(--text-muted)'}}>You have no active orders.</p>
          ) : (
            currentOrders.map(renderOrderCard)
          )}
        </div>

        {/* Past Orders */}
        <div style={{flex: 1, minWidth: '350px'}}>
          <h2 style={{fontSize: '1.5rem', marginBottom: '20px', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '10px'}}>
            📦 Order History
          </h2>
          {pastOrders.length === 0 ? (
            <p style={{color: 'var(--text-muted)'}}>You have no past orders.</p>
          ) : (
            pastOrders.map(renderOrderCard)
          )}
        </div>
      </div>

      <div style={{marginTop: '40px', display: 'flex', justifyContent: 'center', borderTop: '1px solid #333', paddingTop: '20px'}}>
        <button className="btn btn-secondary" onClick={() => navigate('/dashboard')}>
          ⬅ Back to Dashboard
        </button>
      </div>
    </div>
  );
}
