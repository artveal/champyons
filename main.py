from champyons.core.i18n.translation import format_message


def main():
    message = "Tu equipo puede acabar en {pos1, selectordinal, one {#ª posición} other {#ª posición}} y {pos2, selectordinal, one {#ª posición} other {#ª posición}}"

    fmt_message = format_message(message, pos1=1, pos2=2)
    print(fmt_message)
        
if __name__ == "__main__":
    main()
