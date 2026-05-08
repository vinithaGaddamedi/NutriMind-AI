import { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import { useNavigate } from 'react-router-dom';

export default function MealPlanner({ userId }) {
  const [planType, setPlanType] = useState('single');
  const navigate = useNavigate();
  const [diet, setDiet] = useState('vegetarian');
  
  // Single Profile
  const [singleProfile, setSingleProfile] = useState({
    name: "Vinitha", age: 30, weight: 70, height: 170, gender: "female", goal: "weight_loss",
    allergiesInput: "", dislikesInput: ""
  });

  // Family Profiles
  const [familyMembers, setFamilyMembers] = useState([
    { name: "User1", age: 30, weight: 70, height: 170, gender: "male", goal: "weight_loss" },
    { name: "User2", age: 60, weight: 65, height: 160, gender: "female", goal: "maintenance" }
  ]);

  const [generatedPlan, setGeneratedPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Load from cache on mount
  useEffect(() => {
    const cachedPlan = localStorage.getItem('lastMealPlan');
    if (cachedPlan) {
      try {
        setGeneratedPlan(JSON.parse(cachedPlan));
      } catch (e) {
        console.error("Failed to load cached plan");
      }
    }
  }, []);

  const validateInputs = () => {
    if (planType === 'single') {
      if (!singleProfile.age || singleProfile.age <= 0) return "Age must be greater than 0";
      if (!singleProfile.weight || singleProfile.weight <= 0) return "Weight must be greater than 0";
      if (!singleProfile.height || singleProfile.height <= 0) return "Height must be greater than 0";
    } else {
      for (let i = 0; i < familyMembers.length; i++) {
        const m = familyMembers[i];
        if (!m.age || m.age <= 0) return `Member ${i+1} age must be greater than 0`;
        if (!m.weight || m.weight <= 0) return `Member ${i+1} weight must be greater than 0`;
        if (!m.height || m.height <= 0) return `Member ${i+1} height must be greater than 0`;
      }
    }
    return null;
  };

  const handleGeneratePlan = async (e) => {
    if (e) e.preventDefault();
    setError('');
    
    const validationError = validateInputs();
    if (validationError) {
      setError(validationError);
      return;
    }

    setLoading(true);
    const payload = { diet };
    
    try {
      let currentPantry = [];
      const currentPantryStr = localStorage.getItem('userPantry');
      if (currentPantryStr) {
        try { 
          const parsed = JSON.parse(currentPantryStr);
          currentPantry = Object.keys(parsed).filter(k => parsed[k]);
        } catch(e) {}
      }

      let dataToSave;
      if (planType === 'single') {
        const p = {
           ...singleProfile,
           allergies: singleProfile.allergiesInput ? singleProfile.allergiesInput.split(',').map(s=>s.trim()).filter(Boolean) : [],
           dislikes: singleProfile.dislikesInput ? singleProfile.dislikesInput.split(',').map(s=>s.trim()).filter(Boolean) : [],
           pantry: currentPantry
        };
        payload.profile = p;
        const res = await apiClient.post('/meal/meal-plan/single', payload);
        dataToSave = { type: 'single', data: res.data };
      } else {
        const m = familyMembers.map(member => ({
           ...member,
           pantry: currentPantry
        }));
        payload.members = m;
        const res = await apiClient.post('/meal/meal-plan/family', payload);
        dataToSave = { type: 'family', data: res.data };
      }
      
      setGeneratedPlan(dataToSave);
      localStorage.setItem('lastMealPlan', JSON.stringify(dataToSave));
    } catch (err) {
      console.error("Error generating plan", err);
      setError("Failed to generate plan. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  const addFamilyMember = () => {
    setFamilyMembers([...familyMembers, { name: `User${familyMembers.length + 1}`, age: 25, weight: 65, height: 165, gender: "female", goal: "maintenance" }]);
  };

  const updateFamilyMember = (index, field, value) => {
    const updated = [...familyMembers];
    updated[index][field] = value;
    setFamilyMembers(updated);
  };

  return (
    <div style={{padding: '40px', maxWidth: '1200px', margin: '0 auto'}}>
      <h2 className="text-gradient" style={{marginBottom: '10px'}}>Personal + Family Nutrition Meal Planner</h2>
      <p style={{marginBottom: '30px', color: 'var(--text-muted)'}}>Optimized for BMR + Goals. One family, one cooking session, tailored portions.</p>
      
      <div style={{display: 'flex', gap: '40px', flexWrap: 'wrap'}}>
        {/* Form Column */}
        <div className="glass-panel" style={{padding: '30px', flex: '1', minWidth: '350px', alignSelf: 'flex-start'}}>
          <div style={{display: 'flex', gap: '10px', marginBottom: '20px'}}>
            <button type="button" className={`btn ${planType === 'single' ? 'btn-primary' : 'btn-secondary'}`} onClick={() => setPlanType('single')}>Single Plan</button>
            <button type="button" className={`btn ${planType === 'family' ? 'btn-primary' : 'btn-secondary'}`} onClick={() => setPlanType('family')}>Family Mode</button>
          </div>

          <form onSubmit={handleGeneratePlan}>
            <div style={{marginBottom: '20px'}}>
              <label style={{display: 'block', marginBottom: '8px', color: 'var(--text-muted)'}}>Diet Preference</label>
              <select name="diet" value={diet} onChange={e => setDiet(e.target.value)} style={{width: '100%', padding: '10px', background: '#1e293b', color: 'white', border: '1px solid #333', borderRadius: '8px'}}>
                <option value="vegetarian">Vegetarian</option>
                <option value="nonveg">Non-Vegetarian</option>
              </select>
            </div>

            {planType === 'single' ? (
              <div style={{padding: '15px', background: 'rgba(0,0,0,0.2)', borderRadius: '8px', marginBottom: '20px'}}>
                <h4 style={{marginBottom: '15px'}}>Your Profile</h4>
                <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px'}}>
                  <div style={{gridColumn: 'span 2'}}>
                    <label style={{display: 'block', marginBottom: '8px', color: 'var(--text-muted)', fontSize: '0.9rem'}}>Name</label>
                    <input type="text" name="name" placeholder="Name" value={singleProfile.name} onChange={e => setSingleProfile({...singleProfile, name: e.target.value})} style={{width: '100%', padding: '10px', background: '#0f172a', color: 'white', border: '1px solid #333', borderRadius: '8px'}} />
                  </div>
                  <div>
                    <label style={{display: 'block', marginBottom: '8px', color: 'var(--text-muted)', fontSize: '0.9rem'}}>Age</label>
                    <input type="number" name="age" placeholder="Age" value={singleProfile.age || ''} onChange={e => setSingleProfile({...singleProfile, age: parseInt(e.target.value)})} style={{width: '100%', padding: '10px', background: '#0f172a', color: 'white', border: '1px solid #333', borderRadius: '8px'}} />
                  </div>
                  <div>
                    <label style={{display: 'block', marginBottom: '8px', color: 'var(--text-muted)', fontSize: '0.9rem'}}>Weight (kg)</label>
                    <input type="number" name="weight" placeholder="Weight (kg)" value={singleProfile.weight || ''} onChange={e => setSingleProfile({...singleProfile, weight: parseInt(e.target.value)})} style={{width: '100%', padding: '10px', background: '#0f172a', color: 'white', border: '1px solid #333', borderRadius: '8px'}} />
                  </div>
                  <div>
                    <label style={{display: 'block', marginBottom: '8px', color: 'var(--text-muted)', fontSize: '0.9rem'}}>Height (cm)</label>
                    <input type="number" name="height" placeholder="Height (cm)" value={singleProfile.height || ''} onChange={e => setSingleProfile({...singleProfile, height: parseInt(e.target.value)})} style={{width: '100%', padding: '10px', background: '#0f172a', color: 'white', border: '1px solid #333', borderRadius: '8px'}} />
                  </div>
                  <div>
                    <label style={{display: 'block', marginBottom: '8px', color: 'var(--text-muted)', fontSize: '0.9rem'}}>Gender</label>
                    <select name="gender" value={singleProfile.gender} onChange={e => setSingleProfile({...singleProfile, gender: e.target.value})} style={{width: '100%', padding: '10px', background: '#0f172a', color: 'white', border: '1px solid #333', borderRadius: '8px'}}>
                      <option value="male">Male</option>
                      <option value="female">Female</option>
                    </select>
                  </div>
                  <div style={{gridColumn: 'span 2'}}>
                    <label style={{display: 'block', marginBottom: '8px', color: 'var(--text-muted)', fontSize: '0.9rem'}}>Goal</label>
                    <select name="goal" value={singleProfile.goal} onChange={e => setSingleProfile({...singleProfile, goal: e.target.value})} style={{width: '100%', padding: '10px', background: '#0f172a', color: 'white', border: '1px solid #333', borderRadius: '8px'}}>
                      <option value="weight_loss">Weight Loss (-500 kcal)</option>
                      <option value="maintenance">Maintenance</option>
                      <option value="muscle_gain">Muscle Gain (+300 kcal)</option>
                    </select>
                  </div>
                  <div style={{gridColumn: 'span 2'}}>
                    <label style={{display: 'block', marginBottom: '8px', color: 'var(--text-muted)', fontSize: '0.9rem'}}>Allergies (comma separated)</label>
                    <input type="text" placeholder="E.g., Peanuts, Dairy" value={singleProfile.allergiesInput || ''} onChange={e => setSingleProfile({...singleProfile, allergiesInput: e.target.value})} style={{width: '100%', padding: '10px', background: '#0f172a', color: 'white', border: '1px solid #333', borderRadius: '8px'}} />
                  </div>
                  <div style={{gridColumn: 'span 2'}}>
                    <label style={{display: 'block', marginBottom: '8px', color: 'var(--text-muted)', fontSize: '0.9rem'}}>Dislikes (comma separated)</label>
                    <input type="text" placeholder="E.g., Mushroom, Beef" value={singleProfile.dislikesInput || ''} onChange={e => setSingleProfile({...singleProfile, dislikesInput: e.target.value})} style={{width: '100%', padding: '10px', background: '#0f172a', color: 'white', border: '1px solid #333', borderRadius: '8px'}} />
                  </div>
                </div>
              </div>
            ) : (
              <div style={{marginBottom: '20px'}}>
                <h4 style={{marginBottom: '15px'}}>Family Members</h4>
                {familyMembers.map((member, idx) => (
                  <div key={idx} style={{padding: '15px', background: 'rgba(0,0,0,0.2)', borderRadius: '8px', marginBottom: '10px'}}>
                    <div style={{marginBottom: '10px'}}>
                      <label style={{display: 'block', marginBottom: '8px', color: 'var(--text-muted)', fontSize: '0.9rem'}}>Member Name</label>
                      <input type="text" value={member.name} onChange={e => updateFamilyMember(idx, 'name', e.target.value)} style={{width: '100%', padding: '10px', background: '#0f172a', color: 'white', border: '1px solid #333', borderRadius: '8px'}} />
                    </div>
                    <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px'}}>
                      <div>
                        <label style={{display: 'block', marginBottom: '8px', color: 'var(--text-muted)', fontSize: '0.9rem'}}>Age</label>
                        <input type="number" name={`member${idx+1}_age`} placeholder="Age" value={member.age || ''} onChange={e => updateFamilyMember(idx, 'age', parseInt(e.target.value))} style={{width: '100%', padding: '10px', background: '#0f172a', color: 'white', border: '1px solid #333', borderRadius: '8px'}} />
                      </div>
                      <div>
                        <label style={{display: 'block', marginBottom: '8px', color: 'var(--text-muted)', fontSize: '0.9rem'}}>Weight (kg)</label>
                        <input type="number" name={`member${idx+1}_weight`} placeholder="Weight (kg)" value={member.weight || ''} onChange={e => updateFamilyMember(idx, 'weight', parseInt(e.target.value))} style={{width: '100%', padding: '10px', background: '#0f172a', color: 'white', border: '1px solid #333', borderRadius: '8px'}} />
                      </div>
                      <div>
                        <label style={{display: 'block', marginBottom: '8px', color: 'var(--text-muted)', fontSize: '0.9rem'}}>Goal</label>
                        <select value={member.goal} onChange={e => updateFamilyMember(idx, 'goal', e.target.value)} style={{width: '100%', padding: '10px', background: '#0f172a', color: 'white', border: '1px solid #333', borderRadius: '8px'}}>
                          <option value="weight_loss">Weight Loss</option>
                          <option value="maintenance">Maintenance</option>
                          <option value="muscle_gain">Muscle Gain</option>
                        </select>
                      </div>
                      <div>
                        <label style={{display: 'block', marginBottom: '8px', color: 'var(--text-muted)', fontSize: '0.9rem'}}>Gender</label>
                        <select value={member.gender} onChange={e => updateFamilyMember(idx, 'gender', e.target.value)} style={{width: '100%', padding: '10px', background: '#0f172a', color: 'white', border: '1px solid #333', borderRadius: '8px'}}>
                          <option value="male">Male</option>
                          <option value="female">Female</option>
                        </select>
                      </div>
                    </div>
                  </div>
                ))}
                <button type="button" onClick={addFamilyMember} className="btn btn-secondary" style={{width: '100%', fontSize: '0.8rem'}}>+ Add Member</button>
              </div>
            )}
            
            {error && <p style={{color: 'red', marginBottom: '15px'}}>{error}</p>}
            
            <button type="submit" data-testid="generate-btn" className="btn btn-primary" style={{width: '100%'}}>
              {loading ? "Generating..." : "Generate Weekly Plan"}
            </button>
          </form>
        </div>

        {/* Results Column */}
        <div className="glass-panel" style={{padding: '30px', flex: '2', minWidth: '400px'}}>
          {loading && <p>Generating your smart meal plan...</p>}
          
          {!loading && !generatedPlan && <p>No plan generated yet</p>}

          {!loading && generatedPlan && (
            <>
              {generatedPlan.type === 'single' ? (
                <div style={{marginBottom: '30px', padding: '20px', background: 'rgba(99, 102, 241, 0.1)', border: '1px solid var(--primary-color)', borderRadius: '12px'}}>
                  <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start'}}>
                    <div style={{flex: 1}}>
                      <div style={{marginBottom: '15px'}}>
                        <h3 style={{marginBottom: '10px'}}>{generatedPlan.data.user}'s Nutrition Goal</h3>
                        <div style={{fontSize: '2.5rem', fontWeight: 'bold', color: 'var(--primary-color)'}}>
                          {generatedPlan.data.calories} <span style={{fontSize: '1.2rem', fontWeight: 'normal'}}>kcal/day</span>
                        </div>
                      </div>

                      <div style={{display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '15px', background: 'rgba(0,0,0,0.2)', padding: '15px', borderRadius: '10px'}}>
                        <div style={{textAlign: 'center'}}><div style={{fontSize: '1.2rem', color: 'white', fontWeight: 'bold'}}>{generatedPlan.data.macros.protein_g}g</div><div style={{fontSize: '0.8rem', color: 'var(--text-muted)'}}>Protein</div></div>
                        <div style={{textAlign: 'center'}}><div style={{fontSize: '1.2rem', color: 'white', fontWeight: 'bold'}}>{generatedPlan.data.macros.carbs_g}g</div><div style={{fontSize: '0.8rem', color: 'var(--text-muted)'}}>Carbs</div></div>
                        <div style={{textAlign: 'center'}}><div style={{fontSize: '1.2rem', color: 'white', fontWeight: 'bold'}}>{generatedPlan.data.macros.fats_g}g</div><div style={{fontSize: '0.8rem', color: 'var(--text-muted)'}}>Fats</div></div>
                        <div style={{textAlign: 'center'}}><div style={{fontSize: '1.2rem', color: 'white', fontWeight: 'bold'}}>{generatedPlan.data.macros.iron_mg}mg</div><div style={{fontSize: '0.8rem', color: 'var(--text-muted)'}}>Iron</div></div>
                        <div style={{textAlign: 'center'}}><div style={{fontSize: '1.2rem', color: 'white', fontWeight: 'bold'}}>{generatedPlan.data.macros.calcium_mg}mg</div><div style={{fontSize: '0.8rem', color: 'var(--text-muted)'}}>Calcium</div></div>
                        <div style={{textAlign: 'center'}}><div style={{fontSize: '1.2rem', color: 'white', fontWeight: 'bold'}}>{generatedPlan.data.macros.vitamin_a_iu}IU</div><div style={{fontSize: '0.8rem', color: 'var(--text-muted)'}}>Vitamin A</div></div>
                      </div>
                    </div>
                    {generatedPlan.data.nutrition_score && (
                      <div style={{textAlign: 'center', background: 'rgba(34, 197, 94, 0.2)', padding: '10px 20px', borderRadius: '12px', border: '1px solid #22c55e'}}>
                        <div style={{fontSize: '0.9rem', color: 'var(--text-muted)'}}>Nutrition Score</div>
                        <div style={{fontSize: '2rem', fontWeight: 'bold', color: '#22c55e'}}>{generatedPlan.data.nutrition_score}/10</div>
                      </div>
                    )}
                  </div>
                </div>
              ) : (
                <div style={{marginBottom: '30px', padding: '20px', background: 'rgba(236, 72, 153, 0.1)', border: '1px solid var(--secondary-color)', borderRadius: '12px'}}>
                  <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start'}}>
                    <div>
                      <h3 style={{marginBottom: '10px'}}>Family Common Plan</h3>
                      <p style={{color: 'var(--text-muted)', fontSize: '0.9rem'}}>All members eat the same meals, but portion sizes vary by caloric need.</p>
                    </div>
                    {generatedPlan.data.nutrition_score && (
                      <div style={{textAlign: 'center', background: 'rgba(34, 197, 94, 0.2)', padding: '10px 20px', borderRadius: '12px', border: '1px solid #22c55e'}}>
                        <div style={{fontSize: '0.9rem', color: 'var(--text-muted)'}}>Family Nutrition Score</div>
                        <div style={{fontSize: '2rem', fontWeight: 'bold', color: '#22c55e'}}>{generatedPlan.data.nutrition_score}/10</div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {generatedPlan.data.insights && generatedPlan.data.insights.length > 0 && (
                <div style={{marginBottom: '30px', padding: '15px 20px', background: 'rgba(255, 255, 255, 0.05)', borderRadius: '8px', borderLeft: '4px solid #a855f7'}}>
                  <h4 style={{marginBottom: '10px', color: '#a855f7', display: 'flex', alignItems: 'center', gap: '8px'}}>
                    ✨ AI Insights
                  </h4>
                  <ul style={{margin: 0, paddingLeft: '20px', color: 'var(--text-light)', fontSize: '0.95rem'}}>
                    {generatedPlan.data.insights.map((insight, i) => (
                      <li key={i} style={{marginBottom: '5px'}}>{insight}</li>
                    ))}
                  </ul>
                </div>
              )}

              <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px'}}>
                <h3 style={{margin: 0}}>Weekly Plan</h3>
                <button onClick={handleGeneratePlan} className="btn btn-secondary" style={{padding: '8px 16px', fontSize: '0.85rem'}}>Regenerate Plan</button>
              </div>

              <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '15px'}}>
                {generatedPlan.type === 'single' ? (
                  Object.entries(generatedPlan.data.meal_plan).map(([day, meals]) => (
                    <div key={day} style={{background: 'rgba(0,0,0,0.2)', padding: '15px', borderRadius: '8px'}}>
                      <h4 style={{textTransform: 'capitalize', marginBottom: '15px', color: 'var(--primary-color)'}}>{day}</h4>
                      <ul style={{listStyle: 'none', padding: 0, fontSize: '0.95rem', color: 'var(--text-light)'}}>
                        <li style={{marginBottom: '15px'}}>
                          <strong>Breakfast:</strong> <span style={{color: 'var(--text-muted)'}}>{meals.breakfast.name}</span>
                          <div style={{fontSize: '0.8rem', color: 'var(--primary-color)', marginTop: '4px'}}>💡 Why? → {meals.breakfast.reason}</div>
                        </li>
                        <li style={{marginBottom: '15px'}}>
                          <strong>Lunch:</strong> <span style={{color: 'var(--text-muted)'}}>{meals.lunch.name}</span>
                          <div style={{fontSize: '0.8rem', color: 'var(--primary-color)', marginTop: '4px'}}>💡 Why? → {meals.lunch.reason}</div>
                        </li>
                        <li>
                          <strong>Dinner:</strong> <span style={{color: 'var(--text-muted)'}}>{meals.dinner.name}</span>
                          <div style={{fontSize: '0.8rem', color: 'var(--primary-color)', marginTop: '4px'}}>💡 Why? → {meals.dinner.reason}</div>
                        </li>
                      </ul>
                    </div>
                  ))
                ) : (
                  Object.entries(generatedPlan.data.family_plan).map(([day, plan]) => (
                    <div key={day} style={{background: 'rgba(0,0,0,0.2)', padding: '15px', borderRadius: '8px', gridColumn: '1 / -1'}}>
                      <h4 style={{textTransform: 'capitalize', marginBottom: '15px', color: 'var(--primary-color)', fontSize: '1.2rem', borderBottom: '1px solid #333', paddingBottom: '10px'}}>{day}</h4>
                      
                      <div style={{display: 'flex', gap: '20px', flexWrap: 'wrap'}}>
                        <div style={{flex: 1, minWidth: '200px'}}>
                          <h5 style={{color: 'var(--text-muted)', marginBottom: '10px'}}>Common Meals</h5>
                          <ul style={{listStyle: 'none', padding: 0, fontSize: '0.95rem'}}>
                            <li style={{marginBottom: '12px'}}>
                              <strong>☀️ Breakfast:</strong> {plan.meals.breakfast.name}
                              <div style={{fontSize: '0.8rem', color: 'var(--primary-color)'}}>💡 {plan.meals.breakfast.reason}</div>
                            </li>
                            <li style={{marginBottom: '12px'}}>
                              <strong>🍲 Lunch:</strong> {plan.meals.lunch.name}
                              <div style={{fontSize: '0.8rem', color: 'var(--primary-color)'}}>💡 {plan.meals.lunch.reason}</div>
                            </li>
                            <li style={{marginBottom: '8px'}}>
                              <strong>🌙 Dinner:</strong> {plan.meals.dinner.name}
                              <div style={{fontSize: '0.8rem', color: 'var(--primary-color)'}}>💡 {plan.meals.dinner.reason}</div>
                            </li>
                          </ul>
                        </div>
                        
                        <div style={{flex: 1, minWidth: '200px', background: 'rgba(255,255,255,0.05)', padding: '15px', borderRadius: '8px'}}>
                          <h5 style={{color: 'var(--text-muted)', marginBottom: '10px'}}>Portions</h5>
                          {Object.entries(plan.portions).map(([member, mplan]) => (
                             <div key={member} style={{marginBottom: '10px', display: 'flex', justifyContent: 'space-between'}}>
                               <strong style={{color: 'white'}}>{member}:</strong>
                               <span style={{color: 'var(--secondary-color)', fontWeight: 'bold'}}>{mplan.calories} kcal</span>
                             </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>

              <div style={{marginTop: '40px', display: 'flex', justifyContent: 'space-between', borderTop: '1px solid #333', paddingTop: '20px'}}>
                <button className="btn btn-secondary" onClick={() => navigate('/dashboard')}>
                  ⬅ Back to Dashboard
                </button>
                <button className="btn btn-primary" onClick={() => navigate('/pantry')}>
                  Proceed to Pantry 📦 ➡
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
