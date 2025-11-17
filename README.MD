Multithreaded python script to turn on/off Uniview cameras intelegent detection.

Reason: I have a lot of Uniview cameras that have "intellegent" motion/intrusion detection but no easy way to switch it off or on.
It's annoying when camera flashes everytime someone is outside.
So here is the solution:

Setup "intelligent" detection rule on cameras.
Add script to home assistant and you have a pretty button to switch detection off or on.


If debug output is needed ala how many cameras have detection on/off change yml:
python3 /config/scripts/cctv/unv_nvr.py status -> python3 /config/scripts/cctv/unv_nvr.py status debug


