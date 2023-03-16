# Författare - Andreas Garcia
# Datum - 20/01/2022
# Senast reviderad - 08/04/2022

from tkinter import *  # GUI
from PIL import ImageTk  # Bildhantering i GUI
import datetime  # Felhantering för datum och tid


class Car:
    """
    Attributes:
    reg_nmr: The registration number of the car
    price_class: The size of the car
    owner: The name of the car owner
    fund_surplus: Money left over from earlier transactions (credited)
    """

    def __init__(self, reg_nmr, price_class, owner, fund_surplus):
        """
        Creates a new car
        :param reg_nmr: The registration number of the car
        :param price_class: The size of the car
        :param owner: The name of the car owner
        :param fund_surplus: Money left over from earlier transactions (credited)
        """
        self.reg_nmr = reg_nmr
        self.price_class = price_class
        self.owner = owner
        self.fund_surplus = float(fund_surplus)  # Pengar tillgodo


class Passage:
    """
    Attributes:
    date: The date of the passage
    reg_nmr: The registration number of the car
    in_time: The start-time of the passage
    out_time: The end-time of the passage
    payment_status: The payment status of the passage (paid or not)
    """

    def __init__(self, date, reg_nmr, in_time, out_time, payment_status):
        """
        Creates a new passage
        :param date: The date of the passage
        :param reg_nmr: The registration number of the car
        :param in_time: The start-time of the passage
        :param out_time: The end-time of the passage
        :param payment_status: The payment status of the passage (paid or not)
        """
        self.date = date
        self.reg_nmr = reg_nmr
        self.in_time = in_time
        self.out_time = out_time
        self.payment_status = payment_status  # Betalningsstatus (Ja/Nej)


def read_from_file(file_input, window, readfile_window_button, add_passage_button,
                   add_car_button, calc_price_button, show_history_button,
                   pay_debt_button, file_prompt_label):
    """
    Used to get data from the passage log-file (file_input) and append the Passage
    objects to a list
    :param file_input: The name of the log-file
    :param window: The graphical window used for executing this function
    :param readfile_window_button: The button in the window used for executing file reading
    :param add_passage_button: The button for opening the graphical window used for adding passages
    :param add_car_button: The button for opening the graphical window used for adding cars
    :param calc_price_button: The button for opening the graphical window used for calculating debt
    :param show_history_button: The button for opening the graphical window used for showing history
    :param pay_debt_button: The button for opening the graphical window used for paying debt
    :param file_prompt_label: The graphical prompt at the beginning of the program telling the user to
    input the passage log-file
    :return: (nothing)
    """
    if not file_found(window, file_input):  # Felhantering filinläsning
        return None

    opened_file = file_found(window, file_input)

    global file  # Global för åtkomst genom GUI:s olika fönster
    file = file_input

    lines_of_file, list_of_passages = read_and_close_file(opened_file)  # Inläsning och skapandet av passagelista

    rowcount = 0  # För utskrift av antalet registreringar som lästs in lyckat
    file_errors = 0  # För att räkna antalet fel i filen efter inläsning, under bearbetningen
    rowcount, file_errors = correct_file_format(window, rowcount,
                                                file_errors, lines_of_file, list_of_passages)  # Felhantering filformat

    Label(window, text="Inläsning lyckades! " + str(rowcount-file_errors) + " registreringar lästes in")\
        .grid(column=0, row=4, pady=20, padx=20)

    change_button_state(readfile_window_button)  # Avaktivering av inläsningsknapp i inläsningsfönstret &
    # aktivering av resterande GUI-knappar
    change_button_state(add_passage_button)
    change_button_state(add_car_button)
    change_button_state(calc_price_button)
    change_button_state(show_history_button)
    change_button_state(pay_debt_button)
    file_prompt_label.destroy()  # Borttagning av inläsningsprompt som visas innan loggfil lästs in


file = ""  # Tillgängliggör filen


def open_file(file_input):
    """
    Used to open a given file with utf-8 encoding
    :param file_input: The file-name of the given file
    :return: The opened file
    """
    opened_file = open(file_input, "r", encoding="utf-8")
    return opened_file


