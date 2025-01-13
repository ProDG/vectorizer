from uuid import UUID


class AnyInt:
    """ Placeholder to put in unittests in case we expect some integer
        (let's say, an object ID) which is hard to determine and we don't
        care about specific value.
    """

    def __eq__(self, other):
        if isinstance(other, str):
            try:
                int(other)
                return True
            except ValueError:
                return False

        return isinstance(other, int)


class AnyFloat:
    def __eq__(self, other):
        if isinstance(other, str):
            try:
                float(other)
                return True
            except ValueError:
                return False

        return isinstance(other, float)


class AnyStr:
    """ Placeholder to put in unittests in case we expect some string
        (let's say, an date string) which is hard to determine and we don't
        care about specific value.
    """

    def __eq__(self, other):
        return isinstance(other, str)


class AnyUUID:
    """ Placeholder to put in unittests in case we expect some integer
        (let's say, an object UUID) which is hard to determine and we don't
        care about specific value.
    """

    def __eq__(self, other):
        try:
            if isinstance(other, str):
                UUID(other, version=4)
                return True
        except ValueError:
            pass

        return False
