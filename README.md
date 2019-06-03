# Item Catalog

An application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items. A requirement for Udacity's Fullstack Nanodegree Program.

## Getting Started

My operating system is a Mac so the installation instructions reflect this system. The code editor used was Atom. Most of the files and configurations were provided by Udacity.

### Installing Git

Git is already installed on MacOS, but these instructions are to ensure we have the latest version:

1. go to [https://git-scm.com/downloads](https://git-scm.com/downloads)
2. download the software for Mac
3. install Git choosing all the default options

Once everything is installed, you should be able to run `git` on the command line. If usage information is displayed, we're good to go!

### Configuring Mac's Terminal (OPTIONAL)

Git can be used without reconfiguring the terminal but doing so makes it easier to use.

To configure the terminal, perform the following:

1. download [udacity-terminal-config.zip](http://video.udacity-data.com.s3.amazonaws.com/topher/2017/March/58d31ce3_ud123-udacity-terminal-config/ud123-udacity-terminal-config.zip)
2. Move the `udacity-terminal-config` directory to the directory of your choice and name it `.udacity-terminal-config`(Note the dot in front)
3. Move the `bash-profile` to the same directory as in `step 2` and name it `.bash_profile`(Note the dot in front)
    * If you already have a `.bash_profile` file in your directory, transfer the content from the downloaded `bash_profile` to the existing `.bash_profile`

**Note:** It's considerably easier to just use
`mv bash_profile .bash_profile`
and `mv udacity-terminal-config .udacity-terminal-config`
when moving and renaming these files in order to avoid mac system errors

### First Time Git Configuration
Run each of the following lines on the command line to make sure everything is set up.
```
# sets up Git with your name
git config --global user.name "<Your-Full-Name>"

# sets up Git with your email
git config --global user.email "<your-email-address>"

# makes sure that Git output is colored
git config --global color.ui auto

# displays the original state in a conflict
git config --global merge.conflictstyle diff3

git config --list
```

### Git & Code Editor

The last step of configuration is to get Git working with your code editor. Below is the configuration for Atom. If you use a different editor, then do a quick search on Google for "associate X text editor with Git" (replace the X with the name of your code editor).
```
git config --global core.editor "atom --wait"
```

### Install Virtual Box

VirtualBox is the software that actually runs the virtual machine. Download it [here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1). Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.

### Install Vagrant

Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. Download it [here](https://www.vagrantup.com/downloads.html). Install the version for your operating system.

If vagrant is successfully installed, you will be able to run `vagrant --version` in the terminal to see the version number.

### Download VM configuration

Download [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip). This will give you a directory called **FSND-Virtual-Machine**.

Alternatively you can fork the repo [https://github.com/udacity/fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) on Github.

Change to this newly downloaded directory using `cd` in the terminal. Change to the `vagrant`
directory inside.

### Starting the Virtual Machine

From your terminal, inside the vagrant subdirectory, run the command `vagrant up`. Vagrant will download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.

When `vagrant up` is finished running, you will get your shell prompt back. At this point, you can run `vagrant ssh` to log in to your newly installed Linux VM!

### Logged In

If you are now looking at a shell prompt that starts with the word `vagrant` congratulations — you've gotten logged into your Linux VM.

## Version

This project uses `Python 3`

## Run catalog.py

With data loaded and with `catalog.py` in the `vagrant/catalog` directory, run:

```
python catalog.py
```

or, if this doesn't work:

```
python3 catalog.py
```

### Visit localhost:8000

With the application running, visit `http://localhost:8000` on your favorite browser to test out the app.

## Exit the App

To exit the app, on your keyboard press `control + c`.

## Exit Vagrant

To exit vagrant, on your keyboard press `control + d`.

## Author(s)

* **Roy Telles, Jr.** *(with the help of the Udacity team)*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* I would like to acknowledge and give big thanks to Udacity and team for this excellent resume-building experience