def read_and_close_file(opened_file):
    """
    Used to read and close a given file, whilst creating an empty list for Class objects
    :param opened_file: The opened file
    :return: The lines that were read from the file and the empty list
    """
    lines_of_file = opened_file.readlines()
    list_of_objects = []
    opened_file.close()
    return lines_of_file, list_of_objects


def split_and_append_passage_file(list_of_passages, row):
    """
    Used to split up the lines of the passage-file into sections and append the Passage-objects to passage-list
    :param list_of_passages: The list of passages
    :param row: The lines in the file separated
    :return: The sections and list of passages
    """
    row = row.replace("\n", "")
    section = row.split(" ")
    list_of_passages.append(Passage(section[0], section[1], section[2], section[3], section[4]))
    return section, list_of_passages


def split_and_append_car_file(list_of_cars, row):
    """
    Used to split up the lines of the car-file into sections and append the Car-objects to car-list
    :param list_of_cars: The list of cars
    :param row: The lines in the file separated
    :return: The list of registered cars
    """
    row = row.replace("\n", "")
    section = row.split(" ")
    list_of_cars.append(Car(section[0], section[1], section[2], section[3]))
    return list_of_cars


def update():
    """
    Used to update the lists of Car objects and Passage objects between functions
    :return: The lists of registered cars and passages
    """
    opened_file_passages = open_file(file)
    readfile_passages, list_of_passages = read_and_close_file(opened_file_passages)
    for row in readfile_passages:
        section, list_of_passages = split_and_append_passage_file(list_of_passages, row)

    opened_file_cars = open_file("kundinfo.txt")
    readfile_cars, list_of_cars = read_and_close_file(opened_file_cars)
    for row in readfile_cars:
        list_of_cars = split_and_append_car_file(list_of_cars, row)

    return list_of_cars, list_of_passages


def add_passage(date_input, reg_input, start_input, end_input, window, add_passage_window_button):
    """
    Used to add a new parking passage
    :param date_input: The date input by user
    :param reg_input: The registration number of the car, input by user
    :param start_input: The start-time of the passage, input by user
    :param end_input: The end-time of the passage, input by user
    :param window: The graphical window used for adding passages
    :param add_passage_window_button: The button in the window used for executing this function
    :return: (nothing)
    """

    if not valid_date(window, date_input):  # Felhantering datum
        return None

    if not valid_reg(reg_input):  # Felhantering regnmr
        reg_err = Label(window, text="Registreringsnumret är inte giltigt, försök igen (AAAXXX)!", padx=30)
        reg_err.grid(column=1, row=3)
        reg_err.after(3000, reg_err.destroy)
        return None

    if not valid_start_time(window, start_input):  # Felhantering tid
        return None
    date_time_start, t_format = valid_start_time(window, start_input)

    if not valid_end_time(window, t_format, end_input, date_time_start):
        return None

    Passage(date_input, reg_input, start_input, end_input, "Nej")  # "Nej" = ickebetald
    Label(window, text="Passage tillagd!", pady=30).grid(column=0, row=9)
    change_button_state(add_passage_window_button)

    writefile = open(file, "a", encoding="utf-8")  # Skriver över nya passager till loggfilen
    writefile.write(date_input + " " + reg_input + " " + start_input + " " + end_input + " Nej" + "\n")
    writefile.close()


def add_car(reg, size, name, window, add_car_window_button):
    """
    Used to register a new car to the parking service
    :param reg: The registration number of the car, input by user
    :param size: The size of the car, input by user
    :param name: The name of the car owner, input by user
    :param window: The graphical window used for adding new cars
    :param add_car_window_button: The button in the window used for executing this function
    :return: (nothing)
    """
    list_of_cars, list_of_passages = update()

    if not valid_reg(reg):
        reg_err = Label(window, text="Registreringsnumret är inte giltigt, försök igen (AAAXXX)!", padx=30)
        reg_err.grid(column=1, row=1)
        reg_err.after(3000, reg_err.destroy)
        return None

    for cars in list_of_cars:
        if reg == cars.reg_nmr:
            reg_already = Label(window, text="Registreringsnumret är redan registrerat!", padx=30)
            reg_already.grid(column=1, row=1)
            reg_already.after(3000, reg_already.destroy)
            return None

    if not valid_size(window, size):
        return None

    if not valid_name(window, name):
        return None
    name = valid_name(window, name)

    change_button_state(add_car_window_button)
    Car(reg, size, name, 0)  # 0 = inga pengar tillgodo
    Label(window, text="Bil tillagd!", pady=30).grid(column=0, row=7)

    writefile = open("kundinfo.txt", "a", encoding="utf-8")  # Skriver över nya bilar till kundinfo-filen
    writefile.write(reg + " " + size + " " + name + " " + "0.0" + "\n")
    writefile.close()


