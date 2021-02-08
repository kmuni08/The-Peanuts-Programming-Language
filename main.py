import snoopy

while True:
    user_input_test = input('snoopy > ')
    result, error = snoopy.run('<stdin>', user_input_test)

    if error:
        print(error.as_string())
    else:
        print(result)
