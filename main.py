import numbers
from utils import safe_eval
import dearpygui.dearpygui as dpg

BUTTON_WIDTH: int = 40
BUTTON_HEIGHT: int = 40
ALIAS_VALUES: dict[str, str] = {
    "÷": "/",
    "×": "*",
}

OPS: list[str] = ["+", "-", "/", "*"]

expression = ""
has_dot = False

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()


with dpg.theme() as primarybtn_blue_theme:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding,
                            5, category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button,
                            (52, 103, 179), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,
                            (44, 89, 156), category=dpg.mvThemeCat_Core)


def btn_clicked(sender, app_data, user_data):
    global expression
    global has_dot

    val: str = dpg.get_value("input")
    val_or_alias: str = ALIAS_VALUES.get(user_data, user_data)

    if user_data == "AC":
        expression = ""
        dpg.set_value("input", "0")
        has_dot = False
        return
    elif user_data == "C":
        dpg.set_value("input", "0")
        return
    elif user_data == "DEL":
        length = len(val)
        if length > 0 and val != "0":
            if length == 1:
                dpg.set_value("input", "0")
            else:
                dpg.set_value("input", val[:-1])
        return
    elif user_data == "=":
        res, success = safe_eval(expression)
        if success:
            dpg.set_value("input", res)
        return
    elif user_data == "+/-":
        if isinstance(expression, numbers.Number) and val != "0":
            if expression.startswith('-'):
                expression = expression[1:]
            else:
                expression = "-" + expression
            dpg.set_value("input", expression)
        return
    elif user_data == "%":
        if isinstance(expression, numbers.Number):
            expression = str(float(expression) / 100)
            dpg.set_value("input", expression)
        return

    if val == "0" and user_data != ".":
        if val_or_alias in OPS:
            expression += "0" + val_or_alias
            dpg.set_value("input", "0" + user_data)
            return

        dpg.set_value("input", user_data)
        expression = val_or_alias
        return

    if val_or_alias in OPS:
        has_dot = False
        if len(expression) > 0 and expression[-1] in OPS:
            prev_expr = expression[:-1]
            expression = prev_expr + val_or_alias
            dpg.set_value("input", prev_expr + user_data)
            return

    if val_or_alias == ".":
        if has_dot:
            return
        has_dot = True
        expression += "."
        dpg.set_value("input", val + user_data)
        return

    dpg.set_value("input", val + user_data)
    expression = expression + val_or_alias


button_lists = [
    ["AC", "C", "DEL", "%"],
    ["7", "8", "9", "÷"],
    ["4", "5", "6", "×"],
    ["1", "2", "3", "-"],
    ["+/-", "0", ".", "+"],
]


with dpg.window() as main_window:

    dpg.add_text("0", tag="input")
    dpg.add_spacer(height=10)

    for buttons in button_lists:
        with dpg.group(horizontal=True):
            for button in buttons:
                dpg.add_button(label=button, width=BUTTON_WIDTH,
                               height=BUTTON_HEIGHT, callback=btn_clicked, user_data=button)

        dpg.add_spacer(height=2)

    equal = dpg.add_button(
        label="=", width=BUTTON_WIDTH * len(button_lists[0]) + 25, height=BUTTON_HEIGHT, callback=btn_clicked, user_data="=")
    dpg.bind_item_theme(equal, primarybtn_blue_theme)


if __name__ == "__main__":
    dpg.set_viewport_title("DPG Calculator")

    dpg.set_primary_window(main_window, True)
    dpg.set_viewport_resizable(False)
    dpg.set_viewport_width(200)
    dpg.set_viewport_height(350)

    dpg.show_viewport()

    dpg.start_dearpygui()
    dpg.destroy_context()
