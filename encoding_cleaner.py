file_name = "opus.en-sr-test.sr"
fp = open("./opus-100/" + file_name)
text = "".join(fp.readlines())
new_text = ""
cyrillic_to_latin_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'ђ': 'đ', 'е': 'e', 'ж': 'ž', 'з': 'z',
        'и': 'i', 'ј': 'j', 'к': 'k', 'л': 'l', 'љ': 'lj', 'м': 'm', 'н': 'n', 'њ': 'nj', 'о': 'o',
        'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'ћ': 'ć', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c',
        'ч': 'č', 'џ': 'dž', 'ш': 'š',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Ђ': 'Đ', 'Е': 'E', 'Ж': 'Ž', 'З': 'Z',
        'И': 'I', 'Ј': 'J', 'К': 'K', 'Л': 'L', 'Љ': 'Lj', 'М': 'M', 'Н': 'N', 'Њ': 'Nj', 'О': 'O',
        'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'Ћ': 'Ć', 'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'C',
        'Ч': 'Č', 'Џ': 'Dž', 'Ш': 'Š'
    }

for i in text:
    #print(i)

    if(i == "è"):
        i = "č"

    elif(i == "æ"):
        i = "ć"

    elif(i == "È"):
        i = "Č"

    elif(i == "ð"):
        i = "đ"

    elif (i == "ð".upper()):
        i = "đ".upper()
        print(i)

    elif i in cyrillic_to_latin_dict:
        i = cyrillic_to_latin_dict[i]

    new_text = new_text + i
    #print(i.isascii())

    #print(f"new text: {new_text}")

print(type(new_text))
print(new_text)

fnew = open("corrected." + file_name, "w")
fnew.write(new_text)
