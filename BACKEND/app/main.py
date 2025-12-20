from fastapi import FastAPI
from app.api import blood_search , health , donors , donation_camps , analytics , inventory_logs , admin , admin_auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Smart Blood Bank System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # frontend access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(blood_search.router)
app.include_router(donors.router)
app.include_router(donation_camps.router)
app.include_router(analytics.router)
app.include_router(inventory_logs.router)
app.include_router(admin_auth.router)
app.include_router(admin.router)