from commands.commands import *

non_logged_in_command_map: [int, AbstractCommand] = {
    1: LoginCommand(),
    2: RegisterCommand(),
    3: ListRoomsCommand(),
}

command_map: [int, AbstractCommand] = {
    1: ProfileCommand(),
    2: AddBalanceCommand(),
    3: ListRoomsCommand(),
    4: BookRoomCommand(),
    9: LogoutCommand(),
}


def get_list_of_options_for_non_logged_in():
    return """List of commands, enter number to execute:
    1: Login 
    2: Register
    3: List rooms
   -1: Exit
    """


def get_list_of_options_for_logged_in():
    return """List of commands, enter number to execute:
    1: Profile
    2: Add balance
    3: List rooms
    4: Book room
    9: Logout
   -1: Exit
    """


if __name__ == "__main__":
    while True:
        if SessionHolder.get_current_user() is None:
            print(get_list_of_options_for_non_logged_in())
            option = int(input())
            if option == -1:
                break
            non_logged_in_command_map[option].execute()
        else:
            print(get_list_of_options_for_logged_in())
            option = int(input())
            if option == -1:
                break
            command_map[option].execute()
