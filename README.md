# Share_Photo
## Install Library
```
pip3 install requests
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
## Setting
The following is an example.
```
mkdir -p ~/.local/opt
cd ~/.local/opt
git clone git@github.com:h-akira/Share_Photo.git
# take `credentials.json` and put it in `secret`
cd ~/.local/opt/Share_photo
cp sample/done.sh src
# edit `bin/done.sh`
~/.local/opt/Share_photo/bin/done.sh
# login
```
For periodic execution:
```
mkdir -p ~/.local/etc
cp ~/.local/opt/Share_photo/sample/crontab ~/.local/etc
# edit `~/.local/etc/crontab`
crontab ~/.local/etc/crontab
```
## Reference
- [Guide of Google Photos APIs](https://developers.google.com/photos/library/guides/upload-media?hl=ja#rest_1)
- [Guide of Google Workspace (Gmail)](https://developers.google.com/gmail/api/quickstart/python?hl=ja)
