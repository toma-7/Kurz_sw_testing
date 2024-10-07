########################################
# Projekt 2  ke kurzu Testing Akademie #
# Jméno: Bc.Tomáš Samec                #
########################################

from playwright._impl._errors import TimeoutError as PlaywrightTimeoutError

def potvrzeni_cookies(page):
    """
    *  Funkce 5 vteřin testuje zda se načetlo potvrzovací okno cookies.
    Důvodem tohoto opatření je ošetření varianty spuštění kódu v headless módu,
        při kterém načtení potvrzovacího okna cookies neproběhne a kód skončí chybovou hláškou TimeoutError.
    :param page: Objekt, který představuje jednu webovou stránku otevřenou v prohlížeči
    :return: Funkce vypíše buď potvrzení cookies nebo, že se potvrzovací okno nezobrazilo
    """

    try:
        page.locator("span:has-text('Rozumím a přijímám')").wait_for(state='visible', timeout=5000)
        cookies_button = page.locator("span:has-text('Rozumím a přijímám')")
        cookies_button.click()
        print("\tBylo kliknuto na tlačítko 'Rozumím a přijímám'.")
    except PlaywrightTimeoutError:
        print("\tSouhlas s cookies se nezobrazil do 5 sekund, proto kód pokračoval dál.")
    return



def test_root_telefon_na_vydavatele(page):
    """
    *   Funkce testuje na webové stránce https://www.root.cz/ správnost telefonního čísla na sídlo vydavatele.
    Tvar hledaného telefonního čísla: +420 778 885 502
    :param page: Objekt, který představuje jednu webovou stránku otevřenou v prohlížeči
    :return: Porovnání očekávaného a skutečného telefonního čísla
    """


    # Načtení stránky, potvrzení cookies a proklikání na stránku s kontakty
    page.goto('https://www.root.cz/')
    potvrzeni_cookies(page)
    contact_link = page.locator("a[href='https://www.root.cz/kontakt/']")
    contact_link.click()


    # Nalezení telefonního čísla a úpravy pro jeho získání
    telefon_text = page.locator("p:has-text('Telefon:')")
    actual_text = telefon_text.inner_text().replace('\u00A0', ' ')
    start_index = actual_text.index("Telefon: ") + len("Telefon: ")
    end_index = actual_text.index("E-mail:")
    extracted_phone_number = actual_text[start_index:end_index].strip()


    # Ověření, zda telefonní číslo odpovídá
    expected_phone_number = "+420 778 885 502"
    print(f"\nOčekávané číslo: '{expected_phone_number}', skutečné číslo: '{extracted_phone_number}'")
    assert extracted_phone_number == expected_phone_number, "Telefonní čísla se neshodují."



def test_root_vyhledani_knihy_Ucebnice_jazyka_Python(page):
    """
    *   Funkce testuje na webové stránce https://www.root.cz/ vyhledávání knižního titulu,
    který je na webu Root.cz dostupný ve formátu pdf.
    :param page: Objekt, který představuje jednu webovou stránku otevřenou v prohlížeči
    :return: Počet názvů knihy nalezených na stránce. Žádný název = vyhledávání na webu nefunguje
    :výsledek testu: Webová stránka testem neprošla. Ačkoliv se tam kniha nachází, nebyla vyhledavačem nalezená.
    """


    # Načtení stránky, potvrzení cookies a aktivace vyhledávacího pole
    page.goto('https://www.root.cz/')
    potvrzeni_cookies(page)
    search_link = page.locator("a.navigation__link--search.navigation__link:has(span.element-blind-user:has-text('Hledat'))")
    search_link.click()
    search_field = page.locator("#search-field-query")
    search_field.click()


    # Zadání názvu knihy do vyhledávacího pole
    search_field.fill("Učebnice jazyka Python Jan Švec")
    search_button = page.locator(".design-form__submit.design-button--primary.design-button--large")
    search_button.click()


    # Ověření, zda se na stránce vyskytuje název hledané knihy
    assert page.locator("text='Učebnice jazyka Python'").count() > 0, "Kniha uvedeného názvu nebyla vyhledávačem nalezená."



def test_root_pokus_o_prihlaseni(page):
    """
    *   Funkce testuje na webové stránce https://www.root.cz/ správnost chybové hlášky
    při pokusu o přihlášení s nesprávnými údaji.
    :param page: Objekt, který představuje jednu webovou stránku otevřenou v prohlížeči
    :return: Porovnání očekávaného a skutečného textu chybové hlášky
    """


    # Načtení stránky, potvrzení cookies a proklikání na přihlašovací stránku.
    page.goto('https://www.root.cz/')
    potvrzeni_cookies(page)
    login_link = page.locator("span.icon--profile.icon.design-svg-element")
    login_link.click()


    # Zadání přihlašovacích údajů
    user_name_field = page.locator("#frm-form-local-innerForm-us_name")
    user_name_field.fill("uzivatel_5425fd5g8")
    password_field = page.locator('#frm-form-local-innerForm-us_pwd')
    password_field.fill("fhfutg5252946_@")
    login_button = page.locator('input[type="submit"][name="us_submit"][value="Přihlásit"].design-button--medium.design-button--primary')
    login_button.click()


    # Ověření zda je chybový text správný
    error_message = page.locator('div.design-message__content-inner.acceptance-message.acceptance-message--error')
    expected_full_text = (
        "Vaše přihlašovací údaje nejsou správné.\n"
        "- Obnova zapomenutého hesla\n"
        "- Připomenutí uživatelského jména"
    )
    assert error_message.inner_text().strip() == expected_full_text.strip(), "Text se v chybové hlášce neshoduje."
