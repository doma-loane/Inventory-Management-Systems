import click

@click.command()
@click.option("--name", default="World", help="Name to greet.")
def greet(name):
    """Greet the user by name."""
    print(f"Hello, {name}!")

if __name__ == "__main__":
    # Use Click's main entry point to invoke the command
    greet()
