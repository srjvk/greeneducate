import time


ENERGY_PER_TOKEN_LOCAL_WH   = 0.0003   # 0.3 mWh per token, local GPU
ENERGY_PER_TOKEN_CLOUD_WH   = 0.001    # 1 mWh per token, data-centre overhead
CARBON_INTENSITY_KG_PER_KWH = 0.233    
OPENAI_COST_PER_1K_TOKENS   = 0.002    
LOCAL_COST_PER_KWH           = 0.15    

session_log: list[dict] = []

def record_request(tokens_used: int, model: str = "local"):
    session_log.append({
        "ts":     time.time(),
        "tokens": tokens_used,
        "model":  model,
    })

def get_session_metrics() -> dict:
    total_tokens = sum(r["tokens"] for r in session_log)
    total_requests = len(session_log)

    # Energy
    local_energy_kwh  = total_tokens * ENERGY_PER_TOKEN_LOCAL_WH  / 1000
    cloud_energy_kwh  = total_tokens * ENERGY_PER_TOKEN_CLOUD_WH  / 1000
    energy_saved_kwh  = cloud_energy_kwh - local_energy_kwh

    # Carbon
    local_carbon_kg   = local_energy_kwh * CARBON_INTENSITY_KG_PER_KWH
    cloud_carbon_kg   = cloud_energy_kwh * CARBON_INTENSITY_KG_PER_KWH
    carbon_saved_kg   = cloud_carbon_kg  - local_carbon_kg

    # Cost
    local_cost_usd    = local_energy_kwh * LOCAL_COST_PER_KWH
    cloud_cost_usd    = (total_tokens / 1000) * OPENAI_COST_PER_1K_TOKENS
    cost_saved_usd    = cloud_cost_usd - local_cost_usd

    return {
        "total_requests":    total_requests,
        "total_tokens":      total_tokens,
        "local_energy_kwh":  round(local_energy_kwh,  6),
        "cloud_energy_kwh":  round(cloud_energy_kwh,  6),
        "energy_saved_kwh":  round(energy_saved_kwh,  6),
        "local_carbon_kg":   round(local_carbon_kg,   6),
        "cloud_carbon_kg":   round(cloud_carbon_kg,   6),
        "carbon_saved_kg":   round(carbon_saved_kg,   6),
        "local_cost_usd":    round(local_cost_usd,    4),
        "cloud_cost_usd":    round(cloud_cost_usd,    4),
        "cost_saved_usd":    round(cost_saved_usd,    4),
    }