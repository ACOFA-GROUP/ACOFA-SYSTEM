diff --git a/main.py b/main.py
index 6c6eaf892c8014f40e7d44855f21aa990ce0e434..79c8dc12596769a4ebb0e58fe7a53626fd1d983d 100644
--- a/main.py
+++ b/main.py
@@ -1,82 +1,75 @@
 from fastapi import FastAPI, Request
 from fastapi.middleware.cors import CORSMiddleware
 from fastapi.responses import JSONResponse
 import time
 
 app = FastAPI(
-title=“ACOFA AGROLINK API”,
-description=“API pour la gestion agricole intelligente”,
-version=“1.0.0”,
-docs_url=”/docs”,
-redoc_url=”/redoc”
+    title="ACOFA AGROLINK API",
+    description="API pour la gestion agricole intelligente",
+    version="1.0.0",
+    docs_url="/docs",
+    redoc_url="/redoc",
 )
 
 # Configuration CORS - SEULE MODIFICATION ICI
-
 app.add_middleware(
-CORSMiddleware,
-allow_origins=[”*”],
-allow_credentials=True,
-allow_methods=[”*”],
-allow_headers=[”*”],
-expose_headers=[”*”],  # <- AJOUT DE CETTE LIGNE
+    CORSMiddleware,
+    allow_origins=["*"],
+    allow_credentials=True,
+    allow_methods=["*"],
+    allow_headers=["*"],
+    expose_headers=["*"],  # <- AJOUT DE CETTE LIGNE
 )
 
 # Middleware temps de réponse
-
-@app.middleware(“http”)
+@app.middleware("http")
 async def add_process_time_header(request: Request, call_next):
-start_time = time.time()
-response = await call_next(request)
-process_time = time.time() - start_time
-response.headers[“X-Process-Time”] = str(process_time)
-return response
+    start_time = time.time()
+    response = await call_next(request)
+    process_time = time.time() - start_time
+    response.headers["X-Process-Time"] = str(process_time)
+    return response
 
 # Import des routes
-
 from api.v1 import auth, producteurs
 
 # Include routers
+app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
+app.include_router(producteurs.router, prefix="/api/v1/producteurs", tags=["Producteurs"])
 
-app.include_router(auth.router, prefix=”/api/v1/auth”, tags=[“Authentication”])
-app.include_router(producteurs.router, prefix=”/api/v1/producteurs”, tags=[“Producteurs”])
 
-@app.get(”/”)
+@app.get("/")
 async def root():
-return {
-“message”: “ACOFA AGROLINK API”,
-“version”: “1.0.0”,
-“status”: “running”,
-“docs”: “/docs”
-}
+    return {
+        "message": "ACOFA AGROLINK API",
+        "version": "1.0.0",
+        "status": "running",
+        "docs": "/docs",
+    }
 
-@app.get(”/health”)
+
+@app.get("/health")
 async def health_check():
-try:
-from sqlalchemy import text
-from database.connection import SessionLocal
+    try:
+        from sqlalchemy import text
+        from database.connection import SessionLocal
 
-```
-    """
-    db = SessionLocal()
-    db.execute(text("SELECT 1"))
-    db.close()
-    """
-    
-    return {
-        "status": "healthy",
-        "database": "connected"
-    }
-except Exception as e:
-    return JSONResponse(
-        status_code=503,
-        content={
-            "status": "unhealthy",
-            "database": "disconnected",
-            "error": str(e)
-        }
-    )
-```
+        """
+        db = SessionLocal()
+        db.execute(text("SELECT 1"))
+        db.close()
+        """
 
-“””
-“””
+        return {
+            "status": "healthy",
+            "database": "connected",
+        }
+    except Exception as e:
+        return JSONResponse(
+            status_code=503,
+            content={
+                "status": "unhealthy",
+                "database": "disconnected",
+                "error": str(e),
+            },
+        )
