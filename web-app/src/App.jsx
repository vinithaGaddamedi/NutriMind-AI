import { useState, useEffect } from 'react'
import { Routes, Route, Link, useNavigate, useLocation } from 'react-router-dom'
import './App.css'
import Login from './pages/Login'
import Products from './pages/Products'
import Cart from './pages/Cart'
import MealPlanner from './pages/MealPlanner'
import ShoppingMode from './pages/ShoppingMode'
import Dashboard from './pages/Dashboard'
import FeatureMealPlanner from './pages/FeatureMealPlanner'
import FeatureSmartCart from './pages/FeatureSmartCart'
import FeatureDelivery from './pages/FeatureDelivery'
import PantryScanner from './pages/Pantry'
import OrderSuccess from './pages/OrderSuccess'
import Orders from './pages/Orders'
import ChatWidget from './components/ChatWidget'

function App() {
  const [scrolled, setScrolled] = useState(false);
  const [userId, setUserId] = useState(null);
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleLogout = () => {
    setUserId(null);
    navigate('/');
  };

  return (
    <div className="app-container">
      <header className={scrolled || location.pathname !== '/' ? 'scrolled' : ''}>
        <Link to="/" className="logo text-gradient" style={{textDecoration: 'none'}}>NutriMind AI</Link>
        <ul className="nav-links">
          {userId ? (
            <>
              <li><Link to="/dashboard">Dashboard</Link></li>
              <li><Link to="/meal-planner">Meal Planner</Link></li>
              <li><Link to="/shopping">Shopping Mode</Link></li>
              <li><Link to="/pantry">Pantry</Link></li>
              <li><Link to="/products">Products</Link></li>
              <li><Link to="/cart">Cart</Link></li>
              <li><Link to="/orders">Orders</Link></li>
              <li><button onClick={handleLogout} className="btn btn-secondary" style={{ padding: '8px 20px', fontSize: '0.9rem' }}>Logout</button></li>
            </>
          ) : (
            <li><Link to="/login"><button className="btn btn-secondary" style={{ padding: '8px 20px', fontSize: '0.9rem' }}>Sign In</button></Link></li>
          )}
        </ul>
      </header>

      <main style={location.pathname !== '/' ? {paddingTop: '100px'} : {}}>
        <Routes>
          <Route path="/" element={
            <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
              <section className="hero">
                <div className="bg-shape shape-1"></div>
                <div className="bg-shape shape-2"></div>
                
                <h1 className="animate-fade-up">Groceries that <span className="text-gradient">think for you.</span></h1>
                <p className="animate-fade-up delay-100">
                  The AI-powered platform that learns your diet, plans your weekly meals, and auto-fills your cart with fresh groceries.
                </p>
                <div className="hero-buttons animate-fade-up delay-200">
                  <Link to="/login"><button className="btn btn-primary">Start Planning</button></Link>
                </div>
              </section>

              <section className="features" id="features">
                <Link to="/info-meal-planner" style={{textDecoration: 'none', color: 'inherit'}}>
                  <div className="feature-card glass-panel" style={{cursor: 'pointer'}}>
                    <div className="feature-icon">🥗</div>
                    <h3>AI Meal Planner</h3>
                    <p>Tell us your diet, goals, and allergies. Our AI generates a customized weekly menu in seconds.</p>
                  </div>
                </Link>
                <Link to="/info-smart-cart" style={{textDecoration: 'none', color: 'inherit'}}>
                  <div className="feature-card glass-panel" style={{cursor: 'pointer'}}>
                    <div className="feature-icon">🛒</div>
                    <h3>Smart Cart</h3>
                    <p>One-click add-to-cart for your entire meal plan. We optimize for price, freshness, and minimal waste.</p>
                  </div>
                </Link>
                <Link to="/info-delivery" style={{textDecoration: 'none', color: 'inherit'}}>
                  <div className="feature-card glass-panel" style={{cursor: 'pointer'}}>
                    <div className="feature-icon">⚡</div>
                    <h3>Fast Delivery</h3>
                    <p>Get your curated groceries delivered straight to your door within hours, ready for the week ahead.</p>
                  </div>
                </Link>
              </section>
            </div>
          } />
          <Route path="/login" element={<Login setUserId={setUserId} />} />
          <Route path="/info-meal-planner" element={<FeatureMealPlanner />} />
          <Route path="/info-smart-cart" element={<FeatureSmartCart />} />
          <Route path="/info-delivery" element={<FeatureDelivery />} />
          <Route path="/dashboard" element={<Dashboard userId={userId} />} />
          <Route path="/meal-planner" element={<MealPlanner userId={userId} />} />
          <Route path="/shopping" element={<ShoppingMode userId={userId} />} />
          <Route path="/pantry" element={<PantryScanner userId={userId} />} />
          <Route path="/products" element={<Products userId={userId} />} />
          <Route path="/cart" element={<Cart userId={userId} />} />
          <Route path="/orders" element={<Orders userId={userId} />} />
          <Route path="/order-success" element={<OrderSuccess />} />
        </Routes>

        <ChatWidget userId={userId} />
      </main>
    </div>
  )
}

export default App
