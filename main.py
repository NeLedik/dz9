import tkinter as tk
from tkinter import ttk
import sqlite3


# Класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.db = db
        self.init_main()
        self.view_records()

    def init_main(self):
        # Добавление фрейма
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Создание виджета Treeview
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'tel', 'email'), height=45, show='headings')

        # Добавление столбцов в виджет Treeview
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('tel', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)

        # Отображение названий столбцов виджета Treeview
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('tel', text='Телефон')
        self.tree.heading('email', text='E-mail')

        self.tree.pack(side=tk.LEFT)

        # Кнопка добавить контакт
        self.add_img = tk.PhotoImage(file='img/add.png')
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.add_img, command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)

        # Кнопка редактировать
        self.update_img = tk.PhotoImage(file='img/update.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.update_img, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        # Кнопка поиск
        self.search_img = tk.PhotoImage(file='img/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.search_img, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        # Кнопка удаление
        self.delete_img = tk.PhotoImage(file='img/delete.png')
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.delete_img, command=self.delete_record)
        btn_delete.pack(side=tk.LEFT)

        # Кнопка обновления
        self.refresh_img = tk.PhotoImage(file='img/refresh.png')
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.refresh_img, command=self.view_records)
        btn_delete.pack(side=tk.LEFT)

    # Функция добавления информации из БД в виджет Treeview
    def view_records(self):
        self.db.cursor.execute('''SELECT * FROM db''')

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

    # Функция добавления информации в БД
    def records(self, name, tel, email):
        self.db.insert_data(name, tel, email)
        self.view_records()

    # Функция изменения информации в БД
    def update_record(self, name, tel, email):
        self.db.cursor.execute(
            'UPDATE db SET name = ?, tel = ?, email = ? WHERE id = ?',
            (name, tel, email, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    # Функция удаления информации из БД
    def delete_record(self):
        for selection_item in self.tree.selection():
            self.db.cursor.execute('DELETE FROM db WHERE id = ?', (self.tree.set(selection_item, '#1')))
        self.db.conn.commit()
        self.view_records()

    # Функция поиска контакта по ФИО
    def search_records(self, name):
        name = ('%' + name + '%')
        self.db.cursor.execute('SELECT * FROM db WHERE name LIKE ?', (name,))

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

    # Открывает окно поиск
    def open_search_dialog(self):
        Search()

    # Открывает окно добавить
    def open_dialog(self):
        Child()

    # Открывает окно редактировать позицию
    def open_update_dialog(self):
        Update()


# Класс окна добавить
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_child()

    def init_child(self):
        self.title('Добавить')
        self.geometry('400x220')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        # Текст
        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text='Телефон:')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='E-mail:')
        label_sum.place(x=50, y=110)

        # Поля для ввода информации
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110)

        # Кнопки
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)

        self.btn_ok.bind('<Button-1>', lambda event:
                         self.view.records(self.entry_name.get(),
                                           self.entry_email.get(),
                                           self.entry_tel.get()))


# Класс окна редактировать позицию
class Update(Child):
    def __init__(self):
        super().__init__()
        self.db = db
        self.view = app
        self.default_data()
        self.init_edit()

    def init_edit(self):
        self.title('Редактировать позицию')
        # Кнопка редактировать
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event:
                      self.view.update_record(self.entry_name.get(),
                                              self.entry_email.get(),
                                              self.entry_tel.get()))
        btn_edit.bind('<Button-1>', lambda event:
                      self.destroy(), add='+')
        self.btn_ok.destroy()

    # Функция для вставления информации в поля
    def default_data(self):
        self.db.cursor.execute(
            "SELECT * FROM db WHERE id=?",
            self.view.tree.set(self.view.tree.selection()[0], "#1"), )
        row = self.db.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])


# Класс окна поиск
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.view = app
        self.init_search()

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100')
        self.resizable(False, False)

        # Текст
        label_search = tk.Label(self, text='Поиск:')
        label_search.place(x=50, y=20)

        # Поле ввода
        self.entry_search = tk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        # Кнопки
        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Найти')
        btn_search.place(x=105, y=50)

        btn_search.bind('<Button-1>', lambda event:
                        self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event:
                        self.destroy(), add='+')


# Класс ДБ
class DB:
    def __init__(self):
        # Подключение к БД
        self.conn = sqlite3.connect('db.db')
        self.cursor = self.conn.cursor()

        # Cоздание таблицы в БД
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS db(
                id INTEGER PRIMARY KEY,
                name TEXT,
                tel TEXT,
                email TEXT
            )'''
        )
        self.conn.commit()

    # Функция для вставления информации в БД
    def insert_data(self, name, tel, email):
        self.cursor.execute('''INSERT INTO db (name, tel, email) VALUES (?, ?, ?)''', (name, tel, email))
        self.conn.commit()


if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Телефонная книга')
    root.geometry('665x450')
    root.resizable(False, False)
    root.mainloop()
