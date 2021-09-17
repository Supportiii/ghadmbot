from locales_dict import Locale, LocalesDict

locale_en = Locale()
locale_de = Locale()
locale_it = Locale()

locales = LocalesDict({
    'en': locale_en,
    'de': locale_de,
    'it': locale_it
}, locale_en)

# TOO_LONG_TITLE
locale_en.too_long_title = 'Your message is too long'
locale_de.too_long_title = 'Deine Nachricht ist zu lang'
locale_it.too_long_title = 'Il tuo messaggio è troppo lungo'

# FOR_TITLE
locale_en.for_title = 'For %s'
locale_de.for_title = 'Für %s'
locale_it.for_title = 'Per %s'

# EXCEPT_TITLE
locale_en.except_title = 'Except %s'
locale_de.except_title = 'Akzeptiere %s'
locale_it.except_title = 'Tranne %s'

# SPOILER_TITLE
locale_en.spoiler_title = 'Spoiler'
locale_de.spoiler_title = 'Spoiler'
locale_it.spoiler_title = 'Spoiler'

# TOO_LONG_MESSAGE
locale_en.too_long_message = '🥺 Sorry, your message can\'t be sent as it exceeds the limit of 200 characters.'
locale_de.too_long_message = '🥺 Sorry, deine Nachricht kann nicht gesendet werden, da sie das Limit von 200 Zeichen überschreitet.'
locale_it.too_long_message = '🥺 Mi dispiace, il tuo messaggio non può essere mandato, supera il limite di 200 caratteri.'

# FOR_MESSAGE
locale_en.for_message = 'Private message for GroupHelp admins'
locale_de.for_message = 'Private Nachricht an GroupHelp-Admins'
locale_it.for_message = 'Messaggio privato a GroupHelp-Admins'

# SPOILER_MESSAGE
locale_en.spoiler_message = '🌐 A Public spoiler message for all members:'
locale_de.spoiler_message = '🌐 Ein Post für alle Mitglieder:'
locale_it.spoiler_message = '🌐 Un post per tutti i membri:'

# INFO_MESSAGE
locale_en.info_message = (
        '👋 Hello! This bot is exclusively for communication between GH admins.')
locale_de.info_message = (
        '👋 Hallo! Dieser Bot ist ausschließlich zur Kommunikation zwischen GH-Admins.')
locale_it.info_message = (
        '👋 Ciao, questo bot è esclusivamente per la comunicazione tra gli amministratori di GH.')

# TOO_LONG_DESCRIPTION
locale_en.too_long_description = 'Please shorten the length of your message so that it doesn\'t exceed the limit of 200 characters.'
locale_de.too_long_description = 'Bitte fasse dich etwas kürzer und überschreite das Limit von 200 Zeichen nicht.'
locale_it.too_long_description = 'Perfavore accorcia la lunghezza del tuo messaggio in modo che non superi i 200 caratteri.'

# NOT_ALLOWED
locale_en.not_allowed = '❌ You are not allowed to view this content.'
locale_de.not_allowed = '❌ Diese Nachricht ist nicht für dich.'
locale_it.not_allowed = '❌ Non hai il permesso per vedere questo messaggio.'

# NOT_ACCESSIBLE
locale_en.not_accessible = 'This content is no longer accessible.'
locale_de.not_accessible = 'Der Inhalt ist nicht mehr sichtbar.'
locale_it.not_accessible = 'Questo contenuto non è più accessibile.'

# VIEW
locale_en.view = '👀 View'
locale_de.view = '👀 Ansehen'
locale_it.view = '👀 Vedi'
