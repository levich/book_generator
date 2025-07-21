
from dynaconf import Dynaconf
settings = Dynaconf(
envvar_prefix="DYNACONF",
settings_files=['base.toml','settings.3.toml', '.secrets.toml'],
)
        