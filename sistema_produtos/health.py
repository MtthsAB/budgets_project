from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.core.cache import cache
import os
import time

@csrf_exempt
@require_http_methods(["GET", "HEAD"])
def health_check(request):
    """
    Health check endpoint for load balancers and monitoring systems.
    
    Checks:
    - Database connectivity
    - Cache connectivity (if configured)
    - Application readiness
    
    Returns HTTP 200 if healthy, HTTP 503 if unhealthy.
    """
    start_time = time.time()
    health_status = {
        "status": "healthy",
        "timestamp": int(time.time()),
        "version": os.getenv("APP_VERSION", "unknown"),
        "checks": {}
    }
    
    # Check database connectivity
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        health_status["checks"]["database"] = {"status": "healthy", "response_time_ms": 0}
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    # Check cache connectivity (if Redis is configured)
    try:
        cache.set("health_check", "ok", 10)
        if cache.get("health_check") == "ok":
            health_status["checks"]["cache"] = {"status": "healthy", "response_time_ms": 0}
        else:
            health_status["checks"]["cache"] = {"status": "unhealthy", "error": "Cache write/read failed"}
    except Exception as e:
        health_status["checks"]["cache"] = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    # Calculate total response time
    total_time = int((time.time() - start_time) * 1000)
    health_status["response_time_ms"] = total_time
    
    # Return appropriate status code
    status_code = 200 if health_status["status"] == "healthy" else 503
    
    return JsonResponse(health_status, status=status_code)

@csrf_exempt
@require_http_methods(["GET"])
def readiness_check(request):
    """
    Readiness check endpoint - simpler version for container readiness probes.
    """
    try:
        # Quick database check
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        
        return JsonResponse({
            "status": "ready",
            "timestamp": int(time.time()),
            "version": os.getenv("APP_VERSION", "unknown")
        })
    except Exception as e:
        return JsonResponse({
            "status": "not_ready",
            "error": str(e),
            "timestamp": int(time.time())
        }, status=503)

@csrf_exempt
@require_http_methods(["GET"])
def liveness_check(request):
    """
    Liveness check endpoint - minimal check for container liveness probes.
    """
    return JsonResponse({
        "status": "alive",
        "timestamp": int(time.time()),
        "version": os.getenv("APP_VERSION", "unknown")
    })
