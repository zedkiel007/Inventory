from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
import datetime

class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, name, quantity, price):
        date = datetime.date.today()
        if name in self.products:
            self.products[name]['quantity'] += quantity
        else:
            self.products[name] = {'quantity': quantity, 'price': price, 'date': date}

class InventoryApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inventory = Inventory()

    def build(self):
        self.title = "Gudacas Litsong Manok Inventory"
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Title
        title_label = Label(text="Gudacas Inventory System", size_hint_y=0.1, font_size='18sp')
        main_layout.add_widget(title_label)

        # Buttons
        button_layout = GridLayout(cols=2, size_hint_y=0.15, spacing=5)
        input_btn = Button(text="Add Product")
        input_btn.bind(on_press=self.show_input_popup)
        button_layout.add_widget(input_btn)

        save_btn = Button(text="Save Report")
        save_btn.bind(on_press=self.save_report)
        button_layout.add_widget(save_btn)
        main_layout.add_widget(button_layout)

        # Inventory display
        scroll = ScrollView(size_hint=(1, 0.6))
        self.inventory_text = Label(text="No products yet", size_hint_y=None, markup=True)
        self.inventory_text.bind(texture_size=self.inventory_text.setter('size'))
        scroll.add_widget(self.inventory_text)
        main_layout.add_widget(scroll)

        # Messages
        self.message_text = TextInput(text="Welcome to Gudacas Inventory!\n", multiline=True, readonly=True, size_hint_y=0.15)
        main_layout.add_widget(self.message_text)

        self.update_display()
        return main_layout

    def show_input_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)

        name_input = TextInput(hint_text="Product Name (e.g. Litsong Manok)", multiline=False)
        qty_input = TextInput(hint_text="Quantity", input_filter='int', multiline=False)
        price_input = TextInput(hint_text="Price per piece", input_filter='float', multiline=False)

        add_btn = Button(text="Add to Inventory", size_hint_y=0.3)

        def add_product():
            try:
                name = name_input.text.strip()
                qty = int(qty_input.text)
                price = float(price_input.text)
                if name:
                    self.inventory.add_product(name, qty, price)
                    self.message_text.text += f"Added {qty} {name} @ ₱{price}\n"
                    self.update_display()
                    popup.dismiss()
                else:
                    self.message_text.text += "Please enter product name\n"
            except ValueError:
                self.message_text.text += "Invalid quantity or price\n"

        add_btn.bind(on_press=lambda x: add_product())
        content.add_widget(name_input)
        content.add_widget(qty_input)
        content.add_widget(price_input)
        content.add_widget(add_btn)

        popup = Popup(title='Add Gudacas Product', content=content, size_hint=(0.9, 0.7))
        popup.open()

    def update_display(self):
        if not self.inventory.products:
            self.inventory_text.text = "No products in inventory"
        else:
            text = "[b]Product | Qty | Price | Total | Date[/b]\n\n"
            total_value = 0
            for name, details in self.inventory.products.items():
                total = details['quantity'] * details['price']
                total_value += total
                text += f"{name}\n{details['quantity']} pcs @ ₱{details['price']} = ₱{total}\nAdded: {details['date']}\n\n"
            text += f"[b]Total Inventory Value: ₱{total_value}[/b]"
            self.inventory_text.text = text

    def save_report(self, instance):
        self.message_text.text += "Report saved locally!\n"

if __name__ == '__main__':
    InventoryApp().run()
