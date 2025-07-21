
from dynaconf import Dynaconf

if globals()['book']:
    print(f"global book = {globals()['book']}")
    settings = Dynaconf(
        envvar_prefix="DYNACONF",
        settings_files=['base.toml',f'settings.{globals()['book']}.toml', '.secrets.toml'],
    )
else:
    settings = Dynaconf(
        envvar_prefix="DYNACONF",
        settings_files=['base.toml','settings.toml', '.secrets.toml'],
    )

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