def calc_price(reg, window, calc_price_window_button):
    """
    Used to calculate the debt of a car based on earlier parking
    :param reg: The registration number of the car, input by user
    :param window: The graphical window used for calculating the debt
    :param calc_price_window_button: The button in the window used for executing this function
    :return: The amount of debt to be paid and the fund surplus of the car (owner)
    """
    list_of_cars, list_of_passages = update()

    if not valid_reg(reg):
        reg_err = Label(window, text="Registreringsnumret är inte giltigt, försök igen (AAAXXX)!")
        reg_err.grid(column=0, row=3, pady=30, padx=30)
        reg_err.after(3000, reg_err.destroy)
        return None

    pph = 0  # Pris per timme i kr
    funds = 0.0
    reg_found = False
    for cars in list_of_cars:
        if reg == cars.reg_nmr:  # Identifierar prisklass på bil beroende på storlek, samt överskottspengar
            reg_found = True
            if cars.price_class == "Liten":
                pph = 20
            elif cars.price_class == "Mellan":
                pph = 25
            elif cars.price_class == "Stor":
                pph = 30
            funds = cars.fund_surplus
            break

    if not reg_found:
        reg_not_found = Label(window, text="Registreringsnumret finns inte registrerat! Försök igen.")
        reg_not_found.grid(column=0, row=3, padx=30, pady=30)
        reg_not_found.after(3000, reg_not_found.destroy)
        return None

    amount = 0.0
    for passages in list_of_passages:
        if reg == passages.reg_nmr and passages.payment_status == "Nej":  # Ackummulering av obetalda parkeringar
            start = passages.in_time
            end = passages.out_time
            total_min = time_processing(start, end)  # Parkeringstid beräknas i minuter

            price = (pph/60) * total_min
            amount += price  # Skuld

    change_button_state(calc_price_window_button)
    Label(window, text="Din totala skuld: " + str(amount) + " kr").grid(column=0, row=3, pady=15)

    return amount, funds  # Används vid betalning av skuld


def show_parking(reg, window, show_history_window_button):
    """
    Used to display earlier parking of a car
    :param reg: The registration number of the car, input by user
    :param window: The graphical window used for showing parking history
    :param show_history_window_button: The button in the window used for executing this function
    :return: (nothing)
    """
    list_of_cars, list_of_passages = update()

    if not valid_reg(reg):
        reg_err = Label(window, text="Registreringsnumret är inte giltigt, försök igen (AAAXXX)!")
        reg_err.grid(column=0, row=3, pady=30, padx=30)
        reg_err.after(3000, reg_err.destroy)
        return None

    reg_found = False
    i = 0  # För printning av passage på ny rad efter varje iterering
    for passages in list_of_passages:  # Utskrift av historik
        if reg == passages.reg_nmr:
            Label(window, text=passages.date + " " + passages.reg_nmr + " " +
                  passages.in_time + " " + passages.out_time).grid(column=0, row=4 + i, pady=5)
            reg_found = True
            i += 1

    if not reg_found:
        reg_no_history = Label(window, text="Registreringsnumret har ingen historik! Försök igen.")
        reg_no_history.grid(column=0, row=3, pady=30, padx=30)
        reg_no_history.after(3000, reg_no_history.destroy)
        return None
    else:
        Label(window, text="|   DATUM   |   REG   |   IN   |  UT  |").grid(column=0, row=3, pady=5)

    change_button_state(show_history_window_button)


