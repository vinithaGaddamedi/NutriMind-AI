import { useState, useEffect } from 'react';
import { apiClient } from '../api/client';

export default function Products({ userId }) {
  const [products, setProducts] = useState([]);
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    const fetchProducts = async () => {
      const res = await apiClient.get('/products');
      setProducts(res.data);
    };
    const fetchRecommendations = async () => {
      if (userId) {
        const res = await apiClient.get(`/recommendations/${userId}`);
        setRecommendations(res.data);
      }
    };
    fetchProducts();
    fetchRecommendations();
  }, [userId]);

  const addToCart = async (productId) => {
    await apiClient.post('/cart/', { user_id: userId, product_id: productId, quantity: 1 });
    alert("Added to cart!");
  };

  return (
    <div style={{padding: '40px', maxWidth: '1200px', margin: '0 auto'}}>
      {recommendations.length > 0 && (
        <section style={{marginBottom: '40px'}}>
          <h2 className="text-gradient">Recommended for You</h2>
          <div className="features" style={{padding: '20px 0'}}>
            {recommendations.map(rec => (
              <div key={`rec-${rec.product_id}`} className="feature-card glass-panel" style={{padding: '20px'}}>
                <h3>{rec.name}</h3>
                <p style={{marginBottom: '15px'}}>{rec.reason}</p>
                <button className="btn btn-secondary" onClick={() => addToCart(rec.product_id)}>Add to Cart</button>
              </div>
            ))}
          </div>
        </section>
      )}

      <h2>All Products</h2>
      <div className="features" style={{padding: '20px 0'}}>
        {products.map(p => (
          <div key={p.id} className="feature-card glass-panel" style={{padding: '20px'}}>
            <h3>{p.name}</h3>
            <p style={{marginBottom: '15px'}}>${p.price}</p>
            <button className="btn btn-primary" onClick={() => addToCart(p.id)}>Add to Cart</button>
          </div>
        ))}
      </div>
    </div>
  );
}
