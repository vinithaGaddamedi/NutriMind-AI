# NutriMind Test Strategy

## 🎯 Approach & Philosophy
Our strategy emphasizes the **Test Automation Pyramid**: pushing validation down to the lowest possible level to ensure fast, reliable, and decoupled execution.

1. **Unit Tests (Backend/Frontend):** Fast execution, isolated.
2. **API Tests:** Core business logic validation (Fastest ROI).
3. **Integration Tests (Cross-Layer):** Validation of state bridging UI to Backend.
4. **UI Tests:** Focused strictly on User Journey mapping.
5. **Mobile Tests:** Core device interaction verification.

## 🌉 Why API > UI
UI automation is inherently slower and more brittle. We prioritize API tests (`pytest` + `requests`) to validate business rules (e.g., adding to cart, recommendation algorithms, order totaling). The UI tests (`Playwright`) simply verify that the React client properly visualizes these core states.

## 🔗 Cross-Layer Testing Approach
The most critical part of our automation architecture is **Cross-Layer Validation**. 
Instead of testing purely in silos:
- **Scenario 1:** A Playwright script adds an item to the cart via the UI, but the assertion is handled by a direct API call to `/cart/{user_id}`. This proves the Frontend properly triggered the API layer and the Database committed the state.
- **Scenario 2:** An API script creates an order directly via `/order`, and a Playwright UI script asserts that the order appears on the user's dashboard.

This guarantees true End-to-End state continuity and demonstrates Test Architect-level design.
