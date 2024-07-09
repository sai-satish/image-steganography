import cv2
import string
import os

# storing ASCII values
d = {}
c = {}
alphabets = string.ascii_lowercase
for i in range(255):
    d[chr(i)] = i
    c[i] = chr(i)


while True:
    choice = int(input("1. Encrypt\n2. Decrypt\n3. Exit\nEnter Choice\t:"))
    match choice:
        case 1:
            # reading image
            x = cv2.imread(r"D:\Study\Engineering\E2-S2\WT\Sem-prep\practise\original.png")
            i = x.shape[0]  # height
            j = x.shape[1]  # width
            origin = [i // 2, j // 2]

            secret_key = input("Please enter the secret key\t:")
            text = input("Enter text to hide\t\t:")
            keyLength = 0
            text_length = len(text)
            actual_key_length = len(secret_key)
            z = 0  # select color plane in the image

            # encrypting part-1
            displacing_amount = alphabets.index(secret_key[-1]) % 94
            # print("last digit", d[secret_key[-1]])
            # print("displacement_amount:", displacing_amount)
            new_text = []
            for char in text:
                if 33 <= d[char] <= 126:
                    index = (d[char] + displacing_amount) if (d[char] + displacing_amount) <= 126 else 33 + (d[char] + displacing_amount - 127)
                    replacing_char = c[index]
                    # print(char, ":", replacing_char, ".")
                    new_text.append(replacing_char)
                else:
                    new_text.append(char)

            cipher_text = ''.join(new_text)
            # print(cipher_text)

            # encrypting part-2
            coordinates = [[origin[0] + 1, origin[1] + 1], [origin[0] - 1, origin[1] + 1], [origin[0] - 1, origin[1] - 1], [origin[0] + 1, origin[1] - 1]]
            select_coordinate = 0
            for i in range(text_length):
                n = coordinates[select_coordinate][0]
                m = coordinates[select_coordinate][1]
                x[n, m, z] = d[cipher_text[i]] ^ d[secret_key[keyLength]]

                # update current coordinate
                if select_coordinate == 0:
                    coordinates[select_coordinate][0] += 1
                    coordinates[select_coordinate][1] += 1
                elif select_coordinate == 1:
                    coordinates[select_coordinate][0] -= 1
                    coordinates[select_coordinate][1] += 1
                elif select_coordinate == 2:
                    coordinates[select_coordinate][0] -= 1
                    coordinates[select_coordinate][1] -= 1
                elif select_coordinate == 3:
                    coordinates[select_coordinate][0] += 1
                    coordinates[select_coordinate][1] -= 1

                z = (z + 1) % 3
                select_coordinate = (select_coordinate + 1) % 4
                keyLength = (keyLength + 1) % actual_key_length

            cv2.imwrite(f"encrypted-{text_length}.png", x)
            #os.startfile(f"encrypted-{text_length}.png")
            print("Data hiding is completed successfully")

        case 2:
            z = 0
            key_entered = input("Enter secret key\t\t:")
            key_length = len(key_entered)
            displacing_amount = alphabets.index(key_entered[-1]) % 94
            path = input("Enter Encrypted Image path:")
            find_name = path.split("\\")

            #read encrypted image
            x = cv2.imread(path)
            i = x.shape[0]  # height
            j = x.shape[1]
            origin = [i // 2, j // 2]

            coordinates = [[origin[0] + 1, origin[1] + 1], [origin[0] - 1, origin[1] + 1], [origin[0] - 1, origin[1] - 1], [origin[0] + 1, origin[1] - 1]]
            select_coordinate = 0
            keyLength = 0

            # decrypting part-1
            text_length = int(find_name[-1].split(".")[0].split("-")[1])                
            print(text_length)
            decrypt = ""
            for i in range(text_length):
                try:
                    n = coordinates[select_coordinate][0]
                    m = coordinates[select_coordinate][1]
                    decrypt += c[x[n, m, z] ^ d[key_entered[keyLength]]]
                    
                    if select_coordinate == 0:
                        coordinates[select_coordinate][0] += 1
                        coordinates[select_coordinate][1] += 1
                    elif select_coordinate == 1:
                        coordinates[select_coordinate][0] -= 1
                        coordinates[select_coordinate][1] += 1
                    elif select_coordinate == 2:
                        coordinates[select_coordinate][0] -= 1
                        coordinates[select_coordinate][1] -= 1
                    elif select_coordinate == 3:
                        coordinates[select_coordinate][0] += 1
                        coordinates[select_coordinate][1] -= 1

                    z = (z + 1) % 3
                    keyLength = (keyLength + 1) % key_length
                    select_coordinate = (select_coordinate + 1) % 4
                except Exception as e:
                    print(f"Error: {e}")
                    break
            #print("Encrypted text: ", decrypt)
            # decrypting part-2
            decrypting = []
            for char in decrypt:
                if 33 <= d[char] <= 126:
                    index = (d[char] - displacing_amount) if (d[char] - displacing_amount) >= 33 else 127 - (33 - (d[char] - displacing_amount))
                    original_char = c[index]
                    decrypting.append(original_char)
                else:
                    decrypting.append(char)

            decrypted_text = ''.join(decrypting)
            print("Decrypted text:", decrypted_text)

            
        case 3:
            print("Thank you. Exiting...")
            break
        case _:
            print("Enter properly..!")