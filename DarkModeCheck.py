from winreg import ConnectRegistry, OpenKey, QueryValueEx, HKEY_CURRENT_USER

def isLightModeOn():
    """Checks User's Window's settings to see if dark mode is enabled.
    
    Returns:
        bool -- light_mode = True/False
    """
    light_mode = True

    # key values is a raw string so backslashes are escape characters
    key_values = r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize'
    regis = ConnectRegistry(None, HKEY_CURRENT_USER)
    opened_key = OpenKey(regis, key_values)

    val = QueryValueEx(opened_key, "AppsUseLightTheme")[0]

    if val == 0: # dark mode enabled
        light_mode = False
    return light_mode

if __name__ == "__main__":
    LIGHT_MODE_ON = isLightModeOn()
    if not LIGHT_MODE_ON:
        print("User has dark mode enabled.")
    else:
        print("User has light mode enabled.")
