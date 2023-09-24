# Makerspace API 

## Contributors
python version 3.10.6

# Big thanks
Mventory - check their repo out - most code from them
Person who's behind mventory - @proffalken

use ful links
- https://stackoverflow.com/questions/46053922/delete-method-on-django-rest-framework-modelviewset
- https://stackoverflow.com/questions/2845080/how-do-i-fix-this-django-error-exception-type-operationalerror-exception-value
- https://stackoverflow.com/questions/35760943/how-can-i-enable-cors-on-django-rest-framework
- https://mattermost.com/blog/user-authentication-with-the-django-rest-framework-and-angular/
- https://stackoverflow.com/questions/3052975/django-models-avoid-duplicates
- https://stackoverflow.com/questions/46805662/collections-ordereddict-object-has-no-attribute-pk-django-rest-framework
- https://simpleisbetterthancomplex.com/tutorial/2018/11/22/how-to-implement-token-authentication-using-django-rest-framework.html
- https://stackoverflow.com/questions/42091013/django-rest-framework-updating-a-model-using-model-modelviewset
- https://www.django-rest-framework.org/api-guide/filtering/
- https://stackoverflow.com/questions/43871604/valueerror-dependency-on-app-with-no-migrations-customuser
- https://stackoverflow.com/questions/33496333/valueerror-related-model-uapp-model-cannot-be-resolved
- https://stackoverflow.com/questions/40073205/django-core-exceptions-improperlyconfigured-could-not-resolve-url-for-hyperlink
- https://stackoverflow.com/questions/33496333/valueerror-related-model-uapp-model-cannot-be-resolved

# mile stones


# backup
- https://django-archive.readthedocs.io/en/latest/
- https://stackoverflow.com/questions/21049330/how-to-backup-a-django-db


https://www.reddit.com/r/django/comments/knznxb/difference_between_hosting_on_1270018000_and/

add to allowed hosts

# monty_makerspace

A flutter thingy by Eddie Tang 2025

## resources

https://stackoverflow.com/questions/69316963/flutter-web-access-development-server-from-another-device


## Run server

`python -m http.server 6969 --bind  192.168.86.111`

use `netstat -tuln | grep 8080` on linux to check if processes are running

or just run `netstat` and wait for something to start with `192.` etc then use that ip address without the :8080 ending or smth


If you're having trouble connecting to the HTTP server you started using `python -m http.server` with the `--bind 0.0.0.0` option, there could be a few reasons for the issue. Here are some steps you can take to troubleshoot and resolve the problem:

1. **Check Firewall Settings**: Ensure that your computer's firewall settings are not blocking incoming connections to the specified port (8080 in this case). You might need to create an exception in your firewall settings to allow traffic on that port.

2. **Check Antivirus or Security Software**: If you have antivirus or security software installed, it might be blocking incoming connections. Temporarily disabling the software or adding an exception for the Python executable could help.

3. **Confirm Server is Running**: Double-check that the Python HTTP server is running and has bound to the correct IP and port. When you run the command `python -m http.server 8080 --bind 0.0.0.0`, it should display a message like `Serving HTTP on 0.0.0.0 port 8080 ...`.

4. **Check IP and Port**: Make sure you're trying to access the server from the correct IP address and port. If you're accessing the server from the same machine, you can use `http://localhost:8080` in your web browser. If you're trying to access it from another device on the same network, you'll need to use the IP address of the machine running the server, followed by `:8080`.

5. **Network Configuration**: Ensure that your network configuration allows communication between devices on the same network. Devices on the same subnet should be able to communicate with each other.

6. **Other Processes on Port 8080**: Check if there are any other processes or applications using port 8080. You can use the `netstat` command to see if there's any conflict. Run `netstat -ano | findstr :8080` to check if the port is already in use.

7. **Python Version**: Ensure that you're using a compatible version of Python. The `http.server` module is available in Python 3.x. If you have both Python 2 and Python 3 installed, make sure you're using the correct command.

8. **Try a Different Port**: If you're still having trouble, try using a different port (e.g., 8000) to see if the issue persists. Sometimes certain ports might be restricted or blocked by the system.

9. **Restart the Server**: If all else fails, try stopping the server and then starting it again. This can sometimes resolve any issues that might have arisen during the initial setup.

10. **Check Web Browser**: If you're using a web browser to access the server, make sure the browser is functioning properly. You could try a different browser or clearing cache and cookies.

If you've tried these steps and are still unable to connect to the server, there might be more complex networking issues at play, and it could be helpful to seek assistance from someone familiar with your network setup.


# TODO:

- https://www.youtube.com/watch?v=VDIJ4GgKxR8
- https://github.com/nathan-osman/django-archive/issues/3
- https://docs.djangoproject.com/en/4.2/howto/initial-data/


- https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Generic_views
- https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Models