def pay_step(payment, window, pay_window_button, amount, funds, reg):
    """
    Used to pay the parking debt (function 2/2)
    :param payment: The chosen amount to pay towards the debt, input by user
    :param window: The graphical window used for paying the debt
    :param pay_window_button: The button in the window used for executing this function
    :param amount: The price of the debt
    :param funds: The fund surplus of the car (owner)
    :param reg: The registration number of the car, input by user
    :return: (nothing)
    """
    list_of_cars, list_of_passages = update()

    if not valid_payment(window, payment, amount, funds):  # Felhantering av vald betalsumma
        return None
    payment = valid_payment(window, payment, amount, funds)

    write_cars = open("kundinfo.txt", "w", encoding="utf-8")

    for cars in list_of_cars:
        if reg == cars.reg_nmr:
            cars.fund_surplus = payment + funds - amount  # Lägger till eventuellt pengaöverskott till kundinfo
        write_cars.write(cars.reg_nmr + " " + cars.price_class + " " + cars.owner +
                         " " + str(cars.fund_surplus))
        write_cars.write("\n")
    write_cars.close()

    writefile = open(file, "w", encoding="utf-8")

    for passages in list_of_passages:
        if reg == passages.reg_nmr:
            passages.payment_status = "Ja"  # Skriver om parkeringarna som betalda till loggfilen
        writefile.write(passages.date + " " + passages.reg_nmr + " " + passages.in_time + " "
                        + passages.out_time + " " + passages.payment_status)
        writefile.write("\n")
    writefile.close()

    Label(window, text="Tack för din betalning!").grid(column=0, row=9, pady=15)
    change_button_state(pay_window_button)


def pay_parking(reg, window, calc_window_button):
    """
    Used to pay the parking debt (function 1/2), uses calc_price function
    :param reg: The registration number of the car, input by user
    :param window: The graphical window used for paying the debt
    :param calc_window_button: The button in the window used for executing the calc_price function
    :return: (nothing)
    """
    try:
        amount, funds = calc_price(reg, window, calc_window_button)  # Använder beräkningsfunktionen
    except TypeError:  # Ifall beräkningsfunktionen får fel och returnerar None uppkommer denna exception
        return None

    Label(window, text="Du har " + str(funds) + " kr tillgodo").grid(column=0, row=4, pady=15)
    if amount-funds < 0:
        Label(window, text="Total kostnad: " + "0.0 kr").grid(column=0, row=5, pady=15)
    else:
        Label(window, text="Total kostnad: " + str((amount-funds)) + " kr").grid(column=0, row=5, pady=15)

    pay_prompt = Label(window, text="Hur mycket vill du betala (kr)?")
    pay_prompt.grid(column=0, row=6, pady=15)
    amount_input = Entry(window, width=10)
    amount_input.grid(column=0, row=7, pady=15)
    pay_button = Button(window, text="Betala", command=lambda: pay_step(amount_input.get(), window,
                                                                        pay_button, amount, funds, reg))
    pay_button.grid(column=0, row=8, pady=30)


def file_found(window, file_input):
    """
    Used to confirm if file exists (else error-handling)
    :param window: The graphical window used for reading the file
    :param file_input: The file name, input by user
    :return: The opened file, or None
    """
    try:
        opened_file = open_file(file_input)

    except FileNotFoundError:
        file_err = Label(window, text="Filen existerar inte, vänligen kontrollera namnet!")
        file_err.grid(column=0, row=4, pady=20)
        file_err.after(1500, file_err.destroy)
        return None

    return opened_file


def correct_file_format(window, rowcount, file_errors, lines_of_file, list_of_passages):
    """
    Used to confirm if file is on the correct format (else error-handling)
    :param window: The graphical window used for reading the file
    :param rowcount: The amount of rows that have been processed
    :param file_errors: The amount of un-processable lines in the file
    :param lines_of_file: The lines of the file
    :param list_of_passages: The list of parking passages
    :return: The rowcount and the amount of file errors, or None
    """
    for row in lines_of_file:  # Bearbetning av inläsning och append till passagelistan
        try:
            section, list_of_passages = split_and_append_passage_file(list_of_passages, row)
            if len(section[0]) != 10 or len(section[1]) != 6 or len(section[2]) != 5 or \
                    len(section[3]) != 5 or len(section[4]) != 3 and len(section[4]) != 2:
                file_error(window, rowcount)  # Senaste raden med fel kommer visas
                file_errors += 1
            rowcount += 1
        except IndexError:  # IndexError uppkommer t.ex. om en hel sektion saknas
            file_error(window, rowcount)  # Senaste raden med fel kommer visas
            rowcount += 1
            file_errors += 1

    return rowcount, file_errors


