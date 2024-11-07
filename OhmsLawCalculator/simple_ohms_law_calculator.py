from tabulate import tabulate
import sys
import time

VOLTAGE = "Voltage (V)"
CURRENT = "Current (I)"
RESISTANCE = "Resistance (R)"
POWER = "Power (P)"

LETTERS = {
    VOLTAGE: "V",
    CURRENT: "I",
    RESISTANCE: "R",
    POWER: "P",
}

UNITS = {
    VOLTAGE: {"unit": "Volts", "shorthand": "V"},
    CURRENT: {"unit": "Amps", "shorthand": "A"},
    RESISTANCE: {"unit": "Ohms", "shorthand": "Ω"},
    POWER: {"unit": "Watts", "shorthand": "W"},
}

OPTIONS = {
    '1': VOLTAGE,
    '2': CURRENT,
    '3': RESISTANCE,
    '4': POWER,
}

FORMULAS = {
    VOLTAGE: {
        (CURRENT, RESISTANCE): ("{0} * {1}", "{0} * {1}"),
        (POWER, CURRENT): ("{0} / {1}", "{0} / {1}"),
        (POWER, RESISTANCE): ("√({0} * {1})", "({0} * {1}) ** 0.5")
    },
    CURRENT: {
        (VOLTAGE, RESISTANCE): ("{0} / {1}", "{0} / {1}"),
        (POWER, VOLTAGE): ("{0} / {1}", "{0} / {1}"),
        (POWER, RESISTANCE): ("√({0} / {1})", "({0} / {1}) ** 0.5")
    },
    RESISTANCE: {
        (VOLTAGE, CURRENT): ("{0} / {1}", "{0} / {1}"),
        (POWER, CURRENT): ("{0} / {1}²", "{0} / ({1} ** 2)"),
        (POWER, VOLTAGE): ("{1}² / {0}", "({1} ** 2) / {0}")
    },
    POWER: {
        (VOLTAGE, CURRENT): ("{0} * {1}", "{0} * {1}"),
        (CURRENT, RESISTANCE): ("{0}² * {1}", "({0} ** 2) * {1}"),
        (VOLTAGE, RESISTANCE): ("{0}² / {1}", "({0} ** 2) / {1}")
    },
}

class QuitException(Exception):
    pass

def check_quit(user_input):
    if user_input.upper() == 'Q':
        print("\nThank you for using the Ohm's Law Calculator!")
        time.sleep(2)
        raise QuitException

def get_user_choice(options):
    while True:
        print()
        choice = input("Choose a number and press 'Enter': ")
        check_quit(choice)
        if choice in options:
            return options[choice]
        else:
            print("Invalid input. Please enter a valid number.")

def get_known_variables(known_variables):
    variable_values = {}
    while len(known_variables) > 1:
        print()
        print("What known variable do you have?")
        print("Please choose from the options below:")
        print()
        options = {str(i + 1): var for i, var in enumerate(known_variables)}
        for i, var in options.items():
            print(f"{i}. {var}")
        var = get_user_choice(options)
        print()
        known_variables.remove(var)
        while True:
            value = input(f"{var} in {UNITS[var]['unit']}: ")
            if value == '':
                print("Invalid input. Input should not be an empty string.")
            elif value.count('.') > 1:
                print("Invalid input. Input should not have more than one decimal.")
            else:
                try:
                    check_quit(value)
                    variable_values[var] = float(value)
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
    return variable_values

def format_number(n, unit):
    n = float(n)  # ensure n is a float
    if n.is_integer():
        n = int(n)
        if n == 1:
            unit = unit.rstrip('s')  # Remove 's' at the end if present
    else:
        n = round(n, 3)
    return n, unit

def main():
    print("Welcome to the Ohm's Law Calculator!")
    print("Press 'Q' then 'Enter' to quit.")
    print()
    print("Please select what you would like to calculate:")
    print()
    for i, option in OPTIONS.items():
        print(f"{i}. {option}")

    calculated_variable = get_user_choice(OPTIONS)
    print()
    print(f"You have selected to calculate {calculated_variable}.")
    known_variables = [var for var in UNITS.keys() if var != calculated_variable]
    variable_values = get_known_variables(known_variables)

    for variables, formulas in FORMULAS[calculated_variable].items():
        if all(variable in variable_values for variable in variables):
            display_formula, calculation_formula = formulas

            formula_values = [variable_values[variable] for variable in variables]
            formula_str = calculation_formula.format(*formula_values)
            calculated_value, calculated_unit = format_number(eval(formula_str), UNITS[calculated_variable]['unit'])
            result = [[variable, f"{format_number(value, UNITS[variable]['unit'])[0]} {format_number(value, UNITS[variable]['unit'])[1]}"] for variable, value in variable_values.items()]
            result.append([calculated_variable, f"{calculated_value} {calculated_unit}"])
            print()
            print(tabulate(result, headers=["Variable", "Value"], tablefmt="fancy_grid"))
            print()
            formula_letter_str = display_formula.format(*[LETTERS[var] for var in variables])
            formula_values_units_str = [f"{format_number(value, UNITS[var]['unit'])[0]} {UNITS[var]['shorthand']}" for var, value in zip(variables, formula_values)]
            formula_values_str = display_formula.format(*formula_values_units_str)
            print(f"{LETTERS[calculated_variable]} = {formula_letter_str}")
            print()
            print(f"{calculated_value} {UNITS[calculated_variable]['shorthand']} = {formula_values_str}")
            break

if __name__ == "__main__":
    while True:
        try:
            main()
            print()
            print(
                "Press 'Enter' to restart or 'Q' then 'Enter' to quit.")
            user_input = input()
            check_quit(user_input)
        except QuitException:
            break
