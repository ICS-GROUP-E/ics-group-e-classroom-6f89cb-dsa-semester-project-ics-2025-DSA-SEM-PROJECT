# bst_doctorlookup.py

class Doctor:
    def __init__(self, name, specialty):
        self.name = name
        self.specialty = specialty

    def __str__(self):
        return f"{self.name} ({self.specialty})"


class Node:
    def __init__(self, doctor):
        self.doctor = doctor
        self.left = None
        self.right = None


class DoctorBST:
    def __init__(self):
        self.root = None

    def insertDoctor(self, doctor):
        def _insert(node, doctor):
            if not node:
                return Node(doctor)
            if doctor.name < node.doctor.name:
                node.left = _insert(node.left, doctor)
            elif doctor.name > node.doctor.name:
                node.right = _insert(node.right, doctor)
            return node

        self.root = _insert(self.root, doctor)

    def searchDoctor(self, name):
        def _search(node, name):
            if not node:
                return None
            if name == node.doctor.name:
                return node.doctor
            elif name < node.doctor.name:
                return _search(node.left, name)
            else:
                return _search(node.right, name)

        return _search(self.root, name)

    def updateDoctor(self, name, new_specialty):
        doctor = self.searchDoctor(name)
        if doctor:
            doctor.specialty = new_specialty
            return True
        return False

    def deleteDoctor(self, name):
        def _delete(node, name):
            if not node:
                return node
            if name < node.doctor.name:
                node.left = _delete(node.left, name)
            elif name > node.doctor.name:
                node.right = _delete(node.right, name)
            else:
                if not node.left:
                    return node.right
                if not node.right:
                    return node.left
                min_larger = self.getMin(node.right)
                node.doctor = min_larger.doctor
                node.right = _delete(node.right, min_larger.doctor.name)
            return node

        self.root = _delete(self.root, name)

    def getMin(self, node):
        while node.left:
            node = node.left
        return node

    def inorderTraversal(self):
        def _inorder(node):
            return _inorder(node.left) + [node.doctor] + _inorder(node.right) if node else []
        return _inorder(self.root)
