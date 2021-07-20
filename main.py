import sqlite3
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager

Builder.load_file("design.kv")

conn = sqlite3.connect("contactsbook.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS contacts (id SERIAL PRIMARY KEY, name VARCHAR NOT NULL UNIQUE, email VARCHAR UNIQUE, phone VARCHAR UNIQUE)")

class Menu(Screen):

    def findScreen(self):
        self.manager.current = "contactsearch"

    def manageScreen(self):
        self.manager.current = "managecontacts"

class ContactSearch(Screen):

    global contactdetails

    def search(self, name, email, phone):
        query = cur.execute(f"SELECT * from contacts WHERE name = '{name}' OR email = '{email}' OR phone = '{phone}'")
        contactdetail = query.fetchall()

        try:
            self.ids.contactName.text = "Name: " + contactdetail[0][1]
            self.ids.contactPhone.text = "Email: " + contactdetail[0][2]
            self.ids.contactEmail.text = "Phone Number: " + contactdetail[0][3]
        except:
            self.ids.contactName.text = "Cannot find contact. Try again?"
            self.ids.contactPhone.text = ""
            self.ids.contactEmail.text = ""

    def mainmenu(self):
        self.manager.current = "menu"
    pass

class ManageContacts(Screen):

    def add(self, name, email, phone):
        cur.execute(f"INSERT INTO contacts (name, email, phone) VALUES ('{name}', '{email}', '{phone}')")
        self.manager.current = "menu"

    def delete(self, name, email, phone):
        cur.execute(f"DELETE from contacts WHERE name = '{name}' OR email = '{email}' OR phone = '{phone}'")
        self.manager.current = "menu"

    def mainmenu(self):
        self.manager.current = "menu"


class RootWidget(ScreenManager):
    pass

class MainApp(App):

    def build(self):
        return RootWidget()

    def on_stop(self):
        conn.commit()
        conn.close()
        print("Program finished")

if __name__ == "__main__":
    MainApp().run()