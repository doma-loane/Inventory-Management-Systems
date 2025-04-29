class Command:
    def __init__(self, name=None, callback=None, params=None, **kwargs):
        """
        Initialize the Command class.

        :param name: The name of the command.
        :param callback: The callback function to execute.
        :param params: A list of parameters for the command.
        :param kwargs: Additional keyword arguments.
        """
        self.name = name
        self.callback = callback
        self.params = params or []

    def invoke(self, ctx):
        # Execute the callback function with the resolved parameters
        return ctx.invoke(self.callback, **ctx.params)

def greet(name="World"):
    print(f"Hello, {name}!")