def valid_date(window, date_input):
    """
    Used to confirm if the input date is valid (else error-handling)
    :param window: The graphical window used for adding passages
    :param date_input: The date, input by user
    :return: True or None
    """
    try:
        day, month, year = date_input.split("/")
        datetime.datetime(int(year), int(month), int(day))  # Datetime-modulen för felhantering av datum och tid

    except ValueError:
        date_err = Label(window, text="Ogiltigt datum, försök igen!", padx=30)
        date_err.grid(column=1, row=1)
        date_err.after(3000, date_err.destroy)
        return None

    return True


def valid_reg(reg_input):
    """
    Used to confirm if the input registration number of a car is valid
    :param reg_input: The registration number, input by user
    :return: True or None
    """
    if len(reg_input) != 6 or not reg_input[3:6].isnumeric() \
            or not reg_input[0:3].isalpha() or not reg_input[0:3].isupper():
        return None

    return True


def valid_start_time(window, start_input):
    """
    Used to confirm if input start time for parking is valid (else error-handling)
    :param window: The graphical window used for adding passages
    :param start_input: The start time, input by user
    :return: The start time and the correct time format
    """
    t_format = "%H:%M"  # Accepterat tidformat
    try:
        date_time_start = datetime.datetime.strptime(start_input, t_format)
        if len(start_input) != 5:
            t_format_err = Label(window, text="Starttiden är på fel format, försök igen (TT:MM)", padx=30)
            t_format_err.grid(column=1, row=5)
            t_format_err.after(3000, t_format_err.destroy)
            return None
    except ValueError:
        start_err = Label(window, text="Starttiden är ogiltig, skriv in tiden på nytt (TT:MM)!", padx=30)
        start_err.grid(column=1, row=5)
        start_err.after(3000, start_err.destroy)
        return None

    return date_time_start, t_format


def valid_end_time(window, t_format, end_input, date_time_start):
    """
    Used to confirm if input end time for parking is valid (else error-handling)
    :param window: The graphical window used for adding passages
    :param end_input: The end time, input by user
    :param t_format: The correct time format
    :param date_time_start: The start time, processed and correct
    :return: True or None
    """
    try:
        date_time_end = datetime.datetime.strptime(end_input, t_format)
        if len(end_input) != 5:
            t_format_err = Label(window, text="Sluttiden är på fel format, försök igen (TT/MM)", padx=30)
            t_format_err.grid(column=1, row=7)
            t_format_err.after(3000, t_format_err.destroy)
            return None
    except ValueError:
        end_time_error(window)
        return None

    if (date_time_end - date_time_start).total_seconds() < 0:
        end_time_error(window)
        return None

    return True


def valid_size(window, size):
    """
    Used to confirm if the input size of a car is valid (else error handling)
    :param window: The graphical window used for adding cars
    :param size: The size of the car, input by user
    :return: True or None
    """
    if size != "Liten" and size != "Mellan" and size != "Stor":
        size_err = Label(window, text="Ogiltig bilstorlek, försök igen (Stor/Mellan/Liten)!", padx=30)
        size_err.grid(column=1, row=3)
        size_err.after(3000, size_err.destroy)
        return None

    return True


def valid_name(window, name):
    """
    Used to confirm if the input size of a car is valid (else error handling)
    :param window: The graphical window used for adding cars
    :param name: The name of the car owner, input by user
    :return: The name of the car owner, or None
    """
    name.strip()
    if not name.isalpha():
        name_err = Label(window, text="Namnet får endast innehålla bokstäver!", padx=30)
        name_err.grid(column=1, row=5)
        name_err.after(3000, name_err.destroy)
        return None

    return name


def valid_payment(window, payment, amount, funds):
    """
    Used confirm if input payment is valid (else error-handling)
    :param window: The graphical window used for paying the debt
    :param payment: The chosen amount to pay towards the debt, input by user
    :param amount: The amount of the debt
    :param funds: The fund surplus of the car (owner)
    :return: The payment, or None
    """
    if payment:
        if payment[0] != "-":
            try:
                payment = float(payment)
            except ValueError:
                pay_error(window)
                return None
        else:
            pay_error(window)
            return None
    else:
        pay_error(window)
        return None

    if payment < amount-funds:
        pay_not_enough = Label(window, text="Beloppet är för litet, försök igen!")
        pay_not_enough.grid(column=1, row=7, padx=30)
        pay_not_enough.after(3000, pay_not_enough.destroy)
        return None

    return payment


