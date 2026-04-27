# Given the root of a binary tree, return the inorder traversal of its nodes' values.
# In order is left, root, right

from typing import Iterable, Optional, List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution1:
    # note: I used yields here to avoid allocating too many lists. Its possible with lists and the speed
    # is close to the same, however it uses a bit less memory
    def _inorderTraversalIterable(self, root: TreeNode) -> Iterable[int]:
        if root.left:
            yield from self._inorderTraversalIterable(root.left)
        yield root.val
        if root.right:
            yield from self._inorderTraversalIterable(root.right)

    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []
        return list(self._inorderTraversalIterable(root))


# or even better, just keep a list avaiable to all the recursive functions and avoid the overhead of yielding up the stack frames multiple times:


class Solution2:
    def _inorderTraversalRec(self, root: TreeNode):
        if root.left:
            self._inorderTraversalRec(root.left)
        self.result.append(root.val)
        if root.right:
            self._inorderTraversalRec(root.right)

    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []
        self.result = []
        self._inorderTraversalRec(root)
        return self.result


# expect [1, 2, 3, 4]
print(Solution1().inorderTraversal(TreeNode(2, TreeNode(1), TreeNode(4, TreeNode(3)))))
print(Solution2().inorderTraversal(TreeNode(2, TreeNode(1), TreeNode(4, TreeNode(3)))))
