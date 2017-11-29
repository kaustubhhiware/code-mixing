# Install transliteration from https://github.com/libindic/Transliteration
import transliteration as t

en = "This is a english text for transliteration"

def testEnglishToHindi():
    result = t.transliterate(en, "hi_IN")
    print result.encode('utf-8')