def time_processing(start, end):
    """
    Used to process time from the input time stamps to total minutes
    :param start: The processed and correct start time of a passage
    :param end: The processed and correct end time of a passage
    :return: The total parking time in minutes
    """
    if start[0] == "0":  # Bearbetning från sträng till heltal minuter
        start_hour = start[1]
    else:
        start_hour = start[0:2]

    if start[3] == "0":
        start_minute = start[4]
    else:
        start_minute = start[3:5]

    if end[0] == "0":
        end_hour = end[1]
    else:
        end_hour = end[0:2]

    if end[3] == "0":
        end_minute = end[4]
    else:
        end_minute = end[3:5]

    if 0 < int(start_minute) < 30:  # Avrundning uppåt till närmsta halvtimme
        start_minute = "30"
    elif 30 < int(start_minute) < 60:
        start_minute = "0"
        start_hour = int(start_hour) + 1

    if 0 < int(end_minute) < 30:
        end_minute = "30"
    elif 30 < int(end_minute) < 60:
        end_minute = "0"
        end_hour = int(end_hour) + 1

    hour_diff = (int(end_hour) - int(start_hour)) * 60
    min_diff = int(end_minute) - int(start_minute)
    total_min = hour_diff + min_diff

    return total_min


def pay_error(window):
    """
    Used for error handling of the payment input (as function due to repeated use)
    :param window: The graphical window used for paying the debt
    :return: (nothing)
    """
    pay_err = Label(window, text="Betalningen misslyckades, skriv in beloppet igen!")
    pay_err.grid(column=1, row=7, padx=30)
    pay_err.after(3000, pay_err.destroy)


def file_error(window, row):
    """
    Used for error handling in the log-file processing (as function due to repeated use)
    :param window: The graphical window used for file reading
    :param row: The row in the file on which the error occurs
    :return: (nothing)
    """
    file_err = Label(window, text="Filen har minst ett fel, "
                                  "det senaste på rad " + str(row+1) + ", åtgärda!", padx=30)
    file_err.grid(column=1, row=1)
    file_err.after(4000, file_err.destroy)


def end_time_error(window):
    """
    Used for error handling on end-time input for passages (as function due to repeated use)
    :param window: The graphical window used for adding passages
    :return: (nothing)
    """
    end_err = Label(window, text="Sluttiden är ogiltig, skriv in tiden på nytt!", padx=30)
    end_err.grid(column=1, row=7)
    end_err.after(3000, end_err.destroy)


def window_creator():
    """
    Used for creating new windows in the GUI (as function due to repeated use)
    :return: The window
    """
    window = Toplevel()
    window_canvas = Canvas(window, width=300, height=80)
    window_canvas.grid()

    return window


def change_button_state(button):
    """
    Used for changing the state of a given button (NORMAL/DISABLED)
    :param button: The button for which the state should be changed
    :return: (nothing)
    """
    if button["state"] == NORMAL:
        button["state"] = DISABLED
    else:
        button["state"] = NORMAL


def add_passage_window():
    """
    Used to visually display a window for adding passages,
    and call upon the backend function add_passage
    :return: (nothing)
    """
    window = window_creator()
    window.title("Registrera ny passage")

    date_prompt = Label(window, text="Ange datum (DD/MM/YYYY):")
    date_prompt.grid(column=0, row=0)
    date_input = Entry(window, width=10)
    date_input.grid(column=0, row=1)

    reg_prompt = Label(window, text="Ange registreringsnummer (AAAXXX):")
    reg_prompt.grid(column=0, row=2, pady=30)
    reg_input = Entry(window, width=10)
    reg_input.grid(column=0, row=3)

    start_prompt = Label(window, text="Ange starttid (TT:MM):")
    start_prompt.grid(column=0, row=4, pady=30)
    start_input = Entry(window, width=10)
    start_input.grid(column=0, row=5)

    end_prompt = Label(window, text="Ange sluttid (TT:MM):")
    end_prompt.grid(column=0, row=6, pady=30)
    end_input = Entry(window, width=10)
    end_input.grid(column=0, row=7)

    add_passage_button = Button(window, text="Lägg till passage",
                                command=lambda: add_passage(date_input.get(), reg_input.get(),  # Vid knapptryckning
                                                            start_input.get(), end_input.get(),
                                                            window, add_passage_button))
    add_passage_button.grid(column=0, row=8, pady=30)


