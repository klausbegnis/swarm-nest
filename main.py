"""
File: main.py
Project: replace with your project name
Created: Wednesday, 29th October 2025 4:03:14 pm
Author: replace with your name

Copyright (c) 2025 replace with your company. All rights reserved.
"""

if __name__ == "__main__":
    import uvicorn

    from app.config import settings

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        workers=settings.WORKERS,
        reload=settings.DEBUG,
    )
