import tkinter as tk
from main import tokenize
from main import Parser

class SyntaxHighlighter:
    def __init__(self, root):
        self.root = root
        self.text = tk.Text(root, wrap='word', font=('Consolas', 12))
        self.error_label = tk.Label(root, text='', fg='red', anchor='w')
        self.error_label.pack(fill='x')
        self.text.pack(expand=1, fill='both')
        self.text.bind('<KeyRelease>', self.on_change)
        self.parse_button = tk.Button(root, text="Parse Kontrolü", command=self.check_parse)
        self.parse_button.pack(pady=5)

        self.token_colors = {
            'KEYWORD': 'blue',
            'IDENTIFIER': 'black',
            'NUMBER': 'darkorange',
            'STRING': 'green',
            'OPERATOR': 'red',
            'DELIMITER': 'purple',
            'COMMENT': 'gray'
        }

        for token_type, color in self.token_colors.items():
            self.text.tag_config(token_type, foreground=color)

        self.text.tag_config('SYNTAX_ERROR', background='red')

    def on_change(self, event=None):
        self.root.after(100, self.highlight)

    def check_parse(self):
        code = self.text.get('1.0', tk.END)
        tokens = tokenize(code)

        try:
            parser = Parser(tokens)
            parser.parse()
            self.error_label.config(text="✅ Parse edilebilir!", fg='green')
            print("Parse başarılı!")
        except SyntaxError as e:
            self.error_label.config(text=f"❌ Parse Hatası: {e}", fg='red')
            print("Parse hatası:", e)    

    def highlight(self):
        code = self.text.get('1.0', tk.END)
        tokens = tokenize(code)
        print("TOKENS:", tokens)  # Debug amaçlı

    # Temizle
        for tag in list(self.token_colors) + ['SYNTAX_ERROR']:
            self.text.tag_remove(tag, '1.0', tk.END)

        self.error_label.config(text='')  # Hata mesajını temizle

    # Token bazlı renklendirme
        index = '1.0'
        positions = []
        for tok_type, tok_val in tokens:
            if tok_type == 'NEWLINE':
                line, col = map(int, index.split('.'))
                index = f"{line+1}.0"
                continue
            start = index
            line, col = map(int, index.split('.'))
            end_col = col + len(tok_val)
            end = f"{line}.{end_col}"

            self.text.tag_add(tok_type, start, end)
            positions.append((start, end))
            index = end

    # ✅ Parser kontrolü ve hata gösterimi
        try:
            parser = Parser(tokens)
            parser.parse()
        except SyntaxError as e:
            print("SYNTAX ERROR:", e)  # Terminalde gör
            self.error_label.config(text=str(e))  # GUI'de göster

            # Hatalı token konumu tahmini
            if parser.pos < len(tokens):
                line = 1
                col = 0
                for i in range(parser.pos):
                    tok = tokens[i]
                    if tok[0] == 'NEWLINE':
                        line += 1
                        col = 0
                    else:
                        col += len(tok[1])
                error_index = f"{line}.{col}"
                self.text.tag_add('SYNTAX_ERROR', error_index, f"{line}.end")


# GUI başlat
root = tk.Tk()
root.title("Real-Time Python Syntax Highlighter")
SyntaxHighlighter(root)
root.mainloop()
