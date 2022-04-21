

if __name__ == "__main__":
    print("\n### Welcome to the Programming Language Basic Version Shell ###\n")
    while True:
        inp = input("> ")
        commands = {
            "cout": "print",
            "cin": "input",
        }
        for i in commands:
            inp = inp.replace(i, commands[i])
        try: print(exec(inp))
        except: print("Syntax error")