def readfile_window(add_passage_button, add_car_button, calc_price_button,
                    show_history_button, pay_debt_button, file_prompt_label):
    """
    Used to visually display a window for reading and processing the log-file,
    and call upon the backend function read_from_file
    :param add_passage_button: The button for opening the graphical window used for adding passages
    :param add_car_button: The button for opening the graphical window used for adding cars
    :param calc_price_button: The button for opening the graphical window used for calculating debt
    :param show_history_button: The button for opening the graphical window used for showing history
    :param pay_debt_button: The button for opening the graphical window used for paying debt
    :param file_prompt_label: The graphical prompt at the beginning of the program telling the user to
    input the passage log-file
    :return: (nothing)
    """
    window = window_creator()
    window.title("Filinläsning")

    prompt = Label(window, text="Vänligen ange filnamn:")
    prompt.grid(column=0, row=0)
    file_entry = Entry(window, width=20)
    file_entry.grid(column=0, row=1)
    readfile_window_button = Button(window, text="Läs in", command=lambda: read_from_file(file_entry.get(), window,
                                                                                          readfile_window_button,
                                                                                          add_passage_button,
                                                                                          add_car_button,
                                                                                          calc_price_button,
                                                                                          show_history_button,
                                                                                          pay_debt_button,
                                                                                          file_prompt_label))
    readfile_window_button.grid(column=0, row=2, pady=35)


def add_car_window():
    """
    Used to visually display a window for adding new cars,
    and call upon the backend function add_car
    :return: (nothing)
    """
    window = window_creator()
    window.title("Bilregistrering")

    reg_prompt = Label(window, text="Ange registreringsnummer (AAAXXX):")
    reg_prompt.grid(column=0, row=0)
    reg_input = Entry(window, width=10)
    reg_input.grid(column=0, row=1)

    size_prompt = Label(window, text="Ange storlek på bil (Liten/Mellan/Stor):")
    size_prompt.grid(column=0, row=2, pady=30)
    size_input = Entry(window, width=10)
    size_input.grid(column=0, row=3)

    name_prompt = Label(window, text="Ange namn på bilägare:")
    name_prompt.grid(column=0, row=4, pady=30)
    name_input = Entry(window, width=10)
    name_input.grid(column=0, row=5)

    add_car_window_button = Button(window, text="Lägg till bil",
                                   command=lambda: add_car(reg_input.get(), size_input.get(), name_input.get(), window,
                                                           add_car_window_button))
    add_car_window_button.grid(column=0, row=6, pady=30)


def calc_price_window():
    """
    Used to visually display a window for calculating parking debt,
    and call upon the backend function calc_price
    :return: (nothing)
    """
    window = window_creator()
    window.title("Skuldberäkning")

    reg_prompt = Label(window, text="Ange registreringsnummer (AAAXXX):")
    reg_prompt.grid(column=0, row=0)
    reg_input = Entry(window, width=10)
    reg_input.grid(column=0, row=1)

    calc_price_window_button = Button(window, text="Beräkna skuld",
                                      command=lambda: calc_price(reg_input.get(), window, calc_price_window_button))
    calc_price_window_button.grid(column=0, row=2, pady=30)


def show_history_window():
    """
    Used to visually display a window for showing parking history of a car,
    and call upon the backend function show_parking
    :return: (nothing)
    """
    window = window_creator()
    window.title("Parkeringshistorik")

    reg_prompt = Label(window, text="Ange registreringsnummer (AAAXXX):")
    reg_prompt.grid(column=0, row=0)
    reg_input = Entry(window, width=10)
    reg_input.grid(column=0, row=1)

    show_history_button = Button(window, text="Visa historik",
                                 command=lambda: show_parking(reg_input.get(), window, show_history_button))
    show_history_button.grid(column=0, row=2, pady=30)


