from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import cart, order, recommendation, meal, shopping, pantry

app = FastAPI(
    title="NutriMind Platform API",
    description="API for the AI-powered Grocery and Meal Planner application",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cart.router, prefix="/api/cart", tags=["Cart"])
app.include_router(order.router, prefix="/api/order", tags=["Order"])
app.include_router(recommendation.router, prefix="/api/recommendations", tags=["Recommendations"])
app.include_router(meal.router, prefix="/api/meal", tags=["Meal Planner"])
app.include_router(shopping.router, prefix="/api/shopping", tags=["Shopping"])
app.include_router(pantry.router, prefix="/api/pantry", tags=["Pantry"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the NutriMind Platform API"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/products")
def get_products():
    from routes.cart import PRODUCTS
    return [{"id": k, **v} for k, v in PRODUCTS.items()]

# To run the app locally:
# uvicorn main:app --reload
