! This Readme does not fit to the rest of the project anymore!

_______________________________________________

### **Discord Storage** _Rewrite_ (Beta)

**Made by *BoKa***

*Enjoy Discords free and unlimited storage...*

_______________________________________________	


# Usage

## Prepare

Clone this from Github,
make sure there is a directory called "temp" and anotherone called "presplit" in the cloned directory.
If not create those (empty).

You need the following [PIP](https://pypi.org/project/pip/) package:

##### Discord:

	sudo pip install discord

You will need a Discord "servers" token too. This may help you:

Download Discord and generate one

	sudo pamac install snapd

	sudo snap install discord --classic

an API key for this server is required:

[Here](https://www.youtube.com/watch?v=gT_1c9YFffk) is how to create one.

Put both in there right position in filetools.py
	you can find them with <strg> + <f> "!!!" 		#TODO: Optimize that!

## Use the GUI 										#TODO

1. Put some files in the same directory

2. Execute _python3 gui.py_ in Linux console. 

3. Leftclick the filename to upload, or Rightclick a linklists file to download, 
you can even upload them again, because why not.

## Use it as API									#TODO

	import filetools.py

If you realy want to use the script in your application
have a look at the last two functions of the filetools.py script!

Care about the HIPPOCRATIC LICENSE. It contains all modules except of the media module.
This means also its copyleft!
