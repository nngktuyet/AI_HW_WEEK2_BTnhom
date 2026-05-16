import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

load = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'load')
dirty = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'dirty')
thickness = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'thickness')

wash_time = ctrl.Consequent(np.arange(15, 91, 1), 'wash_time')
water = ctrl.Consequent(np.arange(1, 10.1, 0.1), 'water')

load['small'] = fuzz.trimf(load.universe, [0, 0, 3.5])
load['medium'] = fuzz.trimf(load.universe, [2, 5, 8])
load['large'] = fuzz.trimf(load.universe, [6.5, 10, 10])

dirty['low'] = fuzz.trimf(dirty.universe, [0, 0, 3])
dirty['medium'] = fuzz.trimf(dirty.universe, [2, 5, 8])
dirty['high'] = fuzz.trimf(dirty.universe, [6.5, 10, 10])

thickness['thin'] = fuzz.trimf(thickness.universe, [0, 0, 3])
thickness['medium'] = fuzz.trimf(thickness.universe, [2, 5, 8])
thickness['thick'] = fuzz.trimf(thickness.universe, [6, 10, 10])

wash_time['short'] = fuzz.trimf(wash_time.universe, [15, 15, 35])
wash_time['normal'] = fuzz.trimf(wash_time.universe, [30, 50, 70])
wash_time['long'] = fuzz.trimf(wash_time.universe, [60, 90, 90])

water['low'] = fuzz.trimf(water.universe, [1, 1, 4])
water['medium'] = fuzz.trimf(water.universe, [3, 5.5, 8])
water['high'] = fuzz.trimf(water.universe, [7, 10, 10])

rules = [
    ctrl.Rule(load['small'] & dirty['low'] & thickness['thin'],
              [wash_time['short'], water['low']]),

    ctrl.Rule(load['small'] & dirty['medium'],
              [wash_time['normal'], water['medium']]),

    ctrl.Rule(load['medium'] | dirty['medium'] | thickness['medium'],
              [wash_time['normal'], water['medium']]),

    ctrl.Rule(load['large'] | dirty['high'] | thickness['thick'],
              [wash_time['long'], water['high']]),

    ctrl.Rule(dirty['high'] & thickness['thick'],
              [wash_time['long'], water['high']]),

    ctrl.Rule(load['large'] & dirty['low'] & thickness['thin'],
              [wash_time['normal'], water['medium']])
]

washing_ctrl = ctrl.ControlSystem(rules)


fabric_settings = {
    'Silk': {'range': (0, 2), 'mode': 'Silk'},
    'Wool': {'range': (1, 4), 'mode': 'Wool'},
    'Cotton': {'range': (2, 6), 'mode': 'Normal'},
    'Sport': {'range': (1, 5), 'mode': 'Synthetic'},
    'Denim': {'range': (6, 10), 'mode': 'Heavy Duty'},
    'Bulky': {'range': (5, 10), 'mode': 'Bulky'},
}


def get_thickness_from_fabric(fabric_name):
    min_value, max_value = fabric_settings[fabric_name]['range']
    return (min_value + max_value) / 2

class WashingRemoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Máy giặt')
        self.root.geometry('430x760')
        self.root.minsize(390, 690)
        self.root.configure(bg='alice blue')

        self.fabric_var = tk.StringVar(value='Cotton')
        self.dirty_var = tk.DoubleVar(value=5)
        self.weight_var = tk.StringVar(value='3.5')
        self.status_var = tk.StringVar(value='Sẵn sàng')
        self.time_var = tk.StringVar(value='--')
        self.water_var = tk.StringVar(value='--')

        self.build_ui()

    def card(self, parent, pady=(0, 14)):
        frame = tk.Frame(parent, bg='white', bd=0, highlightthickness=1,
                         highlightbackground='light steel blue')
        frame.pack(fill='x', padx=18, pady=pady)
        return frame

    def label(self, parent, text, size=13, weight='normal', fg='midnight blue', bg='white'):
        return tk.Label(parent, text=text, font=('Arial', size, weight), fg=fg, bg=bg)

    def icon_circle(self, parent, text):
        wrap = tk.Frame(parent, bg='alice blue', width=48, height=48)
        wrap.grid_propagate(False)
        tk.Label(wrap, text=text, font=('Arial', 18), fg='royal blue', bg='alice blue').place(relx=0.5, rely=0.5, anchor='center')
        return wrap

    def build_ui(self):
        container = tk.Frame(self.root, bg='alice blue')
        container.pack(fill='both', expand=True)

        # Header
        header = tk.Frame(container, bg='alice blue')
        header.pack(fill='x', padx=18, pady=(14, 10))

        tk.Label(header, text='☰', font=('Arial', 24), bg='alice blue', fg='midnight blue').pack(side='left')
        title_box = tk.Frame(header, bg='alice blue')
        title_box.pack(side='left', expand=True)
        tk.Label(title_box, text='Máy giặt', font=('Arial', 24, 'bold'), bg='alice blue', fg='midnight blue').pack()
        tk.Label(title_box, text='● Online', font=('Arial', 13), bg='alice blue', fg='seagreen').pack()
        tk.Label(header, text='⚙', font=('Arial', 24), bg='alice blue', fg='midnight blue').pack(side='right')

        self.build_status_card(container)
        self.build_input_card(container)
        self.build_display_panel(container)
        self.build_start_button(container)

    def build_status_card(self, parent):
        frame = self.card(parent)
        frame.configure(height=165)
        frame.pack_propagate(False)

        left = tk.Frame(frame, bg='white')
        left.pack(side='left', fill='both', expand=True, padx=(16, 8), pady=16)

        washer = tk.Canvas(left, width=120, height=120, bg='white', highlightthickness=0)
        washer.pack(anchor='center')
        washer.create_rectangle(20, 8, 100, 118, outline='light gray', fill='white', width=2)
        washer.create_rectangle(30, 15, 58, 25, outline='gray', fill='white')
        washer.create_rectangle(64, 15, 94, 28, outline='gray', fill='black')
        washer.create_oval(34, 40, 92, 98, outline='gray20', fill='gray15', width=3)
        washer.create_oval(45, 51, 81, 87, outline='gray40', fill='gray25')

        right = tk.Frame(frame, bg='white')
        right.pack(side='left', fill='both', expand=True, padx=(6, 16), pady=22)
        self.label(right, 'Trạng thái', 12, fg='slate gray').pack(anchor='w')
        tk.Label(right, textvariable=self.status_var, font=('Arial', 24, 'bold'), fg='royal blue', bg='white').pack(anchor='w', pady=(6, 8))
        self.label(right, 'Máy giặt đang ở chế độ chờ', 12, fg='dim gray').pack(anchor='w')

    def build_input_card(self, parent):
        frame = self.card(parent)
        frame.configure(height=250)
        frame.pack_propagate(False)

        self.label(frame, 'NHẬP THÔNG SỐ', 13, 'bold').pack(anchor='w', padx=18, pady=(16, 8))

        form = tk.Frame(frame, bg='white')
        form.pack(fill='both', expand=True, padx=18, pady=(2, 16))
        form.columnconfigure(1, weight=1)

        self.add_fabric_row(form, 0)
        self.add_dirty_row(form, 1)
        self.add_weight_row(form, 2)

    def add_fabric_row(self, parent, row):
        self.icon_circle(parent, '👕').grid(row=row, column=0, padx=(0, 14), pady=8)
        self.label(parent, 'Loại vải', 14).grid(row=row, column=1, sticky='w', pady=8)

        combo = ttk.Combobox(parent, textvariable=self.fabric_var,
                             values=list(fabric_settings.keys()), state='readonly',
                             font=('Arial', 13), width=12)
        combo.grid(row=row, column=2, sticky='ew', pady=8)

    def add_dirty_row(self, parent, row):
        self.icon_circle(parent, '💧').grid(row=row, column=0, padx=(0, 14), pady=8)
        self.label(parent, 'Độ bẩn', 14).grid(row=row, column=1, sticky='w', pady=8)

        box = tk.Frame(parent, bg='white')
        box.grid(row=row, column=2, sticky='ew', pady=8)
        box.columnconfigure(0, weight=1)

        self.dirty_value_label = tk.Label(box, text='5 / 10', font=('Arial', 12, 'bold'), fg='royal blue', bg='white')
        self.dirty_value_label.pack(anchor='e')

        scale = tk.Scale(box, from_=0, to=10, resolution=0.1, orient='horizontal',
                         variable=self.dirty_var, showvalue=False, length=145,
                         bg='white', highlightthickness=0, troughcolor='light steel blue',
                         command=self.update_dirty_label)
        scale.pack(fill='x')

    def add_weight_row(self, parent, row):
        self.icon_circle(parent, 'KG').grid(row=row, column=0, padx=(0, 14), pady=8)
        self.label(parent, 'Số kg quần áo', 14).grid(row=row, column=1, sticky='w', pady=8)

        box = tk.Frame(parent, bg='ghost white', highlightthickness=1, highlightbackground='light gray')
        box.grid(row=row, column=2, sticky='ew', pady=8)
        box.columnconfigure(1, weight=1)

        tk.Button(box, text='−', font=('Arial', 18), fg='royal blue', bg='ghost white',
                  bd=0, command=lambda: self.change_weight(-0.5)).grid(row=0, column=0, padx=8)
        tk.Entry(box, textvariable=self.weight_var, width=5, justify='center',
                 font=('Arial', 16, 'bold'), fg='midnight blue', bg='white', bd=0).grid(row=0, column=1, pady=8)
        self.label(box, 'kg', 12, fg='dim gray', bg='ghost white').grid(row=0, column=2, padx=(0, 6))
        tk.Button(box, text='+', font=('Arial', 18), fg='royal blue', bg='ghost white',
                  bd=0, command=lambda: self.change_weight(0.5)).grid(row=0, column=3, padx=8)

    def build_display_panel(self, parent):
        frame = tk.Frame(parent, bg='midnight blue')
        frame.pack(fill='x', padx=18, pady=(0, 14))

        left = tk.Frame(frame, bg='midnight blue')
        left.pack(side='left', fill='both', expand=True, padx=18, pady=18)
        tk.Label(left, text='THỜI GIAN GIẶT', font=('Arial', 11, 'bold'), fg='dodger blue', bg='midnight blue').pack()
        tk.Label(left, textvariable=self.time_var, font=('Courier New', 32, 'bold'), fg='white', bg='midnight blue').pack(pady=(8, 0))
        tk.Label(left, text='phút', font=('Arial', 11), fg='light steel blue', bg='midnight blue').pack()

        divider = tk.Frame(frame, width=1, bg='light steel blue')
        divider.pack(side='left', fill='y', pady=22)

        right = tk.Frame(frame, bg='midnight blue')
        right.pack(side='left', fill='both', expand=True, padx=18, pady=18)
        tk.Label(right, text='LƯỢNG NƯỚC', font=('Arial', 11, 'bold'), fg='dodger blue', bg='midnight blue').pack()
        tk.Label(right, textvariable=self.water_var, font=('Courier New', 32, 'bold'), fg='white', bg='midnight blue').pack(pady=(8, 0))
        tk.Label(right, text='/ 10', font=('Arial', 11), fg='light steel blue', bg='midnight blue').pack()

    def build_start_button(self, parent):
        tk.Button(parent, text='▶  Bắt đầu giặt', font=('Arial', 17, 'bold'),
                  fg='white', bg='royal blue', activebackground='dodger blue',
                  activeforeground='white', bd=0, height=2,
                  command=self.calculate).pack(fill='x', padx=18, pady=(0, 16))

        tk.Button(parent, text='Reset', font=('Arial', 12),
                  fg='slate gray', bg='alice blue', bd=0,
                  command=self.reset).pack(pady=(0, 10))

    def update_dirty_label(self, value=None):
        self.dirty_value_label.config(text=f'{float(self.dirty_var.get()):.1f} / 10')

    def change_weight(self, amount):
        try:
            current = float(self.weight_var.get())
        except ValueError:
            current = 0
        new_value = min(10, max(0.5, current + amount))
        self.weight_var.set(f'{new_value:.1f}')

    def calculate(self):
        try:
            kg = float(self.weight_var.get())
        except ValueError:
            messagebox.showerror('Lỗi', 'Số kg phải là số hợp lệ. Ví dụ: 3.5')
            return

        if kg <= 0 or kg > 10:
            messagebox.showerror('Lỗi', 'Số kg phải nằm trong khoảng 0 - 10 kg.')
            return

        fabric = self.fabric_var.get()
        dirty_value = float(self.dirty_var.get())
        thick_value = get_thickness_from_fabric(fabric)

        try:
            washing_sim = ctrl.ControlSystemSimulation(washing_ctrl)
            washing_sim.input['load'] = kg
            washing_sim.input['dirty'] = dirty_value
            washing_sim.input['thickness'] = thick_value
            washing_sim.compute()

            final_time = washing_sim.output['wash_time']
            final_water = washing_sim.output['water']

            self.status_var.set('Đang thiết lập')
            self.time_var.set(f'{final_time:.0f}')
            self.water_var.set(f'{final_water:.1f}')

        except Exception as error:
            messagebox.showerror('Lỗi hệ thống', str(error))

    def reset(self):
        self.fabric_var.set('Cotton')
        self.dirty_var.set(5)
        self.weight_var.set('3.5')
        self.status_var.set('Sẵn sàng')
        self.time_var.set('--')
        self.water_var.set('--')
        self.update_dirty_label()


if __name__ == '__main__':
    root = tk.Tk()
    app = WashingRemoteApp(root)
    root.mainloop()
