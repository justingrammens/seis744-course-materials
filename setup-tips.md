## Issues Setting up PiSense on OSX

As I tried to get the PiSense setup on OSX, there were a few things that I needed to do.

When installing [PiSense](https://pisense.readthedocs.io/en/release-0.2/)

Make sure that you follow the installation carefully for the [emulator](https://sense-emu.readthedocs.io/en/v1.1/)

You need to make sure you have brew installed correctly and it only worked when I created the virtual environment using the --system-site-packages flag.

python3 -m venv virtualenv --system-site-packages

Also make sure you

have pip itself is current

`python -m pip install --upgrade pip`

install the missing runtime

`pip install setuptools`

Install the sense-emu with

`pip install sense-emu`

### Two Other Fixes You Need To Apply

### Change anim.py

[Update By Author](https://github.com/programming-the-iot/book-exercise-tasks/issues/50)

From what I understand, the ImageDraw library in 3.10 has deprecated the textsize function, although in my own testing, it appears you can use textbbox instead. Since the version of pisense I tested with relies on textsize, there are at least two potential ways to address this issue.
(1) You can either downgrade your Python (and Pillow) implementation (not recommended due to a CVE concern - see https://pillow.readthedocs.io/en/stable/releasenotes/10.0.1.html), or
(2) make a minor adjustment to the pisense anim.py module's source code, as shown below.
How to update pisense anim.py source code module:
In the pisense module anim.py, you can change line 167 as follows (you'll find this under {your python install location}/lib/python3.10/site-packages/pisense/anim.py):
```
line     code
-----   -----
167:   #width, height = draw.textsize(text, f, spacing=1)
168:    x, y, width, height = draw.textbbox((0,0), text, f)
```

### Change gui.py

If you get this following error when runnning

```
sense_emu_gui
```

```
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/threading.py", line 1043, in _bootstrap_inner
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/threading.py", line 994, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/justingrammens/dev/justingrammens/programming-the-iot/pisensevenv/lib/python3.13/site-packages/sense_emu/gui.py", line 430, in _update_run
    GLib.Bytes.new(self._screen_client.rgb_array.tostring()),
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'numpy.ndarray' object has no attribute 'tostring'
```

You need to modify the sense_emu/gui.py file within your virtual environment (or a local override, similar to the pisense fix).
Locate the file:
The error message gives you the exact path:
{$VIRTUAL_ENV}/lib/python3.13/site-packages/sense_emu/gui.py

Open gui.py for editing.
Go to line 430.

You'll see a line similar to this:

```
GLib.Bytes.new(self._screen_client.rgb_array.tostring()),
```

Change tostring() to tobytes():
Modify the line to:

```
GLib.Bytes.new(self._screen_client.rgb_array.tobytes()),
```

--

Setting up the Python Interpreter, you'll want to make sure you have the path directory to the piotvenv virtual envionment  you have setup, otherwise it will not have access to the libraries you have installed in that enviornment. So for example:

Follow these steps:

Step-by-Step to Add the venv Interpreter Properly

Preferences ▸ PyDev ▸ Interpreters ▸ Python Interpreter
Click New...

For Interpreter Name, enter something like:

piotvenv

For Interpreter Executable, click “Browse…” and paste in the path. For example for me it reads:

```
${HOME_DIRECTORY}/programming-the-iot/piotvenv$/bin/python
```

( this is your virtual environment's Python wrapper, even if it links to the system Python internally)

Click OK — even if it gives the warning:

"An interpreter is already configured with the path..."

BTW - You can ignore this warning if you're sure you selected the path from your venv.

PyDev should now treat this as a separate interpreter, even though it points to the same base binary.
