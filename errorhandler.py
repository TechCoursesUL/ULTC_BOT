import inspect


def ErrorHandler(f):
    async def decorator(*args, **kwargs):
        try:
            await args[1].response.defer()
            return await f(*args, **kwargs)
        except Exception as e:
            await args[1].followup.send(f"Command Failed- {e}")

    decorator.__name__ = f.__name__
    sig = inspect.signature(f)
    decorator.__signature__ = sig.replace(parameters=tuple(sig.parameters.values())[1:])
    return decorator
