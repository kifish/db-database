class DBDB(object):
    def __init__(self,f):
        self._storge = Storage(f) #分开写，self._storge为了检查cursor的关闭还是打开
        self._tree = BinaryTree(self._storge) # self._tree 用于查找

    #db[key]
    def __getitem__(self,key):
        self._assert_not_closed()
        return self._tree.get(key)

    def _assert_not_closed(self):
        if self._storge.closed:
            raise ValueError('Database closed.')

    def __setitem__(self,key,value):
        self._assert_not_closed()
        return self._tree.set(key)

    def commit(self):
        self._assert_not_closed()
        self._tree.commit()
        
