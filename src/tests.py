import pytest
from datetime import datetime
from src.Stacks import ActivityStack, ActivityNode  

class Test:
    def test_push_pop(self):
        """Test basic LIFO functionality."""
        stack = ActivityStack()
        stack.push("ADD", "ISBN: 123")
        assert stack.pop()[1] == "ISBN: 123"  # Verifying book details

    def test_max_size(self):
        """Test stack pruning when exceeding max_size."""
        stack = ActivityStack()
        for i in range(15):
            stack.push(f"ACTION_{i}", f"DATA_{i}")
        assert stack.size == 10  # enforcing the maximum max size

    def test_empty_stack(self):
        """Test edge cases (empty stack)."""
        stack = ActivityStack()
        assert stack.pop() is None
        assert stack.peek() is None

if __name__ == "__main__":
    pytest.main()