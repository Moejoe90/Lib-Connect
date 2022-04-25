# define custom errors
class CustomErrors(Exception):
    """Base class for my custom exceptions"""
    pass


class PageNotFound(CustomErrors):
    """raises when page name not found in database"""
    pass


class PostNotFound(CustomErrors):
    """raises when post not found in database"""
    pass


