import { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import { useNavigate } from 'react-router-dom';

export default function Pantry() {
  const navigate = useNavigate();
  const [groceryList, setGroceryList] = useState([]);
  const [inStock, setInStock] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchList = async () => {
      try {
        const cachedPlan = localStorage.getItem('lastMealPlan');
        let mealPlan = null;
        if (cachedPlan) {
           const parsed = JSON.parse(cachedPlan);
           mealPlan = parsed.data?.meal_plan || parsed.data?.family_plan;
        }
        
        if (!mealPlan) {
          setLoading(false);
          return;
        }

        const payload = {
          meal_plan: mealPlan,
          pantry: [], // empty so we get the full list
          budget: 9999,
          store: "walmart"
        };

        const res = await apiClient.post('/shopping/shopping-plan', payload);
        const allItems = [];
        Object.values(res.data.grocery_list).forEach(items => {
          items.forEach(item => {
            if (!allItems.find(i => i.item === item.item)) {
              allItems.push(item);
            }
          });
        });
        setGroceryList(allItems);

        // Pre-fill from localStorage if exists
        const savedPantry = localStorage.getItem('userPantry');
        if (savedPantry) {
          const parsedPantry = JSON.parse(savedPantry);
          const stockMap = {};
          parsedPantry.forEach(i => stockMap[i] = true);
          setInStock(stockMap);
        }

      } catch (e) {
        console.error("Error fetching groceries for pantry", e);
      } finally {
        setLoading(false);
      }
    };
    fetchList();
  }, []);

  const handleSaveAndProceed = () => {
    const stockItems = Object.keys(inStock).filter(k => inStock[k]);
    localStorage.setItem('userPantry', JSON.stringify(stockItems));
    navigate('/shopping');
  };

  return (
    <div style={{padding: '40px', maxWidth: '800px', margin: '0 auto', animation: 'fadeIn 0.5s ease-out'}}>
      <h1 className="text-gradient" style={{fontSize: '3rem', marginBottom: '20px'}}>Smart Pantry Check</h1>
      <p style={{color: 'var(--text-muted)', marginBottom: '40px', fontSize: '1.1rem'}}>
        Based on your upcoming meal plan, here are the required ingredients. Mark what you already have at home so we don't add it to your shopping list!
      </p>

      {loading ? (
        <div className="glass-panel" style={{padding: '40px', textAlign: 'center'}}>Analyzing meal plan...</div>
      ) : groceryList.length === 0 ? (
        <div className="glass-panel" style={{padding: '40px', textAlign: 'center'}}>
          No meal plan found. Please generate a meal plan first.
        </div>
      ) : (
        <div className="glass-panel" style={{padding: '30px'}}>
          <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '20px'}}>
            {groceryList.map((g, idx) => (
              <div key={idx} style={{
                display: 'flex', 
                flexDirection: 'column',
                gap: '15px',
                padding: '20px', 
                background: inStock[g.item] ? 'rgba(34, 197, 94, 0.1)' : 'rgba(0,0,0,0.3)',
                border: inStock[g.item] ? '1px solid rgba(34, 197, 94, 0.5)' : '1px solid #333',
                borderRadius: '12px',
                transition: 'all 0.2s'
              }}>
                <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                    <span style={{fontSize: '1.1rem', fontWeight: 'bold', color: inStock[g.item] ? '#22c55e' : 'white'}}>{g.item}</span>
                </div>
                
                <div style={{display: 'flex', gap: '5px', background: '#0f172a', padding: '5px', borderRadius: '8px', border: '1px solid #333'}}>
                  <button 
                    onClick={() => setInStock(prev => ({...prev, [g.item]: true}))}
                    style={{
                      flex: 1,
                      padding: '8px 12px', 
                      background: inStock[g.item] ? '#22c55e' : 'transparent',
                      color: inStock[g.item] ? 'white' : 'var(--text-muted)',
                      border: 'none',
                      borderRadius: '6px',
                      cursor: 'pointer',
                      fontWeight: 'bold',
                      transition: 'all 0.2s'
                    }}
                  >
                    In Stock ✓
                  </button>
                  <button 
                    onClick={() => setInStock(prev => ({...prev, [g.item]: false}))}
                    style={{
                      flex: 1,
                      padding: '8px 12px', 
                      background: !inStock[g.item] && inStock[g.item] !== undefined ? '#ef4444' : 'transparent',
                      color: !inStock[g.item] && inStock[g.item] !== undefined ? 'white' : 'var(--text-muted)',
                      border: 'none',
                      borderRadius: '6px',
                      cursor: 'pointer',
                      fontWeight: 'bold',
                      transition: 'all 0.2s'
                    }}
                  >
                    Need It ❌
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div style={{marginTop: '40px', display: 'flex', justifyContent: 'space-between', borderTop: '1px solid #333', paddingTop: '20px'}}>
        <button className="btn btn-secondary" onClick={() => navigate('/meal-planner')}>
          ⬅ Back to Meal Planner
        </button>
        <button className="btn btn-primary" onClick={handleSaveAndProceed} disabled={groceryList.length === 0}>
          Save & Proceed to Shopping 🛒 ➡
        </button>
      </div>
    </div>
  );
}
