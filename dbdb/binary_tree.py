class BinaryTree(LogicalBase):
    def _get(self,node,key):
        while node is not None:
            if key < node.key:
                node = self._follow(node.left_ref)
            elif key > node.key:
                node = self._follow(node.right_ref)
            else:
                return self._follow(node.value_ref)
        raise KeyError # 不存在对应key的k-v pair

    def _insert(self,node,key,value_ref):
        if node is None:
            new_node = BinaryNode(
                self.node_ref_class(),key,value_ref,self.node_ref_class(),1
            )
            # left,k,v,right,1
        elif key < node.key:
            new_node = BinaryNode.from_node(
                node,
                left_ref = self._insert(self._follow(node.left_ref),key,value_ref)
            )
        elif key > node.key:
            new_node = BinaryNode.from_node(
                node,
                right_ref = self._insert(self._follow(node.right_ref),key,value_ref)
            )
        else: #若key相同，则新的value覆盖旧的value
            new_node = BinaryNode.from_node(node,value_ref = value_ref)
        return self.node_ref_class(referent = new_node)

class BinaryNodeRef(ValueRef):
    def prepare_to_store(self,storage):
        if self._referent:
            self._referent.store_ref(storage)

class BinaryNode(object):
    def store_ref(self, storage):
        self.value_ref.store(storage)
        self.left_ref.store(storage)
        self.right_ref.store(storage)

    @staticmethod
    def referent_to_string(referent):
        return pickle.dumps({
            'left': referent.left_ref.address,
            'key': referent.key,
            'value': referent.value_ref.address,
            'right': referent.right_ref.address,
            'length':referent.length
        })
