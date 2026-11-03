from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.metrics import dp

# Устанавливаем темный фон для всего приложения
Window.clearcolor = (0.08, 0.08, 0.1, 1)

# Кастомный стиль для выпадающих списков (чтобы они были темными)
class DarkSpinnerOption(SpinnerOption):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.15, 0.15, 0.2, 1)
        self.color = (1, 1, 1, 1)
        self.font_size = '16sp'

# --- БАЗА ДАННЫХ ---
DATA = {
    "Samsung": {
        "Смартфон": {
            "Galaxy S": {
                "Galaxy S26 Ultra": {"storage": ["256 GB", "512 GB", "1 TB"], "colors": ["Titanium Black", "Titanium Gray"], "price": 5500},
            },
            "Galaxy A": {
                "Galaxy A57 5G": {"storage": ["128 GB", "256 GB"], "colors": ["Navy", "Lilac"], "price": 1500},
            }
        }
    },
    "Apple": {
        "Смартфон": {
            "iPhone": {
                "iPhone 17 Pro": {"storage": ["256 GB", "512 GB"], "colors": ["Silver", "Graphite"], "price": 4800},
            }
        }
    },
    "Xiaomi (Redmi)": {
        "Смартфон": {
            "Redmi Note": {
                "Redmi Note 15 Pro+ 5G": {"storage": ["256 GB", "512 GB"], "colors": ["Black", "Purple"], "price": 1400},
            }
        }
    },
    "Honor": {
        "Смартфон": {
            "Magic": {
                "Honor Magic8 Pro": {"storage": ["256 GB", "512 GB"], "colors": ["Green", "Black"], "price": 3800},
            }
        }
    },
    "Huawei": {
        "Смартфон": {
            "Mate": {
                "Huawei Mate 90 Pro": {"storage": ["512 GB", "1 TB"], "colors": ["Black", "Gold"], "price": 5500},
            }
        }
    }
}

class GadgetSelector(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=dp(40), spacing=dp(15), **kwargs)
        
        # Заголовок
        header = Label(
            text="[b]Выбор гаджета[/b]", 
            font_size='28sp', 
            markup=True,
            size_hint_y=None, 
            height=dp(60),
            color=(0.9, 0.9, 0.9, 1)
        )
        self.add_widget(header)
        
        # Настройки для списков
        spinner_kwargs = {
            'size_hint_y': None, 
            'height': dp(55), 
            'background_color': (0.2, 0.25, 0.35, 1),
            'font_size': '18sp',
            'options_class': DarkSpinnerOption
        }

        self.brand_spinner = Spinner(text='1. Бренд', values=list(DATA.keys()), **spinner_kwargs)
        self.brand_spinner.bind(text=self.on_brand)
        self.add_widget(self.brand_spinner)
        
        self.type_spinner = Spinner(text='2. Тип гаджета', **spinner_kwargs)
        self.type_spinner.bind(text=self.on_type)
        self.add_widget(self.type_spinner)
        
        self.lineup_spinner = Spinner(text='3. Линейка', **spinner_kwargs)
        self.lineup_spinner.bind(text=self.on_lineup)
        self.add_widget(self.lineup_spinner)
        
        self.model_spinner = Spinner(text='4. Модель', **spinner_kwargs)
        self.model_spinner.bind(text=self.on_model)
        self.add_widget(self.model_spinner)
        
        self.storage_spinner = Spinner(text='5. Память', **spinner_kwargs)
        self.add_widget(self.storage_spinner)
        
        self.color_spinner = Spinner(text='6. Цвет', **spinner_kwargs)
        self.add_widget(self.color_spinner)
        
        # Кнопка
        btn = Button(
            text='Показать цену', 
            size_hint_y=None, 
            height=dp(60),
            background_normal='', 
            background_color=(0.1, 0.6, 0.3, 1),
            font_size='20sp',
            bold=True
        )
        btn.bind(on_release=self.show_price)
        self.add_widget(btn)
        
        # Поле результата
        self.result = Label(
            text='', 
            font_size='20sp', 
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(120)
        )
        self.result.bind(size=self.result.setter('text_size'))
        self.add_widget(self.result)

    def reset_from_brand(self):
        self.type_spinner.text = '2. Тип гаджета'
        self.type_spinner.values = []
        self.lineup_spinner.text = '3. Линейка'
        self.lineup_spinner.values = []
        self.model_spinner.text = '4. Модель'
        self.model_spinner.values = []
        self.storage_spinner.text = '5. Память'
        self.storage_spinner.values = []
        self.color_spinner.text = '6. Цвет'
        self.color_spinner.values = []
        self.result.text = ''

    def on_brand(self, spinner, text):
        self.reset_from_brand()
        if text in DATA:
            self.type_spinner.values = list(DATA[text].keys())

    def on_type(self, spinner, text):
        brand = self.brand_spinner.text
        if brand in DATA and text in DATA[brand]:
            self.lineup_spinner.values = list(DATA[brand][text].keys())

    def on_lineup(self, spinner, text):
        brand = self.brand_spinner.text
        dtype = self.type_spinner.text
        if brand in DATA and dtype in DATA[brand] and text in DATA[brand][dtype]:
            self.model_spinner.values = list(DATA[brand][dtype][text].keys())

    def on_model(self, spinner, text):
        brand = self.brand_spinner.text
        dtype = self.type_spinner.text
        lineup = self.lineup_spinner.text
        if all([brand in DATA, dtype in DATA.get(brand, {}), lineup in DATA.get(brand, {}).get(dtype, {}), text in DATA[brand][dtype][lineup]]):
            info = DATA[brand][dtype][lineup][text]
            self.storage_spinner.values = info['storage']
            self.color_spinner.values = info['colors']

    def show_price(self):
        brand = self.brand_spinner.text
        model = self.model_spinner.text
        storage = self.storage_spinner.text
        color = self.color_spinner.text
        
        if '1.' in brand or '4.' in model or '5.' in storage or '6.' in color:
            self.result.text = '[b]Ошибка:[/b] Выбери всё до конца!'
            self.result.color = (1, 0.3, 0.3, 1)
            return
            
        try:
            dtype = self.type_spinner.text
            lineup = self.lineup_spinner.text
            price = DATA[brand][dtype][lineup][model]['price']
            
            self.result.text = f"[b]{brand} {model}[/b]\n{storage} | {color}\n\n[color=00ff00][b]Цена: {price} BYN[/b][/color]"
            self.result.markup = True
            self.result.color = (1, 1, 1, 1)
        except Exception:
            self.result.text = 'Ошибка при выборе'
            self.result.color = (1, 0.3, 0.3, 1)

class GadgetApp(App):
    def build(self):
        return GadgetSelector()

if __name__ == '__main__':
    GadgetApp().run()
