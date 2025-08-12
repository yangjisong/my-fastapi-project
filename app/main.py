# /fastapi-demo-project/app/main.py

from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager

# 从 config 模块导入 get_settings 函数和 get_project_version 函数
from app.core.config import Settings, get_settings, get_project_version , settings

# Lifespan: 在应用启动时调用 get_settings，触发配置加载和缓存
@asynccontextmanager
async def lifespan(app: FastAPI):
    get_settings()
    yield

app = FastAPI(
    title=settings.APP_NAME,
    # 动态从 pyproject.toml 读取版本号
    version=get_project_version(),
    lifespan=lifespan
)

@app.get("/a")
def read_root(
    # 使用 FastAPI 的依赖注入系统来获取配置实例
    # FastAPI 会自动调用 get_settings()，由于缓存的存在，这几乎没有开销
    settings: Settings = Depends(get_settings)
):
    """
    一个示例端点，演示如何访问配置。
    """
    return {
        "message": f"Hello from the {settings.APP_NAME}!",
        "environment": settings.ENVIRONMENT,
        "debug_mode": settings.DEBUG,
        # 演示如何访问嵌套的配置项
        "database_host": settings.DB.HOST,
        # 演示如何使用在模型中动态计算的属性
        "database_url_hidden_password": settings.DB.DATABASE_URL.replace(
            settings.DB.PASSWORD, "****"
        ),
        "app_version": get_project_version()
    }