class HashTable:
    """
    A wrapper around Python's dictionary to act as our primary task storage.
    It provides O(1) average time complexity for insertions, lookups, and deletions.
    """
    def __init__(self):
        """Initializes the hash table."""
        self._data={}

    def insert(self,key,value):
        """Inserts a key value pair into the hash table."""
        self._data[key]=value

    def lookup(self,key):
        """Looks up a value by its key"""
        return self._data.get(key)

    def delete(self,key):
        """Deletes a key-value pair by its key"""
        if key in self._data:
            del self._data[key]

    def get_all_items(self):
        """Returns a list of all values in the hash table."""
        return list(self._data.values())

    def __contains__(self, key):
        """Allows for 'key in instance' checks."""
        return key in self._data