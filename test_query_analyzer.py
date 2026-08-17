import unittest
import query_analyzer as qa


class FakeRoot:
    def __init__(self):
        self._destroyed = False
        self.mainloop_calls = 0

    def withdraw(self):
        return None

    def destroy(self):
        self._destroyed = True

    def winfo_exists(self):
        return not self._destroyed

    def mainloop(self):
        self.mainloop_calls += 1
        self._destroyed = True

    def update(self):
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


class FakeWidget:
    def __init__(self):
        self._destroyed = False

    def pack(self, *args, **kwargs):
        return None

    def destroy(self):
        self._destroyed = True

    def insert(self, *args, **kwargs):
        return None

    def get(self, *args, **kwargs):
        return "alpha\nbeta\n"

    def winfo_exists(self):
        return not self._destroyed

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


class KeywordDialogRegressionTest(unittest.TestCase):
    def test_prompt_for_keyword_updates_uses_tk_mainloop(self):
        root = FakeRoot()
        dialog = FakeWidget()
        text_widget = FakeWidget()
        saved_keywords = {"keywords": ["alpha", "beta"]}

        qa.messagebox.showinfo = lambda *args, **kwargs: None
        qa.messagebox.askyesno = lambda *args, **kwargs: True
        qa.load_saved_custom_keywords = lambda: saved_keywords["keywords"]
        qa.save_custom_keywords = lambda keywords: saved_keywords.__setitem__("keywords", keywords)
        qa.Tk = lambda: root
        qa.Toplevel = lambda *args, **kwargs: dialog
        qa.Label = lambda *args, **kwargs: FakeWidget()
        qa.Button = lambda *args, **kwargs: FakeWidget()
        qa.Frame = lambda *args, **kwargs: FakeWidget()
        qa.Text = lambda *args, **kwargs: text_widget

        result = qa.prompt_for_keyword_updates()

        self.assertEqual(result, ["alpha", "beta"])
        self.assertEqual(root.mainloop_calls, 1)


if __name__ == "__main__":
    unittest.main()
