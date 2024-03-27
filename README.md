## pylptlib

Package to control the Keithley 4200A-SCS parameter analyzer with Python. 
It uses the Keithleys Linear Parametric Test Library (LPT) by wrapping the lptlib.dll using 
ctypes. The lptlib.dll is located on the parameter analyzer and will be automatically
found when running pylptlib on the instrument. The library supports the most common commands
for SMU and pulse units. CVU cards are not supported, yet.

pylptlib is a backend for the [SweepMe!](https://sweep-me.net) instrument drivers for the Keithley 4200-SCS.

The implementation is based on the documentation "4200A-LPT-907-01A_LPT_Dec_2020.pdf"

## Install
The package can be installed using "pip install 'path_to_package'".
Further, you need to install a 32 bit Python on the parameter analyzer 
as the lptlib.dll is 32 bit only.

### Example

``` python
    from pylptlib import lpt, param
    
    lpt.initialize()  # needed to load the dll
    lpt.devint()
    instr_id = lpt.getinstid("PMU1")
    lpt.rpm_config(instr_id, 1, param.KI_RPM_PATHWAY, param.KI_RPM_PULSE)
```

### Function names, arguments and return values
* All arguments are changed to lower case and have underscores in case an argument contained capital letters:
   * numSeq -> num_seq
   * SeqLoopCount -> seq_loop_count

* Functions with 'X' like forceX are wrapped as forcev or forcei.

* Pointer like arguments are  omitted if they can be automatically created.
Functions that are used to query values return the values of the buffer objects if possible.
Otherwise, None is returned.

``` python
    # pointer like argument '*result' is not used
    # function returns the current
    current = lpt.intgi(instr_id)
```

* For exact use of pylptlib, please have a look at the implementation in src\pylptlib\lpt.py

* Please have a look at the pdf documentation of the LPT library to understand the meaning of each argument.

### Remote control

#### Build the server executable
Create a local development environment. Run following commands in the directory of the repository.
Adjust the paths to your python installation as necessary, and make sure to use a 32bit python version.
```powershell
C:\Python39-32\python.exe -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Build the executable. Run following commands in the directory of the repository.
```powershell
.\.venv\Scripts\Activate.ps1
.\tools\Build-Server.ps1
```

The server executable can now be found in the `dist` directory. There is also a default config file called
`4200-Server.ini` that contains the local IP-Address and Port the server is listening at:


## Contact
Please email us at support@sweep-me.net for any queries. We can also add further functions on request.