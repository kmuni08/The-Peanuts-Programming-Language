import snoopy

while True:
    user_input_test = input('snoopy > ')
    result, error = snoopy.run('<stdin>', user_input_test)

    if error:
        print(error.__str__())
    elif result:
        print(result)
