import asyncio


def task_factory(loop, coro):
    task = asyncio.tasks.Task(coro, loop=loop)
    if task._source_traceback:
        del task._source_traceback[-1]

    try:
        task.context = asyncio.Task.current_task(loop=loop).context
    except AttributeError:
        task.context = {}

    return task


def get(key, default=None):
    task = asyncio.Task.current_task()
    if task:
        return task.context.get(key, default)
    else:
        raise ValueError("No event loop found, key %s couldn't be set" % key)


def set(key, value):
    task = asyncio.Task.current_task()
    if task:
        task.context[key] = value
    else:
        raise ValueError("No event loop found, key %s couldn't be set" % key)
