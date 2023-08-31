# FlowCord, the new Discord tool

### Features
1. You can create and use custom rich presence status (with integrated tutorial).
2. You can create and use custom CSS themes for the Discord desktop app.
### Why FlowCord?
You may ask, Why using FlowCord when you can use a tool like BetterDiscord?
The reason is simple, it's ultra easy to setup (just 6 clicks). It's easy to use, just navigate using the arrows trough the menu and select what you want. And... It doesn't crash every time you try to use it.
Also for developers, it's easy to modify/fork as you like.
### Requirements
- [Python 3+](https://www.python.org/downloads/)
- [Node JS](https://nodejs.org/en/download)
- [Windows 10+](https://www.microsoft.com/windows) (Windows 7 not tested yet)
### Installation guide
1. Download the latest release of FlowCord for your OS.
2. Extract it where you want it.
3. Launch the installer.bat script.
4. Launch FlowCord by launching the start.bat script.
5. (Optional) You can create a shortcut for the tool by right clicking on start.bat and selecting 'Create shortcut'. You can move this shortcut anywhere on your computer.
![](https://github.com/Locox-dev/Locox-dev/blob/main/flowcord1.gif)

### Troubleshooting
If you encounter this error:
```py
_curses.error: addwstr() returned ERR
```
This is because the script is trying to write some UI and there is not enough place. To resolve it, just maximize the terminal window size (so everything fit in it).