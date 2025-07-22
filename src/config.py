
from dynaconf import Dynaconf
settings = Dynaconf(
envvar_prefix="DYNACONF",
settings_files=['base.toml','settings.9.toml', '.secrets.toml'],
)
        