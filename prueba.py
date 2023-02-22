import re

def validate_phone_number(numero):
  patron = re.compile(r"^[+1]")
  coincidencia = re.match(patron, numero)
  if coincidencia:
    return True
  else:
    return False



list_numeros = ["+123456789012", "+1 (800) 345-7865", "+1 800 123-4567", "+1 800 1234567", "+1800 1234567", 
"+1800 123-4567", "+1(800)1234567", "+1(800)123-4567", "+18001234567", "+1-800-123-4567", "+1 800 12-34-56-78",
"1234567890"]

for num in list_numeros:
    if validate_phone_number(num):
        print("El número es válido")
    else:
        print("El número no es válido")
