from vedro.core import ExcInfo

__all__ = ("create_exc_info",)


def create_exc_info(exception: BaseException) -> ExcInfo:
    return ExcInfo(type(exception), exception, traceback=None)
