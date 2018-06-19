from typing import Generic, TypeVar, Union, Any, Optional, cast, overload


T = TypeVar("T")  # Success type
E = TypeVar("E")  # Error type


class Result(Generic[T, E]):
    """
    A simple `Result` type inspired by Rust.

    Not all methods (https://doc.rust-lang.org/std/result/enum.Result.html)
    have been implemented, only the ones that make sense in the Python context.
    """
    def __init__(self, is_ok: bool, value: Union[T, E], force: bool = False) -> None:
        """Do not call this constructor, use the Ok or Err class methods instead.

        There are no type guarantees on the value if this is called directly.

        Args:
            is_ok:
                Whether this represents an OK result
            value:
                The value inside the result
            force:
                Force creation of the object. This is false by default to prevent
                accidentally creating instance of a Result in an unsafe way.

        """
        if force is not True:
            raise RuntimeError("Don't instantiate a Result directly. "
                               "Use the Ok(value) and Err(error) class methods instead.")
        else:
            self._is_ok = is_ok
            self._value = value

    def __eq__(self, other: Any) -> bool:
        return (self.__class__ == other.__class__ and
                self.is_ok() == cast(Result, other).is_ok() and
                self._value == other._value)

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return hash((self.is_ok(), self._value))

    def __repr__(self) -> str:
        if self.is_ok():
            return 'Ok({})'.format(repr(self._value))
        else:
            return 'Err({})'.format(repr(self._value))

    @classmethod
    @overload
    def Ok(cls) -> 'Result[bool, E]':
        pass

    @classmethod
    @overload
    def Ok(cls, value: T) -> 'Result[T, E]':
        pass

    @classmethod
    def Ok(cls, value: Any = True) -> 'Result[Any, E]':
        return cls(is_ok=True, value=value, force=True)

    @classmethod
    def Err(cls, error: E) -> 'Result[T, E]':
        return cls(is_ok=False, value=error, force=True)

    def is_ok(self) -> bool:
        return self._is_ok

    def is_err(self) -> bool:
        return not self._is_ok

    def ok(self) -> Optional[T]:
        """
        Return the value if it is an `Ok` type. Return `None` if it is an `Err`.
        """
        return cast(T, self._value) if self.is_ok() else None

    def err(self) -> Optional[E]:
        """
        Return the error if this is an `Err` type. Return `None` otherwise.
        """
        return cast(E, self._value) if self.is_err() else None

    @property
    def value(self) -> Union[T, E]:
        """
        Return the inner value. This might be either the ok or the error type.
        """
        return self._value

    # TODO: Implement __iter__ for destructuring


@overload
def Ok() -> Result[bool, Any]:
    pass


@overload
def Ok(value: T) -> Result[T, Any]:
    pass


def Ok(value: Any = True) -> Result[Any, Any]:
    """
    Shortcut function to create a new Result.
    """
    return Result.Ok(value)


def Err(error: E) -> Result[Any, E]:
    """
    Shortcut function to create a new Result.
    """
    return Result.Err(error)
