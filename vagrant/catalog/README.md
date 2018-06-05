# UDC Item Catalog

This is the Item Catalog project. the fourth from Udacity's full stack web developer nanodegree program.  

The objective of this project is to write a web application that provides a list of items within a variety of fixed categories as well as provider a user registration and authentication system through a third party provider.  The registered users will have the ability to post, edit, and delete their own items.  

This web application accomplishes all of these tasks, using the google oauth2 api in order to setup the authentication of users.  

In order to use the web application, the user must first setup a vagrant machine, download some libraries, and run some files provided in the project repository.


## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You will need to install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
pick the platform package for your respective operating system.

You will then need to install [Vagrant](https://www.vagrantup.com/downloads.html)
which is software that configures a virtual Machine

In the project repository, you will see a file named Vagrantfile.  Please do not alter it, as the file correctly configures the virtual machine as is.

You will also need to make sure you are running these setup commands and the python project in bash.


### Installing

You should first navigate to the catalog directory.  You can do this by entering the fullstack-nanodegree-vm directory you downloaded, by typing in  
```
cd fullstack-nanodegree-vm
```
and pressing enter.  Then you should navigate to the catalog directory by typing in
```
cd catalog
```

When you are in this directory, you should type in the terminal
```
vagrant up
```



After your Vagrant machine finishes the download that started from calling Vagrant up in the catalog directory you installed,
you should type



```
vagrant ssh
```


and press enter in the bash terminal.  After you get into the virtual environment, type

```
cd /vagrant
```


and enter.  Then type
```
cd catalog
```


and press enter. Before setting up the database, there are three directories that you need to install, in order for the project to run smooth on your machine.  Now that you are in vagrant's version of the project directory, you can install the required packages. Type in


```
pip install werkzeug==0.8.3 --user
pip install flask==0.9 --user
pip install Flask-Login==0.1.3 --user
```


and hitting enter after each --user.  The --user at the end is neccessary because otherwise you would use sudo, and there can be issues with using sudo and vagrant on some machines.  


Therefore, I think --user is easier, but you can accomplish the same goal with sudo pip install.  Now you are ready to setup the initial database for the application.


Make sure you are still in the vagrant's version of the project directory.  When you are, type
```
python database_setup.py
```
and press enter to setup the data structures in the database.  Next you should type
```
python catalogitems.py
```
and press enter to populate the database.  You should see the message "added catalog items!" in your vagrant terminal after you run this file.  

If you do not, then it did not get called properly. Now that your database is setup, you can run the application by typing in your vagrant terminal.
```
python main.py
```
Once you press enter, you should see on the vagrant terminal a response
"* Running on http://0.0.0:8000/"
"* Restarting with reloader".
 This means that you have successfully launched the application.  Open up a web browser and type in the search bar
```
http://localhost:8000/
```
and click around.  Note that you can only add, edit, and delete items that you add.  
You must be logged into a google account in order to accomplish any other interact with the category items besides reading them.


## JSON API Endpoints

If you type in
```
http://localhost:8000/catalogs/JSON

```
to your web browser, you will get a list of JSON objects, representing all the data in the Category table.

If you type in
```
http://localhost:8000/catalog/itemname/JSON
```
into your web browser, and replace itemname with the name of a Category item, it will return a JSON object with the serializable parts of the CategoryItem database.

### And coding style tests

The python code follows PEP8 Standards.



## Built With

* [Vagrant](https://www.vagrantup.com/) - Virtual Machine to run linux on
* [Sqlite](https://www.sqlite.org/index.html) - Open Source Relational Database
* [Python](https://www.python.org/) - Programming Language (Version 2.7)

## Contributing

There are no plans to accept contributions at this time.

## Authors

* **Trevor Thomas**


## License

This project is not under any license.
