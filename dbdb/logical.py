class LogicalBase(object):
    def get(self,key):
        if not self._storge.locked: # if locked,dirty read
            self._refresh_tree_ref()
        return self._get(self._follow(self._tree_ref),key)

    def _refresh_tree_ref(self):
        self._tree_ref = self.node_ref_class(address = self._storge.get_root_address())

    def set(self,key,value):
        if self._storge.lock(): #上锁，考虑到之前可能有进程写入并释放了锁，所以刷新获得最新数据
            self._refresh_tree_ref()
        self._tree_ref = self._insert(self._follow(self._tree_ref),key,self.value_ref_class(value))
        #  replaces the root tree node with a new tree containing the inserted (or updated) key/value.

    def commit(self):
        self._tree_ref.store(self._storge)
        self._storge.commit_root_address(self._tree_ref.address)

class ValueRef(object):
    def store(self,storage):
        if self._referent is not None and not self._address:
            self.prepare_to_store(storage)
            self._address = storage.write(self.referent_to_string(self._referent))
