import os
import re

from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=ENV_PATH)
class PropertiesReader:
    """
    @author：     JiaGuo
    @emil：       1520047927@qq.com
    @date：       Created in 2025/4/1 10:32
    @description：读取 .properties 文件，支持环境变量替换
    @modified By：
    @version:     1.1
    """
    ENV_VAR_PATTERN = re.compile(r"\$\{(\w+)}")

    @staticmethod
    def read_properties(path: str) -> dict:
        properties = {}
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = map(str.strip, line.split("=", 1))
                value = PropertiesReader._replace_env_vars(value)
                properties[key] = value
        return properties

    @staticmethod
    def _replace_env_vars(value: str) -> str:
        def replacer(match):
            env_var = match.group(1)
            return os.getenv(env_var, f"${{{env_var}}}")  # 保留格式如果找不到

        return PropertiesReader.ENV_VAR_PATTERN.sub(replacer, value)

