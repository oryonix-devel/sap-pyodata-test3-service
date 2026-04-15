"""
A very basic hello-world program that invokes an action function and returns
a string along with result of the greet action function.
"""

import onix


@onix.action
def greet(arg: str):
    return f"Greetings, {arg}"


@onix.flow
def hello_world(arg: str):
    ret1 = greet(arg="Hi, Guest1")

    return (
        f"hello_world invoked with arg: {arg}. "
        f"Greet action returned: {ret1} "
    )
