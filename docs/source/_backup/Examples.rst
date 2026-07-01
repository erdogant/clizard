.. list-table:: Parameters of :func:`run`
   :widths: 15 10 65
   :header-rows: 1

   * - Name
     - Type
     - Description
   * - username
     - ``str``
     - Target repository account identifier (e.g., PyPI username).
   * - package
     - ``str``
     - Name, version specifier, or local path of the artifact to release.
   * - clean
     - ``bool | None``
     - Flag to purge build directories before execution. Optional; defaults to ``None``. After conversion from an integer argument, values `0` and `1` are interpreted as ``False`` and ``True`` respectively.
   * - install
     - ``bool | None``
     - Flag to resolve and install project dependencies first. Optional; defaults to ``None``. Integer arguments `0` and `1` are converted to ``False`` and ``True``.
   * - twine
     - ``str | None``
     - Path to a custom twine executable. Optional; defaults to ``None``.
   * - verbose
     - ``int | None``
     - Verbosity level for output information. Optional; defaults to ``None``.

.. code-block:: py
    import argparse
    from clizard import auto_cli
    from release_tool import run

    def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("-u", "--username", type=str, help="Username on Github/Gitlab…")
        parser.add_argument("-p", "--package", type=str, help="Package name to be released.")
        parser.add_argument(
            "-c",
            "--clean",
            type=int,
            choices=[0, 1],
            help="Remove local builds: [dist], [build] and [x.egg-info].",
        )
        parser.add_argument(
            "-i",
            "--install",
            type=int,
            choices=[0, 1],
            help="Install this version on the local machine.",
        )
        parser.add_argument(
            "-t",
            "--twine",
            type=str,
            help="Path to twine in case you have a custom build.",
        )
        parser.add_argument(
            "-v",
            "--verbosity",
            type=int,
            choices=[0, 1, 2, 3, 4, 5],
            help="Verbosity level; higher numbers provide more information.",
        )

        args = parser.parse_args()

        def run_callback(cli):
            s = cli.config.settings
            run(
                username=s["username"],
                package=s["package"],
                clean=bool(s["clean"]),
                install=bool(s["install"]),
                twine=s["twine"],
                verbose=s["verbosity"],
            )

        cli = auto_cli(parser, args=args, app_name="ReleaseTool", run_callback=run_callback)
        cli.run()

    if __name__ == "__main__":
        main()

.. include:: add_bottom.add