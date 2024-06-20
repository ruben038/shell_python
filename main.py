import sys
import os

def in_path(commande,paths):
    for path in paths:
        if os.path.exists(f"{path}/{commande}"):
            return True,path
    return False,None
def main():
    # Uncomment this block to pass the first stage
    # Wait for user input
    PATH = os.environ.get("PATH")
    HOME = os.environ.get("HOME")
    paths =PATH.split(":")
    builtins =["echo","type","exit","pwd","cd"]
    #print (paths)
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input()
        cmd= command.split(" ")[0]
        found ,path = in_path(cmd,paths)
        if command == "exit 0":
            #sys.stdout.write(f"{command}: 0\n")
            sys.exit(0)
        elif command.startswith("echo"):
            sys.stdout.write(f"{command[len('echo ') :]}\n")
            sys.stdout.flush()
        elif command.startswith("type"):
            args = command.split("type ")[1]
            find,chemin = in_path(args,paths)

            if not args in builtins:
                if find:
                    sys.stdout.write(f"{args} is {chemin}/{args}\n")
                else:
                    sys.stdout.write(f"{args}: not found\n")
                    sys.stdout.flush()
            else:
                sys.stdout.write(f"{args} is a shell builtin\n")
                sys.stdout.flush()
        elif found:
            os.system(command)
            sys.stdout.flush()
        elif command=="pwd":
            sys.stdout.write(f"{os.getcwd()}\n")
            sys.stdout.flush()
        elif command.startswith("cd"):
            sys.stdout.flush()            
            args = command.split("cd ")[1]
            #print(args)
            try:
                if args=="~":
                    os.chdir(HOME)
                else:
                    if args.startswith("/"):
                        absolute=args
                    elif args.startswith("."):
                        absolute = os.path.join(os.getcwd(), args)
                        absolute = os.path.normpath(absolute)
                    if absolute :
                        os.chdir(absolute)
                    else:
                        sys.stdout.write(f"cd: {args}: No such file or directory\n")
                        sys.stdout.flush()
               
            except FileNotFoundError:
                sys.stdout.write(f"cd: {args}: No such file or directory\n")
        else :
            sys.stdout.write(f"{command}: command not found\n")
            continue

if __name__ == "__main__":
    main()
