# STEPS COMPILE
1. Activate virtualenv
2. ```commandline
   mkdir compile && cd compile
   ```
3. ```commandline
   pyinstaller -w -D -i "..\display\origin_design\icon.ico" --add_data "..\files:files" ..\main.py
   ```
4. Copy folder main from compile\dist to Desktop
5. Run main.exe