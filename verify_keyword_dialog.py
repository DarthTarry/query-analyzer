import query_analyzer as qa

class FakeWidget:
    def __init__(self):
        self._destroyed = False

    def pack(self, *args, **kwargs):
        return None

    def destroy(self):
        self._destroyed = True

    def winfo_exists(self):
        return not self._destroyed

    def update(self):
        self._destroyed = True
        return None

    def update_idletasks(self):
        return None

    def focus_set(self):
        return None

    def grab_set(self):
        return None

    def transient(self, *args, **kwargs):
        return None

    def title(self, *args, **kwargs):
        return None

    def geometry(self, *args, **kwargs):
        return None

    def resizable(self, *args, **kwargs):
        return None

    def minsize(self, *args, **kwargs):
        return None

    def protocol(self, *args, **kwargs):
        return None

    def bind(self, *args, **kwargs):
        return None

    def insert(self, *args, **kwargs):
        return None

    def get(self, *args, **kwargs):
        return "alpha\nbeta\n"

    def pack_configure(self, *args, **kwargs):
        return None

qa.messagebox.showinfo = lambda *args, **kwargs: None
qa.messagebox.askyesno = lambda *args, **kwargs: True
qa.load_saved_custom_keywords = lambda: []
qa.save_custom_keywords = lambda keywords: None
qa.Tk = lambda: FakeWidget()
qa.Toplevel = lambda *args, **kwargs: FakeWidget()
qa.Label = lambda *args, **kwargs: FakeWidget()
qa.Button = lambda *args, **kwargs: FakeWidget()
qa.Frame = lambda *args, **kwargs: FakeWidget()
qa.Text = lambda *args, **kwargs: FakeWidget()

result = qa.prompt_for_keyword_updates()
print(result)
assert result == ['alpha', 'beta']
print('VERIFIED: keyword dialog exits normally and returns entered terms')
