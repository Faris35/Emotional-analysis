import re
import regex
import nltk
from pyarabic import araby
from nltk.corpus import stopwords
from nltk.stem.isri import ISRIStemmer
import emoji

# Ensure you have downloaded the Arabic stop words
nltk.download('stopwords')

class ArabicTextPreprocessor:
    def __init__(self):
        self.emojis = {
                "🙂":"ضحك", "🤣":"ضحك", "😂":"ضحك", "💔":"حزن", "🙂":"ضحك", "❤️":"حب", "❤":"حب", "😍":"حب", "😭":"حزن", "😢":"حزن",
                "😔":"حزن", "♥":"حب", "💜":"حب", "😅":"ضحك", "🙁":"حزن", "💕":"حب", "💙":"حب", "😞":"حزن", "😊":"فرح", "👏":"يصفق",
                "👌":"احسنت", "😴":"نوم", "😀":"ضحك", "😌":"حزن", "🌹":"وردة", "🙈":"حب", "😄":"ضحك", "😐":"محايد", "✌":"منتصر", "✨":"نجمه",
                "🤔":"تفكير", "😏":"يستهزء", "😒":"غضب", "🙄":"ملل", "😕":"غضب", "😃":"ضحك", "🌸":"وردة", "😓":"حزن", "💞":"حب", "💗":"حب",
                "😑":"غضب", "💭":"تفكير", "😎":"ثقة", "💛":"حب", "😩":"حزن", "💪":"عضلات", "👍":"موافق", "🙏🏻":"شكر", "😳":"قلق", "👏🏼":"تصفيق",
                "🎶":"موسيقي", "🌚":"صمت", "💚":"حب", "🙏":"شكر", "💘":"حب", "🍃":"سلام", "☺":"ضحك", "🐸":"ضفدع", "😶":"قلق", "✋🏻":"توقف",
                "😉":"فرح", "🌷":"حب", "🙃":"فرح", "😫":"حزن", "😨":"خوف", "🎼 ":"موسيقي", "🍁":"مرح", "🍂":"مرح", "💟":"حب", "😪":"حزن",
                "😆":"ضحك", "😣":"غضب", "☺️":"حب", "😱":"خوف", "😁":"ضحك", "😖":"استياء", "🏃🏼":"يجري", "😡":"غضب", "🚶":"يسير", "🤕":"مرض",
                "‼️":"تعجب", "🕊":"طائر", "👌🏻":"احسنت", "❣":"حب", "🙊":"مصدوم", "💃":"مرح", "💃🏼":"مرح", "😜":"مرح", "👊":"ضربة", "😟":"استياء",
                "💖":"حب", "😥":"حزن", "🎻":"موسيقي", "✒":"يكتب", "🚶🏻":"يسير", "💎":"الماس", "😷":"مرض", "☝":"واحد", "🚬":"تدخين",
                "💐" : "ورد", "🌞" : "شمس", "👆" : "الاول", "⚠️" :"تحذير", "🤗" : "احتواء", "✖️": "غلط", "📍"  : "مكان", "👸" : "ملكه",
                "👑" : "تاج", "✔️" : "صح", "💌": "قلب", "😲" : "مندهش", "💦": "ماء", "🚫" : "خطا", "👏🏻" : "ممتاز", "🏊" :"يسبح", "👍🏻": "تمام",
                "⭕️" :"دائره", "🎷" : "موسيقي", "👋": "تلويح باليد", "✌🏼": "علامه النصر", "🌝":"ضحك", "➿"  : "عقده مزدوجه", "💪🏼" : "قوي",
                "📩":  "تواصل معي", "☕️": "قهوه", "😧" : "غضب", "🗨": "رسالة", "❗️" :"تعجب", "🙆🏻": "اشاره موافقه", "👯" :"اخوات", "©" :  "رمز",
                "👵🏽" :"سيده عجوزه", "🐣": "كتكوت", "🙌": "تشجيع", "🙇": "شخص ينحني", "👐🏽":"ايدي مفتوحه", "👌🏽": "بالظبط", "⁉️" : "استنكار",
                "⚽️": "كوره", "🕶" :"حب", "🎈" :"بالون", "🎀": "ورده", "💵":  "فلوس", "😋":  "فرح", "😛":  "فرح", "😠":  "غضب", "✍🏻":  "يكتب",
                "🌾":  "ارز", "👣":  "اثر قدمين", "❌":"رفض", "🍟":"طعام", "👬":"صداقة", "🐰":"ارنب", "☂":"مطر", "⚜":"مملكة فرنسا", "🐑":"خروف",
                "🗣":"صوت مرتفع", "👌🏼":"احسنت", "☘":"مرح", "😮":"خوف", "😦":"خوف", "⭕":"الحق", "✏️":"قلم", "ℹ":"معلومات", "🙍🏻":"رفض", "⚪️":"نضارة نقاء",
                "🐤":"حزن", "💫":"مرح", "💝":"حب", "🍔":"طعام", "❤︎":"حب", "✈️":"سفر", "🏃🏻‍♀️":"يسير", "🍳":"ذكر", "🎤":"مايك غناء", "🎾":"كره", "🐔":"دجاجة",
                "🙋":"سؤال", "📮":"بحر", "💉":"دواء", "🙏🏼":"شكر", "💂🏿 ":"حارس", "🎬":"سينما", "♦️":"مرح", "💡":"قكرة", "‼":"تعجب", "👼":"طفل", "🔑":"مفتاح",
                "♥️":"حب", "🕋":"كعبة", "🐓":"دجاجة", "💩":"معترض", "👽":"فضائي", "☔️":"مطر", "🍷":"عصير", "🌟":"نجمة", "☁️":"سحب", "👃":"معترض", "🌺":"مرح",
                "🔪":"سكينة", "♨":"سخونية", "👊🏼":"ضرب", "✏":"قلم", "🚶🏾‍♀️":"يسير", "👊":"ضرب", "😚":"حب", "🔸":"مرح", "👎🏻":"لا يعجبني", "👊🏽":"ضربة", "😙":"حب",
                "🎥":"تصوير", "👉":"جذب انتباه", "👏🏽":"يصفق", "💪🏻":"عضلات", "🏴":"اسود", "🔥":"حريق", "😬":"خوف", "👊🏿":"يضرب", "🌿":"ورقه شجره", "✋🏼":"كف ايد",    
                "👐":"ايدي مفتوحه", "☠️":"رعب", "🎉":"يهنئ", "🔕" :"صامت", "😿":"حزن", "☹️":"حزن", "😘" :"حب", "😰" :"خوف و حزن", "🌼":"ورده", "💋":"بوسه",
                "👇":"لاسفل", "❣️":"حب", "🎧":"سماعات", "📝":"يكتب", "😇":"سعيد", "😈":"رعب", "🏃":"يجري", "✌🏻":"علامه النصر", "🔫":"يضرب", "❗️":"تعجب",
                "👎":"غير موافق", "🔐":"قفل", "👈":"لليمين", "™":"رمز", "🚶🏽":"يتمشي", "😯":"متفاجأ", "✊":"يد مغلقه", "😻":"اعجاب", "🙉" :"قرد", "👧":"طفله",     
                "🔴":"دائره حمراء", "💪🏽":"قوه", "💤":"نوم", "👀":"حيره", "✍🏻":"يكتب", "❄️":"تلج", "💀":"رعب", "😤":"غضب", "🖋":"قلم", "🎩":"كاب", "☕️":"قهوه",     
                "😹":"ضحك", "💓":"حب", "☄️ ":"نار", "👻":"رعب", "🤮":"مقرف", "🤢":"مقرف", "🤪":"مرح", "🥴":"تعب", "🤧":"مرض", "🤒":"مرض", "🤕":"مرض", "🤑":"مرح",
                "🤐":"صمت", "🤫":"صمت", "🤭":"ضحك", "🧐":"تفكير", "🤓":"ذكاء", "🤩":"مرح", "🥳":"مرح", "🥺":"حزن", "🤥":"كذب", "🤔":"تفكير", "🤗":"مرح", "🥰":"مرح",
                "🤍":"حب", "🤲":"دعاء", "󾌴":"", "🤦":"الم", "🤷‍":"قلق", "🤚":"يد", "🦋":"مرح", "🥇":"فوز",
        }

        self.emoticons = {
            ":))": "ضحك", "((:": "ضحك", ":)": "ضحك", "(:": "ضحك",
            ":(": "حزن", "):": "حزن", "xD": "ضحك", "XD": "ضحك",
            ":=(": "يبكي", ":'(": "حزن", ":'‑(": "حزن", "XD" : "ضحك",
            ":D" : "ضحك", "♬" : "موسيقي", "♡" : "حب", "☻"  : "ضحك",
        }

        
        self.negation_words = [
            "لست","مب","غير", "ليس", "سوى", "لم", "لن", "ما", "لا", "بلا", "بدون", "عير", "عدا", "كلا"
        ]
    
        self.stemmer = ISRIStemmer()

    def preprocess_text(self, text):
        text = self.replace_emojis_with_text(text)
        text = self.replace_emoticons_with_text(text)
        text = self.remove_stop_words(text)
        text = self.remove_urls(text)
        text = self.remove_non_arabic(text)
        text = self.remove_numbers(text)
        text = self.normalize_arabic(text)
        text = self.remove_punctuations(text)
        text = self.lemmatize_arabic(text)
        return text

    def remove_stop_words(self, text):
        arabic_stopwords = set(stopwords.words('arabic'))
        # Exclude negation words from the stop words list
        stopwords_to_remove = [word for word in arabic_stopwords if word not in self.negation_words]
        return " ".join([word for word in text.split() if word not in stopwords_to_remove])


    def lemmatize_arabic(self, text):
        return " ".join([self.stemmer.stem(word) for word in text.split()])

    def normalize_arabic(self, text):
        text = text.strip()
        text = re.sub("ى", "ي", text)
        text = re.sub("ؤ", "ء", text)
        text = re.sub("ئ", "ء", text)
        text = re.sub("ة", "ه", text)
        
        #remove repetetions
        text = re.sub("[إأٱآا]", "ا", text)
        text = text.replace('وو', 'و')
        text = text.replace('يي', 'ي')
        text = text.replace('ييي', 'ي')
        text = text.replace('اا', 'ا')

        #Remove extra whitespace
        text = re.sub('\s+', ' ', text)
        
        #Remove longation
        text = re.sub(r'(.)\1+', r"\1\1", text) 
        
        #Strip vowels from a text, include Shadda.
        text = araby.strip_tashkeel(text)
        
        #Strip diacritics from a text, include harakats and small lettres The striped marks are
        text = araby.strip_diacritics(text)
        text=''.join([i for i in text if not i.isdigit()])
        return text

    def remove_non_arabic(self, text):
        return re.sub('[A-Za-z]+', ' ', text)

    def remove_numbers(self, text):
        return ''.join([i for i in text if not i.isdigit()])

    def remove_punctuations(self, text):
        # Remove punctuations
        text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,،-./:;<=>؟?@[\]^_`{|}~"0123456789\\A-Za-z•—"""), ' ', text)
        text = text.replace('؛',"", )

        # Remove extra whitespace
        text = re.sub('\s+', ' ', text)
        text =  " ".join(text.split())
        return text.strip()

    def remove_urls(self, text):
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        return url_pattern.sub(r'', text)

    def replace_emojis_with_text(self, text):
        translated_text = ""
        for char in text:
            if any(emoji.distinct_emoji_list(char) for char in char):
                translated_text += " " + self.emojis.get(char, char) + " "
            else:
                translated_text += self.emojis.get(char, char)
        return translated_text

    def replace_emoticons_with_text(self, text):
        translated_text = ""
        seperarate_word = text.split(' ')
        for word in seperarate_word:
            translated_text += self.emoticons.get(word, word) + " "
        return translated_text
