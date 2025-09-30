
class Stack:

    def __init__(self, size: int):
        """Stack implementation.

        Values pushed passed the size of the stack limit are silently dropped.

        Args:
            size (int): The max size of the stack.
        """
        if not isinstance(size, int) or size < 1:
            raise ValueError(f"Invalid size for class {self.__class__}: {size}")

        self.size = size
        self.values = [None]*size

    def push(self, item: object) -> None:
        """Push an object to the top of the stack.

        If pushing this item would cause too many items to be in the stack,
        the item at the bottom of the stack is silently discarded.

        Args:
            item (object): The item to push.
        """
        self.values.insert(0, item)
        if len(self.values) > self.size:
            self.values = self.values[:self.size]

    def peek(self, index=0) -> object:
        """Peek at the item at the given index.

        Args:
            index (int, optional): The index to peek at. Defaults to 0.

        Returns:
            object: The item at the given index.
        """
        return self.values[index]
