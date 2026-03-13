from aiogram import Router

from .admin import router as admin_router
from .profile import router as profile_router
from .registration import router as registration_router
from .start import router as start_router


def setup_handlers() -> Router:
    router = Router(name="root")
    router.include_router(admin_router)
    router.include_router(start_router)
    router.include_router(registration_router)
    router.include_router(profile_router)
    return router
