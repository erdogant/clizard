"""How to turn your existing argparse main() into a clizard interface."""
import argparse
from clizard import auto_cli


def run(username, package, clean=None, install=None, twine=None, verbose=None):
    """Your existing function, unchanged."""
    print(f"Releasing {package} as {username} (clean={clean}, twine={twine}, verbose={verbose})")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", type=str, help="Username on Github/Gitlab..")
    parser.add_argument("-p", "--package", type=str, help="Package name to be released.")
    parser.add_argument("-c", "--clean", type=int, choices=[0, 1], help="Remove local builds: [dist], [build] and [x.egg-info].")
    parser.add_argument("-i", "--install", type=int, choices=[0, 1], help="Install this versions on local machine.")
    parser.add_argument("-t", "--twine", type=str, help="Path to twine in case you have a custom build.")
    parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2, 3, 4, 5], help="Verbosity, higher number tends to more information.")
    args = parser.parse_args()

    # Instead of calling run(...) directly, build a CLI around it:
    def run_callback(cli):
        s = cli.config.settings
        run(s["username"], s["package"], clean=s["clean"], install=s["install"], twine=s["twine"], verbose=s["verbosity"])

    cli = auto_cli(parser, args=args, app_name="ReleaseTool", run_callback=run_callback)
    cli.run()


if __name__ == "__main__":
    main()
