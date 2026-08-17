import { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import { useNavigate } from 'react-router-dom';

export default function ShoppingMode({ userId }) {
  const [budget, setBudget] = useState(100);
  const [pantryInput, setPantryInput] = useState('Rice, Milk');
  const [store, setStore] = useState('walmart');
  const [shoppingMode, setShoppingMode] = useState('online'); // 'online' or 'instore'
  const [shoppingPlan, setShoppingPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedItems, setSelectedItems] = useState({});
  const [allProducts, setAllProducts] = useState([]);
  const [cartQuantities, setCartQuantities] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch all products
    const fetchProducts = async () => {
      try {
        const res = await apiClient.get('/products');
        setAllProducts(res.data);
      } catch(e) {
        console.error("Failed to fetch products", e);
      }
    };
    // Fetch cart to determine existing quantities
    const fetchCart = async () => {
      if (userId) {
        try {
          const res = await apiClient.get(`/cart/${userId}`);
          const qtyMap = {};
          res.data.forEach(item => {
            qtyMap[item.name] = item.quantity;
          });
          setCartQuantities(qtyMap);
        } catch(e) {
          console.error("Failed to fetch cart", e);
        }
      }
    };
    fetchProducts();
    fetchCart();
  }, [userId]);

  // Load from cache on mount
  const getMealPlan = () => {
    const cachedPlan = localStorage.getItem('lastMealPlan');
    if (cachedPlan) {
      try {
        const parsed = JSON.parse(cachedPlan);
        return parsed.data.meal_plan || parsed.data.family_plan;
      } catch (e) {}
    }
    return {
      "Monday": {
        "breakfast": "Oats with fruits",
        "lunch": "Brown rice + dal + salad",
        "dinner": "Roti + vegetables"
      }
    };
  };

  const handleGeneratePlan = async (e, overrideStore = null, overridePantry = null) => {
    if (e) e.preventDefault();
    setLoading(true);
    setError(null);

    const pantryList = overridePantry !== null ? overridePantry : pantryInput.split(',').map(i => i.trim()).filter(i => i);
    const mealPlan = getMealPlan();

    const payload = {
      meal_plan: mealPlan,
      pantry: pantryList,
      budget: parseFloat(budget),
      store: overrideStore || store
    };

    try {
      const res = await apiClient.post('/shopping/shopping-plan', payload);
      setShoppingPlan(res.data);
      
      // Auto-select all items initially
      const initialSelected = {};
      Object.values(res.data.grocery_list).forEach(items => {
        items.forEach(item => {
          initialSelected[item.item] = item.quantity;
        });
      });
      setSelectedItems(initialSelected);
      
    } catch (err) {
      console.error(err);
      setError("Failed to generate shopping plan");
    } finally {
      setLoading(false);
    }
  };

  // Run automatically if there's a cached plan
  useEffect(() => {
    const savedPantry = localStorage.getItem('userPantry');
    let initPantryList = [];
    if (savedPantry) {
      try {
        const parsed = JSON.parse(savedPantry);
        initPantryList = parsed;
        setPantryInput(parsed.join(', '));
      } catch(e) {}
    }

    if (localStorage.getItem('lastMealPlan')) {
      handleGeneratePlan(null, null, initPantryList);
    }
  }, []);

  const toggleItem = (itemName, qty) => {
    setSelectedItems(prev => {
      const next = { ...prev };
      if (next[itemName]) {
        delete next[itemName];
      } else {
        next[itemName] = qty;
      }
      return next;
    });
  };

  const addToCartDirectly = async (itemName, quantity) => {
    if (!userId) {
      alert("Please login first.");
      navigate('/login');
      return;
    }
    try {
      await apiClient.post('/cart/bulk-add', {
        user_id: userId,
        items: [{name: itemName, quantity}]
      });
      setCartQuantities(prev => ({ ...prev, [itemName]: (prev[itemName] || 0) + quantity }));
    } catch (e) {
      console.error(e);
      alert("Failed to add item to cart.");
    }
  };

  const handleUpdateQuantity = async (itemName, delta) => {
    const currentQty = cartQuantities[itemName] || 0;
    const newQty = currentQty + delta;
    
    try {
      await apiClient.post('/cart/bulk-add', {
        user_id: userId,
        items: [{name: itemName, quantity: delta}]
      });
      
      if (newQty <= 0) {
        const nextQ = {...cartQuantities};
        delete nextQ[itemName];
        setCartQuantities(nextQ);
      } else {
        setCartQuantities(prev => ({ ...prev, [itemName]: newQty }));
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleBulkCheckout = async () => {
    if (!userId) {
      alert("Please login first.");
      navigate('/login');
      return;
    }
    
    const itemsToAdd = Object.entries(selectedItems).map(([name, quantity]) => ({
      name, quantity
    }));
    
    if (itemsToAdd.length === 0) {
      alert("No items selected!");
      return;
    }

    try {
      await apiClient.post('/cart/bulk-add', {
        user_id: userId,
        items: itemsToAdd
      });
      navigate('/cart');
    } catch (err) {
      console.error("Error adding to cart", err);
      alert("Error adding items to cart.");
    }
  };

  const handleCompleteInstore = () => {
    const currentPantryStr = localStorage.getItem('userPantry');
    let currentPantry = [];
    if (currentPantryStr) {
      try { currentPantry = JSON.parse(currentPantryStr); } catch(e) {}
    }
    
    // Get all items that are checked (strike-through) meaning the user picked them up
    const boughtItems = Object.keys(selectedItems).filter(item => !selectedItems[item]); 
    // wait, our UI logic has selectedItems[item] as true if it's NOT crossed out.
    // Let me check toggle logic:
    // When checked=!!selectedItems[item], textDecoration is line-through if NOT selectedItems.
    // Ah, wait: `textDecoration: selectedItems[item.item] ? 'none' : 'line-through'`
    // So if selectedItems[item] is FALSE, it is crossed out (purchased/found).
    // Let's grab all items from the plan, and any that are NOT in selectedItems are bought.
    const allPlanItems = [];
    if (shoppingPlan) {
      Object.values(shoppingPlan.grocery_list).forEach(items => {
        items.forEach(i => allPlanItems.push(i.item));
      });
    }
    const boughtItemsFiltered = allPlanItems.filter(item => !selectedItems[item]);

    const newPantry = [...new Set([...currentPantry, ...boughtItemsFiltered])];
    localStorage.setItem('userPantry', JSON.stringify(newPantry));

    alert("Awesome! You've completed your in-store trip.\n\nThe items you crossed off have been automatically added to your Smart Pantry!");
    navigate('/dashboard');
  };

  const handleSendToWhatsApp = () => {
    let text = "*NutriMind Grocery List*\n";
    text += "Here are the items we need to buy for this week's meal plan:\n\n";
    
    let hasItems = false;
    Object.entries(shoppingPlan.grocery_list).forEach(([category, items]) => {
      const itemsToBuy = items.filter(item => selectedItems[item.item]);
      if (itemsToBuy.length > 0) {
        hasItems = true;
        text += `*${category}*\n`;
        itemsToBuy.forEach(item => {
          text += `• ${item.item}\n`;
        });
        text += "\n";
      }
    });

    if (!hasItems) {
      text += "Looks like we already have everything we need! ✅\n";
    }

    window.open(`https://wa.me/?text=${encodeURIComponent(text)}`, '_blank');
  };

  // Helper to find product price
  const getProductPrice = (name) => {
    const prod = allProducts.find(p => p.name.toLowerCase() === name.toLowerCase() || p.name.toLowerCase().includes(name.toLowerCase()));
    return prod ? prod.price : 4.99; // Fallback price
  };

  return (
    <div style={{padding: '40px', maxWidth: '1200px', margin: '0 auto'}}>
      <h2 className="text-gradient" style={{marginBottom: '10px'}}>Smart Shopping Mode</h2>
      <p style={{marginBottom: '30px', color: 'var(--text-muted)'}}>Optimized for your budget, pantry inventory, and meal plan.</p>
      
      <div style={{display: 'flex', gap: '40px', flexWrap: 'wrap'}}>
        {/* Settings Panel */}
        <div className="glass-panel" style={{padding: '30px', flex: '1', minWidth: '300px', alignSelf: 'flex-start'}}>
          <form onSubmit={handleGeneratePlan}>
            <div style={{marginBottom: '20px'}}>
              <label style={{display: 'block', marginBottom: '8px', color: 'var(--text-muted)'}}>Weekly Budget ($)</label>
              <input type="number" name="budget" value={budget} onChange={e => setBudget(e.target.value)} style={{width: '100%', padding: '10px', background: '#0f172a', color: 'white', border: '1px solid #333', borderRadius: '8px'}} />
            </div>

            <div style={{marginBottom: '20px'}}>
              <label style={{display: 'block', marginBottom: '8px', color: 'var(--text-muted)'}}>In My Pantry</label>
              <input type="text" name="pantry" value={pantryInput} onChange={e => setPantryInput(e.target.value)} placeholder="e.g., Rice, Milk, Dal" style={{width: '100%', padding: '10px', background: '#0f172a', color: 'white', border: '1px solid #333', borderRadius: '8px'}} />
              <p style={{fontSize: '0.8rem', color: '#64748b', marginTop: '5px'}}>We'll automatically remove these from your grocery list.</p>
            </div>

            <div style={{marginBottom: '20px'}}>
              <label style={{display: 'block', marginBottom: '8px', color: 'var(--text-muted)'}}>Preferred Store</label>
              <select name="store" value={store} onChange={e => setStore(e.target.value)} style={{width: '100%', padding: '10px', background: '#0f172a', color: 'white', border: '1px solid #333', borderRadius: '8px'}}>
                <option value="walmart">Walmart</option>
                <option value="costco">Costco</option>
                <option value="amazon_fresh">Amazon Fresh</option>
              </select>
            </div>

            <button type="submit" data-testid="generate-plan" className="btn btn-primary" style={{width: '100%'}}>
              {loading ? "Optimizing..." : "Generate Plan"}
            </button>
            {error && <p style={{color: 'red', marginTop: '10px'}}>{error}</p>}
          </form>
        </div>

        {/* Results Panel */}
        <div style={{flex: '2', minWidth: '500px'}}>
          {!shoppingPlan && !loading && (
            <div className="glass-panel" style={{padding: '30px', textAlign: 'center'}}>
               <p style={{color: 'var(--text-muted)'}}>Configure your budget and pantry to generate an optimized list.</p>
            </div>
          )}

          {loading && <div className="glass-panel" style={{padding: '30px', textAlign: 'center'}}>Generating intelligent shopping list...</div>}

          {shoppingPlan && (
            <div className="glass-panel" style={{padding: '30px'}}>
              {/* Shopping Mode Toggle */}
              <div style={{display: 'flex', gap: '10px', marginBottom: '30px', background: 'rgba(0,0,0,0.3)', padding: '5px', borderRadius: '12px'}}>
                <button 
                  onClick={() => setShoppingMode('online')} 
                  style={{flex: 1, padding: '12px', border: 'none', borderRadius: '8px', cursor: 'pointer', background: shoppingMode === 'online' ? 'var(--primary-color)' : 'transparent', color: 'white', fontWeight: 'bold', transition: 'all 0.3s'}}>
                  Online Shopping (Add to Cart)
                </button>
                <button 
                  onClick={() => setShoppingMode('instore')} 
                  style={{flex: 1, padding: '12px', border: 'none', borderRadius: '8px', cursor: 'pointer', background: shoppingMode === 'instore' ? 'var(--secondary-color)' : 'transparent', color: 'white', fontWeight: 'bold', transition: 'all 0.3s'}}>
                  In-Store Shopping (Aisle Route)
                </button>
              </div>

              {/* Header Info */}
              <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', padding: '15px', background: 'rgba(99, 102, 241, 0.1)', border: '1px solid var(--primary-color)', borderRadius: '8px'}}>
                <div>
                  <h2 style={{margin: 0, color: 'var(--primary-color)'}}>Estimated Total: ${shoppingPlan.total_cost}</h2>
                  <p style={{margin: 0, color: shoppingPlan.status.includes("Adjusted") ? "#f59e0b" : "var(--text-muted)", fontSize: '0.9rem'}}>{shoppingPlan.status}</p>
                </div>
                <button className="btn btn-secondary" onClick={() => navigate('/cart')}>View Cart</button>
              </div>

              {/* Price Comparison */}
              {shoppingPlan.store_totals && (
                <div style={{marginBottom: '30px', padding: '20px', background: 'rgba(255,255,255,0.05)', border: '1px solid #333', borderRadius: '12px'}}>
                  <h3 style={{marginBottom: '15px', fontSize: '1.1rem'}}>Price Comparison <span style={{fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 'normal'}}>(Click to Select)</span></h3>
                  <div style={{display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '15px', textAlign: 'center'}}>
                    {Object.entries(shoppingPlan.store_totals).map(([s, total]) => (
                      <div 
                        key={s} 
                        onClick={() => { setStore(s); handleGeneratePlan(null, s, pantryInput.split(',').map(i => i.trim())); }}
                        style={{
                          padding: '15px', 
                          cursor: 'pointer',
                          background: s === shoppingPlan.best_store ? 'rgba(34, 197, 94, 0.2)' : 'transparent', 
                          borderRadius: '8px', 
                          border: s === store ? '2px solid var(--primary-color)' : s === shoppingPlan.best_store ? '2px solid #22c55e' : '1px solid #444',
                          transition: 'all 0.2s',
                          position: 'relative'
                        }}>
                        {s === store && <div style={{position: 'absolute', top: '-10px', right: '-10px', background: 'var(--primary-color)', color: 'white', borderRadius: '50%', width: '24px', height: '24px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.8rem', fontWeight: 'bold'}}>✓</div>}
                        <div style={{textTransform: 'capitalize', color: s === store ? 'white' : 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '5px', fontWeight: s === store ? 'bold' : 'normal'}}>{s.replace('_', ' ')}</div>
                        <div style={{fontSize: '1.4rem', fontWeight: 'bold', color: s === store ? 'white' : 'inherit'}}>${total.toFixed(2)}</div>
                        {s === shoppingPlan.best_store && <div style={{color: '#22c55e', fontSize: '0.8rem', marginTop: '8px', fontWeight: 'bold', textTransform: 'uppercase', letterSpacing: '1px'}}>Best Store</div>}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Content Based on Mode */}
              {shoppingMode === 'instore' ? (
                <>
                  <h3 style={{marginBottom: '15px', fontSize: '1.2rem', color: 'var(--secondary-color)'}}>Aisle-by-Aisle Route ({store})</h3>
                  <p style={{color: 'var(--text-muted)', marginBottom: '20px', fontSize: '0.9rem'}}>Walk through the store in this exact order to save time.</p>
                  
                  <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px'}}>
                    {Object.entries(shoppingPlan.grocery_list).map(([category, items]) => (
                      <div key={category} style={{background: 'rgba(0,0,0,0.4)', padding: '20px', borderRadius: '8px', borderTop: '3px solid var(--secondary-color)'}}>
                        <h4 style={{marginBottom: '15px', color: 'white', fontSize: '1.1rem'}}>{category}</h4>
                        {items.length === 0 ? (
                          <p style={{fontSize: '0.85rem', color: 'var(--text-muted)'}}>Empty</p>
                        ) : (
                          items.map((item, idx) => (
                            <div key={idx} style={{display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px'}}>
                              <input 
                                type="checkbox" 
                                style={{accentColor: 'var(--secondary-color)', width: '18px', height: '18px'}} 
                                checked={!!selectedItems[item.item]}
                                onChange={() => toggleItem(item.item, item.quantity)}
                              />
                              <span style={{fontSize: '0.95rem', color: selectedItems[item.item] ? 'white' : 'var(--text-muted)', textDecoration: selectedItems[item.item] ? 'none' : 'line-through'}}>{item.item}</span>
                              <span style={{marginLeft: 'auto', color: 'var(--text-muted)', fontSize: '0.85rem'}}>x{item.quantity}</span>
                            </div>
                          ))
                        )}
                      </div>
                    ))}
                  </div>
                </>
              ) : (
                <>
                  <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px'}}>
                    <div>
                      <h3 style={{fontSize: '1.2rem', color: 'var(--primary-color)'}}>Online Store Products</h3>
                      <p style={{color: 'var(--text-muted)', fontSize: '0.9rem'}}>Directly add needed items from your plan to your cart.</p>
                    </div>
                    <button className="btn btn-primary" onClick={handleBulkCheckout}>Add All Checked & Checkout</button>
                  </div>

                  <div style={{display: 'flex', flexDirection: 'column', gap: '30px'}}>
                    {Object.entries(shoppingPlan.grocery_list).map(([category, items]) => {
                      if (items.length === 0) return null;
                      return (
                        <div key={category}>
                          <h4 style={{marginBottom: '15px', color: 'white', fontSize: '1.2rem', borderBottom: '1px solid #333', paddingBottom: '10px'}}>{category}</h4>
                          <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '20px'}}>
                            {items.map((item, idx) => {
                              const price = getProductPrice(item.item);
                              return (
                                <div key={idx} style={{background: 'rgba(0,0,0,0.4)', padding: '20px', borderRadius: '12px', border: '1px solid #333', display: 'flex', flexDirection: 'column'}}>
                                  <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '15px'}}>
                                    <div>
                                      <h4 style={{fontSize: '1.1rem', marginBottom: '5px'}}>{item.item}</h4>
                                      <div style={{color: 'var(--primary-color)', fontWeight: 'bold'}}>${price.toFixed(2)}</div>
                                    </div>
                                    <input 
                                        type="checkbox" 
                                        style={{accentColor: 'var(--primary-color)', width: '20px', height: '20px'}} 
                                        checked={!!selectedItems[item.item]}
                                        onChange={() => toggleItem(item.item, item.quantity)}
                                    />
                                  </div>
                                  
                                  {cartQuantities[item.item] ? (
                                    <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#0f172a', borderRadius: '8px', overflow: 'hidden', border: '1px solid #333', marginTop: 'auto'}}>
                                      <button onClick={() => handleUpdateQuantity(item.item, -1)} style={{padding: '10px 15px', background: 'transparent', border: 'none', color: 'white', cursor: 'pointer', fontSize: '1.2rem', flex: 1}}>-</button>
                                      <span style={{padding: '0 10px', minWidth: '40px', textAlign: 'center', fontWeight: 'bold'}}>{cartQuantities[item.item]}</span>
                                      <button onClick={() => handleUpdateQuantity(item.item, 1)} style={{padding: '10px 15px', background: 'transparent', border: 'none', color: 'white', cursor: 'pointer', fontSize: '1.2rem', flex: 1}}>+</button>
                                    </div>
                                  ) : (
                                    <button 
                                      className="btn btn-secondary" 
                                      style={{marginTop: 'auto', width: '100%', padding: '10px'}}
                                      onClick={() => addToCartDirectly(item.item, 1)}
                                    >
                                      Add to Cart
                                    </button>
                                  )}
                                </div>
                              )
                            })}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </>
              )}

            </div>
          )}

          <div style={{marginTop: '40px', display: 'flex', justifyContent: 'space-between', borderTop: '1px solid #333', paddingTop: '20px'}}>
            <button className="btn btn-secondary" onClick={() => navigate('/pantry')}>
              ⬅ Back to Pantry
            </button>
            {shoppingMode === 'online' ? (
              <button className="btn btn-primary" onClick={() => navigate('/cart')}>
                Proceed to Cart 🛒 ➡
              </button>
            ) : (
              <div style={{display: 'flex', gap: '15px'}}>
                <button className="btn btn-secondary" onClick={handleSendToWhatsApp} style={{padding: '12px 24px', fontSize: '1.1rem'}}>
                  Send to WhatsApp 💬
                </button>
                <button className="btn btn-primary" onClick={handleCompleteInstore} style={{background: 'var(--secondary-color)', border: 'none', padding: '12px 24px', fontSize: '1.1rem'}}>
                  Complete In-Store Trip ✅
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
