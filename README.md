# Multivoice Windows Dialer

This project provides a small command line dialer that triggers calls through the [Multivoice](https://doc.vpbx.me/admin/ws/#ringing) API. It is intended to be packaged as a Windows application that handles `tel:` links from a browser.

## Configuration
1. Install Python 3.10+.
2. Copy `config.example.json` to `config.json` and fill in your API key.
3. Copy `extension.example.txt` to `extension.txt` and set your extension number.
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
```
python dialer.py <phone_number>
```
The script sends a request to `https://vpbx.me/api/originatecall/<phone_number>/<extension>` using your API key and extension
from `extension.txt`. The `<phone_number>` argument can be a plain number or a `tel:` link such as `tel:+123456789`.

## Building a Windows executable
The project can be bundled with [PyInstaller](https://www.pyinstaller.org/):
```bash
pip install pyinstaller
pyinstaller --onefile dialer.py
```
The resulting executable in `dist/` can be associated with the `tel` protocol so that clicking telephone links in a browser will invoke it. To register the handler, create a file `register.bat` with the following content and run it as Administrator:
```
@echo off
REG ADD "HKCU\Software\Classes\tel" /ve /t REG_SZ /d "URL:Telephone" /f
REG ADD "HKCU\Software\Classes\tel" /v "URL Protocol" /t REG_SZ /d "" /f
REG ADD "HKCU\Software\Classes\tel\shell\open\command" /ve /t REG_SZ /d "%~dp0dialer.exe %%1" /f
```
Adjust the path to `dialer.exe` if necessary.
