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
locale_en.for_message = '🌚 Private message for %s.'
locale_de.for_message = '🌚 Private Nachricht für %s.'
locale_it.for_message = '🌚 Messaggio privato per %s.'

# EXCEPT_MESSAGE
locale_en.except_message = 'Private message for everyone except %s.'
locale_de.except_message = 'Private Nachricht an alle ausser %s.'
locale_it.except_message = 'Messaggio privato per tutti tranne %s.'

# SPOILER_MESSAGE
locale_en.spoiler_message = 'Public spoiler message.'
locale_de.spoiler_message = 'Öffentlicher Spoiler.'
locale_it.spoiler_message = 'Messaggio contenente spoiler.'

# GROUP_GREETING_MESSAGE
locale_en.group_greeting_message = (
        '👋 Hi! My name is %s and I can help you send private messages that only certain people can view. '
        'To learn more send /start@%s and feel free to ask for help in our '
        '<a href="t.me/iSupGr">Supportiiis">public community</a> if you\'ve got any questions.')
locale_de.group_greeting_message = (
        '👋 Hallo! Mein Name ist @TGinlineBot und ich kann dir dabei helfen, private Nachrichten zu versenden, die nur bestimmte Personen sehen können. '
        'Drücke auf /start, um mehr zu erfahren und tritt unserer Support Gruppe bei.'
        '<a href="t.me/iSupGr">Supportiiis Gruppe</a> wenn du Fragen hast.')
locale_it.group_greeting_message = (
        '👋 Ciao! Il mio nome è %s E posso aiutarti ad inviare messaggi privati che solo alcuni possono vedere. '
        'per sapere di più invia /start@%s e sentiti libero di chiedere aiuto '
        '<a href="t.me/iSupGr">Supportiiis">gruppo pubblico</a> se hai domande.')

# INFO_MESSAGE
locale_en.info_message = (
        'If you still have questions after reading the article, you can contact support or simply ask '
        'for help in our public chat at any time you want.\n\n'
        '👥 Chat: @iSupGr\n'
        '🆘 Support: @iSupGr')
locale_de.info_message = (
        'Solltest du Fragen haben, nachdem du die Hilfe gelesen hast, kannst du in die Support Gruppe schreiben.'
        'für Hilfe in unserem öffentlichen Chat, wann immer du willst.\n\n'
        '👥 Chat: @iSupGr\n'
        '🆘 Support: @iSupGr')
locale_it.info_message = (
         'Se hai ancora domande dopo aver letto questo articolo, puoi contattare il supporto nella nostra '
         'chat pubblica quando vuoi.\n\n'
         '👥 Chat: @iSupGr\n'
         '🆘 Support: @iSupGr')

# HOW_TO_USE
locale_en.how_to_use = 'How to use this bot?'
locale_de.how_to_use = 'Wie geht das?'
locale_it.how_to_use = 'Come usare questo bot?'

# TOO_LONG_DESCRIPTION
locale_en.too_long_description = 'Please shorten the length of your message so that it doesn\'t exceed the limit of 200 characters.'
locale_de.too_long_description = 'Bitte fasse dich etwas kürzer und überschreite das Limit von 200 Zeichen nicht.'
locale_it.too_long_description = 'Perfavore accorcia la lunghezza del tuo messaggio in modo che non superi i 200 caratteri.'

# NOT_ALLOWED
locale_en.not_allowed = 'You are not allowed to view this content.'
locale_de.not_allowed = 'Nope, das ist nicht für dich.'
locale_it.not_allowed = 'Non hai il permesso per vedere questo messaggio.'

# NOT_ACCESSIBLE
locale_en.not_accessible = 'This content is no longer accessible.'
locale_de.not_accessible = 'Der Inhalt ist nicht länger sichtbar.'
locale_it.not_accessible = 'Questo contenuto non è più accessibile.'

# VIEW
locale_en.view = 'View'
locale_de.view = '👀 Ansehen'
locale_it.view = 'Vedi'

# AND_CONNECTOR
locale_en.and_connector = 'and'
locale_de.and_connector = 'und'
locale_it.and_connector = 'e'