def pay_parking_window():
    """
    Used to visually display a window for paying debt,
    and call upon the backend function pay_parking
    :return: (nothing)
    """
    window = window_creator()
    window.title("Betalning av skuld")

    reg_prompt = Label(window, text="Ange registreringsnummer (AAAXXX):")
    reg_prompt.grid(column=0, row=0)
    reg_input = Entry(window, width=10)
    reg_input.grid(column=0, row=1)

    calc_button = Button(window, text="Beräkna skuld", command=lambda: pay_parking(reg_input.get(),
                                                                                   window, calc_button))
    calc_button.grid(column=0, row=2, pady=30)


def menu_buttons(frame):
    """
    Used for creating and displaying the main menu buttons on the frame, and linking the
    corresponding window-creating functions that execute when clicking them
    :param frame: The main menu window where logo and main menu buttons are displayed
    :return: (nothing)
    """
    add_passage_button = Button(frame, text="Inpassage/Utpassage", height=2, borderwidth=0, padx=47,
                                command=add_passage_window, state=DISABLED)  # Passagetilläggningsknapp i huvudmeny
    add_passage_button.grid(column=0, row=0)

    readfile_button = Button(frame, text="Läs in fil med historik", height=2, borderwidth=0,
                             padx=48, command=lambda: readfile_window(add_passage_button,
                                                                      add_car_button, calc_price_button,
                                                                      show_history_button, payment_button, file_label))
    readfile_button.grid(column=0, row=1)  # Filinläsningsknapp i huvudmeny

    add_car_button = Button(frame, text="Lägg till ny bil", height=2, borderwidth=0, padx=70.5,
                            command=add_car_window, state=DISABLED)  # Biltilläggningsknapp i huvudmeny
    add_car_button.grid(column=0, row=2)

    calc_price_button = Button(frame, text="Beräkna parkeringskostnad för en bil",
                               height=2, borderwidth=0, command=calc_price_window, state=DISABLED)
    calc_price_button.grid(column=0, row=3)  # Skuldberäkningsknapp i huvudmeny

    show_history_button = Button(frame, text="Visa parkeringshistorik för en bil", height=2, borderwidth=0,
                                 padx=14, command=show_history_window, state=DISABLED)
    show_history_button.grid(column=0, row=4)  # Parkeringshistorik-knapp i huvudmeny

    payment_button = Button(frame, text="Betala parkeringsskuld", height=2, borderwidth=0, padx=43,
                            command=pay_parking_window, state=DISABLED)
    payment_button.grid(column=0, row=5)  # Skuldbetalningsknapp i huvudmeny

    exit_button = Button(frame, text="Avsluta", height=2, borderwidth=0, command=quit, padx=90)
    exit_button.grid(column=0, row=6)  # Avsluta-knapp i huvudmeny

    file_label = Label(frame, text="Vänligen läs in en loggfil!", height=2, width=28, fg="red", bg="black")
    file_label.grid(column=0, row=8)  # Initiell text i huvudmenyn som försvinner när man läst in filen

    # Alla huvudknappar (förutom filinläsningen) är DISABLED i början av programmet då
    # de inte ska gå att trycka på innan loggfil har lästs in


def launch_graphics():
    """
    Used for launching the graphics and starting the main-loop of the GUI
    :return: (nothing)
    """
    root = Tk()  # Initierar GUI
    root.title("ParkSafe")  # Fönstertitel

    canvas = Canvas(root, bg="black", width=400, height=600)  # Huvudfönster
    canvas.grid(column=0, row=0)  # Relativistisk placering

    frame = Frame(root)  # Påläggsframe för att göra apploggans bakgrund transparent
    frame.grid(column=0, row=0)

    photo_image = ImageTk.PhotoImage(file="parksafelogo.png")
    canvas.create_image(200, 70, image=photo_image)  # Infogning av applogga i huvudmenyn

    menu_buttons(frame)  # Kallar in huvudmeny-knapparna

    root.mainloop()  # Sluter loopen


def main():
    """
    Used for launching main functionality of program (with a function call)
    :return: (nothing)
    """
    launch_graphics()


main()
